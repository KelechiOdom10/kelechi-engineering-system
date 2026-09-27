# <Product>

<One paragraph: what it is, who it is for, and the single most important architectural fact.>

## Commands

- `pnpm check`: format, lint, typecheck, and the boundary check. Passes before every commit.
- `vp test`: unit and integration tests. Integration tests need local Postgres (`docker compose up -d`).
- `pnpm --filter @<scope>/db db:seed`: idempotent seed into local Postgres.
- `vp dev`: the app on <port>.

## Architecture

Dependencies point inward. `packages/core` is the domain and imports only zod. `packages/db` is the only package that knows the driver. `packages/api` is the Elysia app; `apps/web` mounts it at `/api` and never imports `db`. `boundaries.json` encodes this and `scripts/check-boundaries.mjs` enforces it.

## Boundary rules

- Parse external data at the edge with zod; trust types inside.
- Type assertions carry a `SAFETY:` comment naming the checked invariant.
- Comments only for a non-obvious why.

## Docs

- `docs/product.md`: promise, principles, agreed language.
- `docs/domain.md`: identities, lifecycles, invariants.
- `docs/design.md`: visual direction and state rules.
- `docs/adr/`: decisions that depart from the defaults.
- Proving behaviour: `.claude/skills/verify/SKILL.md`.
