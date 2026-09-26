# Feature

1. Define the user outcome, constraints, non-goals, and the evidence that will prove it works.
2. Map the current system and name the data shape and the boundary that owns it.
3. If the feature crosses boundaries or its semantics are unsettled, run the design playbook as a checkpoint. Settle empirical forks with a prototype.
4. State the simplest viable shape using existing contracts, project helpers, and standard language features. Add a branch, helper, type, module, or export only when evidence shows the simpler shape falls short.
5. Build the thinnest end-to-end slice through the real boundaries first, then widen it. One writer per working tree.
6. Add tests where `kelechi-engineering-standard` testing says risk lives.
7. Exercise the real artifact. A UI change is driven in a real browser: the changed flow, its loading, empty, and error states, and a narrow mobile width.
8. Run a simplification pass: inspect every new condition and concept, swap manual control flow for an established idiom where behaviour holds, delete what the verified contract does not need. Then check authorisation, stale paths, and durable docs.
9. Run `work-validation`, then commit and open a PR within the authority table.
