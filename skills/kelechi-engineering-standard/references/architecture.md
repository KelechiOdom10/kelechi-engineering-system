# Architecture

## Boundaries

- **Dependencies point inward.** The domain core imports its schema library and nothing else: no drivers, framework, or UI. Adapters (API, web, workers, db) depend on the core, never the reverse.
- **The browser cannot bypass the API.** The web app never imports the database package or drivers.
- **Enforce the rule in code.** A monorepo carries a boundary check (an allow/deny import map run in `check`), not a paragraph asking people to behave.
- **Request contracts are hand-written.** Never expose generated database types (Prisma `WhereInput`, raw table shapes) as API input. A request schema states exactly what the caller may ask for; anything else is an authorisation hole and couples the API to the table layout.

## Layout

- **Feature folders.** `modules/<feature>/` holds the feature's route, handler, service, schema, and tests together. Files are named by role: `<feature>.route.ts`, `<feature>.handler.ts`, `<feature>.schema.ts`.
- **Pipelines read as pipelines.** When a concept flows through stages, name files by stage (`plan.ts`, `compiler.ts`, `payload.ts`) and wire variants through a registry.
- **One home per concept.** Shared pure logic that server and client must agree on lives once, in the core.

## Functions

- Positional parameters for one or two arguments. An object parameter at three or more, or when two arguments share a type and could be swapped.
- Business logic stays pure; I/O lives at the edges and is passed in.

## Errors

- **Throw typed errors, map them once at the edge.** Domain and vendor failures are `Error` subclasses with a meaningful name (`RateLimitedError`, `NotConfiguredError`). One edge handler maps them to HTTP status, user messages, and logs.
- A `catch` either handles a specific known error or rethrows. Catch-all swallowing is a defect.
- **Effect earns its place** where retries, caching, resource lifetimes, and composition of failure actually matter, typically an external API client layer. Plain async code elsewhere.

## Reliability

- Operations that can be retried converge to the same end state: idempotency keys for webhooks, jobs, and imports.
- Invariants sit beside the write that must preserve them: a transaction, a constraint, or a conditional write when concurrent callers exist.
- Log enough structured context to reconstruct a request or job, without secrets or unnecessary personal data.
