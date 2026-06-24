# HPC Notes

Notes on HPC clusters you use but do not own or administer; each lives under `<project-notes>/hpcs/<cluster>/`.

---

## Scope

An HPC note covers a cluster that is accessed remotely: login details, hardware specs, scheduler configuration, storage layout, and accumulated operational knowledge.

---

## Structure

```text
hpcs/<cluster>/
├── README.md  # cluster reference sheet; includes codebase-specific build sections where needed
├── log.md     # dated entries: outages, queue changes, module updates, workarounds
├── tasks.md   # open setup and documentation tasks
├── threads/   # focused investigations (a scheduler quirk, a perf problem); same shape as project threads
└── <node>.md  # per-node deltas when nodes differ (hardware, node-local scratch, GPU)
```

`README.md` is the only required file; `log.md`, `tasks.md`, and `threads/` are created when first needed.

The `README.md` is the reference sheet, holding everything needed to start a session from scratch:

- **Instance (`## Instance`):** a placeholder table at the top defining all account-specific values. Shared placeholders (`<username>`, `<home>`) go in one table. Per-project paths go under bold sub-labels (**`<project-code>:`**) with a one-line description and a placeholder table. Name path placeholders `<tier-project>` (e.g. `<scratch-jh2>`, `<gdata-jh2>`) so they are unambiguous when referenced anywhere else in the file. **Always include the code root(s) as named placeholders** (e.g. `<codes>` for a flat layout, or `<sim-codes>` and `<analysis-codes>` when grouped by type); workflow rules reference these placeholders (e.g. `<codes>/quokka-<branch-slug>` for worktrees) and they must resolve here. Every placeholder resolves to a literal string; `<project>` in job scripts is a runtime choice, not a placeholder to define here. SU budgets and current fill levels do not belong here; check them live with `nci_account` or equivalent.
- **Login hostname and access topology:** a sanitized snippet using placeholders defined in `## Instance`; the literal `~/.ssh/config` stays in the setup repo.
- **Partitions, scheduler flags, and queue behaviour.**
- **Storage tiers:** mapped to the `home`/`fast-storage`/`project` concepts (`project` where available).
- **Module load sequences:** the non-standard ones, under `## Software`.
- **Minimal job script:** one, inline, as `## Minimal Job Script`; not a folder of templates, since a run's submission files live in its `jobs/` directory on the cluster.
- **Installed codes (`## Codes`):** a table of name, checkout path, and role; paths use the `<codes>` (or equivalent) placeholder defined in `## Instance`, not hardcoded strings. No remote URLs or other codebase facts, which live in the codebase's own notes. If no codes are installed yet, include the section as a stub so the gap is visible.
- **Host-specific build steps:** a `### <codebase>` subsection under `## Software`, holding the distilled recipe only.
- **Hardware specs and filesystems:** for a single node; once nodes diverge these move to `<node>.md`.

**When something takes real work to get working,** record each part once:

| Output | Goes to |
|---|---|
| What you tried and what broke | `threads/` |
| A dated entry, linking back to the thread | `log.md` |
| The reusable result | the relevant README section (e.g. the `### <codebase>` build recipe) |

**When nodes differ:**

- each `<node>.md` holds only that node's deltas;
- every shared fact lives once in `README.md`;
- the from-scratch bar becomes `README.md` plus the relevant node file.

---

## Out of scope

What does not belong in the note, and where it goes instead:

- Output data from runs.
- Project-specific analysis (it lives in the project notes).
- Config and shell files (they live in the setup repo).
- Hardened workflow conventions, and generic scheduler/module usage, get promoted to `<rules>/`; keep only cluster-specific flags here.

---

## Citing sources

- Every non-obvious factual claim carries its source: a link for web-sourced facts; a verifying command for machine-checked ones.
- A command citation beats a date: it shows how to re-verify, not just when someone last checked.
- For hardware or system fact tables, add a `> **Note:**` after the table with a `| Purpose | Command |` table mapping each command to what it checks. One note covers the whole section; do not annotate individual rows.

---

## tasks.md lifecycle

Follows the same discipline as project notes (see [`workflow/note-taking/project.md`](project.md)):

- Only open items live in `tasks.md`. No ticked checkboxes, no reference material.
- When a task completes, move the relevant fact to the appropriate node file or `README.md`, then remove the task entry entirely.
- Tasks pending an external party (IT, sysadmin) get a status note inline: contact name, date sent, and what to verify once resolved. Example: `(emailed Ole 2026-06-22; confirm /vol/parzival/ssd mounts from lanzelot)`.

---

## threads/

Open a thread when an investigation takes more than a few commands to resolve -- a scheduler quirk, a filesystem anomaly, a performance problem. Each thread is a subfolder with a `README.md`:

- Opens with the question being investigated.
- Records the steps taken and what each one ruled in or out.
- Closes with the resolution and where the finding was promoted (node file, `README.md`, or `log.md`).
- Resolved threads move to `threads/archived/`.

Do not put the investigation trail in the node file or `README.md` directly; those hold only the reusable result.

---

## Keeping notes current

- Update `README.md` when login details, storage paths, or scheduler configuration change.
- Add a log entry for outages, unexpected queue behaviour, or environment changes that affected a run.
- Use `tasks.md` for open setup and documentation items.
- Storage quota ceilings are README reference; log the drifting current-fill levels instead, with the verifying command.
- When the cluster is no longer in active use, add a final log entry and archive the directory.
