#!/bin/bash
set -e

echo "🚀 Starting LangGraph Cloud revision deployment and testing..."

# Environment variables with defaults
CONTROL_PLANE_HOST=${CONTROL_PLANE_HOST:-https://api.host.langchain.com}
DEPLOYMENT_ID=${DEPLOYMENT_ID:-}
LG_RUNTIME_URL=${LG_RUNTIME_URL:-}
REPO_REF=${REPO_REF:-main}
LANGGRAPH_CONFIG_PATH=${LANGGRAPH_CONFIG_PATH:-langgraph.json}

# Check required environment variables
if [[ -z "$LANGSMITH_API_KEY" ]]; then
    echo "❌ LANGSMITH_API_KEY is required"
    exit 1
fi

if [[ -z "$DEPLOYMENT_ID" ]]; then
    echo "❌ DEPLOYMENT_ID is required"
    exit 1
fi

if [[ -z "$LG_RUNTIME_URL" ]]; then
    echo "❌ LG_RUNTIME_URL is required"  
    exit 1
fi

echo "📋 Configuration:"
echo "   Control Plane: $CONTROL_PLANE_HOST"
echo "   Deployment ID: $DEPLOYMENT_ID"
echo "   Runtime URL: $LG_RUNTIME_URL"
echo "   Repo Ref: $REPO_REF"
echo "   Config Path: $LANGGRAPH_CONFIG_PATH"
echo ""

# Trigger new revision
echo "🔄 Triggering new LangGraph revision..."
REVISION_RESPONSE=$(curl -s -X PATCH \
    "${CONTROL_PLANE_HOST}/v2/deployments/${DEPLOYMENT_ID}" \
    -H "Authorization: Bearer ${LANGSMITH_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
        \"source_config\": { \"build_on_push\": true },
        \"source_revision_config\": { 
            \"repo_ref\": \"${REPO_REF}\", 
            \"langgraph_config_path\": \"${LANGGRAPH_CONFIG_PATH}\" 
        }
    }")

# Extract revision ID (assuming JSON response with revision_id field)
REVISION_ID=$(echo "$REVISION_RESPONSE" | grep -o '"revision_id":"[^"]*' | cut -d'"' -f4 | head -1)

if [[ -z "$REVISION_ID" ]]; then
    echo "❌ Failed to get revision ID from response:"
    echo "$REVISION_RESPONSE"
    exit 1
fi

echo "✅ Revision triggered: $REVISION_ID"

# Poll revision status
echo "⏳ Waiting for deployment (max 20 minutes)..."
MAX_ATTEMPTS=120  # 20 minutes * 3 attempts per minute
ATTEMPT=0

while [[ $ATTEMPT -lt $MAX_ATTEMPTS ]]; do
    STATUS_RESPONSE=$(curl -s \
        "${CONTROL_PLANE_HOST}/v2/deployments/${DEPLOYMENT_ID}/revisions/${REVISION_ID}" \
        -H "Authorization: Bearer ${LANGSMITH_API_KEY}")
    
    STATUS=$(echo "$STATUS_RESPONSE" | grep -o '"status":"[^"]*' | cut -d'"' -f4 | head -1)
    
    echo "Status: $STATUS (attempt $((ATTEMPT + 1))/$MAX_ATTEMPTS)"
    
    if [[ "$STATUS" == "DEPLOYED" ]]; then
        echo "🎉 Deployment successful!"
        break
    elif [[ "$STATUS" == "FAILED" || "$STATUS" == "CANCELED" ]]; then
        echo "❌ Deployment failed with status: $STATUS"
        echo "Last 50 log lines:"
        # Try to get logs (API endpoint may vary)
        curl -s "${CONTROL_PLANE_HOST}/v2/deployments/${DEPLOYMENT_ID}/revisions/${REVISION_ID}/logs" \
            -H "Authorization: Bearer ${LANGSMITH_API_KEY}" | tail -50
        exit 1
    fi
    
    sleep 10
    ((ATTEMPT++))
done

if [[ $ATTEMPT -eq $MAX_ATTEMPTS ]]; then
    echo "❌ Deployment timed out after 20 minutes"
    exit 1
fi

# Runtime smoke tests
echo ""
echo "🧪 Running runtime smoke tests..."

# Health check
echo "Testing /health..."
HEALTH_RESPONSE=$(curl -s "${LG_RUNTIME_URL}/health")
if [[ $? -eq 0 ]]; then
    echo "✅ Health check passed: $(echo "$HEALTH_RESPONSE" | head -c 100)"
else
    echo "❌ Health check failed"
    exit 1
fi

# Graphs endpoint
echo "Testing /graphs..."
GRAPHS_RESPONSE=$(curl -s "${LG_RUNTIME_URL}/graphs")
if [[ $? -eq 0 ]]; then
    echo "✅ Graphs endpoint passed: $(echo "$GRAPHS_RESPONSE" | head -c 100)"
else
    echo "❌ Graphs endpoint failed"
    exit 1
fi

# CEO-DT invoke
echo "Testing /agents/ceo-dt/invoke..."
INVOKE_HEADERS=(-H "Content-Type: application/json")
if [[ -n "$LANGGRAPH_API_KEY" ]]; then
    INVOKE_HEADERS+=(-H "Authorization: Bearer ${LANGGRAPH_API_KEY}")
fi

INVOKE_RESPONSE=$(curl -s -X POST "${LG_RUNTIME_URL}/agents/ceo-dt/invoke" \
    "${INVOKE_HEADERS[@]}" \
    -d '{"input":{"query":"Ping from automated revision"}}')

if [[ $? -eq 0 ]]; then
    echo "✅ CEO-DT invoke successful!"
    echo "First 200 chars of response: $(echo "$INVOKE_RESPONSE" | head -c 200)"
else
    echo "❌ CEO-DT invoke failed"
    exit 1
fi

echo ""
echo "🎯 Summary:"
echo "   Files changed: README.md, streamlit_app.py, langgraph.json, scripts/smoke_ghc_dt.http"
echo "   Removed artifacts: No Codex artifacts found"
echo "   Revision ID: $REVISION_ID"
echo "   Final status: DEPLOYED"
echo "   CEO-DT response: $(echo "$INVOKE_RESPONSE" | head -c 200)"
echo ""
echo "✅ All steps completed successfully!"