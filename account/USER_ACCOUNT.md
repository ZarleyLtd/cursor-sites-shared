# Pattern: Connect-style user account

How CursorSites apps let a person **Connect** with a handle and password so the same account works on any device. Viewing stays available as a guest; editing or claiming identity needs an account.

This is a product/UX and client-session convention. Backend endpoints, schema, and `localStorage` key names stay **per app**. There is no file synced by `scripts/sync-ui.ps1`.

## Reference implementations

| App | Client pieces |
|-----|----------------|
| **FamilyTree** | Connect / Register / Reset in `assets/js/components/shell.js`; session in `assets/js/utils/tree-access.js` (`sessionToken` + contributor “me”) |
| **ierne-snooker** | `assets/js/utils/player-session.js` (Connect / Register / Reset dialogs, `whoAmI`, nav chip) |
| **PubliiCrossguns** | Same player-session shape as ierne-snooker |

Say **“Connect-style user account”** or **“user account pattern”** to mean: follow this spec.

## When to use

- An app needs per-person identity across devices
- Guests may read (or use limited features) without registering
- Admins issue invites; users choose their own handle and password

## When not to use

- A single shared **Admin Mode** secret that unlocks manage pages on one browser → that is a different pattern (see below)
- Anonymous device-only prefs with no server account
- OAuth / email magic links unless you deliberately extend this model

## Vocabulary

| UI term | Meaning |
|---------|---------|
| **Connect** | Open the sign-in form (prefer this label over “Log in” / “Sign in” on buttons and chips) |
| **Handle** | Public username (letters/digits; app-defined length rules) |
| **Register** | Create an account with a one-time invite/registration code |
| **Reset password** | Set a new password with a one-time admin-issued reset code |
| **Sign out** | End the session on this device |

Help copy may say “sign in” for clarity; chrome buttons should say **Connect**.

## Product rules

1. **Guest OK** — Public/read views work without an account.
2. **Credentials** — Handle + password; same account on any device.
3. **Register** — Admin issues a one-time **invite / registration code**. User picks handle + password and links to the domain entity (e.g. player, contributor). The invite is single-use and may expire.
4. **Forgot password** — Admin issues a one-time **reset code**. The original invite is **not** reused.
5. **Chrome** — Header/nav chip:
   - Guest → **Connect**
   - Signed in → handle (optional display name); opens account UI (switch account / reset / sign out)
6. **Client session** — Store session token + account summary in `localStorage`. On load, restore with `whoAmI` (or equivalent). Clear local state on expire, disable, or sign out.
7. **Change events** — Dispatch a named `CustomEvent` when session changes so nav and admin chrome can refresh.

## Client checklist (new app)

- [ ] Guest path works with no token
- [ ] Connect dialog/sheet: handle + password
- [ ] Register: invite code + handle + password (+ domain picker if needed)
- [ ] Reset: handle + reset code + new password → then Connect
- [ ] Persist token + account summary; restore on boot
- [ ] Sign out clears local session and notifies the server when possible
- [ ] Nav chip reflects guest vs signed-in
- [ ] API calls that need auth attach the session token
- [ ] Contextual help keys for Connect / Register / Reset if the app uses that pattern

## Not this pattern: Admin Mode

**Admin Mode** is a separate unlock (shared admin secret or “manage pages” gate on one browser). An account marked admin may *also* unlock admin tools while signed in (ierne / Crossguns), but:

- Do **not** merge Admin Mode and Connect into one dialog
- Do **not** replace invite-based user accounts with a single site password for end users
- Document Admin Mode in the app when needed; it is a second-wave candidate for its own shared spec

## Do not

- Invent “Log in with email” as the default when the user asked for Connect-style accounts
- Require an account to view public content unless the product explicitly requires it
- Reuse registration invites as password-reset codes
- Copy another app’s `localStorage` keys or API action names blindly — retarget them
