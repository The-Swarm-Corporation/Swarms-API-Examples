"""
Simple Advanced Research
========================

A minimal advanced-research request — one question in, a researched answer out.

Run:
    python simple_advanced_research.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def simple_advanced_research():
    """
    Simple requests call to the Advanced Research endpoint
    """

    # API configuration
    api_url = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
    api_key = os.getenv("SWARMS_API_KEY")

    # Request payload
    payload = {
        "config": {
            "name": "Simple Research",
            "description": "Simple Research",
            "worker_model_name": "gpt-4.1",
            "director_agent_name": "Director-Agent",
            "director_model_name": "gpt-4.1",
            "director_max_tokens": 8000,
            "max_loops": 1,
        },
        "task": "What are the main benefits of using AI in healthcare? Only use 2 queries.",
    }

    # Headers
    headers = {"Content-Type": "application/json", "x-api-key": api_key}

    try:
        response = requests.post(
            f"{api_url}/v1/advanced-research/completions",
            json=payload,
            headers=headers,
            timeout=500.0,  # 5 minute timeout
        )

        print(json.dumps(response.json(), indent=4))

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    result = simple_advanced_research()
    print(result)
