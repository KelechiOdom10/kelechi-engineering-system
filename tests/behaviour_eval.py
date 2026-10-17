"""Does a changed instruction change what the agent does? Costs real model calls; run when skill prose changes.

python3 tests/behaviour_eval.py [--base origin/main] [--model opus] [--only NAME]   # old vs new, scored by script
python3 tests/behaviour_eval.py --check                                           # validate the cases, no model calls

Each case in behaviour_cases.json injects the named skill files into the system prompt, once as they are at
--base and once as they are in the working tree, with every installed skill and MCP server switched off. Its
assertions are regular expressions over the reply, so a pass is decided by this script, not by a model.
A case whose files do not exist at --base runs the old side with no instructions.
"""
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CASES = os.path.join(ROOT, "tests", "behaviour_cases.json")
FIELDS = {"name", "files", "prompt", "expect", "expect_not"}


class HarnessError(Exception):
    """The run itself failed (auth, API, CLI), so the reply means nothing."""


def load_cases():
    cases = json.load(open(CASES))
    problems = []
    for case in cases:
        name = case.get("name", "?")
        if set(case) - FIELDS or not {"name", "files", "prompt"} <= set(case):
            problems.append(f"{name}: fields must be {sorted(FIELDS)}")
        if not case.get("expect") and not case.get("expect_not"):
            problems.append(f"{name}: needs expect or expect_not")
        for path in case.get("files", []):
            if not os.path.isfile(os.path.join(ROOT, path)):
                problems.append(f"{name}: no file {path}")
        for pattern in case.get("expect", []) + case.get("expect_not", []):
            try:
                re.compile(pattern)
            except re.error as error:
                problems.append(f"{name}: bad pattern {pattern!r}: {error}")
    if len({c.get("name") for c in cases}) != len(cases):
        problems.append("case names must be unique")
    return cases, problems


def instructions(files, base):
    parts = []
    for path in files:
        if base is None:
            text = open(os.path.join(ROOT, path)).read()
        else:
            shown = subprocess.run(["git", "show", f"{base}:{path}"], cwd=ROOT, capture_output=True, text=True)
            if shown.returncode != 0:
                continue
            text = shown.stdout
        parts.append(f"<instructions file=\"{path}\">\n{text}\n</instructions>")
    return "\n\n".join(parts)


def reply(case, base, model, cwd):
    system = "Follow these instructions for this task. Reply in text only; do not use tools.\n\n" + instructions(case["files"], base)
    out = subprocess.run(
        ["claude", "-p", case["prompt"], "--model", model, "--max-turns", "1", "--output-format", "json",
         "--append-system-prompt", system, "--disable-slash-commands", "--strict-mcp-config", "--no-session-persistence"],
        cwd=cwd, capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL,
    )
    try:
        result = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise HarnessError((out.stderr or out.stdout)[:200])
    if result.get("is_error") and result.get("subtype") != "error_max_turns":
        raise HarnessError(str(result.get("result"))[:200])
    return result.get("result") or ""


def score(case, text):
    missing = [p for p in case.get("expect", []) if not re.search(p, text)]
    present = [p for p in case.get("expect_not", []) if re.search(p, text)]
    return not missing and not present, missing + [f"not {p}" for p in present]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--model", default="opus")
    parser.add_argument("--only")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--parallel", type=int, default=4)
    parser.add_argument("--out", help="write every reply here, for reading the failures")
    args = parser.parse_args()

    cases, problems = load_cases()
    if problems:
        sys.exit("behaviour_cases.json:\n- " + "\n- ".join(problems))
    if args.check:
        print(f"{len(cases)} behaviour cases valid")
        return
    cases = [c for c in cases if not args.only or c["name"] == args.only]
    cwd = tempfile.mkdtemp(prefix="behaviour-eval-")
    subprocess.run(["git", "init", "-q"], cwd=cwd, check=True)
    runs = [(case, side) for case in cases for side in ("old", "new")]
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        try:
            replies = list(pool.map(lambda run: reply(run[0], args.base if run[1] == "old" else None, args.model, cwd), runs))
        except HarnessError as error:
            sys.exit(f"Harness error, no case scored: {error}")

    results = {}
    for (case, side), text in zip(runs, replies):
        results[(case["name"], side)] = (*score(case, text), text)
    regressions = failures = 0
    for case in cases:
        old_ok, _, _ = results[(case["name"], "old")]
        new_ok, why, _ = results[(case["name"], "new")]
        failures += not new_ok
        regressions += old_ok and not new_ok
        print(f"{'PASS' if new_ok else 'FAIL'}  old {'pass' if old_ok else 'fail'}  {case['name']:40} {'; '.join(why)[:120]}")
    if args.out:
        with open(args.out, "w") as f:
            for (name, side), (ok, why, text) in results.items():
                f.write(f"## {name} ({side}): {'pass' if ok else 'fail ' + '; '.join(why)}\n\n{text}\n\n")
    print(f"\nnew {len(cases) - failures}/{len(cases)} passed, {regressions} regressions against {args.base}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
