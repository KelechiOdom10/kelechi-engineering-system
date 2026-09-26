# Step 4: stack forks

Start from the defaults in `kelechi-engineering-standard` `references/stack.md`. Ask only the forks this product actually has; state the default as the recommendation.

## Forks

- **Rendering map.** Which routes are public (prerender for static pages, SSR for dynamic ones) and which subtree is the authenticated app (`ssr: false`)?
- **Runtime.** Workers by default. A long-running Bun server only for realtime connections, heavy background work, or native dependencies.
- **Auth.** better-auth by default; ask which sign-in methods, and whether organisations or teams are needed now.
- **Data.** Postgres host for production and how Workers reach it; local Postgres through Docker for development.
- **Vendors.** Each external API: batch ingest or live call, rate limits, and where fixtures are recorded.
- **Background work.** Cron, queues, or none.
- **AI.** Only if the product has an AI feature: which decisions the model owns, and the fixed evaluation set (see `ai-features`).
- **Deploy and domains.** Where it deploys, and preview environments.

Check any library or version fact against its current docs before recommending it.

## Artifacts

- **`AGENTS.md`**, from `../assets/AGENTS.template.md`: what the product is in one paragraph, commands, the dependency rule, boundary rules, and one-line links to `docs/`. It is the file both harnesses read.
- **`CLAUDE.md`** containing only `@AGENTS.md`, so Claude Code reads the same file.
- **`docs/adr/NNNN-<slug>.md`** from `../assets/adr.template.md`, one per non-default choice. A default needs no ADR.

In new-surface mode, write an ADR only for a new dependency or a new boundary, and extend the existing `AGENTS.md`.
