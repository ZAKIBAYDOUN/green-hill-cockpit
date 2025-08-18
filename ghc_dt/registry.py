"""Registry of local LangGraphs."""
from typing import Dict, Any

from ghc_dt.agent import graph as green_hill_graph
from ghc_dt.ghc_dt_agent import ghc_dt_graph

GRAPHS = {
    "green_hill": green_hill_graph,
    "ghc_dt": ghc_dt_graph,
    "ceo-dt": ghc_dt_graph,
}

def list_graphs() -> list[str]:
    return list(GRAPHS.keys())

def invoke_graph(agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    graph = GRAPHS.get(agent_id)
    if not graph:
        raise KeyError(agent_id)
    if agent_id in {"ghc_dt", "ceo-dt"} and isinstance(payload, dict):
        inner = payload.get("input")
        if isinstance(inner, dict) and "query" in inner:
            payload = {"question": inner["query"]}
    return graph.invoke(payload)
