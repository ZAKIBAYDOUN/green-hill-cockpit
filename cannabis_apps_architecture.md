# 🌿 Cannabis Apps Architecture

## App Deployments & Dependencies

### 🎮 Ground Control
- **Type**: Standalone Monitoring App
- **LangSmith**: ❌ NOT REQUIRED
- **Mode**: Autonomous (no external API calls)
- **Status**: ✅ Always Online
- **Purpose**: Monitor and control other apps

### 🌿 Green Hill Cockpit  
- **Type**: Executive AI Assistant
- **LangSmith**: ✅ REQUIRED
- **Deployment**: `cockpit-c5fbf013b8495301890e442307c38955`
- **Status**: ⚠️ 403 (needs API fix)
- **Purpose**: CEO Digital Twin & Multi-agent system

### 🌱 Digital Roots
- **Type**: Cultivation Management AI
- **LangSmith**: ✅ REQUIRED  
- **Deployment**: `digitalroots-bf3899aefd705f6789c2466e0c9b974d`
- **Status**: ⚠️ Needs configuration
- **Purpose**: Cannabis cultivation intelligence

## Why Ground Control Works Without LangSmith

Ground Control is your **command center** that:
- Monitors the OTHER apps
- Doesn't need AI capabilities itself
- Runs simple Python/Streamlit code
- That's why it's always online!

## To Fix The Other Apps

1. **Green Hill Cockpit**: Need to fix LangSmith deployment permissions
2. **Digital Roots**: Already configured, waiting for Streamlit to update

