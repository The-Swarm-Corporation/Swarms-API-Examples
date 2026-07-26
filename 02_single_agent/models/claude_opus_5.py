"""
Claude Opus 5 Agent (SDK)
=========================

Runs an agent on `anthropic/claude-opus-5` through the `swarms_client` SDK,
including the `reasoning_effort` control that frontier reasoning models accept.

Run:
    python claude_opus_5.py

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
    timeout=3000,
)

result = client.agent.run(
    agent_config={
        "agent_name": "ETF Research Analyst",
        "description": "An expert in Exchange-Traded Funds (ETFs), specializing in researching, analyzing, and providing insights on ETF products, performance metrics, sector allocations, and investment strategies.",
        "system_prompt": (
            "You are an experienced ETF research analyst, skilled at investigating and explaining Exchange-Traded Funds. "
            "You review ETF holdings, analyze sectors and regions, examine expense ratios, track record, and major differences between ETFs. "
            "You help investors compare funds, understand the rationale behind ETF creation, assess suitability for portfolio goals, and highlight industry trends. "
            "Always provide data-driven insights, cite reputable sources when possible, and explain complexities in a clear, practical manner. "
            "Your name is ETF Research Analyst."
        ),
        "model_name": "anthropic/claude-opus-5",
        "max_loops": 1,
        "reasoning_effort": "low",
        "max_tokens": 16_000,
        "temperature": 0.0,
        "top_p": 0.0,
    },
    task="What is an ETF, and how does it differ from a mutual fund?",
)

print(json.dumps(result, indent=4))
