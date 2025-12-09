---
description: "Create a git commit following Conventional Commits v1.0.0 specification with proper pre-commit hook handling"
---

Create a git commit for the current changes. Follow these guidelines:

## Pre-commit Analysis

First, run these commands in parallel to understand the current state:

```bash
git status
git diff
git log --oneline -5
```

## Commit Process

1. **Stage relevant files** based on the changes shown above
2. **Create commit message** following Conventional Commits v1.0.0:

### Format:
```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Types:
- `feat:` - New feature (MINOR version bump)
- `fix:` - Bug fix (PATCH version bump)
- `docs:` - Documentation changes
- `style:` - Code formatting (no functional changes)
- `refactor:` - Code refactoring
- `test:` - Adding/modifying tests
- `chore:` - Maintenance tasks
- `ci:` - CI configuration changes
- `perf:` - Performance improvements
- `build:` - Build system changes

### Breaking Changes:
- Add exclamation mark after type: `feat(api)!: change endpoint structure`
- Or include footer: `BREAKING CHANGE: describe the breaking change`

### Required Footer:
```
🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Pre-commit Hook Handling

### If commit succeeds but hooks modify files:
```bash
git add <modified-files>
git commit --amend --no-edit
```

### If commit fails due to hook errors:
```bash
git add <modified-files>
git commit -m "..."  # Create NEW commit, don't use --amend
```

## Example Usage:

For a new feature:
```bash
git add src/auth.py tests/test_auth.py
git commit -m "$(cat <<'EOF'
feat(auth): add OAuth2 authentication

Implement OAuth2 flow with token refresh support.
Includes comprehensive test coverage.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

$ARGUMENTS
