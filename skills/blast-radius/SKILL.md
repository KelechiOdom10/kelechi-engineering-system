---
name: blast-radius
description: Blast radius - what a change breaks outside its diff, with its safety fact proven by running code. Use for "what could this break" or a small diff you don't trust.
---

# Blast radius

A diff shows what changed. The damage lives where the changed thing is consumed: callers, stored data, wire formats, config, generated files, other processes. Listing callers is the easy part and not the job. The job is the breakage grep and the type checker do not show, and a proof, not a persuasive write-up.

Read-only toward the product. The only files you write are proof scripts under `.kelechi/blast-radius/`.

## Evidence ladder

Rate every safety claim by how far down this ladder you got it, and say where it stopped:

1. **Asserted.** You said so. Worth nothing alone.
2. **Located.** A real `file:line`, or the library's own source at the installed version.
3. **Traced.** You walked the failure path step by step and it does not reach.
4. **Executed.** A script or test calls the real code and fails loudly if you are wrong.
5. **Reproduced.** Seen in the running app.

## Steps

1. **Read the change.** The diff, every symbol it adds, changes, or removes, and what now behaves differently, including what the diff does not spell out: defaults, ordering, formats, timing, error types.
2. **Map the consumers.** Spawn the explorer agent (`kelechi:explorer` / `kelechi_explorer`) to list every consumer of each changed symbol and value while you continue. Then go where it cannot: string and format consumers (paths, keys, column values, URLs, cache keys, queue payloads, env names), stored data written in the old shape, fixtures and generated files, feature flags, other languages or services reading the same bytes, and the installed source of any library whose behaviour you rely on.
3. **Find the load-bearing fact.** Most risky-looking changes are safe because of one fact ("only this module reads the value", "no stored row has the old shape"). Name it. If it holds, most risks clear at once.
4. **Prove it.** Write the smallest script under `.kelechi/blast-radius/` that calls the real code or queries the real data and fails loudly if the fact is false. Run it and keep its output. Aim for rung 4; say plainly when you only reached 2 or 3.
5. **Rate the rest.** Each remaining risk gets how it breaks, `file:line`, likelihood and cost, and the cheapest check. A search that found nothing is a result: record it under Cleared with the search you ran. Never invent a caller.
6. **Escalate a wide change.** When the change touches a shared contract or many consumers, recommend `interrogate` on it as well.

## Report

- **What changed**, including the non-obvious part.
- **Safe because of**: the load-bearing fact, its rung, and the proof output (or "unproven" and why).
- **Risks**: mechanism, `file:line`, likelihood and cost, check.
- **Cleared**: what you checked and why it is fine.
- **Before merge**: the cheapest test or command that catches the real risk. Suggest promoting the proof script to a permanent test only when it names a bug that could recur.

Delete `.kelechi/blast-radius/` afterwards unless Kelechi asks to keep the proof.
