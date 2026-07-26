# Software Engineering Examples

Feature planning as a hierarchical swarm — a tech lead decomposing work across
specialists.

## Examples

| File | Swarm type | What it does |
|---|---|---|
| [`software_dev_swarm.py`](software_dev_swarm.py) | Hierarchical | A tech lead decomposing a feature across architecture, backend, and QA |

## Why hierarchical

Breaking a feature into tasks *is* the tech lead's job, and it has to happen before
anyone can work in parallel. The architecture decision constrains the backend work,
which constrains the test plan — so a coordinator who plans first, delegates second,
and reconciles third matches how the work actually flows.

Mechanics: [`../../03_multi_agent/hierarchical_swarm/`](../../03_multi_agent/hierarchical_swarm/).

## Adapting this

1. **Replace the feature description** in `task` with a real ticket or spec.
2. **Add your stack to the prompts.** Generic architecture advice is worth little;
   naming the language, framework, and datastore in each specialist's system prompt
   makes the output actionable.
3. **Add specialists that match your review gates** — security, performance, migrations,
   and API design are common additions.
4. **Give it real constraints.** Existing schema, deploy target, and SLA in the task
   turn plausible plans into usable ones.

## Related

For planning that needs branching rather than a strict hierarchy — say, parallel
investigation of several designs before converging — see
[`../../03_multi_agent/graph_workflow/parallel_fan_out_fan_in.py`](../../03_multi_agent/graph_workflow/parallel_fan_out_fan_in.py).
