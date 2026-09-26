# Testing

**Test what can break that the compiler and linter cannot catch.**

## Rules

- **Every test names the bug it catches.** If you cannot say what realistic change would turn it red, do not write it.
- **Skip what is already guaranteed:** types, lint rules, schema shapes, "renders without crashing", "function exists", a mock returning what it was told to return.
- **Spend tests where risk lives:** invariants and state transitions, branching business rules, edge cases in pure logic, authorisation and tenant boundaries, and one regression test for every real bug fixed.
- **Call it the way users do and assert literal values.** If the test still passes when every import returns `undefined`, rewrite the assertion or delete the test.
- **Fewer, higher tests beat many shallow ones.** Deleting a redundant test is a valid change.

## Shape by layer

| Layer | Default proof |
| --- | --- |
| Pure core (compilers, reducers, rules) | Unit tests with inline literal fixtures |
| API route and database | Integration test through the real HTTP route against a real local database (`*.integration.test.ts`) |
| Critical user flows | Browser end-to-end tests (Playwright) for the few flows that must never break |
| Everything else | Real-boundary verification during the task, not a permanent test |

## Doubles

- Never mock your own modules. If a unit is hard to test without mocking a sibling, the seam is in the wrong place.
- Fake only at the network edge (vendor HTTP), using recorded fixtures. Recorded fixtures are canonical test data; they are regenerated, never hand-edited.

## In review

Test sprawl is a finding, not diligence. Flag tests that guard nothing, duplicate a type check, or assert on implementation details.
