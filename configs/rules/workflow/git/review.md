# Git: Pre-Push Review

Before pushing, step through every changed file on the branch and confirm the diff is correct.

## Workflow

```bash
# 1. See which commits are on the branch
git_helpers show-commits-on-branch --show-files-changed

# 2. Get the full list of changed files vs the base branch
git_helpers show-diff-committed --name-only

# 3. Review each file in turn
git_helpers show-diff-committed --path <file>
```

Go through files one at a time. For each: explain what changed and why, and confirm before moving to the next.
