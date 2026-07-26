"""
Crypto Analysis Agent
=====================

A single agent tuned for cryptocurrency market analysis and risk-adjusted
strategy suggestions.

Run:
    python crypto_analysis_agent.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
# Debug API key loading
if not API_KEY:
    print("ERROR: SWARMS_API_KEY environment variable is not set!")
    print("Please check your .env file or set the environment variable.")
    exit(1)
else:
    print(
        f"API Key loaded: {API_KEY[:10]}..."
        if len(API_KEY) > 10
        else f"API Key loaded: {API_KEY}"
    )

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def run_health_check():
    """Check if the API is healthy"""
    response = requests.get(f"{BASE_URL}/health", headers=headers)
    return response.json()


def run_single_agent():
    """Run a single agent with the new AgentCompletion format"""
    payload = {
        "agent_config": {
            "agent_name": "Crypto Quant Analyst",
            "description": "An expert quantitative analyst specializing in cryptocurrency market analysis and trading strategies",
            "system_prompt": (
                "You are a Crypto Quant Analyst with deep expertise in quantitative analysis of cryptocurrency markets. "
                "Your role is to analyze crypto market data, identify trading patterns, calculate risk metrics, "
                "and develop data-driven trading strategies. You have access to real-time cryptocurrency data "
                "from OKX exchange through specialized tools. "
                "\n\n"
                "Key responsibilities:\n"
                "- Perform technical analysis on cryptocurrency price movements\n"
                "- Calculate volatility, correlation, and risk metrics\n"
                "- Identify market trends and trading opportunities\n"
                "- Analyze trading volumes and market liquidity\n"
                "- Provide quantitative insights for portfolio management\n"
                "- Suggest risk-adjusted trading strategies\n"
                "\n"
                "Always support your analysis with quantitative data and statistical reasoning. "
                "When analyzing cryptocurrencies, consider factors like market cap, trading volume, "
                "price volatility, correlation with other assets, and technical indicators. "
                "Use the available crypto data tools to get real-time information when needed."
            ),
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.3,  # Lower temperature for more analytical responses
            "auto_generate_prompt": False,
            # "mcp_url": 'http://0.0.0.0:8001/sse',  # Connect to OKX crypto server
        },
        "task": "Analyze Bitcoin (BTC)",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/v1/agent/completions", headers=headers, json=payload
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            print(f"Response Headers: {dict(e.response.headers)}")
            try:
                error_detail = e.response.json()
                print(f"Error Details: {json.dumps(error_detail, indent=2)}")
            except Exception as e:
                print(f"Response Text: {e.response.text}")
        return None


if __name__ == "__main__":
    # Check API health
    health = run_health_check()
    print("API Health Check:")
    print(json.dumps(health, indent=4))
    print("\n" + "=" * 50 + "\n")

    # Run single agent
    print("Running Single Agent:")
    agent_result = run_single_agent()
    if agent_result:
        print(json.dumps(agent_result, indent=4))
    print("\n" + "=" * 50 + "\n")
