"""Search agent for PubMed and Google Scholar."""

import time
from ..models.state import AgentState, SearchMetadata
from ..skills.api import search_pubmed, search_scholar
from ..skills.document import deduplicate_results


def search_literature(state: AgentState) -> AgentState:
    """
    Execute parallel searches on PubMed and Google Scholar.

    Args:
        state: Current agent state containing query and max_results

    Returns:
        Updated AgentState with search_results and search_metadata
    """
    start_time = time.time()

    query = state.query
    max_results = state.max_results

    # Search both sources
    pubmed_results = []
    scholar_results = []
    errors = []

    # PubMed search
    try:
        pubmed_results = search_pubmed(query, max_results)
    except Exception as e:
        errors.append(f"PubMed search failed: {str(e)}")

    # Google Scholar search
    try:
        scholar_results = search_scholar(query, max_results)
    except Exception as e:
        errors.append(f"Scholar search failed: {str(e)}")

    # Combine results
    all_results = pubmed_results + scholar_results
    initial_count = len(all_results)

    # Deduplicate
    unique_results = deduplicate_results(all_results)
    duplicates_removed = initial_count - len(unique_results)

    # Create metadata
    execution_time = time.time() - start_time
    metadata = SearchMetadata(
        pubmed_count=len(pubmed_results),
        scholar_count=len(scholar_results),
        total_results=len(unique_results),
        duplicates_removed=duplicates_removed,
        execution_time_seconds=execution_time,
    )

    return state.model_copy(
        update={
            "search_results": unique_results,
            "search_metadata": metadata,
            "errors": state.errors + errors,
        }
    )
