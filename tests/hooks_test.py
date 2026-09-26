"""Runs each hook against realistic Claude Code and Codex payloads. python3 tests/hooks_test.py"""
import json
import os
import subprocess
import sys
import tempfile
import time

HOOKS = os.environ.get("HOOKS_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks")
failures = []


def run(hook, payload):
    out = subprocess.run(
        [sys.executable, os.path.join(HOOKS, hook)],
        input=json.dumps(payload), capture_output=True, text=True, timeout=60,
    )
    if out.returncode != 0:
        failures.append(f"{hook} crashed: {out.stderr.strip()}")
    return json.loads(out.stdout) if out.stdout.strip() else None


def repo(files):
    root = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    for name, content in files.items():
        path = os.path.join(root, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
    return root


def denied(result):
    return bool(result) and result.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


def expect(name, condition):
    if not condition:
        failures.append(name)


def bash(root, command):
    return run("pre_bash.py", {"tool_name": "Bash", "cwd": root, "tool_input": {"command": command}})


pnpm = repo({"pnpm-lock.yaml": "", "package.json": "{}"})
bun = repo({"bun.lock": "", "package.json": "{}"})
vp = repo({"pnpm-lock.yaml": "", "package.json": json.dumps({"devDependencies": {"vite-plus": "^0.1.11"}})})
plain = repo({})

expect("npm blocked in pnpm repo", denied(bash(pnpm, "npm install zod")))
expect("npx blocked in pnpm repo", denied(bash(pnpm, "cd apps/web && npx shadcn add button")))
expect("pnpm allowed in pnpm repo", not denied(bash(pnpm, "pnpm --filter @x/api dev")))
expect("pnpm blocked in bun repo", denied(bash(bun, "pnpm add hono")))
expect("bun run allowed in pnpm repo", not denied(bash(pnpm, "bun run scripts/seed.ts")))
expect("bun add blocked in pnpm repo", denied(bash(pnpm, "bun add hono")))
expect("vitest blocked in vite-plus repo", denied(bash(vp, "vitest run")))
expect("vp test allowed in vite-plus repo", not denied(bash(vp, "vp test")))
expect("npm allowed outside a lockfile repo", not denied(bash(plain, "npm view zod version")))
expect("npm inside a quoted message is not a command",
       not denied(bash(pnpm, 'git commit -m "chore: stop using npm && npx"')))

expect("conventional commit allowed", not denied(bash(plain, 'git commit -m "fix(api): return empty web result"')))
expect("non-conventional commit blocked", denied(bash(plain, 'git commit -m "Fixed the thing"')))
expect("ticket in commit subject blocked", denied(bash(plain, 'git commit -m "fix: SUP-4123 wrong balance"')))
heredoc = "git commit -m \"$(cat <<'EOF'\nfeat(web): show cited sources only\n\nnpm is not used here.\nEOF\n)\""
expect("heredoc conventional commit allowed", not denied(bash(pnpm, heredoc)))
expect("heredoc bad subject blocked", denied(bash(plain, heredoc.replace("feat(web): show", "Show"))))
expect("attribution trailer blocked",
       denied(bash(plain, heredoc.replace("npm is not used here.", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"))))
expect("amend without message allowed", not denied(bash(plain, "git commit --amend --no-edit")))
expect("PR title with ticket blocked", denied(bash(plain, 'gh pr create --title "feat: FIVE-12 add export" --body x')))
expect("good PR title allowed", not denied(bash(plain, 'gh pr create --title "feat(web): add export" --body "## Context"')))
expect("long PR title blocked", denied(bash(plain, 'gh pr create --title "feat: ' + "x" * 80 + '" --body y')))
body = os.path.join(plain, "body.md")
with open(body, "w") as f:
    f.write("## Context\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n")
expect("attribution in --body-file blocked", denied(bash(plain, f'gh pr create --title "fix: x" --body-file {body}')))

src = repo({"package.json": "{}", "src/a.ts": "export const a = 1\n"})
edit = {"tool_name": "Edit", "cwd": src, "tool_input": {
    "file_path": os.path.join(src, "src/a.ts"), "old_string": "export const a = 1",
    "new_string": "// set a to one\nexport const a = 1\n// SAFETY: checked above"}}
result = run("post_edit.py", edit)
context = (result or {}).get("hookSpecificOutput", {}).get("additionalContext", "")
expect("new narrating comment flagged", "src/a.ts (+1)" in context)
edit["tool_input"]["new_string"] = "export const a = 1\n// SAFETY: registry pairs kind with handler"
expect("SAFETY comment not flagged", run("post_edit.py", edit) is None)
patch = "*** Begin Patch\n*** Update File: src/a.ts\n@@\n+// explain the thing\n export const a = 1\n*** End Patch"
codex = run("post_edit.py", {"tool_name": "apply_patch", "cwd": src, "tool_input": {"command": patch}})
expect("codex apply_patch comment flagged", "src/a.ts (+1)" in json.dumps(codex or {}))
test_edit = dict(edit, tool_input={"file_path": os.path.join(src, "src/a.test.ts"), "old_string": "", "new_string": "// arrange"})
expect("comments in tests ignored", run("post_edit.py", test_edit) is None)

fmt = repo({"package.json": json.dumps({"devDependencies": {"prettier": "3"}}), ".prettierrc": "{}", "a.ts": "const  a=1\n"})
os.makedirs(os.path.join(fmt, "node_modules", ".bin"))
fake = os.path.join(fmt, "node_modules", ".bin", "prettier")
with open(fake, "w") as f:
    f.write('#!/bin/sh\nfor a in "$@"; do case "$a" in *.ts) echo "const a = 1" > "$a";; esac; done\n')
os.chmod(fake, 0o755)
run("post_edit.py", {"tool_name": "Write", "cwd": fmt, "tool_input": {"file_path": os.path.join(fmt, "a.ts"), "content": "const  a=1\n"}})
with open(os.path.join(fmt, "a.ts")) as f:
    expect("repo formatter runs on edited file", f.read() == "const a = 1\n")

state = repo({"README.md": "x"})
subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qam", "init", "--allow-empty"], cwd=state)
subprocess.run(["git", "add", "."], cwd=state)
subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init"], cwd=state)
os.makedirs(os.path.join(state, ".kelechi"))
fresh = os.path.join(state, ".kelechi", "handoff-fresh.md")
old = os.path.join(state, ".kelechi", "handoff-old.md")
with open(fresh, "w") as f:
    f.write("---\nkind: handoff\nbranch: main\nstatus: active\n---\n")
with open(old, "w") as f:
    f.write("---\nkind: handoff\nbranch: feat/gone\nstatus: active\n---\n")
week_ago = time.time() - 8 * 86400
os.utime(old, (week_ago, week_ago))
session = json.dumps(run("session_start.py", {"cwd": state}) or {})
expect("stale handoff surfaced", "handoff-old.md" in session and "feat/gone" in session and "older than 7 days" in session)
expect("fresh handoff not surfaced", "handoff-fresh.md" not in session)
expect("no .kelechi means no output", run("session_start.py", {"cwd": plain}) is None)

if failures:
    print("FAIL\n- " + "\n- ".join(failures))
    sys.exit(1)
print("all hook checks passed")
