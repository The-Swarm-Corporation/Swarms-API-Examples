# Auto-Generate Agents

Describe the goal and let the API design the agent team — names, roles, and system
prompts — instead of writing them yourself.

**Use it when** you know what you want but not who should do it, or as a starting
point you then edit by hand.

**Endpoint:** `POST /v1/agents/auto-generate`

## Configuration

| Field | Type | Notes |
|---|---|---|
| `task` | string | Describe the goal in full. Detail here is what makes the generated roster good |

## Shape

```python
payload = {
    "task": (
        "Create a comprehensive market analysis report for AI companies, including "
        "financial metrics, growth potential, and competitive analysis."
    )
}

requests.post(f"{BASE_URL}/v1/agents/auto-generate", headers=headers, json=payload)
```

## Examples

| File | What it shows |
|---|---|
| [`auto_generate_agents.py`](auto_generate_agents.py) | The hosted endpoint |
| [`auto_generate_agents_local.py`](auto_generate_agents_local.py) | The same idea with the local `swarms` package (`AgentsBuilder`) — `pip install swarms` |

## The intended workflow

1. **Generate** a roster from a detailed task description.
2. **Read it.** Treat it as a draft, not a finished design.
3. **Edit the prompts.** Generated system prompts are generic; yours will carry the
   domain knowledge that makes the swarm useful.
4. **Paste into a swarm.** Drop the roster into the `agents` array of whichever
   [swarm type](../) fits the dependency structure.

## Tips

- **Describe the deliverable, not just the topic.** "Analyze AI companies" produces a
  vaguer team than "produce a comparative report with financial metrics, growth
  outlook, and competitive positioning."
- **Generated rosters skew large.** Trimming agents usually improves the result and
  always cuts cost.
- **It doesn't pick a swarm type for you.** That's still your call —
  see the table in [`../README.md`](../README.md).
