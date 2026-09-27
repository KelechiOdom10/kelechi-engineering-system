"""Which skill does each prompt trigger? Costs real model calls; run when descriptions change.

python3 tests/trigger_eval.py [--model opus] [--parallel 4]
Runs in an empty scratch git repository so no project instructions interfere.
"""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import tempfile

class HarnessError(Exception):
    """The run itself failed (auth, API, CLI), so no skill result means nothing."""


CASES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trigger_cases.json")


def skills_fired(prompt, model, cwd):
    out = subprocess.run(
        ["claude", "-p", prompt, "--model", model, "--max-turns", "2", "--allowedTools", "Skill",
         "--output-format", "stream-json", "--verbose"],
        cwd=cwd, capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL,
    )
    fired = []
    for line in out.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result" and event.get("subtype") != "error_max_turns" and (event.get("is_error") or "Failed to authenticate" in str(event.get("result"))):
            raise HarnessError(str(event.get("result"))[:200])
        message = event.get("message")
        if not isinstance(message, dict):
            continue
        for block in message.get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                fired.append(block.get("input", {}).get("skill"))
    return fired


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="opus")
    parser.add_argument("--parallel", type=int, default=4)
    args = parser.parse_args()
    cases = json.load(open(CASES))
    cwd = tempfile.mkdtemp(prefix="trigger-eval-")
    subprocess.run(["git", "init", "-q"], cwd=cwd, check=True)

    try:
        skills_fired(cases[0]["prompt"], args.model, cwd)
    except HarnessError as error:
        sys.exit(f"Harness error, no case scored: {error}")
    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        try:
            results = list(pool.map(lambda c: skills_fired(c["prompt"], args.model, cwd), cases))
        except HarnessError as error:
            sys.exit(f"Harness error, no case scored: {error}")

    failures = 0
    for case, fired in zip(cases, results):
        first = fired[0] if fired else None
        if "expect" in case:
            ok = first == case["expect"]
            want = case["expect"]
        else:
            ok = case["expect_not"] not in fired
            want = f"not {case['expect_not']}"
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  want {want:40}  got {first or 'no skill'}  | {case['prompt'][:60]}")
    print(f"\n{len(cases) - failures}/{len(cases)} passed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
