#!/usr/bin/env python3
"""
🆘 LANGGRAPH EMERGENCY RESTORE
=============================

CRITICAL: Restore LangGraph deployment that was overwritten by AI!

Deployment ID: digitalroots-bf3899aefd705f6789c2466e0c9b974d
Target: Rollback to version BEFORE 17:00 UTC on 2025-08-20
Status: EMERGENCY RESTORE IN PROGRESS

For: ZAKIBAYDOUN (Cannabis Tech Entrepreneur)
"""

import requests
import json
import os
from datetime import datetime
import sys

# Configuration
DEPLOYMENT_ID = "digitalroots-bf3899aefd705f6789c2466e0c9b974d"
CRITICAL_TIME = "2025-08-20T17:00:00Z"
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "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")
BASE_URL = "https://api.smith.langchain.com/api/v1"

def emergency_restore():
    """Emergency restore of LangGraph deployment"""
    
    print("🆘 LANGGRAPH EMERGENCY RESTORE")
    print("=" * 50)
    print(f"Deployment ID: {DEPLOYMENT_ID}")
    print(f"Critical Time: {CRITICAL_TIME}")
    print(f"Current Time: {datetime.utcnow().isoformat()}Z")
    print(f"User: ZAKIBAYDOUN")
    print()
    
    if not LANGSMITH_API_KEY or LANGSMITH_API_KEY == "your-api-key-here":
        print("❌ LANGSMITH_API_KEY not found!")
        print("Set it with: export LANGSMITH_API_KEY='your_key'")
        return False
    
    headers = {
        "Authorization": f"Bearer {LANGSMITH_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "DigitalRoots-Emergency-Restore/1.0"
    }
    
    try:
        # Step 1: Backup current state
        print("🔄 Step 1: Backing up current deployment state...")
        current_url = f"{BASE_URL}/deployments/{DEPLOYMENT_ID}"
        current_response = requests.get(current_url, headers=headers)
        
        if current_response.status_code == 200:
            backup_file = f"digitalroots_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w') as f:
                json.dump(current_response.json(), f, indent=2)
            print(f"✅ Current state backed up to: {backup_file}")
        else:
            print(f"⚠️ Could not backup current state: {current_response.status_code}")
        
        # Step 2: List deployment versions
        print("\n🔍 Step 2: Listing deployment versions...")
        versions_url = f"{BASE_URL}/deployments/{DEPLOYMENT_ID}/versions"
        versions_response = requests.get(versions_url, headers=headers)
        
        if versions_response.status_code != 200:
            print(f"❌ Failed to get versions: {versions_response.status_code}")
            print(f"Response: {versions_response.text}")
            return False
        
        versions = versions_response.json()
        print(f"📊 Found {len(versions)} deployment versions:")
        
        # Step 3: Find version before critical time
        safe_version = None
        print(f"\n🎯 Step 3: Finding safe version before {CRITICAL_TIME}...")
        
        for i, version in enumerate(versions[:10]):  # Show last 10 versions
            created_at = version.get('created_at', '')
            version_id = version.get('id', 'Unknown')
            status = version.get('status', 'Unknown')
            
            print(f"  {i+1}. Version: {version_id}")
            print(f"     Created: {created_at}")
            print(f"     Status: {status}")
            
            if created_at < CRITICAL_TIME and safe_version is None:
                safe_version = version
                print(f"     🎯 SAFE VERSION FOUND!")
            
            print()
        
        if not safe_version:
            print("❌ No safe version found before critical time!")
            print("⚠️ This might mean:")
            print("   - The deployment is newer than expected")
            print("   - All versions are after the critical time")
            print("   - Manual intervention required")
            return False
        
        # Step 4: Execute rollback
        print(f"🔄 Step 4: Rolling back to safe version...")
        print(f"Target Version: {safe_version['id']}")
        print(f"Created At: {safe_version['created_at']}")
        
        rollback_url = f"{BASE_URL}/deployments/{DEPLOYMENT_ID}/rollback"
        rollback_data = {
            "version_id": safe_version['id']
        }
        
        rollback_response = requests.post(rollback_url, json=rollback_data, headers=headers)
        
        if rollback_response.status_code in [200, 202]:
            print("✅ ROLLBACK INITIATED SUCCESSFULLY!")
            print(f"Response: {rollback_response.json()}")
        else:
            print(f"❌ ROLLBACK FAILED: {rollback_response.status_code}")
            print(f"Response: {rollback_response.text}")
            return False
        
        # Step 5: Verify rollback
        print(f"\n✅ Step 5: Verifying rollback...")
        
        # Wait a moment for the rollback to process
        import time
        time.sleep(3)
        
        # Check deployment status
        verify_response = requests.get(current_url, headers=headers)
        if verify_response.status_code == 200:
            deployment_info = verify_response.json()
            current_version = deployment_info.get('current_version', {}).get('id', 'Unknown')
            
            if current_version == safe_version['id']:
                print("🎉 ROLLBACK VERIFIED SUCCESSFUL!")
                print(f"Current Version: {current_version}")
                print(f"Target Version: {safe_version['id']}")
            else:
                print("⚠️ Rollback may still be in progress...")
                print(f"Current Version: {current_version}")
                print(f"Expected Version: {safe_version['id']}")
        
        # Step 6: Test endpoint
        print(f"\n🧪 Step 6: Testing restored endpoint...")
        
        # Construct deployment URL
        deployment_url = f"https://digitalroots-{DEPLOYMENT_ID}.us.langgraph.app"
        
        try:
            test_response = requests.get(deployment_url, timeout=10)
            if test_response.status_code == 200:
                print("✅ ENDPOINT IS RESPONDING!")
                print(f"URL: {deployment_url}")
            else:
                print(f"⚠️ Endpoint responding with status: {test_response.status_code}")
        except Exception as e:
            print(f"⚠️ Could not test endpoint: {e}")
        
        print("\n🎉 EMERGENCY RESTORE COMPLETED!")
        print("=" * 50)
        print("✅ Deployment has been rolled back to safe version")
        print("✅ Your Digital Roots should now be restored")
        print("✅ Test your app to confirm everything works")
        print()
        print("📋 NEXT STEPS:")
        print("1. Test Digital Roots app thoroughly")
        print("2. Add deployment protection to prevent overwrites")
        print("3. Create regular backups")
        print("4. Document what went wrong")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR during restore: {e}")
        print("\n🆘 MANUAL RESTORE REQUIRED:")
        print("1. Go to: https://smith.langchain.com/")
        print(f"2. Find deployment: {DEPLOYMENT_ID}")
        print("3. Click Version History")
        print(f"4. Find version before {CRITICAL_TIME}")
        print("5. Click Rollback")
        
        return False

