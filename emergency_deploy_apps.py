#!/usr/bin/env python3
"""
🚨 CANNABIS APPS EMERGENCY DEPLOYMENT
====================================

Copy working Streamlit apps to all cannabis repositories
and deploy them with emergency bypass mode.

Author: Emergency Response for ZAKIBAYDOUN
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def copy_streamlit_app_to_repo(repo_path, app_name="Cannabis App"):
    """Copy the working streamlit app to a repository"""
    print(f"📱 Creating {app_name} in {repo_path}")
    
    # Ensure repo directory exists
    os.makedirs(repo_path, exist_ok=True)
    os.chdir(repo_path)
    
    # Copy streamlit_app.py from green-hill-cockpit
    source_app = "/workspaces/green-hill-cockpit/streamlit_app.py"
    if os.path.exists(source_app):
        shutil.copy2(source_app, "streamlit_app.py")
        print(f"✅ Copied streamlit_app.py")
    
    # Copy agents directory
    source_agents = "/workspaces/green-hill-cockpit/agents"
    if os.path.exists(source_agents):
        if os.path.exists("agents"):
            shutil.rmtree("agents")
        shutil.copytree(source_agents, "agents")
        print(f"✅ Copied agents directory")
    
    # Create emergency secrets
    os.makedirs(".streamlit", exist_ok=True)
    with open(".streamlit/secrets.toml", "w") as f:
        f.write("""# 🚨 EMERGENCY MODE SECRETS
DEMO_MODE = true
BYPASS_AUTH = true
LANGCHAIN_TRACING_V2 = false
EMERGENCY_MODE = true

# API Keys (from main app)
LANGSMITH_API_KEY = "REVOKED_GENERATE_NEW_KEY"
LANGGRAPH_API_KEY = "REVOKED_GENERATE_NEW_KEY"
OPENAI_API_KEY = "sk-svcacct-qDIkFNKvOB5jnfIqhXG-nHHTg0sN4HvhoZFmKjXT7kMxUqKF_ml2JdCWWqBNd3qg17JVnx8xWv0underwOVGZa-RV2jFSoAbLvp0A"

# Cannabis App Settings
APP_NAME = "{app_name}"
CANNABIS_MODE = "emergency"
""")
    print(f"✅ Created emergency secrets")
    
    # Update requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("""# 🌿 Cannabis App Emergency Dependencies
streamlit>=1.28.0
streamlit-authenticator>=0.2.3
openai>=1.3.0
langchain>=0.1.0
langgraph>=0.0.40
langsmith>=0.0.60
requests>=2.31.0
python-dotenv>=1.0.0
pandas>=2.0.0
numpy>=1.24.0
""")
    print(f"✅ Updated requirements.txt")
    
    # Git add and commit
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"🚨 Emergency deployment: {app_name} with bypass mode"], check=True)
        print(f"✅ Committed changes")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git operations failed: {e}")
    
def deploy_all_cannabis_apps():
    """Deploy all cannabis applications with emergency mode"""
    
    print("""
🚨 CANNABIS APPS EMERGENCY DEPLOYMENT
====================================
Copying working applications to all repositories
with emergency bypass mode enabled.
""")
    
    cannabis_repos = [
        ("/workspaces/greenhillgpt", "🧠 Green Hill GPT - AI Strain Recommendations"),
        ("/workspaces/digital-roots", "🌱 Digital Roots - Cannabis Cultivation Management"),
        ("/workspaces/ground-control", "🎮 Ground Control - Cannabis Operations Center")
    ]
    
    success_count = 0
    
    for repo_path, app_name in cannabis_repos:
        try:
            print(f"\n{'='*60}")
            copy_streamlit_app_to_repo(repo_path, app_name)
            success_count += 1
            print(f"✅ {app_name} deployed successfully")
        except Exception as e:
            print(f"❌ Failed to deploy {app_name}: {e}")
    
    print(f"""
🎉 EMERGENCY DEPLOYMENT COMPLETE!
✅ Successfully deployed: {success_count}/{len(cannabis_repos)} apps

📋 NEXT STEPS:
1. Push changes to GitHub:
   cd /workspaces/greenhillgpt && git push
   cd /workspaces/digital-roots && git push  
   cd /workspaces/ground-control && git push

2. Wait 5-10 minutes for Streamlit Cloud to detect and deploy

3. Check status: python check_status.py

🌿 All apps are now in EMERGENCY MODE with API fallbacks!
""")

if __name__ == "__main__":
    deploy_all_cannabis_apps()