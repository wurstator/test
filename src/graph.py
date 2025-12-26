"""LangGraph workflow definition for scientific literature agent."""

from langgraph.graph import StateGraph, END
from .models.state import AgentState
from .agents.search_agent import search_literature
from .agents.retrieval_agent import retrieve_documents
from .agents.summary_agent import generate_summary


def should_continue_after_search(state: AgentState) -> str:
    """
    Decide whether to continue after search based on results.

    Args:
        state: Current graph state

    Returns:
        Next node name: "retrieve" or "end"
    """
    if not state.search_results:
        return "end"
    return "retrieve"


def should_continue_after_retrieval(state: AgentState) -> str:
    """
    Decide whether to continue after retrieval based on results.

    Args:
        state: Current graph state

    Returns:
        Next node name: "summarize" or "end"
    """
    if not state.documents:
        return "end"
    return "summarize"


def create_literature_graph():
    """
    Create and compile the LangGraph workflow.

    Returns:
        Compiled graph ready for execution

    Workflow:
        START -> search -> retrieve -> summarize -> END
    """
    # Create graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("search", search_literature)
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("summarize", generate_summary)

    # Add edges
    workflow.set_entry_point("search")

    # Conditional edge after search
    workflow.add_conditional_edges(
        "search",
        should_continue_after_search,
        {"retrieve": "retrieve", "end": END},
    )

    # Conditional edge after retrieval
    workflow.add_conditional_edges(
        "retrieve",
        should_continue_after_retrieval,
        {"summarize": "summarize", "end": END},
    )

    # Edge from summarize to end
    workflow.add_edge("summarize", END)

    # Compile graph
    return workflow.compile()


def run_literature_search(
    query: str, max_results: int = 20, model: str = "mistral/mistral-small-latest"
) -> AgentState:
    """
    Execute the complete literature search workflow.

    Args:
        query: Search query for scientific literature
        max_results: Maximum results per source (default: 20)
        model: LLM model to use (default: mistral-small)

    Returns:
        Final AgentState with search results, documents, and summary

    Example:
        >>> result = run_literature_search("CRISPR gene editing")
        >>> print(result.summary)
        >>> print(result.literature_section)
    """
    # Create initial state
    initial_state = AgentState(query=query, max_results=max_results, model=model)

    # Create and run graph
    graph = create_literature_graph()
    result = graph.invoke(initial_state)

    # Convert result back to AgentState if needed
    if isinstance(result, AgentState):
        return result
    else:
        return AgentState(**result)  # type: ignore
