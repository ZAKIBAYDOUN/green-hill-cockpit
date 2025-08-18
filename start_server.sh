#!/bin/bash
# Start the FastAPI server for Green Hill Cockpit
# If this script is not executable, run the Python command directly:
# python -m uvicorn server:app --host 0.0.0.0 --port 8000

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
