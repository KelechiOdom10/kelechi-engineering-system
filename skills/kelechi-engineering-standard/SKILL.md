---
name: kelechi-engineering-standard
description: Kelechi's engineering standard - types, architecture, testing, frontend, comments, AI features, default stack. Use when writing, reviewing, or planning code in Kelechi Mode, or when asked for his standard or stack.
---

# Kelechi engineering standard

A personal layer on top of the repository's own rules. Where a repository already decides something (its stack, formatter, layout), the repository wins; these rules fill the gaps and set the review bar.

## Read by surface

Read every reference whose trigger the work touches. Each is short.

| Reference | Read when the work touches |
| --- | --- |
| [type-safety](references/type-safety.md) | types, schemas, casts, suppressions, external data |
| [architecture](references/architecture.md) | modules, boundaries, APIs, errors, dependencies |
| [testing](references/testing.md) | writing, changing, keeping, or reviewing a test |
| [frontend](references/frontend.md) | UI rendering, state, forms, styling, interaction |
| [naming-and-comments](references/naming-and-comments.md) | new names, renamed concepts, source comments |
| [ai-features](references/ai-features.md) | LLM calls, prompts, tools, agents inside the product |
| [stack](references/stack.md) | starting a project, choosing a library, commits and PRs |
| [structural-review](references/structural-review.md) | reviewing a diff's structure, abstractions, or file size; a "thermo-nuclear" review |

## Review bar

- A blocker names a realistic failure, a weakened invariant, or a real maintenance trap introduced by the change, verified against the call path.
- Fix the unsafe source boundary instead of suppressing the error it causes.
- No new debt in changed code. Require nearby legacy cleanup only when it shares the invariant or makes the change safe.
- Formatter and linter output is not semantic review, unless a check is disabled, bypassed, or misleadingly green.
- Taste is not a blocker. Say so and move on.

Report verified findings by impact: scenario, mechanism, smallest correction, location. Then improvements, residual risks, dismissed concerns. When nothing meets the bar, say so plainly.
