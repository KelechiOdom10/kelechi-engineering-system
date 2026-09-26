# Portability guide

This repository separates personal engineering practice from company-specific knowledge.

## Included

| Material | Why it belongs here |
| --- | --- |
| Kelechi Mode routes, playbooks, and principles | A personal workflow, shared by Claude Code and Codex, useful across repositories. |
| Kelechi engineering standard | Personal type, architecture, testing, frontend, and stack preferences that survive a job change. |
| Delegation policy | A general rule: use parallel read-only evidence, retain one owner for decisions and shared writes. |
| PR-writing and review standards | Personal quality and communication preferences. |
| Generic support-investigation skill | A reusable approach with no provider, customer, or production details. |
| Work-validation skill | A reusable proof standard: format, lint, type-check, focused test, and real boundary. |
| Domain, frontend, and backend skills | Reusable decision frameworks that defer exact technology and commands to the repository adapter. |
| Portable hooks | Guardrails that detect each repository's toolchain; nothing is gated to one employer. |
| Humaans adapter (`adapters/humaans/`) | A separate plugin with the Humaans routing and review layer; installed only on a Humaans machine. |

## Deliberately excluded

- Production connection strings, credentials, API tokens, and local machine paths.
- Customer names, customer data, support-ticket histories, and incident facts.
- Humaans source code, internal documentation, repository instructions, and service-specific skills.
- The Humaans context memory pack, because its project and support entries are institutional
  knowledge rather than portable personal practice.

## Adapt a new repository

1. Keep `skills/kelechi-mode/` unchanged unless a general lesson requires a change.
2. Add an adapter plugin under `adapters/<company>/` with a `<company>-adapter` skill whose description names the repository it applies to. Kelechi Mode loads it first.
3. Put in it that project's formatter, lint, type, focused-test, and
   production-safety commands.
4. Keep access procedures outside the portable core and require explicit authorisation at the
   actual external action.
5. Add narrowly scoped hooks only after a real, recurring failure mode justifies one.
6. Move a lesson into the core only when it survives outside one employer and one codebase.

This boundary keeps the repository useful if Kelechi changes jobs without carrying information
that belongs to a previous employer.
