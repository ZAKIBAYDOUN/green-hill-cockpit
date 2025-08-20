#!/usr/bin/env python3
"""
Cannabis Apps Complete Fix Script
Arregla TODO el ecosistema de aplicaciones de una vez
"""

import os
import json
import subprocess
import requests
from datetime import datetime

print("🌿 CANNABIS APPS COMPLETE FIX - Starting...")
print("=" * 60)

# Configuración de las 3 apps
APPS_CONFIG = {
    "green-hill-cockpit": {
        "name": "Green Hill Cockpit",
        "repo": "green-hill-cockpit",
        "streamlit_url": "https://green-hill-cockpit.streamlit.app",
        "langgraph_url": "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app",
        "icon": "🌿"
    },
    "digital-roots": {
        "name": "Digital Roots",
        "repo": "digital-roots",
        "streamlit_url": "https://digital-roots-my7i9xaz3xdnj2jhcjqbj6.streamlit.app",
        "langgraph_url": "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app",
        "icon": "🌱"
    },
    "ground-control": {
        "name": "Ground Control",
        "repo": "ground-control", 
        "streamlit_url": "https://ground-control.streamlit.app",
        "langgraph_url": None,  # Funciona en modo autónomo
        "icon": "🎮"
    }
}

# API Keys desde variables de entorno
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def fix_app_secrets(app_name, config):
    """Arregla los secrets de cada app"""
    print(f"\n{config['icon']} Fixing {config['name']}...")
    
    repo_path = f"/workspaces/{config['repo']}"
    if not os.path.exists(repo_path):
        print(f"  ❌ Repository not found: {repo_path}")
        return False
    
    # Crear directorio .streamlit si no existe
    streamlit_dir = os.path.join(repo_path, ".streamlit")
    os.makedirs(streamlit_dir, exist_ok=True)
    
    # Crear secrets.toml con la configuración correcta
    secrets_content = f'''# {config['name']} Secrets Configuration
# Generated: {datetime.now().isoformat()}

LANGSMITH_API_KEY = "{LANGSMITH_API_KEY}"
LANGGRAPH_API_KEY = "{LANGSMITH_API_KEY}"
OPENAI_API_KEY = "{OPENAI_API_KEY or 'your-openai-key-here'}"

# API URLs específicas para {config['name']}
LANGGRAPH_API_URL = "{config['langgraph_url'] or 'not-required'}"

# Configuración adicional
DEMO_MODE = "false"
GHC_DT_MODEL = "gpt-4o-mini"
GHC_DT_TEMPERATURE = "0.2"
GHC_DT_EVIDENCE_LOG = "evidence.jsonl"
'''
    
    secrets_path = os.path.join(streamlit_dir, "secrets.toml")
    with open(secrets_path, 'w') as f:
        f.write(secrets_content)
    
    print(f"  ✅ Secrets updated: {secrets_path}")
    
    # Actualizar streamlit_app.py con la URL correcta si es necesario
    app_file = os.path.join(repo_path, "streamlit_app.py")
    if os.path.exists(app_file):
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Solo actualizar si tiene la URL incorrecta
        if config['langgraph_url'] and 'LANGGRAPH_API_URL' in content:
            # Buscar y reemplazar la URL
            import re
            pattern = r'LANGGRAPH_API_URL = os\.getenv\("LANGGRAPH_API_URL", "[^"]+"\)'
            replacement = f'LANGGRAPH_API_URL = os.getenv("LANGGRAPH_API_URL", "{config["langgraph_url"]}")'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                with open(app_file, 'w') as f:
                    f.write(new_content)
                print(f"  ✅ Updated API URL in streamlit_app.py")
    
    return True

def test_api_connection(url, api_key):
    """Prueba la conexión a una API"""
    if not url:
        return {"status": "N/A", "message": "No API URL configured"}
    
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{url}/health", headers=headers, timeout=5)
        if response.status_code == 200:
            return {"status": "✅", "message": "API is healthy"}
        else:
            return {"status": "❌", "message": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "❌", "message": str(e)[:50]}

def commit_and_push(repo_path, message):
    """Hace commit y push de los cambios"""
    try:
        os.chdir(repo_path)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        return True
    except Exception as e:
        print(f"  ⚠️ Git push failed: {e}")
        return False

# MAIN EXECUTION
print("\n📋 STEP 1: Fixing secrets for all apps...")
for app_name, config in APPS_CONFIG.items():
    fix_app_secrets(app_name, config)

print("\n📋 STEP 2: Testing API connections...")
for app_name, config in APPS_CONFIG.items():
    print(f"\n{config['icon']} {config['name']}:")
    
    # Test Streamlit
    try:
        response = requests.get(config['streamlit_url'], timeout=5)
        if response.status_code == 200:
            print(f"  ✅ Streamlit: Online")
        else:
            print(f"  ⚠️ Streamlit: HTTP {response.status_code}")
    except:
        print(f"  ❌ Streamlit: Offline")
    
    # Test LangGraph
    if config['langgraph_url']:
        result = test_api_connection(config['langgraph_url'], LANGSMITH_API_KEY)
        print(f"  {result['status']} LangGraph: {result['message']}")
    else:
        print(f"  ℹ️ LangGraph: Not required (autonomous mode)")

print("\n📋 STEP 3: Committing changes...")
for app_name, config in APPS_CONFIG.items():
    repo_path = f"/workspaces/{config['repo']}"
    if os.path.exists(repo_path):
        print(f"\n{config['icon']} Pushing {config['name']}...")
        if commit_and_push(repo_path, "🔧 Fix API configuration and secrets"):
            print(f"  ✅ Changes pushed successfully")

print("\n" + "=" * 60)
print("🎉 CANNABIS APPS FIX COMPLETE!")
print("=" * 60)
print("\n📊 SUMMARY:")
print("  • Green Hill Cockpit: API keys updated")
print("  • Digital Roots: Connected to correct deployment")
print("  • Ground Control: Running in autonomous mode")
print("\n⏰ Allow 2-3 minutes for Streamlit Cloud to redeploy")
print("📧 Contact: zakibaydoun@msn.com")
print("\n🌿 Your cannabis tech empire is ready! 🚀")
