#!/bin/bash
# 🚨 EMERGENCY KEY ROTATION SCRIPT
# After API key compromise, run this to update all systems

echo "🚨 CANNABIS APPS - EMERGENCY KEY ROTATION"
echo "=========================================="

if [ -z "$NEW_LANGSMITH_KEY" ]; then
    echo "❌ ERROR: NEW_LANGSMITH_KEY environment variable not set"
    echo "Usage: NEW_LANGSMITH_KEY=lsv2_sk_your_new_key_here ./rotate_keys.sh"
    exit 1
fi

echo "🔄 Updating all cannabis applications with new API key..."

# Update main app
echo "📱 Updating green-hill-cockpit..."
sed -i "s/REVOKED_GENERATE_NEW_KEY/$NEW_LANGSMITH_KEY/g" /workspaces/green-hill-cockpit/.env

# Update all cannabis apps
for app in greenhillgpt digital-roots ground-control; do
    echo "📱 Updating $app..."
    if [ -d "/workspaces/$app" ]; then
        cd "/workspaces/$app"
        
        # Update secrets.toml
        sed -i "s/REVOKED_GENERATE_NEW_KEY/$NEW_LANGSMITH_KEY/g" .streamlit/secrets.toml
        
        # Commit and push changes
        git add .
        git commit -m "🔐 Security: Updated API keys after compromise"
        git push origin main
        
        echo "✅ $app updated and pushed"
    fi
done

echo "✅ ALL CANNABIS APPS UPDATED WITH NEW KEY"
echo "🔍 Run check_status.py to verify everything works"