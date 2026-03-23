---
paths:
  - ".claude/rules/**"
  - ".claude/hooks/**"
  - ".claude/skills/**"
  - "**/settings.json"
  - "**/CLAUDE.md"
  - "**/README.md"
---

# CLAUDE.md & README Sync Rule

## When to Check

After any of the following operations on `rules/`, `hooks/`, `skills/`, or `settings.json`:
- **Adding** a new file
- **Renaming** or **deleting** an existing file
- **Changing** a file's purpose or scope significantly

## What to Do

### CLAUDE.md

1. Read the corresponding section in `CLAUDE.md` (e.g., "Key Rules" for `rules/`).
2. Compare the listed entries against the actual files on disk.
3. If there is a discrepancy (missing entry, stale entry, outdated description), propose an update to `CLAUDE.md` to the user before applying it.

### README.md

1. Read the repository root `README.md`.
2. Check whether the change affects any section (e.g., managed files list, documentation table, Claude Code section).
3. If the README references or should reference the changed content, propose an update to the user.

## Scope

- This applies to all `CLAUDE.md` files in the project (repo-root and `.claude/`).
- This also applies to the repository root `README.md`.
- Only update sections that reference the changed directory — do not rewrite unrelated parts.
