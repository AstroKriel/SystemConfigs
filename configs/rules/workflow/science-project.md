# Science Project

Lifecycle conventions for science projects: starting, running, and archiving.

Science projects live in the Asgard ecosystem. All project code builds on `jormi` as the shared foundation; interaction with specific simulation codes is provided by `ww-*-sims` interface layers. See `../code/asgard.md` for ecosystem conventions (structure, imports, logging).

---

## Starting a New mimir Project

Start a new mimir project once the core idea is solid and prototyping in `freyja/` has validated the approach.

Sequence:

1. Create the repo following the naming conventions in the Publication and Archival section below
2. Register it as a git submodule under `Asgard/mimir/`
3. Initialise a uv project and configure `pyproject.toml` per `../code/python/setup-project.md`
4. Add `jormi` and any relevant `ww-*-sims` packages as editable dependencies
5. Open a ProjectNotes directory: `~/Documents/ProjectNotes/<project>/` with `README.md`
6. Push to GitHub

### Initial structure

```text
<project>/
├── pyproject.toml
├── README.md
├── src/
│   └── <package>/
│       └── __init__.py
└── scripts/
```

`scripts/` holds entry-point scripts: analysis, figure generation, data pipeline steps. `src/<package>/` holds reusable library logic. Keep the two layers separate from the start.

---

## Scaffolding a New Interface Layer

When a project needs data from a simulation code not yet covered by a `ww-*-sims` package, create a new one under `Asgard/sindri/submodules/`.

Structure follows existing interface packages:

```text
ww-<code>-sims/
├── pyproject.toml
├── src/
│   └── ww_<code>_sims/
│       ├── __init__.py
│       ├── load.py
│       └── meta.py
└── utests/
```

`load.py` reads files from disk and returns `jormi` field objects. `meta.py` extracts run metadata: grid, units, simulation parameters. No array computation goes in the interface layer; all math belongs in `jormi/ww_arrays/`.

Reference the new package as an editable install during development. See `../code/asgard.md` for the `pyproject.toml` pattern.

---

## Publication and Archival

When a paper is accepted:

1. Rename the repo following the naming conventions below
2. Update the GitHub repository name and any local refs pointing to it
3. Tag the accepted-version commit: `git tag accepted`
4. Make no further changes after renaming
5. Add a final log entry to `ProjectNotes/<project>/log/` with the journal and acceptance date

The local folder name and the GitHub repository name follow different conventions:

| | Format | Example |
|---|---|---|
| Local folder | `<author1>[-<author2>]-<year>-<title-identifiers>` | `kriel-beattie-2025-curvature` |
| GitHub | `<Author1>[<Author2>]<year>_<title-identifiers>` | `KrielBeattie2025_curvature` |

For two or three authors, include all names; for more, use only the first author's name.

Precision promotion is not the responsibility of project code in `mimir/`; it belongs in `jormi/`. See `../code/asgard.md` for the data representation rule.
