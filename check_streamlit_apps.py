#!/usr/bin/env python3
import requests
import time

apps = {
    "Green Hill Cockpit": "https://green-hill-cockpit.streamlit.app",
    "Digital Roots": "https://digital-roots-my7i9xaz3xdnj2jhcjqbj6.streamlit.app",
    "Ground Control": "https://ground-control.streamlit.app"
}

print("🌿 ESTADO DE APPS EN STREAMLIT CLOUD")
print("=" * 50)

for name, url in apps.items():
    try:
        start = time.time()
        response = requests.get(url, timeout=10, allow_redirects=True)
        elapsed = (time.time() - start) * 1000
        
        if response.status_code == 200:
            if "stlite" in response.text or "streamlit" in response.text:
                print(f"✅ {name}: Online ({elapsed:.0f}ms)")
            else:
                print(f"⚠️ {name}: Responde pero no es Streamlit")
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ {name}: Error - {str(e)[:30]}")

print("\n💡 Si alguna app muestra error:")
print("   - Verificar en https://share.streamlit.io/")
print("   - Puede estar reiniciándose (esperar 2-3 min)")
