# Quokka: Data Extraction and Diagnostics

How to extract simulation output and diagnose failed Quokka runs.

---

## Tool

**Package:** `ww-quokka-sims`

- Activate the virtual environment before running any command.
- The environment path is machine-specific; check `<project-notes>` for the current host.

---

## Workflow

| Rule | Detail |
|---|---|
| Diagnostics first | The diagnostic commands are the primary interface with simulation data; use them before writing any custom extraction code. |
| Plot on the host | When sim data lives on a remote host, run the diagnostic commands there. Copy only the diagnostics outputs back. |
| Post-analysis from diagnostics | For comparisons or derived quantities, load the extracted `.npz`/data file from `diagnostics/`; do not re-read the plotfile. |
| Data over images | When `--save-data` has been run, all numerical conclusions must come from the saved data file. Do not read figure image files; figures are outputs for the user, not inputs for analysis. |
| Runs resume by default | Every `generate-*` command's `--overwrite` defaults to `False` (skip snapshots that already have output). Pass `--overwrite` explicitly to force a redo, e.g. after fixing a calibration issue upstream and re-running the same snapshots. |

**Extraction:**

1. **Inspect.** Run `quokka-inspect-snapshot --input-dir <snapshots-dir>` to confirm which field keys are available before running anything else.
2. **Extract.** Run the appropriate `generate-*` (or `extract-dataset`) command with `--save-data --data-dir <sim>/diagnostics`. This writes the figure and data to the sim's `diagnostics/` subdirectory; the tool defaults `--data-dir` to the snapshot's own parent directory if omitted, so pass it explicitly to land in `diagnostics/`. Raw plotfiles stay on the cluster or in `/tmp/`; only diagnostics products are committed.
3. **Sanity-check.** Run `quokka-generate-time-series --statistic rms` (or `total`) on the field(s) of interest to check the volume-integrated evolution before extracting detailed field data.

---

## Commands

| Command | Purpose |
|---|---|
| `quokka-inspect-snapshot` | List the field keys available in a snapshot. Run this first, before anything else. |
| `quokka-extract-dataset` | Extract full-domain field data to `.npz`; the base extraction step most other analysis builds on. |
| `quokka-generate-profiles` | Midplane 1D profiles of scalar or vector field components along any axis. |
| `quokka-generate-slices` | Midplane 2D slices of field components; `--animate` stitches an existing figure series into an MP4. |
| `quokka-generate-pdfs` | Probability distribution functions of field components over a snapshot or series. |
| `quokka-generate-spectra` | Isotropic power spectra of scalar fields. |
| `quokka-generate-time-series` | A time-evolving statistic (`--statistic rms\|total`) of a field across a snapshot series. |

These names changed from an older `quokka-plot-*` naming scheme (and a `quokka-plot-vi-evolution`/`-vi-comparison` pair that is no longer current); if a note or script elsewhere still uses `quokka-plot-*`, treat it as stale and update it, don't assume the old name still resolves. Field names, exact flags, and defaults live in each command's own `--help` — verify there rather than trusting a cached list, since the tool's flags/fields have drifted before and will again.

---

## Flags

| Flag | Applies to | Meaning |
|---|---|---|
| `--input-dir` | all commands | Directory of snapshot dirs (matched by `--tag`), or a single snapshot dir. |
| `--tag` | all commands | Snapshot prefix to match; default `plt`. |
| `--amr-level` | all commands | AMR level to read (composite of finest data up to and including this level); default `0`. |
| `--fields` | extract, profiles, slices, pdfs, spectra, time-series | Field name(s) to operate on; run `--help` for the current list. |
| `--comps` | extract, profiles, slices, pdfs | Vector-field component selector: `x_0`, `x_1`, `x_2`. |
| `--axes` | profiles, slices | Axis/axes to profile or slice along: `x_0`, `x_1`, `x_2`. |
| `--statistic` | time-series | `rms` or `total`. |
| `--data-dir` | extract, all `generate-*` commands | Output directory for extracted/derived data; defaults to the snapshot's own parent directory. |
| `--figures-dir` | all `generate-*` commands | Output directory for figures; defaults to `--data-dir`. |
| `--save-figure` / `--save-data` | all `generate-*` commands | Write a figure / write the underlying data; `extract-dataset` always writes data (no flag needed) and never makes a figure. |
| `--overwrite` | extract, all `generate-*` commands | Redo snapshots whose output already exists, instead of skipping them (default: skip). |
| `--num-workers` | extract, slices, time-series | Parallelise across snapshots; not available on profiles/pdfs/spectra. |
| `--use-log10-bins` | pdfs only | Bin `log10(|field|)` values instead of raw values. Does not affect the plotted/saved output scale the way `--apply-log10-plot` does elsewhere. |
| `--apply-log10-plot` | slices, time-series | **Known bug:** the underlying computation succeeds but the figure-save step crashes (`not a PNG file`); does not affect the saved `.npz`/data file. Workaround: omit this flag, run with `--save-data` only, then compute `log10` locally on the pulled data before plotting. **Needs checking (2026-11-25):** the `jormi` notes trace `not a PNG file` to a matplotlib cache race fixed by `matplotlib>=3.10.6`; if `ww-quokka-sims` now locks that version, this bug and its workaround may be stale. |
| `--animate` / `--no-annotations` | slices only | Stitch existing figures into an MP4 / suppress the min-max-and-sim-time annotation overlay. |
| `--num-bins` | pdfs only | Histogram bin count; default `20`. |

---

## Diagnosing a Failed Run

### Triage sequence

