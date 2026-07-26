# 04 · Industry Examples

Complete builds, not feature demos. Each file solves a real problem end to end and
shows how the pieces from [`02_single_agent/`](../02_single_agent/) and
[`03_multi_agent/`](../03_multi_agent/) fit together in production shape.

Read one in your domain, then adapt the agent roster and prompts.

> These are engineering references, not professional advice. The healthcare examples
> in particular are illustrations of the API — they are not clinical tools and must
> not be used for diagnosis or treatment decisions.

## Healthcare

| File | Swarm type | What it does |
|---|---|---|
| [`healthcare/simple_medical_swarm.py`](healthcare/simple_medical_swarm.py) | Sequential | The shortest clinical pipeline here — start with this one |
| [`healthcare/medical_swarm.py`](healthcare/medical_swarm.py) | Sequential | Intake → differential reasoning → recommendation |
| [`healthcare/icd10_diagnosis_swarm.py`](healthcare/icd10_diagnosis_swarm.py) | Sequential | Lab data → ICD-10 codes → clinical decision support |
| [`healthcare/icd10_coding_swarm.py`](healthcare/icd10_coding_swarm.py) | Sequential | Extract, explain, and validate codes — one agent per step |
| [`healthcare/medical_coding_swarm.py`](healthcare/medical_coding_swarm.py) | Sequential | Coding assistant with tool access for lookups |
| [`healthcare/biomedical_research_swarm.py`](healthcare/biomedical_research_swarm.py) | Sequential | Literature review and synthesis |
| [`healthcare/enterprise_medical_demo.py`](healthcare/enterprise_medical_demo.py) | Sequential | Production-shaped: many specialists, error handling, formatted reporting |
| [`healthcare/speech_transcript_swarm.py`](healthcare/speech_transcript_swarm.py) | Sequential | Clinical review of a speech transcript |
| [`healthcare/lab_data_concurrent_swarm.py`](healthcare/lab_data_concurrent_swarm.py) | Concurrent | Parallel interpretation of a lab panel, one agent per marker group |
| [`healthcare/dermatology_concurrent_swarm.py`](healthcare/dermatology_concurrent_swarm.py) | Concurrent | Parallel specialist review, then log retrieval |

## Finance

| File | Swarm type | What it does |
|---|---|---|
| [`finance/financial_analysis_swarm.py`](finance/financial_analysis_swarm.py) | Sequential | Data gathering → quantitative analysis → written investment view |
| [`finance/financial_swarm_with_tools.py`](finance/financial_swarm_with_tools.py) | Concurrent | Parallel analysts with search and code execution for live data |
| [`finance/etf_analysis_grid.py`](finance/etf_analysis_grid.py) | Batched grid | Risk and quant analysts crossed with several ETFs, run asynchronously |
| [`finance/crypto_analysis_agent.py`](finance/crypto_analysis_agent.py) | Single agent | Market analysis and risk-adjusted strategy suggestions |

## Marketing

| File | Swarm type | What it does |
|---|---|---|
| [`marketing/marketing_department_swarm.py`](marketing/marketing_department_swarm.py) | Hierarchical | A director delegating to strategy, copy, and channel specialists |

## Supply chain

| File | Swarm type | What it does |
|---|---|---|
| [`supply_chain/supply_chain_swarm.py`](supply_chain/supply_chain_swarm.py) | Hierarchical | Sourcing, logistics, and risk analysis under a coordinator |

## Software engineering

| File | Swarm type | What it does |
|---|---|---|
| [`software_engineering/software_dev_swarm.py`](software_engineering/software_dev_swarm.py) | Hierarchical | A tech lead decomposing a feature across architecture, backend, and QA |

## Hospitality

| File | Swarm type | What it does |
|---|---|---|
| [`hospitality/catering_quote_agent.py`](hospitality/catering_quote_agent.py) | Single agent | Event brief → structured catering plan and quote |

---

## Adapting one of these

1. **Keep the swarm type.** It reflects the dependency structure of the work, which
   usually survives a change of domain.
2. **Rewrite the system prompts first.** They carry most of the domain knowledge.
3. **Then adjust the roster.** Add or drop agents; keep each one's job narrow.
4. **Tune `max_loops` and `max_tokens` last**, once the output is roughly right.
