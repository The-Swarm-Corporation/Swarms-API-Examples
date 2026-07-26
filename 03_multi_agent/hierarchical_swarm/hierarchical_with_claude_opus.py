"""
Hierarchical Swarm on Claude Opus 4.8
=====================================

A hierarchical swarm where every agent runs on `anthropic/claude-opus-4-8`,
driven through the `swarms_client` SDK.

Run:
    python hierarchical_with_claude_opus.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

from dotenv import load_dotenv
from swarms_client import SwarmsClient

load_dotenv()

client = SwarmsClient(
    api_key=os.getenv("SWARMS_API_KEY"),
    base_url="https://api.swarms.world",
    timeout=1000,
)


result = client.swarms.run(
    name="Markets Hierarchical Swarm",
    description="Director coordinates an ETF analyst and a stocks analyst.",
    swarm_type="HierarchicalSwarm",
    task="Compare the outlook for the SPY ETF and NVDA stock for the next quarter. Highlight the strongest signal for each.",
    max_loops=1,
    agents=[
        {
            "agent_name": "ETF Analyst",
            "description": "Analyzes broad-market and sector ETFs.",
            "system_prompt": (
                "You are an ETF analyst. Given a ticker, summarize the fund's "
                "exposure, recent flows, and near-term outlook in under 200 words."
            ),
            "model_name": "anthropic/claude-opus-4-8",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
        },
        {
            "agent_name": "Stocks Analyst",
            "description": "Analyzes individual equities.",
            "system_prompt": (
                "You are an equity analyst. Given a ticker, summarize the company's "
                "fundamentals, catalysts, and near-term outlook in under 200 words."
            ),
            "model_name": "anthropic/claude-opus-4-8",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
        },
    ],
)

print(json.dumps(result, indent=4))
