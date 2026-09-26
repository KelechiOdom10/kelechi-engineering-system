# Agents

Three read-only roles. Spawn one only when it adds evidence or an independent lens you would not get inline. Each harness names them differently.

| Role | Claude Code | Codex | Model | Use for | Never |
| --- | --- | --- | --- | --- | --- |
| Explorer | `kelechi:explorer` | `kelechi_explorer` | haiku | mapping code, history, docs, locating owners and tests, large-file scans | edits, design decisions, unverified conclusions |
| Investigator | `kelechi:investigator` | `kelechi_investigator` | sonnet | logs, traces, data, runtime mechanisms, ranked hypotheses | fixes, production mutation, contacting people |
| Comment reviewer | `kelechi:comment-reviewer` | `kelechi_comment_reviewer` | sonnet | judging every comment and suppression a diff adds | editing, or judging code beyond its comments |
| Reviewer | `kelechi:reviewer` | `kelechi_reviewer` | opus | correctness, authorisation, architecture, test-gap review | posting comments, approving, editing the branch |

If a named agent is unavailable, keep the role and its boundary with a built-in agent.

## By route

- **Investigate, perf:** investigator for runtime evidence and explorer for code or history, in parallel when the streams are independent.
- **Review:** one reviewer per independent lens the diff justifies (correctness, security and authorisation, architecture and reader load, tests). Add the explorer only when ownership or history needs separate mapping.
- **Design:** explorer for grounded discovery. Recommendations and trade-offs stay with the primary agent.
- **Fix, feature, refactor:** read-only agents for evidence or review only. The primary agent writes.
- **Babysit:** read-only CI and review triage. Changes and external actions stay with the primary agent.

Brief each agent with file pointers and the exact question, not pasted context. Wait for results, check their evidence, resolve disagreement, and write one conclusion yourself. Model choice changes cost and depth, never authority.
