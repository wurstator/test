"""Summary generation agent using LLM."""

import time
from ..models.state import AgentState, GenerationMetadata
from ..skills.llm import call_llm_with_template, format_prompt, load_prompt_template
from ..skills.citation import create_citation, generate_references_section
from ..skills.document import truncate_content


def generate_summary(state: AgentState) -> dict:
    """
    Generate comprehensive summary from retrieved documents.

    Args:
        state: Current agent state with documents and query

    Returns:
        State update dict with summary, references, literature_section,
        and generation_metadata

    Process:
        1. Format documents for LLM context
        2. Generate summary using summarization template
        3. Create citations for all papers
        4. Generate formatted references section
    """
    start_time = time.time()

    documents = state.documents
    query = state.query
    model = state.model
    errors = []

    if not documents:
        return {
            "summary": "No documents were retrieved. Unable to generate summary.",
            "references": [],
            "literature_section": "## References\n\nNo references available.",
            "generation_metadata": GenerationMetadata(
                model_used=model, execution_time_seconds=0.0
            ),
            "errors": ["No documents available for summarization"],
        }

    # Step 1: Format documents for LLM
    doc_texts = []
    for i, doc in enumerate(documents, 1):
        paper = doc.paper
        authors_str = ", ".join(paper.authors[:3])  # First 3 authors
        if len(paper.authors) > 3:
            authors_str += " et al."

        year = paper.year or "n.d."

        # Truncate very long content
        content = truncate_content(doc.content, max_words=5000)

        doc_text = f"""
### Document {i}: {paper.title}
**Authors**: {authors_str}
**Year**: {year}
**Type**: {doc.content_type}
**Source**: {paper.source}

{content}
"""
        doc_texts.append(doc_text)

    documents_formatted = "\n\n---\n\n".join(doc_texts)

    # Step 2: Generate summary using LLM
    try:
        summary_response, metadata = call_llm_with_template(
            template_name="summarization",
            model=model,
            temperature=0.7,
            query=query,
            documents=documents_formatted,
        )
        summary = summary_response

    except Exception as e:
        errors.append(f"Summary generation failed: {str(e)}")
        summary = f"Error generating summary: {str(e)}"
        metadata = {}

    # Step 3: Create citations
    citations = [create_citation(doc.paper) for doc in documents]

    # Step 4: Generate references section
    try:
        # Option 1: Use LLM to format references (more consistent)
        citations_text = "\n\n".join([c.citation_text for c in citations])
        template = load_prompt_template("literature_section")
        lit_prompt = format_prompt(template, citations=citations_text)

        lit_section, _ = call_llm_with_template(
            template_name="literature_section",
            model=model,
            temperature=0.0,  # Lower temperature for formatting
            citations=citations_text,
        )

        # Option 2: Direct formatting (fallback)
        if not lit_section or "error" in lit_section.lower():
            lit_section = generate_references_section(citations)

    except Exception as e:
        errors.append(f"References generation failed: {str(e)}")
        lit_section = generate_references_section(citations)

    # Create metadata
    execution_time = time.time() - start_time
    gen_metadata = GenerationMetadata(
        model_used=model,
        total_tokens=metadata.get("total_tokens"),
        prompt_tokens=metadata.get("prompt_tokens"),
        completion_tokens=metadata.get("completion_tokens"),
        execution_time_seconds=execution_time,
    )

    return {
        "summary": summary,
        "references": citations,
        "literature_section": lit_section,
        "generation_metadata": gen_metadata,
        "errors": errors,
    }
