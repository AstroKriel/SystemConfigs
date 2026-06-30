# Quokka: MHD Naming Conventions

Naming and comment conventions for `mhd_system.hpp` and adjacent MHD source files. These rules apply inside the `MHDSystem` class and any GPU device functions it calls.

---

## Comment style

- Prose is lowercase throughout.
- Acronyms stay uppercase: EMF, HLL, LLF, MHD, PPM.
- Paper citations are proper nouns using the shorthand tag: `Balsara25a`, `Felker18a`, `LD2004`.
- Function-header comments use the form: `// <description>; <CitationTag> (<Author(s)> <year>, <Journal> <vol>).`

---

## Naming pattern

All variables follow:

```
[centering]_[type]_<quantity>[_<qualifier>]_[<index>...]
```

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

`cVars` is already plural; do not add a second `s`.

### Qualifier

Qualifiers go **before** the world-direction index: `<quantity>_<qualifier>_wcomp<n>`.

| Qualifier | Meaning |
|---|---|
| `ave` | averaged value |
| `T`, `B`, `L`, `R`, `RT`, `LT`, `RB`, `LB` | edge position (top, bottom, left, right, and corners) |
| `dstar`, `T_star`, `R_star`, `L_star`, `B_star` | paper-symbol intermediate (Balsara25a) |
| `p`, `m` (on emf scalars) | plus/minus Riemann state |
| `old`, `new` | time-level label |

### Secondary indices

Secondary indices come **after** the world-direction index. They are slot values that index into a container, not qualifiers.

| Index | Meaning |
|---|---|
| `_iquad0` to `_iquad3` | quadrant slot (iquad == n) |
| `_lo`, `_hi` | bounding edge position |
| `_m`, `_p` (on b-field Array4s) | jeside slot (jeside == 0 or 1) |

The `_m`/`_p` suffix on **emf scalars** is a Riemann-state qualifier and goes before the world-direction index. On **b-field Array4s** extracted from a `jeside`-indexed container it is a slot value and goes after.

---

## World-direction index convention

The loop variable `wcomp0` is the face-normal direction. `wcomp1 = (wcomp0+1)%3`, `wcomp2 = (wcomp0+2)%3`. This is established at the top of any direction loop:

```cpp
for (int wcomp0 = 0; wcomp0 < AMREX_SPACEDIM; ++wcomp0) {
    const int wcomp1 = (wcomp0 + 1) % 3;
    const int wcomp2 = (wcomp0 + 2) % 3;
    ...
}
```

---

## Scalar field variable naming

Rule: `<quantity>[_<qualifier>]_wcomp<n>`, then secondary indices after.

| Pattern | Meaning |
|---|---|
| `<qty>_wcomp<n>` | scalar physics quantity in world direction n |
| `<qty>_<position>_wcomp<n>` | scalar at a named edge position |
| `<qty>_<symbol>_wcomp<n>` | paper-symbol intermediate value |
| `<qty>_iquad<k>_wcomp<n>` | scalar at quadrant k, world direction n |
| `<qty>_p_wcomp<n>`, `<qty>_m_wcomp<n>` | plus/minus Riemann state, world direction n |
| `<qty>_wcomp<n>_lo`, `<qty>_wcomp<n>_hi` | scalar at lo/hi bounding edge of wcomp<n> axis |

---

## Array field comments

### `// indexing:` comment

Add an `// indexing:` comment at each `std::array` field declaration to describe what each slot represents:

```
// indexing: field[<N>: <description>]
```

### Dual-purpose b-field containers

When a b-field container's slot index doubles as the stored field component (the fc-normal direction equals the component stored), say so explicitly:

```cpp
// indexing: field[3: fc-normal direction = field component]
```

---

## Direction arrays and scalars

| Name | Type | Meaning |
|---|---|---|
| `delta_wcomp0`, `delta_wcomp1`, `delta_wcomp2` | `std::array<int,3>` | Unit stencil step in the wcomp0/wcomp1/wcomp2 direction |
| `dx_wcomp0`, `dx_wcomp1`, `dx_wcomp2` | `amrex::Real` | Cell size in the wcomp0/wcomp1/wcomp2 direction |

---

## Index letter convention

Index variable names follow the pattern `[letter][what-it-indexes]`. The letter gives the index type; the suffix says what it ranges over. A bare letter without a suffix is not permitted.

| Letter | Meaning | Examples |
|---|---|---|
| `i` | first (or only) array index | `icomp`, `ieside`, `iquad` |
| `j` | second array index in a two-indexed array | `jquad`, `jeside` |
| `w` | world-direction index (0=x, 1=y, 2=z) | `wcomp`, `wcomp0`, `wcomp1`, `wcomp2` |

When a specific slot value is known, the variable name becomes `[letter][value]`:

```
<qty>_icomp     // abstract: icomp is the loop variable
<qty>_i0        // concrete: first component (icomp == 0)
<qty>_wcomp0    // concrete: world direction 0 (wcomp == 0)
```

---

## Short index variables

Short index variables do not require underscore separators:

`icomp`, `ieside`, `iquad`, `jeside`, `jquad`, `wcomp`, `idx0`, `idx1`, `wcomp0`, `wcomp1`, `wcomp2`

The underscore rule applies only to multi-concept physics names where `_wcomp<n>` or other qualifiers are needed to distinguish quantity from direction.

---

## GPU lambda capture

- Never declare local copies of Array4 variables inside a `[=]` lambda body to re-alias outer variables. Capture by value directly; the outer name is available inside the lambda.
- Never capture raw host pointers inside `AMREX_GPU_DEVICE` lambdas.
