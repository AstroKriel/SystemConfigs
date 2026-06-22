# Codebase Notes

Notes on tools and codebases in active use; each lives under `<project-notes>/codebases/<code>/`.

---

## Scope

A code note covers a tool, library, or codebase that is used regularly but not owned or primarily developed here. It records how to use it, known quirks, and accumulated troubleshooting knowledge.

This is distinct from project notes: a code note is about the tool itself, not about a project that happens to use it.

**A tool you also develop.** When you own or primarily develop the code, its investigations and dated behaviour already live in the project notes, so the codebase note legitimately shrinks to a router: `README.md` plus file-location orientation pointing at the project notes and `~/.rules/`. With no pinned release, record a rolling baseline (branch + commit + date) in `log.md` rather than a version in the README.

---

## Structure

```text
codebases/<code>/
├── README.md  # what the code is, version in use, how to install and invoke
├── log.md     # dated entries: discovered behaviours, workarounds, version changes
├── recipes/   # reusable invocation patterns and configuration snippets
└── threads/   # focused investigations (bug hunts, validations); same shape as project threads
```

The `README.md` orients a new reader on its own. It is the only required file; `log.md`, `recipes/`, and `threads/` are created when first needed. Keep the README to orientation, and route the rest:

- a dated discovery goes in `log.md`;
- a reusable invocation or configuration snippet goes in `recipes/`;
- an investigation goes in `threads/` (the project thread shape in [`project.md`](project.md)), with any durable conclusion promoted back into the code `README.md` or `log.md`.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Installation and environment setup | Source code for the tool itself |
| Known bugs and workarounds | Results produced by running the tool |
| Invocation patterns and flags | Project-specific analysis using the tool |
| Version-specific behaviour | Binding conventions (promote to `~/.rules/code/`) |

---

## Keeping notes current

- Update `README.md` when the installed version or the canonical invocation changes.
- Add a log entry for any non-obvious behaviour discovered in use, even minor: future debugging often traces back to behaviour first noticed in passing.
