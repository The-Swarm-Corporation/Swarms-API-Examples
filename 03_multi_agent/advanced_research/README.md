# Advanced Research

A managed research pipeline: multi-source collection, analysis, and synthesis with
citations. You supply the question — the API supplies the team.

**Use it when** the task is research-shaped and you don't want to design an agent
roster for it.

**Endpoint:** `POST /v1/advanced-research/completions`

## Features

- **Multi-source research** — collects from multiple sources rather than one pass
- **Comprehensive analysis** — deep analysis of the topic, not a summary
- **Source citations** — findings carry source references
- **Structured results** — organized output rather than free prose

## Configuration

| Field | Type | Notes |
|---|---|---|
| `task` | string | The research question |
| `config.worker_model_name` | string | Model the research workers run on |
| `config.sources` | integer | How many sources to gather |
| `config.depth` | string | e.g. `"comprehensive"` — how deep to go |

## Shape

```python
research_input = {
    "config": {
        "worker_model_name": "gpt-4.1",
        "sources": 5,
        "depth": "comprehensive",
    },
    "task": "Research topic here",
}

post(f"{BASE_URL}/v1/advanced-research/completions", headers=headers, json=research_input)
```

## Examples

| File | What it shows |
|---|---|
| [`simple_advanced_research.py`](simple_advanced_research.py) | One question in, a researched answer out |
| [`advanced_research.py`](advanced_research.py) | Research depth, source handling, structured findings |

## Advanced research vs. building it yourself

| You want | Use |
|---|---|
| Researched answers with no roster design | This endpoint |
| Control over who researches what | A [`GraphWorkflow`](../graph_workflow/) or [`HierarchicalSwarm`](../hierarchical_swarm/) |
| Maximum depth, cost no object | [`HeavySwarm`](../heavy_swarm/) |

## Tips

- **Ask a researchable question.** "What are the tradeoffs between X and Y as of 2026"
  works; "write me a strategy" doesn't — that's a task for a swarm.
- **Raise `sources` before `depth`.** More sources usually improves grounding more
  than deeper analysis of the same few.
- **Expect minutes.** Set a generous client timeout, as with heavy swarm.
