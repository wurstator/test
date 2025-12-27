"""Visualize the Scientific Literature Agent architecture and workflow."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree
from rich import box


console = Console()


def show_architecture():
    """Display the overall architecture."""
    tree = Tree("📚 [bold cyan]Scientific Literature Agent[/bold cyan]")

    # Agents branch
    agents = tree.add("🤖 [bold yellow]Agents[/bold yellow]")
    agents.add("[green]SearchAgent[/green] - Parallel PubMed & Scholar search")
    agents.add("[green]RetrievalAgent[/green] - Fetch full text or abstracts")
    agents.add("[green]SummaryAgent[/green] - LLM-powered synthesis")

    # Models branch
    models = tree.add("📊 [bold yellow]Pydantic Models[/bold yellow]")
    state_branch = models.add("[blue]AgentState[/blue] - Workflow state")
    state_branch.add("query, max_results, model")
    state_branch.add("search_results, search_metadata")
    state_branch.add("documents, retrieval_stats")
    state_branch.add("summary, references, literature_section")
    models.add("[blue]Paper[/blue] - Paper metadata")
    models.add("[blue]Document[/blue] - Full text + metadata")
    models.add("[blue]Citation[/blue] - Formatted references")

    # Skills branch
    skills = tree.add("🛠️  [bold yellow]Skills[/bold yellow]")
    skills.add("[magenta]api.py[/magenta] - PubMed/Scholar integration")
    skills.add("[magenta]llm.py[/magenta] - LiteLLM wrapper")
    skills.add("[magenta]document.py[/magenta] - PDF parsing, deduplication")
    skills.add("[magenta]citation.py[/magenta] - APA formatting")

    # Prompts branch
    prompts = tree.add("📝 [bold yellow]Prompt Templates[/bold yellow]")
    prompts.add("[cyan]query_validation.md[/cyan]")
    prompts.add("[cyan]summarization.md[/cyan]")
    prompts.add("[cyan]literature_section.md[/cyan]")

    console.print(Panel(tree, title="Architecture Overview", border_style="cyan"))


def show_workflow():
    """Display the LangGraph workflow."""
    workflow = """
[bold cyan]LangGraph Workflow[/bold cyan]

    ┌─────────────────┐
    │   [bold green]START[/bold green]        │
    │  (User Query)   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │  [yellow]SearchAgent[/yellow]   │  ← search_literature()
    │                 │    • PubMed API (Bio.Entrez)
    │  • Query PubMed │    • Google Scholar (scholarly)
    │  • Query Scholar│    • Deduplicate results
    │  • Deduplicate  │
    └────────┬────────┘
             │
             ▼
      [dim]Has results?[/dim]
         │       │
         │ Yes   │ No
         │       └──────────────┐
         ▼                      │
    ┌─────────────────┐         │
    │ [yellow]RetrievalAgent[/yellow] │         │
    │                 │         │
    │ • Try PMC full  │         │
    │   text          │         │
    │ • Fallback to   │         │
    │   abstract      │         │
    └────────┬────────┘         │
             │                  │
             ▼                  │
      [dim]Has documents?[/dim]      │
         │       │              │
         │ Yes   │ No           │
         │       └──────────────┤
         ▼                      │
    ┌─────────────────┐         │
    │  [yellow]SummaryAgent[/yellow]  │         │
    │                 │         │
    │ • Format docs   │         │
    │ • Call LLM      │         │
    │ • Generate refs │         │
    └────────┬────────┘         │
             │                  │
             ▼                  ▼
    ┌─────────────────────────────┐
    │         [bold green]END[/bold green]              │
    │  (Summary + References)     │
    └─────────────────────────────┘
    """
    console.print(Panel(workflow, title="Workflow Diagram", border_style="green"))


def show_state_transitions():
    """Display state transitions with Pydantic models."""
    table = Table(title="State Transitions (Pydantic AgentState)", box=box.ROUNDED)

    table.add_column("Stage", style="cyan", no_wrap=True)
    table.add_column("Input State", style="yellow")
    table.add_column("Agent Action", style="green")
    table.add_column("Output State", style="magenta")

    table.add_row(
        "1️⃣  Search",
        "• query\n• max_results\n• model",
        "search_literature()\n→ PubMed + Scholar\n→ Deduplicate",
        "• search_results: [Paper]\n• search_metadata",
    )

    table.add_row(
        "2️⃣  Retrieve",
        "• search_results",
        "retrieve_documents()\n→ Fetch full text\n→ Fallback abstract",
        "• documents: [Document]\n• retrieval_stats",
    )

    table.add_row(
        "3️⃣  Summarize",
        "• documents\n• query\n• model",
        "generate_summary()\n→ Format context\n→ Call LLM\n→ Create citations",
        "• summary: str\n• references: [Citation]\n• literature_section",
    )

    console.print(table)


def show_data_flow():
    """Display data flow through Pydantic models."""
    flow = """
