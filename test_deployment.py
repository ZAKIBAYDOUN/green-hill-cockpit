#!/usr/bin/env python3
"""
🌿 Cannabis Apps Deployment - Test & Demo
=========================================

Quick test to verify everything is working before full deployment
Author: Zaki Baydoun (zakibaydoun@msn.com)

Usage: python test_deployment.py
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path

def test_environment():
    """Test if environment is properly configured"""
    print("🔍 Testing environment configuration...")
    
    required_vars = ["LANGSMITH_API_KEY", "GITHUB_TOKEN", "OPENAI_API_KEY", "STREAMLIT_SHARING_EMAIL"]
    missing_vars = []
    
    # Try to load from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed, checking environment variables directly")
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    print("✅ All environment variables found")
    return True

def test_internet_connection():
    """Test internet connectivity"""
    print("🌐 Testing internet connection...")
    
    test_urls = [
        "https://api.github.com",
        "https://api.smith.langchain.com", 
        "https://api.openai.com",
        "https://streamlit.io"
    ]
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {url} - HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - {str(e)}")
            return False
    
    return True

def test_python_environment():
    """Test Python environment"""
    print("🐍 Testing Python environment...")
    
    print(f"✅ Python version: {sys.version}")
    print(f"✅ Python executable: {sys.executable}")
    
    required_modules = ["requests", "json", "os", "sys", "pathlib", "datetime"]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module {module}: Available")
        except ImportError:
            print(f"❌ Module {module}: Missing")
            return False
    
    return True

def create_demo_config():
    """Create demo configuration files"""
    print("📋 Creating demo configuration...")
    
    # Create demo .env if it doesn't exist
    if not os.path.exists(".env"):
        demo_env = """# 🌿 Demo Environment Variables
# Replace with your actual values

LANGSMITH_API_KEY=ls__your_langsmith_api_key_here
GITHUB_TOKEN=ghp_your_github_token_here  
OPENAI_API_KEY=sk-your_openai_api_key_here
STREAMLIT_SHARING_EMAIL=zakibaydoun@msn.com

# Demo settings
DEMO_MODE=true
DEBUG_MODE=true
"""
        with open(".env", "w") as f:
            f.write(demo_env)
        print("✅ Created demo .env file")
    else:
        print("✅ .env file already exists")
    
    return True

def main():
    """Run complete deployment test"""
    
    print(f"""
🌿============================================================================🌿
                      CANNABIS DEPLOYMENT SYSTEM TEST                          
                            {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🌿============================================================================🌿

👤 Pharmacist: Zaki Baydoun
📧 Contact: zakibaydoun@msn.com
🎯 Testing deployment readiness for 3 cannabis applications

This test will verify:
✓ Environment variables and API keys
✓ Internet connectivity to required services  
✓ Python environment and dependencies
✓ Configuration files

🌿============================================================================🌿
""")
    
    test_results = []
    
    # Run tests
    test_results.append(("Environment Variables", test_environment()))
    test_results.append(("Internet Connection", test_internet_connection()))  
    test_results.append(("Python Environment", test_python_environment()))
    test_results.append(("Demo Configuration", create_demo_config()))
    
    # Summary
    print(f"\n🌿============================================================================🌿")
    print("                                TEST RESULTS")
    print("🌿============================================================================🌿")
    
    passed_tests = 0
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed_tests += 1
    
    print(f"\n📊 Tests Passed: {passed_tests}/{len(test_results)}")
    
    if passed_tests == len(test_results):
        print("""
🎉 ALL TESTS PASSED! Your system is ready for cannabis app deployment.

🚀 Next steps:
   1. Add your real API keys to .env file
   2. Run: python fix_everything.py
   3. Your 3 cannabis apps will be automatically deployed

💤 After 72 hours awake, automated success is finally here!
        """)
        return True
    else:
        print("""
⚠️  Some tests failed. Please fix the issues above before deploying.

💡 Common fixes:
   - Install missing Python packages: pip install requests python-dotenv
   - Check internet connection
   - Verify API keys in .env file
   
📧 Need help? Contact zakibaydoun@msn.com
        """)
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)