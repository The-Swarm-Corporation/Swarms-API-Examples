"""
Stream an Agent Response
========================

Sets `stream: true` and prints server-sent events as they arrive, so tokens
appear in real time instead of after the full response is generated.

Stream a single-agent completion from the local Swarms API and print tokens
in real time as they arrive.

Run the API first:
    uvicorn api.main:app --reload --port 8080

Then run this script:
    python agent_streaming_example.py

Run:
    python stream_agent_response.py

Requires SWARMS_API_KEY in your environment or a .env file.
"""

import json
import os
import sys
from typing import Union

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SWARMS_API_KEY")
BASE_URL = os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


def run_agent_streaming(task: str, max_loops: Union[int, str] = 3) -> str:
    """POST to /v1/agent/completions with streaming and print tokens live.

    Tokens flow through `event: chunk` frames as the LLM produces them, across
    every loop. Tool calls and inter-loop bookkeeping produce silent gaps —
    that's expected. Pass `max_loops="auto"` to let the agent decide when to
    stop.
    """
    payload = {
        "task": task,
        "agent_config": {
            "agent_name": "Iterative Research Writer",
            "description": "Drafts and refines its output across multiple loops.",
            "system_prompt": (
                "You are a senior research writer. On each loop, critique your "
                "previous draft and produce a tighter, sharper version. Always "
                "return the latest full draft."
            ),
            "model_name": "claude-sonnet-4-20250514",
            "role": "worker",
            "max_loops": max_loops,
            "max_tokens": 2048,
            "temperature": 0.3,
            "streaming_on": True,
            "dynamic_temperature_enabled": False,
            "top_p": None,
        },
    }

    print(f"POST {BASE_URL}/v1/agent/completions  (max_loops={max_loops!r})")
    print(f"Task: {task}")
    print("=" * 80)

    response = requests.post(
        f"{BASE_URL}/v1/agent/completions",
        headers=headers,
        json=payload,
        stream=True,
        timeout=600,
    )

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return ""

    full_output = ""
    current_event = None

    for raw in response.iter_lines():
        if not raw:
            continue
        line = raw.decode("utf-8")

        if line.startswith("event: "):
            current_event = line[7:]
            continue

        if not line.startswith("data: "):
            continue

        try:
            data = json.loads(line[6:])
        except json.JSONDecodeError:
            continue

        # First frame after connect is metadata, sent without an event tag.
        if current_event is None and data.get("type") == "metadata":
            print(f"job_id: {data.get('job_id')}")
            print(f"agent:  {data.get('name')}")
            print("-" * 80)
            continue

        if current_event == "start":
            print(f"[start] {data.get('message')}\n")

        elif current_event == "chunk":
            token = data.get("content", "")
            full_output += token
            sys.stdout.write(token)
            sys.stdout.flush()

        elif current_event == "usage":
            print("\n" + "-" * 80)
            print(
                f"usage: in={data.get('input_tokens')} "
                f"out={data.get('output_tokens')} "
                f"total={data.get('total_tokens')}"
            )
            billing = data.get("billing_info") or {}
            if billing:
                print(f"cost:  ${billing.get('total_cost')}")

        elif current_event == "end":
            print(f"[end] job_id={data.get('job_id')}")

        elif current_event == "done":
            print(f"[done] {data.get('message')}")

        elif current_event == "error":
            print(f"\n[error] {data.get('error')}")

    print("=" * 80)
    return full_output


if __name__ == "__main__":
    task = (
        "Draft, then iteratively refine, a one-paragraph executive summary "
        "of the current state of agentic AI in financial research. On each "
        "loop, tighten the prose and sharpen the claims."
    )

    # Fixed-loop streaming
    run_agent_streaming(task, max_loops=3)

    # Autonomous streaming — uncomment to try max_loops="auto"
    # run_agent_streaming(
    #     "Use your tools to compute 17 + 25, then state the result.",
    #     max_loops="auto",
    # )
