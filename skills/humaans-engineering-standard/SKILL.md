---
name: humaans-engineering-standard
description: Apply Kelechi's personal engineering bar when reviewing Humaans changes or preparing a Humaans pull request. Adds blocking type-safety checks, proportional touched-legacy cleanup, and conditional frontend, naming, and comment review while composing the repository's own code-reviewer guidance. Do not use for non-Humaans repositories.
---

# Humaans Engineering Standard

Apply this personal layer after reading the current repository instructions. It
augments Humaans' review conventions; it does not copy or replace them.

For a pull-request review, read `.claude/commands/code-review.md` and use its
current hypothesis-first, inline-by-default router. Read only the
`.claude/agents/code-reviewer-*.md` files selected by the changed surface or an
escalation signal. Their checklists are repository guidance even when their
frontmatter names a Claude-specific model.

Pair this standard with `thermo-nuclear-review` for a Humaans PR review when
that skill is available. Return one deduplicated review rather than separate
reports from each lens.

## Review bar

- A blocker must identify a realistic failure, weakened invariant, or
  meaningful maintenance trap introduced by the change.
- Verify the call path and existing project pattern before reporting it.
- Prefer fixing an unsafe source boundary over suppressing the resulting error.
- Separate blockers from worthwhile improvements. Do not hold a PR for taste.
- Enforce no new debt in changed code. Require nearby legacy cleanup only when
  it affects the same invariant or is necessary to make the change safe; do not
  expand a focused change into an unrelated migration.
- Do not report deterministic formatter or linter output as semantic review
  unless the check is disabled, bypassed, or misleadingly green.

Always read [references/type-safety.md](references/type-safety.md) for relevant
TypeScript, ReScript, schema, generated-type, and suppression changes.

When the diff changes UI rendering, styling, interaction, or page wiring, read
[references/frontend.md](references/frontend.md).

When the change introduces or renames services, abstractions, or source
comments, read
[references/naming-and-comments.md](references/naming-and-comments.md).

## Output

Report verified findings first, ordered by impact. State the affected scenario,
failure mechanism, smallest sensible correction, and precise location. Then
list material improvements, residual risks, and dismissed concerns.

If no finding meets the bar, say so plainly. Do not invent findings to make the
review appear thorough.
