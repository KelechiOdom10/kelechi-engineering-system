# Routing

Choose exactly one primary route. Each has a command, `/kelechi:<route>`. Add specialists only when their trigger applies; one marked *optional* is used when installed and skipped silently when not. A route that is a skill brings its own specialists.

| User intent | Route | Runs | Specialists |
| --- | --- | --- | --- |
| kickoff, new project or product surface | `kickoff` | `kickoff` skill | |
| investigate, diagnose, root cause, support ticket | `investigate` | `playbooks/investigation.md` | `support-investigation` for a customer report; adapter log, trace, and data skills |
| fix, bug, broken | `fix` | `playbooks/fix.md` | investigation first; *optional* `diagnosing-bugs`, `tdd` |
| feature, build, implement | `feature` | `playbooks/feature.md` | `domain-modeling` when semantics are unclear; `frontend-quality`, `frontend-design-direction`, `component-api-design`, or `backend-service-design` by surface; *optional* `better-*` UI skills |
| shape an API, module, or shared type before coding | `architect` | `architect` skill | |
| refactor, simplify, consolidate | `refactor` | `playbooks/refactor.md` | `domain-modeling` when a boundary drifted; *optional* `codebase-design` |
| slow, latency, memory | `perf` | `playbooks/performance.md` | adapter trace and profiler skills |
| review, audit, check this diff | `review` | `playbooks/review.md` | `kelechi-engineering-standard`; surface skills the diff touches |
| tear apart, stress test, adversarial review | `interrogate` | `interrogate` skill | |
| what could this break | `blast-radius` | `blast-radius` skill | |
| remove comments, before a PR | `no-comments` | `no-comments` skill | |
| design, plan, model | `design` | `playbooks/design.md` | `domain-modeling`; *optional* `grilling` only when asked |
| prototype, sketch, which approach | `prototype` | `playbooks/prototype.md` | *optional* `prototype` |
| explain, teach, how, why | `explain` | `playbooks/explain.md` | adapter history and context skills |
| babysit, drive a PR, fix CI | `babysit` | `playbooks/babysit.md` | `kelechi-pr-writing`, `work-validation` |
| how to run this app, prove it works | `verify-skill` | `verify-skill` skill | |
| reflect, what did we learn | `reflect` | `reflect` skill | |
| pause, handoff | `pause` | `playbooks/pause.md` | |
| resume, pick up | `resume` | `playbooks/resume.md` | |
| autonomous, keep going | `autonomous` | `playbooks/autonomous.md` | |
| software factory, recurring engineering automation | `software-factory` | `software-factory` skill | |

Every route that changes code ends with `work-validation`; every route that opens or updates a PR uses `kelechi-pr-writing`.

## Tie-breakers

- A support ticket starts as an investigation even when the goal is a fix; switch to fix explicitly after the checkpoint.
- `review` is one careful pass inside the diff; `interrogate` assumes the diff is broken and attacks it from several lenses and a second model; `blast-radius` looks outside the diff.
- `Review and fix` is the fix route with a review checkpoint. `Review` alone is read-only.
- `Explain how` needs current source; `explain why` may need history. Label which is which.
- A refactor whose target shape is unknown starts as design.
- A design question that running code could settle is a prototype.
- A new product, or a surface with unsettled language and domain, is a kickoff; a feature inside a settled domain is a feature.
