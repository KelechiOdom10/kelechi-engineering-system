# Routing

Choose exactly one primary route. Add specialist skills only when their triggers apply.

| User intent | Primary playbook | Typical specialists |
| --- | --- | --- |
| investigate, diagnose, root cause, inspect, `SUP-` ticket | `playbooks/investigation.md` | `support`, `humaans-context`, then `gcloud-logs`, `honeycomb-traces`, or `authorization-review` only when evidence calls for them |
| fix, repair, bug | `playbooks/fix.md` | investigation specialists first, then `unit-test-developer`, `frontend-developer`, `rescript-developer`, `mcp-developer`, `authorization-review` |
| feature, build, implement | `playbooks/feature.md` | `domain-modeling` when the business model is unclear; `frontend-quality`, `frontend-design-direction`, or `component-api-design` for the relevant UI trigger; `backend-service-design` at a service boundary; relevant test skills |
| refactor, simplify, consolidate | `playbooks/refactor.md` | `domain-modeling` when a boundary has drifted; language and test skills |
| performance, slow, latency, memory | `playbooks/performance.md` | `honeycomb-traces`, `node-debugger`, `fullstack-debugger` |
| review, TNR, interrogate, audit | `playbooks/review.md` | repository review guidance, then `frontend-quality`, `component-api-design`, `backend-service-design`, or `domain-modeling` when the changed surface requires it |
| design, architect, model, plan | `playbooks/design.md` | `domain-modeling`; `grill-me` or `grill-with-docs` only when explicitly requested |
| explain, teach, how, why | `playbooks/explain.md` | `humaans-context` for historical context; relevant domain skills |
| babysit, monitor PR, drive PR, fix CI | `playbooks/babysit.md` | `gh-fix-ci`, `create-pr`, `kelechi-pr-writing`, `validate-branch`, `rebase-conflicts` |
| pause, handoff, park | `playbooks/pause.md` | `handoff` when a durable handoff is requested |
| resume, continue, pick up | `playbooks/resume.md` | `humaans-context`, then task-specific specialists |
| autonomous, keep going, run until | `playbooks/autonomous.md` | route-specific specialists; authorization remains unchanged |

## Tie-breakers

- A support ticket always begins with the investigation route, even when the eventual goal is a fix. Complete or summarize the investigation checkpoint before switching to the fix playbook.
- The `support` skill owns production-replica procedure. `psql-dev` is only for local dev/test databases and must not be substituted for production investigation.
- `Review and fix` is a fix route with an explicit review checkpoint. `Review` alone is read-only.
- `Explain why` may require history; `explain how` requires current source and runtime behavior. When both matter, clearly separate them.
- A broad refactor whose target shape is unknown begins as design. A known behavior-preserving transformation uses refactor.
- `Babysit` must declare whether it is read-only checking or authorized driving before taking actions.
