"""
Auto-Generate Agents Locally
============================

The same idea using the local `swarms` package (`AgentsBuilder`) rather than
the hosted API. Requires `pip install swarms`.

Run:
    python auto_generate_agents_local.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

from swarms.structs.agent_builder import AgentsBuilder
from dotenv import load_dotenv

load_dotenv()

swarm = AgentsBuilder()

print(
    swarm.run(
        task="Create a comprehensive market analysis report for AI companies, including financial metrics, growth potential, and competitive analysis."
    )
)
