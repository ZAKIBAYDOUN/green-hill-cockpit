import os
import json
from datetime import datetime
from typing import Optional, Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class GHCDTState(TypedDict):
    question: str
    answer: str
    agent_type: str
    meta: dict


def ghc_dt_node(state: GHCDTState) -> GHCDTState:
    """GHC-DT (CEO Digital Twin) LangGraph node."""
    question = state.get("question", "")
    agent_type = state.get("agent_type", "CEO")

    system_prompt = os.getenv(
        "GHC_DT_SYSTEM_PROMPT",
        "You are GHC-DT, the CEO Digital Twin of Green Hill Canarias. Be concise, executive, and action-oriented. If information is unknown, say 'Unknown'. Structure answers as: Summary, Key Points, Next Actions. Avoid internal file names in public outputs. Log evidence if enabled.",
    )
    model = os.getenv("GHC_DT_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("GHC_DT_TEMPERATURE", "0.2"))

    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question),
    ]

    response = llm.invoke(messages)
    answer = response.content

    result = {
        "question": question,
        "answer": answer,
        "agent_type": "ghc_dt",
        "meta": {"agent": "ghc_dt", "tokens": None},
    }

    evidence_log = os.getenv("GHC_DT_EVIDENCE_LOG")
    if evidence_log:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "answer": answer,
            "state": state,
            "meta": result["meta"],
        }
        try:
            with open(evidence_log, "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass  # Do not fail on logging errors

    return result


# Build GHC-DT LangGraph
workflow = StateGraph(GHCDTState)
workflow.add_node("ghc_dt", ghc_dt_node)
workflow.set_entry_point("ghc_dt")
workflow.add_edge("ghc_dt", END)

ghc_dt_graph = workflow.compile()


def run_ghc_dt(question: str, state: Optional[dict] = None) -> dict:
    """Run the GHC-DT agent using LangGraph.

    If ``OPENAI_API_KEY`` is not configured the function falls back to an
    echo response so smoke tests can run without external dependencies.
    """
    if not os.getenv("OPENAI_API_KEY"):
        return {"answer": f"Echo: {question}", "meta": {}}

    input_state = {
        "question": question,
        "answer": "",
        "agent_type": "ghc_dt",
        "meta": {},
    }

    try:
        result = ghc_dt_graph.invoke(input_state)
        return {"answer": result["answer"], "meta": result["meta"]}
    except Exception:
        return {"answer": f"Echo: {question}", "meta": {}}
