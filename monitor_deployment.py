#!/usr/bin/env python3
"""
Monitor específico para el deployment de Green Hill Cockpit
"""

import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Green Hill Deployment Monitor", page_icon="🌿")

st.title("🌿 Green Hill Cockpit - Deployment Monitor")
st.caption(f"Monitoring deployment: 243a8593-9c11-47ea-b164-4959510bb2de")

# Configuración
deployment_url = "https://243a8593-9c11-47ea-b164-4959510bb2de.us.langgraph.app"
api_key = st.text_input("API Key", type="password", value="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")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Test Health"):
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            response = requests.get(f"{deployment_url}/health", headers=headers, timeout=5)
            if response.status_code == 200:
                st.success(f"✅ Health Check: OK")
            else:
                st.error(f"❌ Health Check: HTTP {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error: {e}")

with col2:
    if st.button("🤖 Test Invoke"):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "question": "Hello, test",
            "agent": "ghc_dt",
            "state": {}
        }
        try:
            response = requests.post(f"{deployment_url}/invoke", headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                st.success("✅ Invoke: OK")
                st.json(response.json())
            else:
                st.error(f"❌ Invoke: HTTP {response.status_code}")
                st.text(response.text[:500])
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.divider()
st.subheader("📋 Quick Links")
st.markdown(f"""
- [🔗 LangSmith Dashboard](https://smith.langchain.com/o/d6219b54-6d6e-42ee-8a50-c327796371fe/host/deployments/243a8593-9c11-47ea-b164-4959510bb2de)
- [📱 Green Hill Cockpit App](https://green-hill-cockpit.streamlit.app)
- [📊 Streamlit Cloud Dashboard](https://share.streamlit.io/)
""")

st.info("""
**Deployment Info:**
- Organization: d6219b54-6d6e-42ee-8a50-c327796371fe
- Deployment: 243a8593-9c11-47ea-b164-4959510bb2de
- Region: US
""")
