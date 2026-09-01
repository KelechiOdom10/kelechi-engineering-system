# Repository adapter checklist

Document only the information that changes engineering decisions in this repository.

- Build, lint, type-check, and focused-test commands.
- Scoped rules for packages or services.
- Data-access and production-safety boundaries.
- Deployment, review, and ownership conventions.
- Known toolchain or generated-code constraints.

Keep credentials, customer information, and stale incident history out of the adapter. Prefer a
focused skill or a hook only after the repository demonstrates a recurring need.
