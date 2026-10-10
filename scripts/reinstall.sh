#!/usr/bin/env bash
# Refresh the installed plugins in every local Claude Code and Codex home from this checkout,
# and link every standalone skill in ~/.agents/skills into each Claude home (Codex reads that
# directory itself). Homes default to ~/.claude* and ~/.codex* directories; override with space-separated
# KELECHI_CLAUDE_HOMES or KELECHI_CODEX_HOMES.
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
codex_manifests=("$repo/.codex-plugin/plugin.json" "$repo/adapters/humaans/.codex-plugin/plugin.json")
stamp=$(date -u +%Y%m%d%H%M%S)

homes() { for dir in "$@"; do if [ -d "$dir" ]; then printf '%s\n' "$dir"; fi; done; }
read -r -a claude_homes <<<"${KELECHI_CLAUDE_HOMES:-$(homes ~/.claude ~/.claude[-_]* | tr '\n' ' ')}"
read -r -a codex_homes <<<"${KELECHI_CODEX_HOMES:-$(homes ~/.codex ~/.codex[-_]* | tr '\n' ' ')}"

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
  for home in "${codex_homes[@]}"; do
    echo "Codex: $home"
    CODEX_HOME="$home" codex plugin add kelechi-mode@personal
    codex_plugins=$(CODEX_HOME="$home" codex plugin list 2>/dev/null || true)
    if grep -q "^kelechi-humaans@personal .*installed" <<<"$codex_plugins"; then
      CODEX_HOME="$home" codex plugin add kelechi-humaans@personal
    fi
    mkdir -p "$home/agents"
    cp "$repo"/codex/agents/*.toml "$home/agents/"
  done
else
  echo "codex not found; skipping Codex"
fi

shared_skills=~/.agents/skills
if [ -d "$shared_skills" ]; then
  for home in "${claude_homes[@]}"; do
    mkdir -p "$home/skills"
    for link in "$home"/skills/*; do
      if [ -L "$link" ] && [ ! -e "$link" ] && [[ $(readlink "$link") == *.agents/skills/* ]]; then
        rm "$link"
      fi
    done
    for skill in "$shared_skills"/*/; do
      skill=${skill%/}
      target="$home/skills/$(basename "$skill")"
      if [ -f "$skill/SKILL.md" ] && [ ! -e "$target" ] && [ ! -L "$target" ]; then
        ln -s "$skill" "$target"
        echo "Linked skill $(basename "$skill") into $home"
      fi
    done
  done
fi

if command -v claude >/dev/null; then
  for home in "${claude_homes[@]}"; do
    echo "Claude Code: $home"
    claude_plugins=$(CLAUDE_CONFIG_DIR="$home" claude plugin list 2>/dev/null || true)
    for plugin in kelechi kelechi-humaans; do
      if grep -q "❯ $plugin@kelechi\$" <<<"$claude_plugins"; then
        CLAUDE_CONFIG_DIR="$home" claude plugin uninstall "$plugin@kelechi" >/dev/null
        CLAUDE_CONFIG_DIR="$home" claude plugin install "$plugin@kelechi"
      fi
    done
  done
  echo "Start a new Claude Code session to load the refresh."
else
  echo "claude not found; skipping Claude Code"
fi
