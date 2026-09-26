"""SessionStart: surface stale Kelechi Mode working-state files in .kelechi/."""
import os
import re
import subprocess
import time

from _common import add_context, cwd_of, git_root, read_input

STALE_DAYS = 7


def git(root, *args):
    try:
        out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out if out.returncode == 0 else None


def frontmatter(path):
    try:
        with open(path) as f:
            text = f.read(2000)
    except OSError:
        return {}
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return {}
    return dict(
        (key.strip(), value.strip())
        for key, _, value in (line.partition(":") for line in match.group(1).splitlines())
        if key.strip()
    )


def default_branch(root):
    ref = git(root, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    return ref.stdout.strip().removeprefix("refs/remotes/") if ref else "main"


def reasons(root, path, meta):
    found = []
    if time.time() - os.path.getmtime(path) > STALE_DAYS * 86400:
        found.append(f"older than {STALE_DAYS} days")
    branch = meta.get("branch")
    if branch and not git(root, "rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"):
        found.append(f"branch `{branch}` no longer exists")
    head = meta.get("head")
    base = default_branch(root)
    if head and branch and branch not in (base, base.split("/")[-1]):
        if git(root, "merge-base", "--is-ancestor", head, base):
            found.append(f"its head {head} is already merged into {base}")
    if meta.get("status") == "consumed":
        found.append("marked consumed")
    return found


def main():
    payload = read_input()
    root = git_root(cwd_of(payload))
    folder = os.path.join(root, ".kelechi") if root else None
    if not folder or not os.path.isdir(folder):
        return
    stale = []
    for name in sorted(os.listdir(folder)):
        path = os.path.join(folder, name)
        if os.path.isfile(path) and name.endswith(".md"):
            why = reasons(root, path, frontmatter(path))
            if why:
                stale.append(f"- .kelechi/{name}: {'; '.join(why)}")
    if stale:
        add_context(
            "SessionStart",
            "Kelechi Mode working state that may be stale. Re-verify before relying on it, "
            "then promote the lasting part to docs/ or delete it:\n" + "\n".join(stale),
        )


if __name__ == "__main__":
    main()
