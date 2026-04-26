# Claude Code Global Configuration

## Configuration Architecture

`~/.claude/` is managed by chezmoi. Chezmoi source: `dot_claude/`.

**Rules** — `~/.claude/rules/` contains `<name>.rule.md` files. All rules are Claude-specific. Edit directly in `dot_claude/rules/`.

**Skills** — `~/.ai-shared/skills/` holds skills shared across AI tools (Claude, Codex). Chezmoi source: `dot_ai-shared/skills/`.

**Adding a new rule:**

Add `dot_claude/rules/<name>.rule.md` directly.

## Hooks (in `hooks/`)

- `ruff-check.sh` — Stop hook: lint and format check on changed `.py` files
- `block-pip-install.sh` — PreToolUse: prevent `pip install` (use `uv` instead)
- `readme-sync-reminder.sh` — PostToolUse: remind to update README.md when CLAUDE.md, rules, hooks, skills, or settings change

## Task-Specific Docs (in `docs/`, read on demand)

- `idd-workflow.md` — Intent-Driven Development and ADR workflow

## Development

- Research the codebase before editing. Never change code you haven't read.
