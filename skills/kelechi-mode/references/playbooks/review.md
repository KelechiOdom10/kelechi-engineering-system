# Review

Read-only unless the user explicitly asks for fixes.

1. Establish the intended behaviour, the scope, and the repository's review instructions. A named PR is the scope; do not substitute the local diff.
2. Acquire PR metadata, base and head, and the full diff without disturbing the working tree. Read the surrounding owning code, not isolated lines. Report anything you could not review: truncation, generated files, binaries.
3. State one hypothesis about where this change's real risk lies before reading for findings.
4. Apply `kelechi-engineering-standard` and any adapter review layer. Add surface skills when the diff touches them: `backend-service-design`, `frontend-quality`, `component-api-design`, `domain-modeling`. Treat caller-supplied identifiers and tenant boundaries as security surface.
5. Check the two drifts: does this diff make any durable doc untrue, and does it add tests that guard nothing?
6. For a large or risky diff, run independent lenses in parallel with `kelechi:reviewer` agents, one per lens the diff justifies, at most three.
7. Verify every candidate finding against the code. Drop speculative, duplicate, and formatter-level claims.
8. Report one deduplicated result: blockers, then worthwhile improvements, then dismissed concerns with the reason. Each finding names the scenario, the mechanism, the smallest fix, and the location. If nothing meets the bar, say so.
9. Posting comments, approving, or requesting changes requires explicit authority.
