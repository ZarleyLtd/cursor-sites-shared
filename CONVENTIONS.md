# CursorSites conventions

Cross-project patterns shared by multiple repos under this folder. When asking an AI to implement one, name the **skill** (or the pattern phrase below); each personal skill points at the canonical spec.

| Pattern | Phrase / skill | Canonical spec |
|---------|----------------|----------------|
| Brief message | `brief-message` | [ui/BRIEF_MESSAGE.md](ui/BRIEF_MESSAGE.md) |
| Confirm dialog | `confirm-dialog` | [ui/CONFIRM_DIALOG.md](ui/CONFIRM_DIALOG.md) |
| Working indicator | `working-indicator` | [ui/WORKING_INDICATOR.md](ui/WORKING_INDICATOR.md) |
| Contextual help | `contextual-help` | [ui/CONTEXTUAL_HELP.md](ui/CONTEXTUAL_HELP.md) |
| Edison-style installable app | `installable-app` | [installable-app/INSTALLABLE_APP.md](installable-app/INSTALLABLE_APP.md) |
| Connect-style user account | `user-account` | [account/USER_ACCOUNT.md](account/USER_ACCOUNT.md) |
| Shared Supabase database | `shared-supabase` | [supabase/SHARED_DATABASE.md](supabase/SHARED_DATABASE.md) |
| JP logo (footer credit) | `jp-logo` | [jp-logo/JP_LOGO.md](jp-logo/JP_LOGO.md) |

Synced UI code (edit under `ui/` or `jp-logo/`, then run `scripts/sync-ui.ps1`): brief message, confirm dialog (BGS), working indicator (Splitify), JP logo (Stomper). FamilyTree’s sheet-based confirm is not overwritten by sync until migrated.

## Brief message

Short, ephemeral UI feedback anchored to the control the user clicked. Not a modal, not a toast — a contextual pill/card that auto-dismisses.

- **Canonical spec:** [ui/BRIEF_MESSAGE.md](ui/BRIEF_MESSAGE.md)
- **Canonical code:** [ui/](ui/)
- **Sync script:** `scripts/sync-ui.ps1`
- **Skill:** `brief-message`

When adding brief-message behaviour to a new project, sync the shared files and add a thin `docs/UI_BRIEF_MESSAGE.md` that links to the canonical spec.

## Confirm dialog

In-page Yes/No overlay for destructive or hard-to-undo actions. Prefer this over `window.confirm`.

- **Canonical spec:** [ui/CONFIRM_DIALOG.md](ui/CONFIRM_DIALOG.md)
- **Canonical code:** `confirm-dialog.js` / `confirm-dialog.css` under [ui/](ui/)
- **Skill:** `confirm-dialog`

## Working indicator

Busy overlay for user-started work expected to take more than ~500 ms. The overlay paints only after a 500 ms delay so fast calls do not flash.

- **Canonical spec:** [ui/WORKING_INDICATOR.md](ui/WORKING_INDICATOR.md)
- **Canonical code:** `working-indicator.js` / `working-indicator.css` under [ui/](ui/)
- **Skill:** `working-indicator`

## Contextual help (click-to-target)

**?** in the header (and in any overlay that covers the header). The next tap is intercepted and a popover explains that control. Copy describes the feature, never a particular record. This is not the brief-message pattern, and it is not Splitify’s “How it works” dialog.

- **Canonical spec:** [ui/CONTEXTUAL_HELP.md](ui/CONTEXTUAL_HELP.md)
- **Reference implementation:** FamilyTree (`assets/js/components/contextual-help.js`, `assets/css/contextual-help.css`, `assets/js/utils/help-catalog.js`)
- **Skill:** `contextual-help`

Nothing in this pattern is synced by `sync-ui.ps1`. Copy the engine, retarget the catalog global, and write a new catalog. Add a thin `docs/UI_CONTEXTUAL_HELP.md` that links to the canonical spec.

## Edison-style installable app

A static site that Chrome on Android offers to **Install**, adding a home-screen icon that opens the site without the address bar. The phrase **“Edison-style installable app”** means this pattern.

- **Canonical spec:** [installable-app/INSTALLABLE_APP.md](installable-app/INSTALLABLE_APP.md)
- **Reference implementation:** the Edison repo (`manifest.json`, `sw.js`, the `<head>` links, and the registration in `assets/js/main.js`)
- **Skill:** `installable-app`

Copy the manifest, icons, and service worker into the project. Nothing in this pattern is synced by `sync-ui.ps1`.

## Connect-style user account

Handle + password **Connect**, guest-readable by default, one-time registration invite and admin reset codes. Same vocabulary as FamilyTree and the snooker apps.

- **Canonical spec:** [account/USER_ACCOUNT.md](account/USER_ACCOUNT.md)
- **References:** FamilyTree shell + `tree-access.js`; ierne-snooker / PubliiCrossguns `player-session.js`
- **Skill:** `user-account`

Not synced. Distinct from site-wide **Admin Mode** unlock.

## Shared Supabase database

Several apps share one Supabase project with per-app schemas. Do not use `supabase db push` for schema changes on that project.

- **Canonical spec:** [supabase/SHARED_DATABASE.md](supabase/SHARED_DATABASE.md)
- **Skill:** `shared-supabase`

## JP logo

The owner's JP logo as a small "Created by" credit, usually in the footer. It is a button: tapping it plays the logo animation backwards to an upright J and P, then forwards to the logo again.

- **Canonical spec:** [jp-logo/JP_LOGO.md](jp-logo/JP_LOGO.md)
- **Canonical files:** [jp-logo/](jp-logo/) (PNG, script-driven SVG, `jp-logo.js`, `jp-logo.css`); generator and GIF/WebP/standalone SVG in `jp-logo/source/`
- **Reference implementation:** Stomper
- **Skill:** `jp-logo`

Synced by `sync-ui.ps1` to the apps in `$jpLogoTargets`. Change the animation with `jp-logo/source/jpLogo-animate.py`, never by editing an app copy.

## Candidates (not yet first-class)

Promote to a full spec + skill when reuse is clear:

- Client image compress (`image-compress.js` in many apps)
- Admin Mode unlock (golf / snooker / crossguns / scrabble) — separate from user account
- App shell / bottom sheet (`openSheet`) if enough apps share the interaction
