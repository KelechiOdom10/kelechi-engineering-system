# kelechi-engineering-system

Kelechi Mode: one plugin read by both Claude Code (`.claude-plugin/`) and Codex (`.codex-plugin/`). Skills in `skills/` are shared by both harnesses; write them harness-neutral.

## Commands

- `./scripts/check.sh`: validates both plugins in both harnesses, runs every test suite, and checks token budgets. Green before every PR.
- `./scripts/reinstall.sh`: refreshes the installed plugin in every local Claude Code and Codex home (`~/.claude*`, `~/.codex*`) from this checkout, copies the Codex agents, and links every standalone skill in `~/.agents/skills` into each Claude home.

## Changing a skill

1. Check every command, flag, and API the skill names against `--help` or the installed package before writing it down.
2. Run the skill headless on a throwaway target in both harnesses (`claude -p`, and `codex exec ... < /dev/null`). Review-type skills get planted bugs to find.
3. Check the run's claims against the files it produced, not its report.
4. Fold fixes in as their own commit, then `./scripts/check.sh`. Installation changes local agent configuration; follow the active session's authorization before `./scripts/reinstall.sh`.
5. When a skill or agent description changes, run `python3 tests/trigger_eval.py` (real model calls) and add a case for any new skill to `tests/trigger_cases.json`. It loads this checkout with session-local `--plugin-dir`; no reinstall is needed to evaluate unapproved source. Verify the installed version separately after an authorized refresh.

A budget failure in `check.sh` means prune something weaker, or raise the budget in the same PR with a reason.
