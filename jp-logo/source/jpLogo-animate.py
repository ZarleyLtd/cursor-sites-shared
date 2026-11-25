"""Generate the JP logo animation from the logo's geometry.

Run:  python jp-logo/source/jpLogo-animate.py [--svg-only]
Writes
  jp-logo/jpLogo-animated.svg            the app copy (scripted, currentColor), synced by sync-ui.ps1
  jp-logo/source/jpLogo-standalone.svg   plays once on load, click replays (white); for <img> or sharing
  jp-logo/source/jpLogo-animated.gif     loops; on #1d2026 (GIF has no soft transparency)
  jp-logo/source/jpLogo-animated.webp    loops; transparent
--svg-only skips the slow GIF/WebP render. See jp-logo/JP_LOGO.md.

Local units: stroke width 1, shared stem centreline at x=0, top of stem at y=0 (upright "JP").
The final transform reproduces jpLogo-white-rotated-2000.png (2000 x 1186).
"""
import math, sys, os
from PIL import Image, ImageDraw, ImageChops

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(SRC_DIR)

# ---- fitted geometry ----
# Fitted with the joints constrained so the parts meet exactly: the bowl and the hook sit
# flush with the stem's edges, the hook is one stroke thick, and the stem ends on the hook's
# centre line. That keeps the V notch at the top of the final logo clean.
W_PX, TH_F, TX, TY = 299.544, 226.3475, 264.0625, 1077.7188
SW = 1.0
PCX, PCY, PRI, PRO = SW / 2, 1.9069, 0.932, 1.9147      # P bowl (right half-ring)
JCY, JRI = 3.8998, 0.9656                               # J hook (bottom half-ring)
JRO = JRI + SW
JCX = SW / 2 - JRO
L = JCY                                                  # shared stem: top 0 to hook centre line
BOTTOM = JCY + JRO                                       # foot of the J = foot of the full P
CW, CH = 2000, 1186

# ---- timeline (seconds) ----
T_FADE, T_SLIDE0, T_SLIDE1 = 0.5, 0.5, 1.5
T_TAIL0, T_TAIL1 = 1.6, 2.1     # the P's lower stem dissolves once the letters have merged
T_ROT0, T_ROT1, T_END = 2.2, 3.6, 5.6
SEP = 2.5                       # how far each letter starts from the merged position (units)
S0 = 165.0                      # upright scale (px per unit)
C_LOCAL = ((JCX - JRO + PCX + PRO) / 2, BOTTOM / 2)    # centre of the upright JP: the pivot
TH_END = TH_F - 360             # -133.9: rotate the short way (anticlockwise)
SPLINE = (0.65, 0, 0.35, 1)     # ease-in-out, shared by SVG keySplines and the raster frames

def rot(th, x, y):
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return c * x - s * y, s * x + c * y

rx, ry = rot(TH_F, C_LOCAL[0] * W_PX, C_LOCAL[1] * W_PX)
C0 = (CW / 2, CH / 2)
CF = (TX + rx, TY + ry)

def bezier_ease(t, p=SPLINE):
    x1, y1, x2, y2 = p
    lo, hi = 0.0, 1.0
    for _ in range(40):
        m = (lo + hi) / 2
        x = 3 * (1 - m) ** 2 * m * x1 + 3 * (1 - m) * m * m * x2 + m ** 3
        lo, hi = (m, hi) if x < t else (lo, m)
    m = (lo + hi) / 2
    return 3 * (1 - m) ** 2 * m * y1 + 3 * (1 - m) * m * m * y2 + m ** 3

def phase(t, a, b):
    return 0.0 if t <= a else 1.0 if t >= b else bezier_ease((t - a) / (b - a))

# ---- shapes as polygons in local units ----
def arc(cx, cy, r, a0, a1, n=64):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

STEM = [(-SW / 2, 0), (SW / 2, 0), (SW / 2, L), (-SW / 2, L)]
BOWL = arc(PCX, PCY, PRO, -90, 90) + arc(PCX, PCY, PRI, 90, -90)
HOOK = arc(JCX, JCY, JRO, 0, 180) + arc(JCX, JCY, JRI, 180, 0)
TAIL_E = 0.05   # overlap the tail onto the stem so no hairline seam shows
TAIL = [(-SW / 2, L - TAIL_E), (SW / 2, L - TAIL_E), (SW / 2, BOTTOM), (-SW / 2, BOTTOM)]
LETTER_J = [STEM, HOOK]
LETTER_P = [STEM, BOWL]          # plus TAIL, drawn separately so it can dissolve

