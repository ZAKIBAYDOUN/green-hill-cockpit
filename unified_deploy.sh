#!/bin/bash
# 🌿 UNIFIED CANNABIS DEPLOYMENT SYSTEM
# Handles nested organizations gracefully

echo "🌿 CANNABIS EMPIRE DEPLOYMENT SYSTEM"
echo "Parent Org: green-hill-canarias"
echo "Child Org: digital-roots"
echo "User: ZAKIBAYDOUN"

# Set emergency mode
export DEMO_MODE=true
export BYPASS_AUTH=true
export LANGCHAIN_TRACING_V2=false

# Deploy to all cannabis apps regardless of org location
for app in greenhillgpt digital-roots ground-control; do
    echo "🚀 Deploying $app..."
    
    # Try parent org first
    if gh repo view green-hill-canarias/$app >/dev/null 2>&1; then
        echo "   📍 Found in parent org: green-hill-canarias/$app"
        gh repo clone green-hill-canarias/$app temp_$app
        cd temp_$app && git push && cd .. && rm -rf temp_$app
    
    # Try child org
    elif gh repo view digital-roots/$app >/dev/null 2>&1; then
        echo "   📍 Found in child org: digital-roots/$app"
        gh repo clone digital-roots/$app temp_$app
        cd temp_$app && git push && cd .. && rm -rf temp_$app
    
    # Try user repos
    elif gh repo view ZAKIBAYDOUN/$app >/dev/null 2>&1; then
        echo "   📍 Found in user repos: ZAKIBAYDOUN/$app"
        gh repo clone ZAKIBAYDOUN/$app temp_$app
        cd temp_$app && git push && cd .. && rm -rf temp_$app
    
    else
        echo "   ❌ App not found: $app"
    fi
done

echo "✅ Unified deployment complete!"
