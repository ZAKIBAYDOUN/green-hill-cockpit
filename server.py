from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from importlib.metadata import PackageNotFoundError, version
import os
import uvicorn

# Import agents
from agent import graph as green_hill_graph
from ghc_dt_agent import run_ghc_dt

app = FastAPI(title="Green Hill LangGraph API", version="1.0.0")

MODE = os.getenv("MODE", "local")

try:
    SERVICE_VERSION = version("green-hill-cockpit")
except PackageNotFoundError:
    SERVICE_VERSION = "0.0.0"


class InvokeRequest(BaseModel):
    question: str
    state: Optional[Dict[str, Any]] = None


class InvokeResponse(BaseModel):
    answer: str
    agent: str
    status: str
    meta: Optional[Dict[str, Any]] = None


class CeoDTInvokeRequest(BaseModel):
    input: Dict[str, Any]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "mode": MODE}


@app.get("/ready")
async def ready_check():
    """Readiness probe"""
    return {"status": "ok", "mode": MODE}


@app.get("/version")
async def version_route():
    """Service version info"""
    return {"service": "green-hill-cockpit", "version": SERVICE_VERSION, "mode": MODE}


@app.get("/graphs")
async def graphs_route():
    """List available graphs"""
    return {"graphs": ["ceo-dt"]}


@app.post("/agents/ceo-dt/invoke")
async def invoke_ceo_dt(request: CeoDTInvokeRequest):
    """Invoke the CEO Digital Twin agent"""
    query = request.input.get("query", "")
    try:
        result = run_ghc_dt(query, request.input)
        return {"agent": "ceo-dt", "data": {"answer": result["answer"]}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking ceo-dt agent: {e}")


@app.post("/agents/ghc_dt/invoke", response_model=InvokeResponse)
async def invoke_ghc_dt_legacy(request: InvokeRequest):
    """Invoke the GHC-DT agent (legacy endpoint)"""
    try:
        result = run_ghc_dt(request.question, request.state)
        return InvokeResponse(
            answer=result["answer"],
            agent="ghc_dt",
            status="ok",
            meta=result.get("meta", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking GHC-DT agent: {e}")


@app.post("/agents/green_hill/invoke", response_model=InvokeResponse)
async def invoke_green_hill(request: InvokeRequest):
    """Invoke the original Green Hill agent"""
    try:
        state = {
            "input": request.question,
            "output": "",
            "agent_type": request.state.get("agent_type", "Strategy") if request.state else "Strategy"
        }
        result = green_hill_graph.invoke(state)
        return InvokeResponse(
            answer=result["output"],
            agent="green_hill",
            status="ok",
            meta={"agent_type": result.get("agent_type", "Strategy")}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking Green Hill agent: {e}")


@app.post("/invoke")
async def generic_invoke(request: InvokeRequest):
    """Generic invoke endpoint that routes to specific agents based on state"""
    agent_type = request.state.get("agent") if request.state else "green_hill"
    if agent_type == "ghc_dt":
        return await invoke_ghc_dt_legacy(request)
    else:
        return await invoke_green_hill(request)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
