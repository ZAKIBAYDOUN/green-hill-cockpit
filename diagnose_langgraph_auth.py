#!/usr/bin/env python3
"""
Diagnosticar problemas de autenticación con LangGraph
"""

import requests
import os
import json

print("🔍 DIAGNÓSTICO DE AUTENTICACIÓN LANGGRAPH")
print("=" * 60)

# Verificar variables de entorno
api_key = os.getenv("LANGSMITH_API_KEY", "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")
print(f"API Key: {api_key[:20]}...{api_key[-10:]}")

deployments = {
    "Green Hill Cockpit": "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app",
    "Digital Roots": "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app"
}

print("\n📊 Probando diferentes endpoints y métodos:\n")

for name, base_url in deployments.items():
    print(f"🔧 {name}:")
    print(f"   Base URL: {base_url}")
    
    # Probar diferentes endpoints
    endpoints = [
        ("GET", "/health", None),
        ("GET", "/", None),
        ("POST", "/invoke", {"question": "test", "agent": "ghc_dt", "state": {}})
    ]
    
    for method, endpoint, data in endpoints:
        url = f"{base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=5)
            else:
                response = requests.post(url, headers=headers, json=data, timeout=5)
            
            status = f"{response.status_code}"
            if response.status_code == 403:
                status += " ❌ Forbidden - API key no válida o sin permisos"
            elif response.status_code == 404:
                status += " ⚠️ Not Found - Endpoint no existe"
            elif response.status_code == 200:
                status += " ✅ OK"
            
            print(f"   {method} {endpoint}: {status}")
            
            # Si es 403, mostrar más detalles
            if response.status_code == 403:
                try:
                    error_detail = response.json()
                    print(f"      Detalle: {error_detail}")
                except:
                    print(f"      Response: {response.text[:100]}")
                    
        except Exception as e:
            print(f"   {method} {endpoint}: ❌ Error: {str(e)[:50]}")
    
    print()

print("\n💡 POSIBLES SOLUCIONES:")
print("1. Verificar que la API key es válida en LangSmith")
print("2. Verificar que los deployments existen y están activos")
print("3. Regenerar la API key si es necesario")
print("4. Verificar permisos del proyecto en LangSmith")
print("\n🔗 Dashboard: https://smith.langchain.com/")
