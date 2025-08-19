import streamlit as st
import os
import requests
import time

st.title("🌿 Green Hill Executive Cockpit")

# Backend configuration - LangGraph Cloud API format
try:
    BACKEND_BASE_URL = st.secrets.get("BACKEND_BASE_URL") or "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app"
except:
    BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app")

# Remove trailing slash if present
BACKEND_BASE_URL = BACKEND_BASE_URL.rstrip('/')

AGENTS = {
    "CEO-DT": "agent",
    "Green Hill Agent": "agent"
}

selected_agent = st.selectbox("Select Agent:", list(AGENTS.keys()))
user_query = st.text_area("Your query:", height=100)

def call_langgraph_cloud_agent(question, agent_key):
    """Call LangGraph Cloud using the standard API format"""
    
    headers = {"Content-Type": "application/json"}
    
    # Add authentication if available
    try:
        api_key = st.secrets.get("LANGGRAPH_API_KEY")
    except:
        api_key = os.getenv("LANGGRAPH_API_KEY")
        
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        # Step 1: Create a thread
        thread_response = requests.post(
            f"{BACKEND_BASE_URL}/assistants/{agent_key}/threads",
            headers=headers,
            json={"config": {"configurable": {}}},
            timeout=30
        )
        
        if thread_response.status_code != 200:
            return None, f"❌ Thread creation failed: {thread_response.status_code} - {thread_response.text[:100]}"
        
        thread_data = thread_response.json()
        thread_id = thread_data.get("thread_id")
        
        if not thread_id:
            return None, f"❌ No thread_id in response: {thread_data}"
        
        # Step 2: Create a run
        run_response = requests.post(
            f"{BACKEND_BASE_URL}/threads/{thread_id}/runs",
            headers=headers,
            json={
                "assistant_id": agent_key,
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                }
            },
            timeout=30
        )
        
        if run_response.status_code != 200:
            return None, f"❌ Run creation failed: {run_response.status_code} - {run_response.text[:100]}"
        
        run_data = run_response.json()
        run_id = run_data.get("run_id")
        
        if not run_id:
            return None, f"❌ No run_id in response: {run_data}"
        
        # Step 3: Wait for completion and get result
        max_attempts = 30
        for attempt in range(max_attempts):
            status_response = requests.get(
                f"{BACKEND_BASE_URL}/threads/{thread_id}/runs/{run_id}",
                headers=headers,
                timeout=10
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data.get("status")
                
                if status == "success":
                    # Get the messages from the thread
                    messages_response = requests.get(
                        f"{BACKEND_BASE_URL}/threads/{thread_id}/messages",
                        headers=headers,
                        timeout=10
                    )
                    
                    if messages_response.status_code == 200:
                        messages_data = messages_response.json()
                        messages = messages_data.get("messages", [])
                        
                        # Find the assistant's response
                        for msg in reversed(messages):
                            if msg.get("type") == "ai" or msg.get("role") == "assistant":
                                content = msg.get("content", "")
                                if isinstance(content, list) and content:
                                    content = content[0].get("text", str(content))
                                elif isinstance(content, dict):
                                    content = content.get("text", str(content))
                                return {"response": content}, f"✅ {selected_agent}"
                        
                        return {"response": "No assistant response found"}, f"✅ {selected_agent}"
                    else:
                        return None, f"❌ Messages fetch failed: {messages_response.status_code}"
                
                elif status == "failed":
                    return None, f"❌ Run failed: {status_data.get('error', 'Unknown error')}"
                
                elif status in ["pending", "running"]:
                    time.sleep(1)
                    continue
                else:
                    return None, f"❌ Unknown status: {status}"
            else:
                return None, f"❌ Status check failed: {status_response.status_code}"
        
        return None, f"❌ Timeout waiting for response (30 seconds)"
        
    except Exception as e:
        return None, f"❌ Connection error: {str(e)}"

# Health check function
def check_backend_health():
    """Check if backend is accessible"""
    try:
        response = requests.get(f"{BACKEND_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, "✅ Backend is healthy"
        else:
            return False, f"❌ Backend returned {response.status_code}"
    except Exception as e:
        return False, f"❌ Cannot reach backend: {str(e)}"

# Sidebar with backend info and health check
st.sidebar.info(f"Backend: {BACKEND_BASE_URL}")

if st.sidebar.button("🔍 Check Backend Health"):
    is_healthy, status = check_backend_health()
    if is_healthy:
        st.sidebar.success(status)
    else:
        st.sidebar.error(status)

# Main execution
if st.button("🚀 Execute"):
    if user_query.strip():
        agent_backend_key = AGENTS[selected_agent]
        
        with st.spinner(f"Consulting {selected_agent}..."):
            result, status = call_langgraph_cloud_agent(user_query, agent_backend_key)
        
        if result:
            st.success(status)
            st.write(result["response"])
        else:
            st.error(status)
    else:
        st.warning("Please enter a query first.")
