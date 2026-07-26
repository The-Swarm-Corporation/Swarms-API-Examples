"""
Metrics Summary
===============

Aggregate usage metrics for your account from `GET /v1/metrics/summary`.

Run:
    python metrics_summary.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
HEADERS = {"x-api-key": os.getenv("SWARMS_API_KEY")}

response = requests.get(
    f"{BASE_URL}/v1/metrics/summary",
    headers=HEADERS,
)

data = response.json()
print(json.dumps(data, indent=4))
