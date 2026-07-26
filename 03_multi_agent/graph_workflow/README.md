# GraphWorkflow

You declare the workflow as a directed graph: agents are nodes, edges are data flow.
The API respects your dependency order and runs independent branches in parallel.

**Use it when** the dependency structure isn't a straight line — fan-out, fan-in,
branching, or agents that need input from several predecessors.

**Endpoint:** `POST /v1/graph-workflow/completions`

Full reference: [`../../docs/graph_workflow.md`](../../docs/graph_workflow.md).

## Features

- **Directed graph structure** — nodes are agents, edges are connections
- **Parallel execution** — agents in the same layer run simultaneously
- **Entry and end points** — you control where the workflow starts and terminates
- **Edge metadata** — attach context to an edge so the receiving agent knows what it got
- **Automatic compilation** — the graph is optimized before execution

## Configuration

| Field | Type | Notes |
|---|---|---|
| `agents` | array | Agent configs — the graph's nodes |
| `edges` | array | `{"source": "A", "target": "B"}` — data flows A → B |
| `entry_points` | array | Agent names where execution begins |
| `end_points` | array | Agent names whose output is the final result |
| `task` | string | Goal handed to the entry-point agents |
| `name`, `description` | string | Labels for the run |

Edges also accept metadata and shorthand forms — see
[`edge_formats.py`](edge_formats.py) and
[`graph_with_edge_metadata.py`](graph_with_edge_metadata.py).

## Shape

```python
workflow_input = {
    "name": "My-Workflow",
    "agents": [
        {"agent_name": "Researcher", "model_name": "gpt-4.1", "max_loops": 1},
        {"agent_name": "Analyzer",   "model_name": "gpt-4.1", "max_loops": 1},
    ],
    "edges": [{"source": "Researcher", "target": "Analyzer"}],
    "entry_points": ["Researcher"],
    "end_points": ["Analyzer"],
    "task": "Your task here",
}

post(f"{BASE_URL}/v1/graph-workflow/completions", headers=headers, json=workflow_input)
```

## Examples

| File | What it shows |
|---|---|
| [`basic_graph.py`](basic_graph.py) | Two nodes, one edge — the concepts in miniature |
| [`complete_graph.py`](complete_graph.py) | Every feature plus error handling — copy this one |
| [`parallel_fan_out_fan_in.py`](parallel_fan_out_fan_in.py) | Fan out to parallel agents, fan back in |
| [`multi_layer_graph.py`](multi_layer_graph.py) | Several dependent layers |
| [`graph_with_edge_metadata.py`](graph_with_edge_metadata.py) | Labelling edges with context |
| [`edge_formats.py`](edge_formats.py) | Every accepted way to declare an edge |

cURL version: [`../../05_integrations/curl/graph_workflow.sh`](../../05_integrations/curl/graph_workflow.sh).

## Graph vs. the simpler types

| Your graph is | Use instead |
|---|---|
| A straight line | [`SequentialWorkflow`](../sequential_workflow/) — same result, less config |
| All nodes with no edges | [`ConcurrentWorkflow`](../concurrent_workflow/) |
| One node fanning out and back in | Graph is right, but see [`parallel_fan_out_fan_in.py`](parallel_fan_out_fan_in.py) first |

## Tips

- **Every agent needs a path.** A node unreachable from an entry point never runs.
- **Name agents distinctly.** Edges reference agents by `agent_name`; duplicates make
  the graph ambiguous.
- **Use edge metadata for provenance.** When an agent has several inbound edges, it
  needs to know which input came from where.
