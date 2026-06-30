# Quokka: MHD Naming Conventions

Naming and comment conventions for `mhd_system.hpp` and adjacent MHD source files in `quokka`.

---

## Naming pattern

All variables follow:

```
[centering]_[type]_<quantity>[_<qualifier>]_[wcomp<value>]_[<index>...]
```

### Index loop variables

| Rule | Detail |
|---|---|
| Pattern | `[letter][what-it-indexes]`; a bare letter without a suffix is not permitted |
| Concrete values | when a slot value is known, use `[letter][value]` instead |
| No separators | single-concept index variables do not need underscore separators |

| Letter | Meaning | Examples |
|---|---|---|
| `i` | first (or only) array index | `icomp`, `ieside`, `iquad` |
| `j` | second array index in a two-indexed array | `jquad`, `jeside` |
| `w` | world-direction index (0=x, 1=y, 2=z) | `wcomp`, `wcomp0`, `wcomp1`, `wcomp2` |

### Centering prefix

| Prefix | Meaning |
|---|---|
| `cc_` | cell-centred |
| `fc_` | face-centred |
| `ec_` | edge-centred |
| `fcw_` | `std::array` of fc quantities; each element is fc in the direction of its slot index |

Omit only when centering is genuinely unknown at the declaration site (e.g. a generic helper that accepts any centering).

### Type marker

| Marker | Type |
|---|---|
| `mf_` | `amrex::MultiFab` |
| `fabs_` | `amrex::FArrayBox` (locally extracted) |
| `a4_` | single `amrex::Array4` |
| (none) | `std::array` of `amrex::Array4`; plural containers omit the type marker |

### Quantity name

Lowercase physics name (`b`, `u`, `emf`, `fspd`, `flux`, `cVars`). `std::array` containers use a **plural** quantity name regardless of element type: `<X>` becomes `<Xs>` in the variable name.

### Qualifier

Qualifiers go before the world-direction index: `<quantity>_<qualifier>_wcomp<value>`.

| Qualifier | Meaning |
|---|---|
| `ave` | averaged value |
| `T`, `B`, `L`, `R` | sides (top, bottom, left, right) |
| `RT`, `LT`, `RB`, `LB` | corners (right-top, left-top, right-bottom, left-bottom) |
| `star`, `dstar` | intermediate Riemann fan states |
| `iquad0`, `iquad1`, ... `iquad3` | quadrant value (iquad == value) |
| `_p`, `_m` | plus/minus state |
| `old`, `new` | time-level label |

### World-direction index

`wcomp0` is the face-normal direction; `wcomp1 = (wcomp0+1)%3`, `wcomp2 = (wcomp0+2)%3`. Established at the top of any direction loop:

```cpp
for (int wcomp0 = 0; wcomp0 < AMREX_SPACEDIM; ++wcomp0) {
    const int wcomp1 = (wcomp0 + 1) % 3;
    const int wcomp2 = (wcomp0 + 2) % 3;
    ...
}
```

Per-direction quantities follow `<quantity>_wcomp<value>`; centering and qualifier rules apply unchanged.

### Index suffixes

Secondary indices come after the world-direction index; they are slot values from a container, not qualifiers.

| Index | Meaning |
|---|---|
| `_lo`, `_hi` | bounding edge position |

| `_m`/`_p` used as | Meaning | Position |
|---|---|---|
| qualifier | Riemann state or directional sign | before world-direction index |
| secondary index | container slot value | after world-direction index |

---

## Array field comments

### `// indexing:` comment

Add an `// indexing:` comment at each `std::array` field declaration to describe what each slot represents:

```
// indexing: field[<N>: <description>]
```

### Dual-purpose containers

When a container's slot index equals the stored field component, state both roles explicitly:

```
// indexing: <field>[<N>: <index-role> = <component-role>]
```

---

## GPU lambda capture

- Never declare local copies of Array4 variables inside a `[=]` lambda body to re-alias outer variables. Capture by value directly; the outer name is available inside the lambda.
- Never capture raw host pointers inside `AMREX_GPU_DEVICE` lambdas.
