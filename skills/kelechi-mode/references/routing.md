# Routing

Choose exactly one primary route. Add specialists only when their trigger applies. A specialist marked *optional* is used when installed and skipped silently when not.

| User intent | Command | Playbook | Specialists |
| --- | --- | --- | --- |
| kickoff, new project, new product surface | `/kelechi:kickoff` | `kickoff` skill | `domain-modeling`, `frontend-design-direction`, `kelechi-engineering-standard` stack reference |
| investigate, diagnose, root cause, support ticket | `/kelechi:investigate` | `playbooks/investigation.md` | `support-investigation` for a customer report; adapter log, trace, and data skills |
| fix, bug, broken | `/kelechi:fix` | `playbooks/fix.md` | investigation first; *optional* `diagnosing-bugs`, `tdd` |
| feature, build, implement | `/kelechi:feature` | `playbooks/feature.md` | `domain-modeling` when semantics are unclear; `frontend-quality`, `frontend-design-direction`, `component-api-design`, or `backend-service-design` by surface; *optional* `better-*` UI skills |
| architect, shape this API or module, before coding a new boundary | `/kelechi:architect` | `architect` skill | *optional* `pr-lens` for the intended-change diagram |
| refactor, simplify, consolidate | `/kelechi:refactor` | `playbooks/refactor.md` | `domain-modeling` when a boundary has drifted; *optional* `codebase-design` |
| interrogate, tear apart, stress test, adversarial review | `/kelechi:interrogate` | `interrogate` skill | `kelechi-engineering-standard`; the other harness's CLI for the cross-model reviewer |
| blast radius, what could this break, small diff I don't trust | `/kelechi:blast-radius` | `blast-radius` skill | `kelechi:explorer` for consumer mapping; `interrogate` for a wide change |
| no comments, remove the comments, before opening a PR | `/kelechi:no-comments` | `no-comments` skill | `kelechi:comment-reviewer` |
| slow, latency, memory, performance | `/kelechi:perf` | `playbooks/performance.md` | adapter trace and profiler skills |
| review, audit, check this diff | `/kelechi:review` | `playbooks/review.md` | `kelechi-engineering-standard`; surface skills when the diff touches them |
| design, architect, plan, model | `/kelechi:design` | `playbooks/design.md` | `domain-modeling`; *optional* `grilling` only when asked to be grilled |
| prototype, sketch, "which approach" | `/kelechi:prototype` | `playbooks/prototype.md` | *optional* `prototype` |
| explain, teach, how, why | `/kelechi:explain` | `playbooks/explain.md` | adapter history and context skills |
| babysit, drive PR, fix CI | `/kelechi:babysit` | `playbooks/babysit.md` | `kelechi-pr-writing`, `work-validation` |
| reflect, what did we learn, capture lessons | `/kelechi:reflect` | `reflect` skill | the other routes' skills, as edit targets |
| verify skill, how do I run this app, prove it works | `/kelechi:verify-skill` | `verify-skill` skill | the browser tool or Playwright |
| pause, handoff, park | `/kelechi:pause` | `playbooks/pause.md` | none |
| resume, continue, pick up | `/kelechi:resume` | `playbooks/resume.md` | route-specific |
| autonomous, keep going, run until | `/kelechi:autonomous` | `playbooks/autonomous.md` | route-specific |

Every route that changes code ends with `work-validation`. Every route that opens or updates a PR uses `kelechi-pr-writing`.

## Tie-breakers

- A support ticket always starts as an investigation, even when the goal is a fix. Finish the investigation checkpoint, then switch to fix explicitly.
- `Blast radius` looks outside the diff for what the change breaks and proves the safety fact by running code; `review` and `interrogate` look inside the diff.
- `Review` gives one careful verified pass. `Interrogate` assumes the change is broken and attacks it from several lenses and a second model family; use it for risky or contested changes.
- `Review and fix` is the fix route with a review checkpoint. `Review` alone is read-only.
- `Explain how` needs current source and runtime behaviour. `Explain why` may need history. Label which is which when both matter.
- A refactor whose target shape is unknown starts as design. A known behaviour-preserving transformation is a refactor.
- A design question someone could settle by running code is a prototype.
- A new product or a new surface with unsettled language and domain starts as kickoff; a new feature inside a settled domain is a feature.
- `Babysit` declares `check` (read-only) or `drive` before acting.
