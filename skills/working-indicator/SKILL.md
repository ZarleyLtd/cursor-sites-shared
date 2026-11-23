---
name: working-indicator
description: Implement or reference the CursorSites working indicator, a busy overlay that only appears after a delay. Use when the user asks for a working indicator, busy overlay, "please wait", a saving spinner, or feedback for actions expected to take more than about 500 ms (uploads, network writes, image compression) in any app under C:\CursorSites.
---

# Working indicator (CursorSites)

A full-viewport busy overlay that shows a spinner and a short message while an action the user started is running. It only appears after **500 ms**, so fast calls never flash it. The pattern started in Splitify.

## When to use

- Work expected to take more than about 500 ms: network writes, uploads, image compression, multi-step API calls.
- The user can't usefully continue until the work finishes.

## When not to use

- Instant local UI updates.
- Background refreshes the user can ignore. Never block the whole app for those.
- Short success or no-op text: use `brief-message` instead.
- A Yes/No choice: use `confirm-dialog` instead.

## Implementation

The canonical source is `cursor-sites-shared/ui/working-indicator.js` / `working-indicator.css`. Each app keeps synced copies at `assets/js/utils/working-indicator.js` and `assets/css/working-indicator.css`.

```html
<link rel="stylesheet" href="assets/css/working-indicator.css" />
<script src="assets/js/utils/working-indicator.js"></script>
```

```javascript
await WorkingIndicator.withWorking(doSave(), 'Saving…');   // preferred: always ends, even on error

WorkingIndicator.begin('Saving…');
try { /* ... */ } finally { WorkingIndicator.end(); }
WorkingIndicator.setMessage('Uploading photo…');
```

Rules:

- `begin`/`end` are reference-counted, so nested calls are safe. The overlay hides only when the count returns to zero.
- `begin` starts the count straight away. The overlay only appears after `WorkingIndicator.SHOW_DELAY_MS` (500 ms). If `end` runs before then, nothing is shown.
- The global is `WorkingIndicator`. The shared script also sets the legacy alias `SplitifyWorking`.
- The hidden state uses the class `working-indicator--hidden`. The legacy class `hidden` also works.
- Theme variables: `--working-panel-bg`, `--working-panel-color` and `--working-radius`.

## Rollout

`sync-ui.ps1` currently syncs this pattern only to **Splitify**. To add another app:

1. Add the app to `$workingTargets` in `cursor-sites-shared/scripts/sync-ui.ps1`.
2. Run the script.

To change the shared code:

1. Edit the files in `cursor-sites-shared/ui/`.
2. Run the sync.
3. Commit in each affected app.

## Full spec

`cursor-sites-shared/ui/WORKING_INDICATOR.md`.

## Do not

- Invent a different full-screen spinner.
- Call `begin` without a matching `end` on error paths. Prefer `withWorking`.
- Show the indicator for work you know is instant.
