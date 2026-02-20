---
name: sync-status
description: Inspect the current chezmoi sync state and report unapplied changes, unmanaged files, and whether it is safe to run chezmoi apply.
---

# chezmoi Sync Status

Provide a clear overview of the current chezmoi state and guide the user through safely applying any pending changes.

## Instructions

### 1. Gather State Information

Run all of these in parallel:

```bash
# Summary of managed file states
chezmoi status

# Detailed diff of what would change on apply
chezmoi diff

# Git status of the source directory
git -C ~/.local/share/chezmoi status

# Recent commits in the source repo
git -C ~/.local/share/chezmoi log --oneline -5
```

### 2. Interpret `chezmoi status` Output

Each line has a two-character status code. Explain relevant entries to the user:

| Code | Meaning |
|---|---|
| `A` | File is managed but missing from target — will be created |
| `M` | Source and target differ — target will be updated |
| `D` | File removed from source — will be deleted from target |
| `R` | File permissions differ |

### 3. Assess Safety of `chezmoi apply`

Flag concerns before applying:

- **Uncommitted source changes** — source has edits not yet in git; applying would work but changes aren't versioned yet
- **Diverged from remote** — run `git -C ~/.local/share/chezmoi fetch && git status` to check
- **Large number of deletions** — confirm intentional before applying

### 4. Summarise Unmanaged Files (optional)

If the user wants to know what config files exist on the system but are NOT managed by chezmoi:

```bash
# Common config locations to audit
ls ~/.config/
ls ~/
```

Compare against `chezmoi managed` output and highlight candidates worth adding.

### 5. Apply If Safe

If there are no concerns, offer to apply:

```bash
chezmoi apply --verbose
```

Then verify:

```bash
chezmoi status   # should show no remaining differences
```

### 6. Commit Uncommitted Source Changes

If the source directory has uncommitted edits, prompt the user to commit:

```bash
git -C ~/.local/share/chezmoi status
git -C ~/.local/share/chezmoi add <files>
git -C ~/.local/share/chezmoi commit -m "chore: sync dotfiles"
```

## Output

Produce a structured summary:

```
## chezmoi Sync Status

### Pending Changes  (N files)
- Modified: ...
- Added: ...
- Deleted: ...

### Source Repo Git State
- Branch: main (clean / N uncommitted changes)
- Remote: up to date / N commits behind

### Safety Assessment
- ✅ Safe to apply  /  ⚠️  Review before applying

### Recommended Next Steps
1. ...
```

$ARGUMENTS
