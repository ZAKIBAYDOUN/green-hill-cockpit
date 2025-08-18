import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

from ghc_dt.registry import REGISTRY
from ghc_dt.adapters.langgraph_client import LangGraphClient

APP_VERSION = "0.1.0"

app = FastAPI(title="Green Hill Cockpit API", version=APP_VERSION)

origins = [o for o in os.getenv("CORS_ORIGINS", "").split(",") if o]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_url = os.getenv("LANGGRAPH_BASE_URL")
client = LangGraphClient(base_url) if base_url else None


class InvokeRequest(BaseModel):
    input: Dict[str, Any] = {}


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
async def version() -> Dict[str, Any]:
    mode = "proxy" if client else "local"
    return {"version": APP_VERSION, "mode": mode}


@app.get("/graphs")
async def graphs() -> Dict[str, Any]:
    if client:
        try:
            return await client.list_graphs()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
    return {"graphs": list(REGISTRY.keys())}


@app.post("/agents/{agent_id}/invoke")
async def invoke_agent(agent_id: str, request: InvokeRequest) -> Dict[str, Any]:
    payload = request.input
    if client:
        try:
            return await client.invoke(agent_id, payload)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(status_code=404, detail="unknown agent")
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
    if agent_id not in REGISTRY:
        raise HTTPException(status_code=404, detail="unknown agent")
    try:
        result = REGISTRY[agent_id].invoke(payload)
        return {"agent": agent_id, "data": result}
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc))


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=port)
