# Claude Code Configuration

This directory contains Claude Code configuration for the scientific literature agent project.

## Structure

```
.claude/
├── config.json         # Project configuration
├── commands/           # Custom slash commands
│   ├── search.md      # /search - Run test searches
│   ├── test.md        # /test - Run test suite
│   └── format.md      # /format - Format and lint code
└── hooks/              # Event hooks
    └── pre-commit.md  # Pre-commit quality checks
```

## Slash Commands

### /search {query}
Run a test literature search with the specified query.

**Example:**
```
/search CRISPR gene editing
```

### /test
Run the pytest test suite.

**Example:**
```
/test
```

### /format
Format code with Black and lint with Ruff.

**Example:**
```
/format
```

## Hooks

### pre-commit
Runs before git commits to ensure:
- Code is formatted
- Linting passes
- No secrets are committed
- Tests pass (if applicable)

## Configuration

The `config.json` file defines:
- Project metadata
- Python/UV settings
- Testing configuration
- Important files for context
- Exclusion patterns

## Usage with Claude Code

Claude Code will automatically:
1. Load this configuration when working in this directory
2. Make slash commands available via `/command-name`
3. Execute hooks at appropriate times
4. Use context hints for better assistance

## Customization

Feel free to add more:
- **Commands**: Create new `.md` files in `commands/`
- **Hooks**: Add event handlers in `hooks/`
- **Settings**: Modify `config.json` for project-specific needs
