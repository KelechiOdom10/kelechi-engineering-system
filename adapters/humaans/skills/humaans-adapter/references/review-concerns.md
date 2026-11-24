# Humaans review concerns

Lens briefs for a Humaans review. They replace the generic hunting briefs in `interrogate`'s lens table and the `review` playbook's parallel lenses. Use them after the repository's `.claude/commands/code-review.md` router, not instead of it. Distilled from `humaans/rowebotic-review-stem` at `5e59b531ffe7`; the repository files named here own the detail, so read them rather than restating them.

## Guidance files

For each changed file, read every `AGENTS.md` between the repository root and that file. For `app/athena-*` and `packages/athena-shared`, also read `ATHENA.md`. Read them at the PR head (`git show <head>:<path>`), so a guidance file the PR changes is reviewed as changed.

## Lenses

Each finding belongs to exactly one lens. A reviewer that sees another lens's finding names it in one line and moves on.

| Lens | Run when | Skip when | Read | Hunt for, beyond what the read covers |
| --- | --- | --- | --- | --- |
| Correctness | always | never | `code-reviewer-backend-service`, `code-reviewer-backend-platform` | nested service calls that drop the caller's user, company, or transaction; a schema or shared enum whose values, `nullable`, or `maxLength` no longer fit the column's type, NOT NULL, or CHECK constraint; a flag checked in some paths but not others; a retried job or side effect without idempotency; changed behaviour with no test, naming the missing test |
| Security | backend services or hooks, policies, auth, schemas, routes, MCP or AI tools, queries scoped by company or person | client-only, test-only, docs-only | `authorization-review` (with `access-control.md`), `code-reviewer-security` | for each changed policy, hook, schema, or service option: what new data or action it permits, and to whom |
| Dependents | a contract other code uses changes | new code nothing calls yet; internals behind the same contract | [dependents-map.md](dependents-map.md) | callers outside the diff that break or need the same update |
| Tests | a test file, helper, fixture, or setup changes | snapshot-only updates and minor edits, unless they delete, skip, or weaken assertions | `app/server/test/AGENTS.md`, `app/client/test/AGENTS.md`, `packages/e2e/AGENTS.md` | a test that passes with the fix reverted; a permission test without a denied path and a positive control; stubs on Humaans' own services; flakiness with its mechanism and line, reported even when CI was green |
| Performance | `find` queries, joins, filters, sorts; calls or writes in loops or per-record hooks; queue workers; bulk paths; client fetching | a lone read or write by id outside loops and hooks; rendering, copy, types; refactors with the same calls | `code-reviewer-performance` | a new filter, join, or sort with no supporting index (`\di <table>*` via `psql-dev`) |
| Frontend | source under `app/client/src`, `app/athena-client/src`, or `packages/ui` | minor changes | `code-reviewer-frontend-component`, `code-reviewer-frontend-wiring`, `humaans-engineering-standard`'s frontend reference | duplicated or derived state kept in `useState`; effects that derive render data (`remove-unnecessary-use-effects`) |

## Database facts

- Check schema facts with `psql-dev` against the local development database. It is migrated to `master`, has none of the PR's own migrations (read those in the diff), and has no Athena tables.
- If the local database is behind the PR's base, read the newer migrations with `git diff <base> origin/master -- app/server/migrations/` and judge the PR against `master`.
- It holds no production data. Never infer table size or lock time from it.

## Severity

A test that hides a real bug, or removed security or tenancy coverage, is a blocker. Cross-company access, PII exposure, and unauthorised mutation are always reported. Weak or flaky tests and substantive convention breaks are improvements.
