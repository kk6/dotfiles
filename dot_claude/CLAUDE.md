# Claude Code Global Configuration

## Toolchain
- **Language**: Python (primary)
- **Package manager**: uv
- **Linting/Formatting**: ruff (enforced via Stop hook)
- **Type checking**: ty
- **Testing**: pytest
- **VCS**: git with conventional commits, semantic-release

## Hooks (in `hooks/`)
- `ruff-check.sh` — Stop hook: lint and format check on changed `.py` files
- `block-pip-install.sh` — PreToolUse: prevent `pip install` (use `uv` instead)
- `readme-sync-reminder.sh` — PostToolUse: remind to update README.md when CLAUDE.md, rules, hooks, skills, or settings change

## Task-Specific Docs (in `docs/`, read on demand)
- `idd-workflow.md` — Intent-Driven Development and ADR workflow
