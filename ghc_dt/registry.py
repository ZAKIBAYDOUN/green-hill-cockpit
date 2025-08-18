from typing import TypedDict
from langgraph.graph import StateGraph, END


class EchoState(TypedDict):
    question: str
    answer: str


def echo_node(state: EchoState) -> EchoState:
    """Simple local graph node that echoes the question."""
    question = state.get("question", "")
    state["answer"] = f"Echo: {question}"
    return state


workflow = StateGraph(EchoState)
workflow.add_node("echo", echo_node)
workflow.set_entry_point("echo")
workflow.add_edge("echo", END)

ghc_dt_graph = workflow.compile()

# Registry of locally available graphs
REGISTRY = {
    "ghc_dt": ghc_dt_graph,
}
