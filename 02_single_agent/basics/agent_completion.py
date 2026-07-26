"""
Single Agent Completion
=======================

Runs one agent against `POST /v1/agent/completions` with a full `agent_config`.
This is the reference example for every field an agent accepts: model, system
prompt, loop count, token ceiling, temperature and dynamic temperature.

Run:
    python agent_completion.py

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
            "model_name": "gpt-5.4",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 1,
            "auto_generate_prompt": False,
            "dynamic_temperature_enabled": True,
        },
        "task": "What are the best ways to find samples of diabetes from blood samples?",
    }

    response = requests.post(
        f"{BASE_URL}/v1/agent/completions", headers=headers, json=payload, timeout=1000
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    agent_result = run_single_agent()
    print(json.dumps(agent_result, indent=4))
