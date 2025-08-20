#!/usr/bin/env python3
"""
Habilitar modo demo en todas las apps para que funcionen sin LangGraph
"""

import os

apps = ["green-hill-cockpit", "digital-roots", "ground-control"]

for app in apps:
    secrets_path = f"/workspaces/{app}/.streamlit/secrets.toml"
    
    if os.path.exists(secrets_path):
        # Leer archivo actual
        with open(secrets_path, 'r') as f:
            content = f.read()
        
        # Asegurar que DEMO_MODE está en true
        if 'DEMO_MODE' in content:
            # Reemplazar valor existente
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('DEMO_MODE'):
                    lines[i] = 'DEMO_MODE = "true"'
            content = '\n'.join(lines)
        else:
            # Agregar al final
            content += '\n\n# Modo demo habilitado temporalmente\nDEMO_MODE = "true"\n'
        
        # Guardar
        with open(secrets_path, 'w') as f:
            f.write(content)
        
        print(f"✅ {app}: Modo demo habilitado")
    else:
        print(f"⚠️ {app}: No tiene secrets.toml")

print("\n💡 Las apps ahora funcionarán en modo demo")
print("   Esto permite usar la interfaz sin depender de LangGraph")
