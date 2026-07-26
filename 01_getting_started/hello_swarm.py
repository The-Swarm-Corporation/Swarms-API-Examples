"""
Hello, Swarm
============

The smallest useful multi-agent request: three agents chained together with
`SequentialWorkflow`, so each one receives the previous agent's output.

A swarm request adds three things to the single-agent shape:

  agents      - the list of agents, in the order they should run
  swarm_type  - how they are orchestrated (see 03_multi_agent/ for the others)
  task        - the goal handed to the first agent

Run:
    python hello_swarm.py

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
    "name": "Research Briefing Swarm",
    "description": "Researches a topic, analyzes the findings, and writes a brief",
    "swarm_type": "SequentialWorkflow",
    "max_loops": 1,
    "agents": [
        {
            "agent_name": "Researcher",
            "description": "Gathers the relevant facts",
            "system_prompt": (
                "You are a researcher. Gather the facts that matter for the given "
                "topic. List them plainly. Do not editorialize."
            ),
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.3,
        },
        {
            "agent_name": "Analyst",
            "description": "Turns raw facts into insight",
            "system_prompt": (
                "You are an analyst. Take the research you are given and identify "
                "the patterns, tradeoffs, and implications a decision-maker needs."
            ),
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
        {
            "agent_name": "Writer",
            "description": "Writes the final brief",
            "system_prompt": (
                "You are a writer. Turn the analysis you are given into a short "
                "executive brief: a one-line summary, three key points, and a "
                "recommendation."
            ),
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.5,
        },
    ],
    "task": "How is retrieval-augmented generation being used in enterprise search today?",
}

response = requests.post(
    f"{BASE_URL}/v1/swarm/completions",
    headers=headers,
    json=payload,
    timeout=900,
)
response.raise_for_status()

print(json.dumps(response.json(), indent=4))
