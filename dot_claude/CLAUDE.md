# Claude Code Configuration

## General Guidelines
- **You must think exclusively in English**. However, you are required to **respond in Japanese**.

## Session Initialization

**Required Action**: Before providing any command-line suggestions or executing shell commands, read `~/.zshrc` to understand the current alias configuration. Pay special attention to:

- Rust-based tool aliases (`lsd`, `fd`, `bat`, etc.)
- Git pager settings
- Any custom command configurations

This ensures all command suggestions align with the actual shell environment.

## Development Workflow Preferences

### Project Structure

#### Python Projects
- **src** directory for source code
- **tests** directory for unit tests
- **docs** directory for documentation
- Uses **uv** for Python package management
- **pytest** for testing with AAA pattern (Arrange-Act-Assert)

### Code Style

#### Python
- PEP 8 compliant, type hints preferred
- Use `ruff` for linting and formatting
- Use `ty` for type checking
- Use `pre-commit` hooks for automatic formatting and linting
- Use `semantic-release` for versioning and changelog generation
- **Line length**: 88 characters (Ruff standard)
- **Import order**: Standard lib, third-party, local modules
- **Docstrings**: Google style preferred
- **Logging**: Never use f-strings in logging statements
- **Standalone Python Script**: If external modules are needed, follow [PEP 723](https://peps.python.org/pep-0723/) guidelines

### Git Workflow
- Uses conventional commits
- Prefers feature branches
- Code review through PRs
- Uses semantic versioning

### Test-Driven Development (TDD)
- Write tests before implementing features
- Use t-wada's recommended method for TDD
