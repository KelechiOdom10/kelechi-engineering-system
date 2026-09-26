"""PreToolUse guard for shell commands: package manager, VCS titles, AI attribution, PR Lens canvas."""
import json
import os
import re
import shlex
import subprocess

from _common import cwd_of, deny, git_root, read_input

CONVENTIONAL = re.compile(
    r"^(feat|fix|chore|refactor|test|perf|docs|style|build|ci|revert)(\([^)]+\))?!?: \S"
)
TICKET = re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d+\b")
ATTRIBUTION = [
    re.compile(r"co-authored-by:[^\n]*(claude|codex|openai|anthropic|chatgpt)", re.I),
    re.compile(r"generated with \[?claude code", re.I),
    re.compile(r"noreply@anthropic\.com", re.I),
    re.compile(r"🤖 generated with", re.I),
]
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n(]|\$\(")
LOCKFILES = {
    "pnpm-lock.yaml": "pnpm",
    "bun.lock": "bun",
    "bun.lockb": "bun",
    "yarn.lock": "yarn",
    "package-lock.json": "npm",
}
BUN_PM_VERBS = {"install", "i", "add", "remove", "rm", "update", "x", "pm"}
VP_WRAPPED = {"vitest": "vp test", "oxlint": "vp lint", "oxfmt": "vp fmt", "tsdown": "vp pack"}


def first_word(segment):
    try:
        words = shlex.split(segment, posix=True)
    except ValueError:
        words = segment.split()
    while words and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0]):
        words.pop(0)
    return words


HEREDOC_BODY = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?\s*\n.*?\n\s*\1", re.S)
QUOTED = re.compile(r"\"(?:\\.|[^\"\\])*\"|'[^']*'")


def invoked_tools(command):
    code_only = QUOTED.sub("''", HEREDOC_BODY.sub("", command))
    for segment in SEGMENT_SPLIT.split(code_only):
        words = first_word(segment.strip())
        if words:
            yield words[0], words[1:]


def package_manager(root):
    found = {pm for name, pm in LOCKFILES.items() if os.path.exists(os.path.join(root, name))}
    return found.pop() if len(found) == 1 else None


def uses_vite_plus(root):
    try:
        with open(os.path.join(root, "package.json")) as f:
            pkg = json.load(f)
    except (OSError, json.JSONDecodeError):
        return False
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    return "vite-plus" in deps


def check_package_manager(command, root):
    pm = package_manager(root)
    vite_plus = uses_vite_plus(root)
    for tool, args in invoked_tools(command):
        verb = args[0] if args else ""
        if vite_plus and tool in VP_WRAPPED:
            deny(f"This repo uses Vite+. Run `{VP_WRAPPED[tool]}` instead of `{tool}`.")
        if vite_plus and tool == "npx":
            deny("This repo uses Vite+. Run `vp dlx` instead of `npx`.")
        if pm is None:
            continue
        wrong = (
            (tool in ("npm", "npx") and pm != "npm")
            or (tool == "yarn" and pm != "yarn")
            or (tool in ("pnpm", "pnpx") and pm != "pnpm")
            or (tool == "bunx" and pm != "bun")
            or (tool == "bun" and verb in BUN_PM_VERBS and pm != "bun")
        )
        if wrong:
            deny(f"This repo's lockfile says {pm}. Use {pm} instead of `{tool}`.")


def heredoc_first_line(command):
    match = re.search(r"<<-?\s*['\"]?(\w+)['\"]?\s*\n(.*?)\n\s*\1", command, re.S)
    if not match:
        return None
    lines = [line.strip() for line in match.group(2).splitlines() if line.strip()]
    return lines[0] if lines else None


def flag_value(command, flags):
    try:
        words = shlex.split(command, posix=True)
    except ValueError:
        return None
    for i, word in enumerate(words[:-1]):
        if word in flags:
            return words[i + 1]
        for flag in flags:
            if flag.startswith("--") and word.startswith(flag + "="):
                return word.split("=", 1)[1]
    return None


