# Python: Docstrings and Comments

How to write Python docstrings and inline comments.

---

## Docstrings

Prose style follows `~/.rules/writing/docs.md`: short and direct, active voice, no filler words.

- Write docstrings for all public functions, methods, classes, and dataclasses.
- Docstrings are optional for private functions and methods.

- One-liners: opening and closing `"""` on the same line.
- Multi-line: `"""` opens with text immediately on the first line; closing `"""` on its own line.

```python
"""<One-sentence description ending with a period>."""

"""
<Opening sentence.>

<Optional second paragraph for non-obvious behaviour.>
"""
```

| Rule | |
|---|---|
| Opening sentence | imperative or declarative voice: "Compute X", "Return X"; sentence case; ends with a period |
| Compound behaviour | join related clauses with `;` rather than starting a new sentence or using "and" or "where"; prefer a semicolon-joined one-liner over a multi-line paragraph unless the second clause genuinely requires its own sentence |
| Second paragraph | add only when the opening sentence leaves something genuinely unclear: edge case behaviour, what triggers a raise, a non-obvious side effect; 2-4 sentences max; never restate what the type annotations already say |

- Add a `Parameters ---` section when there are four or more parameters and their constraints are not clear from the type hints alone.
- Only document what the annotation does not already say.

```python
"""
Short purpose sentence.

Parameters
---
- `param_name`:
    What it expects; constraints; what None means if applicable.
"""
```

Add a `Fields ---` section to a dataclass when field names alone do not convey their constraints or expected shape:

```python
"""
<One-sentence description of what the dataclass represents.>

Fields
---
- `<field>`:
    What it holds; valid ranges or invariants; what None means if applicable.

- `<other_field>`:
    Constraint relating it to another field, if any.
"""
```

| Rule | |
|---|---|
| Names and values | backticks: `` `param_name` ``, `` `True` ``, `` `None` `` |
| Inline math | code style: `` `y = a * x^b` `` |
| Boolean returns | `` `True` iff <condition>. `` |
| Types | never repeat in the docstring; the signature already has them |
| Format | never use numpy/sphinx-style `Parameters:\n-----------` blocks |

---

## Comments

| Rule | |
|---|---|
| Standalone marker | `##` (double hash); harder to accidentally uncomment than `#` |
| Inline marker | `#` (single hash) when the comment sits to the right of code on the same line |
| Spacing | two spaces between code and the `#` marker; do not align inline comments across lines; applies to `pyproject.toml` as well |
| Case | lowercase, unless referring to a named thing: a function, class, constant, or variable |
| Length | a few words to one sentence; never a paragraph |
| Purpose | only three reasons to comment: section structure, non-obvious constraints or invariants, and algorithmic decisions where the why is not derivable from the code |
| Formatting | use backticks for parameter names, flag names, config keys, filenames, and literal values: `` `param_name` ``, `` `--dry-run` ``, `` `this-system.toml` ``, `` `True` `` |
| Silence | leave obvious code uncommented: standard NumPy idioms, straightforward validation calls, and self-documenting function names need no explanation |

### Type-checker suppressions

| Rule | |
|---|---|
| Form | `# pyright: ignore[reportXxx]` |
| Never use | `# type: ignore[mypy-code]`; pyright silently ignores mypy error codes, so the suppression has no effect |
| Never use | bare `# type: ignore`; suppresses all errors on the line, not just the one intended |
| When | only genuine false positives that cannot be resolved at the type signature level |

---

Mathematical notation is preferred over English prose where appropriate:

```python
## <out> = <values>^2
numpy.multiply(
    <values>,
    <values>,
    out=<out>,
)
```
