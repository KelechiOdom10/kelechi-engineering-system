---
name: interrogate
description: Adversarial multi-lens, cross-model review that tries to break a change before it ships. Use for "interrogate", /kelechi:interrogate, "tear this apart", "stress test this", or a second opinion on a risky diff or design.
---

# Interrogate

Several independent reviewers attack the same change from different angles, and one of them runs on a different model family. You are the lead: verify their claims, judge them, and hand back one verdict. The deliverable is the verdict; apply nothing.

Differs from the review playbook: review produces one careful pass; interrogate assumes the change is broken and hunts for how, and treats cross-model agreement as the strongest signal.

## 1. Scope

Resolve the change under attack: a named PR (`gh pr diff`), the branch against its base (`git diff <base>...HEAD`), named files, or a design doc. Write the diff to `.kelechi/interrogate/diff.patch` and list the owning files a reviewer must read around it. Reviewers get pointers to these, not pasted content.

## 2. Intent

Write one paragraph stating what the change is meant to do and for whom, from the request, PR body, commits, and code. If the intent is genuinely unclear, ask before spawning anyone: an attack on the wrong intent is noise.

## 3. Lenses

Read `references/lenses.md`. Pick the lenses the diff's surface justifies, at most three, then add the **cross-model** reviewer.

## 4. Spawn

In one batch, run every reviewer in parallel and in the background:

- Each lens: the read-only reviewer agent (`kelechi:reviewer` in Claude Code, `kelechi_reviewer` in Codex), briefed with `references/reviewer-prompt.md` filled with the intent, the pointers, and that lens.
- Cross-model: the other harness's CLI, following `references/cross-model.md`. Skip it, and say so, when that CLI is missing or a repository adapter forbids sending code to another provider.

## 5. Verify and synthesise

For every candidate finding, open the cited `file:line` yourself and confirm the failure path before it counts. Then:

- Merge duplicates and note which reviewers raised each one.
- **Consensus** (two or more reviewers, especially across model families) is the highest signal.
- A lone finding still counts when you verified it.
- Record explicit disagreements; they shape the verdict.

## 6. Judge

Read `references/verdict.md` and sort every finding into Act on, Consider, Noted, or Dismissed, each with a one-line reason and its reviewers. You are a pragmatic senior engineer, not an aggregator: dismiss wrong or taste-level claims plainly.

## 7. Report

Reply in the verdict format. Delete `.kelechi/interrogate/` afterwards unless Kelechi asks to keep it. Fixing anything is a separate, explicit switch to the fix playbook.
