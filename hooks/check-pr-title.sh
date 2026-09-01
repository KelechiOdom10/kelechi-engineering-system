#!/bin/bash

set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$script_dir/is-humaans-repo.sh" || exit 0

command=$(jq -r '.tool_input.command // ""')

case "$command" in
  *"gh pr create"*|*"gh pr edit"*) ;;
  *) exit 0 ;;
esac

case "$command" in
  *"--title"*) ;;
  *) exit 0 ;;
esac

title=$(printf '%s' "$command" | sed -nE 's/.*--title[[:space:]]+"([^"]+)".*/\1/p;s/.*--title[[:space:]]+'\''([^'\'']+)'\''.*/\1/p' | head -n1)

[ -z "$title" ] && exit 0

if printf '%s' "$title" | grep -qE '(FIVE|SUP|HUMV)-[0-9]+'; then
  jq -n --arg title "$title" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: ("PR title contains a ticket number (" + $title + "). Ticket numbers belong in the branch name or PR body, never the title.")
    }
  }'
  exit 0
fi

if ! printf '%s' "$title" | grep -qE '^(feat|fix|chore|refactor|test|perf|docs|style|build|ci|revert)(\([^)]+\))?(!)?: '; then
  jq -n --arg title "$title" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: ("PR title (" + $title + ") must use Conventional Commits style: <type>(scope): description.")
    }
  }'
fi

exit 0
