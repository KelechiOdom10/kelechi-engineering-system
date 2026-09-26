"""Checks the reflect digest against small Claude Code and Codex transcripts. python3 tests/digest_test.py"""
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "reflect", "scripts", "digest.py")
failures = []


def digest(lines, *extra):
    path = tempfile.mktemp(suffix=".jsonl")
    with open(path, "w") as f:
        f.write("\n".join(json.dumps(line) for line in lines))
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
    out = subprocess.run([sys.executable, SCRIPT, "--transcript", path, *extra], capture_output=True, text=True, env=env)
    if out.returncode != 0:
        failures.append(f"digest crashed: {out.stderr.strip()}")
    return out.stdout


def expect(name, condition):
    if not condition:
        failures.append(name)


claude = digest([
    {"type": "user", "message": {"content": "Fix the flaky test <system-reminder>internal note</system-reminder>"}},
    {"type": "assistant", "message": {"content": [
        {"type": "thinking", "thinking": "secret reasoning"},
        {"type": "text", "text": "Reproducing first."},
        {"type": "tool_use", "name": "Bash", "input": {"command": "pnpm test"}},
    ]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "is_error": True, "content": "Exit code 1: 2 tests failed"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "all good"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "PreToolUse:Bash hook error: use pnpm"}]}},
    {"type": "assistant", "isSidechain": True, "message": {"content": [{"type": "text", "text": "subagent chatter"}]}},
])
expect("claude user message kept", "**U** Fix the flaky test" in claude)
expect("system reminders stripped", "internal note" not in claude)
expect("thinking never included", "secret reasoning" not in claude)
expect("tool call recorded", "**T** Bash: pnpm test" in claude)
expect("tool error recorded", "**E** Exit code 1: 2 tests failed" in claude)
expect("hook block recorded even without is_error", "**E** PreToolUse:Bash hook error" in claude)
expect("successful output omitted", "all good" not in claude)
expect("subagent sidechain omitted", "subagent chatter" not in claude)
expect("claude counts", "User messages: 1 | assistant messages: 1 | tool calls: 1 | errors and blocks: 2" in claude)

codex = digest([
    {"type": "session_meta", "payload": {"cwd": "/repo"}},
    {"type": "response_item", "payload": {"type": "message", "role": "developer", "content": [{"text": "system rules"}]}},
    {"type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"text": "<environment_context>noise</environment_context>"}]}},
    {"type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"text": "Why is CI red?"}]}},
    {"type": "response_item", "payload": {"type": "function_call", "name": "exec_command", "arguments": "{\"cmd\":\"gh pr checks\"}"}},
    {"type": "response_item", "payload": {"type": "function_call_output", "output": "Command blocked by PreToolUse hook: wrong package manager"}},
    {"type": "response_item", "payload": {"type": "message", "role": "assistant", "content": [{"text": "The lint job fails."}]}},
])
expect("codex user message kept", "**U** Why is CI red?" in codex)
expect("codex developer and injected context dropped", "system rules" not in codex and "noise" not in codex)
expect("codex tool call recorded", "**T** exec_command" in codex)
expect("codex hook block recorded", "**E** Command blocked by PreToolUse hook" in codex)
expect("codex source labelled", "(Codex)" in codex)

if failures:
    print("FAIL\n- " + "\n- ".join(failures))
    sys.exit(1)
print("all digest checks passed")
