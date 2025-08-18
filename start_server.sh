#!/bin/bash

# Start the Green Hill Cockpit backend
echo "Starting Green Hill Cockpit server..."

# Load environment variables if present
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Run with uvicorn. If this script is not executable, use:
#   python -m uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}
python -m uvicorn server:app --host 0.0.0.0 --port "${PORT:-8080}"
