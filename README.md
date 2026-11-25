# cursor-sites-shared

Shared UI utilities and conventions used across CursorSites projects.

## Contents

| Path | Description |
|------|-------------|
| `ui/brief-message.js` | Ephemeral anchored feedback utility |
| `ui/brief-message.css` | Default brief-message styles (CSS variables for theming) |
| `ui/BRIEF_MESSAGE.md` | Canonical spec for the brief message pattern |
| `ui/confirm-dialog.js` | In-page Yes/No confirm overlay |
| `ui/confirm-dialog.css` | Confirm dialog styles (CSS variables for theming) |
| `ui/CONFIRM_DIALOG.md` | Canonical spec for the confirm dialog pattern |
| `ui/working-indicator.js` | Delayed busy overlay for long actions |
| `ui/working-indicator.css` | Working indicator styles |
| `ui/WORKING_INDICATOR.md` | Canonical spec for the working indicator pattern |
| `ui/CONTEXTUAL_HELP.md` | Canonical spec for click-to-target contextual help (**?** then tap a control). Reference code stays in FamilyTree; it is not synced. |
| `installable-app/INSTALLABLE_APP.md` | Canonical spec for an Edison-style installable app (home-screen icon) |
| `account/USER_ACCOUNT.md` | Canonical spec for Connect-style user accounts (handle + invite). Not synced. |
| `jp-logo/` | The JP logo footer credit: PNG, animated SVG, `jp-logo.js`, `jp-logo.css` (synced) and `JP_LOGO.md` (spec) |
| `jp-logo/source/` | Generator for the logo animation, plus standalone SVG, GIF and WebP versions for sharing |
| `scripts/sync-ui.ps1` | Copy shared UI files into consuming projects |
| `skills/` | Claude Code skills for each pattern |
| `CLAUDE.md` | Shared rules for Claude Code across all CursorSites apps |
| `CONVENTIONS.md` | Overview of every shared pattern |
| `supabase/SHARED_DATABASE.md` | How to apply schema changes on the shared Apps Supabase project |

## Usage

1. Edit files under `ui/` (or `jp-logo/` for the JP logo).
2. Run `.\scripts\sync-ui.ps1` from this directory.
3. Commit changes in each affected project repo.

`installable-app/INSTALLABLE_APP.md`, `ui/CONTEXTUAL_HELP.md`, and `account/USER_ACCOUNT.md` are specs to follow in each project. They are not copied by the sync script. Contextual help’s engine and catalog stay in the app that implements them (FamilyTree is the reference). Account Connect UI stays per app (FamilyTree and the snooker apps are references).

See also: `CONVENTIONS.md` (overview of every pattern) and `CLAUDE.md` (shared rules for Claude Code; the root `CLAUDE.md` in C:/CursorSites imports it).

## Skills

`skills/<name>/SKILL.md` are the Claude Code skills for each pattern. On the owner's PC, `~/.claude/skills/<name>` is a directory junction to each folder here. Edison's Claude workflow installs them on the GitHub Actions runner. Push changes so cloud runs pick them up.
