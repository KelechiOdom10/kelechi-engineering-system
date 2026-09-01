# Kelechi Engineering System

An evidence-first engineering workflow by Kelechi Odom.

This repository is the portable home for **Kelechi Mode**: an opt-in Codex plugin that routes
engineering work to the appropriate playbook and specialist skills while keeping diagnosis,
verification, judgement, and authority with the engineer.

It contains three layers:

- **Portable core** — Kelechi Mode's routes, playbooks, principles, and model-aware delegation
  boundaries.
- **Personal standards** — review and pull-request writing standards that make changes easier to
  assess and maintain.
- **Adapters and templates** — portable support investigation and work-validation skills, generic
  templates, and a Humaans-gated adapter for the practices that only make sense in that repository.

## How Kelechi Mode works

```text
request
  → select a route
  → gather evidence
  → use the appropriate specialist
  → make the smallest coherent decision or change
  → verify the real boundary
  → communicate the result clearly
```

The plugin covers investigation, fixes, features, refactors, performance, reviews, design,
explanations, PR babysitting, pause, resume, and autonomous work. Its important constraint is
simple: persistence never expands authority.

## Repository map

| Path | Purpose |
| --- | --- |
| `.codex-plugin/plugin.json` | Codex plugin manifest. |
| `skills/kelechi-mode/` | The core router, routes, playbooks, principles, and custom-agent roles. |
| `skills/humaans-engineering-standard/` | Personal Humaans review layer. |
| `skills/kelechi-pr-writing/` | Personal pull-request writing layer. |
| `skills/support-investigation/` | Portable support-investigation workflow. |
| `skills/work-validation/` | Formatter, lint, type, test, and real-boundary validation workflow. |
| `hooks/` | Humaans-gated guardrails; inert outside `humaans/humaans`. |
| `templates/` | Generic templates for support investigations and repository adapters. |
| `docs/` | Design record and portability boundary. |

## Portability boundary

This repository deliberately excludes customer data, credentials, production connection details,
company source code, internal incident notes, and private institutional memory. The Humaans
adapter stays gated to the Humaans repository. Read [the portability guide](docs/PORTABILITY.md)
before adapting this system elsewhere.

## Validate

Run the bundled plugin validator from the Plugin Creator skill against this repository before
installing or publishing a change. For ordinary engineering changes, use `work-validation` after
implementation: format, lint, type-check, run focused tests, and exercise the real boundary.
