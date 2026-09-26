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

Add `## Demo` with screenshots or a recording for a visual or interaction change. Add risk, rollout, or before/after sections only when they help the reviewer.

## Comprehension budget

- Behaviour and intent; the diff already shows the mechanics.
- About one screen, unless the risk genuinely needs more.
- Explain an unavoidable internal term once, in plain words. Replace shorthand like "load-bearing", "plumbing", or "hydrate" with the concrete behaviour.
- Leave out investigation diaries, file inventories, and code pastes (unless a contract cannot be understood without one).
- No AI attribution. If Kelechi asks for one, name the exact model.

Re-read the body as someone unfamiliar with the change. If they could not explain the change after one pass, simplify.
