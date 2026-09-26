---
name: verify
description: How to prove <product> works end to end - start it, seed it, and drive its key flows. Use before calling a change done or when asked to verify, run, or demo the app.
---

# Verify <product>

## Start

1. `docker compose up -d` for local Postgres.
2. `pnpm --filter @<scope>/db db:migrate && pnpm --filter @<scope>/db db:seed`.
3. `vp dev`, then open <http://localhost:PORT>.

## Test accounts

<Seeded users and how to sign in locally. Never real credentials.>

## Flows

| Flow | Steps | Expected |
| --- | --- | --- |
| <primary action> | <click path> | <observable result> |

Drive each changed flow in a real browser, including its loading, empty, and error states and a narrow mobile width. Add a row here whenever a new flow ships.
