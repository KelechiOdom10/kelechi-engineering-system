#!/usr/bin/env bash
# Validates both plugins in both harnesses, runs every test suite, and checks token budgets.
set -euo pipefail
cd "$(dirname "$0")/.."

claude plugin validate .claude-plugin/plugin.json
claude plugin validate adapters/humaans/.claude-plugin/plugin.json
for dir in skills agents commands adapters/humaans/skills; do claude plugin validate "$dir"; done

validator=~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py
if [ -f "$validator" ]; then
  venv="${TMPDIR:-/tmp}/kelechi-check-venv"
  [ -x "$venv/bin/python" ] || { python3 -m venv "$venv" && "$venv/bin/pip" install -q pyyaml; }
  "$venv/bin/python" "$validator" .
  "$venv/bin/python" "$validator" adapters/humaans
else
  echo "Codex plugin validator not found; skipping Codex validation"
fi

python3 tests/hooks_test.py
python3 tests/digest_test.py
python3 tests/codex_agents_test.py
python3 tests/behaviour_eval.py --check
node --test tests/check_boundaries_test.mjs
python3 tests/budget_test.py
