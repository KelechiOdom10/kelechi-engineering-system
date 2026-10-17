#!/usr/bin/env python3
"""Condense a Claude Code or Codex session transcript into a reviewable digest.

Usage: digest.py [--harness claude|codex] [--transcript PATH] [--cwd DIR] [--out FILE]
Without --transcript, finds the current session. Claude Code: CLAUDE_CODE_SESSION_ID, under
CLAUDE_CONFIG_DIR (default ~/.claude).
Codex: the newest rollout whose session cwd is --cwd (default: the current directory).
--harness defaults to claude when CLAUDE_CODE_SESSION_ID is set, otherwise codex.
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
REMINDER = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
LEADING_XML = re.compile(r"\A\s*<([A-Za-z_][\w-]*)[^>]*>.*?</\1>\s*", re.S)
HEADING = re.compile(r"^#{1,6} .*$", re.M)
SHORT_REQUEST = 1200
REQUEST_TAIL = 4000
MAX = {"user": SHORT_REQUEST + REQUEST_TAIL, "assistant": 700, "tool": 220, "error": 500}


def clip(text, limit):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[:limit] + " [...]"


def keep_request(text):
    """Harnesses prepend long context to a user turn; the request typed after it is what matters.

    Keeps the first line, which names who or what sent the message, and the end: the section
    after the last markdown heading when it fits, otherwise the last REQUEST_TAIL characters.
    """
    text = text.strip()
    if len(text) <= SHORT_REQUEST:
        return text
    first = text.split("\n", 1)[0][:200]
    headings = list(HEADING.finditer(text))
    start = headings[-1].end() if headings and len(text) - headings[-1].end() <= REQUEST_TAIL else len(text) - REQUEST_TAIL
    start = max(start, len(first))
    if not text[start:].strip():
        start = max(len(first), len(text) - REQUEST_TAIL)
    return f"{first} [... {start - len(first)} chars of leading context elided ...] {text[start:].strip()}"


def strip_leading_xml(text):
    while match := LEADING_XML.match(text):
        text = text[match.end():]
    return text


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
                    output = text_of(block.get("content"))
                    if block.get("is_error") or SIGNAL.search(output[:400]):
                        yield "error", output
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
            output = payload.get("output")
            output = output if isinstance(output, str) else json.dumps(output)
            if SIGNAL.search(output[:600]):
                yield "error", output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness", choices=["claude", "codex"])
    parser.add_argument("--transcript")
    parser.add_argument("--cwd", default=os.getcwd())
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
