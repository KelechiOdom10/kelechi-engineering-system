# AI features

For product features built on an LLM: chat, tools, agents, extraction, generation.

- **The model never produces a fact the code can own.** Numbers, scores, dates, and records come from typed queries and validated payloads. The model plans, routes, and phrases; it does not compute or remember data.
- **Typed plan in, validated payload out.** Model output that drives code is parsed against a schema before use, exactly like any other external input.
- **Freshness is data, not a prompt rule.** Compute recency, staleness, and availability in code and pass structured facts to the model.
- **A prompt rule is not a fix.** When a behaviour bug is "fixed" by adding a system-prompt line, a tool-description tweak, or an injected hint, and a second one follows on the same premise, stop and attack the premise: usually the tool boundary, the data shape, or who owns the decision is wrong.
- **Tools have one clear job each,** with descriptions that state when to use them and structured results, not prose for the model to parse.
- **Evaluate behaviour changes.** A prompt or model change is checked against a small fixed set of real questions with expected outcomes before it ships.
- **Fail visibly.** A missing tool result, quota, or vendor error returns a typed empty or error state the UI can render, not a confident guess.
