"""
Check Account Credits
=====================

Reads your remaining credit balance.

Run:
    python check_account_credits.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
HEADERS = {
    "x-api-key": os.getenv("SWARMS_API_KEY"),
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
}


def test_account_credits() -> Dict[str, Any]:
    """Test the account credits endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/v1/account/credits", headers=HEADERS)
        print(response.status_code)
        print(json.dumps(response.json(), indent=4))
    except Exception as e:
        print(e)


test_account_credits()
