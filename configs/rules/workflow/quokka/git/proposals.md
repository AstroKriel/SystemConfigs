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

The following sections are always expected:

**`## Proposed change`**: the concrete design. Include parameter names with defaults and interface signatures where relevant. Use bullet lists for multi-part designs and tables for structured comparisons.

**`## Test pipeline impact`**: whether the change affects existing tests. "None" is a complete answer; follow it with the reason, typically that the default behaviour is preserved and the new behaviour is opt-in.

**`## Motivation`**: why this is worth doing. When both immediate and longer-term motivations apply, split them with bold sub-labels.

Use the following sections where they apply:

**`## Relation to other proposals`**: dependencies and relationships to other open discussions or PRs. State the nature of the relationship in one phrase: "Dependency of", "Depends on", "Prerequisite for".

**`## Deferred`**: items explicitly out of scope for this proposal, with a reason and a cross-reference where one exists. This prevents scope creep and signals to reviewers what not to expect.

---

## Citing test results

Wherever a test result is quoted to motivate or support a design choice, include a figure and state the test name and any non-default parameters used.

---

## After posting

Notify on Slack with a link to the discussion. Wait for feedback before starting implementation.
