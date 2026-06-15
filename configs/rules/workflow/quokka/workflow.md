# Quokka: Build and Run

Building, configuring, and running Quokka.

## Related

| Location | What |
|---|---|
| `<quokka-checkout>/CLAUDE.md` | Architecture, build commands, code style, GPU safety. Maintained by the repo. |
| `<quokka-checkout>/AGENTS.md` | LLM agent guidance for the Quokka codebase. Maintained by the repo. |
| `<project-notes>/codebases/quokka/` | Orientation: what Quokka is, file locations on this machine. |
| `<project-notes>/<paper>/` | Paper project context and notes. |

---

## Build Directories

| Rule | |
|---|---|
| Always start cold | A build tree is only valid for the session, node architecture, and branch that created it. Delete `CMakeCache.txt` and reconfigure when resuming work in a new session, switching branches, or moving to a different node type. |
| One config per tree | Never share a build tree between configurations. Name each tree after its configuration, e.g. `build/3d-release`, `build/3d-debug`. |
| No Python | Always pass `-DQUOKKA_PYTHON=OFF`. Do not create a Python environment inside the quokka checkout; all analysis goes through `ww-quokka-sims`. |
| Toolchain | When a host needs a non-default compiler, source `~/.config/quokka/profile.sh` before running CMake. Per-host specifics live in `<project-notes>/hpcs/<host>/`. |
| Pin build tools explicitly | On HPC nodes, always pass `-DCMAKE_MAKE_PROGRAM`, `-DCMAKE_AR`, and `-DCMAKE_RANLIB` explicitly on the cmake command line, **and** `rm -f CMakeCache.txt` before configuring. Command-line `-DCMAKE_*` flags are silently overridden by cached values when `CMakeCache.txt` exists; deleting the cache is the only reliable fix. |

Common configurations:

```bash
cmake -S . -B build/3d-release -G Ninja -DCMAKE_BUILD_TYPE=Release -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF
cmake -S . -B build/3d-debug   -G Ninja -DCMAKE_BUILD_TYPE=Debug   -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF
cmake -S . -B build/3d-asan    -G Ninja -DCMAKE_BUILD_TYPE=Debug   -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF -DENABLE_ASAN=ON
```

On HPC nodes where system modules may be architecture-specific, use portable tool installs instead:

```bash
# Install a portable ninja wheel (manylinux, works on any x86_64 node):
pip install --user ninja          # installs to ~/.local/bin/ninja

# Then configure with explicit tool pins:
rm -f "$BUILD/CMakeCache.txt"
cmake -S "$SRC" -B "$BUILD" -G Ninja \
    -DCMAKE_MAKE_PROGRAM=$HOME/.local/bin/ninja \
    -DCMAKE_AR=/usr/bin/ar \
    -DCMAKE_RANLIB=/usr/bin/ranlib \
    ...
```

This avoids crashes when module-provided tools are compiled for a different CPU ISA than the build node. See `workflow/remote-work/hpc.md` for the general rule.

---

## Git Worktrees

Use git worktrees to work on multiple feature branches in parallel without switching branches or invalidating builds.

| Rule | |
|---|---|
| Main checkout on `development` | The primary checkout tracks `development`. Worktrees branch off from there. |
| One worktree per feature branch | Create a worktree for each active branch; delete it when the branch is merged or shelved. |
| Naming | Name each worktree after its branch with `/` replaced by `-`, placed as a sibling to the main checkout directory. Branch `<scope>/<type>/<name>` becomes `quokka-<scope>-<type>-<name>`. |
| Initialise submodules on creation | After `git worktree add`, run `git submodule update --init` inside the new worktree before building. |
| Extern drift | Each worktree has its own `extern/` working tree; submodule pins are per-branch. If a feature branch falls behind `development` on submodule pins, fix by merging or rebasing `development` into the feature branch so the pins come back into sync. |
| Build directories | Each worktree has its own build tree. On local, build dirs live inside the worktree (`build/3d-release`, etc.). On HPC, source lives on quota-limited Ceph home; build dirs go on node-local scratch. See Build locations below. |
| Trial run data | Short-lived `tmp/` runs belong inside the feature worktree, not the main checkout. |

