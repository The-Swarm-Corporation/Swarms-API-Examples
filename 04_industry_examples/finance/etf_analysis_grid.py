"""
ETF Analysis Grid
=================

Runs a grid of ETF analysts (risk, performance, allocation) across several
ETFs at once using the batched grid workflow, driven asynchronously.

Run:
    python etf_analysis_grid.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import asyncio
import os
from typing import Any, Dict

import httpx
from dotenv import load_dotenv

load_dotenv()


def create_workflow_payload() -> Dict[str, Any]:
    """Create the batched grid workflow payload with risk and quant agents."""
    return {
        "name": "ETF Analysis Grid",
        "description": "Risk and quantitative analysis of energy and semiconductor ETFs",
        "agent_completions": [
            {
                "agent_name": "Risk Analyst",
                "description": "Focuses on risk assessment and portfolio risk metrics",
                "system_prompt": "You are a risk analyst specializing in ETF analysis. Evaluate ETFs based on volatility, downside risk, correlation, concentration risk, and risk-adjusted returns. Provide detailed risk metrics including Sharpe ratio, maximum drawdown, beta, and Value at Risk (VaR).",
                "model_name": "gpt-4.1",
                "max_loops": 1,
                "temperature": 0.3,
            },
            {
                "agent_name": "Quantitative Analyst",
                "description": "Focuses on quantitative metrics and performance analysis",
                "system_prompt": "You are a quantitative analyst specializing in ETF analysis. Evaluate ETFs based on performance metrics, expense ratios, tracking error, liquidity, holdings composition, and quantitative factors. Provide detailed analysis of returns, Sharpe ratio, information ratio, and factor exposures.",
                "model_name": "gpt-4.1",
                "max_loops": 1,
                "temperature": 0.3,
            },
        ],
        "tasks": [
            "Analyze the top energy ETFs including XLE, VDE, and IYE. Provide detailed risk and performance metrics, holdings analysis, and investment considerations.",
            "Analyze the top semiconductor ETFs including SMH, SOXX, and XSD. Provide detailed risk and performance metrics, holdings analysis, and investment considerations.",
        ],
        "max_loops": 1,
    }


async def make_api_request(
    payload: Dict[str, Any],
) -> httpx.Response:
    """Make API request to Swarms batched grid workflow endpoint."""
    url = "https://api.swarms.world/v1/batched-grid-workflow/completions"
    headers = {
        "x-api-key": os.getenv("SWARMS_API_KEY"),
        "Content-Type": "application/json",
    }
    async with httpx.AsyncClient(timeout=300.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        return response


def parse_and_display_responses(response_data: Dict[str, Any]) -> None:
    """Parse and display only the agent responses."""
    outputs = response_data.get("outputs", [])

    if not outputs:
        return

    for task_outputs in outputs:
        if isinstance(task_outputs, dict):
            for role, agent_response in task_outputs.items():
                print(f"\n--- {role} ---\n{agent_response}")


if __name__ == "__main__":
    response = asyncio.run(make_api_request(create_workflow_payload()))

    response_data = response.json()
    parse_and_display_responses(response_data)
