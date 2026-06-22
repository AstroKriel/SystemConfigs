# Quokka: MHD Configuration

How to configure Quokka for MHD simulations, covering TOML parameters, EMF schemes, and MPI decomposition.

## Build requirement

`AMReX_SPACEDIM=3` is mandatory for all MHD problems. A 1D or 2D build silently omits all MHD targets with no warning. Changing `SPACEDIM` requires a fresh build directory.

---

## TOML parameters

AMReX exposes many parameters and often multiple ways to achieve the same thing. This section documents the preferred parameters and values for MHD runs, not an exhaustive reference.

**`geometry` / `quokka` (domain setup):**

| Parameter | Values | Notes |
|---|---|---|
| `geometry.prob_lo` | float array | Lower corner of the domain per dimension. |
| `geometry.prob_hi` | float array | Upper corner of the domain per dimension. Cell size follows: `dx = (prob_hi - prob_lo) / n_cell`. |
| `quokka.bc` | `"periodic"`, `"reflecting"` | Required. Boundary conditions for all fields. Reflecting BC support for magnetic fields is incomplete; use periodic for MHD tests. |

**`amr`:**

| Parameter | Recommended | Notes |
|---|---|---|
| `amr.n_cell` | int array | Number of cells per dimension. Sets resolution; `dx` follows from domain size. |
| `amr.max_level` | `0` | Single-level for most MHD tests. |
| `amr.blocking_factor_x` | `16` | See MPI decomposition below. |
| `amr.max_grid_size` | `128` | See MPI decomposition below. |
| `do_reflux` | `0` | Disable for single-level runs. |
| `do_subcycle` | `0` | Disable for single-level runs. |
| `plotfile_prefix` | `"plotfiles/plt"` | Output path prefix for plotfiles; defaults to `plt` in the run working directory if absent. |

**`hydro`:**

| Parameter | Values | Notes |
|---|---|---|
| `hydro.rk_integrator_order` | `2` | RK2 time integration. Standard for all MHD runs. |
| `hydro.reconstruction_order` | `1` (PCM), `2` (PLM), `3` (PPM), `5` (PPM-EP) | Spatial reconstruction order for hydro. |
| `hydro.use_dual_energy` | `0` | Disable for MHD. |
| `hydro.artificial_viscosity_coefficient` | float, optional | Scalar viscosity coefficient; adds diffusive flux to momentum equations. Use to damp post-shock oscillations. |

**`mhd`:**

| Parameter | Values | Notes |
|---|---|---|
| `mhd.emf_compute_scheme` | `"FelkerStone2017"`, `"Balsara2025"`, `"Quokka2026"` | How edge-centred EMFs are computed from face-centred fluxes. |
| `mhd.emf_averaging_scheme` | `"LondrilloDelZanna2004"`, `"Balsara2025"` | How EMFs are averaged at shared edges between adjacent faces. |
| `mhd.emf_reconstruction_order` | `1` (PCM), `2` (PLM), `3` (PPM), `5` (PPM-EP) | Spatial reconstruction order for MHD. Must match `hydro.reconstruction_order` in convergence tests. |
| `mhd.resistivity` | float, default `0` | Physical resistivity; enforces parabolic timestep limit `dt < dx^2 / (2 * eta)`. |

---

## EMF scheme reference

All three compute schemes are stable and comparable in accuracy; `Quokka2026` is the recommended default (fastest).

| Compute scheme | Notes |
|---|---|
| `Quokka2026` | Recommended default. |
| `Balsara2025` | Alternative. |
| `FelkerStone2017` | Well-validated reference. |

| Averaging scheme | Notes |
|---|---|
| `LondrilloDelZanna2004` | Standard upwind averaging. |
| `Balsara2025` | |

---

## Resistivity

Enable with `mhd.resistivity = <eta>`. The parabolic timestep limit is enforced automatically.

| Rule | |
|---|---|
| No resistivity in Richardson convergence tests | `FastWaveConvergence` and `SlowWaveConvergence` abort if `mhd.resistivity != 0`. Resistivity validation uses `AlfvenWaveLinear`. |
| Reference input | `inputs/AlfvenWaveLinear_resistive.toml` (eta=0.01, grid-aligned, FS17+LD04). |
| Analytic reference | Amplitude decays as `exp(-gamma*t)` where `gamma = eta*k^2/2`. Velocity lags B by `phi = arctan(gamma/omega_real)`. |

---

## MPI decomposition

Setting `amr.blocking_factor_x` to `max(16, nx)` and `amr.max_grid_size` to `nx` forces a single AMReX box at every resolution, making all MPI ranks beyond the first idle with no warning. Always set:

```toml
amr.blocking_factor_x = 16
amr.max_grid_size = 128
```

This allows AMReX to split a 512-cell domain into up to 32 boxes.

---

## Minimum cell count

The hydro stencil uses `nghost = 4`. A single-box periodic grid below 8 cells per dim has opposite-side ghosts overlapping inside the valid region. Use at least 8 cells per dim under periodic boundary conditions.
