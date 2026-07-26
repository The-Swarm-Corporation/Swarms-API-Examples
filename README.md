# Swarms API Examples

Runnable examples for the [Swarms API](https://docs.swarms.ai) — from a single agent
answering one question, to multi-agent swarms coordinating dozens of specialists.

Every example is a standalone file. Set your API key, pick one, run it.

---

## Quick start

```bash
git clone https://github.com/The-Swarm-Corporation/Swarms-API-Examples.git
cd Swarms-API-Examples

pip install -r requirements.txt

cp .env.example .env        # then paste your key into .env
export SWARMS_API_KEY="your-api-key"

python 01_getting_started/hello_agent.py
```

Get an API key at [swarms.world/platform/api-keys](https://swarms.world/platform/api-keys).

Every example reads `SWARMS_API_KEY` from the environment or a `.env` file, and
defaults to `https://api.swarms.world`. Point at a different deployment by setting
`SWARMS_API_BASE_URL`.

---

## Where to start

| If you want to… | Start here |
|---|---|
| Run your first request | [`01_getting_started/hello_agent.py`](01_getting_started/hello_agent.py) |
| Run your first swarm | [`01_getting_started/hello_swarm.py`](01_getting_started/hello_swarm.py) |
| Use the Python SDK instead of HTTP | [`01_getting_started/hello_agent_sdk.py`](01_getting_started/hello_agent_sdk.py) |
| Use no dependencies at all | [`01_getting_started/hello_agent.sh`](01_getting_started/hello_agent.sh) |
| Understand every agent config field | [`02_single_agent/basics/agent_completion.py`](02_single_agent/basics/agent_completion.py) |
| Pick the right swarm type | [Swarm types](#swarm-types) below |
| See a real-world build | [`04_industry_examples/`](04_industry_examples/) |

---

## Repository layout

| Folder | What's in it |
|---|---|
| [`01_getting_started/`](01_getting_started/) | Four minimal, heavily commented first requests |
| [`02_single_agent/`](02_single_agent/) | One agent: config, streaming, vision, reasoning, model selection |
| [`03_multi_agent/`](03_multi_agent/) | Every swarm type, one folder each |
| [`04_industry_examples/`](04_industry_examples/) | Complete builds for healthcare, finance, marketing, and more |
| [`05_integrations/`](05_integrations/) | Python SDK, MCP server, raw cURL |
| [`06_platform_utilities/`](06_platform_utilities/) | Models, rate limits, credits, usage, logs |
| [`docs/`](docs/) | Long-form reference for agent completions and graph workflows |

---

## Swarm types

The `swarm_type` field decides how your agents are orchestrated. Pick by the shape
of the work, not by agent count.

| Swarm type | Agents… | Use it when | Examples |
|---|---|---|---|
| `SequentialWorkflow` | run in order, each seeing the last one's output | each step depends on the previous one | [sequential_workflow/](03_multi_agent/sequential_workflow/) |
| `ConcurrentWorkflow` | all run at once on the same task | the agents are independent and you want speed | [concurrent_workflow/](03_multi_agent/concurrent_workflow/) |
| `HierarchicalSwarm` | a coordinator plans and delegates to workers | the work needs planning before it can be split | [hierarchical_swarm/](03_multi_agent/hierarchical_swarm/) |
| `GraphWorkflow` | run as a directed graph you define | you need fan-out, fan-in, or branching dependencies | [graph_workflow/](03_multi_agent/graph_workflow/) |
| Batched grid | a grid of agents × tasks in one request | you have many agents and many tasks to cross | [batched_grid_workflow/](03_multi_agent/batched_grid_workflow/) |
| `HeavySwarm` | a large internal agent team | research-grade depth matters more than latency | [heavy_swarm/](03_multi_agent/heavy_swarm/) |
| Advanced research | a managed research pipeline | you want researched answers without designing a team | [advanced_research/](03_multi_agent/advanced_research/) |

List what your account can reach with
[`06_platform_utilities/list_swarm_types.py`](06_platform_utilities/list_swarm_types.py).

---

## Examples by industry

The same examples, indexed by the domain they were built for.

| Industry | Examples |
|---|---|
| **Healthcare** | [ICD-10 diagnosis](04_industry_examples/healthcare/icd10_diagnosis_swarm.py) · [ICD-10 coding](04_industry_examples/healthcare/icd10_coding_swarm.py) · [medical swarm](04_industry_examples/healthcare/medical_swarm.py) · [biomedical research](04_industry_examples/healthcare/biomedical_research_swarm.py) · [enterprise demo](04_industry_examples/healthcare/enterprise_medical_demo.py) · [medical coding](04_industry_examples/healthcare/medical_coding_swarm.py) · [lab data](04_industry_examples/healthcare/lab_data_concurrent_swarm.py) · [dermatology](04_industry_examples/healthcare/dermatology_concurrent_swarm.py) · [speech transcripts](04_industry_examples/healthcare/speech_transcript_swarm.py) |
| **Finance** | [financial analysis](04_industry_examples/finance/financial_analysis_swarm.py) · [analysis with tools](04_industry_examples/finance/financial_swarm_with_tools.py) · [ETF grid](04_industry_examples/finance/etf_analysis_grid.py) · [crypto agent](04_industry_examples/finance/crypto_analysis_agent.py) |
| **Marketing** | [marketing department](04_industry_examples/marketing/marketing_department_swarm.py) |
| **Supply chain** | [supply chain analysis](04_industry_examples/supply_chain/supply_chain_swarm.py) |
| **Software engineering** | [dev team swarm](04_industry_examples/software_engineering/software_dev_swarm.py) |
| **Hospitality** | [catering quotes](04_industry_examples/hospitality/catering_quote_agent.py) |

---

## Capabilities

| Capability | Examples |
|---|---|
| Streaming responses | [single agent](02_single_agent/streaming/) · [swarm](03_multi_agent/streaming/) |
| Vision / image input | [02_single_agent/vision/](02_single_agent/vision/) |
| Tool use | [concurrent workflow with tools](03_multi_agent/concurrent_workflow/concurrent_workflow_with_tools.py) · [streaming with tools](02_single_agent/streaming/streaming_with_tools.py) |
| Agent handoffs | [agent_handoffs.py](02_single_agent/basics/agent_handoffs.py) |
| Batch requests | [agents](02_single_agent/basics/batch_completions.py) · [swarms](03_multi_agent/sequential_workflow/batch_swarm_completions.py) |
| Reasoning agents | [02_single_agent/reasoning/](02_single_agent/reasoning/) |
| Auto-generated agent teams | [03_multi_agent/auto_generate_agents/](03_multi_agent/auto_generate_agents/) |
| Frontier models (Claude Opus) | [02_single_agent/models/](02_single_agent/models/) |
| MCP server | [05_integrations/mcp/](05_integrations/mcp/) |

---

## Requirements

Python 3.10+. Install everything with `pip install -r requirements.txt`, or install
only what you need:

| Package | Needed by |
|---|---|
| `requests`, `python-dotenv` | almost every example |
| `httpx` | heavy swarm, ETF grid, the httpx model example |
| `swarms-client` | SDK examples |
| `fastmcp` | MCP integration |
| `swarms` | only `auto_generate_agents_local.py` |

---

## Documentation and support

- **API docs** — <https://docs.swarms.ai>
- **Swarms docs** — <https://docs.swarms.world>
- **Agent completions reference** — [`docs/agent_completions.md`](docs/agent_completions.md)
- **Graph workflow reference** — [`docs/graph_workflow.md`](docs/graph_workflow.md)
- **Talk to us** — <https://cal.com/swarms>

## Contributing

New examples are welcome. Keep to the conventions the existing files follow:

1. One concept per file, runnable on its own.
2. A module docstring naming what it demonstrates and how to run it.
3. Read the key from `SWARMS_API_KEY`; never hardcode credentials.
4. Read the host from `os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")`.
5. Add the file to its folder README and to the tables above.
