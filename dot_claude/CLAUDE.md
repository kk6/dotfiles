# Claude Code Global Configuration

## Configuration Architecture

`~/.claude/` is managed by chezmoi. Chezmoi source: `dot_claude/`.

**Rules** — `~/.claude/rules/` contains `<name>.rule.md` files, auto-loaded every session. All rules are Claude-specific. Edit directly in `dot_claude/rules/`.

**Rule Library** — `~/.claude/rule-library/` holds rules that only apply to a specific framework (e.g. Django), where a `paths:` glob can't reliably detect that framework. Not auto-loaded; copy the relevant file into a project's own `.claude/rules/` when needed.

**Skills** — `~/.claude/skills/` holds Claude-specific skills. Not shared with Codex (`~/.codex/skills/`) — prompts are tuned per model rather than reused across tools.

**Adding a new rule:**

- Applies to every project, or scopable via `paths:` glob → add `dot_claude/rules/<name>.rule.md` directly.
- Applies only to a specific framework/stack that `paths:` can't isolate → add `dot_claude/rule-library/<name>.rule.md` instead.

## Hooks (in `hooks/`)

- `ruff-check.sh` — Stop hook: lint and format check on changed `.py` files
- `block-pip-install.sh` — PreToolUse: prevent `pip install` (use `uv` instead)
- `readme-sync-reminder.sh` — PostToolUse: remind to update README.md when CLAUDE.md, rules, hooks, skills, or settings change

## Task-Specific Docs (in `docs/`, read on demand)

- `idd-workflow.md` — Intent-Driven Development and ADR workflow

## Development

- Research the codebase before editing. Never change code you haven't read.
