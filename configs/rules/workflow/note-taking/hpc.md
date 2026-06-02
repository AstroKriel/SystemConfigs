# HPC Notes

Notes on HPC clusters you use but do not own or administer; each lives under `<project-notes>/hpcs/`.

---

## Scope

An HPC note covers a cluster that is accessed remotely: login details, hardware specs, scheduler configuration, storage layout, and accumulated operational knowledge. It does not cover setup steps that belong in a per-machine setup repo (see `personal-machine.md`).

Location: `<project-notes>/hpcs/<cluster>/`

---

## Structure

```text
hpcs/<cluster>/
├── README.md  # cluster reference sheet; includes codebase-specific build sections where needed
├── log.md     # dated entries: outages, queue changes, module updates, workarounds
└── tasks.md   # open setup and documentation tasks
```

The `README.md` is the reference sheet: everything needed to start a session from scratch. It should include the login hostname, available partitions, and the storage tier paths mapped to the concepts defined in `workflow/remote-work/hpc.md` (`home`, `fast-storage`, `project` where available). Also record any non-standard module load sequences, and a single minimal job script inline as a `## Minimal Job Script` section. Do not keep a separate folder of job-script templates: the canonical submission files for a run live in that run's `jobs/` directory on the cluster (see `workflow/remote-work/hpc.md`), and the inline minimal script covers the host-specific pattern.

When a codebase requires host-specific build steps (toolchain sourcing, GPU backend flags, module stack), add it as a `### <codebase>` subsection under the README's `## Software` section (titled `## Software` or `## Software / Modules`), alongside the cluster's general module notes.

---

## What belongs here

| Belongs | Does not belong |
|---|---|
| Hardware specs and partition layout | Output data from runs |
| Storage tier paths and quotas | Project-specific analysis |
| Scheduler flags and queue behaviour | Config files or shell config (those go in setup repos) |
| Module load sequences | Binding workflow conventions (promote to `~/.rules/`) |
| Known outages and maintenance windows | |

---

## Keeping notes current

Update `README.md` when login details, storage paths, or scheduler configuration change. Add a log entry for outages, unexpected queue behaviour, or environment changes that affected a run. Use `tasks.md` for open setup and documentation items.

When the cluster is no longer in active use, add a final log entry and archive the directory.
