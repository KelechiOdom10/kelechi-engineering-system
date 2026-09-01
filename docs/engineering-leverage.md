# Kelechi Odom — the engineering system behind the work

**July 2025 to September 2026**

The product timeline records what Kelechi shipped at Humaans. This document records a
different body of work: the engineering system he built around that product work.

It is a practical system for turning a vague request, a support escalation, a risky change,
or a pull request into evidence, a small decision, verified code, and a clear hand-off. Its
parts live in the repository, in personal Codex skills, and in a personal Codex plugin called
**Kelechi Mode**.

This is not a claim that an agent replaces engineering judgement. The system makes the
judgement visible, asks for evidence before action, and puts recurring lessons where the next
piece of work can use them.

## The central piece: Kelechi Mode

Kelechi Mode is an original, opt-in Codex plugin. It adapts the useful parts of Cursor's
pstack model to Humaans and to Codex rather than copying it: a route selects the right
playbook, current project skills do the specialist work, and the engineer keeps control of
the decision and every external action.

The plugin has twelve routes:

| Work arriving | Route | What it protects |
| --- | --- | --- |
| A customer issue or unexplained failure | Investigate | Facts, hypotheses, and conclusions stay separate. |
| A known defect | Fix | Diagnosis happens before implementation. |
| New product work | Feature | The work is broken into verifiable units. |
| A known simplification | Refactor | The behaviour stays stable while complexity falls. |
| Slowness or resource use | Performance | The baseline is measured before a change. |
| A change to assess | Review | Findings must be concrete and verified. |
| An uncertain system shape | Design | Decisions and trade-offs are made before code. |
| A question about behaviour or history | Explain | Current source is separated from historical context. |
| A PR that needs driving | Babysit | CI, review, and release boundaries stay explicit. |
| Work to park | Pause | The next engineer gets a durable hand-off. |
| Work to continue | Resume | Prior context is re-checked against current source. |
| Long-running work | Autonomous | Persistence never widens permission. |

The routes are deliberately narrow. A support ticket always starts as an investigation; a
review does not silently become a code change; “keep going” never authorises a deploy or an
external post. This is the distinction that makes a workflow useful around production systems
rather than merely convenient.

```text
request
  → choose a route
  → gather evidence
  → use the relevant specialist skill
  → make the smallest coherent decision or change
  → verify the real boundary
  → write a concise result, PR, or hand-off
```

Kelechi Mode also defines when agents help: independent read-only evidence can be delegated;
the primary engineer retains synthesis, implementation, integration, verification, and
external authority. It includes model-aware roles for codebase mapping, investigations, and
review, while preventing several agents from editing one shared working tree.

## A workflow that compounds knowledge

The system did not start as a single plugin. It grew from repeated engineering problems and
was then moved into reusable forms.

| Period | What was added | What it changed in practice |
| --- | --- | --- |
| Jul 2025 | The first Codex configuration | The repository began carrying an explicit, shared agent setup. |
| Oct 2025 | The first repository instructions and common commands | An agent starts with the project’s real build and migration paths. |
| Jan 2026 | Stronger `AGENTS.md` guidance, scoped instructions, and language-server context | Rules live next to the code they govern instead of in a chat transcript. |
| Feb–May 2026 | Automatic formatting, a review command, specialist reviewer roles, and domain skills | Routine checks happen consistently; deeper review follows the changed surface. |
| Jun–Aug 2026 | Leaner skill structure, dedicated evaluation and debugging playbooks, tighter permissions guidance, and corrected guardrails | The system became easier to load, safer at system boundaries, and based on observed failure modes. |
| Sep 2026 | Kelechi Mode and personal engineering standards | Existing specialist knowledge became one portable, evidence-first operating model. |

The important pattern is maintenance. The agent system was not treated as a document written
once. It was changed when a command was too broad, a test runner had moved, a review process
was too heavy, or a real incident exposed a missing safety boundary.

## The specialised systems

### Support investigation

The personal support skill turns an `SUP-` ticket into a repeatable investigation:

1. Read the ticket and restate the customer, affected person, and symptom.
2. Confirm read-only production access is available.
3. Reproduce the exact reported symptom in data before reading for a plausible cause.
4. Write ranked, falsifiable hypotheses and test one variable at a time.
5. Decide whether the result is configuration, a quick fix, a larger product decision, or a
   request for more information; quantify blast radius when it is a real bug.
6. Produce a short, non-technical write-up for Customer Support without posting it.

This encodes hard-earned discipline: a familiar ticket title is not a diagnosis, the customer
must see the precise problem in the data, and a fix should start only after the cause is known.
It preserves both the technical investigation and the human communication needed to close the
loop.

### Review as routing, not a generic checklist

The repository review command first states what the change does and where its concrete risk
lies. It routes only when the changed surface calls for a specialist:

- Security: authentication, permissions, tenant isolation, caller-controlled identifiers, and
  UI permission gates.
- Backend platform: migrations, queues, MCP contracts, flags, and transaction or hook order.
- Backend services: service logic, query shapes, schema validation, and untested branches.
- Performance: hot queries, loops, queues, batching, and unnecessary fetching.
- Shared packages: public contracts and every downstream consumer.
- Frontend wiring and components: data ownership, interaction states, accessibility, and
  design-system use.

