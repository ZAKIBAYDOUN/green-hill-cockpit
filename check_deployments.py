#!/usr/bin/env python3
import requests
import os

deployments = {
    "Green Hill Cockpit": "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app",
    "Digital Roots": "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app"
}

api_key = os.getenv("LANGSMITH_API_KEY", "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")

print("🔍 Verificando deployments de LangGraph...\n")

for name, url in deployments.items():
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{url}/health", headers=headers, timeout=5)
        status = f"✅ Online (HTTP {response.status_code})" if response.status_code == 200 else f"❌ Error HTTP {response.status_code}"
    except Exception as e:
        status = f"❌ Error: {str(e)[:50]}"
    
    print(f"{name}: {status}")
    print(f"  URL: {url}\n")
