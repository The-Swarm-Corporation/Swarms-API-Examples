"""
Hello, Agent (SDK)
==================

The same single-agent request as `hello_agent.py`, but through the official
Python SDK instead of raw HTTP. The SDK handles auth headers, retries, and
response parsing for you.

    pip install swarms-client

Run:
    python hello_agent_sdk.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

from dotenv import load_dotenv
from swarms_client import SwarmsClient

load_dotenv()

client = SwarmsClient(
    api_key=os.getenv("SWARMS_API_KEY"),
    base_url=os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world"),
    timeout=300,
)

result = client.agent.run(
    agent_config={
        "agent_name": "Research Analyst",
        "description": "Analyzes information and reports the key takeaways",
        "system_prompt": (
            "You are a research analyst. Read the question, identify what actually "
            "matters, and answer in clear, structured prose. Be concrete and skip "
            "filler."
        ),
        "model_name": "gpt-4.1",
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.5,
    },
    task="What are the main tradeoffs between vector search and keyword search?",
)

print(json.dumps(result, indent=4))
