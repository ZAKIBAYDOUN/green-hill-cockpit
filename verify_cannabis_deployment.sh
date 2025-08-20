#!/bin/bash
echo "🌿 CANNABIS APPS DEPLOYMENT VERIFICATION"
echo "========================================"

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar cada app
echo -e "\n📱 Checking Streamlit Apps..."
for url in \
    "https://green-hill-cockpit.streamlit.app" \
    "https://digital-roots-my7i9xaz3xdnj2jhcjqbj6.streamlit.app" \
    "https://ground-control.streamlit.app"
do
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|302"; then
        echo -e "${GREEN}✅ $url${NC}"
    else
        echo -e "${YELLOW}⚠️  $url (deploying...)${NC}"
    fi
done

echo -e "\n🔧 Checking LangGraph APIs..."
for api in \
    "https://cockpit-c5fbf013b8495301890e442307c38955.us.langgraph.app/health" \
    "https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app/health"
do
    if curl -s -o /dev/null -w "%{http_code}" "$api" -H "Authorization: Bearer $LANGSMITH_API_KEY" | grep -q "200"; then
        echo -e "${GREEN}✅ $api${NC}"
    else
        echo -e "${RED}❌ $api${NC}"
    fi
done

echo -e "\n📊 DEPLOYMENT STATUS:"
echo "====================="
echo "Green Hill Cockpit: Check https://green-hill-cockpit.streamlit.app"
echo "Digital Roots: Check https://digital-roots-my7i9xaz3xdnj2jhcjqbj6.streamlit.app"
echo "Ground Control: Check https://ground-control.streamlit.app"
echo ""
echo "Monitor all apps: streamlit run monitor_cannabis_apps.py"
echo ""
echo "🌿 Your cannabis technology empire awaits! 🚀"
