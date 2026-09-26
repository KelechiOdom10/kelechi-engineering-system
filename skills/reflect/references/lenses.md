# Lenses

Give each subagent this preamble, then its lens.

```text
You are reviewing a finished agent session to find durable lessons: things that would go wrong, or go better, on a different future task. You are read-only.

The session digest is at [digest path]. Items are numbered; cite them as #N. The raw transcript is at [transcript path] if you need more context around an item.
The skills and hooks that already govern this agent are under [plugin root]/skills and [plugin root]/hooks. Before proposing a lesson, search them: a lesson already encoded is not a finding.

For each lesson return:
1. The lesson, as one sentence stating the future behaviour.
2. Evidence: the #N items that show it, quoted briefly.
3. Why it recurs: the kind of future task it would affect.
4. Proposed destination (plugin skill or reference, hook or script, project AGENTS.md, memory, or backlog) and the edit, as concrete as you can make it.

Return at most six lessons, strongest first. If the session holds none, say "no durable lessons" and what you checked.
```

## Judgment

Where did the work change course? Hunt for: user corrections and repeated asks; wrong assumptions that cost time; a playbook step that was missing, mis-ordered, or skipped; a decision the user had to make that the agent could have settled by running something; places the agent stopped too early or went too far without authority.

## Tooling

What did the environment teach? Hunt for: commands that failed, hung, or needed retries; hook blocks and permission denials, and whether each was right; toolchain, platform, and CLI gotchas; manual steps done twice that a script, hook, or check would do. Prefer lessons that become code.

## Divergent

What would the other two lenses miss? Hunt for: what went well and should become the default; a skill that fired wrongly or should have fired and did not (its description needs tuning); friction in the reply style or the questions asked; a lesson that belongs to the project rather than the workflow.
