"""
Check Rate Limits
=================

Reads your current rate limits and remaining quota from `GET /v1/rate/limits`.

Run:
    python check_rate_limits.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

from typing import Dict, Any
import os
import requests
from dotenv import load_dotenv
import traceback
import json

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",  # Enable gzip compression
}


def test_ratelimits() -> Dict[str, Any]:
    """Test ratelimits"""
    try:
        response = requests.get(f"{BASE_URL}/v1/rate/limits", headers=headers)
        return response.json()
    except Exception as e:
        return f"Error: {e} Traceback: {traceback.format_exc()}"


print(json.dumps(test_ratelimits(), indent=4))
