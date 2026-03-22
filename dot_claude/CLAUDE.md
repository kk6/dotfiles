# Claude Code Configuration

Global configuration for Claude Code. Rules are in `rules/`, hooks are in `hooks/`.

## Key Rules (in `rules/`)
- `response-style.rule.md` — Language and response structure (BLUF, Japanese output)
- `coding-philosophy.rule.md` — Code/test/commit/comment responsibilities
- `python-development.rule.md` — Python toolchain and style
- `python-exception-handling.rule.md` — Exception handling guidelines (silent failure prohibition)
- `pytest-best-practices.rule.md` — Test naming, AAA pattern, fixtures, parametrize
- `task-completion.rule.md` — Pre-submission checklist
- `session-management.rule.md` — Progress preservation and escalation
- `git-workflow.rule.md` — Conventional commits, TDD, branching
- `idd-workflow.rule.md` — Intent-Driven Development and ADR workflow
- `claude-md-sync.rule.md` — Keep CLAUDE.md in sync when rules/hooks change
