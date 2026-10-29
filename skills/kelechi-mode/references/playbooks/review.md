# Review

Read-only unless the user explicitly asks for fixes.

1. Establish the intended behaviour, the scope, and the repository's review instructions. A named PR is the scope; do not substitute the local diff.
2. Acquire PR metadata, base and head, and the full diff without disturbing the working tree. Read the surrounding owning code, not isolated lines. Report anything you could not review: truncation, generated files, binaries.
3. State one hypothesis about where this change's real risk lies before reading for findings.
   Derive acceptance from the request and domain, independently of the implementation's tests.
   Trace the risk through its actual readers, writers and final state, including alternate entry
   points, legacy data, fallback representations and retry gaps where relevant. Challenge expected
   test outputs when the product contract is unsettled.
4. Apply `kelechi-engineering-standard` and any adapter review layer. Add surface skills when the diff touches them: `backend-service-design`, `frontend-quality`, `component-api-design`, `domain-modeling`. Treat caller-supplied identifiers and tenant boundaries as security surface.
5. Check the three drifts: does this diff make any durable doc untrue, change a flow in `.claude/skills/verify/features/` without updating its file, or add tests that guard nothing?
6. For a large or risky diff, run independent lenses in parallel with `kelechi:reviewer` agents, one per lens the diff justifies, at most three.
7. Verify every candidate finding against the code. Drop speculative, duplicate, and formatter-level claims.
8. Report one deduplicated result: blockers, then worthwhile improvements, then dismissed concerns with the reason. Each finding names the scenario, the mechanism, the smallest fix, and the location. If nothing meets the bar, say so.
   Pin the verdict to the reviewed base/head and working state. A disclosed correctness risk is not
   implicitly accepted: fix it, disprove it, or leave it open for an authorized decision. Name checks
   and consumers not exercised. For factory tasks, record the [delivery review](../../../../docs/delivery.md).
9. Posting comments, approving, or requesting changes requires explicit authority.
