#!/usr/bin/env bash
# Set up Beacon (https://beacon.sh) in every local Claude Code and Codex home, found as reinstall.sh
# finds them, then run reinstall.sh so its skills reach every Claude home. Defaults to Beacon Cloud in
# metadata-only mode with the last 30 days of sessions; --local keeps everything on this machine,
# --standard uploads full session content, --no-backfill uploads new sessions only. Leaves an
# administrator-managed Beacon alone.
set -euo pipefail

repo=$(cd "$(dirname "$0")/.." && pwd)
plan=cloud privacy=metadata-only backfill=()
for arg in "$@"; do
  case "$arg" in
    --local) plan=local ;;
    --standard) privacy=standard ;;
    --no-backfill) backfill=(--no-backfill) ;;
    *) echo "usage: $0 [--local] [--standard] [--no-backfill]" >&2; exit 2 ;;
  esac
done

tap_formula() { echo "$(brew --repository)/Library/Taps/asymptote-labs/homebrew-tap/Formula/$1.rb"; }

# Homebrew refuses tap formulae when the Command Line Tools are outdated, though nothing is compiled.
# Fall back to the same verified release archives the formulae download, installed under ~/.local.
install_from_archives() {
  [ "$(uname -s)-$(uname -m)" = Darwin-arm64 ] || { echo "Archive fallback covers Apple Silicon only; see https://docs.beacon.sh/cli/manual-install" >&2; exit 1; }
  local work version archive vector_url vector_sha
  work=$(mktemp -d)
  version=$(sed -nE 's/.*releases\/download\/v([0-9.]+)\/beacon_.*darwin_arm64.*/\1/p' "$(tap_formula beacon)")
  archive=beacon_${version}_darwin_arm64.tar.gz
  curl -fsSL -o "$work/$archive" "https://github.com/asymptote-labs/agent-beacon/releases/download/v$version/$archive"
  curl -fsSL -o "$work/checksums.txt" "https://github.com/asymptote-labs/agent-beacon/releases/download/v$version/checksums.txt"
  (cd "$work" && grep "  $archive$" checksums.txt | shasum -a 256 -c -)
  vector_url=$(grep -A1 -m1 'arm64-apple-darwin' "$(tap_formula beacon-vector)" | sed -nE 's/.*url "([^"]+)".*/\1/p')
  vector_sha=$(grep -A2 -m1 'arm64-apple-darwin' "$(tap_formula beacon-vector)" | sed -nE 's/.*sha256 "([0-9a-f]+)".*/\1/p')
  curl -fsSL -o "$work/vector.tar.gz" "$vector_url"
  echo "$vector_sha  $work/vector.tar.gz" | shasum -a 256 -c -
  mkdir -p "$work/beacon" "$work/vector" ~/.local/bin ~/.local/libexec/beacon-vector
  tar -xzf "$work/$archive" -C "$work/beacon"
  tar -xzf "$work/vector.tar.gz" -C "$work/vector"
  install -m 0755 "$work"/beacon/beacon "$work"/beacon/beacon-hooks "$work"/beacon/beacon-otelcol ~/.local/bin/
  install -m 0755 "$(find "$work/vector" -path '*/bin/vector' -type f)" ~/.local/libexec/beacon-vector/vector
  export PATH="$HOME/.local/bin:$PATH"
}

if brew list beacon >/dev/null 2>&1; then
  brew update && brew upgrade beacon
elif ! command -v beacon >/dev/null; then
  command -v brew >/dev/null || { echo "Install Homebrew, or Beacon from https://docs.beacon.sh/cli/install" >&2; exit 1; }
  brew update
  brew trust asymptote-labs/tap
  brew tap asymptote-labs/tap
  brew install asymptote-labs/tap/beacon || install_from_archives
fi
beacon version

json_field() { python3 -c "import json,sys; d=json.load(sys.stdin); print(d$1)"; }

homes() { for dir in "$@"; do if [ -d "$dir" ]; then printf '%s\n' "$dir"; fi; done; }
read -r -a claude_homes <<<"${KELECHI_CLAUDE_HOMES:-$(homes ~/.claude ~/.claude[-_]* | tr '\n' ' ')}"
read -r -a codex_homes <<<"${KELECHI_CODEX_HOMES:-$(homes ~/.codex ~/.codex[-_]* | tr '\n' ' ')}"

# Beacon configures one Claude and one Codex home per run, chosen by CLAUDE_CONFIG_DIR and CODEX_HOME.
in_each_home() {
  for home in "${claude_homes[@]}"; do CLAUDE_CONFIG_DIR="$home" "$@" claude; done
  for home in "${codex_homes[@]}"; do CODEX_HOME="$home" "$@" codex; done
}
telemetry_on() {
  beacon endpoint discover --json | python3 -c "import json,sys; sys.exit(not any(h['name'].startswith('$1') and h['telemetry_status'] == 'enabled' for h in json.load(sys.stdin)))"
}
install_endpoint() { telemetry_on "$1" || beacon endpoint install --harness "$1" ${backfill[@]+"${backfill[@]}"}; }
connect_mcp() { beacon mcp connect --yes --harness "$1"; }

if [ "$(beacon endpoint status --system --json | json_field "['service']['loaded']")" = True ]; then
  echo "Beacon here is managed by your organisation (system mode); leaving its endpoint alone."
  echo "To send it to Beacon Cloud, an admin-approved 'sudo beacon endpoint connect --system' is needed."
else
  in_each_home install_endpoint
  beacon endpoint test-event

  if [ "$plan" = cloud ]; then
    if [ "$(beacon endpoint status --json | json_field "['managed_ingest']['enabled']")" != True ]; then
      beacon whoami >/dev/null 2>&1 || beacon login
      vector_bin=()
      [ -x ~/.local/libexec/beacon-vector/vector ] && vector_bin=(--vector-bin ~/.local/libexec/beacon-vector/vector)
      beacon endpoint connect --privacy-mode "$privacy" ${backfill[@]+"${backfill[@]}"} ${vector_bin[@]+"${vector_bin[@]}"}
    fi
    in_each_home connect_mcp
  fi
  beacon endpoint status
fi

beacon skills install
"$repo/scripts/reinstall.sh"

if [ "$plan" = cloud ]; then
  open https://beacon.sh/dashboard 2>/dev/null || echo "Open https://beacon.sh/dashboard"
  echo "Sign in to beacon-managed once in each agent (/mcp in Claude Code)."
else
  beacon endpoint dashboard --open
fi
