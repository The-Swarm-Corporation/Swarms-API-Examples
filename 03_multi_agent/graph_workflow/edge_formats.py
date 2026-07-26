"""
Graph Edge Formats
==================

The accepted shorthand and long-form ways of declaring edges, including
one-to-many and many-to-one declarations.

Run:
    python edge_formats.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
from dotenv import load_dotenv
from requests import post

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

# Define agents
agents = [
    {
        "agent_name": "Agent1",
        "description": "First agent in the workflow",
        "system_prompt": "You are Agent 1. Process the initial task.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "Agent2",
        "description": "Second agent in the workflow",
        "system_prompt": "You are Agent 2. Process data from Agent 1.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "Agent3",
        "description": "Third agent in the workflow",
        "system_prompt": "You are Agent 3. Process data from Agent 2.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
]

# Define edges using different formats
# Format 1: Simple dictionary with source and target
edge1 = {"source": "Agent1", "target": "Agent2"}

# Format 2: Dictionary with metadata
edge2 = {
    "source": "Agent2",
    "target": "Agent3",
    "metadata": {
        "priority": "high",
        "data_type": "processed_data",
    },
}

edges = [edge1, edge2]

# Create the graph workflow request
workflow_input = {
    "name": "Edge-Formats-Example",
    "description": "Example demonstrating different edge format options",
    "agents": agents,
    "edges": edges,
    "entry_points": ["Agent1"],
    "end_points": ["Agent3"],
    "max_loops": 1,
    "task": "Process a simple task through a three-agent pipeline",
    "auto_compile": True,
    "verbose": False,
}

print("Sending GraphWorkflow request with different edge formats...")
print(f"Workflow: {workflow_input['name']}")
print(f"Task: {workflow_input['task']}")
print("Edge formats:")
print(f"  1. Simple dict: {edge1}")
print(f"  2. Dict with metadata: {edge2}\n")

response = post(
    f"{BASE_URL}/v1/graph-workflow/completions",
    headers=headers,
    json=workflow_input,
)

if response.status_code == 200:
    result = response.json()
    print("Workflow completed successfully!")
    print(f"Job ID: {result.get('job_id')}")
    print(f"Status: {result.get('status')}")
    print("\nOutputs:")
    outputs = result.get("outputs", {})
    for agent_name in ["Agent1", "Agent2", "Agent3"]:
        if agent_name in outputs:
            output_preview = str(outputs[agent_name])[:150]
            print(f"  {agent_name}: {output_preview}...")
    print("\nUsage:")
    usage = result.get("usage", {})
    print(f"  Input tokens: {usage.get('input_tokens', 0)}")
    print(f"  Output tokens: {usage.get('output_tokens', 0)}")
    print(f"  Total tokens: {usage.get('total_tokens', 0)}")
    print(f"  Token cost: ${usage.get('token_cost', 0):.4f}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
