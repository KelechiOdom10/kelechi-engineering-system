# Lenses

Pick at most three by what the diff touches. Each lens is a hunting brief, not a checklist.

| Lens | Pick when the diff touches | Hunt for |
| --- | --- | --- |
| **Correctness** | any logic change (almost always) | wrong results, unhandled states, off-by-one and boundary values, race conditions, error paths that swallow or mislead, behaviour that differs from the stated intent |
| **Security and data** | auth, sessions, tenant or user ids, request input, queries, secrets, webhooks, file or URL handling | missing authorisation, caller-controlled identifiers, unvalidated input reaching a trusted type, injection, data leaking across tenants, secrets in logs |
| **Design and premise** | a new abstraction, API, module, schema, or a second fix to the same area | is this the right change at all; does it fight the domain model or dependency rule; could it be smaller; does it add reader load; is it a patch on a failing premise |
| **Tests** | new or changed tests, or behaviour without any | behaviour with no test that would go red; tests that guard nothing (type-level, mocks returning what they were told); tests coupled to implementation |
| **Operations** | migrations, jobs, queues, retries, config, deploy files | non-idempotent retries, unsafe migrations, missing rollback, failure invisible in logs, config that differs between environments |

Every lens also checks the change against `kelechi-engineering-standard`. The cross-model reviewer gets no single lens: it runs the whole rubric so its independence is intact.
