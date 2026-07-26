# Single Agent — Streaming

Set `"stream": true` and the API returns server-sent events instead of one JSON body,
so tokens reach your user as they are produced rather than after the full response.

**Endpoint:** `POST /v1/agent/completions` with `"stream": true`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `stream` | bool | `true` switches the response to SSE |
| everything else | — | Identical to a non-streaming agent request |

Client side, the only change is `stream=True` on the request and iterating the
response instead of reading `.json()`.

## Shape

```python
payload = {
    "agent_config": {"agent_name": "Writer", "model_name": "gpt-4.1", "max_loops": 1},
    "task": "Your task here",
    "stream": True,
}

with requests.post(
    f"{BASE_URL}/v1/agent/completions", headers=headers, json=payload, stream=True
) as response:
    for line in response.iter_lines():
        if line:
            print(line.decode(), flush=True)
```

`flush=True` matters — without it Python buffers stdout and the output arrives in
chunks even though the network delivered it token by token.

## Examples

| File | What it shows |
|---|---|
| [`minimal_streaming.py`](minimal_streaming.py) | The smallest client that works — start here |
| [`stream_agent_response.py`](stream_agent_response.py) | The standard client, with event parsing |
| [`streaming_with_tools.py`](streaming_with_tools.py) | Streaming an agent that also has tools available |
| [`streaming_agent_and_swarm.py`](streaming_agent_and_swarm.py) | Both the agent and swarm endpoints, with error handling |
| [`inspect_raw_stream_events.py`](inspect_raw_stream_events.py) | Raw, unparsed SSE lines — reach for this when a stream stalls |

Streaming a whole swarm: [`../../03_multi_agent/streaming/`](../../03_multi_agent/streaming/).

## Debugging a stream

| Symptom | Usually means |
|---|---|
| Output arrives all at once | Client-side buffering — add `flush=True`, and `stream=True` on the request |
| Nothing arrives for a long time, then everything | The agent is reasoning before emitting; check `max_loops` |
| Events look wrong or unparseable | Run [`inspect_raw_stream_events.py`](inspect_raw_stream_events.py) to see the actual bytes |
