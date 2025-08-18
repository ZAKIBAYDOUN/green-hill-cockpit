import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def call_agent(agent_id: str, payload: dict) -> dict:
    """Call backend FastAPI server."""
    url = f"{BACKEND_URL}/agents/{agent_id}/invoke"
    try:
        resp = requests.post(url, json=payload, timeout=30)
        if resp.ok:
            return resp.json()
        return {"error": resp.text}
    except Exception as exc:  # pragma: no cover
        return {"error": str(exc)}


st.title("Green Hill Cockpit")
agent_id = st.selectbox("Agent", ["ghc_dt"])
question = st.text_input("Question")

if st.button("Invoke"):
    data = call_agent(agent_id, {"input": {"question": question}})
    st.json(data)
