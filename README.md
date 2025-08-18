# Green Hill Cockpit

FastAPI backend with LangGraph agents and Streamlit dashboard.

## Setup

```bash
pip install -r requirements.txt
pip install -e .
```

## Run

### Backend
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8080
```

### Streamlit
```bash
BACKEND_BASE_URL=http://localhost:8080 streamlit run streamlit_app.py --server.port 8501
```

## Smoke Test
```bash
curl http://localhost:8080/health
curl http://localhost:8080/graphs
curl -X POST http://localhost:8080/agents/ceo-dt/invoke -H "Content-Type: application/json" -d '{"input":{"query":"Ping"}}'
```

## LangGraph Cloud

Configuration for LangGraph Cloud lives in `langgraph.json`.
