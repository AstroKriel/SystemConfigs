# Quokka: Fork Workflow

How branch and remote setup splits between the Quokka upstream and a personal fork.

---

## Remote naming

- `upstream` = `quokka-astro/quokka` (the org repo). Fetched from, never pushed to directly for personal-only work.
- `origin` = `<username>/quokka` (the personal fork). Everything gets pushed here first.

This matches the naming quokka's own `CONTRIBUTING.md` uses (`git fetch upstream`, `git push origin <branch>`), so its instructions apply as written.

---

## `main`

The only persistent local branch. Tracks `origin/main`, the fork's default branch (renamed from `development` at fork time to avoid two same-named branches with different histories). Holds every established sim, merged in once each is no longer a work-in-progress. Never opened as a PR.

There is no persistent local `development` branch: `upstream/development` (the remote-tracking ref, refreshed by `git fetch upstream`) already is the up-to-date base for upstream-bound work, with no separate branch to keep in sync. See "Choosing a base branch" below.

---

## Choosing a base branch

| Destined for | Branch off | Push to | End state |
|---|---|---|---|
| Upstream PR | `upstream/development` | `origin` | Opened as a PR against `quokka-astro/development`; branch deleted after merge. |
| Personal sim | `main` | `origin` | Merged into `main` once the sim is established; topic branch deleted. Never a PR. |

Starting new upstream-bound work:

```
git fetch upstream --no-recurse-submodules
git worktree add ../quokka-worktrees/<verb>-<name> -b <verb>/<name> upstream/development
```

The `git fetch` immediately beforehand is the whole "keep it current" step; there's no separate branch to pull first.

---

## Syncing `main`

```
git checkout main
git fetch upstream --no-recurse-submodules
git merge upstream/development
git submodule update --init --recursive
git push origin main
```

`main` is a long-running integration branch per [`workflow/git/sync.md`](../../git/sync.md): merge, not rebase or squash, so the sims already merged in don't get replayed on every sync.

Conflicts should be rare: sims live in their own `src/problems/<sim>` directories, so the only real collisions are between `main` and upstream when a core file both touch changes on the upstream side. Worth resolving carefully when it happens, not routine noise.

---

## Sync cadence

- **Weekly**, as a baseline, so `main` doesn't drift far behind.
- **On demand**, immediately before branching a new sim off `main` and immediately before merging a finished sim into `main`, so conflicts surface while they're still small. This is the "pull before forking" rule in [`workflow/git/worktrees.md`](../../git/worktrees.md), applied to `main`.

---

## Cold start: wiring a new clone

```
git clone --recursive git@github.com:<username>/quokka.git
cd quokka
git remote add upstream git@github.com:quokka-astro/quokka.git
```

The clone already lands on `main` (tracking `origin/main`) since that's the fork's default branch; nothing else needs setting up. The base clone stays on `main` and is never switched away from, per [`workflow/git/worktrees.md`](../../git/worktrees.md).

Clones used only to build and run sims (e.g. an HPC clone) don't need `upstream` configured at all. `git pull origin main` is enough to pick up the latest merged state.

---

## Worktrees

Every subsequent branch, whether a PR-bound topic branch off `upstream/development` or a personal sim off `main`, gets its own worktree per [`workflow/git/worktrees.md`](../../git/worktrees.md). New worktrees start with empty submodule directories; run `git submodule update --init --recursive` inside before building.
