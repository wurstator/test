"""Document retrieval agent for fetching full text or abstracts."""

import time
from ..models.state import AgentState, RetrievalStats
from ..skills.api import fetch_pmc_fulltext, fetch_abstract
from ..skills.document import create_document_from_paper


def retrieve_documents(state: AgentState) -> AgentState:
    """
    Retrieve full text or abstracts for search results.

    Args:
        state: Current agent state containing search_results

    Returns:
        Updated AgentState with documents and retrieval_stats

    Strategy:
        1. For PubMed papers: Try PMC full text -> fallback to abstract
        2. For Scholar papers: Use abstract from search results
        3. Track statistics for retrieval success
    """
    start_time = time.time()

    papers = state.search_results
    documents = []
    errors = []

    stats = {
        "attempted": 0,
        "fulltext_retrieved": 0,
        "abstract_retrieved": 0,
        "failed": 0,
        "total_words": 0,
    }

    for paper in papers:
        stats["attempted"] += 1
        content = None
        content_type = None

        try:
            # Strategy 1: Try full text for PubMed papers with PMC ID
            if paper.source == "pubmed" and paper.pmcid:
                content = fetch_pmc_fulltext(paper.pmcid)
                if content:
                    content_type = "fulltext"
                    stats["fulltext_retrieved"] += 1

            # Strategy 2: Fallback to abstract
            if not content:
                if paper.abstract:
                    content = paper.abstract
                    content_type = "abstract"
                    stats["abstract_retrieved"] += 1
                elif paper.pmid:
                    # Try fetching abstract from PubMed
                    content = fetch_abstract(paper.pmid)
                    if content:
                        content_type = "abstract"
                        stats["abstract_retrieved"] += 1

            # Create document if we got content
            if content and content_type:
                doc = create_document_from_paper(paper, content, content_type)
                documents.append(doc)
                stats["total_words"] += doc.word_count
            else:
                stats["failed"] += 1
                errors.append(f"No content available for: {paper.title}")

        except Exception as e:
            stats["failed"] += 1
            errors.append(f"Retrieval failed for {paper.title}: {str(e)}")

    # Create statistics
    execution_time = time.time() - start_time
    retrieval_stats = RetrievalStats(
        attempted=stats["attempted"],
        fulltext_retrieved=stats["fulltext_retrieved"],
        abstract_retrieved=stats["abstract_retrieved"],
        failed=stats["failed"],
        total_words=stats["total_words"],
        execution_time_seconds=execution_time,
    )

    return state.model_copy(
        update={
            "documents": documents,
            "retrieval_stats": retrieval_stats,
            "errors": state.errors + errors,
        }
    )
