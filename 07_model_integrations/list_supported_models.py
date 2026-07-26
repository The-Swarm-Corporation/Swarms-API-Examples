import os
import sys
from collections import defaultdict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")

headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def fetch_models() -> list:
    """Return every model name the API will accept as `model_name`."""
    response = requests.get(
        f"{BASE_URL}/v1/models/available", headers=headers, timeout=60
    )
    response.raise_for_status()
    body = response.json()

    # The endpoint has returned a bare list and a wrapped object over time;
    # accept both rather than depending on one shape.
    if isinstance(body, dict):
        for key in ("models", "data", "available_models"):
            if key in body:
                body = body[key]
                break

    names = []
    for entry in body:
        if isinstance(entry, dict):
            names.append(entry.get("id") or entry.get("model_name"))
        else:
            names.append(entry)
    return sorted(n for n in names if n)


def group_by_provider(names: list) -> dict:
    """Bucket `provider/model` names by their prefix; unprefixed names go to 'default'."""
    groups = defaultdict(list)
    for name in names:
        provider = name.split("/")[0] if "/" in name else "(no prefix)"
        groups[provider].append(name)
    return groups


if __name__ == "__main__":
    filters = [term.lower() for term in sys.argv[1:]]

    models = fetch_models()
    if filters:
        models = [m for m in models if any(term in m.lower() for term in filters)]

    if not models:
        print("No models matched. Run without arguments to see the full list.")
        sys.exit(1)

    for provider, names in sorted(group_by_provider(models).items()):
        print(f"\n{provider}  ({len(names)})")
        for name in names:
            print(f"  {name}")

    print(f"\n{len(models)} model(s).")
