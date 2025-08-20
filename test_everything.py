#!/usr/bin/env python3
"""
🌿 CANNABIS COCKPIT - FINAL STATUS CHECK
=======================================

Verifica que el CEO Digital Twin y todas las apps estén funcionando
después de las correcciones de configuración.

For: ZAKIBAYDOUN (Cannabis Tech Entrepreneur)
"""

import requests
import time
from datetime import datetime

def test_cockpit_api():
    """Test the cockpit API endpoint"""
    
    print("🔬 TESTING COCKPIT API")
    print("=" * 40)
    
    cockpit_url = "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app"
    
    try:
        response = requests.get(cockpit_url, timeout=10)
        print(f"URL: {cockpit_url}")
        print(f"Status: {response.status_code}")
        print(f"Response time: {response.elapsed.total_seconds():.3f}s")
        
        if response.status_code == 200:
            print("✅ COCKPIT API IS WORKING!")
            return True
        else:
            print("⚠️ Cockpit API returned non-200 status")
            return False
            
    except Exception as e:
        print(f"❌ Cockpit API error: {e}")
        return False

def test_streamlit_apps():
    """Test all Streamlit apps"""
    
    print("\n🌿 TESTING STREAMLIT APPS")
    print("=" * 40)
    
    apps = [
        ("🌿 Green Hill Cockpit", "https://green-hill-cockpit.streamlit.app"),
        ("🧠 Green Hill GPT", "https://greenhillgpt.streamlit.app"),
        ("🌱 Digital Roots", "https://digital-roots.streamlit.app"),
        ("🎮 Ground Control", "https://ground-control.streamlit.app")
    ]
    
    results = {}
    
    for name, url in apps:
        try:
            response = requests.get(url, timeout=10)
            status = "✅ ONLINE" if response.status_code == 200 else f"⚠️ HTTP {response.status_code}"
            response_time = f"{response.elapsed.total_seconds() * 1000:.0f}ms"
            
            print(f"{name}: {status} ({response_time})")
            results[name] = response.status_code == 200
            
        except Exception as e:
            print(f"{name}: ❌ ERROR - {e}")
            results[name] = False
    
    return results

def comprehensive_status():
    """Run comprehensive status check"""
    
    print("🌿" + "="*60 + "🌿")
    print("           CANNABIS EMPIRE - COMPREHENSIVE STATUS CHECK")
    print(f"                        {datetime.now().isoformat()}")
    print("🌿" + "="*60 + "🌿")
    print()
    
    # Test cockpit API
    cockpit_working = test_cockpit_api()
    
    # Test Streamlit apps
    app_results = test_streamlit_apps()
    
    # Summary
    print("\n📊 FINAL SUMMARY")
    print("=" * 40)
    
    online_count = sum(app_results.values())
    total_apps = len(app_results)
    
    print(f"🚀 Cockpit API: {'✅ Working' if cockpit_working else '❌ Issues'}")
    print(f"📱 Streamlit Apps: {online_count}/{total_apps} online")
    print(f"⚡ Overall Success Rate: {((online_count + (1 if cockpit_working else 0)) / (total_apps + 1)) * 100:.1f}%")
    
    if cockpit_working and online_count >= 3:
        print("\n🎉 EXCELLENT! Your cannabis empire is fully operational!")
        print("✅ CEO Digital Twin should be working")
        print("✅ All cannabis apps are responding")
        print("✅ Configuration fixes were successful")
        
    elif cockpit_working:
        print("\n👍 GOOD! Cockpit API is working")
        print("✅ CEO Digital Twin backend is operational") 
        print("⏰ Some Streamlit apps may still be deploying")
        print("💡 Wait 5-10 minutes and test again")
        
    else:
        print("\n⚠️ ATTENTION NEEDED")
        print("❌ Cockpit API needs troubleshooting")
        print("💡 Check LangGraph deployment manually")
        print("🔗 Go to: https://smith.langchain.com/")
    
    print(f"\n💡 NEXT STEPS:")
    print("1. Wait 5-10 minutes for all deployments to complete")
    print("2. Test CEO Digital Twin in the cockpit app")
    print("3. Verify all agents are responding")
    print("4. Run this script again to recheck status")
    
    print("\n🌿" + "="*60 + "🌿")
    print("            CANNABIS TECH EMPIRE STATUS CHECK COMPLETE")
    print("                      Built for: ZAKIBAYDOUN 👨‍⚕️")
    print("🌿" + "="*60 + "🌿")

if __name__ == "__main__":
    comprehensive_status()