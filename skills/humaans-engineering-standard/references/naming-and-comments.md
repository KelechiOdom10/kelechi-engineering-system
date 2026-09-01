# Naming and comments

## Service names

Repository evidence shows both `<domain>Service` and the older `<domain>Svc`
for values returned by `app.service(...)`. The expanded form is the dominant
modern convention.

- Prefer `<domain>Service` for a direct Feathers service handle in new or
  renamed code.
- Do not require mechanical renames of established `Svc` variables in otherwise
  unrelated changes.
- Reserve `Service` or `Svc` for an actual service handle. Name a domain
  operation, client, repository, adapter, or factory by that role instead.
- Block a name only when it conceals the object's role enough to invite misuse
  or makes distinct concepts indistinguishable. Mere abbreviation is not a PR
  blocker.

## Source comments

Prefer clear names, types, and structure over comments that narrate the code. A
source comment earns its place when it preserves information the code cannot
express clearly, such as:

- a non-obvious invariant or ordering requirement;
- a security or authorization constraint;
- a vendor or protocol quirk;
- a compatibility or migration boundary;
- a surprising trade-off whose obvious alternative is unsafe.

Reject comments that restate the next line, record the author's thought
process, describe temporary implementation steps, or compensate for unclear
naming. Comments may use more than one line when the constraint genuinely needs
it; concision is a goal, not a line-count rule.

Comment findings are normally advisory. Treat one as blocking only when it is
misleading, contradicts behavior, exposes sensitive information, or encourages
an unsafe invariant.
