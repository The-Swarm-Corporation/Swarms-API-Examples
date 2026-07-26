"""
Supply Chain Swarm
==================

Hierarchical supply-chain analysis covering sourcing, logistics and risk.

Hierarchical Swarm Example - Supply Chain Analysis

Demonstrates a HiearchicalSwarm for comprehensive supply chain analysis
with a director coordinating logistics, inventory, and procurement specialists.

Run:
    python supply_chain_swarm.py

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
    "name": "Supply Chain Hierarchical Swarm",
    "description": "A hierarchical swarm for comprehensive supply chain analysis",
    "swarm_type": "HiearchicalSwarm",
    "task": """
    Analyze the current supply chain challenges facing the semiconductor industry 
    and provide optimization recommendations for a mid-sized electronics manufacturer.
    
    Consider:
    1. Current supply chain bottlenecks and disruptions
    2. Inventory management strategies during shortages
    3. Supplier diversification opportunities
    4. Long-term resilience improvements
    """,
    "max_loops": 1,
    "agents": [
        {
            "agent_name": "Supply Chain Director",
            "description": "Oversees the overall supply chain analysis and optimization strategy",
            "system_prompt": """You are a Supply Chain Director with extensive experience in global supply chain management.

Your role is to:
1. Coordinate analysis across logistics, inventory, and procurement functions
2. Identify bottlenecks and inefficiencies in the supply chain
3. Develop optimization strategies for cost reduction and efficiency
4. Ensure supply chain resilience and risk mitigation

Synthesize inputs from your team into actionable strategic recommendations.""",
            "model_name": "gpt-4.1",
            "role": "coordinator",
            "max_loops": 1,
            "max_tokens": 8192,
            "temperature": 0.3,
        },
        {
            "agent_name": "Logistics Specialist",
            "description": "Expert in transportation and distribution optimization",
            "system_prompt": """You are a Logistics Specialist focused on transportation and distribution efficiency.

Your expertise includes:
1. Transportation mode optimization and route planning
2. Distribution network design and efficiency
3. Last-mile delivery solutions
4. Freight cost analysis and optimization

Provide detailed analysis of logistics operations with improvement recommendations.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
        {
            "agent_name": "Inventory Manager",
            "description": "Specialist in inventory management and demand forecasting",
            "system_prompt": """You are an Inventory Management expert specializing in stock optimization.

Your focus areas include:
1. Demand forecasting and planning
2. Inventory optimization and safety stock calculation
3. Warehouse management and space utilization
4. Inventory carrying cost reduction

Provide data-driven recommendations for inventory efficiency improvements.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
        },
        {
            "agent_name": "Procurement Analyst",
            "description": "Expert in supplier management and strategic sourcing",
            "system_prompt": """You are a Procurement Analyst with expertise in strategic sourcing.

Your responsibilities include:
1. Supplier evaluation and relationship management
2. Sourcing strategy and vendor diversification
3. Cost negotiation and contract optimization
4. Supplier risk assessment and mitigation

Provide analysis that balances cost efficiency with supply reliability.""",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
            "max_tokens": 4096,
            "temperature": 0.4,
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
