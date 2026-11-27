# Notes: Thread

A thread is one focused line of work inside a `<topic>` or another thread; each lives under `<topic>/threads/<thread>/`.

---

## Scope

A `<topic>` is any folder of notes with its own README, e.g. a project, a codebase, or a machine.

Open a thread when a question or piece of work takes more than one session, or more than a few commands, to settle. A thread can be shared on its own. It inherits no context from the rest of `<project-notes>`: it states any background the reader needs.

---

## Structure

A thread is organised by type of product. The README connects the products; each folder holds one type:

```text
<thread>/
├── README.md         # index of the products
├── log.md            # dated sections, appended as work happens
├── tasks.md          # open action items; see Design and tasks
├── notes/            # markdown: what is known now, edited in place
├── feedback/         # markdown headed into your own rules, tools, or projects; see feedback.md
├── scripts/          # what you run yourself: scripts, configs, fixtures, and the uv environment
├── data/             # small derived outputs that figures are redrawn from; never raw output
├── figures/          # figures the README links to
├── minimal-example/  # a minimal case packaged for someone else to build and run
└── threads/          # sub-threads
    └── archived/
```

`tasks.md`, `notes/`, and `feedback/` are open to every thread. The other folders depend on the kind of thread (see Kinds of thread). Every folder is created only when its first file arrives. A file that fits none of them goes into the closest one rather than into a new folder.

- `minimal-example/` is self-contained: source files in any language, build files, inputs, and a `README.md` with the steps to build and run, and the expected and observed result. It is the smallest case that shows the behaviour. When a recipient asks for an archive, such as a tarball attached to a bug report, the archive is built from this folder with a command given in its `README.md`, and is not stored.
- `scripts/` carries a self-contained `uv`-managed environment (`pyproject.toml` and `uv.lock`, with `.venv/` gitignored) so the scripts run with `uv run`. Shared libraries (e.g. `jormi`) are pinned to a git commit, never a local path, so the environment rebuilds wherever the thread is shared.
- A file in `notes/` that grows too large, or comes to span several parts, splits into a folder of the same name, with a `README.md` that indexes the parts; e.g. `design.md` becomes `design/README.md` and `design/<part>.md`. This is the structure ladder in [`writing/markdown.md`](../../writing/markdown.md).
- Papers do not go in a thread. They go in `notes/refs/` of the `<topic>` that holds the thread, and the thread cites them.

---

## README.md

The README is the one file to read first. It holds the index; the log sits next to it in `log.md`.

It opens with metadata:

- `**Opened:**` and, once settled, `**Resolved:**` dates;
- quick-reference fields such as `**Status:**`, `**Branch:**`, or `**PR:**`.

The metadata fields are the only content updated in place. For a resolved thread, one sentence of plain prose after `**Resolved:**` states the conclusion; it is written once.

Then comes `## Summary`: written once on opening, and not kept current. It ends with the index: a `| File | Covers |` table listing `log.md`, `tasks.md`, every file in `notes/` and `feedback/`, every sub-thread, and each other folder once.

Content that is kept current, such as a design or the open tasks, goes in `notes/` or `tasks.md`, not in the README.

Other threads are referenced by folder name in backticks (e.g. `<thread-name>/`), not by relative path, so the reference survives archiving.

---

## log.md

Dated sections, `## YYYY-MM-DD: <title>`, appended as work happens. The thread grows by appending, never by rewriting. The chain of observations, and what each ruled in or out, comes from these sections rather than from a separate narrative. The log starts, grows, and splits as in [`project.md`](project.md).

---

## Design and tasks

A design is the conceptual level: what a thing is and why. It is edited in place, and each entry is decided, proposed, or open.

Tasks are action items: work that can actually be done. They follow the task lifecycle in [`project.md`](project.md): checkboxes, ticked with a date when done, subtasks collapsing into their parent, and ticked tasks moving into the next dated section of `log.md`. When order matters, the subtasks of a campaign are listed in order, and each says how it is known to be done.

A decided design entry that is not built yet, or an open question, usually has a matching task.

The design of a tool you own lives at `<topic>/notes/design/`. A thing with no `<topic>` of its own keeps its design in the thread, in `notes/design.md`.

---

## Kinds of thread

The kind of a thread decides which products it usually has. These layouts are examples, not requirements; `feedback/` can appear in any of them.

### Debugging a problem

```text
<thread>/
├── README.md
├── log.md            # each attempt and what it ruled out; the last section names the file that shows the result
├── scripts/          # failing configs and check scripts
├── figures/          # when the behaviour shows in output
└── minimal-example/  # when the problem is reported to someone else
```

### Building code

For a library, a tool, or a feature. The code, its tests, and its validation live in the repository of the code. The thread holds the tasks and links to the branch and pull request; design decisions go to the design of the thing (see Design and tasks).

```text
<thread>/
├── README.md
├── log.md
├── tasks.md       # the steps, numbered when order matters
└── notes/
    └── design.md  # only when the thing has no <topic> of its own
```

### Investigating a question with simulations or calculations

```text
<thread>/
├── README.md
├── log.md
├── notes/
│   └── simulations.md  # one row per run: code and commit, machine, storage path, and why it was run
├── scripts/
├── data/
└── figures/
```

### Settling a tool through use

```text
<thread>/
├── README.md
└── log.md     # each use adds a dated section: what helped, what was missing, what was too much
```

### Coordinating with others

```text
<thread>/
├── README.md
├── log.md
└── notes/
    └── <proposal>.md  # proposals and drafts for others, e.g. one file per referee
```

A thread can change kind, e.g. from debugging a problem to building the fix. It then gains the folders of the new kind, and the log records the change.

---

## Sub-threads

A thread opens a sub-thread in its own `threads/` when a question arises inside it and only makes sense in its context.

- A question that serves several threads, or gathers existing ones, is a sibling instead, and references them by name.
- The parent index lists each sub-thread, and the parent log records the date it was spawned.
- A sub-thread is self-contained like any thread, and names its parent in backticks.
- One level of nesting is the norm. A third level is a sign that the middle thread has become a project of its own.

---

## Archiving

A thread is archived once it is resolved, or once it is set aside.

1. Empty `feedback/`, as described in [`feedback.md`](feedback.md).
2. Resolve each open sub-thread, or move it up one level if it has outlived the question of its parent.
3. Add `**Resolved:**` with its one-sentence conclusion, and a last dated section that says where each finding went: a rule, a tool, a project note, or nowhere.
4. Move the thread to `archived/` next to it, and update the index entry of the parent to the resolved status and date.

A conclusion carried out of a thread must not be stated more broadly than the thread established.
