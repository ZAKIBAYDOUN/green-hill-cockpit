#!/usr/bin/env python3
"""
Verificar la estructura real de GitHub para Green Hill Canarias
"""

import subprocess
import json

print("🌿 GREEN HILL CANARIAS - GitHub Structure Analysis")
print("=" * 60)

# La estructura CORRECTA es:
print("✅ ESTRUCTURA CORRECTA IDENTIFICADA:")
print("├── Organización: green-hill-canarias")
print("│   ├── Team: digital-roots")
print("│   └── Repositorios:")
print("│       ├── green-hill-cockpit (el actual)")
print("│       ├── digital-roots (repo dentro de la org)")
print("│       └── ground-control (repo dentro de la org)")
print("")

# Verificar con GitHub CLI
try:
    # Listar repos de la organización
    result = subprocess.run(
        ["gh", "repo", "list", "green-hill-canarias", "--limit", "50", "--json", "name,url"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        repos = json.loads(result.stdout)
        print(f"📁 Repositorios en green-hill-canarias: {len(repos)}")
        for repo in repos:
            print(f"   - {repo['name']}: {repo['url']}")
    else:
        print("❌ No se pudo listar repos (puede necesitar autenticación)")
        
except Exception as e:
    print(f"⚠️ GitHub CLI no disponible: {e}")

print("\n📋 ACCIONES NECESARIAS:")
print("1. Todos los repos deben estar en: github.com/green-hill-canarias/")
print("2. NO usar digital-roots como organización separada")
print("3. Usar el team digital-roots para permisos dentro de la org")
print("=" * 60)
