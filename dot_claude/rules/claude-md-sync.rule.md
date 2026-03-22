# CLAUDE.md Sync Rule

## When to Check

After any of the following operations on `rules/` (or `hooks/`):
- **Adding** a new file
- **Renaming** or **deleting** an existing file
- **Changing** a file's purpose or scope significantly

## What to Do

1. Read the corresponding section in `CLAUDE.md` (e.g., "Key Rules" for `rules/`).
2. Compare the listed entries against the actual files on disk.
3. If there is a discrepancy (missing entry, stale entry, outdated description), propose an update to `CLAUDE.md` to the user before applying it.

## Scope

- This applies to all `CLAUDE.md` files in the project (repo-root and `.claude/`).
- Only update sections that reference the changed directory — do not rewrite unrelated parts.
