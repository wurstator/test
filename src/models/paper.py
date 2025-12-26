"""Pydantic models for papers and documents."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Paper(BaseModel):
    """Metadata for a scientific paper."""

    title: str
    authors: list[str]
    abstract: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    pmcid: Optional[str] = None
    url: Optional[str] = None
    source: str = Field(description="Source database: pubmed or scholar")
    citation_count: Optional[int] = None

    class Config:
        frozen = True  # Immutable


class Document(BaseModel):
    """Full document content with metadata."""

    paper: Paper
    content: str = Field(description="Full text or abstract")
    content_type: str = Field(description="fulltext or abstract")
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)
    word_count: int = Field(default=0)

    class Config:
        frozen = True

    def __init__(self, **data):
        super().__init__(**data)
        if self.word_count == 0:
            object.__setattr__(self, "word_count", len(self.content.split()))


class Citation(BaseModel):
    """Formatted citation."""

    paper: Paper
    citation_text: str = Field(description="Formatted citation (e.g., APA)")
    in_text_citation: str = Field(description="Short form for in-text use")

    class Config:
        frozen = True
