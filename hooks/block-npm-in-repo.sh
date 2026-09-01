#!/bin/bash

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$script_dir/is-humaans-repo.sh" || exit 0

command=$(jq -r '.tool_input.command // empty')

if printf '%s' "$command" | grep -qE '(^|[;&|(]|&&|\|\|)[[:space:]]*(npm|npx)([[:space:]]|$)'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "This project uses pnpm, not npm/npx. Use pnpm instead."
    }
  }'
fi

exit 0
