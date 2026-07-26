# Single Agent — Reasoning

Reasoning agents are specialized agent types that reason about a problem — or about
someone else's work — rather than producing a direct answer.

**Endpoints:**
`POST /v1/reasoning-agent/completions` · `GET /v1/reasoning-agent/types`

## Reasoning agent types

| Type | What it does |
|---|---|
| `reasoning-duo` | Two agents reason against each other, surfacing disagreement |
| `self-consistency` | Multiple independent attempts, converged on the most consistent answer |
| `IRE` | Iterative reflective reasoning — revise, then revise again |
| `AgentJudge` | Evaluates and critiques work rather than producing it |

The list is account-dependent. Print what yours can reach by running
[`reasoning_agent_types.py`](reasoning_agent_types.py), which calls
`GET /v1/reasoning-agent/types` before running one.

## Shape

```python
payload = {
    "agent_name": "reasoning-agent",
    "model_name": "gpt-4.1",
    "swarm_type": "reasoning-duo",
    "task": "Your reasoning task here",
}

requests.post(f"{BASE_URL}/v1/reasoning-agent/completions", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`reasoning_agent_types.py`](reasoning_agent_types.py) | List the available types, then run `reasoning-duo` |
| [`reasoning_agents.py`](reasoning_agents.py) | `AgentJudge` — an agent evaluating work instead of producing it |

## When to use these

Reach for a reasoning agent when the *quality of the reasoning* is the deliverable —
evaluating a plan, checking an argument, deciding between options. For work that just
needs doing, a well-prompted standard agent at `max_loops: 1` is cheaper and faster.

`AgentJudge` pairs well with a swarm: generate with a
[`ConcurrentWorkflow`](../../03_multi_agent/concurrent_workflow/), then judge the
outputs.
