---
name: verify-skill
description: Create or maintain a repository's verify skill - how to start the app safely, sign in locally, and prove each key flow. Use for "verify skill", /kelechi:verify-skill, a repo with no scripted way to prove its behaviour, or when the verify skill's feature map has drifted.
---

# Verify skill

Give each repository a skill that lets any agent prove the app works without rediscovering how to run it. It lives in the repository at `.claude/skills/verify/`, and `AGENTS.md` points to it so Codex reads it too. Write it for an agent reading it cold, mid-task.

Pick a mode and say which: **create** when `.claude/skills/verify/` is missing, **maintain** when it exists.

## Create

1. **Interview the repo, not Kelechi.** From scripts, README, `AGENTS.md`, config, and a live run, establish:
   - **Surfaces** users touch: web UI, API, CLI, jobs. The primary one first.
   - **Run:** the exact start commands, env files, ports, and the signal that it is ready.
   - **Isolation:** its own ports and a throwaway database (a new container or database name) so it never touches the main checkout's dev data or another project's containers.
   - **Sign-in:** a local test user and how local auth delivers links or codes, with no real email, account, or credential.
   - **Drive and observe:** the browser tool or Playwright for UI, HTTP for APIs, the CLI itself; what evidence proves a result.
   - **Gotchas** the repo already knows: toolchain rules, busy ports, required env.

   If the app does not start as-is, fix it on a branch or report the blocker precisely before writing anything.
2. **Write it** from `references/template.md`: `SKILL.md` plus `features/README.md` and one file for each of the top 3-5 user flows. Every command is real and every placeholder is filled.
3. **Point to it** with one line in `AGENTS.md`: `Proving behaviour: .claude/skills/verify/SKILL.md`.
4. **Prove it cold.** Hand only the generated skill to a fresh subagent (or a new session) and ask it to launch, run the doctor check, drive one mapped flow, capture evidence, and clean up. Everything it had to rediscover is a gap: fix the skill and repeat. Evidence must survive cleanup.
5. **Commit** on a branch: `docs: add verify skill`.

Claude Code protects `.claude/`, so an unattended session may be refused the write. Then write the files to `.kelechi/verify/` and give Kelechi one command that moves them into `.claude/skills/verify/` and commits; do not route around the refusal. When the sandbox blocks running the app (as Codex's often does), write the skill, mark it unproven, and say what could not run.

## Maintain

1. Read `verified-at` in `features/README.md` and diff from that commit to `HEAD` against the files each feature lists.
2. Re-drive every feature whose files changed, add flows for new routes or commands, and delete features that no longer exist. Fix start-up steps that no longer work.
3. Set `verified-at` to the current commit and commit `docs: refresh verify skill`, in one PR.

The review playbook flags a diff that changes a mapped flow without updating its feature file.
