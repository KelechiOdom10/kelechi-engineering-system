# Naming and comments

## Names

- Name a thing by its role in the domain: a service handle, client, repository, adapter, or factory each gets the word for what it is.
- One term per concept across code, docs, and UI. When the product has agreed language, the code uses it.
- Block a name only when it hides a role well enough to invite misuse, or makes two concepts indistinguishable. Abbreviation alone is not a blocker.

## Comments

Code explains itself through names, types, and structure. A comment earns its place only when it preserves a *why* the code cannot express:

- a non-obvious invariant or ordering requirement;
- a `SAFETY:` justification for a type assertion;
- a security or authorisation constraint;
- a vendor, platform, or protocol quirk;
- a compatibility or migration boundary;
- a trade-off whose obvious alternative is unsafe.

Delete comments that restate the next line, narrate steps, record the author's thought process, or compensate for a poor name. Rename or restructure instead. A comment is blocking only when it is misleading, contradicts behaviour, leaks sensitive information, or encourages an unsafe invariant.
