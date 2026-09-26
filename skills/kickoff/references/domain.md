# Step 3: domain model

Load `domain-modeling` and follow it. Work from the agreed language in `docs/product.md`; a new term here goes back into the glossary.

## Frontier

- **Identities.** Which concepts have a lifecycle and need a stable id? Which are plain values?
- **Lifecycles.** The states each identity moves through, and what permits each transition.
- **Invariants.** Each rule that must always hold, and the transaction, constraint, or conditional write that enforces it.
- **Owners.** Which boundary owns each concept; which only consume it. Tenant scoping for every query.
- **External sources.** Vendors and integrations, whether their data arrives as a batch import or a live call, and where it is parsed.
- **Deferred.** Decisions deliberately left open, and what would force them.

Recommend a modular monolith and one owning module per concept unless a concrete constraint says otherwise.

## `docs/domain.md`

Use the shape of `../../../templates/domain-model.md`, compressed to one screen: one line per identity with its lifecycle, a list of invariants with their enforcement point, and a short external-sources list. The domain model is what the first slice's tests assert.
