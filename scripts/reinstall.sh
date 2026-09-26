#!/usr/bin/env bash
# Refresh the installed plugins in Claude Code and Codex from this checkout.
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
codex_manifests=("$repo/.codex-plugin/plugin.json" "$repo/adapters/humaans/.codex-plugin/plugin.json")
stamp=$(date -u +%Y%m%d%H%M%S)

restore() { git -C "$repo" checkout -- "${codex_manifests[@]}"; }
trap restore EXIT

if command -v codex >/dev/null; then
  for manifest in "${codex_manifests[@]}"; do
    python3 - "$manifest" "$stamp" <<'PY'
import json, sys
path, stamp = sys.argv[1], sys.argv[2]
with open(path) as f:
    manifest = json.load(f)
manifest["version"] = manifest["version"].split("+")[0] + "+codex." + stamp
with open(path, "w") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")
PY
  done
  codex plugin add kelechi-mode@personal
  codex_plugins=$(codex plugin list 2>/dev/null || true)
  if grep -q "^kelechi-humaans@personal .*installed" <<<"$codex_plugins"; then
    codex plugin add kelechi-humaans@personal
  fi
else
  echo "codex not found; skipping Codex"
fi

if command -v claude >/dev/null; then
  claude_plugins=$(claude plugin list 2>/dev/null || true)
  for plugin in kelechi kelechi-humaans; do
    if grep -q "❯ $plugin@kelechi\$" <<<"$claude_plugins"; then
      claude plugin uninstall "$plugin@kelechi" >/dev/null
      claude plugin install "$plugin@kelechi"
    fi
  done
  echo "Start a new Claude Code session to load the refresh."
else
  echo "claude not found; skipping Claude Code"
fi
