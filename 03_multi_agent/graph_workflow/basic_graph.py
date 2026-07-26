"""
Basic Graph Workflow
====================

Two agents wired as a directed graph: researcher -> analyzer. Introduces
`entry_points`, `end_points` and `edges`.

Basic example demonstrating how to use the GraphWorkflow endpoint
with a simple sequential workflow.

This example shows a basic two-agent workflow where one agent
performs research and another performs analysis.

Run:
    python basic_graph.py

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

# Define agents for the workflow
agents = [
    {
        "agent_name": "ResearchAgent",
        "description": "Conducts research on given topics",
        "system_prompt": "You are an expert researcher. Conduct thorough research and provide comprehensive findings.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "AnalysisAgent",
        "description": "Analyzes research findings and provides insights",
        "system_prompt": "You are an expert analyst. Analyze the provided research and extract key insights.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
]

# Define edges - sequential flow: ResearchAgent -> AnalysisAgent
edges = [
    {
        "source": "ResearchAgent",
        "target": "AnalysisAgent",
    }
]

# Create the graph workflow request
workflow_input = {
    "name": "Research-Analysis-Workflow",
    "description": "A simple sequential workflow for research and analysis",
    "agents": agents,
    "edges": edges,
    "entry_points": ["ResearchAgent"],
    "end_points": ["AnalysisAgent"],
    "max_loops": 1,
    "task": "What are the latest trends in AI development?",
    "auto_compile": True,
    "verbose": False,
}

response = post(
    f"{BASE_URL}/v1/graph-workflow/completions",
    headers=headers,
    json=workflow_input,
    timeout=300,
)

print(response.json())