```bash
# Create a worktree for a feature branch (run from the main checkout):
git worktree add ../quokka-<branch-slug> <branch>
cd ../quokka-<branch-slug>
git submodule update --init

# Remove a worktree when the branch is merged or shelved:
git worktree remove ../quokka-<branch-slug>
```

### Build locations

Worktrees are the same concept on local and HPC; only where the build tree lives differs. `<branch-slug>` is the branch name with `/` replaced by `-` (e.g. `<scope>-add-<name>`).

**Local:** build dirs sit inside the worktree, source and build co-located. Run from inside the worktree directory:

```bash
cmake -S . -B build/3d-release -G Ninja -DCMAKE_BUILD_TYPE=Release -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF
cmake -S . -B build/3d-debug   -G Ninja -DCMAKE_BUILD_TYPE=Debug   -DAMReX_SPACEDIM=3 -DQUOKKA_PYTHON=OFF
ninja -C build/3d-release <ProblemName>
```

**HPC:** source worktrees live on quota-limited home; build trees go on node-local scratch. Use explicit `-S`/`-B` to separate them. Toolchain flags vary per host; see host notes and the portable tool install block in Build Directories above:

```bash
SRC=<codes>/quokka-<branch-slug>
BUILD=<scratch>/$USER/quokka-<branch-slug>/build/<config>
rm -f "$BUILD/CMakeCache.txt"
cmake -S "$SRC" -B "$BUILD" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DAMReX_SPACEDIM=3 \
    -DQUOKKA_PYTHON=OFF \
    # ... plus host-specific toolchain flags
ninja -C "$BUILD" <ProblemName>
```

`<codes>` and `<scratch>` are defined in `<project-notes>/hpcs/<host>/`. The worktree name (`quokka-<branch-slug>`) is the same in both cases; only the root path differs.

---

## The `quokka` Script

`scripts/bash/quokka` is a thin wrapper around CMake, Ninja, and CTest. Use it for listing problems, running tests, and CTest operations. Config and build use raw CMake and Ninja directly.

| Command | What it does |
|---|---|
| `quokka list` | List problem directories under `src/problems/`. |
| `quokka target` | Print the raw CMake target list. |
| `quokka clean` | Remove plotfiles, checkpoints, and output files from `tests/`. |

Typical workflow (after configuring a build tree):

```bash
# Build
ninja -C build/3d-release <ProblemName>

# Run
cd tests && ../build/3d-release/src/problems/<ProblemName>/<ProblemName> ../inputs/<ProblemName>.toml
```

### Prefer raw tools over the wrapper

Drive `cmake`, `ninja`, and the compiled binary directly rather than through `scripts/bash/quokka` or CTest; the wrapper and harness encode other contributors' tolerances and plumbing. Reserve the wrapper for listing problems and bulk test runs. Do not go below CMake to hand-invoke the compiler; the build system and its required flags are not optional.

---

## MHD Configuration

### Build requirement

`AMReX_SPACEDIM=3` is mandatory for all MHD problems. A 1D or 2D build silently omits all MHD targets with no warning. Changing `SPACEDIM` requires a fresh build directory.

### TOML parameters

**MHD schemes:**

| Parameter | Values | Notes |
|---|---|---|
| `mhd.emf_compute_scheme` | `"FelkerStone2017"`, `"Balsara2025"`, `"Quokka2026"` | How edge-centred EMFs are computed from face-centred fluxes. |
| `mhd.emf_averaging_scheme` | `"LondrilloDelZanna2004"`, `"Balsara2025"` | How EMFs are averaged at shared edges between adjacent faces. |
| `mhd.resistivity` | float, default `0` | Physical resistivity; enforces parabolic timestep limit `dt < dx^2 / (2 * eta)`. |

**Reconstruction and integration:**

