# Healthcare Examples

Clinical and biomedical workflows — the largest example set in this repo, because
healthcare work decomposes naturally across specialists.

> **Not medical software.** These are engineering references demonstrating the API.
> They are not clinical tools, have not been validated, and must not inform diagnosis
> or treatment decisions.

## Start here

[`simple_medical_swarm.py`](simple_medical_swarm.py) — the shortest clinical pipeline
in the folder. Then [`enterprise_medical_demo.py`](enterprise_medical_demo.py) for the
production-shaped version of the same idea.

## Sequential pipelines

Each step depends on the previous one: read the case → reason about it → produce the
output.

| File | What it does |
|---|---|
| [`simple_medical_swarm.py`](simple_medical_swarm.py) | The shortest clinical pipeline here |
| [`medical_swarm.py`](medical_swarm.py) | Intake → differential reasoning → recommendation |
| [`icd10_diagnosis_swarm.py`](icd10_diagnosis_swarm.py) | Lab data → ICD-10 codes → clinical decision support |
| [`icd10_coding_swarm.py`](icd10_coding_swarm.py) | Extract → explain → validate, one agent per step |
| [`medical_coding_swarm.py`](medical_coding_swarm.py) | Coding assistant with tool access for lookups |
| [`biomedical_research_swarm.py`](biomedical_research_swarm.py) | Literature review and synthesis |
| [`enterprise_medical_demo.py`](enterprise_medical_demo.py) | Many specialists, error handling, formatted reporting |
| [`speech_transcript_swarm.py`](speech_transcript_swarm.py) | Clinical review of a speech transcript |

## Concurrent pipelines

Independent specialists reviewing the same case at once.

| File | What it does |
|---|---|
| [`lab_data_concurrent_swarm.py`](lab_data_concurrent_swarm.py) | Parallel interpretation of a lab panel, one agent per marker group |
| [`dermatology_concurrent_swarm.py`](dermatology_concurrent_swarm.py) | Parallel specialist review, then log retrieval |

## Why these swarm types

**Coding and diagnosis are sequential** — you cannot validate a code before it is
extracted, and you cannot explain a diagnosis before you have one. The dependency is
real, so the workflow is a chain.

**Panel interpretation is concurrent** — a lipid specialist and a metabolic specialist
read the same panel without needing each other's conclusions, so they run at once and
the results are combined afterward.

See [`../../03_multi_agent/sequential_workflow/`](../../03_multi_agent/sequential_workflow/)
and [`../../03_multi_agent/concurrent_workflow/`](../../03_multi_agent/concurrent_workflow/)
for the mechanics of each.

## Adapting these

1. **Replace the case data.** Every file has a hardcoded sample case — swap in your own
   input shape first and confirm the pipeline still runs.
2. **Rewrite the system prompts.** They carry the clinical framing; that's what makes
   the output usable.
3. **Keep the agent boundaries.** The split between extraction, reasoning, and
   validation is what makes these auditable — collapsing it into one agent loses that.
4. **Add a validation agent** for anything consequential. `icd10_coding_swarm.py` shows
   the pattern: a final agent whose only job is checking the previous agents' work.
