import os
from typing import Any, Dict, Optional
import httpx


class LangGraphClient:
    """Client for forwarding requests to LangGraph Cloud."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.base_url = base_url or os.getenv("LANGGRAPH_BASE_URL", "")
        self.api_key = api_key or os.getenv("LANGGRAPH_API_KEY")

    async def _request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        async with httpx.AsyncClient() as client:
            resp = await client.request(method, f"{self.base_url}{path}", json=json, headers=headers)
        resp.raise_for_status()
        return resp.json()

    async def list_graphs(self) -> Dict[str, Any]:
        """Return available graphs from LangGraph Cloud."""
        return await self._request("GET", "/graphs")

    async def invoke(self, agent_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a remote agent graph."""
        return await self._request("POST", f"/agents/{agent_id}/invoke", json=payload)