| Parameter | Values | Notes |
|---|---|---|
| `hydro.reconstruction_order` | `1` (PCM), `2` (PLM), `3` (PPM), `5` (PPM-EP) | Spatial reconstruction order for hydro. |
| `mhd.emf_reconstruction_order` | `1` (PCM), `2` (PLM), `3` (PPM), `5` (PPM-EP) | Spatial reconstruction order for MHD. Must match `hydro.reconstruction_order` in convergence tests. |
| `hydro.rk_integrator_order` | `2` | RK2 time integration. Standard for all MHD runs. |
| `hydro.use_dual_energy` | `0` | Disable for MHD. |

**Grid and AMR:**

| Parameter | Recommended | Notes |
|---|---|---|
| `amr.max_level` | `0` | Single-level for most MHD tests. |
| `amr.blocking_factor_x` | `16` | See MPI decomposition below. |
| `amr.max_grid_size` | `128` | See MPI decomposition below. |
| `do_reflux` | `0` | Disable for single-level runs. |
| `do_subcycle` | `0` | Disable for single-level runs. |

### EMF scheme reference

| Compute scheme | Stability | Notes |
|---|---|---|
| `FelkerStone2017` | Most stable | Safe default; well-validated reference. |
| `Balsara2025` | Stable | |
| `Quokka2026` | Least stable | Known to go unstable for the slow wave at high resolution with PPM-EP. |

| Averaging scheme | Notes |
|---|---|
| `LondrilloDelZanna2004` | Standard upwind averaging. |
| `Balsara2025` | |

### MPI decomposition

Setting `amr.blocking_factor_x` to `max(16, nx)` and `amr.max_grid_size` to `nx` forces a single AMReX box at every resolution, making all MPI ranks beyond the first idle with no warning. Always set:

```toml
amr.blocking_factor_x = 16
amr.max_grid_size = 128
```

This allows AMReX to split a 512-cell domain into up to 32 boxes.

### Minimum cell count

The hydro stencil uses `nghost = 4`. A single-box periodic grid below 8 cells per dim has opposite-side ghosts overlapping inside the valid region. Use at least 8 cells per dim under periodic boundary conditions.

### Resistivity

Enable with `mhd.resistivity = <eta>`. The parabolic timestep limit is enforced automatically.

| Rule | |
|---|---|
| No resistivity in Richardson convergence tests | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. Resistivity validation uses `AlfvenWaveLinear`. |
| Reference input | `inputs/AlfvenWaveLinear_resistive.toml` (eta=0.01, grid-aligned, FS17+LD04). |
| Analytic reference | Amplitude decays as `exp(-gamma*t)` where `gamma = eta*k^2/2`. Velocity lags B by `phi = arctan(gamma/omega_real)`. |

---

## HPC Run Setup

Quokka maps onto the standard project layout from `workflow/remote-work/hpc.md`:

| Concept | Quokka name | Notes |
|---|---|---|
| `<sim-inputs>` | `<problem>.toml` | TOML input file for the problem |
| `<sim-outputs>` | `plotfiles/` | AMReX HDF5 plotfiles |
| `<derived>` | `derived/` | Extracted data from `ww-quokka-sims` |

```text
<concept>/<sim-name>/
├── jobs/
│   ├── sim.sh
│   └── extract.sh
├── <problem>.toml
├── logs/
├── plotfiles/
└── derived/
```

Point AMReX output to `plotfiles/` in the run TOML:

```toml
plotfile_prefix = "plotfiles/plt"
```

AMReX profiling output (`ProfData_*`) lands in the working directory; with `--chdir`/`-d` set to the run directory, this goes to the run root rather than `logs/`.

| Script | Purpose |
|---|---|
| `jobs/sim.sh` | Run the Quokka executable with the problem TOML |
| `jobs/extract.sh` | Run `ww-quokka-sims` diagnostics; output goes to `derived/` |

