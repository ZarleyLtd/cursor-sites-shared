---
name: shared-supabase
description: Apply schema, migration or Edge Function changes on the shared CursorSites "Apps" Supabase project (ref yzyipxvlsoxfphwobfkb). Use whenever a CursorSites app needs a new table, column, index, view, RLS policy, storage bucket or migration, or when the user mentions shared Supabase, the Apps project, apply_migration or supabase db push, or before running any supabase CLI command in a repo under C:\CursorSites.
---

# Shared Supabase database (CursorSites)

Several CursorSites apps share one Supabase project, **Apps** (ref `yzyipxvlsoxfphwobfkb`, org ZarleyLtd). Each app owns its own Postgres schema, for example `scrabble`, `crossguns`, `ierne_snooker`, `theConfessional`, `familytree`, `splitify`, `rnr` and `thegolfapp` (which BGS shares as society `botanic`). Many apps also have their own Storage bucket. Each app has its own Edge Function, but the **migration history table is global**.

## Critical rule

**Never run `supabase db push` on this project.** It expects this repo's `supabase/migrations/` to match the entire remote history. Other apps' migrations are already recorded on the remote and are not in this repo, so the push fails with "Remote migration versions not found in local migrations directory".

**Never "repair" another app's remote versions or mark them as reverted** (`supabase migration repair --status reverted`) to make a push succeed. That corrupts the shared history for every other app.

Some older READMEs and `.cursorrules` files still mention `db push`. This rule overrides them.

## How to change the schema

1. Write SQL that touches only **this app's schema**, plus this app's row in `storage.buckets` if needed. Schema-qualify every name, for example `scrabble.games`.
2. Create the migration file with `supabase migration new short_snake_name` and put the SQL in it.
3. Apply the same SQL with the Supabase MCP tool **`apply_migration`** on project `yzyipxvlsoxfphwobfkb`, with a snake_case `name` that matches the file. This runs the DDL and records it in the shared history without a full push. If the MCP tool isn't available, ask the user to run the identical SQL in the Supabase SQL editor.
4. Check the result with read-only **`execute_sql`** queries.
5. Commit the local migration file, so the repo documents what was applied.

A new schema also has to be added under **Project Settings → API → Exposed Schemas** in the dashboard, if the Edge Function reaches it through PostgREST.

## Edge Functions

Function deploys don't depend on migration history:

```powershell
supabase functions deploy <app>-api --no-verify-jwt
```

All apps use `--no-verify-jwt`, because browsers call the function without logging in to Supabase. Secrets such as `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` and `SUPABASE_DB_URL` are set per function or per project. **The service role key never goes in frontend code.** The browser only knows the function URL, plus the anon key where Realtime is used.

## Full spec

`cursor-sites-shared/supabase/SHARED_DATABASE.md`

## Do not

- Run `supabase db push` against the Apps project.
- Touch another app's schema or bucket.
- Use `migration repair --status reverted` on another app's versions.
