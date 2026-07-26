"""
Simple Hierarchical Swarm
=========================

The smallest hierarchical swarm worth running: one coordinator, two workers.

Simple Hierarchical Swarm Example

A minimal example demonstrating the HiearchicalSwarm type with a coordinator
and two worker agents.

Run:
    python simple_hierarchical.py

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
    "name": "Simple Hierarchical Swarm",
    "description": "A basic hierarchical swarm with coordinator and workers",
    "swarm_type": "HiearchicalSwarm",
    "task": "Analyze the pros and cons of remote work for software engineering teams",
    "max_loops": 1,
    "agents": [
        {
            "agent_name": "Team Lead",
            "description": "Coordinates analysis and provides recommendations",
            "system_prompt": "You are a team lead who synthesizes input from specialists to provide balanced recommendations.",
            "model_name": "gpt-4.1",
            "role": "coordinator",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.3,
        },
        {
            "agent_name": "Productivity Analyst",
            "description": "Analyzes productivity implications",
            "system_prompt": "You are a productivity analyst who evaluates work efficiency and output quality.",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 2048,
            "temperature": 0.4,
        },
        {
            "agent_name": "Culture Specialist",
            "description": "Analyzes team culture and collaboration",
            "system_prompt": "You are a culture specialist who evaluates team dynamics and collaboration patterns.",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 2048,
            "temperature": 0.4,
        },
    ],
}

response = requests.post(
    f"{BASE_URL}/v1/swarm/completions",
    headers=headers,
    json=payload,
    timeout=300,
)

print(json.dumps(response.json(), indent=2))
