#!/usr/bin/env python3
"""Condense a Claude Code or Codex session transcript into a reviewable digest.

Usage: digest.py [--harness claude|codex] [--transcript PATH] [--cwd DIR] [--lessons FILE] [--out FILE]
Without --transcript, finds the current session. Claude Code: CLAUDE_CODE_SESSION_ID, under
CLAUDE_CONFIG_DIR (default ~/.claude).
Codex: the newest rollout whose session cwd is --cwd (default: the current directory).
--harness defaults to claude when CLAUDE_CODE_SESSION_ID is set, otherwise codex.
--lessons defaults to the reflect skill's lessons.jsonl; each lesson whose detector matches is listed at the end.
"""
import argparse
import glob
import json
import os
import re
import sys

SIGNAL = re.compile(
    r"hook error|blocked by|denied|permission|exit code [1-9]|traceback|error:|failed|not found|timed out|hung",
    re.I,
)
# Claude Code flags failed tool results with is_error, so its text only needs scanning for hook blocks.
BLOCK = re.compile(r"hook error|blocked by|denied|permission", re.I)
HARMLESS = re.compile(r"^.*warning: confstr\(\) failed with code 5.*$\n?", re.M)
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
LEADING_XML = re.compile(r"\A\s*<([A-Za-z_][\w-]*)[^>]*>.*?</\1>\s*", re.S)
HEADING = re.compile(r"^#{1,6} .*$", re.M)
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
REQUEST_TAIL = 4000
MAX = {"user": REQUEST_TAIL + 300, "assistant": 700, "tool": 220, "error": 500}


def clip(text, limit):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[:limit] + " [...]"


def keep_request(text):
    """Harnesses prepend long context to a user turn; the request typed after it is what matters.

    A message that fits REQUEST_TAIL is kept whole. A longer one keeps its first line, which names
    who or what sent it, and its end: the section after its last markdown heading outside a code
    fence when that fits, otherwise the last REQUEST_TAIL characters.
    """
    text = text.strip()
    if len(text) <= REQUEST_TAIL:
        return text
    first = text.split("\n", 1)[0][:200]
    fenced = [m.span() for m in FENCE.finditer(text)]
    ends = [h.end() for h in HEADING.finditer(text) if not any(a <= h.start() < b for a, b in fenced)]
    last = ends[-1] if ends else 0
    start = last if len(text) - last <= REQUEST_TAIL and text[last:].strip() else len(text) - REQUEST_TAIL
    start = max(start, len(first))
    return f"{first} [... {start - len(first)} chars of leading context elided ...] {text[start:].strip()}"


def strip_leading_xml(text):
    while match := LEADING_XML.match(text):
        text = text[match.end():]
    return text


def parsed(text):
    if text.lstrip()[:1] in ("{", "["):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    return text


def structured_failures(node, parse=True, sibling_output=""):
    """Failures a tool reported as data: isError, an error object, or a non-zero exit code.

    JSON is read from the result itself and from its text parts. Any other string value, such as a
    document body that quotes an old failure, stays text and is never read as a flag.
    """
    if isinstance(node, str):
        node = parsed(node) if parse else node
        if isinstance(node, str):
            return
    if isinstance(node, list):
        for item in node:
            yield from structured_failures(item, parse, sibling_output)
        return
    if not isinstance(node, dict):
        return
    own = []
    error = node.get("error")
    if isinstance(error, dict) and (error.get("code") or error.get("message")):
        details = error.get("details") if isinstance(error.get("details"), dict) else {}
        cause = f" ({details['message']})" if details.get("message") else ""
        flags = " (retryable)" if error.get("retryable") else ""
        own.append(f"{error.get('code') or 'error'}: {error.get('message', '')}{cause}{flags}".strip())
    elif isinstance(error, str) and error.strip():
        own.append(f"error: {error}")
    output = str(node.get("output") or node.get("stderr") or sibling_output or "")
    exit_code = node.get("exit_code", node.get("exitCode"))
    if isinstance(exit_code, int) and exit_code != 0:
        output = HARMLESS.sub("", output).strip()
        own.append(f"exit {exit_code}: {output[-(MAX['error'] - 40):]}")
    nested = [
        f for key, value in node.items() if isinstance(value, (dict, list, str))
        for f in structured_failures(value, key == "text", output)
    ]
    if (node.get("isError") is True or node.get("is_error") is True) and not own and not nested:
        own.append(text_of(node.get("content")) or "isError")
    yield from own + nested


def failure(output, signal=SIGNAL):
    """One line describing what failed in a tool result, or None when it succeeded."""
    found = list(dict.fromkeys(structured_failures(output)))
    if found:
        return "; ".join(found)
    parts = output if isinstance(output, list) else [output]
    plain = " ".join(
        p for p in (part.get("text", "") if isinstance(part, dict) else part for part in parts)
        if isinstance(p, str) and isinstance(parsed(p), str)
    )
    plain = HARMLESS.sub("", plain).strip()
    return plain if signal.search(plain[:600]) else None


def find_claude():
    session = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not session:
        return None
    home = os.environ.get("CLAUDE_CONFIG_DIR") or "~/.claude"
    matches = glob.glob(os.path.join(os.path.expanduser(home), "projects", "*", f"{session}.jsonl"))
    return matches[0] if matches else None


