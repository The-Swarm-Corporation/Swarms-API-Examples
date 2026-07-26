"""
Hierarchical Swarm
==================

A coordinator agent plans the work and delegates to worker agents, then
synthesizes their output. Set `role` to `coordinator` or `worker` on each agent.

Hierarchical Swarm Example - Market Research Analysis

Demonstrates a HiearchicalSwarm with a coordinator directing specialized workers
to conduct comprehensive market research analysis.

Run:
    python hierarchical_swarm.py

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
    "name": "Market Research Hierarchical Swarm",
    "description": "A hierarchical swarm for comprehensive market research analysis",
    "swarm_type": "HierarchicalSwarm",
    "task": """
    Conduct a comprehensive market research analysis for a new electric vehicle (EV) 
    charging station network targeting urban areas in the United States.
    
    Please analyze:
    1. Current market landscape and major competitors
    2. Consumer preferences and adoption barriers
    3. Financial viability and investment requirements
    4. Strategic recommendations for market entry
    """,
    "max_loops": 1,
    "agents": [
        {
            "agent_name": "Market Research Director",
            "description": "Senior director who coordinates the research team and synthesizes findings",
            "system_prompt": """You are a seasoned Market Research Director with 20 years of experience.

Your role is to:
1. Coordinate the research efforts of your team of specialists
2. Synthesize findings from market analysts, consumer insights specialists, and financial analysts
3. Identify key strategic implications and opportunities
4. Provide actionable recommendations for business decisions

Structure your response with Executive Summary, Key Findings, Strategic Implications, and Recommended Actions.""",
            "model_name": "gpt-4.1",
            "role": "coordinator",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.3,
        },
        {
            "agent_name": "Market Analyst",
            "description": "Specialist in market trends and competitive landscape",
            "system_prompt": """You are an expert Market Analyst specializing in competitive intelligence.

Your responsibilities include:
1. Analyzing current market trends and their trajectories
2. Mapping the competitive landscape and key players
3. Identifying market opportunities and threats
4. Evaluating market size, growth rates, and segmentation

Provide detailed, data-driven analysis with specific examples.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
        {
            "agent_name": "Consumer Insights Specialist",
            "description": "Expert in consumer behavior and preferences",
            "system_prompt": """You are a Consumer Insights Specialist with expertise in customer behavior.

Your focus areas include:
1. Consumer behavior patterns and purchasing decisions
2. Demographic and psychographic segmentation
3. Customer needs, pain points, and unmet demands
4. Brand perception and loyalty factors

Provide insights that connect consumer understanding to business opportunities.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
        {
            "agent_name": "Financial Analyst",
            "description": "Specialist in financial modeling and ROI analysis",
            "system_prompt": """You are a Financial Analyst specializing in market economics.

Your expertise covers:
1. Financial modeling and ROI projections
2. Cost-benefit analysis of market opportunities
3. Pricing strategy evaluation
4. Investment requirements and resource allocation

Provide quantitative analysis to support strategic decisions.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.3,
        },
    ],
}

response = requests.post(
    f"{BASE_URL}/v1/swarm/completions",
    headers=headers,
    json=payload,
    timeout=300,
)

print(json.dumps(response.json(), indent=2))
