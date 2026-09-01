---
name: kelechi-pr-writing
description: Apply Kelechi's personal Humaans pull-request title and description preferences whenever creating or editing a PR, or after pushing commits to an open PR. Use alongside the repository's create-pr skill; this personal structure wins when its description-format guidance conflicts.
---

# Kelechi PR Writing

Read the repository's `create-pr` skill for shared mechanics, title constraints,
and keeping an open PR synchronized with its diff. Apply this personal format
when its description guidance conflicts with the repository default.

Use `plain-writing` before creating or updating the PR when it is available.

## Title

- Use Conventional Commits style.
- Keep it under 70 characters.
- Describe intent, not mechanics.
- Do not put a ticket number in the title.

## Description

The description is an orientation document, not a design archive. A reader who
did not implement the change should understand, in one pass:

1. What was wrong or needed to change?
2. Why was it happening?
3. What behavior changes now?
4. How was it verified?

Use this default shape:

```md
## Context

Two to four sentences describing the observed behavior, its impact, and the
cause in ordinary language.

## Solution

- The important behavioral changes.
- A key design choice or trade-off, only when it helps the reader.

## Test plan

- [ ] Verification at the real boundary
- [ ] Relevant automated tests
- [ ] Important regression case
```

Add `## Demo` for a visual or interaction change. Add risk, rollout, or
before/after sections only when they materially help the reviewer.

## Comprehension budget

- Focus on behavior and intent; the diff already shows the mechanics.
- Keep the body roughly to one screen unless the risk genuinely requires more.
- Explain unavoidable internal terms once, in ordinary language.
- Do not include an investigation diary, file inventory, generated recap, or
  repeated summary.
- Do not paste code unless an API or data contract cannot be understood without
  it.
- Replace shorthand such as "load-bearing", "plumbing", or "hydrate" with the
  concrete behavior it means.
- Do not add AI attribution unless Kelechi explicitly requests it. If requested,
  name the exact model rather than only the agent.

Re-read the final body as someone unfamiliar with the implementation. If they
cannot explain the fundamental change after one pass, simplify it.
