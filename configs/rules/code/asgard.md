# Asgard Project Conventions

Conventions for the `Asgard/` project, complementing and overriding the general `python/` conventions where they overlap.

---

## README Files

README files in `Asgard/` default to project-local workflow notes; `~/.rules/writing/docs.md` is the baseline, with these exceptions:

- a mildly personal tone is acceptable when the README documents the author's workflow or repo conventions
- Unicode tree diagrams are acceptable when they are the clearest way to show repository layout
- concise prose is preferred over rigid formal structure when the file is mainly for day-to-day use

---

## Data Representation

- Interface layers preserve the source representation: `float32` data returns as `float32`, not silently promoted to `float64`.
- Numerical promotion belongs in the computation layer (`jormi/`); the compute-side implementation converts or promotes arrays when an operation requires higher precision.

---

## Imports

Asgard projects extend the standard import order with two additional library groups, placed based on how the dependency is referenced:

| Group | Purpose |
|---|---|
| `## stdlib` | Python standard library |
| `## third-party` | external packages |
| `## personal (remote)` | personal libraries referenced as a pinned git commit |
| `## local` | imports from within the current project |
| `## personal (local)` | personal libraries referenced as an editable install |

---

### Referencing Personal Libraries

During active development, personal libraries are referenced as editable installs. The path for sindri packages is `../submodules/<package-name>`; see [`code/python/setup-module.md`](python/setup-module.md) for the full pattern.

Once a project has matured and the dependency has stabilised, personal libraries are referenced as a pinned git commit:

```toml
[tool.uv.sources]
<package-name> = { git = "https://github.com/<username>/<package-name>", rev = "<commit-hash>" }
```

---

## Terminal Feedback

- User-facing terminal feedback uses `jormi.ww_io.manage_log`: actions, progress messages, warnings, summaries, skipped work, created/saved files, validation-script pass/fail status, and other operational messages intended for a person reading the terminal.
- Pure compute helpers, low-level transformations, and routine internal state do not use `manage_log`; they return values or raise exceptions. Raised exceptions are not replaced with logging unless the function is responsible for handling the error and continuing.
- Direct terminal output is limited to: the logger implementation itself, generated shell-script content, and raw child-process output streamed by a subprocess helper. `print()` is not used for user-facing feedback; functions accept a `verbose` flag when a message is optional.

---

## Scaffolding a New Interface Layer

When a project needs data from a simulation code not yet covered by a `ww-*-sims` package, create a new one under `Asgard/sindri/submodules/`.

```text
ww-<code>-sims/
├── pyproject.toml
├── src/
│   └── ww_<code>_sims/
│       ├── __init__.py
│       └── <module>.py   # internal organisation grows as the interface matures
└── utests/
```

The package bridges the simulation code's file format to jormi field objects. What belongs here:

- loading from disk: read raw data from the simulation's file format; return jormi field objects
- metadata: grid, units, and simulation parameters from snapshot files
- format-specific derived fields: quantities that require knowledge of the simulation code's conventions or variable layout; general reusable physics computations belong in `jormi/` instead

Reference the new package as an editable install during development. See [Referencing Personal Libraries](#referencing-personal-libraries) for the `pyproject.toml` pattern.