def find_codex(cwd):
    rollouts = sorted(
        glob.glob(os.path.expanduser("~/.codex/sessions/*/*/*/rollout-*.jsonl")),
        key=os.path.getmtime,
        reverse=True,
    )
    for path in rollouts:
        try:
            with open(path) as f:
                meta = json.loads(f.readline())
        except (OSError, json.JSONDecodeError):
            continue
        if meta.get("payload", {}).get("cwd") == cwd:
            return path
    return None


def text_of(content):
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        if isinstance(block, dict):
            parts.append(block.get("text") or (text_of(block["content"]) if "content" in block else ""))
    return " ".join(p for p in parts if p)


def claude_events(lines):
    for line in lines:
        if line.get("isSidechain"):
            continue
        kind, message = line.get("type"), line.get("message") or {}
        content = message.get("content")
        if kind == "user":
            if line.get("isMeta"):
                continue
            via = f"(via {line['promptSource']}) " if line.get("promptSource") else ""
            if isinstance(content, str):
                text = REMINDER.sub("", content).strip()
                if text:
                    yield "user", via + keep_request(text)
                continue
            for block in content or []:
                if block.get("type") == "tool_result":
                    result = block.get("content")
                    reason = failure(result, BLOCK)
                    if block.get("is_error") or reason:
                        yield "error", reason or text_of(result)
                elif block.get("type") == "text":
                    text = REMINDER.sub("", block.get("text", "")).strip()
                    if text:
                        yield "user", via + keep_request(text)
        elif kind == "assistant":
            for block in content or []:
                if block.get("type") == "text" and block.get("text", "").strip():
                    yield "assistant", block["text"]
                elif block.get("type") == "tool_use":
                    data = block.get("input") or {}
                    detail = data.get("command") or data.get("file_path") or data.get("skill") or data.get("subagent_type") or json.dumps(data)
                    yield "tool", f"{block.get('name')}: {detail}"


def codex_events(lines):
    for line in lines:
        payload = line.get("payload") or {}
        kind = payload.get("type")
        if kind == "message" and payload.get("role") in ("user", "assistant"):
            text = text_of(payload.get("content"))
            if payload["role"] == "user":
                text = keep_request(strip_leading_xml(text))
                if not text:
                    continue
            yield payload["role"], text
        elif kind in ("function_call", "custom_tool_call"):
            yield "tool", f"{payload.get('name')}: {payload.get('arguments') or payload.get('input')}"
        elif kind in ("function_call_output", "custom_tool_call_output"):
            reason = failure(payload.get("output"))
            if reason:
                yield "error", reason


def recurrences(events, lessons_path):
    """One line per lesson whose detector matches an event of its kind; a broken lesson says so."""
    if not os.path.isfile(lessons_path):
        return []
    found = []
    with open(lessons_path) as f:
        for line in filter(str.strip, f):
            lesson = None
            try:
                lesson = json.loads(line)
                kind, detect = lesson["detect"]["kind"], re.compile(lesson["detect"]["pattern"])
                name, text = lesson["id"], lesson["lesson"]
            except (json.JSONDecodeError, KeyError, TypeError, re.error) as error:
                found.append(f"- {lesson.get('id', '?') if isinstance(lesson, dict) else '?'}: unreadable detector ({error})")
                continue
            hits = [i for i, (k, event) in enumerate(events, 1) if k == kind and detect.search(event)]
            if hits:
                found.append(f"- {name} ({', '.join(f'#{i}' for i in hits)}): {text}")
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness", choices=["claude", "codex"])
    parser.add_argument("--transcript")
    parser.add_argument("--cwd", default=os.getcwd())
    parser.add_argument("--lessons", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lessons.jsonl"))
    parser.add_argument("--out")
    args = parser.parse_args()

    harness = args.harness or ("claude" if os.environ.get("CLAUDE_CODE_SESSION_ID") else "codex")
    path = args.transcript or (find_claude() if harness == "claude" else find_codex(args.cwd))
    if not path:
        sys.exit("No transcript found. Pass --transcript PATH.")
    with open(path) as f:
        lines = [json.loads(l) for l in f if l.strip()]
    is_codex = lines and lines[0].get("type") == "session_meta"
    events = list((codex_events if is_codex else claude_events)(lines))

    counts = {k: sum(1 for kind, _ in events if kind == k) for k in ("user", "assistant", "tool", "error")}
    out = [
        f"# Session digest\n",
        f"Source: `{path}` ({'Codex' if is_codex else 'Claude Code'})",
        f"User messages: {counts['user']} | assistant messages: {counts['assistant']} | tool calls: {counts['tool']} | errors and blocks: {counts['error']}\n",
        "Legend: U user, A assistant, T tool call, E error, block, or denial. Numbers are digest order, for citing.\n",
    ]
    label = {"user": "U", "assistant": "A", "tool": "T", "error": "E"}
    for i, (kind, text) in enumerate(events, 1):
        out.append(f"{i}. **{label[kind]}** {clip(text, MAX[kind])}")
    seen = recurrences(events, args.lessons)
    out.append("\n## Known lessons seen again\n")
    out.append("\n".join(seen) if seen else "No known lesson recurred.")
    digest = "\n".join(out) + "\n"
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            f.write(digest)
        print(f"Wrote {args.out}: {len(digest)} chars, {len(events)} events, {counts['error']} errors and blocks.")
    else:
        try:
            sys.stdout.write(digest)
        except BrokenPipeError:
            pass


if __name__ == "__main__":
    main()
