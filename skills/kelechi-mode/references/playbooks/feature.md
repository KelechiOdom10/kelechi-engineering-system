# Feature

1. Define the user outcome, constraints, non-goals, and acceptance evidence.
2. Map the current system and identify the owning data shape or domain boundary.
3. If the feature crosses boundaries or has unresolved semantics, use the design playbook as a checkpoint before implementation.
4. Before implementation, state the simplest viable shape using existing contracts, project helpers, and standard language features. Add a branch, helper, type, module, or export only when evidence shows that simpler shape is insufficient.
5. Implement the smallest end-to-end coherent slice. Keep one writer per working tree.
6. Use project-specific implementation and testing skills. Add unit or end-to-end coverage at the boundary that proves the behavior.
7. Exercise the real artifact or flow, not only isolated helpers.
8. Run a simplification pass before calling the change ready. Inspect every new condition and concept; replace manual control flow with an established idiom where behavior stays the same, and remove anything not justified by the verified contract. Then review authorization, stale paths, and documentation needs.
9. Use commit and PR workflows only when requested or otherwise authorized.
