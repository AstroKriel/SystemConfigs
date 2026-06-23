# Asgard Project Conventions

Conventions for the `Asgard` project, complementing and overriding the general `python` conventions where they overlap.

---

## Data Representation

Return data with the dtype it has on disk; do not promote a quantity when reading it from file (e.g. `float32` to `float64`). Promote at the part of the stack where work is done with or on the quantity, that way the conversion is visible and easier to track.

---

## Imports

Asgard adds `## personal (remote)` and `## personal (local)` to the standard import order, based on how the dependency is declared:

| Group | Purpose |
|---|---|
| `## stdlib` | Python standard library |
| `## third-party` | external packages |
| `## personal (remote)` | personal libraries referenced as a pinned git commit |
| `## local` | imports from within the current project |
| `## personal (local)` | personal libraries referenced as an editable install |

### Referencing Personal Libraries

During active development, reference personal libraries as editable installs; see [`<rules>/code/python/setup-module.md`](python/setup-module.md) for the full pattern.

Once a project matures and the dependency stabilises, pin personal libraries to a git commit:

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
- format-specific derived fields: quantities that require knowledge of the simulation code's conventions or variable layout; general reusable physics computations belong in `jormi` instead

Reference the new package as an editable install during development. See [Referencing Personal Libraries](#referencing-personal-libraries) for the `pyproject.toml` pattern.
