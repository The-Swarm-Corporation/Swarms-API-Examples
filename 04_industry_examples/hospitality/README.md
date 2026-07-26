# Hospitality Examples

Event and catering workflows.

## Examples

| File | Swarm type | What it does |
|---|---|---|
| [`catering_quote_agent.py`](catering_quote_agent.py) | Single agent | Turns an event brief into a structured catering plan and quote |

## Why a single agent

Menu, headcount, dietary constraints, and price are interdependent — changing the menu
changes the cost, and a dietary restriction can change both. One agent holding all of
it produces a coherent quote; splitting it across specialists would mean reconciling
four partial answers that each assumed something different.

This is the useful counterexample in this folder: **more agents is not the default
better answer.** Reach for a swarm when the work genuinely decomposes, not because the
API supports it.

## Adapting this

1. **Replace the event brief** — guest count, cuisine, budget, and constraints are at
   the top of the file.
2. **Put your actual menu and pricing in the system prompt.** That's what turns a
   plausible quote into your quote.
3. **Ask for structured output** if you're feeding the result into a form or database —
   specify the exact fields you want in the prompt.
4. **If you add a second agent, make it a checker.** A validation pass over pricing and
   dietary coverage is worth more here than a second planner.
