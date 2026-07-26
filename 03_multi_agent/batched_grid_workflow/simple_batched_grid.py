"""
Simple Batched Grid
===================

A two-agent, two-task grid — the smallest useful version of the pattern.

Simple Batched Grid Workflow Example

This is a minimal example demonstrating the batched grid workflow endpoint.
It runs 2 agents on 2 tasks, creating 4 total executions.

Run:
    python simple_batched_grid.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os

from dotenv import load_dotenv
from requests import post

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

# Simple workflow with 2 agents and 2 tasks
workflow_input = {
    "name": "Simple-Research-Grid",
    "description": "Basic research workflow with two agents",
    "agent_completions": [
        {
            "agent_name": "Researcher-1",
            "system_prompt": "You are a research assistant focused on providing concise, factual information.",
            "model_name": "gpt-4.1",
            "max_tokens": 2000,
            "temperature": 0.5,
        },
        {
            "agent_name": "Researcher-2",
            "system_prompt": "You are a research assistant focused on providing detailed analysis.",
            "model_name": "gpt-4.1",
            "max_tokens": 2000,
            "temperature": 0.5,
        },
    ],
    "tasks": [
        "What are the key benefits of using multi-agent systems?",
        "Explain how AI agents can work together collaboratively.",
    ],
    "max_loops": 1,
    "imgs": [],
}

print("Running simple batched grid workflow...")
print("Total executions: 2 agents × 2 tasks = 4 executions\n")

response = post(
    f"{BASE_URL}/v1/batched-grid-workflow/completions",
    headers=headers,
    json=workflow_input,
    timeout=120,
)

if response.status_code == 200:
    result = response.json()
    print(result)
else:
    print(f"Error: {response.status_code}")
    print(response.text)
