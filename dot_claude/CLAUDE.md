# Claude Code Global Configuration

## Configuration Architecture

`~/.claude/` is a two-layer system managed by chezmoi.

**Shared layer** — `~/.ai-shared/core/` holds tool-agnostic rules used by Claude, Codex, and future AI tools. Chezmoi source: `dot_ai-shared/core/`.

**Claude-specific layer** — `~/.claude/rules/` has two kinds of files:
- `symlink_<name>.md.tmpl` — chezmoi-managed symlinks pointing to `~/.ai-shared/core/<name>.md`. Edit the source in `dot_ai-shared/core/`, not the symlink.
- `<name>.rule.md` — Claude-only rules. Edit directly in `dot_claude/rules/`.

**Adding a new rule:**

| Type | chezmoi source location(s) |
|---|---|
| Shared (Claude + other tools) | `dot_ai-shared/core/<name>.md` + `dot_claude/rules/symlink_<name>.md.tmpl` |
| Claude-only | `dot_claude/rules/<name>.rule.md` |

## Hooks (in `hooks/`)

- `ruff-check.sh` — Stop hook: lint and format check on changed `.py` files
- `block-pip-install.sh` — PreToolUse: prevent `pip install` (use `uv` instead)
- `readme-sync-reminder.sh` — PostToolUse: remind to update README.md when CLAUDE.md, rules, hooks, skills, or settings change

## Task-Specific Docs (in `docs/`, read on demand)

- `idd-workflow.md` — Intent-Driven Development and ADR workflow

## Development

- Research the codebase before editing. Never change code you haven't read.
