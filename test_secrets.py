import streamlit as st
import os
import requests

st.title("🔧 Secrets Test")

# Try to load from st.secrets first, then environment
def get_secret(key):
    try:
        if key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key)

# Load secrets
LANGGRAPH_API_URL = get_secret("LANGGRAPH_API_URL")
LANGGRAPH_API_KEY = get_secret("LANGGRAPH_API_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")

# Display status
st.subheader("Secrets Status:")
col1, col2, col3 = st.columns(3)

with col1:
    if LANGGRAPH_API_URL:
        st.success(f"✅ URL: ...{LANGGRAPH_API_URL[-20:]}")
    else:
        st.error("❌ URL: Not found")

with col2:
    if LANGGRAPH_API_KEY:
        st.success(f"✅ API Key: {LANGGRAPH_API_KEY[:10]}...")
    else:
        st.error("❌ API Key: Not found")

with col3:
    if OPENAI_API_KEY:
        st.success(f"✅ OpenAI: {OPENAI_API_KEY[:10]}...")
    else:
        st.error("❌ OpenAI: Not found")

# Test API call
if st.button("Test LangGraph API"):
    if LANGGRAPH_API_URL and LANGGRAPH_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {LANGGRAPH_API_KEY}"}
            response = requests.get(f"{LANGGRAPH_API_URL}/health", headers=headers, timeout=5)
            st.write(f"Response: {response.status_code}")
            st.json(response.json() if response.status_code == 200 else {"error": response.text})
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Missing URL or API Key")

# Show how to add secrets
with st.expander("How to add secrets in Streamlit Cloud"):
    st.code("""
LANGGRAPH_API_URL = "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app"
LANGGRAPH_API_KEY = "REVOKED_GENERATE_NEW_KEY"
OPENAI_API_KEY = "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"
    """)
