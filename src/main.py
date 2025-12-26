"""Main entry point for scientific literature agent."""

import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from .graph import run_literature_search
from .config import config


console = Console()


def format_output(result) -> str:
    """
    Format the agent result for display.

    Args:
        result: AgentState from workflow execution

    Returns:
        Formatted string for output
    """
    sections = []

    # Header
    sections.append("# Literature Search Results\n")
    sections.append(f"**Query**: {result.query}\n")

    # Search Statistics
    if result.search_metadata:
        meta = result.search_metadata
        sections.append("\n## Search Statistics")
        sections.append(f"- PubMed results: {meta.pubmed_count}")
        sections.append(f"- Google Scholar results: {meta.scholar_count}")
        sections.append(f"- Total unique papers: {meta.total_results}")
        sections.append(f"- Duplicates removed: {meta.duplicates_removed}")
        sections.append(f"- Search time: {meta.execution_time_seconds:.2f} seconds\n")

    # Retrieval Statistics
    if result.retrieval_stats:
        stats = result.retrieval_stats
        sections.append("\n## Retrieval Statistics")
        sections.append(f"- Documents attempted: {stats.attempted}")
        sections.append(f"- Full text retrieved: {stats.fulltext_retrieved}")
        sections.append(f"- Abstracts retrieved: {stats.abstract_retrieved}")
        sections.append(f"- Failed: {stats.failed}")
        sections.append(f"- Total words: {stats.total_words:,}")
        sections.append(
            f"- Retrieval time: {stats.execution_time_seconds:.2f} seconds\n"
        )

    # Summary
    if result.summary:
        sections.append("\n---\n")
        sections.append(result.summary)

    # Literature Section
    if result.literature_section:
        sections.append("\n\n---\n")
        sections.append(result.literature_section)

    # Generation Statistics
    if result.generation_metadata:
        meta = result.generation_metadata
        sections.append("\n\n## Generation Statistics")
        sections.append(f"- Model: {meta.model_used}")
        if meta.total_tokens:
            sections.append(f"- Total tokens: {meta.total_tokens:,}")
            sections.append(f"- Prompt tokens: {meta.prompt_tokens:,}")
            sections.append(f"- Completion tokens: {meta.completion_tokens:,}")
        sections.append(f"- Generation time: {meta.execution_time_seconds:.2f} seconds")

    # Errors
    if result.errors:
        sections.append("\n\n## Errors/Warnings")
        for error in result.errors:
            sections.append(f"- {error}")

    return "\n".join(sections)


def save_output(content: str, query: str) -> Path:
    """
    Save output to a file.

    Args:
        content: Formatted output content
        query: Original search query

    Returns:
        Path to saved file
    """
    output_dir = config.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create filename from query
    filename = "".join(c if c.isalnum() else "_" for c in query[:50])
    output_path = output_dir / f"{filename}.md"

    # Handle duplicate filenames
    counter = 1
    while output_path.exists():
        output_path = output_dir / f"{filename}_{counter}.md"
        counter += 1

    output_path.write_text(content, encoding="utf-8")
    return output_path


def main():
    """
    Main CLI entry point.

    Usage:
        python -m src.main "your search query"
        python -m src.main "CRISPR gene editing" --max-results 30
    """
    if len(sys.argv) < 2:
        console.print(
            Panel(
                "[red]Error:[/red] No search query provided.\n\n"
                "[yellow]Usage:[/yellow]\n"
                '  python -m src.main "your search query"\n'
                '  python -m src.main "CRISPR gene editing"\n\n'
                "[yellow]Environment Variables:[/yellow]\n"
                "  LLM_MODEL - Default: mistral/mistral-small-latest\n"
                "  MAX_RESULTS - Default: 20\n"
                "  ENTREZ_EMAIL - Required for NCBI API\n"
                "  VERBOSE - Enable verbose logging",
                title="Scientific Literature Agent",
                border_style="red",
            )
        )
        sys.exit(1)

    query = sys.argv[1]

    # Parse optional arguments
    max_results = config.max_results_per_source
    if "--max-results" in sys.argv:
        idx = sys.argv.index("--max-results")
        if idx + 1 < len(sys.argv):
            max_results = int(sys.argv[idx + 1])

    # Display search info
    console.print(
        Panel(
            f"[bold]Query:[/bold] {query}\n"
            f"[bold]Max Results:[/bold] {max_results} per source\n"
            f"[bold]Model:[/bold] {config.default_model}",
            title="Starting Literature Search",
            border_style="blue",
        )
    )

    try:
        # Run the workflow
        with console.status("[bold green]Searching literature..."):
            result = run_literature_search(
                query=query, max_results=max_results, model=config.default_model
            )

        # Format output
        output = format_output(result)

        # Display results
        console.print("\n")
        console.print(Markdown(output))

        # Save if configured
        if config.save_results:
            output_path = save_output(output, query)
            console.print(
                f"\n[green]✓[/green] Results saved to: [blue]{output_path}[/blue]"
            )

    except KeyboardInterrupt:
        console.print("\n[yellow]Search cancelled by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        if config.verbose:
            console.print_exception()
        sys.exit(1)


if __name__ == "__main__":
    main()
