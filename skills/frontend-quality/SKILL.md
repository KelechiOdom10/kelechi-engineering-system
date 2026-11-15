---
name: frontend-quality
description: Build or review UI for state ownership, visual quality, accessibility, and real-browser proof. Use for component, form, page, or flow changes.
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
7. For every visible change, load and apply the relevant `better-layout`, `better-typography`,
   `better-colors`, `better-ui`, `better-accessibility` and `better-writing` skills while building.
   Follow the engineering standard's frontend reference and the repository's design system.
8. Run frontend checks and drive the changed flow in a real browser. Before handoff, run
   `better-interface` on screenshots of the changed states in light and dark (unsupported themes
   need a reason). Supply the affected screens, not a branch/PR target; it owns screen review.
   Use its coverage and findings table, measure defects against rendered values and tokens,
   and fix HIGH and MEDIUM findings or justify each remaining one with evidence. Retain original
   and corrected screenshots; include before/after images and the findings table in the PR.
   Record missing skills or unavailable rendering as unverified coverage, never a visual pass.
   Use the [frontend-change template](../../templates/frontend-change.md) for interaction proof.

For a feature-wide state audit or retained screenshot catalog, use `ui-sweep`. Use `create-canvas`
when the user needs preserved live alternatives before selecting the implementation.
