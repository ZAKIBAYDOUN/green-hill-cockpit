import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
# Short timeouts avoid hanging when OpenAI is unreachable
client = OpenAI(api_key=api_key, timeout=20, max_retries=0) if api_key else None

def choose_model() -> str:
    explicit = os.getenv("MODEL_NAME")
    if explicit:
        return explicit
    return "gpt-5"

def run_ceo_dt(question: str) -> Dict[str, Any]:
    if not client:
        return {"text": f"Echo: {question}", "model": "echo"}

    messages = [{"role": "user", "content": question}]
    model = choose_model()
    try:
        resp = client.chat.completions.create(model=model, messages=messages)
        return {"text": resp.choices[0].message.content, "model": model}
    except Exception as e:
        if not os.getenv("MODEL_NAME") and model == "gpt-5":
            try:
                fallback_model = "gpt-4o"
                resp = client.chat.completions.create(model=fallback_model, messages=messages)
                return {"text": resp.choices[0].message.content, "model": fallback_model}
            except Exception as e2:
                return {"text": f"Echo: {question} (fallback, error: {e2})", "model": "echo"}
        return {"text": f"Echo: {question} (fallback, error: {e})", "model": "echo"}


class GHCDTState(TypedDict):
    question: str
    answer: str
    agent_type: str
    meta: dict

def ghc_dt_node(state: GHCDTState) -> GHCDTState:
    """GHC-DT (CEO Digital Twin) LangGraph node."""
    question = state.get("question", "")
    result = run_ceo_dt(question)
    answer = result["text"]

    node_result = {
        "question": question,
        "answer": answer,
        "agent_type": "ghc_dt",
        "meta": {"agent": "ghc_dt", "model": result.get("model"), "tokens": None},
    }

    evidence_log = os.getenv("GHC_DT_EVIDENCE_LOG")
    if evidence_log:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "answer": answer,
            "state": state,
            "meta": node_result["meta"],
        }
        try:
            with open(evidence_log, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass

    return node_result

workflow = StateGraph(GHCDTState)
workflow.add_node("ghc_dt", ghc_dt_node)
workflow.set_entry_point("ghc_dt")
workflow.add_edge("ghc_dt", END)

ghc_dt_graph = workflow.compile()

def run_ghc_dt(question: str, state: Optional[dict] = None) -> dict:
    """Run the GHC-DT agent using LangGraph."""
    input_state = {
        "question": question,
        "answer": "",
        "agent_type": "ghc_dt",
        "meta": {},
    }
    result = ghc_dt_graph.invoke(input_state)
    return {"answer": result["answer"], "meta": result["meta"]}
