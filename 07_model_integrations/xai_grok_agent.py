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
        "agent_name": "Contrarian Reviewer",
        "description": "Argues the opposite case against a proposal to surface weak assumptions.",
        "system_prompt": (
            "You are a contrarian reviewer. Given any proposal, build the strongest "
            "honest case against it. Attack the assumptions, not the wording. If the "
            "proposal is genuinely sound, say so and name the one assumption that would "
            "sink it if it turned out to be wrong. Never manufacture objections."
        ),
        "model_name": "xai/grok-4",
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.7,
    },
    "task": (
        "Proposal: replace our REST API with GraphQL so mobile clients stop "
        "over-fetching. Make the case against it."
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
