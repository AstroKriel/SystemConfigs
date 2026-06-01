# Python: Module Setup

How to configure a Python library package: build backend, source layout, and editable installation.

---

## Structure

```text
<package>/
├── pyproject.toml
├── README.md
├── src/
│   └── <package>/  # the installable package
│       └── __init__.py
├── utests/  # unit tests
└── vtests/  # validation tests
```

---

## Build Backend

Use hatchling:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
sources = ["src"]
```

---

## Editable Installation

When another project consumes this package as a local dependency, declare it in `[tool.uv.sources]` in the consumer's `pyproject.toml`. Do **not** add `[tool.hatch.metadata] allow-direct-references = true`; that is only needed for direct URL references written inline in the `dependencies` list:

```toml
dependencies = ["<package-name>"]

[tool.uv.sources]
<package-name> = { path = "<relative-path>", editable = true }
```
