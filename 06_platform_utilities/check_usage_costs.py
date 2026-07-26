"""
Check Usage Costs
=================

Breaks down what you have spent, by request.

Run:
    python check_usage_costs.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os

from dotenv import load_dotenv
from httpx import post

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")

response = post(
    "https://api.swarms.world/v1/usage/costs", headers={"x-api-key": API_KEY}
)

print(json.dumps(response.json(), indent=4))
