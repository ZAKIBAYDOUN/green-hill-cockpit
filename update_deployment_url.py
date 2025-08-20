#!/usr/bin/env python3
"""
Actualizar Green Hill Cockpit con el deployment correcto de LangSmith
"""

import re

# El nuevo deployment ID correcto
NEW_DEPLOYMENT_ID = "243a8593-9c11-47ea-b164-4959510bb2de"
NEW_URL = f"https://{NEW_DEPLOYMENT_ID}.us.langgraph.app"

print(f"🔧 Actualizando Green Hill Cockpit con nuevo deployment")
print(f"📋 Deployment ID: {NEW_DEPLOYMENT_ID}")
print(f"🔗 Nueva URL: {NEW_URL}")

# Actualizar streamlit_app.py
with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Buscar y reemplazar la URL antigua
old_pattern = r'https://cockpit-[a-zA-Z0-9\-]+\.us\.langgraph\.app'
content = re.sub(old_pattern, NEW_URL, content)

# También actualizar si está hardcodeada
content = content.replace(
    'https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app',
    NEW_URL
)

# Guardar cambios
with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("✅ streamlit_app.py actualizado")

# Actualizar secrets.toml
secrets_path = '.streamlit/secrets.toml'
try:
    with open(secrets_path, 'r') as f:
        secrets_content = f.read()
    
    # Actualizar URL en secrets
    secrets_content = re.sub(
        r'LANGGRAPH_API_URL = "[^"]*"',
        f'LANGGRAPH_API_URL = "{NEW_URL}"',
        secrets_content
    )
    
    with open(secrets_path, 'w') as f:
        f.write(secrets_content)
    
    print("✅ secrets.toml actualizado")
except Exception as e:
    print(f"⚠️ No se pudo actualizar secrets.toml: {e}")

print("\n🎉 Deployment actualizado correctamente!")
print(f"🔗 Tu app ahora usa: {NEW_URL}")
