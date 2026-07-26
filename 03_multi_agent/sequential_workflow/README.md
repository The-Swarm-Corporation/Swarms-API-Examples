# SequentialWorkflow

Agents run one after another in the order you list them. Each agent receives the
previous agent's output as its input.

**Use it when** step 2 genuinely needs step 1's result — research → analysis → write-up,
extract → validate → format. If the agents don't depend on each other, use
[ConcurrentWorkflow](../concurrent_workflow/) instead; it's faster.

**Endpoint:** `POST /v1/swarm/completions`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `swarm_type` | string | `"SequentialWorkflow"` |
| `agents` | array | Agent configs, **in execution order** |
| `task` | string | Goal handed to the first agent |
| `max_loops` | integer | Loops over the whole chain (default `1`) |
| `name`, `description` | string | Labels for the run; show up in logs |

Each entry in `agents` takes the same fields as a single agent's `agent_config` —
see [`../../02_single_agent/basics/agent_completion.py`](../../02_single_agent/basics/agent_completion.py).

## Shape

```python
payload = {
    "name": "Sequential-Workflow",
    "swarm_type": "SequentialWorkflow",
    "agents": [
        {"agent_name": "Researcher", "system_prompt": "...", "model_name": "gpt-4.1", "max_loops": 1},
        {"agent_name": "Analyst",    "system_prompt": "...", "model_name": "gpt-4.1", "max_loops": 1},
    ],
    "task": "Your task here",
    "max_loops": 1,
}

requests.post(f"{BASE_URL}/v1/swarm/completions", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`../../01_getting_started/hello_swarm.py`](../../01_getting_started/hello_swarm.py) | A minimal three-stage chain — start here |
| [`batch_swarm_completions.py`](batch_swarm_completions.py) | Several complete swarms in one request (`POST /v1/swarm/batch/completions`) |

Applied sequential swarms live in [`../../04_industry_examples/`](../../04_industry_examples/) —
most of the healthcare and finance examples use this type.

## Tips

- **Order is the design.** The chain is only as good as its weakest handoff; make each
  agent's output explicitly usable by the next one.
- **Prompt for the handoff.** Tell each agent what it will receive and what the next
  agent needs from it.
- **Keep roles narrow.** Three focused agents beat one agent asked to do three jobs.
