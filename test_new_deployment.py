#!/usr/bin/env python3
"""
Probar el nuevo deployment de LangSmith
"""

import requests
import os

# Configuración del nuevo deployment
deployment_url = "https://243a8593-9c11-47ea-b164-4959510bb2de.us.langgraph.app"
api_key = os.getenv("LANGSMITH_API_KEY", "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")

print("🔍 PROBANDO NUEVO DEPLOYMENT")
print("=" * 50)
print(f"URL: {deployment_url}")
print(f"Deployment ID: 243a8593-9c11-47ea-b164-4959510bb2de")
print(f"API Key: {api_key[:20]}...{api_key[-10:]}")

# Probar health endpoint
headers = {"Authorization": f"Bearer {api_key}"}

print("\n📊 Probando conexión...")
try:
    response = requests.get(f"{deployment_url}/health", headers=headers, timeout=10)
    print(f"Status: HTTP {response.status_code}")
    
    if response.status_code == 200:
        print("\n✅ ¡ÉXITO! El deployment está funcionando correctamente")
        print("Tu Green Hill Cockpit ahora puede conectarse a LangGraph")
    elif response.status_code == 403:
        print("\n❌ Error 403: La API key no tiene permisos para este deployment")
        print("Verifica en LangSmith que la API key tenga acceso")
    elif response.status_code == 404:
        print("\n⚠️ Error 404: El endpoint /health no existe")
        print("El deployment podría estar funcionando pero sin health check")
    else:
        print(f"\n⚠️ Respuesta inesperada: {response.text[:200]}")
        
except Exception as e:
    print(f"\n❌ Error de conexión: {e}")
    
print("\n💡 PRÓXIMOS PASOS:")
print("1. Si funciona: commit y push los cambios")
print("2. Si da 403: verificar permisos en LangSmith")
print("3. Si da error: verificar que el deployment está activo")
