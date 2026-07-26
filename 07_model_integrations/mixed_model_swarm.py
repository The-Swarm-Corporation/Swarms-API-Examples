import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}

# Each agent carries its own model_name, so a swarm can spend frontier tokens
# only where the work is hard and cheap tokens everywhere else.
payload = {
    "name": "Mixed Model Research Swarm",
    "description": "Gathers, analyzes, and writes up a topic using a different model per step",
    "swarm_type": "SequentialWorkflow",
    "max_loops": 1,
    "agents": [
        {
            # Bulk reading and extraction — fast and cheap is enough.
            "agent_name": "Researcher",
            "description": "Gathers the relevant facts",
            "system_prompt": (
                "You are a researcher. List the facts that matter for the given topic, "
                "one per line, with no commentary and no conclusions."
            ),
            "model_name": "groq/llama-3.3-70b-versatile",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.2,
        },
        {
            # The hard step: this is where a wrong answer propagates.
            "agent_name": "Analyst",
            "description": "Turns raw facts into insight",
            "system_prompt": (
                "You are an analyst. Take the facts you are given and identify the "
                "patterns, tradeoffs, and second-order effects a decision-maker needs. "
                "Flag any fact you think is wrong or missing context."
            ),
            "model_name": "anthropic/claude-opus-5",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "reasoning_effort": "high",
            "temperature": 0.3,
        },
        {
            # Writing quality matters, but the reasoning is already done.
            "agent_name": "Writer",
            "description": "Writes the final brief",
            "system_prompt": (
                "You are a writer. Turn the analysis you are given into an executive "
                "brief: a one-line summary, three key points, and a recommendation. "
                "Add nothing the analysis does not support."
            ),
            "model_name": "anthropic/claude-sonnet-5",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.5,
        },
    ],
    "task": "How are enterprises actually deploying open-weight models in production today?",
}

response = requests.post(
    f"{BASE_URL}/v1/swarm/completions",
    headers=headers,
    json=payload,
    timeout=1000,
)
response.raise_for_status()

print(json.dumps(response.json(), indent=4))