**1. Check for output.** Look for plotfiles in `snapshots/`. If none exist, go to [No output](#no-output).

**2. Plot what ran.** Run diagnostic commands on the HPC, directing output to a new `tmp/` subdirectory:

```bash
quokka-generate-time-series --input-dir <sim>/snapshots --data-dir <project>/tmp/vi-check/<YYYYMMDD>-initial --fields kinetic_energy magnetic_energy --statistic total --save-figure --save-data
```

Pull only the figures locally and inspect visually.

**3. Dig deeper if needed.** If the volume-integrated quantities show a problem (blow-up, stall, unexpected drift), run further `generate-*` commands targeting the relevant fields. Pull figures only until the cause is clear.

**4. Check the logs, live if needed.** If the job script redirects to `logs/run.log` (see [`workflow/quokka/build.md`](build.md), Run settings), `tail` it directly. Otherwise, for a still-running PBS job, use `qcat -o <jobid>` to read the scheduler's live-captured stdout without waiting for completion — `logs/` and the final `.o<jobid>` file both stay empty until the job ends. Either way, confirm when the run stopped (or whether it's still progressing) and whether it was a scheduler kill or a code exit.

### No output

If plotfiles were configured but none were written, the run failed before producing anything. Start with the log (see step 4 above):

- Config or TOML parsing errors appear at the top of the AMReX output.
- A missing file or bad path will error immediately on startup — including the wrong-working-directory failure mode in [`workflow/quokka/build.md`](build.md) (`Couldn't create directory: snapshots/plt0000000`), which looks like a code bug but is a job-submission mistake.
- A scheduler kill before the job started leaves no AMReX output at all; check the job accounting.

### Stuck, not crashed: sim time frozen despite active CPU/GPU use

A run can sit at 99%+ CPU/GPU utilization (check `resources_used.cpupercent` via `qstat -f <jobid>`, or the SLURM equivalent) while making essentially zero physical progress for a long stretch — this is a real, silent failure mode distinct from either a clean run or a crash, and it burns wall-time without ever producing an error.

**Signature** (visible in the log with `amr.v = 1`): the same `Coarse STEP` sim-time value repeats across many consecutive steps, `dt` sits many orders of magnitude below a normal value and creeps up slowly (often ~10% per step, since most codes cap how fast the timestep is allowed to recover), and the "timestep limited by" diagnostic keeps naming the **same** cell coordinates every step:

```
...[level 0] 	hydro timestep limited at cell (162, 30, 13) with signal speed = 3.281759e+23
...[level 0] 	cell density = 2.080185e-25, |v| = 5.405361e+00, cs = 1.000000e+00
```

**Root cause (MHD specifically):** a cell has rarefied toward near-vacuum density. The Alfvén speed scales as `B / sqrt(rho)`, so as density collapses, the local signal speed used for the CFL constraint diverges even though velocity and sound speed look unremarkable — this is what an astronomically large `signal speed` alongside an ordinary `|v|`/`cs` means. FOFC (first-order flux correction; always active, see `abortOnFofcFailure_` in `QuokkaSimulation.hpp`) does not necessarily fire on every step where this cell is the timestep limiter — grep the log for `FOFC` and compare how often it fires to how often the same cell is named as the limiter; a large gap means the cell is sitting in an extreme-but-not-yet-flagged-as-bad regime most of the time, unaddressed by the safety net.

**Prevention:** set `dt_cutoff` (see [`workflow/quokka/build.md`](build.md), Run settings) so a run in this state aborts within minutes instead of grinding at a near-zero `dt` for however long the walltime allows. Detecting this by eye (watching for a frozen sim-time in the log, or `resources_used.cpupercent` via `qstat -f` staying high with no new output) works, but costs however many GPU-hours pass before someone notices.

**Recovery, in roughly increasing order of effort:**

1. Kill the job.
2. Identify the last checkpoint written *before* the cell started diverging (compare checkpoint timestamps/sim-times against when the frozen sim-time first appears in the log).
3. Remove any snapshots/checkpoints written after that point, so the restart doesn't collide with stale output.
4. Lower `cfl` (e.g. halve it) and restart from that checkpoint with `restartfile = <checkpoint-path>` — gentler per-step flux changes reduce the odds of driving any single cell to vacuum-like density before FOFC (or the next checkpoint) can catch it. Treat this as a delay, not a fix: in practice a lower CFL let a run get further before hitting the same failure mode again, at a different cell, rather than preventing it.
5. Try a density floor (`density_floor = <value>`, see [`workflow/quokka/build.md`](build.md), TOML parameters) on top of the lower CFL. Same caveat as CFL: this can also just delay the failure to a later time and a different cell rather than resolve it, so don't treat a clean run for N snapshots as confirmation it's fixed. **Needs checking (2026-11-25):** `build.md` has no TOML parameters section and does not mention `density_floor`; confirm the parameter name and point this at its real reference.
6. If the reconstruction scheme is `hydro.reconstruction_order = 5` (PPM-EP, the xPPM-WENO hybrid), the most effective lever found so far is dropping to `3` (plain PPM) for both `hydro.reconstruction_order` and `mhd.emf_reconstruction_order`. PPM-EP's extremum-preserving property is more prone to producing the unphysical reconstructions that trigger this failure at extreme density contrasts (see the `PositivePrimitiveReconstruction` fix upstream, which targets exactly this); plain PPM's more diffusive limiter avoided the failure entirely in a case where lowering CFL and adding a density floor both only delayed it. This costs accuracy in resolved turbulent structure, so treat it as a robustness fallback, not a default.
7. Re-run from `t=0` only if no checkpoint predates the divergence — restarting from a checkpoint that already contains the collapsing cell just resumes the same trajectory.
