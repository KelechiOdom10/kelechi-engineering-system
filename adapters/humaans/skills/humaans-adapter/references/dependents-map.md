# Humaans dependents map

Where code outside a diff depends on what the diff changed. Use it for the Dependents lens, `blast-radius`, and any fix that changes a contract. Distilled from `humaans/rowebotic-review-stem` at `5e59b531ffe7`; paths checked against `master`.

Run it when the diff changes a contract other code uses: a service's methods, hooks, results or schema, a DB column, a queue payload, an MCP or AI tool's inputs or outputs, a `packages/**` export, or a new reference from stored data to existing records. Skip it when the diff only adds code nothing calls yet, or changes internals behind the same contract.

Search for callers first, then decide whether each one still works.

| Where | How to find it | What breaks |
| --- | --- | --- |
| Other services | `rg` the service path (`'api/workflow-tasks'`) and its table name; services read each other through service calls and raw SQL or Knex | an aggregator such as `api/tasks`, which collects `api/workflow-tasks` and others |
| Delete paths | the deleted service's `removeRelated` hook (`app/server/hooks/removeRelated.ts`) and delete guards | dependent rows left pointing at nothing: a request type with requests, a custom field referenced in another service's configuration |
| Database | `psql-dev`: `\d <table>` lists triggers and the foreign keys that reference it; `\df+ <fn>` reads a trigger function; `\dv` then `\d+ <view>` reads views | triggers, functions, and views on a renamed or retyped column |
| Queue workers | `app/server/queues/`, including `aiCompanion/` and `workflowAi/` | a worker built for the old payload or result shape; queued jobs enqueued before the deploy |
| MCP and AI tools | `app/server/mcp/tools/`, `app/server/ai/tools/`, `app/server/queues/workflowAi/tools/` | a tool description or schema that now lies about the service it calls |
| Shared packages | every importer of the changed `packages/**` export, including `packages/athena-shared` | widened or narrowed types, callers the diff did not update |

Old and new code run side by side during a deploy: a changed payload, column, or enum must work in both directions until the old version is gone.

Leave bugs inside the diff, permission gaps, style, and duplication to the other lenses.
