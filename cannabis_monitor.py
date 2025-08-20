#!/usr/bin/env python3
"""
🌿 Cannabis Apps Monitoring Dashboard
====================================

Real-time monitoring for all 3 cannabis applications
Author: Zaki Baydoun (zakibaydoun@msn.com)
"""

import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="🌿 Cannabis Apps Monitor",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Cannabis Applications Monitoring Dashboard")
st.caption("Real-time status for all cannabis applications")

# App configurations
APPS = {
    "greenhillgpt": {
        "repo": "greenhillgpt",
        "display_name": "Green Hill GPT",
        "description": "AI-powered cannabis strain recommendation system",
        "streamlit_url": "https://greenhillgpt.streamlit.app",
        "langgraph_url": "https://green-hill-gpt-ai-a1b2c3d4e5f6.us.langgraph.app"
    },
    "digital-roots": {
        "repo": "digital-roots",
        "display_name": "Digital Roots",
        "description": "Cannabis cultivation management platform",
        "streamlit_url": "https://digital-roots.streamlit.app",
        "langgraph_url": "https://digital-roots-cultivation-g7h8i9j0k1l2.us.langgraph.app"
    },
    "ground-control": {
        "repo": "ground-control",
        "display_name": "Ground Control",
        "description": "Cannabis operations command center",
        "streamlit_url": "https://ground-control.streamlit.app",
        "langgraph_url": "https://ground-control-a0ae430fa0b85ca09ebb486704b69f2b.us.langgraph.app"
    }
}

def check_app_status(url):
    """Check if an app is responding"""
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

# Create columns for each app
cols = st.columns(3)

for i, (app_key, app_config) in enumerate(APPS.items()):
    with cols[i]:
        st.subheader(f"🌿 {app_config['display_name']}")
        
        # Check Streamlit app
        streamlit_status = check_app_status(app_config['streamlit_url'])
        if streamlit_status:
            st.success("✅ Streamlit: Online")
        else:
            st.error("❌ Streamlit: Offline")
            
        # Check LangGraph API
        langgraph_status = check_app_status(app_config['langgraph_url'])
        if langgraph_status:
            st.success("✅ LangGraph: Online")
        else:
            st.error("❌ LangGraph: Offline")
            
        # App links
        st.markdown(f"[🔗 Open App]({app_config['streamlit_url']})")
        st.markdown(f"[🔧 API Docs]({app_config['langgraph_url']})")

# Auto-refresh every 30 seconds
time.sleep(30)
st.rerun()
