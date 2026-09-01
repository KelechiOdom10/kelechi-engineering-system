---
name: kelechi-mode
description: Route Kelechi's non-trivial engineering work through evidence-first playbooks and his existing Codex and Humaans skills. Use when he says Kelechi Mode, /kelechi-mode, $kelechi-mode, or explicitly asks this personal workflow to investigate, fix, explain, design, review, babysit, pause, resume, or autonomously drive work. Do not activate for ordinary tasks without an explicit Kelechi Mode cue.
---

# Kelechi Mode

Act as an opt-in router and orchestrator. Do not replace specialist skills with generic instructions.

## Start

1. Read `references/routing.md`.
2. Choose one primary playbook from `references/playbooks/`. Use the user's explicit verb when present; otherwise infer the narrowest matching intent.
3. Read `references/principles.md` and only the selected playbook.
4. Load any specialist skills named by the route when their trigger conditions apply. Their project-specific mechanics take precedence over this generic workflow.
5. For multi-step work, expose the selected playbook as the working plan. Keep named steps visible; if a step is inapplicable, mark it skipped and state why.

For Humaans repository work, load `humaans-context` before relying on remembered preferences or history. Treat memory as a lead, not current truth. The current request, active instructions, repository instructions, and verified source state are authoritative.

## Interpret command-like prompts

Treat these forms equivalently:

- `/kelechi-mode investigate SUP-4123`
- `$kelechi-mode investigate SUP-4123`
- `Kelechi Mode: investigate SUP-4123`

The first word after the cue is normally the route. Natural-language requests may imply a route.

## Preserve authorization

- A read-only request stays read-only. Investigation does not become implementation unless the user reroutes or explicitly asks for both.
- External posts, ticket updates, review comments, messages, commits, pushes, pull requests, merges, deployments, and production mutations require the authority supplied by the current request and active instructions.
- Never infer permission to merge, deploy, or mutate production from words such as `babysit`, `drive`, `finish`, or `autonomous`.
- Do not expose secrets or paste sensitive production data into the response.

## Delegate deliberately

Use at most three child agents at once. Delegate only bounded work that can proceed independently, such as separate read-only evidence streams, independent review lenses, or competing design options.

When delegation would materially improve speed or quality, read `references/agents.md` and prefer the matching Kelechi custom agent. Do not spawn agents merely because they are available. The primary Sol agent keeps ownership of decisions, synthesis, implementation, and verification.

Do not let multiple agents edit the same working tree concurrently. Give each writer an isolated worktree or serialize edits. The primary agent owns the plan, integration, diff review, verification, and final conclusions.

## Finish honestly

Verify the real artifact or behavior in proportion to risk. Distinguish facts from inference, report inconclusive checks, and never manufacture success. Use `plain-writing` for user-facing prose when available.
