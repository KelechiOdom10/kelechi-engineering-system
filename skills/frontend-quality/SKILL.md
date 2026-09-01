---
name: frontend-quality
description: Build or review a frontend change for clear state ownership, accessible interaction, responsive rendering, and real-browser verification. Use for component, form, page, or UI-flow changes; do not use for a purely visual asset task.
---

# Frontend quality

1. Identify the user task, the source of each displayed value, and the state transition caused by
   each action. Keep server state, URL state, form state, and temporary UI state separate.
2. Derive render data during rendering. Use an effect only to synchronise with an external system,
   not to compute a value, respond to a click, or mirror props into state.
3. Make every state visible and intentional: loading, empty, partial, error, disabled, success, and
   permission-denied states. Preserve user input and focus across asynchronous transitions when the
   product expects it.
4. Use semantic controls and labels. Check keyboard operation, visible focus, error association,
   touch targets, reduced motion, and the accessible name of every interactive element.
5. Keep component APIs small. Prefer explicit variants or composition when modes have different
   structure or behaviour; do not add flags that make consumers combine incompatible states.
6. Measure before optimising. Avoid unnecessary requests, repeated derived work, unstable list keys,
   and expensive rendering in long lists; do not introduce memoisation without a demonstrated cost.
7. Run the repository's frontend checks and exercise the changed flow in a real browser. Use the
   [frontend-change template](../../templates/frontend-change.md) for the interaction and
   accessibility evidence.
