# Session Management

## Initialization
**Required Action**: Before providing any command-line suggestions or executing shell commands, read `~/.zshrc` to understand the current alias configuration. Pay special attention to:
- Rust-based tool aliases (`lsd`, `fd`, `bat`, etc.)
- Git pager settings
- Any custom command configurations

## Progress Preservation
When sessions end mid-implementation, always save progress by committing partial work with 'WIP:' prefix or leaving a TODO comment summarizing next steps.

## Task Completion
For PR-related tasks, always complete the full generation/implementation before pausing - PR descriptions, review responses, and refactoring should be atomic operations.
