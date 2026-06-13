# Project Notes

Notes on active research and teaching projects; each lives under `<project-notes>/`.

---

## Scope

A project note covers the context, status, tasks, and accumulated knowledge for a single research paper, teaching project, or supervision case.

Covered by this file:

| Category | Location |
|---|---|
| Research projects (lead author) | `<project-notes>/research/lead-author/<project>/` |
| Student supervision | `<project-notes>/research/student-projects/<student>/` |
| Teaching projects | `<project-notes>/<teaching-project>/` |
| Tools | `<project-notes>/<tool>/` |

---

## Structure: Research Projects

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

Each thread is a subfolder containing `README.md` and, if needed, `figures/`, and is a standalone investigation that can be shared on its own. A thread does not inherit context from the rest of `<project-notes>`: it states any background the reader needs, and a reference to another thread is made so that it still resolves when only the thread directories are shared (a relative link to the sibling thread), never by assuming the surrounding notes. The `README.md` opens with `**Opened:**` and, once settled, `**Resolved:**` dates, then states the bottom line (the resolution once settled, the open question while active); for an investigation, it then tells how the finding was reached as a deduction story, the observations and what each one ruled in or out, leading to the conclusion. Figures not tied to a thread belong in the project repo, not `<project-notes>`.

### log/

The log is an append-only session trail. Each file covers one session (named `YYYY-MM-DD.md`) and is a snapshot of what was understood at that moment. Notes and threads evolve over time; the log does not. Some duplication between the log and notes is expected and acceptable: if a finding first surfaces in a log entry, it belongs there even if it later appears in notes or threads. Omit stable reference material (parameters, storage paths, naming conventions); that belongs in `notes/`.

---

## Structure: Student Supervision

```text
<student>/
├── README.md  # who, project summary, degree milestones, current status
├── tasks.md   # current tasks for student and supervisor
├── log/       # dated meeting notes; one file per meeting named YYYY-MM-DD.md
└── notes/     # reference material (project description, setup details, etc.)
```

### notes/ and tasks/ pairing

When a project grows a `tasks/` folder, the `notes/` folder grows a matching file for each topic. The two files for the same topic are complementary: `tasks/<topic>.md` holds only active and pending work; `notes/<topic>.md` holds the durable record of what exists or has been done.

The lifecycle of a piece of work:
1. It starts as a task in `tasks/<topic>.md`.
2. When it completes, its record moves to `notes/<topic>.md`; the checkbox is removed, not just ticked.
3. `tasks/<topic>.md` shrinks over time. `notes/<topic>.md` grows.

A `tasks/<topic>.md` file that is nothing but ticked checkboxes is a sign the notes file is missing or out of date.

**What goes in `notes/<topic>.md`:**

- Organise by subject, then by system or subsystem (e.g. HPC cluster, machine, or environment) as subsections.
- Each dataset or run is recorded with its parameters listed as an itemised list before any table of runs. Parameters include resolution, stop time, plot interval, scheme, Mach number, and any other values a reader would need to reproduce or interpret the data.
- Contextual remarks and caveats following a table go in a `> **Note:**` blockquote, not as inline prose.
- Storage paths, naming conventions, and machine-assignment rationale belong here, not in tasks.

**What stays in `tasks/<topic>.md`:**

- Uncompleted checkboxes only. No reference material, no completed items, no storage layout docs.
- A brief status line at the top noting current priority and what is blocked or in flight.

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
