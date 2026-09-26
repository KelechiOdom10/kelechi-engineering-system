# Step 6: first slice

The first slice is a **tracer bullet**: the thinnest user-visible flow that passes through every real boundary the product will have. UI to API to core to database and back, plus auth if the product needs it on day one.

## Choosing it

Propose two or three candidate slices and recommend one. A good slice:

- delivers the primary action from `docs/product.md`, even crudely;
- exercises at least one invariant from `docs/domain.md`;
- touches every package in the target layout;
- fits in one PR.

## Issues

Draft the issues in `.kelechi/issues.md` first. Each issue:

```md
## <intent-led title>

**Outcome.** What a user can do when this lands.
**Acceptance.** The observable evidence: the flow driven in a browser, the tests that must pass.
**Boundaries.** Which packages it touches.
**Out of scope.** What waits for a later issue.
```

One issue for the walking skeleton and slice, then at most a handful of follow-ups that widen the slice. Delivery order lives in GitHub milestones, never in a roadmap file. Creating the issues is an external action: show the drafts and ask once. Delete `.kelechi/issues.md` after they exist on GitHub.
