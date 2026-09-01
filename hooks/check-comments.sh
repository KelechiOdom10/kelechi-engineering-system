#!/bin/bash

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$script_dir/is-humaans-repo.sh" || exit 0

patch=$(jq -r '.tool_input.command // ""')

findings=$(printf '%s\n' "$patch" | awk '
  /^\*\*\* (Add|Update) File: / {
    file = $0
    sub(/^\*\*\* (Add|Update) File: /, "", file)
    skip = file ~ /(^|\/)tests?\// || file ~ /\.(test|spec)\.[^.]+$/
    next
  }
  /^\*\*\* / {
    file = ""
    next
  }
  file != "" && !skip && file ~ /\.(jsx?|tsx?)$/ && $0 ~ /^\+[[:space:]]*(\/\/|\/\*|\*)/ && $0 !~ /@ts-|eslint-|biome-|oxlint-|https?:\/\// {
    print file
  }
' | sort | uniq -c)

[ -z "$findings" ] && exit 0

message=$(printf 'This edit adds source-comment lines:\n%s\nKeep comments only when they preserve a non-obvious invariant, security constraint, vendor quirk, compatibility boundary, or important trade-off. Remove narration and temporary thought process. Use as many lines as clarity genuinely requires.' "$findings")

jq -n --arg message "$message" '{
  systemMessage: $message,
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    additionalContext: $message
  }
}'
