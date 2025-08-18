import os
from typing import Dict, Any, List

import httpx

BASE_URL = os.getenv("LANGGRAPH_BASE_URL", "")

async def list_graphs() -> List[str]:
    """Fetch available graphs from LangGraph Cloud."""
    if not BASE_URL:
        return []
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/graphs")
        resp.raise_for_status()
        data = resp.json()
        # assume remote returns {"graphs": [...]} or list
        if isinstance(data, dict) and "graphs" in data:
            return data["graphs"]
        if isinstance(data, list):
            return data
        return []

async def invoke_graph(agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Forward invocation to LangGraph Cloud."""
    if not BASE_URL:
        raise RuntimeError("LANGGRAPH_BASE_URL is not set")
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{BASE_URL}/agents/{agent_id}/invoke", json=payload)
        resp.raise_for_status()
        return resp.json()
