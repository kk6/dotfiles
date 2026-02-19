# chezmoi File Naming Conventions

## Source Path to Target Path Mapping

chezmoi transforms filenames in the source directory (`~/.local/share/chezmoi/`) when deploying to the home directory.

## Prefix Reference

| Prefix | Meaning | Example |
|---|---|---|
| `dot_` | Translated to a leading `.` | `dot_zshrc` → `~/.zshrc` |
| `private_` | Deployed with permission 0600 | `private_dot_npmrc` → `~/.npmrc` (0600) |
| `executable_` | Deployed with execute permission (0755) | `executable_script.sh` → `~/script.sh` |
| `empty_` | Deployed as an empty file (content ignored for tracking) | `empty_starship.toml` |
| `readonly_` | Deployed as read-only | |

Prefixes can be combined. The required order is `private_` → `executable_` → `dot_`.

## Directory Prefixes

The same prefixes apply to directories:

```
private_dot_config/git/    → ~/.config/git/    (directory itself uses normal permissions)
private_dot_ssh/           → ~/.ssh/           (directory 0700)
```

## Source-to-Target Mapping in This Repository

| Source | Target |
|---|---|
| `dot_zshrc` | `~/.zshrc` |
| `dot_zshenv` | `~/.zshenv` |
| `dot_zprofile` | `~/.zprofile` |
| `dot_tmux.conf` | `~/.tmux.conf` |
| `dot_vimrc` | `~/.vimrc` |
| `dot_editorconfig` | `~/.editorconfig` |
| `dot_fzf.zsh` | `~/.fzf.zsh` |
| `dot_stylelintrc` | `~/.stylelintrc` |
| `dot_claude/` | `~/.claude/` |
| `private_dot_config/` | `~/.config/` |
| `private_dot_npmrc` | `~/.npmrc` |

## Notes When Adding Files

- Use `chezmoi add <target-path>` to automatically create a source file with the correct naming.
- When creating source files manually, follow the naming conventions strictly.
- Forgetting `private_` on a file containing secrets will deploy it with world-readable permissions.
