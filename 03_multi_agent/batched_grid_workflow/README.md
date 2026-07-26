# Batched Grid Workflow

Cross a list of agents with a list of tasks: every agent processes every task, in one
request. An agents × tasks matrix.

**Use it when** you have several perspectives to apply across several subjects — three
analysts over five companies, four reviewers over six documents. One request instead
of fifteen or twenty-four.

**Endpoint:** `POST /v1/batched-grid-workflow/completions`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `agent_completions` | array | The agents — note the field name is **not** `agents` |
| `tasks` | array | The list of tasks; each agent processes each one |
| `max_loops` | integer | Loops per agent (default `1`) |
| `imgs` | array | Optional images shared across the grid |
| `name`, `description` | string | Labels for the run |

## Shape

```python
workflow_input = {
    "name": "Grid-Workflow",
    "agent_completions": [
        {"agent_name": "Risk Analyst", "system_prompt": "...", "model_name": "gpt-4.1", "max_loops": 1},
        {"agent_name": "SEO Specialist", "system_prompt": "...", "model_name": "gpt-4.1", "max_loops": 1},
    ],
    "tasks": ["Task 1", "Task 2", "Task 3"],
    "max_loops": 1,
}

post(f"{BASE_URL}/v1/batched-grid-workflow/completions", headers=headers, json=workflow_input)
```

## Examples

| File | What it shows |
|---|---|
| [`simple_batched_grid.py`](simple_batched_grid.py) | Two agents, two tasks |
| [`batched_grid_workflow.py`](batched_grid_workflow.py) | The full grid payload |

Applied: [ETF analysis grid](../../04_industry_examples/finance/etf_analysis_grid.py) —
risk and quant analysts across several ETFs, driven asynchronously.

cURL version: [`../../05_integrations/curl/batched_grid_workflow.sh`](../../05_integrations/curl/batched_grid_workflow.sh).

## Grid vs. batch vs. concurrent

| You have | Use |
|---|---|
| N agents × M tasks, all combinations | This grid |
| One agent, M unrelated tasks | [`batch_completions.py`](../../02_single_agent/basics/batch_completions.py) |
| N agents, one shared task | [`ConcurrentWorkflow`](../concurrent_workflow/) |
| M complete swarms | [`batch_swarm_completions.py`](../sequential_workflow/batch_swarm_completions.py) |

## Tips

- **The grid multiplies.** 5 agents × 10 tasks is 50 model calls — check
  [`check_rate_limits.py`](../../06_platform_utilities/check_rate_limits.py) before
  scaling up, and expect the cost to scale with the product.
- **`agent_completions`, not `agents`.** This endpoint uses a different field name than
  `/v1/swarm/completions`; it's the most common mistake here.
- **Go async for large grids.** [`etf_analysis_grid.py`](../../04_industry_examples/finance/etf_analysis_grid.py)
  shows the `httpx` + `asyncio` pattern.
