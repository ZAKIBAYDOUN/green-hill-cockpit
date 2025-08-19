from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import uvicorn

# Import only the simple agent for now
from simple_agent import graph as simple_graph

app = FastAPI(title="Green Hill LangGraph API", version="1.0.0")

MODE = os.getenv("MODE", "local")

class InvokeRequest(BaseModel):
    input: Dict[str, Any]

@app.get("/health")
async def health_check():
    return {"status": "ok", "mode": MODE}

@app.get("/ready")
async def ready_check():
    return {"status": "ok", "mode": MODE}

@app.get("/version")
async def version_route():
    return {"service": "green-hill-cockpit", "version": "1.0.0", "mode": MODE}

@app.get("/graphs")
async def graphs_route():
    return {"graphs": ["agent"]}

@app.post("/assistants/agent/threads")
async def create_thread(request: InvokeRequest = None):
    return {"thread_id": "thread_123"}

@app.post("/threads/{thread_id}/runs")
async def create_run(thread_id: str, request: InvokeRequest):
    try:
        input_text = ""
        if "input" in request.input and "messages" in request.input["input"]:
            input_text = request.input["input"]["messages"][0]["content"]
        elif "messages" in request.input:
            input_text = request.input["messages"][0]["content"]
        
        state = {"input": input_text, "output": ""}
        result = simple_graph.invoke(state)
        
        return {
            "run_id": "run_123",
            "status": "success",
            "output": result["output"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
