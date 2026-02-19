# chezmoi Dotfiles Repository

Personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

## Repository Structure

- `dot_*` / `private_dot_*` — source files that chezmoi deploys under `~/`
- `dot_claude/` — **global Claude Code configuration** deployed to `~/.claude/` (not repo-specific)
- `.claude/` — **repo-specific** Claude Code configuration (not managed by chezmoi)
- `private_dot_config/` — configuration files deployed under `~/.config/`
- `docs/` — documentation for each tool's configuration

## Editing Principle

**Always edit chezmoi-managed files via their source path.**
Editing the deployed target (e.g. `~/.zshrc`) directly takes it outside chezmoi's control.

```bash
# Correct approach
chezmoi edit ~/.zshrc   # opens the source file and applies on save
# or edit the source directly, then:
chezmoi apply
```

## chezmoi Naming Conventions

See `.claude/rules/chezmoi-naming.rule.md` for full details.

- `dot_` → translated to `.` (e.g. `dot_zshrc` → `~/.zshrc`)
- `private_` → deployed with permission 0600
- `executable_` → deployed with execute permission
- `private_dot_config/` → `~/.config/` (0600)
- Prefixes can be combined (e.g. `private_dot_config/`)

## Workflow

To add a new file:

```bash
chezmoi add ~/.some_config_file
```

To inspect changes:

```bash
chezmoi diff
chezmoi status
```

## Important Notes

- `dot_claude/` is the source for `~/.claude/` (global settings). Do not add repo-specific rules there.
- Never commit secrets or credentials (files needing protection must use the `private_` prefix).
- `settings.json` and `statusline.sh` live directly in the repo root and are not deployed by chezmoi.

## Commit Convention

Use Conventional Commits format. See `.claude/rules/chezmoi-git.rule.md` for details.
