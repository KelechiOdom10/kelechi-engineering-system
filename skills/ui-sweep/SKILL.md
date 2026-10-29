---
name: ui-sweep
description: Inspect a web feature across its reachable states, widths, roles and themes, retaining an inspected screenshot catalog and evidenced defects. Use for a UI sweep, feature-state audit or screenshot catalog; read-only product assessment unless fixes are requested.
---

# UI sweep

Produce a local catalog of actual UI evidence. Ref MCP, external uploads and automatic PR publication are not required. A sweep request authorizes relevant local browser work; a passing screenshot is not permission to change the product.

1. Scope the feature from the request, ticket or changed paths. Read repository/browser instructions and the existing verification recipe. Inventory entry points, user actions, data sources, roles, flags and important states before capture. Use [the sweep record](../../templates/ui-sweep.md). Reuse its existing fixture/sign-in recipe on later runs.
2. Establish checkout/head, serving process/build, ports, fixture and test account identity. Use isolated allowed test state. Never seed or repair shared/production data, impersonate a customer or stop an existing process merely to enable a screenshot. Load repository adapters; Humaans server tests use their own runner and local isolation rules. If a boundary is unavailable, record the specific blocked rows and continue useful independent checks.
3. Cover the normal task plus meaningful loading, empty, partial, error, disabled, permission and success states. Choose representative desktop and phone widths (default 1440 and390 pixels), supported themes and roles from the feature's risks; do not invent unsupported themes or an exhaustive Cartesian matrix. Mark impossible/not-applicable cases with reasons. Distinguish seeded/mocked states from actual integration paths.
4. Capture the real application with the available browser tooling. Save one PNG per distinct capture with stable descriptive IDs. Open every PNG and inspect it; a successful capture command alone is insufficient. Record state, dimensions, role/theme, fixture, source/build identity, reproduction and actual image path. Never manufacture screenshots, report an image as inspected without viewing it, or claim motion/device behavior from a still.
5. Exercise the associated interactions, keyboard/focus, error recovery and persistence where relevant. Inspect hierarchy, readability, spacing, clipping and reference fidelity as well as behavior. For design exploration, use `create-canvas`; a sweep evaluates the chosen result rather than silently redesigning it.
6. Retain the inventory, captured images and a local catalog linking each image, its caption and observations. Include defects by severity with reachable reproduction, expected/actual result, evidence and suspected boundary; uncertain causes remain hypotheses. Record captured-and-inspected, blocked and not-applicable separately, with honest coverage totals. Do not upload customer screenshots or publish catalogs without authorization.
7. Default to an assessment. When fixes are requested, use the normal fix route, regression proof and fresh sweep of affected states; keep the original images. A good-looking mock is not proof that a workflow or document token resolves correctly. Clean up only resources this run created and retain reusable recipes/evidence. Report what was exercised, missing proof and next blocking event.

Adapted from [Ref's ui-sweep](https://github.com/ref-tools/marketplace/blob/main/plugins/ref-skills/skills/ui-sweep/SKILL.md), replacing service-coupled publication with local evidence and existing host tools.
