# Git Workflow (chezmoi dotfiles repository)

## Branch Strategy

- Committing directly to `main` is fine for this personal repository.
- Use a feature branch for larger changes (major config overhauls, adding a new tool, etc.).

## Conventional Commits

Commit messages follow [Conventional Commits v1.0.0](https://www.conventionalcommits.org/).

### Common types for this repository

| Type | When to use |
|---|---|
| `feat` | Adding a new tool or configuration |
| `fix` | Correcting a misconfiguration |
| `chore` | Routine updates (version bumps, etc.) |
| `docs` | Documentation changes |
| `refactor` | Reorganizing or cleaning up configuration |
| `style` | Formatting changes with no functional effect |

### Using scope (optional)

Use the target tool name as the scope:

```
feat(zsh): add fzf-tab plugin
fix(git): correct merge conflict style
chore(ghostty): update font size
feat(claude): add new custom command
```

## Apply-then-Commit Flow

```bash
# 1. Edit the source file
chezmoi edit ~/.zshrc

# 2. Review the diff
chezmoi diff

# 3. Apply to home directory
chezmoi apply

# 4. Verify it works, then commit
git add dot_zshrc
git commit -m "feat(zsh): add new alias"
```

## Pre-commit Checklist

- [ ] No secrets, tokens, or passwords included
- [ ] Confirmed `chezmoi apply` deploys cleanly
- [ ] Files requiring restricted permissions have the `private_` prefix
