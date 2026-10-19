"""Checks each Codex agent is read-only and named as the skills spawn it. python3 tests/codex_agents_test.py"""
import glob
import os
import re
import sys
import tomllib

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
spawned = set()
for path in glob.glob(os.path.join(root, "skills", "**", "*.md"), recursive=True):
    spawned |= set(re.findall(r"`(kelechi_[a-z_]+)`", open(path).read()))

failures = []
names = set()
for path in sorted(glob.glob(os.path.join(root, "codex", "agents", "*.toml"))):
    with open(path, "rb") as f:
        agent = tomllib.load(f)
    names.add(agent["name"])
    if agent.get("sandbox_mode") != "read-only":
        failures.append(f"{os.path.basename(path)}: sandbox_mode is {agent.get('sandbox_mode')!r}, expected 'read-only'")
for name in sorted(spawned - names):
    failures.append(f"skills spawn {name}, but no codex/agents file declares it")

if failures:
    print("\n".join(failures))
    sys.exit(1)
print(f"codex agents ok: {', '.join(sorted(names))}")
