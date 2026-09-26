# Routing

## Destinations

Choose the strongest form that fits; code beats prose.

| Lesson is about | Destination | Form, strongest first |
| --- | --- | --- |
| How Kelechi Mode works in any repo | this plugin (`kelechi-engineering-system`) | hook or script; test; a line in the owning skill, playbook, or reference; a tuned skill description |
| One repository's facts or gotchas | that repository | a check or test; a line in its `AGENTS.md` |
| Kelechi's preferences about how to work | memory | one memory entry, linked to related ones |
| Needs design, or is too big to apply now | backlog | a GitHub issue on `kelechi-engineering-system` |

A lesson goes into the owning file at the step where it would have changed the outcome, not into a new catch-all section. A new skill is rare: only when the lesson is a whole workflow with its own trigger.

## Reject when

- It happened once and would not recur.
- It is already encoded: name the file that covers it.
- The edit would not change behaviour: the model already does this by default.
- It restates a general virtue ("be careful", "test more") with no concrete trigger.

## Proposal format

```md
### Accepted
1. **<lesson>** (evidence #N, #M) → `<destination file or check>`
   <the exact edit: a diff, the new line, or the script change>

### Backlog
- **<lesson>** → issue: <title>. <why not now>

### Rejected
- <lesson>: <reason, naming the file if already encoded>
```

## Applying

- **Plugin.** In the `kelechi-engineering-system` checkout: a branch, one commit per lesson (`fix(<skill>): <lesson>`), the test suites (`python3 tests/hooks_test.py`, `node --test tests/check_boundaries_test.mjs`), `./scripts/reinstall.sh`, and a draft PR written with `kelechi-pr-writing`. A hook or script change carries a regression test.
- **Project.** A branch in that repository, one commit per lesson, its own checks green. Push and PR follow the authority table.
- **Memory.** Write or update the entry; never duplicate an existing one.
- **Backlog.** `gh issue create` on `kelechi-engineering-system`, only for items Kelechi approved.
