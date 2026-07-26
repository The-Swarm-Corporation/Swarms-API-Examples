# 07 · Model Integrations

The same single-agent request against every model provider the API can route to. Each
file changes one thing — `model_name` — so you can compare capability, cost, and
latency on your own task.

**Endpoint:** `POST /v1/agent/completions`

## Naming

Models are addressed as `provider/model`:

| Provider | Prefix | Example |
|---|---|---|
| Anthropic | `anthropic/` | `anthropic/claude-opus-5` |
| OpenAI | `openai/` | `openai/gpt-5` |
| Google | `gemini/` | `gemini/gemini-2.5-pro` |
| Groq | `groq/` | `groq/llama-3.3-70b-versatile` |
| DeepSeek | `deepseek/` | `deepseek/deepseek-reasoner` |
| xAI | `xai/` | `xai/grok-4` |
| OpenRouter | `openrouter/<vendor>/` | `openrouter/meta-llama/llama-3.3-70b-instruct` |

OpenRouter takes **two** slashes — the vendor segment is OpenRouter's own, not a Swarms
provider. Some short names (`gpt-4.1`, `gpt-4o`) also resolve without a prefix.

Model catalogues change constantly. Confirm a name before depending on it:

```bash
python list_supported_models.py anthropic
```

## Examples

| File | Model | Transport |
|---|---|---|
| [`anthropic_claude_opus_5.py`](anthropic_claude_opus_5.py) | `anthropic/claude-opus-5` | SDK |
| [`anthropic_claude_sonnet_5.py`](anthropic_claude_sonnet_5.py) | `anthropic/claude-sonnet-5` | raw HTTP |
| [`openai_gpt_5.py`](openai_gpt_5.py) | `openai/gpt-5` | raw HTTP |
| [`google_gemini_agent.py`](google_gemini_agent.py) | `gemini/...` | raw HTTP |
| [`groq_agent.py`](groq_agent.py) | `groq/...` | raw HTTP |
| [`deepseek_agent.py`](deepseek_agent.py) | `deepseek/...` | raw HTTP |
| [`xai_grok_agent.py`](xai_grok_agent.py) | `xai/...` | raw HTTP |
| [`openrouter_agent.py`](openrouter_agent.py) | `openrouter/<vendor>/...` | raw HTTP |
| [`compare_models.py`](compare_models.py) | seven at once | Same agent and task across every provider, concurrently |
| [`mixed_model_swarm.py`](mixed_model_swarm.py) | three in one swarm | A different model per agent in a single request |
| [`list_supported_models.py`](list_supported_models.py) | — | Lists what your key can actually reach |

The two Anthropic files send the same request through different transports — compare
them to see what the SDK builds for you.

`list_supported_models.py` takes optional filter terms:

```bash
python list_supported_models.py                 # everything, grouped by provider
python list_supported_models.py anthropic       # names containing "anthropic"
python list_supported_models.py gpt-5 claude    # names matching either term
```

## Choosing

| Priority | Start with |
|---|---|
| Hardest reasoning, expensive-to-be-wrong work | Claude Opus 5, GPT-5 at higher effort |
| Balanced default, and swarm interiors | Claude Sonnet 5 |
| Raw speed — routing, classification, extraction | Groq |
| Cost per correct answer on math, logic, code | DeepSeek |
| Very long inputs | Gemini |
| Open-weight models with no first-party endpoint | OpenRouter |

Don't pick from the table alone. [`compare_models.py`](compare_models.py) sends one
task to seven models concurrently and prints latency, token counts, and cost for each —
point it at *your* prompt and read the actual output.

**Reasoning models** (Claude Opus/Sonnet 5, GPT-5, `deepseek-reasoner`) accept
`reasoning_effort`. Higher effort spends more tokens thinking before answering — start
low and raise it only where your evaluation shows it earns the cost. GPT-5's `minimal`
behaves close to a non-reasoning model.

## Mixing models in a swarm

Every agent in a swarm carries its own `model_name`, so a coordinator can run on a
frontier model while workers run on something cheap and fast. That is usually the right
shape for a large swarm.

[`mixed_model_swarm.py`](mixed_model_swarm.py) does it in a `SequentialWorkflow`: Groq
gathers the facts, Opus 5 does the analysis, Sonnet 5 writes the brief. The same applies
to every swarm type in [`../03_multi_agent/`](../03_multi_agent/) — see
[`hierarchical_swarm/`](../03_multi_agent/hierarchical_swarm/) for the coordinator
pattern.

## Related

- Single-agent model examples: [`../02_single_agent/models/`](../02_single_agent/models/)
- Every model your account can route to: [`../06_platform_utilities/list_models.py`](../06_platform_utilities/list_models.py)
- Full `agent_config` reference: [`../02_single_agent/basics/README.md`](../02_single_agent/basics/README.md)
