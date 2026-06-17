# Quokka: Proposals

How to write and post feature proposals as GitHub Discussions before implementing.

> **Note:** post a proposal before starting implementation. The goal is to surface objections and design feedback early, not after the work is done.

---

## When to write a proposal

Write a proposal for any change that:

- adds a new parameter, struct field, or callable interface
- changes the behaviour of an existing test or harness in a non-trivial way
- consolidates, removes, or restructures existing code in a way that affects other contributors

Small bug fixes and self-contained additions that do not affect other contributors do not need a proposal.

---

## Structure

Open with a paragraph tracing the causal chain: what exists, what follows from it, and why that is a problem. No heading; the problem should be clear from the first sentence. Do not state that something is a problem without also stating the consequence.

Then use the following sections as relevant:

**`## Proposed change`**: the concrete design. State every new parameter with its name and default value inline: "`setup.<param>` (default: `<value>`)". Use bullet lists for multi-part designs and tables for structured comparisons (e.g. a Keep/Remove table when consolidating binaries).

**`## Test pipeline impact`**: whether the change affects existing tests. "None" is a complete answer; follow it with the reason, typically that the default behaviour is preserved and the new behaviour is opt-in.

**`## Motivation`**: why this is worth doing. When both timescales apply, use **Immediate:** and **Longer term:** bold sub-labels.

**`## Relation to other proposals`**: dependencies and relationships to other open discussions or PRs. State the nature of the relationship in one phrase: "Dependency of", "Depends on", "Prerequisite for".

**`## Deferred`**: items explicitly out of scope for this proposal, with a reason and a cross-reference where one exists. This prevents scope creep and signals to reviewers what not to expect.

---

## After posting

Notify Ben Wibking, Mark Krumholz, and ChongChong He on Slack with a link to the discussion. Wait for feedback before starting implementation.
