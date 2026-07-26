# Marketing Examples

A marketing department modelled as a hierarchical swarm.

## Examples

| File | Swarm type | What it does |
|---|---|---|
| [`marketing_department_swarm.py`](marketing_department_swarm.py) | Hierarchical | A director delegating to strategy, copy, and channel specialists |

## Why hierarchical

A campaign brief has to be interpreted before it can be split — deciding *what* the
strategy, copy, and channel work should each cover is itself the director's judgment.
That planning step is exactly what a `coordinator` role is for, and the synthesis at
the end is what turns four specialist outputs into one campaign.

A [`ConcurrentWorkflow`](../../03_multi_agent/concurrent_workflow/) would give you four
disconnected opinions on the same brief; a
[`SequentialWorkflow`](../../03_multi_agent/sequential_workflow/) would force an order
that doesn't exist between copy and channel selection.

Mechanics: [`../../03_multi_agent/hierarchical_swarm/`](../../03_multi_agent/hierarchical_swarm/).

## Adapting this

1. **Replace the brief** — the `task` field near the bottom of the file.
2. **Rewrite the director's prompt first.** It sets what the specialists are asked for,
   so it shapes everything downstream.
3. **Change the specialist roster** to match how your team actually splits work — brand,
   performance, lifecycle, and content are common alternatives.
4. **Give the director the stronger model.** It does the planning and the synthesis;
   the specialists can often run cheaper.
