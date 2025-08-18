# Green Hill Cockpit

FastAPI backend with LangGraph agents and Streamlit dashboard.

## Runbook

### Local install
```bash
pip install -r requirements.txt
pip install -e .
```

### Backend
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

### Streamlit
```bash
BACKEND_BASE_URL=http://localhost:8080 streamlit run streamlit_app.py --server.port 8501
```

To use the existing LangGraph service immediately (no build wait):
```bash
BACKEND_BASE_URL=https://digitalroots-bf3899aefd705f6789c2466e0c9b974d.us.langgraph.app \
  streamlit run streamlit_app.py --server.headless true --server.port 8501
```

### Smoke tests
```bash
curl http://localhost:8080/health
curl http://localhost:8080/version
curl http://localhost:8080/graphs
curl -X POST http://localhost:8080/agents/ceo-dt/invoke -H "Content-Type: application/json" -d '{"input":{"query":"Ping"}}'
```

## LangGraph Cloud

Configuration for LangGraph Cloud lives in `langgraph.json`.
