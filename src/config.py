"""Configuration management for scientific literature agent."""

import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config(BaseModel):
    """Application configuration."""

    # LLM Settings
    default_model: str = Field(
        default="mistral/mistral-small-latest",
        description="Default LLM model for summarization",
    )
    temperature: float = Field(default=0.7, description="LLM temperature")
    max_tokens: int = Field(default=4000, description="Max tokens for LLM responses")

    # Search Settings
    max_results_per_source: int = Field(
        default=20, description="Max results from each source (PubMed, Scholar)"
    )
    enable_pubmed: bool = Field(default=True, description="Enable PubMed search")
    enable_scholar: bool = Field(default=True, description="Enable Google Scholar")

    # API Settings
    entrez_email: str = Field(
        default="research@example.com", description="Email for NCBI Entrez API"
    )
    request_timeout: int = Field(default=30, description="HTTP request timeout (seconds)")

    # Document Processing
    max_document_words: int = Field(
        default=5000, description="Max words per document for summarization"
    )
    prefer_fulltext: bool = Field(
        default=True, description="Prefer full text over abstracts"
    )

    # Output Settings
    citation_style: str = Field(default="apa", description="Citation style (apa, chicago, etc.)")
    save_results: bool = Field(default=False, description="Save results to disk")
    output_dir: Path = Field(default=Path("./output"), description="Output directory")

    # Debug Settings
    verbose: bool = Field(default=False, description="Enable verbose logging")
    litellm_verbose: bool = Field(default=False, description="Enable LiteLLM verbose mode")

    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.

        Environment variables:
            - LLM_MODEL: Default LLM model
            - MAX_RESULTS: Max results per source
            - ENTREZ_EMAIL: Email for NCBI API
            - VERBOSE: Enable verbose mode
            - And more...

        Returns:
            Config instance
        """
        return cls(
            default_model=os.getenv("LLM_MODEL", "mistral/mistral-small-latest"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_results_per_source=int(os.getenv("MAX_RESULTS", "20")),
            entrez_email=os.getenv("ENTREZ_EMAIL", "research@example.com"),
            verbose=os.getenv("VERBOSE", "false").lower() == "true",
            litellm_verbose=os.getenv("LITELLM_VERBOSE", "false").lower() == "true",
        )


# Global config instance
config = Config.from_env()
