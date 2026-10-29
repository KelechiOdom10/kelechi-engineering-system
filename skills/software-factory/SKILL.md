---
name: software-factory
description: Define and run repeatable engineering tasks with explicit triggers, ownership, duplicate prevention, evidence and human handoffs. Use when building a software factory or automating a recurring engineering workflow.
---

# Software factory

A factory is a collection of bounded tasks using the existing host. Start with one task whose outcome and failure are observable. Read [delivery](../../docs/delivery.md) for the CLI and record formats; resolve the plugin root from this skill's location.

## Define the task

Use [the task example](../../examples/delivery-task.json). Establish the trigger and stable event key, intended outcome, acceptance criteria independent of the implementation, declared write scope, checks, budgets, stop conditions and the exact point work returns to a person. Empty `writes` means read-only intent. Scope and human decisions belong to the repository's owner; this definition does not grant authority.

Choose a task with an existing verification recipe. For unfamiliar or unsettled work, use investigation or design first. For visual work, choose the task, reference and direction before implementing; preserve meaningful component alternatives in the existing showcase. Browser interaction checks and visual critique prove different facts.

For unsettled choices, use `research` and [the research loop](../../docs/research-loop.md). For live visual alternatives use `create-canvas`, then `ui-sweep` for actual state evidence. Research may revise leads within fixed bounds; a validated discovery becomes a separate delivery task. A successful collector run does not prove research is true.

## Run one event

1. Use `delivery.py init` to claim the task/event. Reuse the printed run path to continue; a duplicate claim in the same store stops another owner. Default state is ignored `.kelechi/delivery` in this checkout. For multiple checkouts, pass the same host-writable `--state-dir` to each and grant that directory through the host. Do not bypass a sandbox to write evidence.
2. Give the existing feature/fix route the acceptance criteria and scope. Keep one writer. The host supplies isolation, provider calls and events; use its supported completion notifications instead of polling.
3. Run declared checks with `delivery.py run`. Inspect the actual logs. The collector bounds command time and records source before and after; source-mutating checks need a rerun against the result.
4. For consequential work, give a fresh reviewer the requirement and affected boundaries before the author's conclusions. Trace readers, writers, fallbacks, legacy states, retries and final writes where relevant. Challenge test expectations against the intended behavior. Record the review using `delivery.py review`.
5. Run `delivery.py ready` against the final state. Missing proof or open blockers means incomplete. A draft PR can still carry incomplete work with a clear account of the gap. Readiness means ready for human review, never permission to merge or deploy.

Three check attempts and three review rounds are a starting budget, configurable per task. The host also needs an explicit time/model budget: this CLI does not enforce model spend. At the limit, reassess the approach instead of creating another event key to evade it.

## Improve the task

Record friction as expected behavior, actual failure and evidence. Group recurrences and prefer a fixture, type, script or check over another prompt paragraph. Keep traces separate from verified reusable lessons. Add tasks only after the first works; schedule them only when requested. Historical review evaluation and live outcomes determine whether to expand autonomy, not successful task counts.

Use `friction-log` during work to retain material failures and interventions; later reflection consumes verified patterns instead of reconstructing them from memory.
