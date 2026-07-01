# Quokka: MHD Naming Conventions

Naming and comment conventions for `mhd_system.hpp` and adjacent MHD source files in `quokka`.

---

## Naming pattern

All variables follow the naming pattern:

```
[centering]_[type]_<quantity>_[index]
```

### Centering prefix

| Prefix | Meaning |
|---|---|
| `cc_` | cell-centred |
| `fc_` | face-centred |
| `ec_` | edge-centred |

> **Note:** `fcw_` holds a collection of 3x `fc` quantities, where entry `w` is `fc` in direction `w`.

### Type marker

| Marker | Type |
|---|---|
| `mf_` | `amrex::MultiFab` |
| `fabs_` | `amrex::FArrayBox` (locally extracted) |
| `a4_` | single `amrex::Array4` |

### Quantity name

A shorthand for the concept that the variable stores and which form it is in.

> **Note:** when a variable holds a collection of the same quantity, the name is pluralised: `<quantity>` becomes `<quantity>s`.

### Index

The index encodes what varies parametrically. A quantity with multiple components identifies each by tagging the variable name with `comp[value]`. Index components can also be chained to progressively add context.

#### Index prefixes

| Prefix | Meaning |
|---|---|
| `i`, `j` | local array index |
| `w` | world-direction index |

> **Note:** `i` and `j` distinguish levels in a nested collection: `i` for the outer dimension, `j` for the inner.

> **Note:** the solver permutes spatial indices at each step so the solving direction is always local index 0. `i`/`j` indices live in this permuted space; only `w` indices are anchored to global directions.

#### World-direction index

`wcomp0` is the face-normal direction; `wcomp1 = (wcomp0+1)%3` and `wcomp2 = (wcomp0+2)%3` complete the right-handed triple.

#### Positional and directional tags

| Tag | Meaning |
|---|---|
| `lo`, `hi` | low/high boundary |
| `m`, `p` | minus/plus direction |

---

## Array field comments

### Indexing comment

Add an `// indexing:` comment at each container field declaration to describe what each entry represents:

```
// indexing: <field>[<N>: <description>]
```

where `<N>` is the number of entries.

> **Note:** when a slot index equals the stored field component, state both roles explicitly: `<field>[<N>: <index-role> = <component-role>]`.

