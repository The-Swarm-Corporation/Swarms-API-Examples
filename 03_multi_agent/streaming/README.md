# Multi-Agent — Streaming

Set `"stream": true` on a swarm request and each agent's output arrives as it is
produced, instead of one payload after the whole swarm finishes.

This matters more for swarms than for single agents: a swarm can run for minutes, and
without streaming the user sees nothing until it completes.

**Endpoint:** `POST /v1/swarm/completions` with `"stream": true`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `stream` | bool | `true` switches the response to SSE |
| everything else | — | Identical to a non-streaming swarm request |

## Shape

```python
payload = {
    "name": "Streaming-Swarm",
    "swarm_type": "SequentialWorkflow",
    "agents": [...],
    "task": "Your task here",
    "stream": True,
}

with requests.post(
    f"{BASE_URL}/v1/swarm/completions", headers=headers, json=payload, stream=True
) as response:
    for line in response.iter_lines():
        if line:
            print(line.decode(), flush=True)
```

## Examples

| File | What it shows |
|---|---|
| [`stream_swarm_response.py`](stream_swarm_response.py) | Each agent's output printed as the swarm produces it |

Single-agent streaming, including a minimal client and a raw-event inspector:
[`../../02_single_agent/streaming/`](../../02_single_agent/streaming/).

## Tips

- **Events are tagged by agent.** In a multi-agent stream you need to know who is
  speaking — parse the agent identifier rather than concatenating everything.
- **Sequential swarms stream in order; concurrent swarms interleave.** Buffer per
  agent if you are rendering [`ConcurrentWorkflow`](../concurrent_workflow/) output.
- **Always `flush=True`.** Otherwise Python's stdout buffering hides the streaming you
  just implemented.
