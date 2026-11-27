# Kelechi Engineering System

An evidence-first engineering workflow by Kelechi Odom, packaged as one plugin for **Claude Code** and **Codex**.

**Kelechi Mode** routes engineering work to a playbook. Specialist skills do the detailed work, while diagnosis, verification, judgement, and authority stay explicit.

```text
request
  → pick a route
  → gather evidence
  → use the right specialist
  → make the smallest coherent change
  → verify the real boundary
  → report plainly
```

Persistence never expands authority.

For repeatable engineering work, use the [software-factory skill](skills/software-factory/SKILL.md)
and [delivery collector](docs/delivery.md). Tasks get explicit triggers, shared-state event deduplication,
sequential check receipts and independent findings tied to current source. Readiness means ready
for human review; protected CI and repository policy still own merge authority.
The [seeded research loop](docs/research-loop.md) feeds this workflow with focused,
verified proposals while keeping exploratory priorities separate from delivery acceptance.
The [PR completion helper](docs/pr-completion.md) adds a review-source ledger and fresh,
exact-commit CI assessment to the existing babysit route.

For the saved workflows, use [research](skills/research/SKILL.md) for an unsettled decision,
[create-canvas](skills/create-canvas/SKILL.md) for preserved live design alternatives,
[ui-sweep](skills/ui-sweep/SKILL.md) for inspected state catalogs, and
[friction-log](skills/friction-log/SKILL.md) for failures captured while working.

## Install

**Claude Code**

```bash
claude plugin marketplace add KelechiOdom10/kelechi-engineering-system
claude plugin install kelechi@kelechi
```

On a Humaans machine, also install `kelechi-humaans@kelechi`.

**Codex.** The personal marketplace at `~/.agents/plugins/marketplace.json` points `./plugins/kelechi-mode` at a checkout of this repo (a symlink). On a Humaans machine, add a `kelechi-humaans` entry pointing `./plugins/kelechi-humaans` at the checkout's `adapters/humaans`; `reinstall.sh` installs the adapter whenever the marketplace lists it.

After changing the plugin, run `./scripts/reinstall.sh` from the checkout you want installed. It points Claude Code's `kelechi` marketplace and the Codex marketplace links at that checkout, reinstalls both, and prints the branch and commit it installed, with a warning when that is not a clean `main`. It bumps the Codex cache version and restores it afterwards, so the tree stays clean.

## Use

| Claude Code | Codex | Route |
| --- | --- | --- |
| `/kelechi:kickoff` | `$kickoff` | new product or surface: decisions, then a walking skeleton |
| `/kelechi:investigate` | `$kelechi-mode investigate` | read-only diagnosis |
| `/kelechi:fix` | `$kelechi-mode fix` | reproduce, root-cause, fix, verify |
| `/kelechi:feature` | `$kelechi-mode feature` | an end-to-end verified slice |
| `/kelechi:architect` | `$architect` | settle callers, types, and placement before coding a boundary |
| `/kelechi:refactor` | `$kelechi-mode refactor` | behaviour-preserving change |
| `/kelechi:perf` | `$kelechi-mode performance` | measure, trace, improve |
| `/kelechi:review` | `$kelechi-mode review` | read-only rigorous review |
| `/kelechi:blast-radius` | `$blast-radius` | what a change breaks outside its diff, with the safety fact proven by running code |
| `/kelechi:no-comments` | `$no-comments` | strip narrating comments and encode the rest as renames, types, or tests |
| `/kelechi:interrogate` | `$interrogate` | adversarial multi-lens review, with a cross-model reviewer from the other CLI |
| `/kelechi:design` | `$kelechi-mode design` | recommend a shape |
| `/kelechi:prototype` | `$kelechi-mode prototype` | settle a fork by observation |
| `/kelechi:explain` | `$kelechi-mode explain` | how and why |
| `/kelechi:babysit` | `$kelechi-mode babysit` | drive a PR to green |
| `/kelechi:reflect` | `$reflect` | turn a session's lessons into approved skill, hook, project, or memory edits |
| `/kelechi:verify-skill` | `$verify-skill` | create or refresh a repo's verify skill: start safely, sign in, prove each flow |
| `/kelechi:pause`, `/kelechi:resume` | `$kelechi-mode pause`, `resume` | park and pick up work |
| `/kelechi:autonomous` | `$kelechi-mode autonomous` | run to a terminal condition |
| `/kelechi:factory` | `$software-factory` | define or run a bounded, repeatable engineering task |

