import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

payload = {
    "agent_config": {
        "agent_name": "Systems Design Reviewer",
        "description": "Reviews proposed system designs for correctness, failure modes, and cost.",
        "system_prompt": (
            "You are a staff engineer reviewing system designs. For any design you are "
            "given, identify the failure modes first, then the scaling limits, then the "
            "operational cost. Be concrete: name the component, the condition that breaks "
            "it, and the consequence. Do not restate the design back to the reader."
        ),
        "model_name": "openai/gpt-5",
        "max_loops": 1,
        "max_tokens": 8192,
        "reasoning_effort": "medium",
        "dynamic_temperature_enabled": False,
    },
    "task": (
        "We want to serve 50k requests/second of vector search over 2 billion embeddings "
        "with p99 under 100ms. Sketch the architecture and tell me where it breaks."
    ),
}

response = requests.post(
    f"{BASE_URL}/v1/agent/completions",
    headers=headers,
    json=payload,
    timeout=1000,
)
response.raise_for_status()

print(json.dumps(response.json(), indent=4))
