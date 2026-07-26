"""
Reasoning Agent Types
=====================

Lists the reasoning agent types the API supports via
`GET /v1/reasoning-agent/types`, then runs one (`reasoning-duo`) against
`POST /v1/reasoning-agent/completions`.

Run:
    python reasoning_agent_types.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os
import traceback
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
# Add gzip compression support to headers
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    # "Accept-Encoding": "gzip, deflate, br",  # Enable gzip compression
}


def get_reasoning_agent_types():
    """
    Example demonstrating how to use the reasoning agent API with different reasoning types.
    """

    try:
        response = requests.get(
            f"{BASE_URL}/v1/reasoning-agent/types",
            headers=headers,
        )

        print(response.status_code)
        print(response.text)
        return response.json()
        # print(response.json())
    except Exception as e:
        print(f"❌ Exception: {str(e)} Traceback: {traceback.format_exc()}")


def run_reasoning_agent_example():
    """
    Example demonstrating how to use the reasoning agent API with different reasoning types.
    """
    basic_reasoning_payload = {
        "agent_name": "math-reasoner",
        "description": "A reasoning agent specialized in mathematical problem solving",
        "model_name": "claude-sonnet-4-20250514",
        "system_prompt": """You are an expert mathematical reasoning agent. 
        When solving problems, always show your step-by-step reasoning process.
        Break down complex problems into smaller, manageable steps.
        Verify your solutions and explain your logic clearly.""",
        "max_loops": 1,
        "swarm_type": "reasoning-duo",
        "num_samples": 1,
        "task": "If a train travels 120 miles in 2 hours, and then travels 180 miles in 3 hours, what is the average speed for the entire journey? Show your reasoning step by step.",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/reasoning-agent/completions",
            headers=headers,
            json=basic_reasoning_payload,
        )

        result = response.json()

        print(response.status_code)
        print(response.text)

        return result
    except Exception as e:
        print(f"❌ Exception: {str(e)} Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    # print(json.dumps(get_reasoning_agent_types(), indent=4))
    out = run_reasoning_agent_example()
    print(json.dumps(out, indent=4))
