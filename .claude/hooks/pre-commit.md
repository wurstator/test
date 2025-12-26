# Pre-Commit Hook

Before committing code, ensure:

1. **Code is formatted**: Run `uv run black src/` to format all Python files
2. **Linting passes**: Run `uv run ruff check src/` to check for issues
3. **No secrets**: Verify no API keys or sensitive data in committed files
4. **Tests pass** (if applicable): Run `uv run pytest` if tests exist

This hook helps maintain code quality and prevent common mistakes.
