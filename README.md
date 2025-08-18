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

# Allow requests from Streamlit frontend
CORS_ORIGINS=http://localhost:8501

# Optional: proxy mode for LangGraph Cloud
LANGGRAPH_BASE_URL=https://your-langgraph-cloud

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

2. Start the backend server:

```bash
bash start_server.sh
# OR manually
python -m uvicorn server:app --host 0.0.0.0 --port 8000
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

- `GET /health` – health check
- `GET /version` – service version
- `GET /graphs` – list available graphs
- `POST /agents/{id}/invoke` – invoke a specific agent

## Testing

Use the smoke test file:

```bash
# With a REST client such as VS Code's REST Client extension
# Run the requests in scripts/smoke_ghc_dt.http
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