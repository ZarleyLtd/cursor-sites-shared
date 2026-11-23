---
name: contextual-help
description: Implement or reference the CursorSites click-to-target contextual help pattern, where the user taps a ? button and then taps a control to see what it does. Use when the user asks for contextual help, help mode, click-to-target help, data-help attributes, a help catalog, or a ? help button like FamilyTree's, in any app under C:\CursorSites.
---

# Contextual help (CursorSites)

Contextual help is opt-in. The user taps **?** in the header, or in any overlay that covers the header, and then taps a control. That tap does **not** activate the control. Instead, a popover explains the **feature**. Help text never describes a particular record.

This is not the brief-message pattern, and it is not Splitify's "How it works" dialog.

## When to use

- Phone-first apps with many controls whose purpose isn't obvious from the label.
- Charts, lists, forms and overlays that need the same explanations.

## When not to use

- A one-time product tour: use a dialog instead.
- Feedback after an action: use `brief-message`.
- Errors or Yes/No choices: use an alert or `confirm-dialog`.

## Implementation

`sync-ui.ps1` does **not** sync any of this pattern. To add it to an app:

1. Copy the FamilyTree engine.
2. Retarget the catalog global for the new app.
3. Write a new catalog for that app.

**Reference implementation (FamilyTree):**

- `FamilyTree/assets/js/components/contextual-help.js`: the engine, `ContextualHelp.init()`.
- `FamilyTree/assets/css/contextual-help.css`: import it from `style.css`, next to `brief-message.css`.
- `FamilyTree/assets/js/utils/help-catalog.js`: the help text, keyed by control.

**Wiring:**

1. Mark each control with `data-help="<key>"`.
2. The **?** button gets `data-help-toggle`. Put one in the header, in sheets and in the lightbox.
3. Load the catalog before the engine.
4. Call `ContextualHelp.init()` before the page binds its own listeners.
5. Add a thin `docs/UI_CONTEXTUAL_HELP.md` that links to the canonical spec.

## Full spec

Read `cursor-sites-shared/ui/CONTEXTUAL_HELP.md` (about 280 lines) before implementing. It covers popover positioning, layering over sheets and lightboxes, cursor state, and the banner.

## Do not

- Describe a specific record in help text.
- Invent a different help-mode interaction when this pattern was requested.
- Reuse another app's help catalog word for word without retargeting the keys and text.
