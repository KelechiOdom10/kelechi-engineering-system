# Steps 1-2: promise, principles, language

## Step 1 frontier

Ask what is still open from this set. Recommend an answer for each, grounded in what Kelechi has already said.

- **Audience.** Who is the first user, and who is the broader audience?
- **Core job.** One sentence: what does this help that person do that is painful today?
- **Primary action.** The one action a user takes most often.
- **Tenancy and ownership.** Who owns the data: a person, a team, an organisation? What is private by default?
- **Principles.** Propose 3-7, each a short imperative with a reason ("Remember first, polish later: capture must be fast"). Principles settle future trade-offs; a principle nobody would argue against is filler.
- **Must not become.** The products, patterns, or feelings this must not resemble.
- **Success signal.** What observable behaviour would show it works for the first user?
- **Depth check**, for a product that scores, ranks, explains, or recommends. Take each question it answers through: what a leading practitioner does (read their primary material when unsure), the rawest evidence it needs, the method, what the available data actually supports, and a check of correctness other than the model or Kelechi. Mark claims the data cannot support. A competitor's demo shows a workflow, not equal data access or accuracy.

## Step 2 frontier

Harvest every recurring noun from step 1 and from Kelechi's own words. For each noun with two plausible meanings, or two nouns for one thing, ask which term wins and what it means. Mark terms the UI must use verbatim.

## `docs/product.md`

```md
# <Product>

<The promise, two sentences.>

## Audience

## Principles

1. **<Imperative>.** <Why, one line.>

## Not this

## Agreed language

| Term | Meaning | Not to be confused with |
| --- | --- | --- |
```

In new-surface mode, add a `## <Surface>` section to the existing file instead.
