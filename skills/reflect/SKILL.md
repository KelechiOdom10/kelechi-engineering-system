---
name: reflect
description: Turn a session's lessons into concrete, approved edits - to Kelechi Mode skills, hooks, and checks, to the project's own instructions, or to memory. Use for "reflect", /kelechi:reflect, "what did we learn", or after a long or painful task.
---

# Reflect

Mine a session for durable lessons and route each one to the place that will change future behaviour. A lesson is durable when it would recur on another task; a one-off is not a lesson. Nothing is applied until Kelechi approves.

## 1. Scope

Reflect on the current session unless Kelechi names a transcript. Say which. Skip, and say so, when the session was short or went exactly as the skills already prescribe.

## 2. Digest

```bash
python3 <this skill>/scripts/digest.py --out .kelechi/reflect/digest.md
```

It finds the current Claude Code or Codex session (pass `--harness`, or `--transcript PATH` for a named one) and condenses it to user messages, assistant messages, tool calls, and every error, block, or denial, numbered for citing. Read the digest yourself before spawning anyone.

## 3. Mine

Read `references/lenses.md`. In one batch, spawn three read-only subagents on the strongest available model, one per lens, and wait for all three. Each gets the digest path, the plugin's `skills/` and `hooks/` paths so it can check what is already encoded, and its lens prompt.

## 4. Triage

Read `references/routing.md`. For every candidate:

1. Confirm its evidence in the digest. No evidence, no lesson.
2. Check it is not already encoded: search the skills, hooks, the project's `AGENTS.md`/`CLAUDE.md`, and memory.
3. Test it for durability: would it recur on a different task? Would the proposed edit change behaviour, or is it something the model already does by default?
4. Choose the destination and the strongest form: a check, hook, script, or test before a sentence of prose.

## 5. Propose

Present the result in the format in `references/routing.md`: Accepted (each with its exact proposed edit), Rejected (one line why), Backlog. Wait for Kelechi to approve all, some, or none. Edits to skills change every future session in both harnesses.

## 6. Apply

For each approved item, follow its destination's procedure in `references/routing.md`: plugin edits on a branch with one commit per lesson, tests, `scripts/reinstall.sh`, and a draft PR; project edits on a branch in that repository; memory written directly; backlog issues created only because Kelechi approved them in step 5.

## 7. Report

List what changed and where (PR links, files, memory entries), what went to backlog, and what was rejected. Delete `.kelechi/reflect/`.
