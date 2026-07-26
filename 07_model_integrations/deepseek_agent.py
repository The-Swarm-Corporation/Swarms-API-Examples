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
        "agent_name": "Algorithm Verifier",
        "description": "Checks algorithms for correctness and complexity before they are implemented.",
        "system_prompt": (
            "You verify algorithms. For any algorithm you are given, state whether it is "
            "correct, give a counterexample if it is not, and derive its time and space "
            "complexity with the reasoning shown. Treat 'it looks right' as insufficient."
        ),
        "model_name": "deepseek/deepseek-reasoner",
        "max_loops": 1,
        "max_tokens": 8192,
        "reasoning_effort": "high",
        "temperature": 0.0,
    },
    "task": (
        "To find the k-th smallest element in two sorted arrays, I binary search on the "
        "value range and count elements less than the midpoint. Is that correct, and "
        "what is its complexity?"
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
