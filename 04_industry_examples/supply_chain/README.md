# Supply Chain Examples

Supply chain analysis as a hierarchical swarm.

## Examples

| File | Swarm type | What it does |
|---|---|---|
| [`supply_chain_swarm.py`](supply_chain_swarm.py) | Hierarchical | Sourcing, logistics, and risk analysis under a coordinator |

## Why hierarchical

Supply chain questions are cross-cutting: a sourcing change alters logistics cost,
which alters the risk profile. Independent specialists would each answer within their
own domain and miss the interactions. The coordinator's job is to hold the whole
picture — decide what to ask each specialist, then reconcile answers that pull against
each other.

Mechanics: [`../../03_multi_agent/hierarchical_swarm/`](../../03_multi_agent/hierarchical_swarm/).

## Adapting this

1. **Replace the scenario** in the `task` field with your network, supplier set, or
   disruption.
2. **Match the specialists to your risk surface.** Sourcing / logistics / risk is a
   reasonable default; regulated or multi-region chains often want compliance and
   customs agents too.
3. **Tell the coordinator to surface tradeoffs, not just synthesize.** The value here is
   in naming what conflicts — the default synthesis tends toward a smooth summary.
4. **Feed it real constraints.** Lead times, capacity limits, and contract terms in the
   task make the output specific instead of generic.