def state(t):
    k = phase(t, T_SLIDE0, T_SLIDE1)
    r = phase(t, T_ROT0, T_ROT1)
    th = TH_END * r
    cx, cy = C0[0] + (CF[0] - C0[0]) * r, C0[1] + (CF[1] - C0[1]) * r
    s = S0 + (W_PX - S0) * r
    if r > 0:
        s = min(s, cap_from(t))   # never spill outside the frame mid-turn, and never shrink
    return dict(op=min(1.0, t / T_FADE), jdx=-SEP * (1 - k), pdx=SEP * (1 - k),
                tail=1 - phase(t, T_TAIL0, T_TAIL1), th=th, s=s, cx=cx, cy=cy)

ALL_PTS = [p for poly in LETTER_J + LETTER_P for p in poly]

def fit_scale(th, cx, cy):
    best = 1e9
    for x, y in ALL_PTS:
        ax, ay = rot(th, x - C_LOCAL[0], y - C_LOCAL[1])
        if ax > 1e-9: best = min(best, (CW - cx) / ax)
        if ax < -1e-9: best = min(best, cx / -ax)
        if ay > 1e-9: best = min(best, (CH - cy) / ay)
        if ay < -1e-9: best = min(best, cy / -ay)
    return best

def raw_cap(t):
    r = phase(t, T_ROT0, T_ROT1)
    return fit_scale(TH_END * r, C0[0] + (CF[0] - C0[0]) * r, C0[1] + (CF[1] - C0[1]) * r) * FIT_ADJ

_CAP_T = [T_ROT0 + (T_ROT1 - T_ROT0) * i / 400 for i in range(401)]
_CAP = None
def cap_from(t):
    """Smallest cap from t to the end of the turn, so the scale only ever grows."""
    global _CAP
    if _CAP is None:
        caps = [raw_cap(x) for x in _CAP_T]
        for i in range(len(caps) - 2, -1, -1):
            caps[i] = min(caps[i], caps[i + 1])
        _CAP = caps
    i = min(len(_CAP) - 1, max(0, int((t - T_ROT0) / (T_ROT1 - T_ROT0) * 400)))
    return _CAP[i]

FIT_ADJ = max(1.0, W_PX / fit_scale(TH_END, *CF))   # the PNG crops a hair tight; keep the exact end size

def to_px(st, dx, x, y):
    x, y = x + dx - C_LOCAL[0], y - C_LOCAL[1]
    px, py = rot(st['th'], x * st['s'], y * st['s'])
    return st['cx'] + px, st['cy'] + py

# ---- raster frames ----
def frame(t, w, bg, ss=3):
    sc = w * ss / CW
    h = round(CH * w / CW)
    st = state(t)
    def poly_px(dx, poly):
        return [(x * sc, y * sc) for x, y in (to_px(st, dx, *p) for p in poly)]
    mask = Image.new('L', (w * ss, h * ss), 0)
    d = ImageDraw.Draw(mask)
    for dx, polys in ((st['jdx'], LETTER_J), (st['pdx'], LETTER_P)):
        for poly in polys:
            d.polygon(poly_px(dx, poly), fill=255)
    if st['tail'] > 0:
        tail = Image.new('L', mask.size, 0)
        ImageDraw.Draw(tail).polygon(poly_px(st['pdx'], TAIL), fill=round(255 * st['tail']))
        mask = ImageChops.lighter(mask, tail)
    mask = mask.resize((w, h), Image.LANCZOS).point(lambda v: round(v * st['op']))
    img = Image.new('RGBA', (w, h), bg)
    img.paste((255, 255, 255, 255), (0, 0), mask)
    return img

def write_raster(fps=30, w=480):
    n = round(T_END * fps)
    dur = round(1000 / fps)
    hold = round((T_END - T_ROT1) * 1000)
    ts = [i / fps for i in range(n) if i / fps <= T_ROT1] + [T_END]
    durs = [dur] * (len(ts) - 1) + [hold]
    # GIF on Stomper's footer panel colour (GIF has no soft transparency)
    g = [frame(t, w, (0x1d, 0x20, 0x26, 255)).convert('RGB') for t in ts]
    g[0].save(os.path.join(SRC_DIR, 'jpLogo-animated.gif'), save_all=True, append_images=g[1:],
              duration=durs, loop=0, optimize=True)
    # WebP with real alpha
    wp = [frame(t, w, (255, 255, 255, 0)) for t in ts]
    wp[0].save(os.path.join(SRC_DIR, 'jpLogo-animated.webp'), save_all=True, append_images=wp[1:],
               duration=durs, loop=0, lossless=False, quality=90, method=6)

# ---- SVG (SMIL; plays once and holds; works in <img>) ----
def f(v): return f'{v:.4f}'.rstrip('0').rstrip('.')

