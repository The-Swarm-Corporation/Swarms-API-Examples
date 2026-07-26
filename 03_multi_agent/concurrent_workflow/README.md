# ConcurrentWorkflow

Every agent runs at the same time against the same task. Their outputs come back
side by side; no agent sees another's work.

**Use it when** the agents are genuinely independent — several specialists reviewing
the same case, several analysts examining the same dataset. It is the fastest swarm
type, because total time is the slowest agent rather than the sum of all of them.

**Endpoint:** `POST /v1/swarm/completions`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `swarm_type` | string | `"ConcurrentWorkflow"` |
| `agents` | array | Agent configs — order is irrelevant here |
| `task` | string | The same task handed to every agent |
| `max_loops` | integer | Loops per agent (default `1`) |
| `name`, `description` | string | Labels for the run |

## Shape

```python
payload = {
    "name": "Concurrent-Workflow",
    "swarm_type": "ConcurrentWorkflow",
    "agents": [
        {"agent_name": "Risk Analyst",        "system_prompt": "...", "model_name": "gpt-4.1", "max_loops": 1},
        {"agent_name": "Performance Analyst", "system_prompt": "...", "model_name": "gpt-4.1", "max_loops": 1},
    ],
    "task": "Your task here",
}

requests.post(f"{BASE_URL}/v1/swarm/completions", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`concurrent_workflow_with_tools.py`](concurrent_workflow_with_tools.py) | Parallel agents with search and code-execution tools |

Applied concurrent swarms:
[lab data](../../04_industry_examples/healthcare/lab_data_concurrent_swarm.py) ·
[dermatology](../../04_industry_examples/healthcare/dermatology_concurrent_swarm.py) ·
[financial analysis with tools](../../04_industry_examples/finance/financial_swarm_with_tools.py).

## Tips

- **Differentiate the prompts.** Identical agents produce near-identical output and
  waste the parallelism. Give each one a distinct lens.
- **You get N answers, not one.** If you need them merged, follow with a synthesis
  step — a [`SequentialWorkflow`](../sequential_workflow/) or a
  [`HierarchicalSwarm`](../hierarchical_swarm/), where the coordinator does the merge.
- **Watch rate limits.** N agents means N concurrent model calls;
  [`check_rate_limits.py`](../../06_platform_utilities/check_rate_limits.py) tells you
  your ceiling.
