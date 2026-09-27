---
name: architect
description: "Architect a change before writing it - callers, types, placement. Use for /kelechi:architect or before adding or changing a module, API, service method, or shared type."
---

# Architect

Settle the shape of a change before implementing it: the caller's code, the data shape, and the owning module. The design playbook decides what the system should do; architect decides what this change's code looks like from the outside. Stop before implementation.

Read `kelechi-engineering-standard` references `architecture` and `type-safety` first.

## Steps

1. **Frame.** One sentence: what the change lets a caller do. List the real callers, current and planned; a shape with no caller is speculation.
2. **Write the callers first.** Sketch two or three real call sites as they would read after the change, in `.kelechi/architect/<topic>.md`. The usage decides the interface: if a call site reads badly, the interface is wrong, not the caller.
3. **Name the data shape.** The types and schemas the change introduces or edits. Where external data is parsed, which states are impossible to represent, which union needs a registry, and which invariant is enforced where.
4. **Place it.** The feature module that owns it, the direction of every new dependency, and what `boundaries.json` says about it. List what this makes obsolete, to delete in the same change.
5. **Compare only real alternatives.** When two or three shapes are genuinely open, sketch each one's call sites and compare them on reader load, invalid states, migration, and test surface. When running code could settle it, use the prototype playbook instead of arguing.
6. **Draw it** when the change crosses a boundary or adds a feature, request, or data flow, and the `pr-lens` skill is installed: write the intended change as a PR Lens graph, validate it, render it locally, and keep `graph.json` in `.kelechi/architect/`. Never push it to a canvas unless Kelechi asks. At PR time, `kelechi-pr-writing` compares the built change against it.
7. **Decide.** Recommend one shape and name what would change your mind. Ask Kelechi only when the choice is a preference no experiment settles, as a decision with concrete consequences.

## Output

The sketch file holds the frame, the call sites, the data shape, the placement, the rejected options with one line each, and the diagram path. It is working state: implementation starts from it, and at the PR it is promoted to an ADR when the decision should outlive the change, or deleted.
