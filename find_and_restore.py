#!/usr/bin/env python3
"""
🆘 LANGGRAPH DEPLOYMENT FINDER & RESTORER
========================================

Since the deployment ID returned 404, let's find the correct deployment
and restore it manually.

For: ZAKIBAYDOUN (Cannabis Tech Entrepreneur)
"""

import requests
import json
import os
from datetime import datetime

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")
ORG_ID = "3d60abf5-78b5-4d90-8b55-2f69b0f53557"  # Your organization ID
BASE_URL = "https://api.smith.langchain.com/api/v1"

def find_all_deployments():
    """Find all deployments in your organization"""
    
    print("🔍 FINDING ALL LANGGRAPH DEPLOYMENTS")
    print("=" * 50)
    
    headers = {
        "Authorization": f"Bearer {LANGSMITH_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Try different endpoints to find deployments
        endpoints_to_try = [
            f"{BASE_URL}/deployments",
            f"{BASE_URL}/organizations/{ORG_ID}/deployments",
            f"{BASE_URL}/deployments?organization_id={ORG_ID}"
        ]
        
        for endpoint in endpoints_to_try:
            print(f"🔍 Trying: {endpoint}")
            
            response = requests.get(endpoint, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                deployments = response.json()
                print(f"✅ Found deployments!")
                
                if isinstance(deployments, dict) and 'deployments' in deployments:
                    deployments = deployments['deployments']
                
                if not deployments:
                    print("No deployments found")
                    continue
                
                print(f"\n📊 Found {len(deployments)} deployments:")
                
                for i, deployment in enumerate(deployments):
                    print(f"\n{i+1}. Deployment:")
                    print(f"   ID: {deployment.get('id', 'Unknown')}")
                    print(f"   Name: {deployment.get('name', 'Unknown')}")
                    print(f"   Status: {deployment.get('status', 'Unknown')}")
                    print(f"   URL: {deployment.get('url', 'Unknown')}")
                    print(f"   Created: {deployment.get('created_at', 'Unknown')}")
                    
                    # Check if this might be Digital Roots
                    name = deployment.get('name', '').lower()
                    if 'digital' in name or 'roots' in name:
                        print(f"   🎯 POTENTIAL DIGITAL ROOTS DEPLOYMENT!")
                
                return deployments
            
            elif response.status_code == 401:
                print("❌ Authentication failed - check your API key")
                return None
            
            elif response.status_code == 404:
                print("⚠️ Endpoint not found")
            
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
        
        print("\n❌ Could not find deployments through API")
        return None
        
    except Exception as e:
        print(f"❌ Error finding deployments: {e}")
        return None

def manual_restore_instructions():
    """Provide manual restore instructions"""
    
    print("\n🆘 MANUAL RESTORE INSTRUCTIONS")
    print("=" * 50)
    print()
    print("Since API access is limited, please restore manually:")
    print()
    print("🌐 OPTION 1: LangSmith Dashboard (RECOMMENDED)")
    print("1. Go to: https://smith.langchain.com/")
    print("2. Login with your account")
    print("3. Navigate to: Deployments section")
    print("4. Look for deployment containing 'digitalroots' or 'digital-roots'")
    print("5. Click on the deployment")
    print("6. Go to: Version History or Versions tab")
    print("7. Find version created BEFORE 17:00 UTC today (2025-08-20)")
    print("8. Click 'Rollback' on that version")
    print()
    print("📧 OPTION 2: Contact Support")
    print("Email: support@langchain.com")
    print("Subject: URGENT: Accidental deployment overwrite - need rollback")
    print("Body: Include these details:")
    print("   - Your organization ID: 3d60abf5-78b5-4d90-8b55-2f69b0f53557")
    print("   - Deployment name: Digital Roots or similar")
    print("   - Request rollback to version before 17:00 UTC on 2025-08-20")
    print("   - Explain that AI accidentally overwrote your deployment")
    print()
    print("🔧 OPTION 3: Re-deploy from Backup")
    print("If you have the original Digital Roots code:")
    print("1. Create a new LangGraph deployment")
    print("2. Deploy your original code")
    print("3. Update your Streamlit app to use the new endpoint")
    print()
    print("💡 IMMEDIATE ACTION:")
    print("Check if you have Digital Roots code backed up in:")
    print("- Git history in digital-roots repo")
    print("- Local files")
    print("- Previous commits")
    
def check_git_history():
    """Check git history for Digital Roots backup"""
    
    print("\n🔍 CHECKING GIT HISTORY FOR DIGITAL ROOTS")
    print("=" * 50)
    
    try:
        import subprocess
        
        # Change to digital-roots directory
        os.chdir("/workspaces/digital-roots")
        
        # Get git log
        result = subprocess.run([
            "git", "log", "--oneline", "-10"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("📝 Recent git commits:")
            print(result.stdout)
            
            # Check if we can find original code
            print("\n🔍 Checking for original Digital Roots code...")
            
            # Try to show content from before the bulletproof deployment
            show_result = subprocess.run([
                "git", "show", "94c540c:streamlit_app.py"
            ], capture_output=True, text=True)
            
            if show_result.returncode == 0:
                print("✅ Found original Digital Roots code in git!")
                print("First 20 lines:")
                lines = show_result.stdout.split('\n')[:20]
                for line in lines:
                    print(f"   {line}")
                
                print("\n💡 You can restore with:")
                print("   cd /workspaces/digital-roots")
                print("   git checkout 94c540c -- streamlit_app.py")
                print("   # Then re-deploy to LangGraph")
                
                return True
        
        print("⚠️ Could not access git history")
        return False
        
    except Exception as e:
        print(f"⚠️ Error checking git history: {e}")
        return False

if __name__ == "__main__":
    print("🆘 DIGITAL ROOTS DEPLOYMENT RECOVERY")
    print(f"Time: {datetime.now().isoformat()}")
    print("User: ZAKIBAYDOUN")
    print()
    
    # Try to find deployments
    deployments = find_all_deployments()
    
    if not deployments:
        print("\n🔍 Checking local git history for backup...")
        found_backup = check_git_history()
        
        if found_backup:
            print("\n✅ GOOD NEWS: Your original code is in git history!")
        else:
            print("\n⚠️ Could not find local backup")
    
    # Always show manual instructions
    manual_restore_instructions()
    
    print("\n🎯 IMMEDIATE NEXT STEPS:")
    print("1. Try the LangSmith dashboard method first")
    print("2. If that fails, restore from git and re-deploy")
    print("3. Contact support as backup option")
    print()
    print("💪 Don't worry - your Digital Roots can be restored!")