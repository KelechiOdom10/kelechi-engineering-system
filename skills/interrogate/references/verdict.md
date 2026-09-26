# Verdict

## Buckets

- **Act on.** A verified failure that affects correctness, security, or maintainability given the change's real goals. Would block a real PR.
- **Consider.** Legitimate, but the cost of addressing it now may outweigh the benefit. Name the trade-off.
- **Noted.** True but not actionable now: premature, context-dependent, or low impact.
- **Dismissed.** Wrong, taste-level, or missing context. One line on why.

## Format

```md
### Intent
> <the intent paragraph>

### Reviewers
- <lens>: <agent and model>, <N findings>
- Cross-model: <CLI and model>, <N findings> (or: skipped, <reason>)

### Act on
- **<title>** (<reviewers>). <failure scenario>. `file:line`. Fix: <smallest fix>.

### Consider
- **<title>** (<reviewers>). <trade-off>.

### Noted
- <title>: <why not now>.

### Dismissed
- <title> (<reviewer>): <why>.

### Agreement map
<Where reviewers agreed, where they diverged, and what the pattern says about the change's risk.>
```

Keep the reply to the verdict. If Act on is empty, say so first.
