# Swarms API Examples

A comprehensive example suite for the [Swarms API](https://docs.swarms.ai) — one
endpoint that runs AI agents, alone or in coordinated swarms, on any frontier model.

An agent is a system prompt, a model, and a task:

```bash
curl -X POST "https://api.swarms.world/v1/agent/completions" \
  -H "x-api-key: $SWARMS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_config": {
      "system_prompt": "You are a research analyst.",
      "model_name": "anthropic/claude-opus-5"
    },
    "task": "What are the tradeoffs between vector search and keyword search?"
  }'
```

From there the request grows along two axes, and nothing else about it changes:

- **Models** — swap `model_name` for `openai/gpt-5`, `gemini/gemini-2.5-pro`,
  `groq/llama-3.3-70b-versatile`, or anything on OpenRouter → [Models](#models)
- **Agents** — replace `agent_config` with a list of `agents` and a `swarm_type`, and
  the same endpoint runs them in sequence, in parallel, under a coordinator, or as a
  graph you define → [Swarm types](#swarm-types)

No framework to learn, no orchestration to host, no provider SDKs to wire together.
Every example here is a standalone file: set your key, pick one, run it.

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
| Pick the right model | [Models](#models) below |
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
| [`07_model_integrations/`](07_model_integrations/) | One agent per provider — GPT-5, Claude Opus/Sonnet 5, Gemini, Groq, DeepSeek, Grok, OpenRouter |

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

## Models

Every provider reaches you through the same `agent_config`. Only `model_name` changes,
so any example in this repo runs on any model in this table.

| Provider | `model_name` | Example |
|---|---|---|
| OpenAI | `openai/gpt-5` | [openai_gpt_5.py](07_model_integrations/openai_gpt_5.py) |
| Anthropic | `anthropic/claude-opus-5` | [anthropic_claude_opus_5.py](07_model_integrations/anthropic_claude_opus_5.py) |
| Anthropic | `anthropic/claude-sonnet-5` | [anthropic_claude_sonnet_5.py](07_model_integrations/anthropic_claude_sonnet_5.py) |
| Google | `gemini/gemini-2.5-pro` | [google_gemini_agent.py](07_model_integrations/google_gemini_agent.py) |
| DeepSeek | `deepseek/deepseek-reasoner` | [deepseek_agent.py](07_model_integrations/deepseek_agent.py) |
| xAI | `xai/grok-4` | [xai_grok_agent.py](07_model_integrations/xai_grok_agent.py) |
| Groq | `groq/llama-3.3-70b-versatile` | [groq_agent.py](07_model_integrations/groq_agent.py) |
| OpenRouter | `openrouter/<vendor>/<model>` | [openrouter_agent.py](07_model_integrations/openrouter_agent.py) |

OpenRouter takes **two** slashes — the vendor segment is OpenRouter's, not a Swarms
provider. A few short OpenAI names (`gpt-4.1`, `gpt-4o`) still resolve without a prefix,
which is why older examples here use them; prefer the explicit prefix in new code.

| Then | Run |
|---|---|
| Compare models on your own task — latency, tokens, cost | [compare_models.py](07_model_integrations/compare_models.py) |
| Use a different model per agent inside one swarm | [mixed_model_swarm.py](07_model_integrations/mixed_model_swarm.py) |
| Confirm what your key can actually route to | [list_supported_models.py](07_model_integrations/list_supported_models.py) |

Reasoning models (GPT-5, Claude Opus/Sonnet 5, `deepseek-reasoner`) accept
`reasoning_effort` — `minimal`, `low`, `medium`, or `high`. Higher effort spends more
tokens thinking before answering; the default is `low`. Full notes in
[`07_model_integrations/README.md`](07_model_integrations/README.md).

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
| Every model provider | [07_model_integrations/](07_model_integrations/) — see [Models](#models) above |
| Comparing models on one task | [compare_models.py](07_model_integrations/compare_models.py) |
| Different model per agent in a swarm | [mixed_model_swarm.py](07_model_integrations/mixed_model_swarm.py) |
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
- **Agent completions reference** — <https://docs.swarms.ai/api-reference/agents/execute-agent-completion>
- **Model integrations** — [`07_model_integrations/README.md`](07_model_integrations/README.md)
- **Talk to us** — <https://cal.com/swarms>

## Contributing

New examples are welcome. Keep to the conventions the existing files follow:

1. One concept per file, runnable on its own.
2. A module docstring naming what it demonstrates and how to run it.
3. Read the key from `SWARMS_API_KEY`; never hardcode credentials.
4. Read the host from `os.getenv("SWARMS_API_BASE_URL", "https://api.swarms.world")`.
5. Add the file to its folder README and to the tables above.
