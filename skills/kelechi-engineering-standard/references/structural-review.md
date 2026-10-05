# Structural review

The thermo-nuclear lens: a strict maintainability review of a diff's shape, not its bugs. Working code that leaves the codebase messier does not pass.

## Look for the code-judo move first

- Ask whether a reframing of the change, keeping its behaviour, would make whole branches, helpers, modes, or layers disappear. Push for deleting complexity over rearranging it.
- A refactor that moves code around without reducing the concepts a reader must hold is not a simplification.
- Prefer the version that feels inevitable in hindsight: direct, boring, and using the existing architecture instead of working around it.

## Presumptive blockers

Each holds unless the author gives a clear structural reason.

- **A file crosses 1,000 lines because of this diff.** Ask for decomposition first: helpers, subcomponents, or a focused module.
- **Spaghetti growth.** Ad-hoc conditionals, one-off booleans, nullable modes, or special cases bolted onto an unrelated or already busy flow. Move the logic behind its own abstraction, a typed model, or an explicit dispatcher.
- **Feature logic in a shared path.** A feature check scattered through shared code, or an implementation detail leaking through an API. Move it to the layer that owns the concept.
- **Indirection that buys nothing.** Thin wrappers, identity abstractions, pass-through helpers, or generic "magic" that hides a simple data shape. Keep the direct flow.
- **A muddied contract.** Casts, `any`, `unknown`, needless optionality, or loosely shaped objects where an explicit type or shared contract would simplify the control flow. A silent fallback papering over an unclear invariant means the boundary should be made explicit.
- **Duplication.** Copy-pasted logic, or a bespoke helper where the codebase already has a canonical one.
- **A preserved mess.** The diff keeps a lot of incidental complexity when a visible restructuring would delete it.

## Also flag

- Independent work serialised for no reason, when parallel execution is also simpler.
- Related updates that can leave state half-applied, when an atomic structure is obvious.
- "Temporary" branching likely to become permanent.
- Narrow edge-case handling added in the middle of an already busy function.

## Questions for every meaningful change

- Can fewer concepts, branches, or layers carry this behaviour?
- Did a cohesive module become more coupled, stateful, or harder to scan?
- Do repeated conditionals signal a missing model or helper?
- Is each new abstraction earning its keep?
- Does the logic live in the canonical layer?

## Reporting

- Order: structural regressions, missed simplifications, branching growth, boundary and type contracts, file size and decomposition, then legibility.
- Few high-conviction findings over many cosmetic ones. No rename nits while a structural issue stands.
- Each finding names the concrete restructuring, not just the smell. Be direct about a missed simplification: "this moves complexity around but doesn't delete it" is a finding, not a nit.
- Approval needs no structural regression, no visible missed simplification, no unjustified file-size growth, and no unjustified presumptive blocker.
