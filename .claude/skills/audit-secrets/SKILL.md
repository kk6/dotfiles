---
name: audit-secrets
description: Scan chezmoi source files for accidentally exposed secrets and verify sensitive files have the private_ prefix.
---

# Secrets Audit for chezmoi Dotfiles

Scan the chezmoi source directory for potential secret exposure and report findings.

## Instructions

### 1. Find Files Without `private_` That May Contain Secrets

Run pattern searches across all source files that do NOT have the `private_` prefix:

```bash
# List all non-private source files
find ~/.local/share/chezmoi -type f \
  ! -path '*/.git/*' \
  ! -name 'private_*' \
  ! -path '*/private_*'
```

Search those files for common secret patterns:

```bash
# API keys, tokens, passwords
grep -rn --include='*' \
  -e 'api[_-]key\s*=' \
  -e 'api[_-]secret\s*=' \
  -e 'access[_-]token\s*=' \
  -e 'secret[_-]key\s*=' \
  -e 'password\s*=' \
  -e 'passwd\s*=' \
  -e 'AUTH_TOKEN' \
  -e 'PRIVATE_KEY' \
  ~/.local/share/chezmoi \
  --exclude-dir='.git'
```

```bash
# High-entropy strings (possible raw tokens)
grep -rEn '[A-Za-z0-9+/]{40,}' ~/.local/share/chezmoi \
  --exclude-dir='.git' \
  ! -path '*/private_*'
```

### 2. Verify Known Sensitive Files Use `private_`

Check that these file types have the `private_` prefix in their source names:

- `.npmrc` → should be `private_dot_npmrc`
- `.netrc` → should be `private_dot_netrc`
- `.ssh/config` → should be under `private_dot_ssh/`
- Any file under `~/.config/` containing credentials

```bash
chezmoi status
chezmoi managed --include=files | grep -v '^private'
```

Review the list of non-private managed files for anything that looks sensitive.

### 3. Check Git History for Accidentally Committed Secrets

```bash
git -C ~/.local/share/chezmoi log --oneline -20
git -C ~/.local/share/chezmoi diff HEAD~5..HEAD -- . ':!*.png' ':!*.jpg'
```

Look for any patterns matching secrets in recent commits.

### 4. Report Findings

Categorize findings into:

- **CRITICAL** — Active secret or credential found in a non-private file
- **WARNING** — File looks sensitive but lacks `private_` prefix
- **INFO** — Pattern matched but likely a false positive (e.g. placeholder value)

For each finding, suggest the remediation:

```bash
# To re-add a file with private_ prefix
chezmoi add --force <target-path>   # chezmoi will re-evaluate permissions
# or manually rename the source file and re-run chezmoi apply
```

## Output

Produce a structured report:

```
## Secrets Audit Report

### CRITICAL
- (none) or list of files with confirmed secrets

### WARNING
- (none) or list of suspicious files

### INFO
- Any false positives noted

### Recommendations
- Specific remediation steps for each finding
```

$ARGUMENTS
