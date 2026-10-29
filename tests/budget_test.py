"""Token budgets for the plugin's own instructions. python3 tests/budget_test.py

Tokens are estimated as characters / 4. A failure means: prune something weaker, or raise the
budget in the same PR with a one-line reason in the PR body.
"""
import glob
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BUDGETS = {
    "always_on": 1800,
    "router_core": 2700,
    "skill_file": 1300,
}
ROUTER_CORE = [
    "skills/kelechi-mode/SKILL.md",
    "skills/kelechi-mode/references/routing.md",
    "skills/kelechi-mode/references/principles.md",
]


def tokens(text):
    return (len(text) + 3) // 4


def read(path):
    with open(os.path.join(ROOT, path)) as f:
        return f.read()


def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    return match.group(1) if match else ""


def always_on(plugin_root):
    """Frontmatter the model sees every session: skills and agents, minus user-only (disable-model-invocation) entries."""
    total = 0
    for path in glob.glob(os.path.join(ROOT, plugin_root, "skills/*/SKILL.md")) + glob.glob(
        os.path.join(ROOT, plugin_root, "agents/*.md")
    ) + glob.glob(os.path.join(ROOT, plugin_root, "commands/*.md")):
        with open(path) as f:
            meta = frontmatter(f.read())
        if "disable-model-invocation: true" not in meta:
            total += tokens(meta)
    return total


failures = []
for path in glob.glob(os.path.join(ROOT, "commands/*.md")):
    name = os.path.splitext(os.path.basename(path))[0]
    if os.path.isfile(os.path.join(ROOT, "skills", name, "SKILL.md")):
        meta = frontmatter(open(path).read())
        if "disable-model-invocation: true" not in meta:
            failures.append(f"commands/{name}.md shadows skills/{name}/SKILL.md; make the command user-only")

measured = {"always_on": always_on("."), "router_core": sum(tokens(read(p)) for p in ROUTER_CORE)}
for name in ("always_on", "router_core"):
    if measured[name] > BUDGETS[name]:
        failures.append(f"{name}: ~{measured[name]} tokens, budget {BUDGETS[name]}")

largest = []
for path in glob.glob(os.path.join(ROOT, "**/skills/**/*.md"), recursive=True):
    size = tokens(open(path).read())
    largest.append((size, os.path.relpath(path, ROOT)))
    if size > BUDGETS["skill_file"]:
        failures.append(f"{os.path.relpath(path, ROOT)}: ~{size} tokens, budget {BUDGETS['skill_file']}")
largest.sort(reverse=True)

report = (
    f"always-on ~{measured['always_on']}/{BUDGETS['always_on']}, "
    f"router core ~{measured['router_core']}/{BUDGETS['router_core']}, "
    f"largest skill file ~{largest[0][0]}/{BUDGETS['skill_file']} ({largest[0][1]})"
)
if failures:
    print("FAIL: over budget. Prune something weaker, or raise the budget with a reason.\n- " + "\n- ".join(failures))
    print(report)
    sys.exit(1)
print(f"within budget: {report}")
