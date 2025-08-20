#!/usr/bin/env python3
"""
🌿 Quick Cannabis Apps Status Checker
=====================================

Fast status check for all your cannabis applications
Perfect for monitoring after deployment
Author: Zaki Baydoun (zakibaydoun@msn.com)

Usage: python check_status.py
"""

import requests
import time
from datetime import datetime
import sys

# Your Cannabis Apps Configuration
APPS = {
    "Green Hill GPT": {
        "streamlit": "https://greenhillgpt.streamlit.app",
        "langgraph": "https://green-hill-gpt-ai-a1b2c3d4e5f6.us.langgraph.app",
        "emoji": "🧠"
    },
    "Digital Roots": {
        "streamlit": "https://digital-roots.streamlit.app", 
        "langgraph": "https://digital-roots-cultivation-g7h8i9j0k1l2.us.langgraph.app",
        "emoji": "🌱"
    },
    "Ground Control": {
        "streamlit": "https://ground-control.streamlit.app",
        "langgraph": "https://ground-control-a0ae430fa0b85ca09ebb486704b69f2b.us.langgraph.app", 
        "emoji": "🎮"
    }
}

def check_url_status(url, timeout=10):
    """Check if a URL is responding"""
    try:
        response = requests.get(url, timeout=timeout)
        return {
            "status": "✅ Online" if response.status_code == 200 else f"⚠️  HTTP {response.status_code}",
            "response_time": round(response.elapsed.total_seconds() * 1000, 2),
            "success": response.status_code == 200
        }
    except requests.exceptions.Timeout:
        return {"status": "⏰ Timeout", "response_time": timeout * 1000, "success": False}
    except requests.exceptions.ConnectionError:
        return {"status": "❌ Connection Failed", "response_time": 0, "success": False}
    except Exception as e:
        return {"status": f"❌ Error: {str(e)[:50]}", "response_time": 0, "success": False}

def main():
    print(f"""
🌿============================================================================🌿
                          CANNABIS APPS STATUS CHECK                           
                            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                              
🌿============================================================================🌿
""")
    
    total_services = 0
    online_services = 0
    
    for app_name, app_config in APPS.items():
        print(f"\n{app_config['emoji']} {app_name}")
        print("─" * 60)
        
        # Check Streamlit app
        print(f"📊 Streamlit App: {app_config['streamlit']}")
        streamlit_result = check_url_status(app_config['streamlit'])
        print(f"   Status: {streamlit_result['status']} ({streamlit_result['response_time']}ms)")
        total_services += 1
        if streamlit_result['success']:
            online_services += 1
            
        # Check LangGraph API
        print(f"🔧 LangGraph API: {app_config['langgraph']}")
        langgraph_result = check_url_status(app_config['langgraph'])
        print(f"   Status: {langgraph_result['status']} ({langgraph_result['response_time']}ms)")
        total_services += 1  
        if langgraph_result['success']:
            online_services += 1
    
    # Summary
    print(f"""
🌿============================================================================🌿
                                 SUMMARY                                       
🌿============================================================================🌿

📊 Services Online: {online_services}/{total_services}
⚡ Success Rate: {(online_services/total_services*100):.1f}%
📧 Contact: zakibaydoun@msn.com
🐙 GitHub: @zakibaydoun

""")
    
    if online_services == total_services:
        print("🎉 All cannabis applications are running perfectly!")
        print("🌿 Your automated deployment system is working flawlessly.")
        sys.exit(0)
    else:
        print("⚠️  Some services are offline. Check the details above.")
        print("💡 Run 'python fix_everything.py' to redeploy if needed.")
        sys.exit(1)

if __name__ == "__main__":
    main()