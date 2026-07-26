import json
import os

from dotenv import load_dotenv
from swarms_client import SwarmsClient

load_dotenv()

client = SwarmsClient(
    api_key=os.getenv("SWARMS_API_KEY"),
    base_url=os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world"),
    timeout=3000,
)

result = client.agent.run(
    agent_config={
        "agent_name": "Quantitative Strategist",
        "description": "Designs and stress-tests systematic trading strategies.",
        "system_prompt": (
            "You are a quantitative strategist. You reason from first principles about "
            "market structure, transaction costs, and capacity constraints. When you "
            "propose a strategy, you state the hypothesis, the mechanism that would make "
            "it profitable, the conditions under which it stops working, and the cost "
            "assumptions the returns depend on. You never present backtest intuition as "
            "an established result."
        ),
        "model_name": "anthropic/claude-opus-5",
        "max_loops": 1,
        "max_tokens": 16_000,
        "reasoning_effort": "high",
        "temperature": 0.2,
    },
    task=(
        "A cross-sectional momentum strategy on US equities decays sharply after 2015. "
        "Give me the three most likely structural explanations and how I would "
        "distinguish between them."
    ),
)

print(json.dumps(result, indent=4))
