# Type safety

The goal is truthful types from where data enters the system to where it is used, not a quiet `tsc`.

## Rules

- **Parse at the edge, trust inside.** HTTP bodies, vendor JSON, env, storage, messages, and SQL rows pass through a schema (zod) at the boundary. Internal code accepts the parsed type and does not re-validate.
- **Type assertions carry a `SAFETY:` comment** stating the invariant that makes the cast sound, and only where the type system cannot relate two facts you have checked. Every other assertion is a defect.
- **Registries over switches for `kind` unions.** A mapped type keyed by the discriminant (`{ [K in Plan["kind"]]: Handler<K> }`) makes a new variant fail to compile until its handler exists.
- **Exhaust every union.** A new case must not fall through unnoticed.
- **Derive from the authoritative schema.** One source per contract; server and client share it instead of drifting copies.
- **Brand primitives that carry meaning** (ids, slugs, money) when mixing them up is a realistic bug.

## Blocking by default

- `any`, `as any`, `as unknown as T`, or a broad cast silencing a real mismatch.
- `@ts-ignore` / `@ts-expect-error` used in place of fixing the source type. A narrow `@ts-expect-error` survives only in a negative type test or for a documented external limitation.
- Unvalidated external or persisted data asserted into a trusted type.
- Optional fields, partial objects, or stringly-typed discriminators added only to satisfy a caller, admitting states the runtime cannot handle.
- A type guard or schema that claims more than it checks.

## Questions

1. Where did this value originate, and what proves its shape there?
2. Does the type describe reality, including absence, failure, and in-between states?
3. Is this cast bridging a checked fact, or hiding a disagreement between two layers?

Type sophistication is not the objective. A small truthful local type beats elaborate machinery.
