#!/usr/bin/env python3
"""
Actualizar todas las configuraciones de deployment con las URLs correctas
"""

import os
import json

print("🔧 Updating deployment configurations...")

# Configuración CORRECTA
CORRECT_CONFIG = {
    "organization": "green-hill-canarias",
    "team": "digital-roots",
    "apps": {
        "green-hill-cockpit": {
            "repo_url": "https://github.com/green-hill-canarias/green-hill-cockpit",
            "streamlit_url": "https://green-hill-cockpit.streamlit.app",
            "langgraph_url": "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app"
        },
        "digital-roots": {
            "repo_url": "https://github.com/green-hill-canarias/digital-roots",
            "streamlit_url": "https://digital-roots-my7i9xaz3xdnj2jhcjqbj6.streamlit.app",
            "langgraph_url": "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app"
        },
        "ground-control": {
            "repo_url": "https://github.com/green-hill-canarias/ground-control",
            "streamlit_url": "https://ground-control.streamlit.app",
            "langgraph_url": None  # Autonomous mode
        }
    }
}

# Guardar configuración correcta
with open('correct_deployment_config.json', 'w') as f:
    json.dump(CORRECT_CONFIG, f, indent=2)

print("✅ Configuration saved to correct_deployment_config.json")

# Actualizar git remotes si es necesario
for app_name, config in CORRECT_CONFIG['apps'].items():
    app_path = f"/workspaces/{app_name}"
    if os.path.exists(app_path):
        print(f"\n📁 Updating {app_name} git remote...")
        os.chdir(app_path)
        
        # Get current remote
        result = os.popen("git remote get-url origin").read().strip()
        
        if "ZAKIBAYDOUN" in result or "digital-roots" in result and app_name != "digital-roots":
            # Update to correct URL
            correct_url = config['repo_url']
            os.system(f"git remote set-url origin {correct_url}")
            print(f"  ✅ Updated remote to: {correct_url}")
        else:
            print(f"  ✅ Remote already correct: {result}")

print("\n✅ All configurations updated!")
print("\n📋 IMPORTANT:")
print("- Organization: green-hill-canarias")
print("- Team: digital-roots (for permissions)")
print("- All repos under: github.com/green-hill-canarias/")
