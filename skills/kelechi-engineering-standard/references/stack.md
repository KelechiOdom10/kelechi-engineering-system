# Default stack

Defaults for new projects. An existing repository's choices win. Every deviation from a default in a new project gets a one-paragraph ADR.

| Concern | Default | Fork |
| --- | --- | --- |
| Toolchain | Vite+ (`vp`) with pnpm workspaces, TypeScript strict, oxlint, oxfmt | Leave experimental Vite flags off; Vite+ is alpha |
| App framework | TanStack Start | Astro for content sites with little interactivity |
| Rendering | Per route: prerender marketing and legal pages, SSR public dynamic pages, `ssr: false` on the authenticated app subtree | Decided per route, not per project |
| API | Elysia with Eden Treaty for end-to-end types | Hono if the Elysia Workers adapter blocks something (record an ADR) |
| Runtime | Cloudflare Workers via the Elysia Cloudflare adapter | A long-running Bun server for realtime connections, heavy background work, or native dependencies |
| Data | Postgres with Drizzle | Prisma only in existing Prisma projects |
| Auth | better-auth | Discussed per project |
| Validation | zod at every edge | none |
| Server state / forms / routing | TanStack Query, Form, Router | none |
| UI | Tailwind v4, shadcn / Base UI, an icon set | The project's own design system |

## Elysia on Workers guardrails

The Cloudflare adapter is experimental. Pin the Elysia version, and keep one integration test that runs through `wrangler dev`, not only `bun test`.

## Git

- Conventional Commits, scoped in a monorepo: `fix(api,db): ...`. Titles state intent, under 70 characters, no ticket numbers.
- Small commits, each leaving the build green, ordered so the history reads as a story.
- One PR per coherent slice, squash-merged. Stacked PRs only when the work has real phases.
- No AI attribution in commits or PRs.
