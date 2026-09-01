---
name: backend-service-design
description: Design or review a backend service boundary for validated inputs, explicit authority, invariant-safe writes, reliable asynchronous work, and observable failure modes. Use for API, service, worker, queue, data-access, or integration changes; do not use for a local pure utility.
---

# Backend service design

1. Trace the real caller to the boundary. State who can invoke it, which tenant or resource scope
   applies, and which fields or actions that caller may read or change.
2. Validate and normalise untrusted input at the boundary. Use domain types that make invalid state
   hard to represent; do not pass loosely shaped request data into internal logic.
3. Put each business invariant beside the write that must preserve it. Use a transaction, constraint,
   or conditional write when concurrent callers could otherwise break the invariant.
4. Make retry behaviour explicit for queues, webhooks, and integrations. Define an idempotency key,
   duplicate behaviour, failure visibility, and the point at which a caller may safely retry.
5. Read only the data the boundary needs. Check query shape, pagination, N+1 work, index use, and
   independent work that can be safely parallelised before claiming a performance improvement.
6. Emit enough structured observability to reconstruct an authorised request or job without logging
   secrets or unnecessary personal data. Use errors for failures and traces or timings for latency.
7. Test valid, invalid, unauthorised, concurrent or duplicate, and retry paths that apply. Exercise
   the actual request, job, schema, or integration boundary before hand-off. Use the
   [backend-change template](../../templates/backend-change.md) for the contract and proof.
