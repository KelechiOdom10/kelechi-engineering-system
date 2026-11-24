# Lenses

Pick at most three by what the diff touches. Each lens is a hunting brief, not a checklist. When a repository adapter supplies lens briefs, use its run and skip conditions and its hunting brief for that lens in place of the generic row below.

| Lens | Pick when the diff touches | Skip when | Hunt for |
| --- | --- | --- | --- |
| **Correctness** | any logic change (almost always) | docs or copy only | wrong results, unhandled states, off-by-one and boundary values, race conditions, error paths that swallow or mislead, behaviour that differs from the stated intent |
| **Security and data** | auth, sessions, tenant or user ids, request input, queries, secrets, webhooks, file or URL handling | client-only, test-only, or docs-only changes | missing authorisation, caller-controlled identifiers, unvalidated input reaching a trusted type, injection, data leaking across tenants, secrets in logs |
| **Dependents** | a contract other code uses: a function, service, or API signature or result, a schema or column, a queue payload, a tool definition, a package export | new code nothing calls yet; internals behind the same contract | callers outside the diff that now break or need the same update: other services, delete paths, database triggers and views, workers, tool definitions, package consumers |
| **Design and premise** | a new abstraction, API, module, schema, or a second fix to the same area | an additional instance of an established pattern | is this the right change at all; does it fight the domain model or dependency rule; could it be smaller; does it add reader load; is it a patch on a failing premise |
| **Tests** | new or changed tests, or behaviour without any | snapshot-only updates, unless they delete, skip, or weaken assertions | behaviour with no test that would go red; tests that pass with the fix reverted; tests that guard nothing (type-level, mocks returning what they were told); tests coupled to implementation |
| **Operations** | migrations, jobs, queues, retries, config, deploy files | no persisted or deployed state changes | non-idempotent retries, unsafe migrations, missing rollback, old and new versions running side by side mid-deploy, failure invisible in logs, config that differs between environments |

Each finding belongs to one lens. A reviewer that spots another lens's finding names it in one line and does not develop it; the lead decides whether it counts.

Every lens also checks the change against `kelechi-engineering-standard`. The cross-model reviewer gets no single lens: it runs the whole rubric so its independence is intact.
