FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration and requirements first for better layer caching
COPY langgraph.json .
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python source files
COPY *.py .
COPY agents/ ./agents/
COPY scripts/ ./scripts/

# Create environment file placeholder
RUN touch .env

# Set default environment variables for cloud deployment
ENV MODE=cloud
ENV PORT=8080
ENV PYTHONPATH=/app

# Expose the LangGraph standard port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Run the server
CMD ["python", "server.py"]
