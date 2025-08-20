#!/bin/bash
# 🌿 Cannabis Apps - One-Command Deployment
# Author: Zaki Baydoun (zakibaydoun@msn.com)
# Usage: ./deploy.sh

echo "🌿============================================================================🌿"
echo "                        CANNABIS DEPLOYMENT SYSTEM                              "
echo "                      One Command - Three Apps - Zero Stress                   "
echo "🌿============================================================================🌿"
echo ""
echo "👤 Pharmacist: Zaki Baydoun"  
echo "📧 Contact: zakibaydoun@msn.com"
echo "⏰ After 72 hours awake, you deserve automation!"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    echo "   Please install Python 3.11+ and try again"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Environment file not found"
    echo "📋 Creating .env from template..."
    cp .env.template .env
    echo ""
    echo "🔧 Please edit .env file with your API keys:"
    echo "   - LANGSMITH_API_KEY=your_key_here"
    echo "   - GITHUB_TOKEN=your_token_here" 
    echo "   - OPENAI_API_KEY=your_key_here"
    echo "   - STREAMLIT_SHARING_EMAIL=zakibaydoun@msn.com"
    echo ""
    echo "💡 Then run: ./deploy.sh again"
    exit 0
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if required variables are set
if [ -z "$LANGSMITH_API_KEY" ] || [ -z "$GITHUB_TOKEN" ] || [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Missing required API keys in .env file"
    echo "   Please check your .env file and add all required keys"
    exit 1
fi

echo "✅ Environment variables loaded"
echo "🚀 Starting cannabis app deployment..."
echo ""

# Run the main deployment script
python3 fix_everything.py

# Check the exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo "📊 Checking app status..."
    echo ""
    python3 check_status.py
    echo ""
    echo "🌿 Your cannabis applications are ready!"
    echo "💤 Now get some sleep - you've earned it after 72 hours!"
else
    echo "❌ Deployment failed - check the logs above"
    echo "📧 Contact zakibaydoun@msn.com for support"
    exit 1
fi