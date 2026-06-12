# Teaching Voice

Writing style for lesson content: READMEs and accompanying prose in teaching repositories.

Extends `markdown.md`: all formatting, structure, and prose mechanics from that file apply here. This file adds conventions specific to teaching material.

---

## Opening

Each lesson opens with a single sentence that captures the core idea or payoff. It should be self-contained and sharp enough to orient a reader who has not yet read anything else.

| Rule | |
|---|---|
| One sentence | the opening line is not a preamble; it earns the lesson |
| States the idea, not the plan | write what is true, not what you are about to cover |
| No filler | do not open with scope, context, or background |

Prefer:

```text
<Core idea or payoff in one sentence.>
```

Not:

```text
In this lesson we will cover <topic>.
```

---

## Problem before solution

Introduce the pain before the cure. The reader needs to feel the cost of the current approach before they can appreciate the alternative. The solution should never appear cold.

| Rule | |
|---|---|
| State the problem first | describe the situation that motivates the lesson before showing the fix |
| Make the cost concrete | name what breaks, what gets lost, or what becomes hard |
| Ground it in a recognisable scenario | use a situation the reader is likely to have encountered, not an abstract case |

---

## Consequence-forward justification

When recommending a practice, say what goes wrong if you do not follow it, not just what goes right if you do.

| Rule | |
|---|---|
| Name the failure mode | be specific: data corruption, silent wrong results, unreadable history |

Prefer:

```text
<Recommendation>. Without it, <concrete failure mode>.
```

Not:

```text
<Recommendation>. This is good practice.
```

---

## Payoff in the reader's terms

State benefits in terms of what changes in the reader's workflow, not in terms of abstract correctness or completeness.

| Rule | |
|---|---|
| Anchor to a concrete situation | name who can do what, and when |
| No abstract virtues | "reproducible", "correct", and "robust" are conclusions, not arguments; show what they mean in practice |

---

## Expectations over guarantees

Frame outcomes the reader will see as things to expect and verify, not facts being asserted.

| Rule | |
|---|---|
| Use "you should see" | not a bare statement of fact |
| Pair with the failure case | say what would appear if the expectation were not met |

Prefer:

```text
For <context>, you should see <outcome>. If <condition were not met>, <tool> would <response>.
```

Not:

```text
<Outcome>. <Tool> confirms every contract.
```

---

## Technical terms

Use exact technical terms. Define each one at first appearance, in the same sentence or the one immediately after. Do not avoid jargon; do not leave it unexplained.

| Rule | |
|---|---|
| Use the precise term | "immutable", "contracted", "first-order accurate" |
| Define at first use | "<term>, which means <definition>: <concrete consequence>" |
| Rely on it after | once defined, use the term without re-explaining it |

---

## Code Blocks

Code blocks contain only code. Distinguish between annotation comments and teaching comments.

| Rule | |
|---|---|
| Annotation comments | labelling what code computes or marking a section, as would appear in real code: `# d/dx`, `## div b = d(b_i)/d(x_i)` |
| Teaching comments | explaining why a line was chosen, what a tool reports, or restating what the surrounding prose says; these belong in prose, not in the block |
| Prose placement | put teaching-level explanation in the sentence immediately before or after the block |

---

## Register

Write as a more experienced colleague showing the reader something, not as an instructor delivering a lesson.

| Rule | |
|---|---|
| Second person | address the reader as "you" throughout |
| Collegial, not condescending | assume the reader is capable; explain why, not just what |
| Flowing sentences | prefer sentences that read as continuation; avoid short punchy standalone clauses |
| Topic sentence | open each paragraph with its conclusion; supporting sentences follow |

Occasional informality is acceptable when it acknowledges a shared experience ("you have probably been here before"); clumsy or sloppy phrasing is not.

---

## Interactive exercises

Where a concept can be demonstrated by deliberately breaking something, invite the reader to do it.

| Rule | |
|---|---|
| Single working script | start from a correct, working solution; do not provide separate before/after files |
| Reader owns the breaking | exercises guide the reader to deliberately break and restore specific behaviour |
| Name the file and the change | be specific enough that the reader can act without guessing |
| State the expected outcome | say which test fails or which error appears |
| Close the loop | tell the reader to undo the change and confirm it passes |

---

## Lesson Structure

Every lesson follows a three-phase arc, regardless of format:

1. **The problem**: motivate the lesson; show the cost of the status quo
2. **The solution or examples**: work through the tools, approach, or technique
3. **The outcome**: show what the reader now has; name the payoff

Lessons with a clear problem and distinct solution layers follow the four-part structure:

| Section | Purpose |
|---|---|
| The Problem | motivate the lesson; show the cost of the status quo |
| The Solutions | one subsection per tool or approach |
| The Lesson: Try Breaking Something | interactive exercises; see [[Interactive exercises]] |
| In Summary | table of what each layer catches, followed by a closing paragraph |

Other lessons adapt the arc to their flow. Section names may vary; the progression should be recognisable.
