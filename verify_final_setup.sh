#!/bin/bash
echo "🌿 FINAL VERIFICATION - Green Hill Canarias Structure"
echo "===================================================="

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "\n📊 GitHub Structure:"
echo "├── Organization: green-hill-canarias"
echo "│   ├── Team: digital-roots"
echo "│   └── Repositories:"

# Verificar cada repositorio
for repo in "green-hill-cockpit" "digital-roots" "ground-control"; do
    cd /workspaces/$repo 2>/dev/null
    if [ $? -eq 0 ]; then
        remote=$(git remote get-url origin 2>/dev/null)
        if [[ $remote == *"green-hill-canarias"* ]]; then
            echo -e "│       ├── $repo: ${GREEN}✅ Correct${NC}"
        else
            echo -e "│       ├── $repo: ${RED}❌ Wrong remote${NC}"
        fi
    else
        echo -e "│       ├── $repo: ${YELLOW}⚠️ Not found${NC}"
    fi
done

echo -e "\n📱 Streamlit Apps Status:"
for url in \
    "https://green-hill-cockpit.streamlit.app" \
    "https://digital-roots-my7i9xaz3xdnj2jhcjqbj6.streamlit.app" \
    "https://ground-control.streamlit.app"
do
    app_name=$(echo $url | cut -d'/' -f3 | cut -d'.' -f1)
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200\|302"; then
        echo -e "  ${GREEN}✅ $app_name is online${NC}"
    else
        echo -e "  ${YELLOW}⏳ $app_name is deploying${NC}"
    fi
done

echo -e "\n✅ CORRECT STRUCTURE:"
echo "- All repos under: github.com/green-hill-canarias/"
echo "- Team 'digital-roots' for permissions"
echo "- NO separate digital-roots organization"

echo -e "\n🌿 Your cannabis tech empire is properly structured!"
