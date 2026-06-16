# Personal Machine Notes

Notes on machines you own and maintain; each has a setup repository and a research reference entry.

---

## Scope

Personal machine notes have two forms, serving different purposes:

**Setup repository**: a standalone repo in `SystemNotes/` that records the configuration, installation history, and operational knowledge for one owned machine. It is the reproduction manual for that machine: following it from a clean install should reproduce the working configuration.

**Research reference entry**: a lightweight reference sheet at `<project-notes>/pcs/<machine>/README.md`, analogous to an HPC reference sheet. It records the machine's role in the research workflow and which code checkouts live on it. It does not duplicate setup steps or config details; those belong in the setup repository. The reference entry is what to consult during active research; the setup repository is what to consult when (re)configuring the machine.

Both forms are distinct from HPC notes (see `hpc.md`): HPC notes record how to use a shared cluster; personal machine notes record how a machine is configured and used.

---

## Structure

### Setup repository

```text
SystemNotes/<machine>/
├── README.md          # machine name, OS, hardware summary, purpose
├── setup.md           # installation steps: OS, packages, configs, services
├── pending-issues.md  # open issues and unresolved configuration problems
├── notes/             # distilled facts about how subsystems work on this machine
│   └── <topic>.md     # one file per topic area; updated in place as understanding deepens
└── debug-diary/       # retrospective entries for resolved issues
    └── YYYY-MM-DD.md  # one file per resolved issue
```

| Belongs | Does not belong |
|---|---|
| Hardware specs and OS version | Config files themselves (those go in `<system-configs>/`) |
| Package and service installation steps | Project data or results |
| Non-obvious configuration decisions | HPC cluster details (see `hpc.md`) |
| Open and resolved configuration issues | Binding conventions (promote to `~/.rules/`) |

`pending-issues.md` is for issues that are currently open: unresolved problems, known workarounds in place, or configuration gaps. It is a live document; entries are added and removed as issues open and close. Every entry for an active workaround must include a concrete test command under "Next steps" that confirms the workaround is functioning. Without it, there is no defined pass or fail condition for post-update checks.

`debug-diary/` is retrospective: each file records a resolved issue, what caused it, and how it was fixed. Entries are append-only and are never edited after the fact. When an issue is resolved, remove it from `pending-issues.md` and add a dated entry to `debug-diary/`.

Every resolution gets a diary entry, including trivial ones that self-resolved upstream. A trivial entry can be brief (symptom, when first noticed, what resolved it, and the date), but it must exist. Without it, a recurrence has no context: no record of the original symptom, no indication of when it disappeared, and no basis for recognising that the same issue has returned.

If forum threads, bug reports, or upstream issues are found during investigation, include their URLs in the diary entry. They confirm the issue is not machine-specific and serve as a reference point if the issue recurs or evolves upstream.

`notes/` documents what was learned about this machine's subsystems: how they work, why they are configured the way they are, and where that understanding came from. Each file covers one topic area and is updated in place as understanding deepens. Record sources alongside facts: upstream documentation, man pages, forum threads, GitHub issues, and release notes. Knowing where information came from is part of the value; it surfaces which documentation is authoritative for each part of the system, so you know where to look when a related issue arises.

| Belongs | Does not belong |
|---|---|
| How a subsystem works on this hardware | Reproduction steps (those go in `setup.md`) |
| Known platform limitations and their causes | Active workarounds (those go in `pending-issues.md`) |
| Context explaining why a config is the way it is | Per-issue narratives (those go in `debug-diary/`) |
| Sources: upstream docs, man pages, forums, issues, specs | |

Update a `notes/` file whenever investigation uncovers how a subsystem works, why a config decision was made, or what an upstream change actually means. If the investigation was prompted by a specific issue or upgrade, reference the relevant `debug-diary/` entry or `pending-issues.md` entry at the top of the file. This links the knowledge back to the event that forced it.

To keep `setup.md` reproducible, update it whenever a significant configuration change is made: a new service, a package upgrade that required intervention, or a config change with machine-specific implications. When a machine is retired, add a final `README.md` note marking the retirement date and disposition.

### Research reference entry

```text
<project-notes>/pcs/<machine>/
└── README.md  # hardware summary, role, and code checkouts
```

The `README.md` covers: machine name and OS, a hardware summary table, the machine's role in the research workflow, a pointer to the setup repository, and a `## Codes` table (code name, checkout path, role). Do not repeat remote URLs here; those belong in the codebase's own notes.

To keep the reference entry current, update it whenever checkout paths change or the machine's research role changes.
