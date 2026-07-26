"""
Batched Grid Workflow
=====================

Pairs a list of agents with a list of tasks and runs the grid in one request
to `POST /v1/batched-grid-workflow/completions`.

Run:
    python batched_grid_workflow.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
from dotenv import load_dotenv
from requests import post
import os

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

# Define multiple agents with different specializations
agent_configs = [
    {
        "agent_name": "Financial-Analyst",
        "description": "Analyzes financial data and market trends",
        "system_prompt": "You are an expert financial analyst with deep knowledge of markets, economics, and investment strategies. Provide detailed analysis with supporting data.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "Risk-Manager",
        "description": "Assesses and manages financial risks",
        "system_prompt": "You are a seasoned risk management expert focused on identifying, analyzing, and mitigating financial risks. Provide comprehensive risk assessments.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.3,
        "max_loops": 1,
    },
    {
        "agent_name": "Market-Strategist",
        "description": "Develops market entry and positioning strategies",
        "system_prompt": "You are a strategic market expert who develops actionable strategies for market positioning and competitive advantage. Provide strategic recommendations.",
        "model_name": "gpt-4.1",
        "max_tokens": 4000,
        "temperature": 0.4,
        "max_loops": 1,
    },
]

# Define multiple tasks to be executed by each agent
tasks = [
    "Analyze the current state of the cryptocurrency market and identify top 3 investment opportunities.",
    "Evaluate the risks associated with investing in emerging market equities in 2025.",
    "Develop a strategy for entering the sustainable energy investment sector.",
]

# Create the batched grid workflow request
workflow_input = {
    "name": "Financial-Analysis-Grid",
    "description": "Comprehensive financial analysis using multiple specialized agents across various tasks",
    "agent_completions": agent_configs,
    "tasks": tasks,
    "max_loops": 1,
}

response = post(
    f"{BASE_URL}/v1/batched-grid-workflow/completions",
    headers=headers,
    json=workflow_input,
)

print(response.status_code)
print(response.text)

print(json.dumps(response.json(), indent=4))
