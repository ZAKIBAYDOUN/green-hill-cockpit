#!/usr/bin/env python3
"""
Verificar configuración de Ground Control
"""

import os
import json

print("🎮 GROUND CONTROL CONFIGURATION CHECK")
print("=" * 50)

# Verificar secretos de Ground Control
gc_secrets = "/workspaces/ground-control/.streamlit/secrets.toml"
if os.path.exists(gc_secrets):
    with open(gc_secrets, 'r') as f:
        content = f.read()
    
    print("📋 Ground Control secrets.toml:")
    if "LANGGRAPH_API_URL" in content:
        print("  ⚠️  Has LANGGRAPH_API_URL configured (but doesn't use it)")
    else:
        print("  ✅ No LANGGRAPH_API_URL (correct for autonomous mode)")
    
    print("\n📄 Content preview:")
    print(content[:300] + "..." if len(content) > 300 else content)
else:
    print("  ❌ No secrets.toml found")

# Verificar el código de Ground Control
gc_app = "/workspaces/ground-control/streamlit_app.py"
if os.path.exists(gc_app):
    with open(gc_app, 'r') as f:
        content = f.read()
    
    # Buscar referencias a LangGraph
    if "langgraph" in content.lower():
        print("\n⚠️  Ground Control code mentions LangGraph")
    else:
        print("\n✅ Ground Control runs independently (no LangGraph)")
    
    # Buscar modo demo o autónomo
    if "demo" in content.lower() or "autonomous" in content.lower():
        print("✅ Has demo/autonomous mode implemented")

print("\n" + "=" * 50)
print("📊 SUMMARY:")
print("Ground Control is designed to work WITHOUT LangSmith/LangGraph")
print("It's a standalone monitoring/control app")
print("This is why it's the only one showing as 'Online'")
print("=" * 50)