For short-lived trial runs (testing a parameter, trialing a scheme), use `tmp/` at the project root rather than a full `<concept>/<sim-name>/` directory. See `workflow/remote-work/hpc.md` for the naming convention.

### Run settings

| Rule | |
|---|---|
| Verbose output | Always set `amr.v = 1`. This enables FOFC firing counts, retry events, and other internal solver diagnostics that are silent at the default `amr.v = 0`. |
| Plotfiles | Always set `plottime_interval = <interval>`. Write snapshots at regular intervals so the evolution can be inspected, not just the outcome. A run that crashes with no plotfiles leaves nothing to analyse. |
| Pass TOML as a relative path | In SLURM job scripts, always pass the input file as a bare filename (`sim_params.toml`), not an absolute path, and set `--chdir` to the run directory. AMReX ParmParse treats any command-line token containing `=` as an inline key=value pair. Absolute paths through directories named with `key=value` segments (e.g. `angle=0-nx=1-ny=0-nz=0`) crash the parser silently with misleading errors about missing definitions. |

---

## Testing

### Before pushing

| Rule | |
|---|---|
| In-scope target | `AlfvenWaveLinear` for MHD changes; confirms the feature compiles and runs |
| Out-of-scope target | `HydroBlast3D` or `RadMarshak` for MHD changes; confirms no unintended breakage outside the changed area |

General principle: `workflow/git/before-push.md`.

---

### Pass/fail signal

| Test type | Signal |
|---|---|
| `*Convergence` problems | Exit code from `quokka::richardson::run()`. Nonzero means measured order of accuracy fell below tolerance. |
| All other problems | Exit code `0` on clean integration. Internal asserts trip on NaN, negative pressure, FPE, and similar conditions. |

A clean exit is consistent with a silently broken solver. Always include at least one `*Convergence` problem when validating a build or code change.

### Solver-path changes

| Rule | |
|---|---|
| Full smoke-test before commit | Any change to a flux, reconstruction, EMF, or Riemann solver path must clear the full MHD smoke-test set (`AlfvenWaveLinear`, `BrioWuShockTube`, `OrszagTang`) before being committed. |
| No speculative commits | Do not commit a solver change as a hypothesis to test. Run the tests first, then commit only a change that demonstrably improves the target metric without regressing other tests. Revert immediately if it does not help. |

### MHD smoke-test set

| Problem | n_cell | stop_time | What it exercises |
|---|---|---|---|
| `AlfvenWaveLinearConvergence` | sweeps `nx` 16..128 | per-resolution | Richardson convergence sweep; the only test with a real correctness signal. |
| `BrioWuShockTube` | `512x16x16` | `0.15` | 1D MHD Riemann problem; shock-capturing baseline. |
| `OrszagTang` | `128x128x8` | `1.0` | 2D MHD vortex; constrained-transport stress test. |

Run each with:

```bash
ninja -C build/3d-release <ProblemName>
cd tests && ../build/3d-release/src/problems/<ProblemName>/<ProblemName> ../inputs/<ProblemName>.toml
```

### Convergence tests

| Rule | |
|---|---|
| Correctness gate | The `*Convergence` problems are the only tests that fail the exit code when the solver is wrong. Treat a nonzero exit as a real regression, not flakiness. |
| Richardson refines nx only | Oblique modes (`num_modes_y != 0` or `num_modes_z != 0`) will not converge under this strategy. The tests abort on nonzero transverse modes. |
| No resistivity | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. |
| MPI decomposition | Set `amr.blocking_factor_x = 16` and `amr.max_grid_size = 128`. |
| Rank count | Size `--ntasks` to the largest resolution in the sweep. At nx=512 on a single rank, the sweep takes hours; use at least 16 ranks. `max_grid_size=32` gives 16 boxes at nx=512 and is compatible with `blocking_factor_x=16`. |
| TOML overrides | Set `setup.machine_precision_target = 0` to disable early exit and run the full resolution sweep. Set `setup.nx_max = <N>` to control the maximum resolution (default is 128; set to 2048 for paper runs). |
