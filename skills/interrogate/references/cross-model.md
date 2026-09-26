# Cross-model reviewer

The reviewer runs through the *other* harness's CLI so it is a different model family. Start it in the same batch as the lens reviewers as a blocking command with a 10-minute timeout, so it runs in parallel and finishes before you judge. Expect about two minutes.

Always close stdin with `< /dev/null`. Without it, the CLI waits for input that never arrives and hangs.

## From Claude Code: ask Codex

```bash
codex exec --sandbox read-only --ephemeral -C "<repo root>" -o .kelechi/interrogate/codex.md "$(cat .kelechi/interrogate/prompt.txt)" < /dev/null > .kelechi/interrogate/codex.log 2>&1
```

Write the filled prompt to `.kelechi/interrogate/prompt.txt` first. Codex uses Kelechi's configured default model; MCP connection errors in `codex.log` are noise. Its final message lands in `.kelechi/interrogate/codex.md`.

## From Codex: ask Claude Code

```bash
claude -p "$(cat .kelechi/interrogate/prompt.txt)" --model opus --allowedTools "Read,Grep,Glob,Bash(git diff:*),Bash(git show:*),Bash(git log:*)" < /dev/null > .kelechi/interrogate/claude.md
```

## Guardrails

- Read-only in both directions: the sandbox or tool allow-list forbids edits.
- This sends the diff and surrounding code to the other provider. Skip it when a repository adapter says code must not leave its provider, and say that it was skipped.
- If the CLI fails or times out, report the reviewer as missing; never fill its slot with a guess.
