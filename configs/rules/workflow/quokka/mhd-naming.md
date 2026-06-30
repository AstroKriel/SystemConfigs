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
| (none) | `std::array` of `amrex::Array4`; plural Array4 containers omit the type marker |

### Quantity name

Lowercase physics name: `b`, `u`, `emf`, `fspd`, `flux`, `cVars`.

`std::array` containers use a **plural** quantity name regardless of element type.

| Variable | Plural quantity | Element type |
|---|---|---|
| `fcw_mf_us_wcomp` | `us` | `MultiFab` |
| `ec_mf_emfs_wcomp` | `emfs` | `MultiFab` |
| `fcw_fspds_wcomp` | `fspds` | `Array4` (no type marker) |
| `cc_fabs_us_wcomp` | `us` | `FArrayBox` |

`cVars` is already plural; do not add a second `s`.

### Qualifier

Qualifiers go **before** the world-direction index.

| Qualifier | Meaning | Example |
|---|---|---|
| `ave` | averaged value | `emf_ave_wcomp2`, `ec_a4_emf_ave_wcomp2` |
| `T`, `B`, `L`, `R`, `RT`, `LT`, `RB`, `LB` | edge position | `b_T_wcomp0`, `emf_RT_wcomp2` |
| `dstar`, `T_star`, `R_star`, `L_star`, `B_star` | paper-symbol intermediate (Balsara25a) | `emf_dstar_wcomp2` |
| `p`, `m` (on emf scalars) | plus/minus Riemann state | `emf_p_wcomp2`, `emf_m_wcomp1` |
| `old`, `new` | time-level label | `fc_mf_cVars_old_wcomp` |

### Secondary indices

Secondary indices come **after** the world-direction index. They are slot values that index into a container, not qualifiers.

| Index | Meaning | Example |
|---|---|---|
| `_iquad0` to `_iquad3` | quadrant slot (iquad == n) | `emf_iquad0_wcomp2` |
| `_lo`, `_hi` | bounding edge position | `eta_j_wcomp1_lo` |
| `_m`, `_p` (on b-field Array4s) | jeside slot (jeside == 0 or 1) | `fc_a4_b_wcomp0_m` |

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

Rule: `<quantity>[_<qualifier>]_w<n>`, then secondary indices after.

| Name | Meaning |
|---|---|
| `b_wcomp0`, `b_wcomp1`, `b_wcomp2` | b-field component in world direction n |
| `u_wcomp0`, `u_wcomp1` | velocity component in world direction n |
| `j_wcomp1`, `j_wcomp2` | current density component in world direction n |
| `b_T_wcomp0`, `b_B_wcomp0` | b-field at top/bottom edge position, world direction 0 |
| `b_L_wcomp1`, `b_R_wcomp1` | b-field at left/right edge position, world direction 1 |
| `emf_iquad0_wcomp2` | emf at quadrant 0 (iquad == 0), world direction 2 |
| `emf_p_wcomp2`, `emf_m_wcomp2` | emf at plus/minus Riemann state, world direction 2 |
| `emf_ave_wcomp2` | averaged emf, world direction 2 |
| `eta_j_wcomp1_lo`, `eta_j_wcomp1_hi` | resistive EMF (eta*j) in wcomp1 direction at lo/hi bounding edge |
| `eta_wcomp1_lo` | resistivity scalar at the wcomp1-edge lo position |
| `ave_b_wcomp1_lo` | average of b_wcomp1 at the lo bounding edge |

---

## Array field comments

### `// indexing:` comment

Add an `// indexing:` comment at each `std::array` field declaration to describe what each slot represents:

```
// indexing: <variable>[<N>: <description>]
```

Example:

```cpp
std::array<amrex::MultiFab, 3> fcw_mf_us_wcomp;  // indexing: field[3: fc-normal direction]
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

| Letter | Meaning | Full variable examples |
|---|---|---|
| `i` | first (or only) array index | `icomp`, `ieside`, `iquad` |
| `j` | second array index in a two-indexed array | `jquad`, `jeside` |
| `w` | world-direction index (0=x, 1=y, 2=z) | `wcomp`, `wcomp0`, `wcomp1`, `wcomp2` |

When embedded in a quantity name, the full index variable name replaces any fused shorthand:

| Old (fused) | Correct |
|---|---|
| `bi` | `b_icomp` |
| `ui` | `u_icomp` |
| `b_w` (no value) | `b_wcomp` |

When a specific slot value is known, the variable name becomes `[letter][value]`:

```
b_icomp     // abstract: icomp is the loop variable
b_i0        // concrete: first component (icomp == 0)
b_wcomp0    // concrete: world direction 0 (wcomp == 0)
```

World-direction loops always use the `wcomp0`/`wcomp1`/`wcomp2` pattern:

```cpp
for (int wcomp0 = 0; wcomp0 < AMREX_SPACEDIM; ++wcomp0) {
    const int wcomp1 = (wcomp0 + 1) % 3;
    const int wcomp2 = (wcomp0 + 2) % 3;
    ...
}
```

---

## Short index variables

Short index variables do not require underscore separators:

`icomp`, `ieside`, `iquad`, `jeside`, `jquad`, `wcomp`, `idx0`, `idx1`, `wcomp0`, `wcomp1`, `wcomp2`

The underscore rule applies only to multi-concept physics names where `_w<n>` or other qualifiers are needed to distinguish quantity from direction.

---

## GPU lambda capture

- Never declare local copies of Array4 variables inside a `[=]` lambda body to re-alias outer variables. Capture by value directly; the outer name is available inside the lambda.
- Never capture raw host pointers inside `AMREX_GPU_DEVICE` lambdas.
