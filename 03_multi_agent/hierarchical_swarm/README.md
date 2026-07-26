# HierarchicalSwarm

A coordinator agent oversees specialist workers: it receives the task, delegates
subtasks, and synthesizes what comes back into one answer.

**Use it when** the work needs planning before it can be split — the decomposition is
itself a judgment call, and you want one coherent deliverable rather than N separate
opinions.

**Endpoint:** `POST /v1/swarm/completions`

## Architecture

```
                    [Coordinator Agent]
                           |
          +----------------+----------------+
          |                |                |
    [Worker Agent 1] [Worker Agent 2] [Worker Agent 3]
```

**The coordinator** receives the initial task, delegates subtasks to workers,
synthesizes their outputs into a cohesive response, and makes the final
recommendation.

**Workers** execute their specialized subtask, apply domain expertise, and report
findings back to the coordinator.

## Configuration

| Field | Type | Notes |
|---|---|---|
| `swarm_type` | string | `"HierarchicalSwarm"` |
| `agents` | array | Agent configs |
| `agents[].role` | string | `"coordinator"` or `"worker"` |
| `task` | string | The main task, received by the coordinator |
| `max_loops` | integer | Execution loops (default `1`) |
| `name`, `description` | string | Labels for the run |

### Roles

| Role | Count | Responsibility |
|---|---|---|
| `coordinator` | Typically one | Plans, delegates, synthesizes the final response |
| `worker` | Many | Executes one domain-specific subtask, reports back |

## Shape

```python
payload = {
    "name": "Simple Hierarchical Swarm",
    "swarm_type": "HierarchicalSwarm",
    "agents": [
        {
            "agent_name": "Team Lead",
            "system_prompt": "You synthesize specialist input into recommendations.",
            "model_name": "gpt-4.1",
            "role": "coordinator",
            "max_loops": 1,
        },
        {
            "agent_name": "Productivity Analyst",
            "system_prompt": "You evaluate work efficiency and output quality.",
            "model_name": "gpt-4.1",
            "role": "worker",
            "max_loops": 1,
        },
    ],
    "task": "Your task here",
    "max_loops": 1,
}

requests.post(f"{BASE_URL}/v1/swarm/completions", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`simple_hierarchical.py`](simple_hierarchical.py) | One coordinator, two workers — start here |
| [`hierarchical_swarm.py`](hierarchical_swarm.py) | A fuller team with per-agent configuration |
| [`hierarchical_with_result_parsing.py`](hierarchical_with_result_parsing.py) | Walking the response to print each agent's contribution separately |
| [`hierarchical_with_claude_opus.py`](hierarchical_with_claude_opus.py) | The whole team on Claude Opus 4.8 via the SDK |

Applied hierarchical swarms:
[marketing department](../../04_industry_examples/marketing/marketing_department_swarm.py) ·
[supply chain](../../04_industry_examples/supply_chain/supply_chain_swarm.py) ·
[software development](../../04_industry_examples/software_engineering/software_dev_swarm.py).

## Tips

- **Give the coordinator the strongest model.** It does the planning and the synthesis;
  workers can often run on something cheaper. Each agent carries its own `model_name`.
- **Say "delegate" in the coordinator prompt.** Coordinators that aren't told to
  delegate tend to answer the whole thing themselves.
- **One coordinator.** Multiple coordinators compete rather than cooperate.
- **Keep worker scopes disjoint.** Overlapping workers produce redundant findings the
  coordinator then has to reconcile.
