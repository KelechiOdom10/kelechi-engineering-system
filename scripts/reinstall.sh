#!/usr/bin/env bash
# Refresh the installed plugins in every local Claude Code and Codex home from this checkout,
# and link every standalone skill in ~/.agents/skills into each Claude home (Codex reads that
# directory itself). Homes default to ~/.claude* and ~/.codex* directories; override with space-separated
# KELECHI_CLAUDE_HOMES or KELECHI_CODEX_HOMES.
# OpenCode and Antigravity have no plugin for this system, so they read the checkout directly: OpenCode
# through skill and command links in ~/.config/opencode, Antigravity through ~/.gemini/config/skills.json.
# Override those folders with KELECHI_OPENCODE_CONFIG or KELECHI_ANTIGRAVITY_CONFIG.
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
    if grep -q "^kelechi-humaans@personal " <<<"$codex_plugins"; then
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

skill_roots=("$repo/skills")
for adapter in "$repo"/adapters/*/; do
  if grep -qs "\"kelechi-$(basename "$adapter")\"" ~/.agents/plugins/marketplace.json; then
    skill_roots+=("${adapter}skills")
  fi
done
skills=()
for root in "${skill_roots[@]}"; do skills+=("$root"/*/); done

opencode_config=${KELECHI_OPENCODE_CONFIG:-~/.config/opencode}
if [ -d "$opencode_config" ]; then
  echo "OpenCode: $opencode_config"
  mkdir -p "$opencode_config/skills" "$opencode_config/commands"
  for link in "$opencode_config"/skills/*; do
    if [ -L "$link" ] && [ ! -e "$link" ] && [[ $(readlink "$link") == "$repo"/* ]]; then
      rm "$link"
    fi
  done
  for skill in "${skills[@]%/}"; do
    name=$(basename "$skill")
    stale="$opencode_config/skill/$name"
    if [ -d "$stale" ] && [ ! -L "$stale" ]; then
      mkdir -p "$opencode_config-skill-backup-$stamp"
      mv "$stale" "$opencode_config-skill-backup-$stamp/"
      echo "Moved stale copy of $name to $opencode_config-skill-backup-$stamp"
    fi
    target="$opencode_config/skills/$name"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "Skipping $name: $target is not a link"
      continue
    fi
    ln -sfn "$skill" "$target"
  done
  ln -sfn "$repo/commands" "$opencode_config/commands/kelechi"
fi

antigravity_config=${KELECHI_ANTIGRAVITY_CONFIG:-~/.gemini/config}
if [ -d "$antigravity_config" ]; then
  echo "Antigravity: $antigravity_config"
  python3 - "$antigravity_config/skills.json" "$repo" "$shared_skills" "${skill_roots[@]}" <<'PY'
import json, os, sys
path, repo, shared, roots = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
manifest = {}
if os.path.exists(path):
    with open(path) as f:
        manifest = json.load(f)
owned = lambda entry: entry.get("path", "").startswith(repo + "/") or entry.get("path") == shared
entries = [entry for entry in manifest.get("entries", []) if not owned(entry)]
if os.path.isdir(shared):
    entries.append({"path": shared})
entries += [{"path": root} for root in roots]
manifest["entries"] = entries
with open(path, "w") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")
PY
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
