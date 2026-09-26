# Companion skills

Kelechi Mode is the operating model. Companion skills provide a capability or a narrowly useful
review lens. Keep them separate so a third-party workflow does not silently become the default.

## Incorporated as original portable practices

| Practice | Where it lives here | Why it belongs in the core |
| --- | --- | --- |
| Domain-driven design | `skills/domain-modeling/` | Complex work needs shared language, ownership boundaries, state transitions, and enforceable invariants. |
| Frontend quality | `skills/frontend-quality/` | UI work needs state ownership, accessibility, performance discipline, and real-browser proof. |
| Frontend design direction | `skills/frontend-design-direction/` | A new visual surface needs an intentional hierarchy and character before implementation. |
| Component API design | `skills/component-api-design/` | Shared components need explicit contracts when structural variants outgrow simple props. |
| Backend service design | `skills/backend-service-design/` | Service work needs explicit authority, validated input, invariant-safe writes, idempotency, and observability. |
| Evidence-first support and validation | `skills/support-investigation/` and `skills/work-validation/` | The workflow needs production-shaped evidence and real proof before hand-off. |

These are original, compact implementations. They take the useful principles of the source
material without copying another project's instructions or binding the workflow to one framework.

## Good optional companions

| Skill or capability | Use it when | Keep it out of the core because |
| --- | --- | --- |
| Handoff | A session, worktree, or engineer needs a durable context transfer. | It is a focused artifact generator, not a default part of every task. |
| Grill Me | A meaningful design has unresolved assumptions or irreversible choices. | An interrogation loop adds friction to straightforward implementation. |
| Web design guidelines | A UI needs a dedicated accessibility and usability audit. | A changing external standard should remain an optional audit source. |
| Real-browser testing | A user flow depends on JavaScript, authentication, timing, or interaction. | It needs a running app and should follow the repository's test setup. |
| Security analysis | A change affects authentication, data access, untrusted input, or sensitive flows. | Static-analysis tools and threat models are repository-specific. |
| Developer-index research | Public repositories, issues, and documentation need primary-source research. | It brings external cost and access decisions that do not belong in a local workflow core. |

## Named companions

Kelechi Mode names these by skill name and uses them only when installed.

| Companion | Where it plugs in |
| --- | --- |
| Matt Pocock's `diagnosing-bugs`, `tdd` | Fix route, after the reproduction is red |
| Matt Pocock's `domain-modeling` (CONTEXT.md, ADRs) | Recording the decisions the local `domain-modeling` skill reaches |
| Matt Pocock's `codebase-design`, `prototype`, `grilling` | Refactor, prototype, and design routes (`grilling` only when asked) |
| The `better-*` interface skills | UI detail work under the frontend standard |

The local skill owns the process; the companion supplies a format or technique.

## Deliberately not default

- **A full multi-agent framework.** Kelechi Mode already specifies the important part: parallelise
  independent evidence, not shared writes; retain one owner for integration and authority. A second
  orchestrator would create competing rules.
- **Next.js-specific React guidance.** It is valuable in a Next.js application, but it should not
  steer React, ReScript, or another frontend stack incorrectly.
- **Composition patterns as a universal style.** The included component-API skill applies them only
  when a shared component has a growing incompatible-mode or boolean-prop problem.
- **Creative frontend-design direction as a default.** The included design-direction skill applies
  only to new or substantially redesigned surfaces; enterprise product work starts with its
  existing design system and user task.
- **Always-on output compression.** Clear support, incident, and design writing occasionally needs
  more than terse fragments. Use concise writing as a judgement, not a permanent loss of detail.

## Review before installing

Read every third-party `SKILL.md` and bundled script. Check its trigger, tools, network access,
write behaviour, and compatibility with the repository adapter. A skill should either add a real
capability or encode a preference you actively want; a popular checklist alone is not enough.

Sources: [Wondel.ai skills](https://github.com/wondelai/skills) and [Firecrawl's skill survey](https://www.firecrawl.dev/blog/best-claude-code-skills).
