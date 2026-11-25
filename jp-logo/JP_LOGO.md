# JP logo (CursorSites)

The owner's JP logo, a J and a P merged into one symbol and turned 226°, shown as a small "Created by" credit, usually in the footer. Tapping the logo plays an animation: it comes apart into an upright J and P, then slides back together and turns into the logo again. Stomper is the reference app.

## Files

Everything canonical lives in `cursor-sites-shared/jp-logo/`. `scripts/sync-ui.ps1` copies the files marked "synced" into each app in `$jpLogoTargets`.

| File | Synced to | What it is |
|---|---|---|
| `jpLogo-white-rotated-2000.png` | `assets/icons/` | Static logo, white on transparent, 2000 × 1186. The fallback inside the button, and usable on its own anywhere. |
| `jpLogo-animated.svg` | `assets/icons/` | The animation, driven by `jp-logo.js`. It does not play by itself. It is drawn in `currentColor`, so it follows `--jp-logo-color`. |
| `jp-logo.js` | `assets/js/components/` | Wires up every `.jp-logo` button. |
| `jp-logo.css` | `assets/css/` | Button and size styles, themed with CSS variables. |
| `source/jpLogo-animate.py` | — | Generator for every animated file. Change the animation here. |
| `source/jpLogo-standalone.svg` | — | Self-playing white SVG: plays once on load and holds, and replays on click when the SVG is inline. For `<img>` tags, sharing, or places without the script. |
| `source/jpLogo-animated.gif` / `.webp` | — | Looping versions (480 px wide) for places where SVG doesn't work, such as email and chat. The GIF is on `#1d2026`, because GIF has no soft transparency; the WebP is transparent. |

## Markup

```html
<button type="button" class="jp-logo" aria-label="JP logo: tap to replay its animation">
  <img src="assets/icons/jpLogo-white-rotated-2000.png" alt="JP">
</button>
```

A footer credit is usually `Created by <button class="jp-logo" …>…</button>`. Match the footer's existing text style and don't add other wording unless asked.

- Load `jp-logo.js` with the other components (config → utils → components → pages → main.js). It wires up every `.jp-logo` once the DOM is ready.
- For markup added after load (a footer rendered by script), call `JpLogo.init(containerEl)`.
- On a page that isn't at the site root, set `data-src` on the button to the SVG's relative path, and fix the `<img src>` path too.

## Behaviour

- On load, `jp-logo.js` fetches the SVG, puts it into the button paused on the finished logo, and swaps out the PNG. If the fetch fails (offline before caching, or opened over `file://`), the PNG stays and the button does nothing.
- A tap plays the 3.6 s timeline backwards and then forwards at 1.5× speed: 2.4 s each way, 4.8 s in all. Taps during playback are ignored. It always ends on the logo.
- Users with reduced motion turned on (`prefers-reduced-motion: reduce`) get no animation.
- In apps with contextual help, a tap while help mode is on shows the help instead, because help captures the tap first.

## Theming

Set these on `.jp-logo` or any ancestor, such as `.footer`:

| Variable | Default | Notes |
|---|---|---|
| `--jp-logo-color` | `#fff` | Colour of the animated SVG. The PNG fallback is always white. |
| `--jp-logo-height` | `22px` | Width follows the 2000 × 1186 shape (37 px at 22 px high). |
| `--jp-logo-focus` | `currentColor` | Keyboard focus outline. Stomper uses its accent colour. |

On a light background, add `jp-logo--dark` to the button. That makes the SVG black and inverts the PNG fallback to match.

## Adding it to an app

1. Add the app to `$jpLogoTargets` in `scripts/sync-ui.ps1`, then run `powershell -ExecutionPolicy Bypass -File cursor-sites-shared\scripts\sync-ui.ps1`.
2. Add `@import url('jp-logo.css');` to the top of the app's main stylesheet, beside the other synced imports.
3. Add `<script src="assets/js/components/jp-logo.js"></script>` with the other component scripts on every page that shows the logo.
4. Add the button where the logo goes. When the app's footer lives in `components/footer.html`, edit that first, then paste the change into every page, as the shared conventions require. If the app has no footer, add a small one styled like the rest of the app, and ask first if it's unclear where it belongs.
5. Set the colour for the background (`--jp-logo-color` or `jp-logo--dark`) and, if needed, `--jp-logo-height`.
6. If the app has `sw.js`, add the PNG, the SVG, `jp-logo.js` and `jp-logo.css` to the shell list and bump the cache name. (Splitify uses its asset-version cache-bust instead.)
7. If the app has a contextual-help catalog and the footer is a help target, mention in its entry that tapping the logo replays it.

## Changing the logo or animation

1. Edit `source/jpLogo-animate.py`: timing (`T_*`), how far apart the letters start (`SEP`), sizes, or the geometry constants.
2. Run `python jp-logo/source/jpLogo-animate.py`, or add `--svg-only` to skip the slow GIF/WebP render. It rewrites `jpLogo-animated.svg` and everything in `source/`.
3. If the timeline length changed, update `DUR` in `jp-logo.js` to the new `T_ROT1`.
4. Run `sync-ui.ps1` and commit in each target app (bump `sw.js` caches).

How the geometry works: in upright units (stroke width = 1, stem centreline at x = 0, stem top at y = 0), the logo is a stem, a half-ring bowl on the right (the P) and a half-ring hook below on the left (the J). The bowl and hook sit flush with the stem's edges, so the V notch at the top of the turned logo stays clean. The numbers were fitted to the original PNG. The final transform (`W_PX`, `TH_F`, `TX`, `TY`) maps them onto the PNG's 2000 × 1186 frame, so the animation ends exactly on the static logo. The J's curve is about 2–4% bigger than the P's, as in the original drawing; keep it that way.

## Do not

- Edit an app's copy of these files. Edit `cursor-sites-shared/jp-logo/` and sync.
- Use the standalone SVG, the GIF or the WebP for the footer button. They play by themselves and fight the script.
- Point an `<img>` at `jpLogo-animated.svg`. Without the script it shows only the finished logo, and it can't be tinted.
- Redraw or approximate the logo by hand. Use these files.
