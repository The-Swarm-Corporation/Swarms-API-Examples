# HeavySwarm

`HeavySwarm` spawns a larger internal agent team than you configure, using a
question-worker pattern for computationally intensive work.

**Use it when** depth matters more than latency — hard research questions, analysis
where you want the system to expand the problem rather than answer it narrowly. Runs
take minutes.

**Endpoint:** `POST /v1/swarm/completions`

## Features

- **Advanced collaboration** — complex multi-agent interactions beyond the roster you define
- **Enhanced reasoning** — built for problems that need decomposition
- **Question-worker pattern** — specialized question and worker agent architecture
- **Heavy processing** — designed for computationally intensive workflows

## Configuration

| Field | Type | Notes |
|---|---|---|
| `swarm_type` | string | `"HeavySwarm"` |
| `agents` | array | Your seed agents; the swarm expands internally |
| `task` | string | The problem to work on |
| `max_loops` | integer | Execution loops (default `1`) |
| `name`, `description` | string | Labels for the run |

## Shape

```python
payload = {
    "name": "Heavy-Swarm",
    "swarm_type": "HeavySwarm",
    "agents": [
        {"agent_name": "Worker", "system_prompt": "...", "model_name": "gpt-4.1", "max_loops": 1},
    ],
    "task": "Your task here",
}

# Use a long timeout — these runs take minutes, not seconds.
with httpx.Client(timeout=3000.0) as client:
    client.post(f"{BASE_URL}/v1/swarm/completions", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`heavy_swarm.py`](heavy_swarm.py) | A heavy swarm run over `httpx` with a long timeout |

## Tips

- **Set a long client timeout.** The default in most HTTP clients is far too short and
  you will see a client-side timeout on a run that was succeeding server-side.
- **Cost scales with the internal team, not your roster.** Two seed agents does not
  mean two model calls. Try it on one real question before running it in a loop.
- **Try [advanced research](../advanced_research/) first** if your task is
  research-shaped — it's a managed pipeline for exactly that, with less setup.
