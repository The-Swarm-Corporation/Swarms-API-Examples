# Single Agent — Basics

The core agent request and the options that shape it. Read
[`agent_completion.py`](agent_completion.py) first; it documents every field an
`agent_config` accepts.

**Endpoint:** `POST /v1/agent/completions`
**Batch endpoint:** `POST /v1/agent/batch/completions`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `agent_config.agent_name` | string | Identifies the agent in logs and responses |
| `agent_config.description` | string | Short statement of the agent's job |
| `agent_config.system_prompt` | string | Where the behaviour actually lives — the highest-leverage field |
| `agent_config.model_name` | string | Any routable model ([`list_models.py`](../../06_platform_utilities/list_models.py)) |
| `agent_config.max_loops` | integer \| `"auto"` | Reasoning passes. `"auto"` lets the API decide |
| `agent_config.max_tokens` | integer | Output ceiling |
| `agent_config.temperature` | float | Sampling temperature |
| `agent_config.dynamic_temperature_enabled` | bool | Let the API vary temperature per loop |
| `agent_config.role` | string | `"worker"` or `"coordinator"` — matters inside swarms |
| `agent_config.handoffs` | array | Specialist agents this agent may delegate to |
| `task` | string | What you want done |
| `img` | string | Base64 data URL for vision — see [`../vision/`](../vision/) |

## Shape

```python
payload = {
    "agent_config": {
        "agent_name": "Research Analyst",
        "system_prompt": "You are a research analyst...",
        "model_name": "gpt-4.1",
        "max_loops": 1,
        "max_tokens": 8192,
        "temperature": 0.5,
    },
    "task": "Your task here",
}

requests.post(f"{BASE_URL}/v1/agent/completions", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`agent_completion.py`](agent_completion.py) | The full config surface — the reference example |
| [`max_loops_auto.py`](max_loops_auto.py) | `"max_loops": "auto"` for tasks of varying difficulty |
| [`conversation_history.py`](conversation_history.py) | What carries across loops, plus a `/health` check |
| [`batch_completions.py`](batch_completions.py) | Many independent tasks in one request |
| [`agent_handoffs.py`](agent_handoffs.py) | Delegation to specialists without building a swarm |

## Batch vs. swarm vs. handoffs

Three ways to involve more than one task or agent — they solve different problems:

| You want | Use |
|---|---|
| The same agent on many unrelated tasks | [`batch_completions.py`](batch_completions.py) |
| One agent that can call specialists when it decides to | [`agent_handoffs.py`](agent_handoffs.py) |
| A team with a fixed orchestration you control | [`../../03_multi_agent/`](../../03_multi_agent/) |

## Tips

- **Spend your time on `system_prompt`.** Model and temperature changes rarely rescue
  a vague prompt.
- **Start at `max_loops: 1`.** Raise it only when you can see the agent needs another
  pass; every loop costs tokens and latency.
- **Set `max_tokens` above your expected output.** A truncated response means a retry.
