# HPC Workflow

How to work on HPC clusters, covering onboarding, module loading, job submission, and data management.

---

## Storage Tiers

| Concept | Role | Typical names |
|---|---|---|
| `home` | Persistent, backed up, small quota; for configs and code checkouts | `/home/<user>` |
| `fast-storage` | High-throughput, large capacity, not backed up; for active runs and outputs | `scratch`, `work`, `lustre`, `nobackup` |
| `project` | Shared with collaborators, larger quota; not available on all clusters | `project`, `group` |

When working on a specific cluster, resolve these concepts from the cluster notes before acting.

---

## Onboarding a New Cluster

When access to a new cluster is gained:

1. Create the cluster notes at `<project-notes>/hpcs/<cluster>/` following [`<rules>/workflow/note-taking/hpc.md`](../note-taking/hpc.md)
2. Add a host entry to `~/.ssh/config` per `./ssh.md`
3. Log in and identify the available storage tiers; map each to its actual path
4. Survey the module environment: compiler toolchain, MPI, HDF5/parallel I/O stack
5. Submit a minimal test job to verify scheduling and I/O work
6. Record the storage tier paths and working module stack in the cluster `README.md`

---

## Job Scripts

Directives are scheduler-specific (SLURM uses `#SBATCH`, PBS uses `#PBS`); check the cluster `README.md` for the scheduler type.

**Naming:** `<project>-<descriptor>`, short enough to read in the queue.

**Working directory:** set explicitly to the run directory using `--chdir` (SLURM) or `-d` (PBS). Do not rely on submission directory or home directory defaults.

**Module loading:** always `module purge` before loading. Pin the full module string (name and version) from the cluster `README.md` and use it verbatim across all jobs for that cluster. Log any version changes in `log.md`.

**Checkpointing for wall-time-limited jobs:** For jobs that may run close to the partition's wall time limit, enable checkpointing at a coarse enough cadence that one or two checkpoints exist before the job ends. This allows a restart from near the cutoff rather than from the beginning.

**Validate before chaining:** Before submitting a build-then-run dependency chain (`sbatch --dependency=afterok:$BUILD_ID`), run the build step once in a short interactive or devel allocation first. A failing build marks all downstream jobs as `DependencyNeverSatisfied` with no diagnostic; the queue shows the symptom, not the cause, and jobs sit there burning wait time.

**Short test job before production at untested scale:** When the cluster's short or interactive queue runs ahead of the production queue, use a short test job (~100 steps) to validate an untested resolution or node count before tying up a long-queue slot. Check the application's startup output for the expected resource counts (MPI ranks, GPU devices); a misconfigured allocation can let the job start and run silently wrong.

---

## Module Architecture

On clusters with mixed CPU architectures, module system packages may be compiled for a specific ISA. A module-provided binary can crash with `SIGILL` on a node with a different architecture, even if it loaded cleanly on the login node.

Before relying on a module-provided binary for a build tool (e.g., make, ninja, ar, ranlib), verify it matches the architecture of the node where the build will run (`module show <name>` shows the build provenance). When in doubt:

- Use system binaries for low-level tools (e.g., `/usr/bin/ar`)
- Use portable installs for build drivers (e.g., `pip install --user ninja` installs a `manylinux` wheel that is portable across all x86_64 nodes)
- Record the working tool choices in the cluster notes

---

## Run Directory Layout

Simulations go under `<fast-storage>/<science-project>/`. Resolve `<fast-storage>` from the cluster's `## Instance` section before acting; on clusters with multiple allocation projects it maps to a project-specific placeholder (e.g. `<scratch-jh2>`), giving a full path of `<scratch-jh2>/<science-project>/`. Note that `<science-project>` is the research project name (e.g. `mhd-turbulence`), not an allocation project code.

Sim directories are grouped by scientific concept; each sim directory is self-contained (no symlinks) so it can be moved or archived without breaking.

| Concept | Role | Name defined by |
|---|---|---|
| `<sim-inputs>` | Config and input files the simulation reads | Code rules |
| `<sim-outputs>` | Raw output written by the simulation | Code rules |
| `<derived>` | Reduced data from analysis tools; what gets transferred locally | Code rules |

```text
<project>/
├── <concept>/
│   └── <sim-name>/
│       ├── jobs/
│       ├── <sim-inputs>
│       ├── logs/
│       ├── <sim-outputs>/
│       └── <derived>/
└── tmp/
```

`tmp/` follows the same concept and naming conventions as `~/tmp/` in [`<rules>/workflow/asgard/project.md`](../asgard/project.md), but on remote systems it lives under `<fast-storage>/<project>/`, not under `~`. Placing it on `home` consumes the small quota and causes usage spikes.

---

## Code Deployment

Deploy only what the cluster needs to execute the job: typically the project repo or the relevant `ww-*-sims` interface layer. Record what was deployed and any build steps in the cluster `log.md`.

### Syncing source changes: git, not rsync

Make code changes **locally**, commit, and push; then bring them to the remote with `git pull` (or `git fetch` + `git reset --hard origin/<branch>` when the remote working tree has stray edits). **Never `rsync`/`scp` source files between local and a cluster checkout.** Doing so desyncs the working tree from git history, breaks output provenance (the build no longer corresponds to a commit), and silently diverges the two trees. This applies to source code only; output data still comes back via the Data Transfer rules below.

### Source, builds, and data

| Artifact | Tier | Why |
|---|---|---|
| Source checkout | `home` (or a shared tier) | One checkout per cluster; small, version-controlled, shared across nodes. |
| Build tree | `fast-storage` (node-local) | Heavy artifacts stay off the small `home` quota, and a build can be node- or GPU-specific. Never build into `home`. |
| Run data | `fast-storage` | Bulk output; not backed up. |

Each project's notes declare where its data and builds live on each cluster, in a `## Data and builds` section of the project `README.md`, so locations stay discoverable.

### Builds under active development

When a codebase is under active development, builds and runs nest one level deeper, by thread (the project's `threads/`), so each build is tied to the branch for its thread:

- For out-of-source build systems (e.g. CMake), one source checkout is kept and each thread's build tree lives under the thread on `fast-storage`, configured against that source on the thread's branch.
- For codes where the build is the run directory (compile-time grid or modules baked in per run), each run directory is its own build, grouped by thread.

- A single source checkout is on one branch at a time; a thread's build is valid only while that branch is checked out.
- A thread's build and runs are deleted once the thread is shelved or merged.
- A matured project that pins a code version replaces the rolling per-thread builds with one frozen build at the pinned commit.

---

## Data Transfer

- Transfer only reduced data to a local machine; never transfer raw output.
- Use `rsync` and preserve directory structure.
