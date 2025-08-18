"""FastAPI backend for Green Hill Cockpit."""
import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="Green Hill Cockpit API", version="0.1.0")

# CORS configuration
origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PROXY_BASE_URL = os.getenv("LANGGRAPH_BASE_URL")
if PROXY_BASE_URL:
    from ghc_dt.adapters import langgraph_client as lg_client
else:
    from ghc_dt import registry


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
async def version() -> Dict[str, str]:
    return {"version": app.version}


@app.get("/graphs")
async def graphs() -> Dict[str, list]:
    if PROXY_BASE_URL:
        graph_list = await lg_client.list_graphs()
    else:
        graph_list = registry.list_graphs()
    return {"graphs": graph_list}


@app.post("/agents/{agent_id}/invoke")
async def invoke_agent(agent_id: str, payload: Dict[str, Any] = Body(...)) -> JSONResponse:
    try:
        if PROXY_BASE_URL:
            result = await lg_client.invoke_graph(agent_id, payload)
        else:
            result = registry.invoke_graph(agent_id, payload)
        return JSONResponse({"status": "ok", "agent": agent_id, "data": result})
    except KeyError:
        return JSONResponse(status_code=404, content={"status": "error", "agent": agent_id, "detail": "unknown agent"})
    except Exception as exc:
        return JSONResponse(status_code=500, content={"status": "error", "agent": agent_id, "detail": str(exc)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
