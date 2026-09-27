# Verify skill template

## `.claude/skills/verify/SKILL.md`

```md
---
name: verify
description: Prove <app> works end to end - start it in isolation, sign in, drive its flows, and capture evidence. Use before calling a change done, or to run, reproduce, or demo <app>.
---

# Verify <app>

## Launch

<Exact commands in order, each with the directory it runs from: throwaway database, migrations, seed, servers. The ready signal for each: a log line or a URL that answers.>

## Doctor

<One read-only check that answers "is this instance worth driving": servers answering, the right database, a seeded user. Run it first, and again whenever anything looks wrong.>

## Isolation

<The ports and database this uses, and why they cannot collide with the main checkout's dev instance or other projects' containers.>

## Sign in

<How to become the local test user and where the magic link, code, or token appears locally. Never real email, accounts, or credentials.>

## Drive

<The tool for each surface and the stable handles to use: routes, labels, test ids, endpoints.>

## Evidence

Drive the real user path, not internal helpers. Capture the action and the resulting state, and check side effects (rows written, requests sent) as well as the screen. Before each screenshot, wait for finite animations to finish, or an entrance fade reads as a faded render. Evidence goes to <path> and survives cleanup.

## Cleanup

<Stop exactly what this run started, by process id or container name; drop the throwaway database; leave the evidence.>

## Gotchas

<Repository rules that trip agents: toolchain wrappers, required env, busy ports.>

## Features

`features/README.md` lists every mapped flow.
```

## `features/README.md`

```md
# Feature map

verified-at: <commit sha> (<YYYY-MM-DD>)

| Feature | File | Owning code |
| --- | --- | --- |
| <name> | `<feature>.md` | `<paths>` |
```

## `features/<feature>.md`

```md
# <Feature>

**What it is.** <One sentence from the user's point of view.>

## How to reach it
<The route, command, or menu, starting from a signed-in session.>

## How to drive it
<Numbered steps with real handles.>

## What proves it works
<The observable end state, plus the side effect to check. Include the loading, empty, and error states for UI.>

## Owning code
<The files maintain mode diffs against.>

## Gotchas
```
