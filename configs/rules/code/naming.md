# Naming

File and folder naming on disk.

---

## In General

| Rule | |
|---|---|
| Casing | lower-case |
| Concept delimiter | `_` between words inside one concept: `<word>_<word>` |
| Concept separator | `-` between distinct concepts: `<concept>-<concept>` |
| Parameter in name | `<name>-<param>=<value>-<param>=<value>` |

```text
<concept>_<qualifier>-<param>=<value>
```

---

## Uppercase Exceptions

| Case | Pattern | Examples |
|---|---|---|
| Conventional scaffolding files | all-uppercase, casing itself is the signal | `README.md`, `CLAUDE.md`, `LICENSE`, `MEMORY.md` |
| Proper-noun roots | TitleCase or PascalCase, treated as a name | `SystemConfigs/`, `GitHelpers/`, `~/Downloads/`, `~/Pictures/` |
| Tool-mandated names | as the tool requires | `Makefile`, `Dockerfile` |

---

## In Python Packages

Python modules and packages must be valid identifiers, so `-` is not allowed; only `_` may separate words. See `~/.rules/code/python/naming.md` for the full convention.
