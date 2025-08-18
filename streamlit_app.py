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

def call_agent(agent_id: str, payload: dict):
    """Invoke a backend agent."""
    api_url = os.getenv("LANGGRAPH_API_URL", "http://localhost:8000")
    try:
        resp = requests.post(f"{api_url}/agents/{agent_id}/invoke", json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data"), f"✅ {agent_id}"
    except Exception as e:
        return None, f"❌ {str(e)}"

if st.button("🚀 Execute"):
    if user_query.strip():
        if selected_agent == "CEO-DT":
            payload = {"question": user_query}
            agent_id = "ghc_dt"
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
