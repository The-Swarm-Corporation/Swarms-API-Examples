# 03 · Multi-Agent Swarms

A swarm is a list of agents plus a `swarm_type` telling the API how to orchestrate
them. One folder per swarm type.

Choose by the shape of the work:

| Your work looks like… | Use |
|---|---|
| Step 2 needs step 1's output | [`SequentialWorkflow`](sequential_workflow/) |
| Every agent can start immediately | [`ConcurrentWorkflow`](concurrent_workflow/) |
| Someone has to plan before splitting the work | [`HierarchicalSwarm`](hierarchical_swarm/) |
| Branching dependencies, fan-out and fan-in | [`GraphWorkflow`](graph_workflow/) |
| Many agents crossed with many tasks | [batched grid](batched_grid_workflow/) |
| Depth matters more than latency | [`HeavySwarm`](heavy_swarm/) |
| You want research without designing the team | [advanced research](advanced_research/) |
| You don't know what team you need | [auto-generate agents](auto_generate_agents/) |

---

## Sequential workflow

Agents run in order; each receives the previous agent's output.

| File | What it shows |
|---|---|
| [`sequential_workflow/batch_swarm_completions.py`](sequential_workflow/batch_swarm_completions.py) | Several complete swarms submitted in one request |

A minimal three-stage sequential swarm lives in
[`../01_getting_started/hello_swarm.py`](../01_getting_started/hello_swarm.py).
Applied sequential swarms are in [`../04_industry_examples/`](../04_industry_examples/).

## Concurrent workflow

Every agent runs at once against the same task. Fastest option when the agents don't
need each other.

| File | What it shows |
|---|---|
| [`concurrent_workflow/concurrent_workflow_with_tools.py`](concurrent_workflow/concurrent_workflow_with_tools.py) | Parallel agents with search and code-execution tools |

## Hierarchical swarm

A `coordinator` agent plans and delegates to `worker` agents, then synthesizes their
results. Set the `role` field on each agent.

| File | What it shows |
|---|---|
| [`hierarchical_swarm/simple_hierarchical.py`](hierarchical_swarm/simple_hierarchical.py) | One coordinator, two workers — start here |
| [`hierarchical_swarm/hierarchical_swarm.py`](hierarchical_swarm/hierarchical_swarm.py) | A fuller team with per-agent configuration |
| [`hierarchical_swarm/hierarchical_with_result_parsing.py`](hierarchical_swarm/hierarchical_with_result_parsing.py) | Walking the response to print each agent's contribution separately |
| [`hierarchical_swarm/hierarchical_with_claude_opus.py`](hierarchical_swarm/hierarchical_with_claude_opus.py) | The whole team running on Claude Opus 4.8 via the SDK |

## Graph workflow

You declare the graph: `agents`, `edges`, `entry_points`, `end_points`. The API
respects your dependency order. Full reference in
[`../docs/graph_workflow.md`](../docs/graph_workflow.md).

| File | What it shows |
|---|---|
| [`graph_workflow/basic_graph.py`](graph_workflow/basic_graph.py) | Two nodes, one edge — the concepts in miniature |
| [`graph_workflow/complete_graph.py`](graph_workflow/complete_graph.py) | Every feature plus error handling — copy this one |
| [`graph_workflow/parallel_fan_out_fan_in.py`](graph_workflow/parallel_fan_out_fan_in.py) | Fan out to parallel agents, fan back in — the map/reduce shape |
| [`graph_workflow/multi_layer_graph.py`](graph_workflow/multi_layer_graph.py) | Several dependent layers |
| [`graph_workflow/graph_with_edge_metadata.py`](graph_workflow/graph_with_edge_metadata.py) | Labelling edges so agents know where input came from |
| [`graph_workflow/edge_formats.py`](graph_workflow/edge_formats.py) | Every accepted way to declare an edge |

cURL version: [`../05_integrations/curl/graph_workflow.sh`](../05_integrations/curl/graph_workflow.sh).

## Batched grid workflow

Cross a list of agents with a list of tasks in one request to
`POST /v1/batched-grid-workflow/completions`.

| File | What it shows |
|---|---|
| [`batched_grid_workflow/simple_batched_grid.py`](batched_grid_workflow/simple_batched_grid.py) | Two agents, two tasks |
| [`batched_grid_workflow/batched_grid_workflow.py`](batched_grid_workflow/batched_grid_workflow.py) | The full grid payload |

Applied version: [ETF analysis grid](../04_industry_examples/finance/etf_analysis_grid.py).

## Heavy swarm

`HeavySwarm` spawns a larger internal agent team for research-grade work. Runs take
minutes — use a long timeout.

| File | What it shows |
|---|---|
| [`heavy_swarm/heavy_swarm.py`](heavy_swarm/heavy_swarm.py) | A heavy swarm run over `httpx` |

## Advanced research

A managed research pipeline behind `POST /v1/advanced-research/completions` — you
supply the question, not the team.

| File | What it shows |
|---|---|
| [`advanced_research/simple_advanced_research.py`](advanced_research/simple_advanced_research.py) | One question in, a researched answer out |
| [`advanced_research/advanced_research.py`](advanced_research/advanced_research.py) | Research depth, source handling, structured findings |

## Auto-generate agents

Describe the goal; let the API design the team.

| File | What it shows |
|---|---|
| [`auto_generate_agents/auto_generate_agents.py`](auto_generate_agents/auto_generate_agents.py) | `POST /v1/agents/auto-generate` |
| [`auto_generate_agents/auto_generate_agents_local.py`](auto_generate_agents/auto_generate_agents_local.py) | The same idea with the local `swarms` package |

## Streaming

| File | What it shows |
|---|---|
| [`streaming/stream_swarm_response.py`](streaming/stream_swarm_response.py) | Each agent's output printed as the swarm produces it |
