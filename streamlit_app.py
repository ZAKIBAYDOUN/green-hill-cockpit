import streamlit as st
import os
import requests

st.title("🌿 Green Hill Executive Cockpit")

# Backend configuration - always use backend, no direct OpenAI calls
try:
    BACKEND_BASE_URL = st.secrets.get("BACKEND_BASE_URL") or os.getenv("BACKEND_BASE_URL", "http://localhost:8080")
except:
    BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8080")

AGENTS = {
    "Strategy": "strategy",
    "Finance": "finance", 
    "Operations": "operations",
    "Market": "market",
    "Risk": "risk",
    "Compliance": "compliance",
    "Innovation": "innovation",
    "CEO-DT": "ceo-dt"
}

selected_agent = st.selectbox("Select Agent:", list(AGENTS.keys()))
user_query = st.text_area("Your query:", height=100)

def call_backend_agent(question, agent_key):
    """Call LangGraph backend for any agent"""
    
    # Use CEO-DT endpoint format for CEO-DT agent
    if agent_key == "ceo-dt":
        endpoint = f"{BACKEND_BASE_URL}/agents/ceo-dt/invoke"
        payload = {"input": {"query": question}}
    else:
        # For other agents, use generic endpoint (if available)
        endpoint = f"{BACKEND_BASE_URL}/agents/{agent_key}/invoke"  
        payload = {"input": {"query": question}}
    
    headers = {"Content-Type": "application/json"}
    
    # Add authentication if available
    try:
        api_key = st.secrets.get("LANGGRAPH_API_KEY") or os.getenv("LANGGRAPH_API_KEY")
    except:
        api_key = os.getenv("LANGGRAPH_API_KEY")
        
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            # Handle different response formats
            answer = data.get("output", {}).get("content") or data.get("answer") or str(data)
            return {"response": answer}, f"✅ {selected_agent}"
        else:
            return None, f"❌ Backend error: {resp.status_code} - {resp.text[:100]}"
    except Exception as e:
        return None, f"❌ Connection error: {str(e)}"

# Show backend URL for debugging
st.sidebar.info(f"Backend: {BACKEND_BASE_URL}")

if st.button("🚀 Execute"):
    if user_query.strip():
        agent_backend_key = AGENTS[selected_agent]
        result, status = call_backend_agent(user_query, agent_backend_key)
        
        if result:
            st.success(status)
            st.write(result["response"])
        else:
            st.error(status)
    else:
        st.warning("Please enter a query first.")
