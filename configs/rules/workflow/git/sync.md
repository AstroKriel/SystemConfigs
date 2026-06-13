# Git: Sync Strategy

How to move code between branches and machines.

## Pull strategy

Always pull with rebase, never merge. `pull.rebase = true` is set as a global default by `git_helpers set-global-config`; run this on every new machine before starting work.

Rebasing replays local commits on top of the remote instead of creating a merge commit. This keeps history linear and handles the common case of resuming work on a different machine cleanly.

---

## Merging branches

| Situation | Strategy |
|---|---|
| Feature branch into `main` | squash merge: collapse all commits into one clean entry |
| Long-running or integration branch | regular merge or rebase; do not squash |

Squash merging keeps `main`'s log readable — one entry per feature — and forces a good summary commit message at merge time. Do not squash branches where the individual commit history carries meaning (e.g. long-lived collaboration branches, submodule pointer bumps).

---

## Multi-device discipline

Push at the end of every session, even for incomplete work. Pull before touching anything when resuming on a different machine. The remote is always the source of truth; local is always a working copy.

HPCs are consumers only: pull code from the remote, never commit or push from an HPC. All development happens on a local machine.

---

## When branches diverge

If a pull fails because local and remote have diverged (e.g. a bot pushed to a shared branch), fetch first to see what changed, then pull with rebase:

```bash
git fetch
git log --oneline origin/<branch>
git pull --rebase
```

Resolve any conflicts at the rebase step, then push.
