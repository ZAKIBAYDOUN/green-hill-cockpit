#!/bin/bash

# Start the LangGraph server
echo "Starting Green Hill LangGraph server..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Start the FastAPI server
python server.py