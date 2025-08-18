"""Registry of local LangGraphs."""
from typing import Dict, Any

from agent import graph as green_hill_graph
from agents.ghc_dt import ghc_dt_graph

GRAPHS = {
    "green_hill": green_hill_graph,
    "ghc_dt": ghc_dt_graph,
}

def list_graphs() -> list[str]:
    return list(GRAPHS.keys())

def invoke_graph(agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    graph = GRAPHS.get(agent_id)
    if not graph:
        raise KeyError(agent_id)
    return graph.invoke(payload)
