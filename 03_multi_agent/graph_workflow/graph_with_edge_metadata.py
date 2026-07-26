"""
Graph Edges With Metadata
=========================

Attaches metadata to edges so downstream agents receive labelled context about
where their input came from.

Example demonstrating GraphWorkflow with custom metadata on edges.

This example shows how to add metadata to edges for additional
context and configuration.

Run:
    python graph_with_edge_metadata.py

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

# Define agents with specific roles
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
    {
        "agent_name": "ReportGenerator",
        "description": "Generates final reports",
        "system_prompt": "You are a report generation expert. Create comprehensive, well-structured reports.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
]

# Define edges with custom metadata
edges = [
    {
        "source": "ResearchAgent",
        "target": "AnalysisAgent",
        "metadata": {
            "data_type": "research_findings",
            "priority": "high",
            "timeout": 300,
            "retry_on_failure": True,
        },
    },
    {
        "source": "AnalysisAgent",
        "target": "ReportGenerator",
        "metadata": {
            "data_type": "analysis_results",
            "priority": "high",
            "format": "structured",
        },
    },
]

# Create the graph workflow request
workflow_input = {
    "name": "Metadata-Workflow",
    "description": "Workflow demonstrating metadata usage on edges",
    "agents": agents,
    "edges": edges,
    "entry_points": ["ResearchAgent"],
    "end_points": ["ReportGenerator"],
    "max_loops": 1,
    "task": "Research and analyze the impact of climate change on agriculture, then generate a comprehensive report",
    "auto_compile": True,
    "verbose": False,
}

print("Sending GraphWorkflow request with metadata...")
print(f"Workflow: {workflow_input['name']}")
print(f"Task: {workflow_input['task']}")
print(f"Edges with metadata: {len(edges)}\n")

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
    for agent_name in ["ResearchAgent", "AnalysisAgent", "ReportGenerator"]:
        if agent_name in outputs:
            output_preview = str(outputs[agent_name])[:150]
            print(f"  {agent_name}: {output_preview}...")
    print("\nUsage:")
    usage = result.get("usage", {})
    print(f"  Input tokens: {usage.get('input_tokens', 0)}")
    print(f"  Output tokens: {usage.get('output_tokens', 0)}")
    print(f"  Total tokens: {usage.get('total_tokens', 0)}")
    print(f"  Token cost: ${usage.get('token_cost', 0):.4f}")
    print(f"  Cost per agent: ${usage.get('cost_per_agent', 0):.4f}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
