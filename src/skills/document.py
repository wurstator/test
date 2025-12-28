"""Document processing utilities."""

from pathlib import Path
import requests
from pypdf import PdfReader
from ..models.paper import Paper, Document


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """
    Extract text content from a PDF file.

    Args:
        pdf_path: Path to PDF file

    Returns:
        Extracted text as string

    Raises:
        Exception: If PDF cannot be read
    """
    try:
        reader = PdfReader(pdf_path)
        text_parts = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

        return "\n\n".join(text_parts)

    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}") from e


def download_pdf(url: str, output_path: str | Path) -> bool:
    """
    Download a PDF from a URL.

    Args:
        url: URL to download from
        output_path: Where to save the PDF

    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        return True

    except Exception:
        return False


def parse_metadata(raw_result: dict) -> Paper:
    """
    Standardize metadata from different sources into Paper model.

    Args:
        raw_result: Raw metadata dict from API

    Returns:
        Standardized Paper object

    Note:
        This is a generic parser. In practice, you'd have source-specific
        parsers for better accuracy.
    """
    return Paper(
        title=raw_result.get("title", ""),
        authors=raw_result.get("authors", []),
        abstract=raw_result.get("abstract"),
        year=raw_result.get("year"),
        doi=raw_result.get("doi"),
        pmid=raw_result.get("pmid"),
        pmcid=raw_result.get("pmcid"),
        url=raw_result.get("url"),
        source=raw_result.get("source", "unknown"),
        citation_count=raw_result.get("citation_count"),
    )


def deduplicate_results(papers: list[Paper]) -> list[Paper]:
    """
    Remove duplicate papers based on DOI or title similarity.

    Args:
        papers: List of Paper objects

    Returns:
        Deduplicated list of Paper objects

    Note:
        Uses simple exact matching. Production code should use
        fuzzy matching for titles.
    """
    seen_dois = set()
    seen_titles = set()
    unique_papers = []

    for paper in papers:
        # Check DOI first (most reliable)
        if paper.doi:
            if paper.doi.lower() in seen_dois:
                continue
            seen_dois.add(paper.doi.lower())

        # Check title (fallback)
        title_normalized = paper.title.lower().strip()
        if title_normalized in seen_titles:
            continue
        seen_titles.add(title_normalized)

        unique_papers.append(paper)

    return unique_papers


def create_document_from_paper(
    paper: Paper, content: str, content_type: str
) -> Document:
    """
    Create a Document object from a Paper and its content.

    Args:
        paper: Paper metadata
        content: Full text or abstract
        content_type: "fulltext" or "abstract"

    Returns:
        Document object
    """
    return Document(paper=paper, content=content, content_type=content_type)


def truncate_content(content: str, max_words: int = 10000) -> str:
    """
    Truncate content to a maximum number of words.

    Args:
        content: Text content
        max_words: Maximum words to keep

    Returns:
        Truncated content
    """
    words = content.split()
    if len(words) <= max_words:
        return content

    return " ".join(words[:max_words]) + "\n\n[Content truncated...]"