Each reviewer is constrained to its own boundary and reports only source-verified findings at
high confidence. That avoids both shallow “looks fine” review and a long list of speculative
style comments.

### Skills for real Humaans work

The repository contains a growing set of specialist skills for the hard-to-recall parts of
the system: local servers, production and staging logs, traces, the production replica,
debuggers, Playwright, unit tests, E2E tests, ReScript, MCP development and evaluation,
authorisation review, feature-flag cleanup, ownership, PR writing, and risk registers.

They capture the actual command, data, and verification paths of the monorepo. A generic
assistant knows that tests are useful; these skills know which Humaans test runner is current,
where a service lives, when a trace is the better signal than a log, and when an escalation
must stop at a read-only boundary.

### Durable memory, not repeated rediscovery

The Humaans context pack stores verified local lessons from active projects and support work:
production investigation patterns, test and build gotchas, integration failure signatures,
and project-specific decisions. It treats that memory as a lead rather than proof: the current
repository and the current request still win.

That makes prior work available at the moment it is useful without turning stale notes into
policy. A support engineer can start with a known pattern; they still reproduce the present
case before acting on it.

## Guardrails that work at the point of action

Several rules are enforced, or at least prompted, where mistakes otherwise happen:

| Guardrail | Behaviour it protects |
| --- | --- |
| Package-manager hook | Blocks `npm` and `npx` only when they are actually invoked in the pnpm monorepo. The rule was narrowed after it proved too broad. |
| Formatting hook | Runs the repository formatter after TypeScript and JavaScript edits, keeping routine format drift out of review and CI. |
| Comment reminder | Flags newly added source comments while leaving judgement with the engineer; the code should explain itself unless a non-obvious reason must be preserved. |
| PR-title hook | Requires a conventional, intent-led title and keeps Linear IDs out of that title. |
| Scoped repository instructions | Directs an agent to the correct package rules, checks, type boundaries, and project conventions before it edits. |

These are modest mechanisms. Their value is that they are precise, reversible, and based on
specific failure modes instead of broad restrictions that people work around.

## Quality standards made portable

Kelechi Mode includes two personal layers that can travel between repositories.

**Humaans Engineering Standard** raises the review bar without replacing the repository’s
rules: no new type debt, fix unsafe source boundaries rather than suppress errors, clean up
nearby legacy only when it affects the same invariant, and distinguish real blockers from
matters of taste. It adds focused checks for type safety, frontend work, names, and comments.

**Kelechi PR Writing** turns a pull request into a one-screen orientation document: an
intent-led conventional title; a brief context, solution, and test plan; a demo only when a
reader needs to see a visual change; and no implementation diary. The aim is a reviewer who
can explain the behavioural change after one pass.

Together with the plain-writing practice used for support and PRs, these standards make the
result legible to the person who has to make the next decision, not only to the person who
made the change.

## Why this is engineering work

The product timeline counts 475 authored pull requests, 633 reviews, and 80 support tickets.
Those numbers understate a second form of contribution: improving the system that makes each
future change safer and easier to reason about.

This work has product effects. It shortens the path from a support escalation to evidence;
it makes authorisation and tenant-isolation checks a standard part of risky reviews; it keeps
tests, traces, and production-shaped verification close to the task; and it leaves decisions
in a form another engineer can reuse.

The contribution is therefore not “using AI to write code.” It is designing an engineering
operating system that uses AI without giving up evidence, ownership, safety boundaries, or
clear communication.

## Portable form

This document is intentionally shaped as the front page of a private personal repository.
That repository should separate portable personal practices from Humaans-specific material:

```text
kelechi-engineering-system/
  README.md                    # this narrative and the operating principles
  plugin/                      # Kelechi Mode manifest, routes, and playbooks
  personal-standards/          # review and PR-writing layers
  templates/                   # support, investigation, hand-off, and PR outlines
  examples/                    # sanitised examples; no customer or production data
  humaans-adapter/             # private, company-specific skills and instructions
```

The portable core is the workflow: evidence before edits, diagnosis before fixing, small
coherent changes, real verification, and explicit authority. The Humaans adapter holds
commands, customer systems, production access patterns, repository paths, and institutional
memory that should remain private to Humaans.

## Evidence for this record

This record is grounded in the current local artifacts rather than a retrospective claim:

- `AGENTS.md`, scoped package instructions, `.claude/settings.json`, and `.claude/hooks/`
- `.claude/commands/code-review.md` and the targeted reviewers in `.claude/agents/`
- `.agents/skills/` and the personal `support`, `humaans-context`, and `plain-writing` skills
- the Kelechi Mode plugin, its routes, playbooks, custom-agent mapping, and two personal
  engineering standards
- the repository history that records the system’s incremental changes

The product work, customer outcomes, PR and ticket totals remain in
`timeline-narrative.md`, `timeline-full.md`, and `timeline-daily.csv`. This document records
the system that helped make that body of work repeatable.
