# Green Hill Cockpit

FastAPI backend with Streamlit frontend for experimenting with LangGraph agents.

## Setup

```bash
pip install -r requirements.txt
```

## Running

Start the backend:

```bash
bash start_server.sh
# if the script is not executable:
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

## Smoke tests

Use the `smoke_ghc_dt.http` file with an HTTP client or `curl` to verify:

- `GET /health`
- `GET /version`
- `GET /graphs`
- `POST /agents/ghc_dt/invoke`

Example invocation:

```bash
curl -X POST http://localhost:8000/agents/ghc_dt/invoke \
  -H 'Content-Type: application/json' \
  -d '{"input": {"question": "hello"}}'
```
