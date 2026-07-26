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
        "agent_name": "Long Document Analyst",
        "description": "Reads long source material and extracts the parts that answer a specific question.",
        "system_prompt": (
            "You read long documents and answer questions against them. Quote the "
            "passages your answer rests on, and say plainly when the document does not "
            "contain the answer rather than inferring one. Never fill a gap in the "
            "source with general knowledge without labelling it as such."
        ),
        "model_name": "gemini/gemini-2.5-pro",
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.2,
    },
    # In practice you would paste a long document into `task` — a contract, a
    # transcript, a stack of logs — and ask a narrow question against it.
    "task": (
        "Summarize the tradeoffs between fixed-window, sliding-window, and token-bucket "
        "rate limiting, and say which one an API gateway should default to."
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
