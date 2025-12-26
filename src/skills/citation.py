"""Citation formatting utilities."""

from ..models.paper import Paper, Citation


def format_authors_apa(authors: list[str]) -> str:
    """
    Format author list in APA style.

    Args:
        authors: List of author names

    Returns:
        Formatted author string

    Examples:
        ["Smith, J."] -> "Smith, J."
        ["Smith, J.", "Jones, M."] -> "Smith, J., & Jones, M."
        ["Smith, J.", "Jones, M.", "Brown, K."] -> "Smith, J., Jones, M., & Brown, K."
    """
    if not authors:
        return ""

    if len(authors) == 1:
        return authors[0]

    if len(authors) == 2:
        return f"{authors[0]}, & {authors[1]}"

    # 3 or more authors
    return ", ".join(authors[:-1]) + f", & {authors[-1]}"


def format_citation_apa(paper: Paper) -> str:
    """
    Format a paper citation in APA 7th edition style.

    Args:
        paper: Paper object to format

    Returns:
        Formatted citation string
    """
    parts = []

    # Authors
    if paper.authors:
        authors_str = format_authors_apa(paper.authors)
        parts.append(authors_str)

    # Year
    year_str = f"({paper.year})" if paper.year else "(n.d.)"
    parts.append(year_str)

    # Title
    if paper.title:
        parts.append(f"{paper.title}.")

    # Source-specific formatting
    if paper.source == "pubmed" and paper.pmid:
        parts.append(f"PubMed PMID: {paper.pmid}.")
        if paper.url:
            parts.append(paper.url)

    elif paper.doi:
        parts.append(f"https://doi.org/{paper.doi}")

    elif paper.url:
        parts.append(paper.url)

    return " ".join(parts)


def create_in_text_citation(paper: Paper) -> str:
    """
    Create a short in-text citation.

    Args:
        paper: Paper object

    Returns:
        In-text citation in format [FirstAuthorYear]

    Examples:
        [Smith2020]
        [Jones2019]
    """
    if not paper.authors:
        author_part = "Unknown"
    else:
        # Extract last name from first author
        first_author = paper.authors[0]
        # Handle formats like "Smith, J." or "John Smith"
        if "," in first_author:
            author_part = first_author.split(",")[0].strip()
        else:
            author_part = first_author.split()[-1].strip()

    year_part = str(paper.year) if paper.year else "n.d."

    return f"[{author_part}{year_part}]"


def create_citation(paper: Paper) -> Citation:
    """
    Create a Citation object from a Paper.

    Args:
        paper: Paper object

    Returns:
        Citation object with formatted text
    """
    citation_text = format_citation_apa(paper)
    in_text = create_in_text_citation(paper)

    return Citation(
        paper=paper, citation_text=citation_text, in_text_citation=in_text
    )


def generate_references_section(citations: list[Citation]) -> str:
    """
    Generate a formatted references section from citations.

    Args:
        citations: List of Citation objects

    Returns:
        Formatted references section as string
    """
    if not citations:
        return "## References\n\nNo references available."

    # Sort citations alphabetically by first author
    sorted_citations = sorted(
        citations, key=lambda c: c.paper.authors[0] if c.paper.authors else ""
    )

    references = ["## References\n"]
    for citation in sorted_citations:
        references.append(citation.citation_text)

    return "\n\n".join(references)
