---
name: kelechi-pr-writing
description: Kelechi's pull-request title and description format. Use when creating or editing a PR, or after pushing commits that change what an open PR does.
---

# Kelechi PR writing

If the repository has its own PR skill or template, read it for mechanics. This format wins where the description guidance conflicts.

## Title

- Conventional Commits, scoped in a monorepo: `fix(api): ...`.
- Under 70 characters. States intent, not mechanics.
- No ticket number; tickets go in the branch name or the body.

## Description

An orientation document, not a design archive. A reader who did not write the change should understand in one pass what was wrong or needed, why, what behaviour changes, and how it was verified.

```md
## Context

Two to four sentences: the observed behaviour, its impact, and the cause, in ordinary language.

## Solution

- The important behaviour changes.
- A key design choice or trade-off, only when it helps the reader.

## Test plan

- [x] Verification at the real boundary
- [x] Relevant automated tests
- [x] The important regression case
```

Add `## Demo` with screenshots or a recording for a visual or interaction change.

## Diagram

Add `## Diagram` when the change crosses a package, service, or process boundary, or adds a feature, request, or data flow. Skip it for anything smaller; a diagram on a small PR is noise.

- Draw it with the `pr-lens` skill when installed: the top architecture view first, then one data-flow view if the change has a sequence worth following.
- Attach the rendered SVGs with `gh pr create` or `gh pr edit` and `--attach` (GitHub CLI 2.99 or newer), so the images live on GitHub.
- Never push to a PR Lens canvas unless Kelechi asks for one in this conversation; a canvas stores the architecture on prlens.dev.
- If `architect` left an intended graph in `.kelechi/architect/`, compare it with what was built and state any drift in one line under the diagram. Add risk, rollout, or before/after sections only when they help the reviewer.

## Comprehension budget

- Behaviour and intent; the diff already shows the mechanics.
- About one screen, unless the risk genuinely needs more.
- Explain an unavoidable internal term once, in plain words. Replace shorthand like "load-bearing", "plumbing", or "hydrate" with the concrete behaviour.
- Leave out investigation diaries, file inventories, and code pastes (unless a contract cannot be understood without one).
- No AI attribution. If Kelechi asks for one, name the exact model.

Pass the body through `gh pr create --body-file -` fed by a heredoc, or from a file in the session scratchpad; a fixed `/tmp` path collides with parallel runs.

Re-read the body as someone unfamiliar with the change. If they could not explain the change after one pass, simplify.
