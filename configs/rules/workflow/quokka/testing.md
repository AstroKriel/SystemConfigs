# Quokka: Testing

How to test Quokka before pushing, from smoke tests through convergence tests and pass/fail signals.

## Testing tiers

Tests escalate across three tiers, in increasing cost and authority. The first two are run by hand before opening a pull request; the third runs automatically on it.

| Tier | What it is | Role |
|---|---|---|
| `local` | The personal development machine | Fast edit-compile-run iteration and the smallest smoke tests, finishing in seconds to minutes. CPU only, unless the machine has a usable GPU. |
| `cluster` | A shared interactive machine with more cores and at least one GPU | Broader pre-PR validation that `local` cannot provide: CPU-and-GPU coverage and medium-resolution sweeps. |
| `continuous integration` | The automated test suite that runs on the pull request | The authoritative correctness gate: high-resolution sweeps across both architectures. Not run by hand. |

Production and campaign machines are a separate category, not a testing tier.

---

## Before pushing

| Rule | Detail |
|---|---|
| Always run with MPI | Always prefix the executable with `mpirun -n <N>`, where `<N>` is the core count for the current machine (see machine notes). Running single-proc inflates wall time by the full rank count and defeats the time budget. |
| Test the changed-area | A problem that exercises the modified code. For MHD changes, `SlowWaveConvergence` is the primary correctness probe (compressive; couples all MHD modes; most sensitive to solver defects). `AlfvenWaveLinearConvergence` is a quicker smoke check and the vehicle for induction/resistivity validation. |
| Test unrelated-areas | A problem outside the modified code (`HydroBlast3D` or `RadMarshak` for MHD changes); confirms no unintended breakage elsewhere. |
| Test on CPU and GPU | Run the pre-push tests on both a CPU build and a GPU build before opening a PR. This is mandatory for any change that touches device code (flux, reconstruction, electromotive force [EMF], Riemann, or time-stepping kernels): changes may pass on CPU, but fail on GPU through lambda-capture errors, managed-memory races, or device-side asserts, so CPU-only validation is insufficient whenever the change could affect GPU execution. The GPU build belongs to the `cluster` tier when the `local` machine has no usable GPU. |
| Time budget | Keep the `local` and `cluster` pre-PR runs to a fast sanity gate (tests and resolutions finishing within ~5 min); the `continuous integration` tier exercises far finer levels. |
| Resolution scope | Limit convergence sweeps to `nx_max = 512` on the `local` and `cluster` tiers: high enough to confirm 2nd order convergence and catch the onset of degradation (the plain piecewise-parabolic method [PPM] stops converging by nx=256-512 on the slow wave), but low enough for quick validation. High resolutions (e.g. up to `nx_max = 2048`) are confirmed by the `continuous integration` tier. |

General principle: [`workflow/git/review-branch.md`](../git/review-branch.md).

---

## Pass/fail signal

| Test type | Signal |
|---|---|
| `*Convergence` problems | Exit code from `quokka::richardson::run()`. Nonzero means measured order of accuracy fell below tolerance. |
| All other problems | Exit code `0` on clean integration. Internal asserts trip on NaN, negative pressure, floating-point exceptions (FPE), and similar conditions. |

> **Note:** a clean exit is consistent with a silently broken solver. Always include at least one `*Convergence` problem when validating a code change.

---

## Solver-path changes

| Rule | Detail |
|---|---|
| Full smoke-test before commit | Any change to a flux, reconstruction, EMF, or Riemann solver path must clear the full MHD smoke-test set (`SlowWaveConvergence`, `BrioWuShockTube`, `OrszagTang`) before being committed. |
| No speculative commits | Do not commit a solver change as a hypothesis to test. Run the tests first, then commit only a change that demonstrably improves the target metric without regressing other tests. Revert immediately if it does not help. |

---

## MHD smoke-test set

| Problem | n_cell | stop_time | What it exercises |
|---|---|---|---|
| `SlowWaveConvergence` | sweeps `nx` 16..512 | per-resolution | Richardson sweep; the order-of-accuracy probe of this set (`BrioWuShockTube` and `OrszagTang` check stability, not order), and the most defect-sensitive wave. |
| `BrioWuShockTube` | `512x16x16` | `0.15` | 1D MHD Riemann problem; shock-capturing baseline. |
| `OrszagTang` | `128x128x8` | `1.0` | 2D MHD vortex; constrained-transport stress test. |

Run each with:

```bash
ninja -C build/3d-release <ProblemName>
cd tests && mpirun -n <N> ../build/3d-release/src/problems/<ProblemName>/<ProblemName> ../inputs/<ProblemName>.toml
```

**Tier-based domain scaling:** Never change `stop_time`; adjust `n_cell` only. Collapse dimensions that are not being resolved to 8 cells. Scale active-dimension resolution to the compute tier:

- `local`: 64 cells in active dims. `OrszagTang` becomes `64x64x8` (~3 min; nx^3 scaling from the reference 128^2 run of ~20 min). `SlowWaveConvergence` caps the sweep at `setup.nx_max=128`.
- `cluster`: reference `n_cell` from the table above.

---

## Convergence tests

| Rule | Detail |
|---|---|
| Correctness gate | The `*Convergence` problems are the only tests that fail the exit code when the solver is wrong. Treat a nonzero exit as a real regression, not flakiness. |
| No resistivity | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. |
| MPI decomposition | Set `amr.blocking_factor_x = 16` and `amr.max_grid_size = 128`. |
| Rank count | Size `--ntasks` to the largest resolution in the sweep. At nx=512 on a single rank, the sweep takes hours; use at least 16 ranks. `max_grid_size=32` gives 16 boxes at nx=512 and is compatible with `blocking_factor_x=16`. |
| TOML overrides | Set `setup.machine_precision_target = 0` to disable early exit and run the full resolution sweep. Set `setup.nx_max = <N>` to control the maximum resolution (default is 128; set to 2048 for paper runs). |

> **Note:** `max_grid_size = 128` gives one box of `128^3` cells per GPU. Scaling tests show strong scaling efficiency drops below 70% when cells per GPU fall below `128^3`; this is the minimum safe box size. `blocking_factor_x = 16` ensures grid dimensions are multiples of 16, satisfying GPU memory alignment requirements.
