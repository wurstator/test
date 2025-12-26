# Setup Guide

Quick start guide for setting up the scientific literature agent.

## Prerequisites

- Python 3.11 or higher
- [UV package manager](https://github.com/astral-sh/uv)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd scientific-literature-agent
```

### 2. Install Dependencies

```bash
# Install all dependencies with UV
uv sync

# Or install with dev dependencies
uv sync --all-extras
```

### 3. Configure Environment

```bash
# Copy the default environment file
cp .env.default .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

**Required configuration:**
```bash
# Set your email for NCBI PubMed API (required!)
ENTREZ_EMAIL=your.email@example.com
```

**Optional configuration:**
```bash
# If using OpenAI
OPENAI_API_KEY=sk-...

# If using Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...

# If using Mistral AI
MISTRAL_API_KEY=...

# Or use local models (no API key needed)
LLM_MODEL=ollama/llama2
```

### 4. Verify Installation

```bash
# Test the installation
uv run python -m src.main "test query" --max-results 5
```

## Configuration Files

### Environment Files

| File | Purpose | Track in Git? |
|------|---------|--------------|
| `.env.default` | Template with safe defaults | ✅ Yes |
| `.env.example` | Alternative template | ✅ Yes |
| `.env` | Your actual configuration | ❌ No (contains secrets) |

### Claude Code Configuration

| File/Dir | Purpose |
|----------|---------|
| `.claude/config.json` | Project settings for Claude Code |
| `.claude/commands/` | Custom slash commands |
| `.claude/hooks/` | Event hooks |

## Usage

### Basic Search

```bash
# Run a literature search
uv run python -m src.main "CRISPR gene editing"

# Limit results
uv run python -m src.main "machine learning" --max-results 30

# Use different model
LLM_MODEL=gpt-4 uv run python -m src.main "quantum computing"
```

### With Claude Code

If using Claude Code, you can use slash commands:

```
/search CRISPR gene editing
/test
/format
```

### Programmatic Usage

```python
from src.graph import run_literature_search

result = run_literature_search(
    query="artificial intelligence in medicine",
    max_results=20,
    model="mistral/mistral-small-latest"
)

print(result.summary)
print(result.literature_section)
```

## Development Setup

### Install Dev Dependencies

```bash
uv sync --all-extras
```

This installs:
- pytest - Testing framework
- black - Code formatter
- ruff - Linter

### Run Tests

```bash
uv run pytest
```

### Format Code

```bash
# Format with Black
uv run black src/

# Lint with Ruff
uv run ruff check src/

# Auto-fix issues
uv run ruff check src/ --fix
```

## Troubleshooting

### "No module named 'src'"

Make sure you're running from the project root directory:
```bash
cd /path/to/scientific-literature-agent
uv run python -m src.main "query"
```

### "ENTREZ_EMAIL is required"

Set your email in `.env`:
```bash
echo "ENTREZ_EMAIL=your.email@example.com" >> .env
```

### "LLM call failed"

1. Check your API key is set correctly
2. Verify the model name is valid
3. Ensure you have API credits/quota
4. Try using a local model (no API key needed):
   ```bash
   LLM_MODEL=ollama/llama2 uv run python -m src.main "query"
   ```

### "Google Scholar rate limited"

This is normal. Scholar aggressively rate limits. Options:
- Wait a few hours and retry
- Use only PubMed (still very effective)
- Reduce max_results

## Next Steps

1. ✅ Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
2. ✅ Read [README.md](README.md) for detailed documentation
3. ✅ Try running a few test searches
4. ✅ Customize prompts in `src/prompts/` for your use case
5. ✅ Explore the code in `src/` to understand the workflow

## Support

For issues or questions:
- Check the [README.md](README.md) troubleshooting section
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for design details
- Open an issue on GitHub
