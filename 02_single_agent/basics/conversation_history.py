"""
Conversation History
====================

Checks API health, then asks an agent what it can recall from its memory.
Shows how conversation state carries across loops within a single completion.

Run:
    python conversation_history.py

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


def run_health_check():
    """Check if the API is healthy"""
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    return response.json()


def run_single_agent():
    """Run a single agent with the new AgentCompletion format"""
    payload = {
        "agent_config": {
            "agent_name": "Research Analyst",
            "description": "An expert in analyzing and synthesizing research data",
            "system_prompt": (
                "You are a Research Analyst with expertise in data analysis and synthesis. "
                "Your role is to analyze provided information, identify key insights, "
                "and present findings in a clear, structured format. "
                "Focus on accuracy, clarity, and actionable recommendations."
            ),
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": "auto",
            "max_tokens": 8192,
            "temperature": 1,
            "auto_generate_prompt": False,
        },
        "task": "What do you see in your memory?",
    }

    response = requests.post(
        f"{BASE_URL}/v1/agent/completions", headers=headers, json=payload, timeout=1000
    )
    return response.json()


if __name__ == "__main__":
    # Check API health
    health = run_health_check()
    print("API Health Check:")
    print(json.dumps(health, indent=4))

    # Run single agent
    agent_result = run_single_agent()
    print(json.dumps(agent_result, indent=4))
