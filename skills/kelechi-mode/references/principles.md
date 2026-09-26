# Principles

Name the principle that shaped a decision when you report the decision.

## Evidence

1. **Evidence before edits.** Read the current system, reproduce the symptom, or measure the baseline before changing anything.
2. **Diagnose before fixing.** Keep facts, hypotheses, and conclusions distinct. Reproduce, then ask why until you reach the cause; fix it there, not where the symptom surfaced.
3. **Attack the premise.** When two fixes that share one premise fail the same check, stop patching and question the premise. Adding another prompt rule, flag, or special case on top of a failing design is the signal.
4. **Current source beats memory.** History, handoffs, and docs explain intent; they do not prove present behaviour.

## Shape

5. **Subtract before you add.** Prefer deletion and the smallest coherent change. Add a branch, helper, type, or layer only when the verified contract needs it.
6. **Name the data shape first.** Choose the types and structures before the logic; put each concept at the boundary that owns it and make invalid states unrepresentable.
7. **Minimise reader load.** Count the layers between a question and its answer. Collapse one-caller wrappers and shrink mutable scope.
8. **Migrate callers, then delete.** A new internal API replaces the old one in the same wave; no compatibility shims without an external consumer.
9. **Build the lever.** For repetitive or sweeping work, write the script, codemod, or check that does it or proves it. The tool is what a reviewer reruns.

## Proof

10. **Prove it works on the real boundary.** A passing mock is weaker than the request, UI flow, job, or artifact that matters. "It compiles" is not proof.
11. **Work in verifiable units.** Each step ends in an observable check; sequence commits so the history proves itself.
12. **Test what the compiler cannot catch.** See `kelechi-engineering-standard` testing reference.

## Operating

13. **Parallelise independent evidence, never shared writes.**
14. **The primary agent owns delegated work** and inspects it before accepting it.
15. **Encode lessons in structure.** A rule repeated twice becomes a lint rule, type, test, script, or hook rather than more prose.
16. **Persistence never expands authority.**
