#!/bin/bash

# Prueba rápida manual para verificar que el CEO-DT está funcionando
# Reemplaza YOUR_DEPLOYMENT_URL con tu URL real de LangGraph Cloud

DEPLOYMENT_URL="https://your-deployment-url.langgraph.cloud"

echo "🧪 Probando CEO Digital Twin..."

curl -X POST "${DEPLOYMENT_URL}/assistants/ceo-dt/threads" \
  -H "Content-Type: application/json" \
  -d '{
    "config": {"configurable": {}},
    "input": {
      "messages": [
        {
          "role": "user",
          "content": "¿Cuáles son las prioridades estratégicas actuales de Green Hill?"
        }
      ]
    }
  }' \
  | jq '.'

echo "✅ Si ves una respuesta JSON con thread_id, ¡el CEO-DT está funcionando!"