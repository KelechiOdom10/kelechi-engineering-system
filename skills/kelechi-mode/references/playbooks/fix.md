# Fix

1. Establish a reproducible symptom on the same surface, or explain why reproduction is unavailable. Security and authorization reproduction defaults to local or test data; production evidence must remain passive and read-only.
2. Read current code and relevant history, then rank falsifiable hypotheses.
3. Confirm the mechanism with direct evidence before editing. A support ticket must pass through the investigation checkpoint first. When a specialist mandates a preflight audit, run it before reading the target implementation and separate pre-existing findings from the target issue.
4. Design the smallest coherent fix at the owning boundary. Pause for a design decision if the change alters architecture or domain semantics.
5. Add a failing regression test first when it is cheap and faithful; otherwise state the verification substitute.
6. Implement with one writer, then run a simplification pass. Inspect every new condition and concept; use established language and project idioms where behavior stays the same, and remove obsolete or unverified paths created by the change.
7. Re-run the original reproduction and targeted validation. Use the repository's specialist test and validation skills.
8. Commit, push, update a ticket, or open a PR only when authorized. Use the current PR and writing skills rather than duplicating their rules here.
