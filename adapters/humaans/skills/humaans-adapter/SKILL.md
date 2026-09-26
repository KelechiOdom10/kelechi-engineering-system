---
name: humaans-adapter
description: Humaans repository adapter for Kelechi Mode. Load first under Kelechi Mode when the git origin is humaans/humaans; supplies the repository's specialists, review router, production-safety rules, and PR conventions.
---

# Humaans adapter

Applies only when `git remote get-url origin` is `humaans/humaans`. Elsewhere, stop and use the generic workflow.

Load `humaans-context` before relying on remembered preferences or history. Memory is a lead; current source and the request are the truth.

## Specialists by route

| Route | Humaans specialists |
| --- | --- |
| Investigate | `support` for any `SUP-` ticket (it owns the production-replica procedure), `humaans-context`; then `gcloud-logs`, `honeycomb-traces`, or `authorization-review` only when the evidence calls for them |
| Fix | investigation specialists first, then `unit-test-developer`, `frontend-developer`, `rescript-developer`, `mcp-developer`, `authorization-review` |
| Feature | the relevant developer and test skills |
| Performance | `honeycomb-traces`, `node-debugger`, `fullstack-debugger` |
| Review | `.claude/commands/code-review.md` router, `humaans-engineering-standard`, and `thermo-nuclear-review` when available |
| Babysit | `gh-fix-ci`, `create-pr`, `validate-branch`, `rebase-conflicts`, with `kelechi-pr-writing` |
| Explain, resume | `humaans-context` for history and prior work |

## Rules

- `psql-dev` is for local dev and test databases only. Production investigation always goes through `support`.
- For a PR review, read `.claude/commands/code-review.md`, state its required hypothesis, and follow its inline-by-default escalation. The selected `.claude/agents/code-reviewer-*.md` files are repository review lenses in either harness.
- The repository uses pnpm and oxfmt; the plugin's generic hooks already enforce both.
- PR titles never carry `FIVE-`, `SUP-`, or `HUMV-` ticket ids.
