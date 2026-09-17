---
name: domain-modeling
description: "Model a complex product or backend change around the business domain: clarify language, boundaries, state transitions, and invariants. Use when a new concept crosses services or the current model no longer matches the business; do not use for a local implementation detail."
---

# Domain modeling

Use this skill before implementing a change whose domain model is unclear or crosses a meaningful
boundary.

1. Name the user-visible outcome and collect the terms used by product, users, and existing code.
   Choose one term for each concept and record an explicit glossary when names conflict.
2. Draw the smallest boundary that owns the concept. Identify the data it owns, the invariants it
   enforces, and the callers or neighbouring contexts that only consume its result.
3. Distinguish identities from values. Give an entity a stable identity only when it has a lifecycle;
   represent a value as immutable data when identity would add no behaviour.
4. Define the state transitions and the conditions that permit each one. Keep every invariant in the
   transaction, service, or aggregate that can actually enforce it.
5. Define events or integration contracts only where another boundary needs to react. State delivery,
   ordering, retry, and duplicate behaviour instead of implying them.
6. Prefer a modular monolith and existing domain boundaries until a concrete scale, ownership, or
   deployment constraint proves they are insufficient.
7. Turn the model into tests for the important transitions and invalid states. Use the
   [domain-model template](../../templates/domain-model.md) when the decision needs to outlive the
   current task.

Do not introduce entities, aggregates, repositories, or events as labels for ordinary data access.
They earn their place only when they make an invariant or boundary clearer.
