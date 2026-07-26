"""
Hello, Agent
============

The smallest useful Swarms API request: one agent, one task, one response.

Every agent request has the same two parts:

  agent_config  - who the agent is (name, system prompt, model, limits)
  task          - what you want it to do

Run:
    python hello_agent.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

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
        "agent_name": "Research Analyst",
        "description": "Analyzes information and reports the key takeaways",
        "system_prompt": (
            "You are a research analyst. Read the question, identify what actually "
            "matters, and answer in clear, structured prose. Be concrete and skip "
            "filler."
        ),
        # Any model the API can route to. See 06_platform_utilities/list_models.py
        "model_name": "gpt-4.1",
        # One pass through the agent. Set to "auto" to let the API decide.
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.5,
    },
    "task": "What are the main tradeoffs between vector search and keyword search?",
}

response = requests.post(
    f"{BASE_URL}/v1/agent/completions",
    headers=headers,
    json=payload,
    timeout=300,
)
response.raise_for_status()

print(json.dumps(response.json(), indent=4))
