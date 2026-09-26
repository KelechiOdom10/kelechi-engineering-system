---
name: work-validation
description: Verify a code or configuration change before hand-off by running the repository's formatter, lint, type checks, focused tests, and relevant real boundary. Use after implementation or before a pull request; do not use as a replacement for investigation.
---

# Work validation

Validation is part of the change. Read the repository instructions and use the commands they
specify; do not substitute a similar command merely because it is familiar.

1. Identify the changed boundary: formatting, static types, service behaviour, user interaction,
   data migration, queue, permission policy, or external integration.
2. Run the formatter for changed source files. Re-read the diff if it makes changes.
3. Run the affected package's lint and type checks. Use the repository's supported command and
   build configuration.
4. Run the smallest focused automated test that proves the changed behaviour. Add broader checks
   when the boundary, shared contract, or regression risk requires them. A new or changed test
   counts only after you have seen it fail: run it against the pre-change code (`git show
   HEAD:<file>` into a temporary directory) or a one-line sabotage, and record the red result.
5. Keep validation off shared state: migrations, seeds, and tests from a branch, worktree, or clone run
   against a throwaway database (a new database name or container), never the dev database the
   main checkout uses, and leave nothing behind in it. Exercise the real boundary where practical: the request path, UI flow, queue, schema output,
   generated artifact, or integration contract. A passing mock alone is not enough when the
   failure can occur outside the mock. A UI change is always driven in a real browser (the
   available browser tool or Playwright): the changed flow, its loading, empty, and error states,
   and a narrow mobile width.
6. Record each command or check, its result, and any check not run. If a required check cannot run,
   say why and do not present the work as fully verified. A subagent or headless run that had no
   browser does not make a check human-only: drive the available browser tool yourself first.

Use the [validation template](../../templates/work-validation.md) for a concise hand-off record.
