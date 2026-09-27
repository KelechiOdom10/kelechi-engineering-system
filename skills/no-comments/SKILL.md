---
name: no-comments
description: "Remove narrating comments and unjustified suppressions, encoding the rest as renames, types, or tests. Use for \"no comments\", /kelechi:no-comments, or before opening a PR."
---

# No comments

Before review, every comment and suppression the change adds must earn its place. Most do not; some point at code that should explain itself. Deletion is the default; encoding is the better outcome.

## Steps

1. **Scope.** The comments and suppressions the diff adds or changes against its base (`git diff <base>...HEAD`, plus uncommitted work). Leave comments the diff did not touch unless Kelechi asks for a wider sweep.
2. **Judge.** Spawn the comment reviewer (`kelechi:comment-reviewer` in Claude Code, `kelechi_comment_reviewer` in Codex) with the diff and its file list, and wait for its table. If sub-agents are unavailable, judge inline by `agents/comment-reviewer.md`'s rules.
3. **Verify.** Check every keep that rests on a claim (a vendor quirk, a constraint, a protected lint rule) against the code or the library source yourself. A claim you cannot confirm is a delete.
4. **Apply deletes.** Remove each deleted comment. Where a deletion leaves a nameless magic value or a block that no longer reads clearly, that is an encode, not a delete.
5. **Apply encodes.** Make the small, behaviour-preserving ones now: a rename, an extracted function, a named constant, a narrower type, the source-type fix that removes a suppression. List larger ones (a new abstraction, a cross-module type) for Kelechi instead of doing them silently.
6. **Validate.** Run `work-validation`. A rename or type change is a code change and gets the same proof.
7. **Commit** separately from the feature: `refactor: remove narrating comments` or `refactor(<scope>): encode <what> in types`, so review can skip it.

A kept comment stays exactly as the diff wrote it; this pass never rewords or reverts one.

## Report

Counts per verdict, each encode applied with its `file:line`, the larger encodes left for Kelechi, and every surviving comment with its keep reason.
