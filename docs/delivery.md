# Delivery evidence and factory tasks

A task definition describes repeatable work. An event claims one execution. A run collects checks and independent review. Readiness is derived from current evidence; it never grants merge or deployment authority.

The first version uses Python 3.10+ and Git on macOS/Linux, matching this repository's existing scripts. It needs no package installation, provider key, server or new scheduler.

## Start and verify a change

Copy `examples/delivery-task.json` outside the plugin checkout and adapt it to the repository. Choose acceptance criteria before writing tests. Declare argv checks rather than shell commands. Check directories are relative to the target repository and cannot escape it. Check commands are trusted code: read a task before executing it.

```bash
python3 /path/to/plugin/scripts/delivery.py init task.json --repo /path/to/repository --base origin/main --key request-123 --owner actual-author-session-reference
```

Use the printed absolute run directory in subsequent commands:

```bash
python3 /path/to/plugin/scripts/delivery.py run /printed/run
python3 /path/to/plugin/scripts/delivery.py run /printed/run --check delivery-regressions
python3 /path/to/plugin/scripts/delivery.py status /printed/run
```

Checks run sequentially, directly without a shell. Each result retains actual argv, working directory, process exit status, timeout, source before/after and a hashed output log. A missing executable records failure. A timeout stops the process group; successful commands cannot leave detached children within that group. This is a check runner, not a service manager or an OS sandbox.

Each check owns a separate receipt directory; identifiers must be unique ignoring case. A numbered attempt is persisted before launch and consumes budget immediately; only its completed result can pass. SIGINT/SIGTERM/SIGHUP stop the child process group and leave the attempt incomplete. Finalization uses a flushed temporary file and atomic replacement. A hard-killed collector still leaves an incomplete attempt; its host must clean up processes on forced termination. Version 1 development records cannot be reused by the version 2 collector.

Runs default to ignored `.kelechi/delivery/` inside the workspace, where ordinary workspace-write sandboxes can store evidence without modifying `.git`. State inside a checkout must be Git-ignored. A host coordinating multiple worktrees must supply the same `--state-dir` to each and grant access to that directory. Claims are namespaced by the common Git directory's identity; unrelated repositories do not collide. Without a shared store, cross-worktree deduplication is not established.

Repeating a task/event in the same store fails instead of starting another owner. Claims remain after completion or failure; use the existing record to continue. An interrupted initialization can leave a partial claim that needs owner reconciliation; do not delete it automatically or start another key to evade ownership. A genuinely new event needs a new key. The tool serializes record writes, but cannot stop arbitrary tools or people from editing the checkout concurrently. The host owns writer isolation. If state is not writable in the active sandbox, stop and configure an allowed directory; do not disable the sandbox. Readiness/status use the existing lock without opening it for writing.

## Independent review

Give a fresh reviewer the acceptance contract, scoped diff, repository instructions and relevant consumers. Require a realistic trigger, reachable failure and source or executable evidence. Structural review and behavioral review answer different questions. The reviewer may return no findings; it must state the scope and unverified boundaries.

The reviewer supplies this JSON artifact. `revision` is the opaque digest printed by `status`, not a Git SHA. `reviewer` must be its actual session/job reference, different from the recorded author.

```json
{
  "version": 1,
  "revision": "digest-from-status",
  "reviewer": "actual-independent-session-reference",
  "scope": "Acceptance criteria, changed code and downstream consumers; name unverified boundaries here",
  "findings": [
    {
      "id": "F1",
      "severity": "blocking",
      "summary": "A concrete reachable failure",
      "evidence": "source path and line or executable counterexample",
      "disposition": "open"
    }
  ]
}
```

```bash
python3 /path/to/plugin/scripts/delivery.py review /printed/run reviewer.json
python3 /path/to/plugin/scripts/delivery.py ready /printed/run
```

An empty findings list is valid. Findings are `blocking` or `advisory`. A later review must keep finding IDs stable. Omitting an old blocker leaves it open. Closing one requires `fixed` or `disproved` plus `resolution_evidence`. The first version deliberately has no automatic risk-acceptance path: an unresolved blocker keeps the run incomplete. An authorized owner can make a separate repository decision, but the agent must not describe that as a green run.

The collector retains reviews across revisions. The latest review must cover the current revision, and every check must pass at that revision. Source identity includes HEAD, tracked and non-ignored untracked file contents, modes and symlink targets. Any source change invalidates evidence conservatively, even an empty commit. Submodules/nested repositories need separate records. Ignored builds, dependencies, environment variables, external systems and linked file contents are not covered by this digest; verification recipes must establish those inputs independently.

## Trust and authority

Local evidence is an audit aid, not a security boundary against an agent able to rewrite the entire store. Reviewer references are attestations, not authenticated identities. The tool cannot establish semantic correctness, reviewer competence, budgeted model spend or an authorized human's acceptance. Preserve originating host/CI records and compare claims with actual artifacts.

For a shared readiness gate, run required commands from a trusted checkout in protected CI. Let CI own its results, artifact collection and current commit binding. Existing branch protection, code owners and release policy remain authoritative. This CLI does not install hooks, approve PRs, push, merge, schedule tasks or send messages.

## A small factory

Start with an explicitly requested support fix, a test repair or a UI change whose verification is known. The host receives the event, claims its key, runs the ordinary workflow, gathers evidence and returns the short behavior/proof/risk/decision summary. Default budgets are three check attempts and three review rounds; exhausted budgets require reassessment. Choose time and model budgets in the host before starting.

For UI work, record the serving process checkout, fixture and build identity. Capture actual states and widths, exercise keyboard/error behavior and critique the chosen visual direction. Use the existing component showcase for alternatives before building a new canvas.

Keep real company PR snapshots and expected defects in a private evaluation corpus. Compare existing and candidate reviews at the same model and budget; hide answers and later fixes. Include clean controls, hold out related defect families together, and track live misses and human intervention as well as replay results. A small pilot does not justify a universal safety rate.

Prepare scoped packets without exposing hidden labels:

```bash
python3 /path/to/plugin/scripts/review_replay.py /private/cases.json --repo /private/repository --output /private/new-packets
```

The private manifest has `version: 1` and a `cases` list. Each case declares `id`, full immutable `base` and `head` SHAs, behavior `intent`, regular-file `paths` and private `expected` labels (empty for a clean control). Optional `context_paths` supplies actual producers, consumers and adjacent contracts at the same pinned head without expanding the changed-file diff. Packets contain only intent, scoped diff, head source and digests. The preparer never copies labels or unknown manifest fields. It neither creates checkouts nor invokes models. Missing dependencies outside the packet are unverified, not assumed correct. A broad value type and a synthetic counterexample do not establish a reachable producer path. Keep run provenance and adjudication outside reviewer packets; a label match requires a verified mechanism, not keyword similarity.
