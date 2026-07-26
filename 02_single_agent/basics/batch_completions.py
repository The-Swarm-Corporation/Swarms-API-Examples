"""
Batch Agent Completions
=======================

Submits several independent agent completions in one request to
`POST /v1/agent/batch/completions`. Cheaper and faster than looping over
single completions when the tasks do not depend on each other.

Run:
    python batch_completions.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import requests
from dotenv import load_dotenv
import json
from typing import List, Dict, Any

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
if not API_KEY:
    raise ValueError("SWARMS_API_KEY environment variable is required")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def run_batch_agents(payloads: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run multiple agents in batch"""
    if not payloads:
        raise ValueError("No payloads provided")

    response = requests.post(
        f"{BASE_URL}/v1/agent/batch/completions",
        headers=headers,
        json=payloads,
        timeout=300,
    )

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    return response.json()


def main():
    # Example payloads with multiple agents
    payloads = [
        {
            "agent_config": {
                "agent_name": "Research Analyst",
                "system_prompt": "You are a Research Analyst. Analyze the given information and provide insights.",
                "model_name": "gpt-4.1",
                "max_tokens": 4096,
                "temperature": 0.5,
            },
            "task": "Analyze the impact of AI on healthcare and provide key insights.",
        },
        {
            "agent_config": {
                "agent_name": "Technical Writer",
                "system_prompt": "You are a Technical Writer. Create clear, concise technical documentation.",
                "model_name": "gpt-4.1",
                "max_tokens": 6144,
                "temperature": 0.3,
            },
            "task": "Write a technical summary of machine learning algorithms used in medical diagnosis.",
        },
    ]

    try:
        print(f"Running batch with {len(payloads)} agents...")
        results = run_batch_agents(payloads)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
