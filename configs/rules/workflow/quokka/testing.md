# Quokka: Testing

Quokka testing: pre-push gates, smoke tests, convergence tests, and pass/fail signals.

## Before pushing

| Rule | |
|---|---|
| In-scope target | `AlfvenWaveLinear` for MHD changes; confirms the feature compiles and runs. |
| Out-of-scope target | `HydroBlast3D` or `RadMarshak` for MHD changes; confirms no unintended breakage outside the changed area. |

General principle: `workflow/git/review-branch.md`.

---

## Pass/fail signal

| Test type | Signal |
|---|---|
| `*Convergence` problems | Exit code from `quokka::richardson::run()`. Nonzero means measured order of accuracy fell below tolerance. |
| All other problems | Exit code `0` on clean integration. Internal asserts trip on NaN, negative pressure, FPE, and similar conditions. |

> **Note:** a clean exit is consistent with a silently broken solver. Always include at least one `*Convergence` problem when validating a code change.

---

## Solver-path changes

| Rule | |
|---|---|
| Full smoke-test before commit | Any change to a flux, reconstruction, EMF, or Riemann solver path must clear the full MHD smoke-test set (`AlfvenWaveLinear`, `BrioWuShockTube`, `OrszagTang`) before being committed. |
| No speculative commits | Do not commit a solver change as a hypothesis to test. Run the tests first, then commit only a change that demonstrably improves the target metric without regressing other tests. Revert immediately if it does not help. |

---

## MHD smoke-test set

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

---

## Convergence tests

| Rule | |
|---|---|
| Correctness gate | The `*Convergence` problems are the only tests that fail the exit code when the solver is wrong. Treat a nonzero exit as a real regression, not flakiness. |
| No resistivity | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. |
| MPI decomposition | Set `amr.blocking_factor_x = 16` and `amr.max_grid_size = 128`. |
| Rank count | Size `--ntasks` to the largest resolution in the sweep. At nx=512 on a single rank, the sweep takes hours; use at least 16 ranks. `max_grid_size=32` gives 16 boxes at nx=512 and is compatible with `blocking_factor_x=16`. |
| TOML overrides | Set `setup.machine_precision_target = 0` to disable early exit and run the full resolution sweep. Set `setup.nx_max = <N>` to control the maximum resolution (default is 128; set to 2048 for paper runs). |
