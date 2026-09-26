"""PostToolUse after file edits: run the repo's formatter, nudge on new source comments."""
import json
import os
import re
import shutil
import subprocess

from _common import add_context, cwd_of, git_root, read_input

FORMAT_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts", ".css", ".json", ".astro", ".vue", ".svelte"}
COMMENT_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".mts", ".cts", ".astro", ".vue", ".svelte"}
TEST_FILE = re.compile(r"(^|/)(tests?|__tests__|fixtures)/|\.(test|spec)\.[^.]+$")
COMMENT_LINE = re.compile(r"^\s*(//|/\*|\*(?!/))")
ALLOWED_COMMENT = re.compile(
    r"SAFETY:|@ts-|eslint-|oxlint-|biome-|prettier-ignore|@license|https?://|^\s*\*/\s*$|^\s*/\*\*?\s*$"
)


def edits(payload):
    """Yield (path, old_text, new_text) for Claude Edit/Write/MultiEdit and Codex apply_patch."""
    tool = payload.get("tool_name", "")
    data = payload.get("tool_input") or {}
    if tool == "Edit":
        yield data.get("file_path"), data.get("old_string", ""), data.get("new_string", "")
    elif tool == "Write":
        yield data.get("file_path"), "", data.get("content", "")
    elif tool == "MultiEdit":
        for edit in data.get("edits", []):
            yield data.get("file_path"), edit.get("old_string", ""), edit.get("new_string", "")
    elif tool == "apply_patch":
        path, added = None, []
        for line in (data.get("command") or data.get("input") or "").splitlines():
            header = re.match(r"^\*\*\* (Add|Update) File: (.+)$", line)
            if header or line.startswith("*** "):
                if path:
                    yield path, "", "\n".join(added)
                path, added = (header.group(2).strip() if header else None), []
            elif path and line.startswith("+"):
                added.append(line[1:])
        if path:
            yield path, "", "\n".join(added)


def formatter(root):
    def local(name):
        path = os.path.join(root, "node_modules", ".bin", name)
        return path if os.path.exists(path) else None

    try:
        with open(os.path.join(root, "package.json")) as f:
            pkg = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    has = lambda *names: any(os.path.exists(os.path.join(root, n)) for n in names)

    if "vite-plus" in deps:
        vp = local("vp") or shutil.which("vp")
        return [vp, "fmt", "--write"] if vp else None
    if "oxfmt" in deps or has(".oxfmtrc.json", ".oxfmtrc.jsonc"):
        return [local("oxfmt"), "--write"] if local("oxfmt") else None
    if "@biomejs/biome" in deps or has("biome.json", "biome.jsonc"):
        return [local("biome"), "format", "--write"] if local("biome") else None
    if "prettier" in deps or has(".prettierrc", ".prettierrc.json", ".prettierrc.cjs", ".prettierrc.js", "prettier.config.js", "prettier.config.mjs"):
        return [local("prettier"), "--write", "--log-level", "warn"] if local("prettier") else None
    return None


def new_comment_lines(old, new):
    before = {line.strip() for line in old.splitlines()}
    return [
        line for line in new.splitlines()
        if COMMENT_LINE.match(line) and not ALLOWED_COMMENT.search(line) and line.strip() not in before
    ]


def main():
    payload = read_input()
    cwd = cwd_of(payload)
    root = git_root(cwd) or cwd
    touched, comments = [], {}

    for path, old, new in edits(payload):
        if not path:
            continue
        absolute = path if os.path.isabs(path) else os.path.join(root, path)
        ext = os.path.splitext(absolute)[1]
        rel = os.path.relpath(absolute, root)
        if ext in FORMAT_EXT and os.path.isfile(absolute) and absolute not in touched:
            touched.append(absolute)
        if ext in COMMENT_EXT and not TEST_FILE.search(rel):
            added = new_comment_lines(old, new)
            if added:
                comments[rel] = comments.get(rel, 0) + len(added)

    command = formatter(root) if touched else None
    if command:
        try:
            subprocess.run(command + touched, cwd=root, capture_output=True, timeout=45)
        except (OSError, subprocess.TimeoutExpired):
            pass

    if comments:
        listing = ", ".join(f"{path} (+{count})" for path, count in comments.items())
        add_context(
            "PostToolUse",
            f"New source comments in {listing}. Keep a comment only for a non-obvious why: an invariant, "
            "a SAFETY: justification, a security constraint, a vendor quirk, or a trade-off. "
            "Rename or restructure instead of narrating.",
        )


if __name__ == "__main__":
    main()
