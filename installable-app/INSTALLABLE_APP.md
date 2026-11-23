# Edison-style installable app

Make a static CursorSites site installable on a phone. On Android Chrome (including a Pixel), the browser offers **Install**. Accepting it adds a home-screen icon and opens the site without the address bar.

Say **“make this an Edison-style installable app”** to mean: follow this spec. The reference implementation is the Edison repo: `manifest.json`, `sw.js`, the `<head>` links on each page, and the registration in `assets/js/main.js`.

This is a normal progressive web app. There is no store listing and no custom Install button. Chrome shows Install when the published HTTPS site has a manifest and a service worker that handles `fetch`.

## What to add

1. Icons under `assets/icons/`.
2. `manifest.json` at the site root.
3. `sw.js` at the site root.
4. The same `<head>` links on every production HTML page.
5. A service-worker registration in the script that runs on those pages.

Skip mockups and any page that is not part of the installed app.

## Icons

| File | Role |
|------|------|
| `assets/icons/icon.svg` | Browser tab icon. Use the project’s own mark. |
| `assets/icons/icon-192.png` | Manifest icon, `purpose: "any"`. Also the Apple touch icon. |
| `assets/icons/icon-512.png` | Manifest icon, `purpose: "any maskable"`. |

Give the SVG a full-bleed background in the project’s page colour and keep the mark inside the centre, with padding, so Android’s circle or squircle crop does not clip it. Export the two PNGs from that SVG. Use relative paths only.

## Manifest

`manifest.json` at the site root:

```json
{
  "name": "Site Name",
  "short_name": "Site",
  "description": "One line about the site.",
  "start_url": "./index.html",
  "scope": "./",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#111111",
  "icons": [
    {
      "src": "assets/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "assets/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

- `name` is the label under the icon. `short_name` is the shorter fallback.
- `start_url` is the page the icon opens. `scope` is `./` so the whole site stays inside the installed app.
- `display` must be `standalone` (or `fullscreen` or `minimal-ui`). `standalone` is the Edison choice: no browser chrome.
- `background_color` shows behind the icon and on the splash. `theme_color` tints the Android status bar. Set both to this project’s colours.

## Head tags

Put these in every production page’s `<head>`. Match colours to the manifest.

```html
<meta name="theme-color" content="#111111" />
<link rel="icon" href="assets/icons/icon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="assets/icons/icon-192.png" />
<link rel="manifest" href="manifest.json" />
```

Adjust the `href` values when the page is not at the site root (`../assets/icons/icon.svg`, and so on). `apple-touch-icon` is the icon iPhone uses for Add to Home Screen. iPhone does not show Chrome’s Install prompt.

If the page has a Content-Security-Policy, `script-src 'self'` (or `worker-src 'self'`) must allow `sw.js`.

## Service worker

`sw.js` at the site root. Edison’s worker precaches the app shell, then uses network-first for same-origin GET requests and falls back to the cache when the network fails.

```js
var CACHE = 'site-shell-v1';
var SHELL = [
  './',
  './index.html',
  './manifest.json',
  './assets/css/style.css',
  './assets/icons/icon.svg',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png',
  './assets/js/main.js'
];

self.addEventListener('install', function (event) {
  event.waitUntil(caches.open(CACHE).then(function (cache) {
    return cache.addAll(SHELL);
  }));
  self.skipWaiting();
});

self.addEventListener('activate', function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (key) { return key !== CACHE; }).map(function (key) {
      return caches.delete(key);
    }));
  }));
  self.clients.claim();
});

self.addEventListener('fetch', function (event) {
  var url = new URL(event.request.url);
  if (url.origin !== self.location.origin || event.request.method !== 'GET') return;
  event.respondWith(fetch(event.request).then(function (response) {
    var copy = response.clone();
    caches.open(CACHE).then(function (cache) { cache.put(event.request, copy); });
    return response;
  }).catch(function () {
    return caches.match(event.request);
  }));
});
```

- Replace `SHELL` with the HTML, CSS, JS, and icons this site needs to paint. Leave out API responses and anything user-specific.
- The `fetch` listener is required. Chrome will not offer Install for a manifest alone. Returning early for other origins keeps GitHub, Supabase, and similar calls out of this cache.
- Bump the `CACHE` name (`site-shell-v2`, and so on) whenever `SHELL` or a precached file changes, so the old cache is deleted on the next visit.

## Registration

From the script that runs on every production page. Edison does this at the top of `assets/js/main.js`:

```js
if ('serviceWorker' in navigator && location.protocol !== 'file:') {
  navigator.serviceWorker.register('sw.js').catch(function () {});
}
```

Use a path relative to the page (`../sw.js` from a nested page). The `file:` check skips registration when the site is opened from disk. Install still requires the published HTTPS URL.

## Check

On desktop Chrome: DevTools → Application → Manifest. Icons load, and the installability panel reports no errors. Application → Service Workers shows `sw.js` activated.

On an Android phone, open the published HTTPS URL. Chrome can take a short period of use before it offers Install; the browser menu item is available once the checks pass. The home-screen icon is the PNG from the manifest.

## Leave out

- A custom Install button or `beforeinstallprompt` handler, unless asked.
- `http://localhost` or a drive letter in page markup, the manifest, or the worker.
- Cross-origin responses in the cache.
- The manifest link on mockup pages.
