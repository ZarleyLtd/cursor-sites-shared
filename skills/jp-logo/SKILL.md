---
name: jp-logo
description: Add, move, restyle or change the owner's JP logo (the merged J and P symbol, usually a "Created by" credit in the footer, which replays its J-and-P animation when tapped) in any app under C:\CursorSites. Use when the user asks to add the JP logo, my logo, the logo, the "Created by" credit or footer credit to an app, to make the logo animate, change its colour or size, or to change the logo animation itself.
---

# JP logo (CursorSites)

The owner's logo: a J and a P merged into one symbol, shown as a small "Created by" credit, usually in the footer. It's a button. Tapping it plays an animation that takes the logo apart into an upright J and P and back again. Stomper is the reference app.

**Canonical spec:** `cursor-sites-shared/jp-logo/JP_LOGO.md`. Read it before starting; it has the file list, theming variables and the full steps.

## Files (canonical: `cursor-sites-shared/jp-logo/`, synced by `scripts/sync-ui.ps1`)

| Canonical | App copy |
|---|---|
| `jpLogo-white-rotated-2000.png` (static, white) | `assets/icons/jpLogo-white-rotated-2000.png` |
| `jpLogo-animated.svg` (script-driven, `currentColor`) | `assets/icons/jpLogo-animated.svg` |
| `jp-logo.js` | `assets/js/components/jp-logo.js` |
| `jp-logo.css` | `assets/css/jp-logo.css` |

`jp-logo/source/` holds the generator (`jpLogo-animate.py`) and the self-playing extras: a standalone SVG, a GIF and a WebP. Those are for sharing and email, not for the app button.

## Adding it to an app ("add the JP logo to the footer of X")

1. Pull the app repo. Add the app to `$jpLogoTargets` in `cursor-sites-shared/scripts/sync-ui.ps1` and run `powershell -ExecutionPolicy Bypass -File cursor-sites-shared\scripts\sync-ui.ps1`.
2. Add `@import url('jp-logo.css');` to the app's main stylesheet.
3. Load `assets/js/components/jp-logo.js` with the other component scripts on each page that shows the logo.
4. Add the markup where the logo goes, normally the footer:
   ```html
   Created by <button type="button" class="jp-logo" aria-label="JP logo: tap to replay its animation"><img src="assets/icons/jpLogo-white-rotated-2000.png" alt="JP"></button>
   ```
   If the footer lives in `components/footer.html`, edit that first, then paste the change into every page. If the app has no footer, add a small one that fits the app's style, and ask if its placement isn't obvious.
5. Match the background. On a dark footer the default white is right. On a light one, add `jp-logo--dark` to the button or set `--jp-logo-color`. Use `--jp-logo-height` (default 22 px) and `--jp-logo-focus` to fit the app.
6. If the app has `sw.js`: add the PNG, the SVG, `jp-logo.js` and `jp-logo.css` to the shell list and bump the cache name.
7. If the app has contextual help and the footer is a help target, mention the tap-to-replay in its help entry.
8. Check it renders: serve the app (see the shared `CLAUDE.md`) and look at the footer. Then commit in the app repo, and in `cursor-sites-shared` for the target list change.

## Changing the logo or animation

Edit `jp-logo/source/jpLogo-animate.py` and run `python jp-logo/source/jpLogo-animate.py` (add `--svg-only` to skip the slow GIF/WebP). If the timeline length changes, update `DUR` in `jp-logo.js`. Then run `sync-ui.ps1` and commit in every target app, bumping their `sw.js` caches. Details are in the spec.

## Do not

- Edit an app's copy of the synced files. Edit `cursor-sites-shared/jp-logo/` and sync.
- Redraw, trace or approximate the logo. Use the shared files.
- Use the standalone SVG, the GIF or the WebP for the button, or point an `<img>` at `jpLogo-animated.svg`.
- Add wording beyond "Created by" unless the user asks.
