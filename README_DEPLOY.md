# Green Hill Cockpit Deployment Guide

## Backend Deployment (LangGraph)

Set these environment variables in your LangGraph deployment:


## Frontend Deployment (Streamlit Cloud)

In Streamlit Cloud, add these secrets:


## Testing

```bash
# Health check
curl -X GET $LANGGRAPH_API_URL/health

# Test CEO-DT agent
curl -X POST $LANGGRAPH_API_URL/agents/ghc_dt/invoke \
  -H "Authorization: Bearer $LANGGRAPH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is our strategic focus?","state":{}}'
eof

## Step 4: Create .env.example

```bash
cat > .env.example << 'EOF'
# LangGraph API Configuration
LANGGRAPH_API_URL=https://your-deployment.langgraph.app
LANGGRAPH_API_KEY=your-api-key-here

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# Optional CEO-DT Configuration
GHC_DT_MODEL=gpt-4o-mini
GHC_DT_TEMPERATURE=0.2
GHC_DT_EVIDENCE_LOG=evidence.jsonl

# Demo mode (true/false)
DEMO_MODE=false
