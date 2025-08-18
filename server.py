from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uvicorn

# Import the agents
from agent import graph as green_hill_graph
from agents.ghc_dt import ghc_dt_graph, run_ghc_dt

app = FastAPI(title="Green Hill LangGraph API", version="1.0.0")

class InvokeRequest(BaseModel):
    question: str
    state: Optional[Dict[str, Any]] = None

class InvokeResponse(BaseModel):
    answer: str
    agent: str
    status: str
    meta: Optional[Dict[str, Any]] = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "green-hill-langgraph"}

@app.post("/agents/ghc_dt/invoke", response_model=InvokeResponse)
async def invoke_ghc_dt(request: InvokeRequest):
    """Invoke the GHC-DT (CEO Digital Twin) agent"""
    try:
        result = run_ghc_dt(request.question, request.state)
        return InvokeResponse(
            answer=result["answer"],
            agent="ghc_dt",
            status="ok",
            meta=result.get("meta", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking GHC-DT agent: {str(e)}")

@app.post("/agents/green_hill/invoke", response_model=InvokeResponse)
async def invoke_green_hill(request: InvokeRequest):
    """Invoke the original Green Hill agent"""
    try:
        # Map question to the expected state format
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
        raise HTTPException(status_code=500, detail=f"Error invoking Green Hill agent: {str(e)}")

@app.post("/invoke")
async def generic_invoke(request: InvokeRequest):
    """Generic invoke endpoint that routes to specific agents based on state"""
    agent_type = request.state.get("agent") if request.state else "green_hill"
    
    if agent_type == "ghc_dt":
        return await invoke_ghc_dt(request)
    else:
        return await invoke_green_hill(request)

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)