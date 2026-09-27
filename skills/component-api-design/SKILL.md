---
name: component-api-design
description: Simplify a shared component's API - boolean-prop sprawl, incompatible modes, unclear contracts. Use when a component has several consumers or structural variants.
---

# Component API design

1. List current consumers and the combinations of props they use. Separate cosmetic variation from
   a genuinely different structure, state model, or accessibility contract.
2. Keep a simple component simple. Add an explicit variant only when its supported states are finite
   and clear; use composition when consumers need to assemble different structures around shared
   state or behaviour.
3. Give each component one job. Keep internal state private unless a consumer must control it for a
   real composition need. Define the accessible contract for each interactive part.
4. Make invalid combinations impossible or rejected at the type boundary. Do not replace a handful
   of booleans with a compound API that has no second consumer or real extension point.
5. Update every consumer, document the resulting contract briefly where the project expects it, and
   test the distinct variants and keyboard paths.
6. Verify that the resulting API reduces the number of concepts a consumer must understand. If it
   does not, retain the simpler original shape.
