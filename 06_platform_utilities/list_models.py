"""
List Available Models
=====================

Prints every model the API can route to, via the SDK.

Run:
    python list_models.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import os
from swarms_client import SwarmsClient
from dotenv import load_dotenv

load_dotenv()

client = SwarmsClient(
    api_key=os.getenv("SWARMS_API_KEY"),
)

print(client.models.list_available())
