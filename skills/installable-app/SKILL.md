---
name: installable-app
description: Make a static CursorSites project an "Edison-style installable app", so that Chrome on Android offers Install and adds a home-screen icon. Use when the user asks for an Edison-style installable app, an installable app, add to home screen, a PWA, a web app manifest, a service worker for offline use, or a home-screen icon like Edison's, in any app under C:\CursorSites.
---

# Edison-style installable app

Read `cursor-sites-shared/installable-app/INSTALLABLE_APP.md` and follow it. That file is the canonical spec.

Edison is the reference implementation. In `Edison`, look at:

- `manifest.json`
- `sw.js`
- the `<head>` links on each page
- the service worker registration in `assets/js/main.js`

FamilyTree and PubliiCrossguns also implement this pattern.

## Add these

1. **Icons.** Create `assets/icons/icon.svg`, `icon-192.png` and `icon-512.png` from the project's own mark. Give the SVG a full-bleed background in the page colour. Keep the mark centred with padding, so a circular or squircle crop doesn't clip it.
2. **Manifest.** Add a root `manifest.json` with:
   - `name` and `short_name`
   - `start_url` set to `./index.html`, `scope` set to `./`, `display` set to `standalone`
   - `background_color` and `theme_color` from the project
   - icons: 192 (`purpose` `any`) and 512 (`purpose` `any maskable`)
3. **Service worker.** Add a root `sw.js` that precaches the app shell. It should be network-first for same-origin GET requests and fall back to the cache when offline. Ignore other origins. Bump the cache name (for example `<app>-shell-v2`) whenever the shell list changes. That includes adding a JS or CSS file to a page.
4. **Page head.** On every production page, add `theme-color`, the SVG icon, `apple-touch-icon` and `<link rel="manifest" href="manifest.json" />`. Skip mockups.
5. **Registration.** Register `sw.js` from the script that runs on those pages. Skip registration when `location.protocol` is `file:`.

## Rules

- Use relative paths only. Never put `http://localhost` or a drive letter in markup, the manifest or the worker.
- Leave out a custom Install button unless the user asks for one.
- If the page has a Content-Security-Policy, `script-src 'self'` or `worker-src 'self'` must allow `sw.js`.

## Verify

1. Open Chrome DevTools → Application → Manifest. The icons should load and the installability panel should show no errors.
2. Open Application → Service Workers. `sw.js` should be activated.
