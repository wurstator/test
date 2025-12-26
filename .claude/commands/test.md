Run the test suite for the scientific literature agent.

Execute: `uv run pytest -v`

If tests don't exist yet, create basic unit tests for:
- API functions (search_pubmed, search_scholar)
- Document processing (deduplication, PDF extraction)
- Citation formatting
- State management