def check_title(title, kind):
    title = title.strip().splitlines()[0] if title.strip() else ""
    if not title or title.startswith(("Merge ", "Revert \"", "fixup!", "squash!")):
        return
    if TICKET.search(title):
        deny(f"{kind} title `{title}` contains a ticket id. Put tickets in the branch name or body.")
    if not CONVENTIONAL.match(title):
        deny(f"{kind} title `{title}` must use Conventional Commits: `type(scope): intent`.")
    if kind == "PR" and len(title) > 72:
        deny(f"PR title is {len(title)} characters. Keep it under 70 and state intent, not mechanics.")


COMMIT = re.compile(r"\bgit\s+(?:-C\s+\S+\s+)?commit\b")
PR_WRITE = re.compile(r"\bgh\s+pr\s+(?:create|edit)\b")
HEREDOC_MESSAGE = re.compile(r"[^\n]*?\s(?:-m|--message)[\s=]+\"\$\(cat\s*<<")


def commit_subjects(command):
    """Yield each `git commit` subject, reading only from that commit onwards."""
    for match in COMMIT.finditer(command):
        rest = command[match.start():]
        if HEREDOC_MESSAGE.match(rest):
            subject = heredoc_first_line(rest)
        else:
            subject = flag_value(rest, ["-m", "--message"])
        if subject:
            yield subject


def check_vcs(command, cwd):
    is_pr = PR_WRITE.search(command)
    if not (COMMIT.search(command) or is_pr or re.search(r"\bgh\s+(pr|issue)\s+comment\b", command)):
        return

    bodies = [command]
    body_file = flag_value(command, ["--body-file", "-F", "--file"])
    if body_file and body_file != "-":
        path = body_file if os.path.isabs(body_file) else os.path.join(cwd, body_file)
        try:
            with open(path) as f:
                bodies.append(f.read())
        except OSError:
            pass
    for text in bodies:
        if any(p.search(text) for p in ATTRIBUTION):
            deny("Remove the AI attribution line. Kelechi's commits and PRs carry no AI attribution.")

    for subject in commit_subjects(command):
        check_title(subject, "Commit")
    if is_pr:
        title = flag_value(command[is_pr.start():], ["--title", "-t"])
        if title:
            check_title(title, "PR")


CANVAS_PUSH = re.compile(r"pr-lens(?:-cli)?(?:@\S+)?\s+canvas\s+push\b")
CANVAS_OPT_IN = re.compile(r"(?:^|[\s;&|(])KELECHI_CANVAS=yes\s")
RESTRICTED_ORIGINS = re.compile(r"[:/]humaans/humaans(?:\.git)?$")


def origin_url(root):
    try:
        out = subprocess.run(["git", "-C", root, "config", "--get", "remote.origin.url"], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip()


def check_canvas(command, root):
    if not CANVAS_PUSH.search(command):
        return
    if RESTRICTED_ORIGINS.search(origin_url(root)):
        deny("PR Lens canvases are not allowed in this repository: prlens.dev is not an approved provider. Attach the rendered SVGs to the PR with `gh pr create --attach` instead.")
    if not CANVAS_OPT_IN.search(command):
        deny(
            "Canvas upload is off by default: it publishes the architecture to prlens.dev behind a link that opens "
            "without a login. Attach the rendered SVGs to the PR with `gh pr create --attach`, or hand back the local "
            "SVG paths. Only if Kelechi explicitly asked for a canvas in this conversation, rerun the command prefixed "
            "with KELECHI_CANVAS=yes."
        )


def main():
    payload = read_input()
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not command:
        return
    cwd = cwd_of(payload)
    check_vcs(command, cwd)
    root = git_root(cwd) or cwd
    check_canvas(command, root)
    check_package_manager(command, root)


if __name__ == "__main__":
    main()
