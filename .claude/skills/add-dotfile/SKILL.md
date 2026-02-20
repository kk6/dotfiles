---
name: add-dotfile
description: Safely add a new dotfile to chezmoi management, determining the correct prefix and committing the result.
---

# Add Dotfile to chezmoi

Guide the user through adding a new configuration file to chezmoi management safely and correctly.

## Instructions

### 1. Identify the Target File

If the user provided a path (e.g. `/add-dotfile ~/.config/starship.toml`), use that.
Otherwise, ask which file they want to add.

Check whether the file exists:

```bash
ls -la <target-path>
```

### 2. Determine the Correct Prefix

Inspect the file content to decide whether `private_` is needed:

```bash
cat <target-path>
```

Apply this decision table:

| File contains | Recommended prefix |
|---|---|
| API keys, tokens, passwords, private keys | `private_` required |
| Personal info (email, username, etc.) | `private_` recommended |
| Only tool settings (theme, keybindings, etc.) | No `private_` needed |
| Executable script | `executable_` required |

Ask the user to confirm the prefix choice before proceeding.

### 3. Add to chezmoi

```bash
# For a regular file
chezmoi add <target-path>

# For a file that should be private
chezmoi add --encrypt <target-path>   # if encryption is configured
# or rely on chezmoi inferring private_ from permissions

# Verify the source path chezmoi created
chezmoi source-path <target-path>
```

### 4. Verify the Result

```bash
chezmoi diff <target-path>
chezmoi status
```

Confirm that:
- The source file exists with the expected name under `~/.local/share/chezmoi/`
- `chezmoi diff` shows no unintended changes

### 5. Apply and Test

```bash
chezmoi apply <target-path>
```

Verify the deployed file looks correct.

### 6. Commit

Stage only the newly added source file and commit:

```bash
git -C ~/.local/share/chezmoi add <source-relative-path>
git -C ~/.local/share/chezmoi commit -m "feat(<tool>): add <filename> to chezmoi"
```

Use the tool name (e.g. `starship`, `ghostty`, `git`) as the commit scope.

## Output

Report:
- The source path that was created (e.g. `private_dot_config/starship.toml`)
- The target path it deploys to
- Whether `private_` was applied and why
- The commit that was created

$ARGUMENTS
