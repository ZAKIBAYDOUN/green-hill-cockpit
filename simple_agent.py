from typing import TypedDict
from langgraph.graph import StateGraph, END

class SimpleState(TypedDict):
    input: str
    output: str

def simple_node(state: SimpleState):
    return {
        "input": state.get("input", ""),
        "output": f"Green Hill Agent Response: {state.get('input', '')}"
    }

workflow = StateGraph(SimpleState)
workflow.add_node("agent", simple_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

graph = workflow.compile()