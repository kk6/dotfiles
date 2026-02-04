# Python Development Standards

## Project Structure
- **src** directory for source code
- **tests** directory for unit tests
- **docs** directory for documentation
- Uses **uv** for Python package management
- **pytest** for testing with AAA pattern (Arrange-Act-Assert)

## Code Style
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

## Debugging Patterns
When debugging duplicate key/ID errors in Python, first check if multiple data sources could be producing the same identifiers, then implement unique composite keys.
