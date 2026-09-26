import json
import os
import subprocess
import sys


def read_input():
    raw = sys.stdin.read()
    try:
        return json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return {}


def git_root(cwd):
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=cwd, capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def cwd_of(payload):
    cwd = payload.get("cwd") or os.getcwd()
    return cwd if os.path.isdir(cwd) else os.getcwd()


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def add_context(event, message):
    print(json.dumps({
        "systemMessage": message,
        "hookSpecificOutput": {"hookEventName": event, "additionalContext": message},
    }))
