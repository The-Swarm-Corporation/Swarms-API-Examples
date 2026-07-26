"""
Agent Handoffs
==============

Gives a primary agent a list of `handoffs` — specialist agents it can delegate
to mid-task. The primary agent decides when to call them; you only send one
request.

Run:
    python agent_handoffs.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def run_agent_with_handoffs():
    """Run an agent with handoff agents using the AgentCompletion format"""
    payload = {
        "agent_config": {
            "agent_name": "Portfolio-Risk-Analyzer",
            "description": "Analyzes portfolio diversification and concentration risk",
            "system_prompt": (
                "You are a portfolio risk analyst. Focus on:\n"
                "- Portfolio diversification analysis\n"
                "- Concentration risk assessment\n"
                "- Correlation analysis\n"
                "- Sector/asset allocation risk\n"
                "- Liquidity risk evaluation\n\n"
                "Provide actionable insights for risk reduction. "
                "You can hand off tasks to specialized risk agents when needed."
            ),
            "model_name": "gpt-4o-mini",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.5,
            "dynamic_temperature_enabled": True,
            "handoffs": [
                {
                    "agent_name": "Risk-Metrics-Calculator",
                    "description": "Calculates key risk metrics like VaR, Sharpe ratio, and volatility",
                    "system_prompt": (
                        "You are a risk metrics specialist. Calculate and explain:\n"
                        "- Value at Risk (VaR)\n"
                        "- Sharpe ratio\n"
                        "- Volatility\n"
                        "- Maximum drawdown\n"
                        "- Beta coefficient\n\n"
                        "Provide clear, numerical results with brief explanations."
                    ),
                    "model_name": "gpt-4o-mini",
                    "max_loops": 1,
                    "dynamic_temperature_enabled": True,
                },
                {
                    "agent_name": "Market-Risk-Monitor",
                    "description": "Monitors market conditions and identifies risk factors",
                    "system_prompt": (
                        "You are a market risk monitor. Identify and assess:\n"
                        "- Market volatility trends\n"
                        "- Economic risk factors\n"
                        "- Geopolitical risks\n"
                        "- Interest rate risks\n"
                        "- Currency risks\n\n"
                        "Provide current risk alerts and trends."
                    ),
                    "model_name": "gpt-4o-mini",
                    "max_loops": 1,
                    "dynamic_temperature_enabled": True,
                },
            ],
        },
        "task": "Call the Market-Risk-Monitor agent to get the current market risk factors.",
    }

    print("Sending request with handoff agents...")
    print(f"Main agent: {payload['agent_config']['agent_name']}")
    print(
        f"Handoff agents: {[h['agent_name'] for h in payload['agent_config']['handoffs']]}"
    )
    print()

    response = requests.post(
        f"{BASE_URL}/v1/agent/completions",
        headers=headers,
        json=payload,
        timeout=1000,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = run_agent_with_handoffs()
    print(json.dumps(result, indent=4))
