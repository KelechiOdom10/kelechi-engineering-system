# Review

This route is read-only unless the user explicitly asks for fixes.

1. Establish the intended behavior, review scope, and relevant repository instructions. When the request names a PR, that PR is the scope; do not substitute the local working-tree or `HEAD` diff.
2. Acquire PR metadata, base/head identity, and diff read-only without disturbing a dirty working tree. Inspect the complete diff and surrounding owning code, not isolated lines. Detect truncation, generated files, binaries, and oversized sections; report any scope that could not be reviewed.
3. For a Humaans PR, read `.claude/commands/code-review.md`, state its required hypothesis, and follow its current inline-by-default escalation signals. Treat the selected `.claude/agents/code-reviewer-*.md` files as repository-owned specialist lenses; their Claude model metadata does not constrain Codex.
4. Apply both `humaans-engineering-standard` and `thermo-nuclear-review`. Use `authorization-review` when trust boundaries or caller-supplied identifiers are involved. When the user explicitly requests parallel reviewers, delegate only independent lenses justified by the diff, up to three at once; otherwise follow the repository router's selective escalation.
5. Verify each candidate finding against the code and discard speculative or duplicate claims.
6. Deduplicate the inline review, selected project lenses, personal standard, and thermonuclear pass into one result. Synthesize by severity and actionability, with precise locations and mechanisms. Separate blockers, worthwhile improvements, and dismissed concerns. Do not expose parallel reviewer chatter to the user.
7. Do not post inline comments, submit a review, approve, request changes, or modify code without explicit authority. A specialist's output format applies, while this playbook supplies the authorization and evidence boundaries.
