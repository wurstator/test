"""Pydantic models for LangGraph state management."""

from typing import Optional
from pydantic import BaseModel, Field
from .paper import Paper, Document, Citation


class SearchMetadata(BaseModel):
    """Metadata about search execution."""

    pubmed_count: int = 0
    scholar_count: int = 0
    total_results: int = 0
    duplicates_removed: int = 0
    execution_time_seconds: float = 0.0


class RetrievalStats(BaseModel):
    """Statistics about document retrieval."""

    attempted: int = 0
    fulltext_retrieved: int = 0
    abstract_retrieved: int = 0
    failed: int = 0
    total_words: int = 0
    execution_time_seconds: float = 0.0


class GenerationMetadata(BaseModel):
    """Metadata about summary generation."""

    model_used: str
    total_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    execution_time_seconds: float = 0.0


class AgentState(BaseModel):
    """Complete state for the LangGraph workflow."""

    # Input
    query: str
    max_results: int = Field(default=20, description="Max results per source")
    model: str = Field(default="mistral/mistral-small-latest")

    # Search stage
    search_results: list[Paper] = Field(default_factory=list)
    search_metadata: Optional[SearchMetadata] = None

    # Retrieval stage
    documents: list[Document] = Field(default_factory=list)
    retrieval_stats: Optional[RetrievalStats] = None

    # Summary stage
    summary: Optional[str] = None
    references: list[Citation] = Field(default_factory=list)
    literature_section: Optional[str] = None
    generation_metadata: Optional[GenerationMetadata] = None

    # Error tracking
    errors: list[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


# Type annotation for LangGraph state updates
def add_messages(left: list, right: list) -> list:
    """Merge lists for state updates."""
    return left + right
