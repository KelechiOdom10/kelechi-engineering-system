# Portability guide

This repository separates personal engineering practice from company-specific knowledge.

## Included

| Material | Why it belongs here |
| --- | --- |
| Kelechi Mode routes, playbooks, and principles | A personal, Codex-native workflow that is useful across repositories. |
| Delegation policy | A general rule: use parallel read-only evidence, retain one owner for decisions and shared writes. |
| PR-writing and review standards | Personal quality and communication preferences. |
| Generic support-investigation skill | A reusable approach with no provider, customer, or production details. |
| Humaans-gated hooks and standard | Personal implementations retained for reference; they do nothing outside the `humaans/humaans` repository. |

## Deliberately excluded

- Production connection strings, credentials, API tokens, and local machine paths.
- Customer names, customer data, support-ticket histories, and incident facts.
- Humaans source code, internal documentation, repository instructions, and service-specific skills.
- The Humaans context memory pack, because its project and support entries are institutional
  knowledge rather than portable personal practice.

## Adapt a new repository

1. Keep `skills/kelechi-mode/` unchanged unless a general lesson requires a change.
2. Add a repository adapter with that project's commands, test paths, and safety boundaries.
3. Keep access procedures outside the portable core and require explicit authorisation at the
   actual external action.
4. Add narrowly scoped hooks only after a real, recurring failure mode justifies one.
5. Move a lesson into the core only when it survives outside one employer and one codebase.

This boundary keeps the repository useful if Kelechi changes jobs without carrying information
that belongs to a previous employer.
