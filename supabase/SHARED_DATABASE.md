# Shared Supabase database (CursorSites Apps)

Several CursorSites apps share one Supabase project (`Apps`, ref `yzyipxvlsoxfphwobfkb`). Each app owns its own Postgres **schema** (for example `scrabble`, `crossguns`, `ierne_snooker`, `theConfessional`). Edge Functions are per-app; the migration history table is **global**.

## Do not use `supabase db push` for schema changes

`supabase db push` expects this repo’s `supabase/migrations/` to match the entire remote migration history. Other apps’ migrations are already recorded on the shared project and are **not** in this repo, so push fails with “Remote migration versions not found in local migrations directory.”

Never “repair” or mark those remote versions as reverted to make push succeed — that would corrupt the shared history for the other apps.

## Schema / DDL changes (tables, constraints, indexes)

1. Write the SQL so it only touches **this app’s schema** (qualify names: `scrabble.…`, `crossguns.…`, etc.).
2. Create a local migration file with the CLI so the filename is correct:
   ```bash
   supabase migration new short_snake_name
   ```
   Put the SQL in the generated file under `supabase/migrations/`.
3. Apply the same SQL to the live database with the Supabase MCP **`apply_migration`** tool (project id `yzyipxvlsoxfphwobfkb`), using a snake_case `name` that matches the intent of the file. That runs the DDL and records it in the shared migration history without needing a full `db push`.
4. Verify with **`execute_sql`** (read-only checks) against the affected schema objects.
5. Keep the local `supabase/migrations/*.sql` file in git so the repo documents what was applied.

If MCP is unavailable, run the identical SQL in the Supabase SQL editor for that project, and still commit the local migration file.

## Edge Functions

Deploying a function does **not** depend on migration history alignment:

```bash
supabase functions deploy <function-name> --no-verify-jwt
```

(Use `--no-verify-jwt` when the function already uses custom auth / public client calls, as with Scrabble’s `scrabble-api`.)

## Checklist

- SQL scoped to this app’s schema only
- Local migration file committed
- Applied via `apply_migration` (or SQL editor), not `db push`
- Edge function redeployed if API behaviour changed
- No `migration repair --status reverted` for other apps’ versions
