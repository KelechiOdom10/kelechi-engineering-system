#!/bin/bash

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$script_dir/is-humaans-repo.sh" || exit 0

patch=$(jq -r '.tool_input.command // ""')
root=$(git rev-parse --show-toplevel)
targets=()

while IFS= read -r file; do
  case "$file" in
    *.js|*.jsx|*.ts|*.tsx)
      [ -f "$root/$file" ] && targets+=("$file")
      ;;
  esac
done < <(printf '%s\n' "$patch" | sed -nE 's/^\*\*\* (Add|Update) File: (.*)$/\2/p' | sort -u)

[ "${#targets[@]}" -eq 0 ] && exit 0

cd "$root"
pnpm exec oxfmt --write "${targets[@]}"
