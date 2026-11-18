# Git: Commits

Conventions for git commit messages: format, actions, scopes, granularity, and presentation.

## Format

Commits are a single line only:

```
<action>-<scope>(<identifier>): <description>.
```

The left side of the colon is the summary. Reading only the left sides in `git log --oneline` should show what kind of change happened, at what level, and to which thing. The description adds detail: what changed and why.

Every commit combines one <action> with one <scope>, joined by a hyphen. The action says what kind of change it is. The scope says where it happened. Never put the kind or purpose of a change in the scope; that belongs in the action or the description.

The identifier in parentheses is the literal name the scope points to: a function/class name for `fn`, a filename for `file` or `content`, a folder name for `folder`, a dependency name for `dep`. Omit the parentheses for `repo` level changes, except for renames (see Arrows).

---

## Identifier

The identifier names the smallest single thing that contains the whole change.

- A change inside one function is `fn(<function>)`.
- A change across several functions in one file is `content(<file>)`.
- A change across several files in one folder is `folder(<folder>/)`.
- A change across several folders is `repo`.

| Rule | Detail |
|---|---|
| One name | never list several names; move up a level instead |
| Never empty | `folder()` is not allowed |
| Real names only | name something in the code, never an invented label |
| Methods | write as `<Class>.<method>`, since bare names like `run` repeat across classes |
| Matching kind | the identifier is the kind of thing its scope names; `fn(<file>.py)` is wrong |

Edits that only support the named unit do not move it up a level. For example, updating one caller after changing a function stays `fn`.

---

## Arrows

Use `old -> new` with a space on each side to show the direction of a change.

- Renames and moves put the arrow in the identifier: `rename-fn(<old_name> -> <new_name>)`.
- Value changes put the arrow in the description: `update-param(<param>): 20 -> 30 pt.`
- Renaming a concept across the repo is `rename-repo(<old_name> -> <new_name>)`. The parentheses tell it apart from renaming the repository itself.

---

## Actions

Use these actions as the default vocabulary. Other verbs are permitted when none of the standard ones fit precisely, as long as the verb is specific and imperative.

| Action | When |
|---|---|
| `del` | deleting something |
| `add` | creating something new |
| `fix` | bug fix |
| `revert` | undoing or rolling back a previous change on this branch; restoring prior behaviour that was intentionally changed away from |
| `update` | changes to existing functionality |
| `refactor` | restructuring without behaviour change |
| `rename` | renaming something |
| `move` | relocating something without renaming it |
| `bump` | changing a dependency pin, submodule pointer, or package version |

---

## Scopes

Scope answers where the change happened. Every action pairs with one of these:

| Scope | What it names |
|---|---|
| `param` | a single parameter, argument, or variable |
| `fn` | a function or class |
| `file` | a whole file, when it is created, deleted, renamed, moved, or restored |
| `content` | edits across several places inside one file that do not change its existence |
| `folder` | a whole folder/module |
| `repo` | the whole repository |
| `dep` | a dependency pin or submodule pointer |

A convention sweep is not its own scope. It takes the scope that contains it, usually `repo` or `folder`, and the description names the convention.

Bumps always state the change with an arrow:

```
bump-dep(<dependency>): <old_hash> -> <new_hash>; <what the new version provides>.
bump-repo: <old_version> -> <new_version>.
```

---

## Granularity

- One logical change per commit.
- Split when changes are independently revertable and target different scopes.
- Keep together when changes are interdependent or incomplete in isolation.
- A fix never rides along with another change; commit it on its own as `fix-`.
- A rename includes every call site. If one is missed, the follow-up `fix` says it was missed by the rename.
- Several `;` parts pointing in different directions are a signal to split.
- Batch iterative tuning of one value into a single commit once it settles.

---

## Details

| Rule | Detail |
|---|---|
| Specificity | name what specifically changed, never vague summaries like `update text`, `fix things`, `mend` |
| Case | lowercase throughout |
| Separator | use `;` to separate multiple related changes within one commit |
| Ending | end with a period |
| Length | total length under 120 characters |
| Characters | ASCII only; no special characters except the `->` arrow |

---

## Commit Message Examples

These illustrate the message format and wording style only, not the full shell workflow:

```
del-param(<param>): drop the unused override in <file>.py.
add-repo: <description of initial repo structure>.
fix-fn(<function>): accept <type> for <param>; accept None for <param>.
fix-content(<file>.py): <old_call> -> <new_call>; missed by the rename.
revert-fn(<function>): drop <feature> that shipped only as a diagnostic.
update-content(<file>.py): <description of a broad change within the file>.
update-param(<param>): 20 -> 30 pt; <reason>.
refactor-fn(<Class>.<method>): <description of restructuring>.
refactor-folder(<folder>/): <description of reorganisation across the folder>.
refactor-repo: <description of a convention applied across the repo>.
rename-file(<file>.py -> <new_file>.py): <reason>.
rename-repo(<old_name> -> <new_name>): <where the new name stops applying>.
move-fn(<function>): <old_file>.py -> <new_file>.py.
bump-dep(<dependency>): <old_hash> -> <new_hash>; <what the new version provides>.
```

---

## Presenting Commits

| Rule | Detail |
|---|---|
| Format | one shell block per commit containing both `git add` and `git commit` |
| Navigation | always use `cd` to enter the repo; never use `git -C` |

Single repository:

```bash
cd <repo>
git add <path/to/file.py>
git commit -m "<action>-<scope>(<file.py>): <description>."
```

Multiple repositories:

```bash
cd <repo-a>
git add <path/to/file.py>
git commit -m "<action>-<scope>(<file.py>): <description>."
```

```bash
cd <repo-b>
git add <path/to/other_file.py>
git commit -m "<action>-<scope>(<other_file.py>): <description>."
```

---

## Git Helpers

Use the `git_helpers` CLI (`<git-helpers>`) for git operations where a command exists. Fall back to raw `git` only when no equivalent command exists. Full reference: `<git-helpers>/README.md`.
