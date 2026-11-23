---
name: user-account
description: Implement or reference the CursorSites Connect-style user account pattern (handle and password, invite-based registration, admin reset codes, read access for guests). Use when the user asks for user accounts, Connect, sign-in with a handle, contributor or player accounts, registration invites, password reset codes, or account chrome like FamilyTree's or the snooker apps', in any app under C:\CursorSites.
---

# Connect-style user account (CursorSites)

People sign in with a handle and password using **Connect**, so the same account works on every device. Guests can view without an account, but identity and editing need one. An admin issues a one-time **invite** for registration and a one-time **reset code** for forgotten passwords. This pattern is not OAuth, and it is not Admin Mode.

This document covers product, UX and client-session conventions only. Backend endpoints, the schema and `localStorage` key names stay **per app**. Nothing is synced.

## Reference implementations

Copy their shape and retarget the API and storage keys:

- **FamilyTree:** `assets/js/components/shell.js` (Connect / Register / Reset) and `assets/js/utils/tree-access.js` (the `sessionToken` and the contributor "me").
- **ierne-snooker** and **PubliiCrossguns:** `assets/js/utils/player-session.js` (the dialogs, `whoAmI` and the nav chip).

## Vocabulary

- **Connect** opens the sign-in form. Use "Connect" on buttons and chips, not "Log in" or "Sign in". Help text may say "sign in".
- **Handle** is the public username.
- **Register** uses a one-time invite code, then the user picks a handle and password and links the account to a domain entity (a player or contributor).
- **Reset password** uses a one-time reset code issued by an admin. **Never reuse the invite code for resets.**
- **Sign out** ends the session on this device.

## Product rules

1. Public views work with no token.
2. The header or nav chip shows **Connect** to a guest. When signed in, it shows the handle and opens the account UI (switch account, reset, sign out).
3. Store the session token and an account summary in `localStorage`. On page load, restore them with `whoAmI` or an equivalent. Clear them when the session expires, is disabled, or the user signs out.
4. Dispatch a named `CustomEvent` when the session changes, so the nav and admin chrome can refresh.
5. API calls that need authentication attach the session token. The server hashes passwords, invite codes and tokens, and never logs them.

## Checklist for a new app

- [ ] The guest path works.
- [ ] Connect form: handle + password.
- [ ] Register form: invite code + handle + password, plus a domain picker if needed.
- [ ] Reset form: handle + reset code + new password, then Connect.
- [ ] The token and account summary persist and are restored on load.
- [ ] Sign out clears local state and tells the server when possible.
- [ ] The nav chip shows the guest or signed-in state.
- [ ] Contextual-help keys exist for Connect, Register and Reset, if the app uses `contextual-help`.

## Admin Mode is a separate pattern

Admin Mode is a separate unlock: a shared admin secret, or a gate on the manage pages in one browser. An account marked as admin may also unlock admin tools (ierne-snooker and Crossguns do this). Even so, **never merge Admin Mode and Connect into one dialog**, and never replace invite-based accounts with a single site password.

## Full spec

`cursor-sites-shared/account/USER_ACCOUNT.md`.

## Do not

- Default to email login, OAuth or magic links when the user asked for Connect-style accounts.
- Require an account to view public content unless the product explicitly needs it.
- Copy another app's `localStorage` keys or API action names without retargeting them.
