import streamlit as st
import os
import requests

# 🔑 API CONFIGURATION - Use environment variables or secrets
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("🔑 Configure OPENAI_API_KEY in secrets or environment")
    st.stop()

def call_real_agent(content, target_agent, lang_code):
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a {target_agent} specialist for Green Hill Canarias cannabis operations."},
                {"role": "user", "content": content}
            ],
            max_tokens=1000
        )
        
        return {"response": response.choices[0].message.content}, f"✅ {target_agent}"
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

st.title("🌿 Green Hill Executive Cockpit")

AGENTS = {
    "Strategy": "strategy",
    "Finance": "finance",
    "Operations": "operations",
    "Market": "market",
    "Risk": "risk",
    "Compliance": "compliance",
    "Innovation": "innovation",
    "CEO-DT": "ghc_dt"
}
selected_agent = st.selectbox("Select Agent:", list(AGENTS.keys()))
user_query = st.text_area("Your query:", height=100)

def call_langgraph_backend(question, agent_type="green_hill", state=None):
    """Call LangGraph backend for any agent"""
    api_url = os.getenv("LANGGRAPH_API_URL", "http://localhost:8000")
    
    # Route to specific agent endpoint
    if agent_type == "ghc_dt":
        endpoint = f"{api_url}/agents/ghc_dt/invoke"
    else:
        endpoint = f"{api_url}/agents/green_hill/invoke"
    
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("LANGGRAPH_API_KEY")
    if hasattr(st, "secrets") and "LANGGRAPH_API_KEY" in st.secrets:
        api_key = st.secrets["LANGGRAPH_API_KEY"]
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    payload = {"question": question, "state": state or {}}
    
    try:
        resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return {"response": data.get("answer", "No answer")}, f"✅ {agent_type.upper()}"
        else:
            return None, f"❌ Backend error: {resp.status_code}"
    except Exception as e:
        return None, f"❌ Exception: {str(e)}"

def call_ghc_dt_backend(question, state=None):
    """Legacy function for backward compatibility"""
    return call_langgraph_backend(question, "ghc_dt", state)

if st.button("🚀 Execute"):
    if user_query.strip():
        agent_backend_name = AGENTS[selected_agent]
        
        # Use LangGraph backend for all agents
        if selected_agent == "CEO-DT":
            result, status = call_langgraph_backend(user_query, "ghc_dt")
        else:
            # Pass agent type in state for other agents
            state = {"agent_type": selected_agent}
            result, status = call_langgraph_backend(user_query, "green_hill", state)
        
        if result:
            st.success(status)
            st.write(result["response"])
        else:
            st.error(status)
