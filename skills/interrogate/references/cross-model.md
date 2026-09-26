# Cross-model reviewer

The reviewer runs through the *other* harness's CLI so it is a different model family. Run it in the background and read its output file when it finishes.

## From Claude Code: ask Codex

```bash
codex exec --sandbox read-only --ephemeral -C "<repo root>" -o .kelechi/interrogate/codex.md "<filled reviewer prompt>"
```

Codex uses Kelechi's configured default model. Its final message lands in `.kelechi/interrogate/codex.md`.

## From Codex: ask Claude Code

```bash
claude -p "<filled reviewer prompt>" --model opus --allowedTools "Read,Grep,Glob,Bash(git diff:*),Bash(git show:*),Bash(git log:*)" > .kelechi/interrogate/claude.md
```

## Guardrails

- Read-only in both directions: the sandbox or tool allow-list forbids edits.
- This sends the diff and surrounding code to the other provider. Skip it when a repository adapter says code must not leave its provider, and say that it was skipped.
- If the CLI fails or times out, report the reviewer as missing; never fill its slot with a guess.
