"""
List Swarm Types
================

Prints the swarm types the API accepts (`SequentialWorkflow`,
`ConcurrentWorkflow`, `HierarchicalSwarm`, `HeavySwarm`, ...) and, optionally,
the models available to them.

Run:
    python list_swarm_types.py

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


def get_swarm_types():
    """Return the swarm types this account can use."""
    response = requests.get(f"{BASE_URL}/v1/swarms/available", headers=headers)
    response.raise_for_status()
    return response.json()


def get_models():
    """Return the models this account can route to."""
    response = requests.get(f"{BASE_URL}/v1/models/available", headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("Available swarm types:")
    print(json.dumps(get_swarm_types(), indent=4))

    # Uncomment to also list every available model:
    # print("\nAvailable models:")
    # print(json.dumps(get_models(), indent=4))
