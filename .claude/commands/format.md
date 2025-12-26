Format and lint all Python code in the project.

Run:
1. `uv run black src/` - Format code with Black
2. `uv run ruff check src/` - Lint with Ruff
3. `uv run ruff check src/ --fix` - Auto-fix linting issues where possible

Display any remaining issues that need manual attention.
