---
name: kickoff
description: Start a new product with Kelechi's kickoff - decisions first, then a walking skeleton. Use for "kickoff", /kelechi:kickoff, starting a new project or repo, or adding a new product surface to an existing repo.
---

# Kickoff

Turn an idea into a small set of durable decisions and a walking skeleton that proves the architecture end to end. Decisions come from Kelechi; facts come from you.

## Modes

Open your first reply with `Mode: new repo` or `Mode: new surface` and one line on why.

- **New repo:** all seven steps.
- **New surface** inside an existing repo: steps 1-3 are scoped to the surface and append to the repo's existing `docs/`; step 4 only decides what the existing stack cannot already express; step 7 builds the first slice inside the repo instead of scaffolding one.

## Rounds

Steps 1-5 are interview rounds. For each round:

1. Research first. Read the repo, the stack reference, and anything Kelechi linked, so no question asks for a fact you could look up.
2. Ask the whole **frontier** at once: every open decision whose prerequisites are settled. Number each question, give the options, and put your recommended answer under it.
3. Wait for answers. Settled answers unblock the next frontier. The round ends when its frontier is empty.
4. Write the step's artifact, then show Kelechi the file path and a one-paragraph summary before starting the next step.

Every durable doc stays about one screen long. It records decisions and why, never the conversation.

## Steps

| # | Step | Reference | Artifact | Done when |
| --- | --- | --- | --- | --- |
| 1 | Promise and principles | `references/product.md` | `docs/product.md` | audience, core job, 3-7 principles, and the "must not become" list are agreed |
| 2 | Agreed language | `references/product.md` | glossary section of `docs/product.md` | every recurring noun has one term and one meaning |
| 3 | Domain model | `references/domain.md` | `docs/domain.md` | identities, lifecycles, invariants, and owners are agreed |
| 4 | Stack forks | `references/stack-forks.md` | `AGENTS.md`, `CLAUDE.md`, `docs/adr/` | every fork is decided and each non-default choice has an ADR |
| 5 | Design direction (UI only) | `references/design.md` | `docs/design.md` | direction, hierarchy, and state rules are agreed, or skipped with a reason |
| 6 | First slice | `references/first-slice.md` | drafted GitHub issues | one thin end-to-end slice is agreed and its issues are drafted |
| 7 | Walking skeleton | `references/skeleton.md` | the repo | the slice runs through every real boundary, checks are green, and it has been driven in a real browser |

Read each reference when its step starts, not before. Open a todo list with the seven steps copied in; mark a skipped step `skip: <reason>`.

## Authority

Creating the repo, files, branches, and local commits proceeds. Creating a GitHub repository, pushing, and opening issues are external actions: draft them, show them, and ask once for the batch.

## Finish

Report the durable docs, the ADRs, the issue links (or drafts), the skeleton's verification evidence, and the next issue to pick up. Delete any `.kelechi/` notes the kickoff produced once their content lives in a durable doc.
