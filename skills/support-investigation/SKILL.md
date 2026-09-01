---
name: support-investigation
description: Investigate a customer support issue from the reported symptom through evidence, a clear verdict, and a reader-ready update. Use for support tickets or customer escalations; do not use it to implement a fix.
---

# Support investigation

Treat a support request as an investigation, not an implementation task.

1. Restate the reporter, affected object, exact symptom, and expected behaviour before gathering
   evidence.
2. Use only access the current task authorises. Confirm any production or customer-data boundary
   before relying on it.
3. Reproduce the exact reported symptom. A nearby anomaly is not proof of the reported problem.
4. Write several ranked, falsifiable hypotheses before testing one. Test one variable at a time.
5. When the evidence is sufficient, choose a verdict: configuration or education, a local bug,
   a broader product decision, or a request for more information. Measure the likely blast radius
   when it is a real bug.
6. Write a concise update for the support owner: what is happening, the evidence, a workaround if
   there is one, and the needed engineering follow-up. Draft only; do not post it without
   explicit authority.

Do not begin a fix in this skill. State the confirmed cause and the smallest next step so the
implementation task begins with evidence rather than a guess.
