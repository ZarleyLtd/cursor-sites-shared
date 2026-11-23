# UI pattern: Working indicator

Full-viewport busy overlay with spinner and short message while a user-started action runs. Originated in **Splitify**; standardized for CursorSites with a delayed paint so fast calls do not flash.

## When to use

- Actions **expected** to take more than about **500 ms** (network writes, uploads, image compress, multi-step API)
- Work the user started and cannot usefully continue until it finishes

## When not to use

- Instant local UI updates
- Short success / no-op feedback → [brief message](BRIEF_MESSAGE.md)
- Asking Yes/No → [confirm dialog](CONFIRM_DIALOG.md)
- Background refresh the user can ignore — do not block the whole app

## Rules

1. **Threshold:** only wrap work you expect to exceed ~500 ms.
2. **Delayed show:** `begin` starts the busy refcount immediately, but the overlay is **not painted until 500 ms** have elapsed (`WorkingIndicator.SHOW_DELAY_MS`). If `end` runs before that, nothing is shown.
3. **Refcount:** nested `begin` / `end` pairs stay correct; the overlay hides only when the count returns to zero.

## API

Canonical utility: `cursor-sites-shared/ui/working-indicator.js` (synced as `assets/js/utils/working-indicator.js`).

```javascript
WorkingIndicator.begin('Saving…');
// ... async work ...
WorkingIndicator.end();

await WorkingIndicator.withWorking(doSave(), 'Saving…');

WorkingIndicator.setMessage('Uploading photo…');
```

| Method | Description |
|--------|-------------|
| `begin(message?)` | Increment busy count; schedule overlay after 500 ms |
| `end()` | Decrement; hide when count is zero |
| `withWorking(promise, message?)` | `begin`, await promise, always `end` |
| `setMessage(message?)` | Update label while busy |
| `SHOW_DELAY_MS` | `500` — delay before paint |

Global name: `WorkingIndicator` (not app-prefixed). The shared script also sets `SplitifyWorking` as a legacy alias so Splitify call sites keep working until they migrate.

## Behaviour

1. Creates a fixed overlay with class `working-indicator` on first use
2. Uses `aria-live="polite"` and `aria-busy`
3. Keeps a pending count so overlapping calls share one overlay
4. Hides with class `working-indicator--hidden` (legacy class `hidden` also works)

## Styling

Canonical stylesheet: `cursor-sites-shared/ui/working-indicator.css` (synced as `assets/css/working-indicator.css`).

```css
@import url('working-indicator.css');

:root {
  --working-panel-bg: rgba(24, 20, 17, 0.92);
  --working-panel-color: #efe6d4;
  --working-radius: 999px;
}
```

## Syncing changes

```powershell
.\scripts\sync-ui.ps1
```

Edit canonical files under `cursor-sites-shared/ui/` first, then sync.

## Include on the page

```html
<link rel="stylesheet" href="assets/css/working-indicator.css" />
<script src="assets/js/utils/working-indicator.js"></script>
```

## Do not

- Show a spinner for sub-500 ms work you know is instant
- Leave `begin` without a matching `end` on error paths (prefer `withWorking`)
- Use this instead of a confirm or brief message
