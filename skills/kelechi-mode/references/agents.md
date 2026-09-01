# Model-aware agents

Use these personal custom agents when delegation adds material value. If a named agent is unavailable, preserve the role and safety boundary with a built-in agent rather than blocking the task.

| Agent | Model profile | Use for | Do not use for |
| --- | --- | --- | --- |
| `kelechi_explorer` | GPT-5.6 Luna, medium, read-only | Codebase mapping, history, documentation, large-file scans, and locating relevant tests | Editing, final architectural decisions, or unverified conclusions |
| `kelechi_investigator` | GPT-5.6 Terra, high, read-only | Support evidence, logs, traces, runtime mechanisms, and ranked debugging hypotheses | Implementing a fix, production mutation, or external communication |
| `kelechi_reviewer` | GPT-5.6 Terra, high, read-only | TNR, correctness, authorization, architecture, and test-gap review | Posting review comments or modifying the branch |

## Route mapping

- Investigation and performance: use `kelechi_investigator` for runtime evidence and `kelechi_explorer` for current code or history when those streams are independent.
- Review: use `kelechi_reviewer`; add `kelechi_explorer` only when surrounding ownership or history needs separate mapping.
- Design: keep recommendation and tradeoff decisions in the primary Sol agent; use `kelechi_explorer` for grounded code or documentation discovery.
- Fix, feature, and refactor: use read-only agents only for evidence or review. The primary agent writes unless an isolated writer is explicitly needed and available.
- Babysit: delegate read-only CI or review triage when useful; keep changes and external actions with the primary agent.

Use no more agents than the evidence streams justify. Wait for relevant results, inspect their evidence, resolve disagreement, and synthesize one conclusion. Model selection changes cost and depth; it does not change authorization.
