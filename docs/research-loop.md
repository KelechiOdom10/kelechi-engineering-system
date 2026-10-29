# Seeded research before delivery

Use this when the next useful question is still uncertain. A recurring research task can feed a software factory, but discovery and delivery need different contracts.

## Begin with examples of useful evidence

Seed the question with a few strong sources or artifacts and explain what makes them useful. Include a counterexample when it helps distinguish substance from generic advice. Past verified defects, well-designed screens, source implementations and customer symptoms are useful seeds for different tasks.

Do not rank findings by novelty alone. A less popular claim still needs evidence and relevance to the decision.

## Keep a small, editable frontier

Use the [research-state template](../templates/research-state.md). Preserve the goal, authority, output location and budget. The agent may update hypotheses, priorities, rejected leads and the next question as evidence changes. It must not silently expand its permissions, modify its own governing rules or make its exploration the accepted product requirement.

Work on one specific question per cycle. Follow a concrete reference, producer, consumer, disagreement or example rather than asking for a large batch of shallow summaries. Retain the source and the claim it supports, what remains unknown, and the consequence for the current decision. A disproved hypothesis is a useful result.

Use the host's supported continuation events or bounded manual runs. A one-minute recurring heartbeat is one implementation choice, not a quality requirement. Scheduling requires a requested cadence, budget and stop condition. Stop when the decision has enough evidence, the remaining leads do not change it, the budget expires, or authority is missing.

## Curate what survives

The source store preserves retrievals. The working frontier preserves where to look next. The final brief preserves the decision, decisive evidence, disagreements and remaining uncertainty. These are different artifacts; do not make the user read the raw store to learn what matters.

Translate a useful finding into a bounded proposal with its benefit, smallest implementation and a way to test it. Delivery starts from independently stated acceptance, known scope and verification. The delivery collector records actual checks and findings for that change; its hashes do not certify the truth of research.

## Apply the loop

| Task | Useful seed | Focused question | Deliverable |
| --- | --- | --- | --- |
| Review improvement | A verified historical miss and its pre-fix source | Which reachable path invalidated the original assumption? | Reproduction and private replay case, including producer/consumer context |
| Design exploration | An approved screen and real components | Which arrangement best supports the user's primary decision? | Preserved meaningful alternatives, chosen direction and state critique |
| Support investigation | Reported symptom and a known data state | What observation separates the competing explanations? | Verified mechanism, scope and a proposed regression or repair check |
| Tooling maintenance | Repeated setup failure | Can one recipe remove this class of intervention? | A tested script or fixture and proof against the original failure |

Learned lessons should become fixtures, types, tests or scripts where possible. Keep unverified observations separate from durable instructions. Validate a proposed lesson on another relevant case before generalizing it.

This approach adapts [seeded iterative research](https://x.com/snbafana/status/2107884667772830032) to engineering. It does not adopt an unbounded self-editing automation or infer research quality from artifact counts.
