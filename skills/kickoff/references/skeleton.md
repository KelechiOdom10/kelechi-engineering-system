# Step 7: walking skeleton

Build the first slice through every real boundary, with the checks that protect the architecture, and nothing more. No UI kit sweep, no speculative packages.

## Target layout

```text
apps/web          TanStack Start: routes, UI, and the /api/$ route that mounts the API
packages/core     domain: schemas, plans, pure logic; imports zod only
packages/db       Drizzle schema, migrations, queries; the only package that knows the driver
packages/api      Elysia app built from feature modules; exports `type App`
scripts/          check-boundaries.mjs and seed scripts
```

Adapt the layout when the ADRs say so (a separate Bun API, no database). A new surface builds inside the existing layout.

## Build order

Commit after each unit with a Conventional Commit; each commit leaves `check` green.

1. **Scaffold.** `vp create vite:monorepo --directory <name> --no-interactive`, then `vp create @tanstack/start --directory apps/web`. Read each command's `--help` first; if a template's output differs from the target layout, move it into the layout rather than bending the layout. Pin the toolchain: a `.node-version` file and a `packageManager` field in the root `package.json` (CI reads both).
2. **Core.** The slice's schemas and pure logic in `packages/core`, with a unit test for the invariant the slice exercises.
3. **Database.** The slice's tables in `packages/db`, local Postgres through Docker Compose, a migration, and an idempotent seed.
4. **API.** The Elysia app in `packages/api` as feature modules, parsing every body with the core schemas. Mount it in Start:

   ```ts
   // apps/web/src/routes/api/$.ts
   import { createFileRoute } from "@tanstack/react-router";
   import { api } from "@<scope>/api";

   const handle = ({ request }: { request: Request }) => api.fetch(request);

   export const Route = createFileRoute("/api/$")({
     server: { handlers: { GET: handle, POST: handle, PUT: handle, PATCH: handle, DELETE: handle } },
   });
   ```

   Give the web app one Eden client that calls the Elysia instance directly on the server and over HTTP in the browser (`createIsomorphicFn` from `@tanstack/react-start`). Confirm both APIs against the installed versions.
5. **Web.** The slice's routes, following the rendering map. The authenticated subtree is a layout route with `ssr: false`. Loading, empty, and error states exist from the first commit.
6. **Auth,** only if the slice needs it: better-auth mounted under the API, sessions checked in the API, never only in the UI.
7. **Boundaries.** Copy `../assets/check-boundaries.mjs` to `scripts/`, write `boundaries.json` from `../assets/boundaries.example.json` (allow-list the core; deny-list the adapters), and make the root `check` script run it after `vp check`.
8. **Integration test.** One test that calls the real `/api` route against local Postgres and asserts the slice's outcome.
9. **CI.** `.github/workflows/ci.yml` from `../assets/ci.yml`.
10. **Deploy config.** Workers config following Start's current Cloudflare guide. Run it once through `wrangler dev` and hit `/api/health`; this is the Elysia-on-Workers guardrail.
11. **Verification skill.** `.claude/skills/verify/SKILL.md` from `../assets/verify-skill.template.md`, with a one-line pointer to it in `AGENTS.md` so Codex finds it too.

## Proof

The skeleton is done when all of these pass, with their output reported:

- `check` (format, lint, types, boundaries) and `vp test`.
- The integration test against local Postgres.
- `wrangler dev` answering `/api/health`.
- The slice driven in a real browser: the primary action, its loading, empty, and error states, and a narrow mobile width.
