"""
Fetch Swarm Logs
================

Pulls the execution log of your past swarm runs — the fastest way to debug a
run after the fact.

Run:
    python fetch_swarm_logs.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
# Standard headers for all requests
headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def get_tools():
    response = requests.get(f"{BASE_URL}/v1/tools/available", headers=headers)
    return response.json()


def get_logs():
    response = requests.get(f"{BASE_URL}/v1/swarm/logs", headers=headers)

    logs = response.json()

    return logs


print(get_logs())
# print(get_tools())
