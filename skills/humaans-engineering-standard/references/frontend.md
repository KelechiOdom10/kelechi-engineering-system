# Frontend standard

Apply this to changed UI behavior after reading the relevant project frontend
reviewer guidance. Use `frontend-developer` for project mechanics.

## Design system and reuse

- Search both Celeste primitives and application-level shared components before
  introducing a new primitive or duplicating an established interaction.
- Use semantic colour, spacing, typography, radius, shadow, duration, and
  z-index tokens. A raw value needs a concrete reason, such as brand artwork,
  data visualization, a third-party asset, or a missing token that should be
  addressed explicitly.
- Reuse shared pure logic when server and client behavior must agree. Do not
  create superficially similar implementations that can drift.

## Accessibility

- Prefer a native semantic element over recreating its behavior with ARIA.
- Every pointer interaction must have an equivalent keyboard path, visible
  focus, and an accessible name.
- Modals, menus, and popovers must place and restore focus predictably.
- Do not communicate meaning by colour alone. Check contrast and relevant
  reduced-motion behavior.
- Loading, errors, validation, and asynchronous completion must be exposed in a
  way assistive technology can understand when the interaction requires it.

Treat an unreachable primary action, missing accessible name, broken focus
flow, or meaning available only by colour as blocking. Minor semantic
improvements can be non-blocking when the interaction remains usable.

## Responsiveness and UI states

- Verify the changed flow at a narrow mobile viewport, an ordinary desktop
  viewport, and any wide or condensed layout it affects.
- Consider long names and translations, 200% zoom, overflow, scroll containers,
  sticky or fixed elements, and touch targets.
- Reuse existing breakpoint utilities rather than adding an arbitrary
  breakpoint for one screenshot.
- Keep loading, empty, error, disabled, and permission states coherent. Do not
  fail open while required data is unavailable.

## Motion and evidence

- Prefer `transform` and `opacity` for animation when changing layout
  properties would cause visible or measurable jank.
- For visible changes, expect proportionate evidence: screenshots or a short
  demo, keyboard verification, and relevant viewport checks. Do not require
  full end-to-end coverage when a smaller test proves the behavior.

Do not block on hypothetical reuse, arbitrary pixel differences, or a raw value
that is demonstrably part of an illustration or external asset.
