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
└── debug-diary/       # retrospective entries for resolved issues
    └── YYYY-MM-DD.md  # one file per resolved issue
```

| Belongs | Does not belong |
|---|---|
| Hardware specs and OS version | Config files themselves (those go in `<system-configs>/`) |
| Package and service installation steps | Project data or results |
| Non-obvious configuration decisions | HPC cluster details (see `hpc.md`) |
| Open and resolved configuration issues | Binding conventions (promote to `~/.rules/`) |

`pending-issues.md` is for issues that are currently open: unresolved problems, known workarounds in place, or configuration gaps. It is a live document; entries are added and removed as issues open and close.

`debug-diary/` is retrospective: each file records a resolved issue, what caused it, and how it was fixed. Entries are append-only and are never edited after the fact. When an issue is resolved, remove it from `pending-issues.md` and add a dated entry to `debug-diary/`.

To keep `setup.md` reproducible, update it whenever a significant configuration change is made: a new service, a package upgrade that required intervention, or a config change with machine-specific implications. When a machine is retired, add a final `README.md` note marking the retirement date and disposition.

### Research reference entry

```text
<project-notes>/pcs/<machine>/
└── README.md  # hardware summary, role, and code checkouts
```

The `README.md` covers: machine name and OS, a hardware summary table, the machine's role in the research workflow, a pointer to the setup repository, and a `## Codes` table (code name, checkout path, role). Do not repeat remote URLs here; those belong in the codebase's own notes.

To keep the reference entry current, update it whenever checkout paths change or the machine's research role changes.
