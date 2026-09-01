# Babysit

1. Declare the mode: `check` is read-only monitoring; `drive` may fix authorized issues; `threads-only` coordinates existing tasks without repository changes. State the terminal predicate, such as all required checks succeeding on the latest head SHA.
2. Inspect current branch, PR, review threads, and CI state. Do not assume an earlier snapshot is current.
3. Triage in this order: conflicts, blocking review findings, failing checks, then description or housekeeping drift.
4. Use `rebase-conflicts`, `gh-fix-ci`, `validate-branch`, `create-pr`, and `kelechi-pr-writing` when their triggers apply. Respect any specialist requirement to present evidence or obtain approval before implementation; drive mode does not override it.
5. In drive mode, fix only issues within the authorized objective and verify each change. Posting replies, pushing, or editing the PR still requires current authority.
6. Re-read the latest head and required checks before declaring success. Report what changed, what remains, and the next blocking event. Never merge or deploy unless explicitly asked and authorized.
