# Git: Before Pushing

Local checks to run before pushing any commit to the remote.

## Local build check

| Rule | |
|---|---|
| Build in scope | one target covering the changed code; confirms the feature compiles and runs |
| Build out of scope | one target outside the changed area; confirms no unintended breakage elsewhere |

The out-of-scope build is the more important of the two. CI is the systematic net; the local machine is the first line of defence.

---

## Project-specific notes

For Quokka, see `workflow/quokka/workflow.md` for which targets to use.
