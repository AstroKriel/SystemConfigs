# Personal Machine Notes

Notes on machines you own and maintain; each has its own setup repository, separate from `<project-notes>/`.

---

## Scope

A personal machine note is a per-machine setup repository: a standalone repo that records the configuration, installation history, and operational knowledge for one owned machine. It is the manual for that specific machine.

This is distinct from HPC notes (see `hpc.md`): HPC notes record how to use a shared cluster; personal machine notes record how a machine is configured and how to reproduce that configuration.

---

## Structure

Each machine has its own repository, stored wherever is convenient on that machine (e.g. `~/repos/<MachineName>/`). The repository structure:

```text
<MachineName>/
├── README.md  # machine name, OS, hardware summary, purpose
├── setup.md  # installation steps: OS, packages, configs, services
├── pending-issues.md  # open issues and unresolved configuration problems
└── debug-diary/  # retrospective entries for resolved issues
    └── YYYY-MM-DD.md  # one file per resolved issue
```

The `README.md` is the orientation document: what the machine is and what it is used for. `setup.md` is the reproduction guide: following it from a clean OS install should reproduce the working configuration.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Hardware specs and OS version | Config files themselves (those go in `<system-configs>/`) |
| Package and service installation steps | Project data or results |
| Non-obvious configuration decisions | HPC cluster details (see `hpc.md`) |
| Open and resolved configuration issues | Binding conventions (promote to `~/.rules/`) |

---

## Open issues vs. debug diary

`pending-issues.md` is for issues that are currently open: unresolved problems, known workarounds in place, or configuration gaps. It is a live document; entries are added and removed as issues open and close.

`debug-diary/` is retrospective: each file records a resolved issue, what caused it, and how it was fixed. Entries are append-only and are never edited after the fact.

When an issue is resolved, remove it from `pending-issues.md` and add a dated entry to `debug-diary/`.

---

## Keeping notes current

Update `setup.md` when a significant configuration change is made: a new service, a package upgrade that required intervention, a config change with machine-specific implications. The goal is that `setup.md` remains reproducible at any point in time.

When a machine is retired, add a final `README.md` note marking the retirement date and disposition.
