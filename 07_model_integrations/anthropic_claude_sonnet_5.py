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
        "agent_name": "Technical Editor",
        "description": "Rewrites engineering prose for clarity without changing its meaning.",
        "system_prompt": (
            "You are a technical editor. You cut hedging, redundancy, and filler while "
            "preserving every technical claim exactly as written. You do not add new "
            "claims, soften accurate ones, or reorder an argument unless the original "
            "order obscures it. Return the edited text, then a short list of what you "
            "changed and why."
        ),
        "model_name": "anthropic/claude-sonnet-5",
        "max_loops": 1,
        "max_tokens": 8192,
        "reasoning_effort": "low",
        "temperature": 0.3,
    },
    "task": (
        "Edit this: 'It should be noted that in most cases the cache layer will "
        "generally tend to improve performance quite significantly, although there may "
        "potentially be some situations where this might not necessarily be the case.'"
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
