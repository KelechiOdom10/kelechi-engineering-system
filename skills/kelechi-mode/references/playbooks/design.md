# Design

1. Ground the problem in current code and, when motivation matters, relevant history.
2. Name the users, callers, data, constraints, failure modes, and decisions that are actually open.
3. Start from caller-facing behavior and the domain model. Produce two or three viable shapes when the tradeoff is real.
4. Use `research` for an unsettled evidence-backed choice; settle assumptions with read-only probes or the prototype playbook. Use `create-canvas` for requested live alternatives, preserving the approved baseline.
5. Compare options on complexity, ownership, migration, authorization, observability, and verification.
6. Recommend one shape and record unresolved decisions. Durable decisions become an ADR; working notes go to `.kelechi/`. Use `grilling` only when the user asks to be grilled.
7. Do not implement merely because the design is ready; implementation requires that authority in the request.
