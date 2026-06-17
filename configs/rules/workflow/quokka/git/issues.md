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

Write the title as an observation, and state what is wrong (and under what conditions).

```
<Component>: <observed behaviour> when <condition>
```

---

## Body

A good issue demonstrates that you have investigated the root cause, not just observed a symptom. The goal is to give maintainers enough to act confidently.

Cover the following:

- **Discovery**: how and when the bug was found. What you were running, and what made it visible.
- **What is wrong**: the observed behaviour, with enough detail to reproduce it.
- **What is expected**: what correct behaviour looks like.
- **Sims tested**: which configurations showed the bug and which did not. This constrains the failure mode.
- **Reproduction**: minimal input file, parameters, or code path that triggers the bug.
- **Diagnosis**: where in the code the failure appears to originate and what the root cause is. If the root cause is not yet known, say so explicitly.
- **Proposed fix**: what should change to resolve the issue, and why that approach is correct over alternatives. Omit only if genuinely unknown.
- **Context**: relevant configuration (build type, dimensionality, compiler, platform) if the bug may be environment-specific.

Include figures, log output, or error messages where they add information that prose alone cannot convey. Wherever a test result is cited, state the test name and any non-default parameters used.
