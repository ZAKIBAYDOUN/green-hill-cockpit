#!/usr/bin/env python3
"""
Cannabis Apps Real-time Monitor
Monitorea el estado de las 3 apps en tiempo real
"""

import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="Cannabis Apps Monitor",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Cannabis Apps Real-time Monitor")
st.caption("Monitoring Green Hill ecosystem health")

# Auto-refresh every 30 seconds
st_autorefresh = st.empty()

APPS = {
    "green-hill-cockpit": {
        "name": "Green Hill Cockpit",
        "streamlit": "https://green-hill-cockpit.streamlit.app",
        "langgraph": "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app",
        "icon": "🌿"
    },
    "digital-roots": {
        "name": "Digital Roots", 
        "streamlit": "https://digital-roots-my7i9xaz3xdnj2jhcjqbj6.streamlit.app",
        "langgraph": "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app",
        "icon": "🌱"
    },
    "ground-control": {
        "name": "Ground Control",
        "streamlit": "https://ground-control.streamlit.app",
        "langgraph": None,
        "icon": "🎮"
    }
}

def check_url(url, timeout=5):
    """Check if URL is accessible"""
    if not url:
        return "N/A", 0
    try:
        start = time.time()
        response = requests.get(url, timeout=timeout)
        elapsed = (time.time() - start) * 1000
        return response.status_code, elapsed
    except:
        return "Timeout", timeout * 1000

# Display status
cols = st.columns(3)

for i, (app_id, config) in enumerate(APPS.items()):
    with cols[i]:
        st.subheader(f"{config['icon']} {config['name']}")
        
        # Check Streamlit
        status, latency = check_url(config['streamlit'])
        if status == 200:
            st.success(f"✅ Streamlit: Online ({latency:.0f}ms)")
        elif status == "Timeout":
            st.error("❌ Streamlit: Timeout")
        else:
            st.warning(f"⚠️ Streamlit: HTTP {status}")
        
        # Check LangGraph
        if config['langgraph']:
            status, latency = check_url(config['langgraph'] + "/health")
            if status == 200:
                st.success(f"✅ LangGraph: Online ({latency:.0f}ms)")
            else:
                st.warning(f"⚠️ LangGraph: HTTP {status}")
        else:
            st.info("ℹ️ LangGraph: Autonomous mode")
        
        st.caption(f"Last check: {datetime.now().strftime('%H:%M:%S')}")

# Instructions
st.divider()
st.subheader("📋 Quick Actions")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **If APIs show 403 Forbidden:**
    1. Check LangSmith dashboard
    2. Verify API key permissions
    3. Regenerate key if needed
    """)

with col2:
    st.markdown("""
    **If Streamlit shows 404:**
    1. Wait 2-3 minutes for deployment
    2. Check GitHub repository exists
    3. Verify Streamlit Cloud connection
    """)

# Auto-refresh
if st.button("🔄 Refresh Now"):
    st.rerun()

st.caption("Auto-refreshes every 30 seconds")
time.sleep(30)
st.rerun()
