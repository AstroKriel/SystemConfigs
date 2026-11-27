# Notes: Project

Notes on active research and teaching projects; each lives under `<project-notes>/`.

---

## Scope

A project note covers the context, status, tasks, and accumulated knowledge for a single research paper, teaching project, or supervision case.

Covered by this file:

| Category | Location |
|---|---|
| Research projects (lead author) | `<project-notes>/research/lead-author/<project>/` |
| Student supervision | `<project-notes>/research/student-projects/<student>/` |
| Teaching projects | `<project-notes>/teaching/<teaching-project>/` |
| Tools | `<project-notes>/tools/<tool>/` |

---

## Structure: Research Projects

Start with just `README.md`. Add files only as the project grows. Two guiding principles:

- The entry point for any folder is always `README.md`.
- A file splits into a folder of the same name when its content spans multiple domains or grows too large (the top rung of the structure ladder in [`writing/markdown.md`](../../writing/markdown.md)).

```text
<paper>/
├── README.md      # overview; becomes index as project grows
├── log.md         # session trail; splits into log/ when it strains
├── tasks.md       # task list; splits into tasks/ when tasks span multiple domains
├── threads/       # threads; see thread.md
│   └── archived/  # resolved threads
├── feedback/      # findings headed into rules, tools, or other projects; see feedback.md
└── notes/         # background material and stable context; refs/ holds papers
```

### README.md

The README is the entry point. It should orient anyone landing cold: what the project is, where to find things, and where to look for supporting context. For compute-heavy projects it includes three standard sections:

- `## Context`: pointers to the HPC notes, codebase notes, and rules that the project depends on. For anything inside `<project-notes>/`, write the path root-relative as `<project-notes>/<path>` (not relative to the file the pointer sits in); use `<rules>/<path>` for rules. Do not use absolute machine paths. Threads are the exception: they are referenced as in [`thread.md`](thread.md), so the reference survives archiving.
- `## Machines`: one row per machine, with its role in the project (e.g. which runs go where).
- The task and thread index sections that link to `tasks/` and `threads/`. The thread index can live in `threads/README.md` instead, with the project README linking to it.

### threads/

Threads follow [`thread.md`](thread.md).

Figures not tied to a thread belong in the project repo, not `<project-notes>`.

### log.md

The log is an append-only session trail: each dated entry is a snapshot of one session's understanding at that moment. Notes and threads evolve; the log does not.

Every kind of note keeps its log the same way, and lets its form emerge like any other file on the structure ladder in [`writing/markdown.md`](../../writing/markdown.md):

- The log starts as `log.md` next to the `README.md`, never inside it. It opens with `# <Name>: Log`, and each entry is a `## YYYY-MM-DD: <title>` section. An entry can hold `###` subsections.
- Entries are appended in the order they are written. An entry written late keeps its place; it is not moved into date order, because the log is never rewritten.
- When `log.md` strains, it splits into a `log/` folder. Each file holds what one sitting would read: one file per day (`YYYY-MM-DD.md`) when entries are whole sessions, one file per year (`YYYY.md`) when entries are a few lines each.
  - A per-day file opens with `# YYYY-MM-DD: <title>`, and its parts are `##` sections.
  - A per-year file opens with `# <Name>: Log <YYYY>`, and holds `## YYYY-MM-DD: <title>` entries as `log.md` does.
- The `README.md` links to the log; it never holds log entries itself.

What goes in the log:

- Some duplication with notes is expected: if a finding first surfaces in a log entry, it belongs there even if it later appears in notes or threads.
- Omit stable reference material (parameters, storage paths, naming conventions); that belongs in `notes/`.

---

## Structure: Student Supervision

```text
<student>/
├── README.md  # who, project summary, degree milestones, current status
├── tasks.md   # current tasks for student and supervisor
├── log.md     # dated meeting notes; splits into log/ as in Structure: Research Projects
└── notes/     # reference material (project description, setup details, etc.)
```

---

## Tasks and Notes Pairing

Applies wherever a project has a task list and a `notes/` directory: research (lead-author and student supervision) and teaching projects alike, not student supervision only. The task list is `tasks.md` before it splits, `tasks/<topic>.md` after.

When a project grows a `tasks/` folder, the `notes/` folder grows a matching file for each topic. The two files for the same topic are complementary: `tasks/<topic>.md` holds only active and pending work; `notes/<topic>.md` holds the durable record of what exists or has been done.

Tasks are checkboxes. A task can hold subtasks, so that a group of steps sits under the campaign they carry out.

The lifecycle of a piece of work:

1. It starts as a task in `tasks.md` (or `tasks/<topic>.md` once split).
2. It grows as it needs to: one line, then a context paragraph under it, then a thread once it becomes an investigation, at which point the task points to the thread.
3. When it is done, it is ticked with its date, at whatever level it sits: `- [x] <YYYY-MM-DD>: <task>`.
4. When the parent itself is done, its subtasks are removed and the parent is ticked with the date it finished. Its sentence names the campaign, so the campaign is what remains at its level. A parent whose subtasks are all ticked, but whose own condition for being done is not met yet, keeps its subtasks.
5. Ticked top-level tasks move into the next dated log entry. Any durable fact the work produced, such as what now exists and where, goes to `notes/<topic>.md` (or the single notes file of the project before it splits).

A task dropped before it is done is ticked the same way and marked as dropped: `- [x] <YYYY-MM-DD>: dropped: <task>`, with the reason after it when it matters. It then follows the same lifecycle.

The task list stays short; the log keeps what was done, and `notes/` keeps what exists.

```markdown
- [ ] <campaign>
  - [x] <YYYY-MM-DD>: <step>
  - [ ] <step>
- [ ] <task>
```

A task list that is mostly ticked entries is a sign the log has not caught up.

**What goes in `notes/<topic>.md`:**

- Organise by subject, then by system or subsystem (e.g. HPC cluster, machine, or environment) as subsections.
- Each dataset or run is recorded with its parameters listed as an itemised list before any table of runs. Parameters include resolution, stop time, plot interval, scheme, Mach number, and any other values a reader would need to reproduce or interpret the data.
- Contextual remarks and caveats following a table go in a `> **Note:**` blockquote, not as inline prose.
- Storage paths, naming conventions, and machine-assignment rationale belong here, not in tasks.

**What stays in `tasks/<topic>.md`:**

- Open tasks, and ticked tasks that have not yet moved to the log. No reference material, no storage layout documents.
- A brief status line at the top noting current priority and what is blocked or in flight.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Current status and open questions | Line-by-line code documentation |
| Key findings and decisions | Raw simulation output |
| Task lists | Configuration files (those go in the project repo) |
| Notes on sources and references | Working conventions (draft in `feedback/rules.md`; see [`feedback.md`](feedback.md)) |
| Reproduction steps for a result | |

---

## Concluding a project

Add a final log entry marking the outcome (accepted, rejected, etc.) and archive the directory. Do not delete it.
