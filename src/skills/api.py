"""API integration for PubMed and Google Scholar."""

import time
from typing import Optional
from Bio import Entrez, Medline
from scholarly import scholarly
from ..models.paper import Paper
from ..config import config


# Set email for Entrez (required by NCBI)
Entrez.email = config.entrez_email


def search_pubmed(query: str, max_results: int = 20) -> list[Paper]:
    """
    Search PubMed for scientific papers.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of Paper objects with metadata

    Raises:
        Exception: If PubMed API call fails
    """
    papers = []

    try:
        # Search for PMIDs
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)  # type: ignore
        handle.close()

        pmids = record["IdList"]  # type: ignore

        if not pmids:
            return papers

        # Fetch details for each PMID
        handle = Entrez.efetch(db="pubmed", id=pmids, rettype="medline", retmode="text")
        records = Medline.parse(handle)

        for record in records:
            # Extract metadata
            pmid = record.get("PMID", "")
            title = record.get("TI", "")
            abstract = record.get("AB", "")
            authors = record.get("AU", [])
            year_str = record.get("DP", "")

            # Parse year
            year = None
            if year_str:
                try:
                    year = int(year_str.split()[0])
                except (ValueError, IndexError):
                    pass

            # Create Paper object
            paper = Paper(
                title=title,
                authors=authors,
                abstract=abstract if abstract else None,
                year=year,
                pmid=pmid,
                doi=record.get("LID", None),  # DOI sometimes in LID field
                url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                source="pubmed",
            )
            papers.append(paper)

        handle.close()

    except Exception as e:
        raise Exception(f"PubMed search failed: {str(e)}") from e

    return papers


def search_scholar(query: str, max_results: int = 20) -> list[Paper]:
    """
    Search Google Scholar for scientific papers.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of Paper objects with metadata

    Note:
        Google Scholar may rate limit requests. This function includes
        delays to avoid being blocked.
    """
    papers = []

    try:
        search_query = scholarly.search_pubs(query)

        count = 0
        for result in search_query:
            if count >= max_results:
                break

            # Extract metadata
            bib = result.get("bib", {})
            title = bib.get("title", "")
            authors = bib.get("author", [])
            if isinstance(authors, str):
                authors = [authors]
            abstract = bib.get("abstract", None)
            year_raw = bib.get("pub_year", None)
            year: int | None = None
            if year_raw:
                try:
                    year = int(year_raw)
                except ValueError:
                    year = None

            # Get URL
            url = result.get("pub_url") or result.get("eprint_url")

            # Citation count
            citation_count = result.get("num_citations", None)

            paper = Paper(
                title=title,
                authors=authors,
                abstract=abstract,
                year=year,
                url=url,
                source="scholar",
                citation_count=citation_count,
            )
            papers.append(paper)
            count += 1

            # Polite delay to avoid rate limiting
            time.sleep(2)

    except Exception as e:
        # Don't raise on Scholar errors, just return what we got
        # Scholar is fragile and often gets blocked
        print(f"Warning: Google Scholar search encountered error: {str(e)}")

    return papers


def fetch_pmc_fulltext(pmcid: str) -> Optional[str]:
    """
    Fetch full text from PubMed Central.

    Args:
        pmcid: PubMed Central ID (e.g., "PMC1234567")

    Returns:
        Full text as string, or None if unavailable

    Note:
        This is a simplified implementation. Production code should
        handle XML parsing more robustly.
    """
    try:
        # Remove PMC prefix if present
        pmc_id = pmcid.replace("PMC", "")

        handle = Entrez.efetch(db="pmc", id=pmc_id, rettype="xml", retmode="text")
        content = handle.read()
        handle.close()

        # In a real implementation, parse the XML to extract clean text
        # For now, return raw content (which will include XML tags)
        return content

    except Exception:
        return None


def fetch_abstract(pmid: str) -> Optional[str]:
    """
    Fetch abstract for a PubMed article.

    Args:
        pmid: PubMed ID

    Returns:
        Abstract text, or None if unavailable
    """
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
        abstract = handle.read()
        handle.close()
        return abstract

    except Exception:
        return None
