# Git: Branch Review

How to review a branch before pushing by stepping through every changed file.

---

## Completeness check

If a shared interface changed (function signature, callable contract, template parameter), grep for all callers before starting the file-by-file review. Confirm every caller was updated.

```bash
grep -r "<changed symbol>" <src-dir>
```

A file-by-file diff review only covers files you already know about. Missing a caller shows up as a failure after the PR is open.

---

## Workflow

1. Get the full list of changed files vs the base branch.

```bash
git_helpers show-commits-on-branch --show-files-changed
```

2. Get a flat list of changed files.

```bash
git_helpers show-diff-committed --name-only
```

3. Review each file in turn.

```bash
git_helpers show-diff-committed --path <file>
```

For each file, make sure you understand what changed and why, that no unintended changes are present, and that all callers or dependents of changed code were updated. Move to the next file only once this is clear.