def svg_path_bowl():
    e = 0.05   # tuck the flat ends into the stem so no hairline seam shows
    return (f'M{f(PCX-e)} {f(PCY-PRO)}H{f(PCX)}A{f(PRO)} {f(PRO)} 0 0 1 {f(PCX)} {f(PCY+PRO)}'
            f'H{f(PCX-e)}V{f(PCY+PRI)}H{f(PCX)}A{f(PRI)} {f(PRI)} 0 0 0 {f(PCX)} {f(PCY-PRI)}H{f(PCX-e)}Z')

def svg_path_hook():
    e = 0.05
    return (f'M{f(JCX+JRO)} {f(JCY-e)}V{f(JCY)}A{f(JRO)} {f(JRO)} 0 0 1 {f(JCX-JRO)} {f(JCY)}'
            f'H{f(JCX-JRI)}A{f(JRI)} {f(JRI)} 0 0 0 {f(JCX+JRI)} {f(JCY)}V{f(JCY-e)}Z')

def write_svg(path, scripted=False):
    """Standalone: plays once on load, click replays. Scripted: no click trigger or id; the page
    drives it with pauseAnimations() / setCurrentTime() (0 to T_ROT1 seconds)."""
    stem = f'M{f(-SW/2)} 0H{f(SW/2)}V{f(L)}H{f(-SW/2)}Z'
    kt = lambda *ts: ';'.join(f(t / T_ROT1) for t in ts)
    spl = ' '.join(f(v) for v in SPLINE)
    begin = '0s' if scripted else '0s;jp.click'
    common = f'dur="{f(T_ROT1)}s" begin="{begin}" fill="freeze" calcMode="spline"'
    # outer transform sampled at 60 fps through the turn (scale follows the fit cap)
    n = round((T_ROT1 - T_ROT0) * 60)
    samples = [T_ROT0 + (T_ROT1 - T_ROT0) * i / n for i in range(n + 1)]
    sts = [state(t) for t in samples]
    key_times = kt(0, *samples)
    lin = f'dur="{f(T_ROT1)}s" begin="{begin}" fill="freeze" calcMode="linear"'
    def anim(type_, key, additive):
        vals = [key(state(0))] + [key(st) for st in sts]
        return (f'<animateTransform attributeName="transform" type="{type_}" additive="{additive}" '
                f'values="{";".join(vals)}" keyTimes="{key_times}" {lin}/>')
    def slide(dx):
        return (f'<animateTransform attributeName="transform" type="translate" '
                f'values="{f(dx)} 0;{f(dx)} 0;0 0;0 0" keyTimes="{kt(0, T_SLIDE0, T_SLIDE1, T_ROT1)}" '
                f'keySplines="0 0 1 1;{spl};0 0 1 1" {common}/>')
    fade = (f'<animate attributeName="opacity" values="0;1;1" keyTimes="{kt(0, T_FADE, T_ROT1)}" '
            f'dur="{f(T_ROT1)}s" begin="{begin}" fill="freeze"/>')
    tail_fade = (f'<animate attributeName="opacity" values="1;1;0;0" '
                 f'keyTimes="{kt(0, T_TAIL0, T_TAIL1, T_ROT1)}" keySplines="0 0 1 1;{spl};0 0 1 1" {common}/>')
    tail = f'M{f(-SW/2)} {f(L-TAIL_E)}H{f(SW/2)}V{f(BOTTOM)}H{f(-SW/2)}Z'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}"{' aria-hidden="true" focusable="false"' if scripted else ''}>
{'' if scripted else '<title>JP</title>'}
<g{'' if scripted else ' id="jp"'} fill="{'currentColor' if scripted else '#fff'}"{'' if scripted else ' style="cursor:pointer"'}>
{fade}
<g transform="translate({f(CF[0])} {f(CF[1])}) rotate({f(TH_F)}) scale({f(W_PX)})">
{anim("translate", lambda st: f"{f(st['cx'])} {f(st['cy'])}", "replace")}
{anim("rotate", lambda st: f(st['th']), "sum")}
{anim("scale", lambda st: f(st['s']), "sum")}
<g transform="translate({f(-C_LOCAL[0])} {f(-C_LOCAL[1])})">
<g>{slide(-SEP)}<path d="{stem}"/><path d="{svg_path_hook()}"/></g>
<g>{slide(SEP)}<path d="{stem}"/><path d="{svg_path_bowl()}"/><path d="{tail}" opacity="0">{tail_fade}</path></g>
</g>
</g>
</g>
</svg>
'''
    open(path, 'w', encoding='utf-8', newline='\n').write(svg)

write_svg(os.path.join(SRC_DIR, 'jpLogo-standalone.svg'))
write_svg(os.path.join(APP_DIR, 'jpLogo-animated.svg'), scripted=True)
if '--svg-only' not in sys.argv:
    write_raster()
