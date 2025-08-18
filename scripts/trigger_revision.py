#!/usr/bin/env python3
"""Create a new LangGraph Cloud revision and run runtime smoke tests.

This script relies entirely on environment variables. Required variables:
- LANGSMITH_API_KEY: control plane API key
- DEPLOYMENT_ID: deployment identifier
- LG_RUNTIME_URL: public runtime URL
Optional variables:
- CONTROL_PLANE_HOST (default https://api.host.langchain.com)
- LANGGRAPH_API_KEY: runtime bearer token
- REPO_REF: branch or tag to build from (default main)
- LANGGRAPH_CONFIG_PATH: path to config (default langgraph.json)
"""

import json
import os
import sys
import time
from typing import Any, Dict

import httpx

CONTROL_PLANE_HOST = os.getenv("CONTROL_PLANE_HOST", "https://api.host.langchain.com")
API_KEY = os.getenv("LANGSMITH_API_KEY")
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")
RUNTIME_URL = os.getenv("LG_RUNTIME_URL")
RUNTIME_TOKEN = os.getenv("LANGGRAPH_API_KEY", "")
REPO_REF = os.getenv("REPO_REF", "main")
CONFIG_PATH = os.getenv("LANGGRAPH_CONFIG_PATH", "langgraph.json")

REQUIRED = {"LANGSMITH_API_KEY": API_KEY, "DEPLOYMENT_ID": DEPLOYMENT_ID, "LG_RUNTIME_URL": RUNTIME_URL}
missing = [k for k, v in REQUIRED.items() if not v]
if missing:
    print(f"MISSING_ENV_VARS: {', '.join(missing)}")
    sys.exit(1)

cp_headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}
client = httpx.Client(base_url=CONTROL_PLANE_HOST, headers=cp_headers, timeout=30.0)


def request_with_retry(method: str, url: str, *, client: httpx.Client, json: Dict[str, Any] | None = None, headers: Dict[str, str] | None = None) -> httpx.Response:
    for attempt in range(3):
        resp = client.request(method, url, json=json, headers=headers)
        if resp.status_code >= 500 and attempt < 2:
            time.sleep(2)
            continue
        return resp
    return resp


# Step 1: trigger new revision
patch_body = {
    "source_config": {"build_on_push": True},
    "source_revision_config": {
        "repo_ref": REPO_REF,
        "langgraph_config_path": CONFIG_PATH,
    },
}
print("Triggering new revision...")
resp = request_with_retry("PATCH", f"/deployments/{DEPLOYMENT_ID}", client=client, json=patch_body)
if resp.status_code // 100 != 2:
    print(f"DEPLOYMENT_PATCH_FAILED: {resp.status_code} {resp.text}")
    sys.exit(1)

# Step 2: get latest revision id
resp = request_with_retry("GET", f"/deployments/{DEPLOYMENT_ID}/revisions", client=client)
try:
    data = resp.json()
    rev_id = data["data"][0]["id"]
except Exception:
    print(f"REVISION_LIST_FAILED: {resp.text}")
    sys.exit(1)
print(f"Revision id: {rev_id}")

# Step 3: poll status
for i in range(120):
    resp = request_with_retry("GET", f"/deployments/{DEPLOYMENT_ID}/revisions/{rev_id}", client=client)
    try:
        status = resp.json()["status"]
    except Exception:
        print(f"REVISION_STATUS_ERROR: {resp.text}")
        sys.exit(1)
    print(f"Status: {status}    ", end="\r", flush=True)
    if status == "DEPLOYED":
        print()
        break
    if status in {"FAILED", "CANCELED"}:
        log_resp = request_with_retry("GET", f"/deployments/{DEPLOYMENT_ID}/revisions/{rev_id}/logs?tail=50", client=client)
        print("BUILD_FAILED")
        print(log_resp.text)
        sys.exit(1)
    time.sleep(10)
else:
    print("BUILD_TIMEOUT")
    sys.exit(1)

# Step 4: runtime smokes
runtime_headers = {"Content-Type": "application/json"}
if RUNTIME_TOKEN:
    runtime_headers["Authorization"] = f"Bearer {RUNTIME_TOKEN}"
rt_client = httpx.Client(timeout=30.0)

def rt_request(method: str, path: str, *, json: Dict[str, Any] | None = None) -> httpx.Response:
    url = RUNTIME_URL.rstrip("/") + path
    return request_with_retry(method, url, client=rt_client, json=json, headers=runtime_headers)

print("Runtime smoke: /health")
resp = rt_request("GET", "/health")
if resp.status_code != 200:
    print(f"RUNTIME_SMOKE_FAILED: /health {resp.status_code} {resp.text}")
    sys.exit(1)

print("Runtime smoke: /graphs")
resp = rt_request("GET", "/graphs")
if resp.status_code != 200:
    print(f"RUNTIME_SMOKE_FAILED: /graphs {resp.status_code} {resp.text}")
    sys.exit(1)

print("Runtime smoke: invoke ceo-dt")
invoke_body = {"input": {"query": "Ping from automated revision"}}
resp = rt_request("POST", "/agents/ceo-dt/invoke", json=invoke_body)
if resp.status_code != 200:
    print(f"RUNTIME_SMOKE_FAILED: invoke {resp.status_code} {resp.text}")
    sys.exit(1)
try:
    invoke_preview = json.dumps(resp.json())[:200]
except Exception:
    invoke_preview = resp.text[:200]

summary = {
    "revision": rev_id,
    "status": "DEPLOYED",
    "runtime": RUNTIME_URL,
    "invoke_preview": invoke_preview,
}
print(json.dumps(summary))
