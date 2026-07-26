import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

payload = {
    "agent_config": {
        "agent_name": "Support Ticket Router",
        "description": "Classifies inbound support tickets into a queue and a priority.",
        "system_prompt": (
            "You classify support tickets. Return only JSON with these keys: "
            '"queue" (one of billing, technical, account, other), '
            '"priority" (one of p0, p1, p2, p3), and "reason" (one sentence). '
            "No prose before or after the JSON."
        ),
        "model_name": "groq/llama-3.3-70b-versatile",
        "max_loops": 1,
        "max_tokens": 512,
        "temperature": 0.0,
    },
    "task": (
        "Ticket: 'Our production API has been returning 503 for the last twenty "
        "minutes and our checkout flow is down. We are on the enterprise plan.'"
    ),
}

start = time.time()
response = requests.post(
    f"{BASE_URL}/v1/agent/completions",
    headers=headers,
    json=payload,
    timeout=300,
)
response.raise_for_status()
elapsed = time.time() - start

print(json.dumps(response.json(), indent=4))
print(f"\nCompleted in {elapsed:.2f}s")
