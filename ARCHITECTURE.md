# Scientific Literature Agent Architecture

## Overview
A LangGraph-based agent system for searching, retrieving, and summarizing scientific literature from Google Scholar and PubMed.

## Core Components

### 1. Agents

#### SearchAgent
- **Responsibility**: Execute searches on Google Scholar and PubMed
- **Skills**:
  - Query formulation and optimization
  - API integration with scholarly and Bio.Entrez
  - Result deduplication and ranking
- **Input**: User query (validated)
- **Output**: List of papers with metadata

#### RetrievalAgent
- **Responsibility**: Fetch full text or abstracts
- **Skills**:
  - Attempt full-text retrieval (PMC, arXiv, preprint servers)
  - Fallback to abstract extraction
  - PDF parsing and text extraction
- **Input**: Paper metadata
- **Output**: Document content (full text or abstract)

#### SummaryAgent
- **Responsibility**: Generate comprehensive summaries
- **Skills**:
  - Multi-document synthesis
  - Citation extraction and formatting
  - Literature section generation
- **Input**: Retrieved documents
- **Output**: Summary with references

### 2. State Management (Pydantic Models)

```
QueryState
├── query: str
├── validated: bool
└── metadata: dict

SearchState
├── query_state: QueryState
├── results: List[Paper]
└── search_metadata: SearchMetadata

RetrievalState
├── papers: List[Paper]
├── documents: List[Document]
└── retrieval_stats: RetrievalStats

SummaryState
├── documents: List[Document]
├── summary: str
├── references: List[Citation]
└── generation_metadata: GenerationMetadata
```

### 3. Skills (Reusable Functions)

#### API Integration
- `search_pubmed(query, max_results)` - PubMed search
- `search_scholar(query, max_results)` - Google Scholar search
- `fetch_pmc_fulltext(pmcid)` - Retrieve PMC full text
- `fetch_abstract(pmid)` - Retrieve abstract

#### Document Processing
- `extract_text_from_pdf(pdf_path)` - PDF text extraction
- `parse_metadata(raw_result)` - Standardize metadata
- `deduplicate_results(results)` - Remove duplicates by DOI/title

#### LLM Operations
- `call_llm(prompt, model, **kwargs)` - Unified LiteLLM wrapper
- `load_prompt_template(template_name)` - Load MD prompts
- `format_prompt(template, **variables)` - Populate templates

#### Citation & Formatting
- `format_citation(paper, style)` - Format citations (APA/Chicago/etc)
- `generate_references_section(citations)` - Create bibliography

### 4. Hooks

#### Pre-Search Hooks
- **validate_query_hook**: Ensure query is not empty and well-formed
- **query_expansion_hook**: Optionally expand query with synonyms

#### Post-Search Hooks
- **filter_results_hook**: Apply relevance/quality filters
- **deduplication_hook**: Remove duplicate papers

#### Pre-Retrieval Hooks
- **check_availability_hook**: Verify document accessibility
- **prioritize_fulltext_hook**: Sort by full-text availability

#### Post-Retrieval Hooks
- **quality_check_hook**: Validate retrieved content
- **length_check_hook**: Ensure sufficient content for summary

#### Pre-Summary Hooks
- **context_limit_hook**: Ensure content fits in context window
- **relevance_filter_hook**: Remove off-topic content

## LangGraph Workflow

```
START
  ↓
[Validate Query] → QueryState
  ↓
[Search Agents (Parallel)]
  ├── PubMed Search
  └── Scholar Search
  ↓
[Merge & Deduplicate] → SearchState
  ↓
[Retrieve Documents] → RetrievalState
  ↓
[Generate Summary] → SummaryState
  ↓
[Format Output]
  ↓
END
```

## Key Design Principles

1. **Parsimonious Design**: Single consolidated function per capability
2. **State Immutability**: Use Pydantic models, avoid in-place mutations
3. **Prompt Externalization**: All LLM prompts in `prompts/*.md`
4. **Error Resilience**: Graceful fallbacks (full-text → abstract → skip)
5. **LLM Flexibility**: LiteLLM for multi-provider support

## Configuration

- Default LLM: `mistral/mistral-small-latest`
- Max search results: 20 per source
- Retry logic: 3 attempts with exponential backoff
- Rate limiting: Respect API limits

## File Structure

```
.
├── pyproject.toml              # UV project config
├── src/
│   ├── agents/
│   │   ├── search_agent.py     # SearchAgent implementation
│   │   ├── retrieval_agent.py  # RetrievalAgent implementation
│   │   └── summary_agent.py    # SummaryAgent implementation
│   ├── models/
│   │   ├── state.py            # Pydantic state models
│   │   └── paper.py            # Paper/Document models
│   ├── skills/
│   │   ├── api.py              # API integration functions
│   │   ├── document.py         # Document processing
│   │   ├── llm.py              # LLM operations
│   │   └── citation.py         # Citation formatting
│   ├── hooks/
│   │   ├── validation.py       # Validation hooks
│   │   └── filtering.py        # Filtering hooks
│   ├── prompts/
│   │   ├── query_validation.md
│   │   ├── summarization.md
│   │   └── synthesis.md
│   ├── graph.py                # LangGraph workflow definition
│   ├── config.py               # Configuration management
│   └── main.py                 # Entry point
├── tests/
└── README.md
```

## Dependencies

- `langgraph` - Graph orchestration
- `litellm` - LLM API abstraction
- `pydantic` - State management
- `scholarly` - Google Scholar API
- `biopython` - PubMed/Entrez access
- `pypdf` - PDF parsing
- `requests` - HTTP client
- `python-dotenv` - Environment config
