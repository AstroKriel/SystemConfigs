# HPC Notes

Notes for HPC clusters that are used but not owned or administered. Each cluster has its own directory under `~/Documents/ProjectNotes/hpcs/`.

---

## Scope

An HPC note covers a cluster that is accessed remotely: login details, hardware specs, scheduler configuration, storage layout, and accumulated operational knowledge. It does not cover setup steps that belong in a per-machine setup repo (see `personal-machine.md`).

Location: `ProjectNotes/hpcs/<cluster>/`

---

## Structure

```text
hpcs/<cluster>/
├── README.md  # cluster reference sheet; includes codebase-specific build sections where needed
├── log.md     # dated entries: outages, queue changes, module updates, workarounds
├── tasks.md   # open setup and documentation tasks
└── jobs/      # example job scripts and submission patterns
```

The `README.md` is the reference sheet: everything needed to start a session from scratch. It should include the login hostname, available partitions, and the storage tier paths mapped to the concepts defined in `workflow/remote-work/hpc.md` (`home`, `fast-storage`, `project` where available). Also record any non-standard module load sequences.

When a codebase requires host-specific build steps (toolchain sourcing, GPU backend flags, module stack), add a `## <codebase>` section to `README.md`.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Hardware specs and partition layout | Output data from runs |
| Storage tier paths and quotas | Project-specific analysis |
| Scheduler flags and queue behaviour | Dotfiles or shell config (those go in setup repos) |
| Module load sequences | Binding workflow conventions (promote to `~/.rules/`) |
| Known outages and maintenance windows | |

---

## Keeping notes current

Update `README.md` when login details, storage paths, or scheduler configuration change. Add a log entry for outages, unexpected queue behaviour, or environment changes that affected a run. Use `tasks.md` for open setup and documentation items.

When the cluster is no longer in active use, add a final log entry and archive the directory.