def install_langgraph_cli():
    """Install LangGraph CLI for additional restore options"""
    
    print("🔧 Installing LangGraph CLI for additional options...")
    
    try:
        import subprocess
        
        # Install LangGraph CLI
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-U", "langgraph-cli"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ LangGraph CLI installed successfully")
            
            print("\n📋 Manual CLI Commands (if API restore fails):")
            print("langgraph auth login")
            print(f"langgraph deployments list-versions --deployment-id {DEPLOYMENT_ID}")
            print(f"langgraph deployments rollback --deployment-id {DEPLOYMENT_ID} --version-id VERSION_ID")
            
            return True
        else:
            print(f"⚠️ CLI install failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️ Could not install CLI: {e}")
        return False

if __name__ == "__main__":
    print("🆘 DIGITAL ROOTS EMERGENCY RESTORE")
    print("Time:", datetime.utcnow().isoformat() + "Z")
    print("User: ZAKIBAYDOUN")
    print("Status: OVERWRITTEN BY AI - RESTORING NOW!")
    print()
    
    # Check for emergency flag
    if "--emergency-rollback" in sys.argv:
        print("🚨 EMERGENCY ROLLBACK MODE ACTIVATED!")
    
    success = emergency_restore()
    
    if not success:
        print("\n🔧 Trying to install CLI for alternative restore...")
        install_langgraph_cli()
        
    print(f"\nRestore completed at: {datetime.utcnow().isoformat()}Z")