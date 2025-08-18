import os
import requests
import streamlit as st

st.title("🌿 Green Hill Executive Cockpit")

AGENTS = {
    "Strategy": "strategy",
    "Finance": "finance",
    "Operations": "operations",
    "Market": "market",
    "Risk": "risk",
    "Compliance": "compliance",
    "Innovation": "innovation",
    "CEO-DT": "ceo-dt",
}

selected_agent = st.selectbox("Select Agent:", list(AGENTS.keys()))
user_query = st.text_area("Your query:", height=100)

def call_agent(agent_id: str, payload: dict):
    """Invoke a backend agent."""
    api_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8080")
    try:
        resp = requests.post(f"{api_url}/agents/{agent_id}/invoke", json=payload, timeout=30)
        data = resp.json()
        if resp.status_code != 200 or data.get("status") != "ok":
            return None, data.get("detail", "error")
        return data.get("data"), f"✅ {agent_id}"
    except Exception as e:
        return None, f"❌ {str(e)}"

if st.button("🚀 Execute"):
    if user_query.strip():
        if selected_agent == "CEO-DT":
            payload = {"input": {"query": user_query}}
            agent_id = "ceo-dt"
        else:
            payload = {"input": user_query, "agent_type": selected_agent}
            agent_id = "green_hill"

        result, status = call_agent(agent_id, payload)

        if result:
            st.success(status)
            response_text = result.get("answer") or result.get("output") or result
            st.write(response_text)
        else:
            st.error(status)
