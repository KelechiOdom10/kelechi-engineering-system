---
name: support-investigation
description: Investigate a customer support issue from the reported symptom through evidence, a clear verdict, and a reader-ready update. Use for support tickets or customer escalations; do not use it to implement a fix.
---

# Support investigation

Treat a support request as an investigation, not an implementation task.

1. Restate the reporter, affected object, exact symptom, and expected behaviour before gathering
   evidence.
2. Confirm the authorised evidence sources are available. This can include a read-only production
   database, application logs, traces, analytics, or a reproducible local environment. Stop and
   report the missing prerequisite if the investigation depends on one that is unavailable.
3. Reproduce the exact reported symptom from the authorised source of truth. Trace the rows,
   events, request, or state transition that produce the observed result. A nearby anomaly is not
   proof of the reported problem.
4. Use the production database to establish facts that the application should show: the affected
   records, their relevant configuration, and the values that feed the symptom. Use read-only
   access. Minimise selected data and do not copy customer data into a ticket or chat unless the
   task requires it.
5. Use logs for errors, request failures, and background work. Use traces or measured timings for
   latency, repeated work, queue behaviour, and caller paths. Do not search telemetry by default
   when the symptom is a wrong value that the database can already explain.
6. Write several ranked, falsifiable hypotheses before testing one. Test one variable at a time.
   Read code and history only after the evidence narrows which contract or recent change matters.
7. When the evidence is sufficient, choose a verdict: configuration or education, a local bug,
   a broader product decision, or a request for more information. Measure the likely blast radius
   when it is a real bug.
8. Write a concise update for the support owner: what is happening, the evidence, a workaround if
   there is one, and the needed engineering follow-up. Draft only; do not post it without
   explicit authority.

Do not begin a fix in this skill. State the confirmed cause and the smallest next step so the
implementation task begins with evidence rather than a guess.
