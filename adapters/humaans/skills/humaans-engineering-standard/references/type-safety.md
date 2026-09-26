# Type-safety standard

The goal is not merely to make `tsc` pass. Preserve truthful types from the
boundary where data enters the system through to the behavior that consumes it.

## Blocking by default

- New `any`, `as any`, double assertions such as `as unknown as T`, or broad
  casts that silence a real mismatch without proving the value's shape.
- New `@ts-ignore` or `@ts-expect-error` used instead of correcting the source
  type, generated type, schema, adapter, or call site. A narrow
  `@ts-expect-error` is acceptable only for an intentional negative type test or
  a documented external limitation that cannot be fixed in this change.
- A suppression whose expected error is no longer specific or whose continued
  necessity is not verified.
- Unvalidated external, persisted, or message payloads being asserted into a
  trusted domain type.
- Types that permit invalid states the runtime cannot safely handle, especially
  optional fields, partial objects, or stringly typed discriminators added only
  to satisfy a caller.
- Server and client representations duplicated in a way that can silently
  drift when a shared contract or generated type is available.
- A type guard, parser, or schema that claims more than it checks.
- Loss of exhaustiveness for a union or state machine where a new case can fall
  through unnoticed.

## Review questions

1. Where did this value originate, and what proves its shape there?
2. Does the type describe reality, including absence, failure, and transitional
   states?
3. Is a cast bridging a genuinely safer abstraction, or hiding disagreement
   between two layers?
4. Could the invariant be encoded once in a schema, generated contract,
   discriminated union, or boundary adapter?
5. Do tests exercise runtime validation as well as compile-time expectations?

Do not demand elaborate type machinery when a small local type is truthful and
clear. Type sophistication is not the objective; removing unproved assumptions
is.
