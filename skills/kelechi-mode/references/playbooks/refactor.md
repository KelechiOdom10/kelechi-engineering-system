# Refactor

1. State the behavior contract that must remain stable and pin it with tests or observable checks.
2. Describe the target shape and the reader-load or maintenance problem it removes.
3. Prefer deletion, consolidation, and clearer ownership over new abstraction layers.
4. Move in small verifiable steps. Keep the build and targeted tests green between conceptual steps when practical.
5. Migrate callers completely and delete obsolete APIs, compatibility shims, and dead tests unless they are still required.
6. Prove behavioral equivalence at meaningful boundaries.
7. Review whether the final result is genuinely easier to understand; line count alone is not the measure.
