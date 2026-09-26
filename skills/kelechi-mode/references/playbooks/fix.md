# Fix

1. Make the bug **red**: reproduce it on the same surface it was reported on, or state why reproduction is unavailable. Security and authorisation reproduction uses local or test data; production stays passive and read-only.
2. Observe before theorising. Read the real state (data, network, logs, traces), then add targeted logs or instrumentation where the evidence runs out. Rank falsifiable hypotheses.
3. Confirm the mechanism with direct evidence before editing. A support ticket passes through the investigation checkpoint first.
4. Pin it: write the failing test at the boundary that proves the behaviour, when that test is cheap and faithful. Otherwise name the verification substitute.
5. Fix at the owning boundary with the smallest coherent change. Pause for a design decision if the fix alters architecture or domain semantics. If this is the second fix on the same premise, apply *attack the premise* before writing a third.
6. Remove the temporary instrumentation. Run a simplification pass over every new condition and concept.
7. Re-run the original reproduction until it is **green**, then run `work-validation`.
8. Commit, push, and open a PR within the authority table. Use `kelechi-pr-writing`.

A fix is done when the original reproduction passes. A guard that silences the symptom (a null check, a catch-all, a retry, another prompt rule) is a fix only when the evidence shows the guarded state is legitimate.
