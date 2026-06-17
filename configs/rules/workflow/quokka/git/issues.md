# Quokka: Issues

How to file bug reports as GitHub Issues.

---

## When to file an issue

File an issue for:

- wrong answers, crashes, or silent failures in the code
- usability problems (e.g. misleading error messages, undocumented required parameters)
- regressions introduced by a recent change

Questions and feature proposals belong in GitHub Discussions, not issues.

---

## Title

Write the title as an observation, not a command. State what is wrong and under what condition.

```
<Component>: <observed behaviour> when <condition>
```

For example: "`Physics_Traits`: `numPassiveScalars` is silently wrong when `numMassScalars` is overridden without also overriding `numPassiveScalars`."

---

## Body

Cover the following:

- **What is wrong**: the observed behaviour, with enough detail to reproduce it.
- **What is expected**: what correct behaviour looks like.
- **Reproduction**: minimal input file, parameters, or code path that triggers the bug.
- **Context**: relevant configuration (build type, dimensionality, compiler, platform) if the bug may be environment-specific.

Include figures, log output, or error messages where they add information that prose alone cannot convey.
