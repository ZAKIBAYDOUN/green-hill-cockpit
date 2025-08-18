# Green Hill Cockpit

Green Hill Executive Cockpit with LangGraph-powered agents including GHC-DT (CEO Digital Twin).

## Architecture

- **LangGraph Backend**: FastAPI server running LangGraph agents
- **Streamlit Frontend**: Executive cockpit interface
- **Agents**:
  - GHC-DT (CEO Digital Twin): Executive-focused agent using LangChain & OpenAI
  - Green Hill Agents: Strategy, Finance, Operations, Market, Risk, Compliance, Innovation

## Quick Start

### Environment Setup

1. Copy environment template:
```bash
cp .env.example .env
```

2. Configure required environment variables in `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here

# GHC-DT Configuration
GHC_DT_MODEL=gpt-4o-mini
GHC_DT_TEMPERATURE=0.2
GHC_DT_SYSTEM_PROMPT=You are GHC-DT, the CEO Digital Twin of Green Hill Canarias...
GHC_DT_EVIDENCE_LOG=evidence.jsonl
```

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the LangGraph server:
```bash
./start_server.sh
# OR manually:
python server.py
```

3. In another terminal, start Streamlit:
```bash
streamlit run streamlit_app.py
```

### Cloud Deployment

#### LangGraph Service
Deploy to your cloud provider using the `langgraph.json` configuration.

#### Streamlit Cloud
1. Connect your repository to Streamlit Cloud
2. Configure secrets:
   - `OPENAI_API_KEY`
   - `LANGGRAPH_API_URL` (your deployed LangGraph service URL)
   - `LANGGRAPH_API_KEY` (if authentication is enabled)

## API Endpoints

- `GET /health` - Health check
- `POST /agents/ghc_dt/invoke` - GHC-DT (CEO Digital Twin)
- `POST /agents/green_hill/invoke` - Green Hill specialists
- `POST /invoke` - Generic endpoint with agent routing

## Testing

Use the smoke test file:
```bash
# Install a REST client like httpie or use VS Code REST Client
# Open scripts/smoke_ghc_dt.http in VS Code and run the requests
```

## Agents

### GHC-DT (CEO Digital Twin)
Executive-focused agent providing:
- Strategic summaries
- Key points identification  
- Next action recommendations
- Executive decision support

### Green Hill Specialists
Domain experts in:
- **Strategy**: EU-GMP compliance, market expansion
- **Finance**: CAPEX, ROI projections
- **Operations**: Production planning, facility management
- **Market**: European cannabis opportunities
- **Risk**: Regulatory and operational risks
- **Compliance**: AEMPS, EU-GMP requirements
- **Innovation**: R&D, technology advancement