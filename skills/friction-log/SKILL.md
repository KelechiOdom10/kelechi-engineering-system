---
name: friction-log
description: Record material agent or developer friction during work, with expected versus actual behavior, attempted resolution, evidence and a concrete action. Use for log-friction requests or recurring setup, tool, documentation and follow-through failures; feeds later reflection.
---

# Friction log

Capture useful failures while they happen, rather than reconstructing a success story at the end. Logging supports the task; it does not replace completing it or override authority.

1. Use a requested destination or one ignored task-local Markdown record, such as `.kelechi/friction/<task>.md`. Reuse the current record. Start with task, source checkout/head, known model/harness, goal and actual bounds. Summarize the request; do not copy full conversations, credentials, customer records or production payloads by default. Preserve only minimal redacted evidence needed to explain the failure.
2. Append a stable-ID entry when an error, confusing instruction, dead end, unnecessary intervention or repeated workaround materially changes the work. Use [the entry shape](../../templates/friction-entry.md). Record expected behavior, observed result, exact evidence/source, attempts and current resolution. Mark inferred explanations and unavailable evidence. Do not invent timestamps, durations, costs or source tags.
3. Update resolution with the actual successful method or leave it unresolved. Keep failed attempts visible. Do not retry an unchanged timeout or repeat failed fixes indefinitely; reassess method and task budget. A denied operation is evidence, not permission to bypass it. Continue independent authorized work while necessary approvals remain outstanding.
4. Treat user corrections as requirements to reconcile. Record the missed deliverable and the concrete action that closes it, not just that the user was unhappy. Answer direct questions, incorporate steering, and preserve the original objective unless explicitly replaced.
5. Every material friction entry needs a specific follow-up: documentation, executable tooling/code, or an investigation with its next falsifiable question. Prefer fixtures, tests, types and scripts for recurring issues over another broad prompt rule. Do not silently edit installed skills/config or publish a lesson because a log exists.
6. Finish with resolved/open counts, decisive fixes, remaining actions and actual measured effort when available. Link the log; summarize only what matters in chat. Feed verified repeated patterns into `reflect`; raw observations are not durable universal rules. Keep this compact and avoid duplicating the host's entire tool trace.

Adapted from [Aurora Scharff's friction-log](https://github.com/aurorascharff/agent-friction-skill/blob/main/SKILL.md), retaining live evidence and actions while minimizing prompt/customer capture and duplicate logging.
