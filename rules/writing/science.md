# Scientific Writing

These rules apply when writing scientific prose: manuscripts, papers, theses, and technical reports intended for publication.

---

## Argument Structure

| Rule | |
|---|---|
| Begin from tension, not machinery | introduce what is unresolved before equations, methods, or numerics |
| Build arguments causally | each paragraph should explain why the next idea follows |
| Separate mechanism from implication | first explain what happens, then why it matters |
| Bound conclusions carefully | explicitly distinguish what is and is not explained |

---

## Physical Interpretation

| Rule | |
|---|---|
| Physical interpretation first | formalism supports the physics, not vice versa |
| Mechanisms over labels | explain what physically changes and why |
| Preserve scale awareness | distinguish local effects from system-scale implications |
| Explain why limitations matter | do not merely state caveats or assumptions |
| Distinguish evidence from interpretation | simulations, measurements, and physical claims should remain separable |

---

## Mathematical Writing

| Rule | |
|---|---|
| Inline math | use `$ ... $` |
| Display derivations | use `align` environments |
| Use mathematics to expose structure | equations should clarify competing processes, scales, or constraints; avoid disconnected formalism |
| Prefer decompositions that expose dynamics | separate competing terms, scales, or symmetries explicitly |
| Introduce variables completely | state symbol, physical meaning, and typical value or range in order |
| Annotate equation terms | label physical contributions in equations so structure is readable without parsing notation |

---

## Grammar

| Rule | |
|---|---|
| No contractions | write "do not", "it is", "we have" |
| No sentence-initial conjunctions | replace "And," "But," with "Moreover,", "However,", "In contrast," |
| Semicolons join coordinate clauses | colons introduce explanations, lists, and equations |
| Embed definitions in running text | use "where", "here", or "(i.e., ...)" rather than standalone definitional sentences |
| Passive only for definitions and constraints | "is defined as", "is given by", "are expected to"; active elsewhere |
| No em dashes | use commas, semicolons, or parentheses for secondary clauses |
| Numbers | spell out below ten; numerals above |

---

## Rhetorical Style

| Rule | |
|---|---|
| Match epistemic markers to confidence | use "consistent with", "suggest", "expect" for uncertain claims; use direct language for established results; avoid intensifiers like "very" and "really" |
| Specificity over vagueness | provide numbers, units, and scales rather than vague qualifications |
| Integrate citations syntactically | weave citations into prose structure; avoid parenthetical citation dumps |
| Signal surprise through structure | frame anomalies as clear problem statements, not through "surprisingly" or "remarkably" |
| Treat limitations analytically | reframe them immediately as motivation for the next move ("To overcome this..."), not as weaknesses to acknowledge and move past |
| Unexpected results are refinements | frame them as clarifying or extending existing understanding, not as contradictions |
| First person is strategic | use "I" for explicit intellectual ownership of key moves; "we" for methods and results |

---

## Preferred Patterns

Use contrastive structure to constrain conclusions:

```text
This can..., but does not by itself...
While X..., Y...
This suggests..., although...
```

Use consequence-driven transitions:

```text
This matters because...
An immediate consequence of this is...
To overcome this...
As a consequence, ...
In turn, ...
With this, we now have...
This motivates...
```

Use leading-order and contrast transitions:

```text
To leading order, ...
By contrast, ...
In contrast, ...
```

Place minor qualifications in parentheticals; move extended caveats to footnotes. Keep the main narrative unbroken.
