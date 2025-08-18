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

## Environment variables

### Local development
| Variable | Description |
| --- | --- |
| `LANGGRAPH_BASE_URL` | Optional LangGraph Cloud endpoint for proxy mode |
| `LANGGRAPH_API_KEY` | API key when proxying to LangGraph Cloud |
| `OPENAI_API_KEY` | OpenAI key for GPT-5/GPT-4o access |
| `MODEL_NAME` | Override default model selection |
| `BACKEND_BASE_URL` | Backend URL for the Streamlit client |
| `DEFAULT_LANGUAGE` | Default UI language code |
| `ALLOWED_LANGUAGES` | Comma list of allowed language codes |
| `CORS_ALLOW_ORIGINS` | Comma list of allowed origins for CORS |

### Streamlit Cloud secrets
| Variable | Value |
| --- | --- |
| `BACKEND_BASE_URL` | `https://<your-service-url>` |
| `DEFAULT_LANGUAGE` | `en` |
| `ALLOWED_LANGUAGES` | `en,is,fr,es` |

### LangGraph Cloud variables
| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | Your OpenAI key |
| `MODEL_NAME` | Preferred model name (e.g., `gpt-5`) |
| `LANGGRAPH_BASE_URL` | Upstream LangGraph service URL when proxying |
| `LANGGRAPH_API_KEY` | Service key for proxying |
| `CORS_ALLOW_ORIGINS` | Allowed origins, e.g., `https://*.streamlit.app` |

## LangGraph Cloud

Configuration for LangGraph Cloud lives in `langgraph.json`.
