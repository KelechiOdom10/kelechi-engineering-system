# Working state and docs

Docs are sorted by how long they stay true.

| Kind | Examples | Home |
| --- | --- | --- |
| Durable why | product principles, agreed language, domain model, ADRs, vendor quirks | `docs/` in the repo, about one screen each, linked by one line from `CLAUDE.md` or `AGENTS.md` |
| Rules | commands, boundary rules, conventions | `CLAUDE.md` / `AGENTS.md`, or better, a lint rule, type, or script |
| Working state | handoffs, plans, investigation notes, audits, review drafts | `.kelechi/` in the repo root, never committed |
| Delivery | roadmap, phases, status | GitHub issues and milestones only |

## `.kelechi/`

Create it only when work spans sessions: a pause, a long autonomous run, an investigation to return to. Branch plus PR description is the handoff for everything else.

On first use, append `.kelechi/` to `.git/info/exclude` so it stays out of git without touching `.gitignore`.

Every file starts with provenance frontmatter:

```yaml
---
kind: handoff | plan | investigation | audit
branch: <branch>
head: <short sha>
created: <YYYY-MM-DD>
status: active | consumed
---
```

## Staying true

- **Resume** compares `branch` and `head` against the current state. If the branch merged or the head moved, say so and re-verify every claim before relying on it.
- **Consumed means deleted.** Delete a handoff once resume has picked it up.
- **Promote or delete at the finish.** When work reaches a PR, decide each `.kelechi/` file: promote the lasting part (a decision to an ADR, a vendor quirk to `docs/`) or delete it.
- **Durable docs change with the code.** A diff that makes a durable doc untrue updates that doc in the same PR. Review checks this.
