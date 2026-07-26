# Finance Examples

Market and investment analysis workflows, covering all three shapes: a single agent, a
sequential pipeline, a concurrent panel, and a grid.

> **Not investment advice.** These demonstrate the API. Model output about markets is
> not research, is frequently wrong about current prices and events, and must not drive
> financial decisions.

## Examples

| File | Swarm type | What it does |
|---|---|---|
| [`crypto_analysis_agent.py`](crypto_analysis_agent.py) | Single agent | Market analysis and risk-adjusted strategy suggestions |
| [`financial_analysis_swarm.py`](financial_analysis_swarm.py) | Sequential | Data gathering → quantitative analysis → written investment view |
| [`financial_swarm_with_tools.py`](financial_swarm_with_tools.py) | Concurrent | Parallel analysts with search and code execution for live data |
| [`etf_analysis_grid.py`](etf_analysis_grid.py) | Batched grid | Risk and quant analysts crossed with several ETFs, run asynchronously |

## Why each swarm type

**Single agent** ([`crypto_analysis_agent.py`](crypto_analysis_agent.py)) — one
coherent perspective on one asset. Adding agents here would add cost without adding
insight.

**Sequential** ([`financial_analysis_swarm.py`](financial_analysis_swarm.py)) — the
write-up needs the analysis, and the analysis needs the data. A real dependency chain.

**Concurrent** ([`financial_swarm_with_tools.py`](financial_swarm_with_tools.py)) —
a risk analyst and a growth analyst examine the same company independently. Neither
needs the other's conclusion first.

**Grid** ([`etf_analysis_grid.py`](etf_analysis_grid.py)) — several analyst lenses ×
several ETFs. The grid runs the full matrix in one request instead of one call per
pair.

## Tools matter here

Financial questions turn on current data, and a model reasoning from memory will
confidently state stale prices.
[`financial_swarm_with_tools.py`](financial_swarm_with_tools.py) shows agents with
search and code execution enabled so they can fetch and compute rather than recall.

Prefer the tool-enabled examples for anything where the answer depends on today's
numbers.

## Adapting these

1. **Swap the tickers and the task.** Both are near the top of each file.
2. **Rewrite the analyst prompts** to match your methodology — that's where a house
   view lives.
3. **Enable tools** if the output depends on current data.
4. **Watch grid cost.** `etf_analysis_grid.py` scales as agents × tickers; five
   analysts over twenty ETFs is one hundred model calls.