[bold cyan]Data Flow (Immutable Pydantic Models)[/bold cyan]

[yellow]1. Initial State[/yellow]
   AgentState(query="...", max_results=20, model="mistral-small")
        │
        ▼
[yellow]2. After Search[/yellow]
   state.model_copy(update={
       "search_results": [Paper(...), Paper(...), ...],
       "search_metadata": SearchMetadata(...),
       "errors": state.errors + new_errors
   })
        │
        ▼
[yellow]3. After Retrieval[/yellow]
   state.model_copy(update={
       "documents": [Document(...), Document(...), ...],
       "retrieval_stats": RetrievalStats(...),
       "errors": state.errors + new_errors
   })
        │
        ▼
[yellow]4. After Summary[/yellow]
   state.model_copy(update={
       "summary": "...",
       "references": [Citation(...), ...],
       "literature_section": "## References\\n...",
       "generation_metadata": GenerationMetadata(...),
       "errors": state.errors + new_errors
   })
        │
        ▼
[green]Final AgentState[/green] → Return to user
    """
    console.print(Panel(flow, title="Pydantic State Flow", border_style="blue"))


def show_agent_details():
    """Show detailed agent information."""
    table = Table(title="Agent Details", box=box.DOUBLE_EDGE)

    table.add_column("Agent", style="bold cyan")
    table.add_column("Function", style="yellow")
    table.add_column("Input", style="green")
    table.add_column("Output", style="magenta")
    table.add_column("Error Handling", style="red")

    table.add_row(
        "SearchAgent",
        "search_literature()",
        "AgentState",
        "AgentState.model_copy()",
        "Catches exceptions\nContinues if one source fails",
    )

    table.add_row(
        "RetrievalAgent",
        "retrieve_documents()",
        "AgentState",
        "AgentState.model_copy()",
        "PMC → Abstract fallback\nSkips failed retrievals",
    )

    table.add_row(
        "SummaryAgent",
        "generate_summary()",
        "AgentState",
        "AgentState.model_copy()",
        "LLM errors logged\nFallback formatting",
    )

    console.print(table)


def show_dependencies():
    """Show key dependencies."""
    deps = Table(title="Key Dependencies", box=box.SIMPLE)

    deps.add_column("Library", style="cyan")
    deps.add_column("Purpose", style="yellow")
    deps.add_column("Usage", style="green")

    deps.add_row("langgraph", "Workflow orchestration", "StateGraph, conditional edges")
    deps.add_row("pydantic", "Type-safe state", "AgentState, Paper, Document models")
    deps.add_row("litellm", "LLM abstraction", "Multi-provider API calls")
    deps.add_row("biopython", "PubMed access", "Bio.Entrez for NCBI API")
    deps.add_row("scholarly", "Google Scholar", "Search academic papers")
    deps.add_row("pypdf", "PDF parsing", "Extract full text")
    deps.add_row("rich", "CLI formatting", "Beautiful terminal output")

    console.print(deps)


def show_design_principles():
    """Show design principles."""
    principles = """
[bold cyan]Design Principles[/bold cyan]

✅ [green]Parsimonious Design[/green]
   • Single function per capability
   • No code duplication
   • Consolidated, reusable skills

✅ [green]Pydantic-First[/green]
   • 100% Pydantic models for state
   • Immutable state (model_copy())
   • Type-safe throughout

✅ [green]Externalized Prompts[/green]
   • All LLM prompts in .md files
   • Easy to maintain and version
   • Separated from code logic

✅ [green]LLM Flexibility[/green]
   • LiteLLM for multi-provider support
   • Easy model switching
   • Default: mistral-small

✅ [green]Robust Error Handling[/green]
   • Graceful degradation
   • Continue on partial failures
   • Full error tracking in state
    """
    console.print(Panel(principles, title="Design Philosophy", border_style="yellow"))


def main():
    """Display all visualizations."""
    console.clear()
    console.print("\n")
    console.rule("[bold cyan]Scientific Literature Agent - Visual Overview[/bold cyan]")
    console.print("\n")

    show_architecture()
    console.print("\n")

    show_workflow()
    console.print("\n")

    show_state_transitions()
    console.print("\n")

    show_data_flow()
    console.print("\n")

    show_agent_details()
    console.print("\n")

    show_dependencies()
    console.print("\n")

    show_design_principles()
    console.print("\n")

    console.rule("[bold green]End of Overview[/bold green]")
    console.print("\n")


if __name__ == "__main__":
    main()
