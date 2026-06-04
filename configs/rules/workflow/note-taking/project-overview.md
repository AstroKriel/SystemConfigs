# Project Notes

Notes on active research and teaching projects; each lives under `<project-notes>/`.

---

## Scope

A project note covers the context, status, tasks, and accumulated knowledge for a single research paper, teaching project, or supervision case.

Covered by this file:

| Category | Location |
|---|---|
| Research papers | `<project-notes>/<paper>/` |
| Teaching projects | `<project-notes>/student-projects/`, `<project-notes>/bitesize-python/` |
| Student supervision | `<project-notes>/student-projects/<student>/` |

---

## Structure: Research Papers

Start with just `README.md`. Add files only as the project grows. Two guiding principles:

- The entry point for any folder is always `README.md`.
- A file splits into a folder of the same name when its content spans multiple domains or grows too large.

```text
<paper>/
├── README.md  # overview; becomes index as project grows
├── log/       # session trail; one file per session named YYYY-MM-DD.md
├── tasks.md   # task list; splits into tasks/ when tasks span multiple domains
├── threads/   # active explorations and open questions
└── notes/     # refs, background material, stable context
```

### README.md

The README is the entry point. It should orient anyone landing cold: what the project is, where to find things, and where to look for supporting context. For compute-heavy projects it includes three standard sections:

- `## Context`: relative-path pointers to the HPC notes, codebase notes, and rules that the project depends on. Use relative paths for anything inside `<project-notes>/`; use `~/.rules/<path>` for rules. Do not use absolute machine paths.
- `## Machines`: one row per machine, with its role in the project (e.g. which runs go where).
- The task and thread index sections that link to `tasks/` and `threads/`.

### threads/

Each thread is a subfolder containing `README.md` and, if needed, `figures/`. When a question is settled, add `**Resolved:**` at the top of the thread `README.md` with the conclusion in one sentence. Figures not tied to a thread belong in the project repo, not `<project-notes>`.

---

## Structure: Student Supervision

```text
<student>/
├── README.md  # who, project summary, degree milestones, current status
├── tasks.md   # current tasks for student and supervisor
├── log/       # dated meeting notes; one file per meeting named YYYY-MM-DD.md
└── notes/     # reference material (project description, setup details, etc.)
```

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Current status and open questions | Line-by-line code documentation |
| Key findings and decisions | Raw simulation output |
| Task lists | Configuration files (those go in the project repo) |
| Notes on sources and references | Working conventions (promote to `~/.rules/`) |
| Reproduction steps for a result | |

---

## Concluding a project

Add a final log entry marking the outcome (accepted, rejected, etc.) and archive the directory. Do not delete it.
