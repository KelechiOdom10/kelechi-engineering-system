# Design

1. Ground the problem in current code and, when motivation matters, relevant history.
2. Name the users, callers, data, constraints, failure modes, and decisions that are actually open.
3. Start from caller-facing behavior and the domain model. Produce two or three viable shapes when the tradeoff is real. If the user asks to be grilled before receiving a recommendation, complete that decision dialogue first.
4. Test uncertain assumptions with small read-only probes or disposable prototypes.
5. Compare options on complexity, ownership, migration, authorization, observability, and verification.
6. Recommend a shape and record unresolved decisions. Use `grill-me` or `grill-with-docs` only when the user explicitly asks to be grilled.
7. Do not implement merely because the design is ready; implementation requires that authority in the request.
