"""
Multi-Layer Graph Workflow
==========================

A deeper graph with several dependent layers, showing how output flows through
multiple stages before reaching the end points.

Complex multi-layer workflow example demonstrating advanced GraphWorkflow
capabilities with multiple layers and parallel processing.

This example shows a three-layer workflow:
1. Data collection layer (multiple collectors)
2. Analysis layer (multiple analysts)
3. Validation and synthesis layer

Run:
    python multi_layer_graph.py

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

# Define agents for different stages
agents = [
    # Layer 1: Data Collectors
    {
        "agent_name": "DataCollector1",
        "description": "Collects data from source 1",
        "system_prompt": "You are a data collector. Gather comprehensive data from your assigned source.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "DataCollector2",
        "description": "Collects data from source 2",
        "system_prompt": "You are a data collector. Gather comprehensive data from your assigned source.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "DataCollector3",
        "description": "Collects data from source 3",
        "system_prompt": "You are a data collector. Gather comprehensive data from your assigned source.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    # Layer 2: Analysts
    {
        "agent_name": "Analyst1",
        "description": "Performs analysis on collected data",
        "system_prompt": "You are an analyst. Analyze the provided data and extract key insights.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "Analyst2",
        "description": "Performs analysis on collected data",
        "system_prompt": "You are an analyst. Analyze the provided data and extract key insights.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "Analyst3",
        "description": "Performs analysis on collected data",
        "system_prompt": "You are an analyst. Analyze the provided data and extract key insights.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    # Layer 3: Validators
    {
        "agent_name": "Validator1",
        "description": "Validates analysis results",
        "system_prompt": "You are a validator. Review and validate the provided analysis for accuracy and completeness.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.2,
        "max_loops": 1,
    },
    {
        "agent_name": "Validator2",
        "description": "Validates analysis results",
        "system_prompt": "You are a validator. Review and validate the provided analysis for accuracy and completeness.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.2,
        "max_loops": 1,
    },
    # Final Layer: Synthesis
    {
        "agent_name": "SynthesisAgent",
        "description": "Synthesizes all validated results",
        "system_prompt": "You are a synthesis expert. Combine all validated analyses into a comprehensive final report.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
]

# Define edges creating a complex multi-layer structure
# Layer 1 -> Layer 2: All collectors feed all analysts (parallel chain)
# Layer 2 -> Layer 3: All analysts feed validators
# Layer 3 -> Final: All validators feed synthesis agent
edges = [
    # Layer 1 -> Layer 2: Parallel chain pattern
    {"source": "DataCollector1", "target": "Analyst1"},
    {"source": "DataCollector1", "target": "Analyst2"},
    {"source": "DataCollector1", "target": "Analyst3"},
    {"source": "DataCollector2", "target": "Analyst1"},
    {"source": "DataCollector2", "target": "Analyst2"},
    {"source": "DataCollector2", "target": "Analyst3"},
    {"source": "DataCollector3", "target": "Analyst1"},
    {"source": "DataCollector3", "target": "Analyst2"},
    {"source": "DataCollector3", "target": "Analyst3"},
    # Layer 2 -> Layer 3: Analysts feed validators
    {"source": "Analyst1", "target": "Validator1"},
    {"source": "Analyst2", "target": "Validator1"},
    {"source": "Analyst3", "target": "Validator1"},
    {"source": "Analyst1", "target": "Validator2"},
    {"source": "Analyst2", "target": "Validator2"},
    {"source": "Analyst3", "target": "Validator2"},
    # Layer 3 -> Final: Validators feed synthesis
    {"source": "Validator1", "target": "SynthesisAgent"},
    {"source": "Validator2", "target": "SynthesisAgent"},
]

# Create the graph workflow request
workflow_input = {
    "name": "Complex-Multi-Layer-Workflow",
    "description": "Complex multi-layer workflow with data collection, analysis, validation, and synthesis",
    "agents": agents,
    "edges": edges,
    "entry_points": ["DataCollector1", "DataCollector2", "DataCollector3"],
    "end_points": ["SynthesisAgent"],
    "max_loops": 1,
    "task": "Conduct comprehensive research on renewable energy markets including data collection, multi-perspective analysis, validation, and final synthesis",
    "auto_compile": True,
    "verbose": True,
}

print("Sending complex multi-layer GraphWorkflow request...")
print(f"Workflow: {workflow_input['name']}")
print(f"Task: {workflow_input['task']}")
print(f"Total agents: {len(agents)}")
print(f"Total edges: {len(edges)}")
print(f"Entry points: {workflow_input['entry_points']}")
print(f"End points: {workflow_input['end_points']}\n")

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
    print("\nFinal synthesis output:")
    outputs = result.get("outputs", {})
    if "SynthesisAgent" in outputs:
        print(f"  {outputs['SynthesisAgent']}")
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