Once entered, the mode stays on for the session.

## Repository map

| Path | Purpose | Harness |
| --- | --- | --- |
| `.claude-plugin/` | Claude plugin manifest and the `kelechi` marketplace | Claude |
| `.codex-plugin/` | Codex plugin manifest | Codex |
| `skills/kelechi-mode/` | Router, routes, principles, playbooks, agent map, working-state policy | both |
| `skills/kelechi-engineering-standard/` | Kelechi's personal standard: types, architecture, testing, frontend, comments, AI features, default stack | both |
| `skills/*` (others) | PR writing, validation, support investigation, domain modelling, frontend, component API, backend service design | both |
| `agents/` | `explorer` (haiku), `investigator` (sonnet), `comment-reviewer` (sonnet), `reviewer` (opus) | Claude |
| `codex/agents/` | The same roles as Codex agent definitions, copied into every Codex home's `agents/` by `scripts/reinstall.sh` | Codex |
| `commands/` | `/kelechi:<route>` shortcuts | Claude |
| `hooks/` | Portable guardrails, one file shared by both harnesses | both |
| `adapters/humaans/` | Humaans adapter plugin: repository routing and review layer | both |
| `templates/` | Domain, design brief, backend, frontend, support, validation, adapter templates | both |
| `scripts/reinstall.sh` | Refreshes the installed plugins in Claude Code and Codex from this checkout, links `~/.agents/skills` into every Claude home, and points OpenCode and Antigravity at this checkout's skills | all |
| `scripts/setup-beacon.sh` | Sets up [Beacon](https://beacon.sh) session recording, its MCP server, and its skills in every Claude Code and Codex home. Cloud metadata-only by default; `--local`, `--standard`, `--no-backfill` | both |
| `scripts/check.sh` | Validates both plugins in both harnesses, runs every test suite, and checks token budgets. Run before every PR. | both |
| `tests/` | Hook, digest, boundary-checker, and token-budget tests, all run by `scripts/check.sh` | n/a |

## Hooks

Each hook reads the repository's own toolchain and does nothing where it does not apply.

- **Package manager.** Blocks a package manager that disagrees with the lockfile, and raw `vitest`, `oxlint`, `oxfmt`, or `npx` in a Vite+ repo.
- **Titles.** Commit subjects and PR titles use Conventional Commits, carry no ticket ids, and PR titles stay under 72 characters.
- **Attribution.** Blocks AI attribution in commits, PR bodies, and comments.
- **PR Lens canvas.** Blocks uploading a diagram to prlens.dev unless Kelechi asked for a canvas (`KELECHI_CANVAS=yes`); never allowed in the Humaans repo.
- **Format on edit.** Runs the repository's formatter (`vp fmt`, oxfmt, Biome, or Prettier) on edited files.
- **Comment nudge.** Flags new source comments that are not a non-obvious why.
- **Stale state.** At session start, lists `.kelechi/` working files that are old, orphaned, merged, or consumed.

## Portability

Customer data, credentials, production details, and company source stay out of this repository. Company-specific practice lives in an adapter under `adapters/`. See [portability](docs/PORTABILITY.md) and [companion skills](docs/COMPANION-SKILLS.md).

See the [daily engineering workflow](docs/daily-workflow.md) for when to use each capability and what evidence to expect.
