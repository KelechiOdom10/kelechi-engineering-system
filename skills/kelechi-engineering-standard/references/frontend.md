# Frontend

## State

Each value has one owner:

| State | Owner |
| --- | --- |
| Server data | TanStack Query |
| Navigation, filters, selection worth sharing | Router search params |
| Form input and validation | TanStack Form with a zod schema |
| Ephemeral UI (open, hover, step) | `useState` / `useReducer` in the component |
| Genuinely global client state | A store, only after prop-drilling measurably hurts |

- Derive values during render. An effect synchronises with an external system; it never computes a value, handles a click, or mirrors props into state.
- Keep component APIs small. Structurally different modes become explicit variants or composition, not boolean flags consumers must combine.

## States and accessibility

- Every data view has intentional loading (skeleton), empty, error, disabled, and permission-denied states. Never fail open while required data is missing.
- Native semantic elements before ARIA. Every pointer action has a keyboard path, visible focus, and an accessible name. Dialogs and menus place and restore focus.
- Meaning never relies on colour alone. Respect reduced motion. Animate `transform` and `opacity`.

## Visual defaults

For greenfield work, when no design system decides otherwise:

- Tailwind v4 with semantic tokens; shadcn / Base UI primitives; one accent colour on neutral bases.
- No emojis in UI, copy, or alt text; use an icon set.
- No pure black. `min-h-[100dvh]` instead of `h-screen`. Mobile-first; every route works on a phone.
- Apply the `better-*` domain skills while building; `frontend-quality` owns the `better-interface` screenshot review before handoff.

## Proof

A UI change is not done until it has been driven in a real browser: the changed flow, its loading, empty, and error states, keyboard use, and a narrow mobile width. Screenshots or a short recording go in the PR demo.
