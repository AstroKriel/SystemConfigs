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

Simulation interface layers preserve the representation of the data as read from disk. If the source data are `float32`, loaders return `float32` fields by default rather than silently casting/promoting to `float64`.

Numerical promotion belongs in the computation layer (`jormi/`). When an operation requires higher precision for correctness or stability, the compute-side implementation converts or promotes the relevant arrays there.

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

During active development, personal libraries are referenced as editable installs. The path for sindri packages is `../submodules/<package-name>`; see `code/python/setup-module.md` for the full pattern.

Once a project has matured and the dependency has stabilised, personal libraries are referenced as a pinned git commit:

```toml
[tool.uv.sources]
<package-name> = { git = "https://github.com/<username>/<package-name>", rev = "<commit-hash>" }
```

---

## Terminal Feedback

User-facing terminal feedback in Asgard projects uses `jormi.ww_io.manage_log`. This covers actions, progress messages, warnings, summaries, skipped work, created/saved files, validation-script pass/fail status, and other operational messages intended for a person reading the terminal.

Pure compute helpers, low-level transformations, and routine internal state do not use `manage_log`; they return values or raise exceptions. Raised exceptions are not replaced with logging unless the function is responsible for handling the error and continuing.

Direct terminal output is limited to: the logger implementation itself, generated shell-script content, and raw child-process output streamed by a subprocess helper. `print()` is not used for user-facing feedback; functions accept a `verbose` flag when a message is optional.

### Log functions

All messages: lowercase throughout; names and identifiers in backticks, runtime data bare. No redundant prefixes (`"Note:"`, `"Warning:"`, `"Error:"`) in messages.

| Function | When to use | Form |
|---|---|---|
| `log_section` | major phase boundary in script output | noun phrase title; no period |
| `log_context` | current parameters or config at the start of a run | noun phrase title; no period |
| `log_task` | before a long-running operation starts | present participle: `"reading file: {path}"`; no period |
| `log_note` | neutral observation worth surfacing (e.g. timing, counts) | sentence or noun phrase; period |
| `log_items` | enumerate a list of things under a title | noun phrase title; noun phrases or short sentences as items; no period |
| `log_hint` | non-fatal issue; data clipped, parameter ignored, fallback applied | sentence; period |
| `log_alert` | something unexpected that may indicate a problem but does not stop execution | sentence; period |
| `log_warning` | soft error condition; pairs with `raise_error=False` | sentence; period |
| `log_error` | non-raising failure; operation failed but execution continues | sentence; period |
| `log_action` | completed operation with outcome, title, and optional notes | noun phrase title; sentence message |
| `log_outcome` | pass/fail result for an individual vtest case | noun phrase; no period |
| `log_summary` | end-of-run summary with key metrics | noun phrase title; key-value notes, values bare; no period |
| `log_debug` | temporary verbose detail; remove once the issue is resolved | sentence; period |
