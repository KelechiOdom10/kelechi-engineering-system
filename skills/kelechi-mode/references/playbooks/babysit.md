# Babysit

1. Declare the mode before acting. `check` is read-only monitoring. `drive` fixes issues inside the stated objective. State the terminal condition, such as every required check green on the latest head.
2. Read the current branch, PR, review threads, and CI state. An earlier snapshot is stale by default.
3. Triage in order: conflicts, blocking review findings, failing checks, description drift.
4. Assess review-bot comments on their merits. Fix real bugs; dismiss noise with a concrete reason instead of churning code.
5. In `drive`, fix only what the objective covers, verify each change, and push the agent's own branch. Replying to threads, marking ready, and requesting reviewers follow the authority table.
6. Re-read the latest head and required checks before declaring success. Report what changed, what remains, and the next blocking event. Merge and deploy only on an explicit instruction.
