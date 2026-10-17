"""Checks the reflect digest against small Claude Code and Codex transcripts. python3 tests/digest_test.py"""
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "reflect", "scripts", "digest.py")
failures = []


def write_jsonl(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(json.dumps(line) for line in lines))


def run(args, env):
    out = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True, env=env)
    if out.returncode != 0:
        failures.append(f"digest crashed: {out.stderr.strip()}")
    return out.stdout


def digest(lines, *extra):
    path = tempfile.mktemp(suffix=".jsonl")
    write_jsonl(path, lines)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_SESSION_ID"}
    return run(["--transcript", path, *extra], env)


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

context = "## Instructions\n" + "Standing context the harness injects on every turn. " * 200
long_request = digest([
    {"type": "user", "promptSource": "sdk", "message": {"content": "Context packet (injected by the host)\n\n" + context + "\n\n## Tasks\n\n\nyes start the plan"}},
    {"type": "user", "isMeta": True, "message": {"content": "[Image: source: /tmp/pasted.png]"}},
    {"type": "user", "message": {"content": "# Notes\n" + "a typed request with its own headings. " * 60 + "\n## Ask\nship it"}},
])
expect("human request at the end of a long message kept", "yes start the plan" in long_request)
expect("first line kept so provenance stays visible", "Context packet (injected by the host)" in long_request)
expect("elided context is labelled", "chars of leading context elided" in long_request)
expect("injected context not repeated", long_request.count("Standing context") < 5)
expect("sdk prompt source labelled", "**U** (via sdk) Context packet" in long_request)
expect("harness meta message omitted", "pasted.png" not in long_request)
expect("long typed request keeps its end", "ship it" in long_request)

codex_context = digest([
    {"type": "session_meta", "payload": {"cwd": "/repo"}},
    {"type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"text": "<environment_context>\n<cwd>/repo</cwd>\n</environment_context>\nWhy is the build slow?"}]}},
    {"type": "response_item", "payload": {"type": "message", "role": "user", "content": [{"text": "Relay from another agent: please start the build\n\n" + context + "\n\n## Tasks\n\n\nso cook then"}]}},
])
expect("codex request after leading XML context kept", "**U** Why is the build slow?" in codex_context)
expect("codex leading XML context stripped", "<cwd>" not in codex_context)
expect("codex request at the end of a long message kept", "so cook then" in codex_context)
expect("relay header kept as provenance", "Relay from another agent" in codex_context)

def exec_output(*parts):
    return [{"type": "input_text", "text": "Script completed\nWall time 0.1 seconds\nOutput:\n"}] + [{"type": "input_text", "text": json.dumps(part)} for part in parts]


def codex_output(output):
    return {"type": "response_item", "payload": {"type": "function_call_output", "output": output}}


WARNING = "python3: warning: confstr() failed with code 5: couldn't get path of DARWIN_USER_TEMP_DIR; using /tmp instead\n"
padding = {"content": [{"type": "text", "text": "x" * 700}]}
errors = digest([
    {"type": "session_meta", "payload": {"cwd": "/repo"}},
    codex_output(exec_output(padding, {"content": [{"type": "text", "text": "Workers cannot start new work from a relayed message."}], "isError": True})),
    codex_output(exec_output({"content": [{"type": "text", "text": json.dumps({"error": {"code": "turn_inactive", "message": "This write was rejected after the turn ended."}})}]})),
    codex_output(exec_output({"label": "fetch", "result": {"exit_code": 127, "output": WARNING + "zsh:1: command not found: ffprobe\n"}})),
    codex_output(exec_output({"content": [{"type": "text", "text": json.dumps({"error": {"code": "BrowserHostUnavailable", "message": "No browser host is available.", "retryable": True}})}], "isError": True})),
    codex_output(exec_output({"label": "decisions.md", "content": "- Earlier dispatch was rejected and the build failed: not found, permission denied."})),
    codex_output(exec_output({"rate_limit": {"status": "allowed", "overageStatus": "rejected"}, "error": None})),
    codex_output(exec_output({"exit_code": 0, "output": WARNING + "Wrote digest.md"})),
    codex_output(WARNING + "done\n"),
    codex_output("Command blocked by PreToolUse hook: wrong package manager"),
])
expect("nested isError past the first 600 chars recorded", "Workers cannot start new work" in errors)
expect("structured error code recorded", "turn_inactive: This write was rejected" in errors)
expect("non-zero exit code recorded without the warning", "exit 127: zsh:1: command not found: ffprobe" in errors and "exit 127: python3: warning" not in errors)
expect("retryable flag kept", "BrowserHostUnavailable" in errors and "retryable" in errors)
expect("quoted historical failure is not an error", "Earlier dispatch" not in errors)
expect("rejected field value is not an error", "overageStatus" not in errors)
expect("harmless sandbox warning is not an error", "Wrote digest.md" not in errors and "done" not in errors.split("errors and blocks")[1])
expect("plain-text hook block still recorded", "**E** Command blocked by PreToolUse hook" in errors)
expect("error counts", "errors and blocks: 5" in errors)

claude_errors = digest([
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": [{"type": "text", "text": json.dumps({"head": {"path": "decisions.md"}, "document": {"content": "x" * 50 + " the last run failed: permission denied"}})}]}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": [{"type": "text", "text": json.dumps({"error": {"code": "caller_turn_inactive", "message": "write rejected"}})}]}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": WARNING + "ok"}]}},
    {"type": "user", "message": {"content": [{"type": "tool_result", "content": "12 passed, 0 failed; README section 'Not found pages' updated"}]}},
])
expect("claude quoted failure in a document is not an error", "last run failed" not in claude_errors)
expect("claude structured error recorded", "**E** caller_turn_inactive: write rejected" in claude_errors)
expect("claude sandbox warning is not an error", "ok" not in claude_errors.split("errors and blocks")[1])
expect("claude successful output mentioning failures is not an error", "12 passed" not in claude_errors)
expect("claude error count", "errors and blocks: 1" in claude_errors)

config_dir = tempfile.mkdtemp()
os.makedirs(os.path.join(config_dir, "projects", "-repo"))
write_jsonl(os.path.join(config_dir, "projects", "-repo", "session-1.jsonl"), [{"type": "user", "message": {"content": "Found via the config dir"}}])
env = {**os.environ, "CLAUDE_CONFIG_DIR": config_dir, "CLAUDE_CODE_SESSION_ID": "session-1"}
expect("claude session found under CLAUDE_CONFIG_DIR", "**U** Found via the config dir" in run(["--harness", "claude"], env))

if failures:
    print("FAIL\n- " + "\n- ".join(failures))
    sys.exit(1)
print("all digest checks passed")
