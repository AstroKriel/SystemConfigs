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

Open with a paragraph describing the current state and why it is a problem. No heading for this opening; the problem statement should be immediately clear from the first sentence.

Then use the following sections as relevant:

**`## Proposed change`**: the concrete design. Include parameter names, defaults, and interface signatures where relevant. Use bullet lists for multi-part designs and tables for structured comparisons.

**`## CI impact`**: whether the change affects existing tests. If the default behaviour is preserved, say so explicitly.

**`## Motivation`**: why this is worth doing. Split into immediate and longer-term motivations when both apply.

**`## Relation to other proposals`**: dependencies and relationships to other open discussions or PRs.

**`## Deferred`**: items explicitly out of scope for this proposal, with a reason. This prevents scope creep and signals to reviewers what not to expect.

---

## After posting

Notify Ben Wibking, Mark Krumholz, and ChongChong He on Slack with a link to the discussion. Wait for feedback before starting implementation.
