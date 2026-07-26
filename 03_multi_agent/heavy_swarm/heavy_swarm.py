"""
Heavy Swarm
===========

Runs the `HeavySwarm` type, which spawns a larger internal agent team for
research-grade tasks. Uses `httpx` with a long timeout — these runs take a while.

Run:
    python heavy_swarm.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
API_KEY = os.getenv("SWARMS_API_KEY")


# Headers for API requests
HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY,
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
    "Accept-Encoding": "lz4",
}


payload = {
    "name": "Market Opportunity Analysis HeavySwarm",
    "description": "A comprehensive multi-agent system for analyzing market opportunities with specialized domain experts",
    "swarm_type": "HeavySwarm",
    "max_loops": 1,
    # HeavySwarm specific configurations
    "heavy_swarm_loops_per_agent": 1,  # Number of iterations per agent
    "heavy_swarm_question_agent_model_name": "claude-sonnet-4-20250514",  # Model for question/coordination agent
    "heavy_swarm_worker_model_name": "claude-sonnet-4-20250514",  # Model for worker agents
    # Task to be analyzed
    "task": """
    Analyze the market opportunity for AI-powered customer service solutions in the healthcare industry.
    
    Please provide a comprehensive analysis covering:
    1. Market size and growth potential
    2. Key competitors and their positioning
    3. Regulatory considerations and compliance requirements
    4. Technology requirements and implementation challenges
    5. Revenue models and pricing strategies
    6. Risk assessment and mitigation strategies
    7. Go-to-market recommendations
    
    Focus on actionable insights that would help a startup make informed decisions about entering this market.
    """,
}

response = httpx.post(f"{BASE_URL}/v1/swarm/completions", headers=HEADERS, json=payload)

print(response.json())
