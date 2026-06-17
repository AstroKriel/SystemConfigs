# Git: Sync Strategy

How to keep git repos in sync across devices, covering pull strategy, merge approach, and workflow discipline.

## Pull strategy

| Rule | |
|---|---|
| Pull strategy | always rebase, never merge; `pull.rebase = true` |
| Apply on new machines | run `git_helpers set-global-config` before starting work |

Rebasing replays local commits on top of the remote instead of creating a merge commit. This keeps history linear and is the right default when working across multiple devices.

---

## Merging branches

| Situation | Strategy |
|---|---|
| Feature branch into `main` | squash merge: collapse all commits into one clean entry |
| Long-running or integration branch | regular merge or rebase; do not squash |

Squash merging keeps `main`'s log readable: one entry per feature, with a clean commit message at merge time. Do not squash branches where the individual commit history carries meaning (e.g. long-lived collaboration branches, submodule pointer bumps).

---

## Multi-device discipline

| Rule | |
|---|---|
| End of session | push before switching to another machine, even for incomplete work |
| Start of session | pull before touching anything on a new machine |
| Source of truth | the remote; local is always a working copy |
| HPCs | pull only; never commit or push from an HPC |

---

## When branches diverge

If a pull fails because local and remote have diverged (e.g. a bot pushed to a shared branch), fetch first to see what changed, then pull with rebase:

```bash
git fetch
git log --oneline origin/<branch>
git pull --rebase
```

Resolve any conflicts at the rebase step, then push.
