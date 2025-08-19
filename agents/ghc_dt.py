"""
CEO Digital Twin (ghc_dt) Agent
Provides strategic guidance and decision support for Green Hill Canarias
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from openai import OpenAI

def run_ghc_dt(question: str, state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    CEO Digital Twin agent implementation
    """
    # Get configuration from environment
    model = os.getenv("GHC_DT_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("GHC_DT_TEMPERATURE", "0.2"))
    evidence_log = os.getenv("GHC_DT_EVIDENCE_LOG")
    
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "answer": "OPENAI_API_KEY not configured. Cannot provide CEO insights.",
            "agent": "ghc_dt",
            "error": "missing_api_key"
        }
    
    client = OpenAI(api_key=api_key)
    
    # Build context from state
    state = state or {}
    context = f"""You are GHC-DT, the CEO Digital Twin of Green Hill Canarias.
Current State:
- Phase: {state.get('phase', 'Phase 1: Pre-Operational Setup')}
- ZEC Tax Rate: {state.get('zec_rate', 4)}%
- Cash Buffer Target Date: {state.get('cash_buffer_to', '2026-06-30')}

Provide strategic, actionable guidance as the CEO would."""
    
    try:
        # Make OpenAI API call
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": question}
            ]
        )
        
        answer = response.choices[0].message.content
        
        # Prepare result
        result = {
            "answer": answer,
            "agent": "ghc_dt",
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Log to evidence file if configured
        if evidence_log:
            try:
                evidence_entry = {
                    "timestamp": result["timestamp"],
                    "agent": "ghc_dt",
                    "question": question,
                    "answer": answer,
                    "state": state
                }
                with open(evidence_log, "a") as f:
                    f.write(json.dumps(evidence_entry) + "\n")
            except Exception as e:
                result["evidence_log_error"] = str(e)
        
        return result
        
    except Exception as e:
        return {
            "answer": f"Error consulting CEO Digital Twin: {str(e)}",
            "agent": "ghc_dt",
            "error": str(e)
        }
