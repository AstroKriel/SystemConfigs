# Quokka: MHD Naming Conventions

Naming and comment conventions for `mhd_system.hpp` and adjacent MHD source files. These rules apply inside the `MHDSystem` class and any GPU device functions it calls.

---

## Comment style

- Prose is lowercase throughout.
- Acronyms stay uppercase: EMF, HLL, LLF, MHD, PPM.
- Paper citations are proper nouns using the shorthand tag: `Balsara25a`, `Felker18a`, `LD2004`.
- Function-header comments use the form: `// <description>; <CitationTag> (<Author(s)> <year>, <Journal> <vol>).`

---

## Array4 variables

Prefix pattern: `[centering_]a4_<quantity>[_w<n>]`

| Segment | Rule |
|---|---|
| Centering | `cc_` cell-centred, `fc_` face-centred, `ec_` edge-centred. Omit when centering is a function parameter and varies at the call site. |
| `a4_` | Always present; marks an `amrex::Array4` type. |
| Quantity | Lowercase physics name: `b`, `u`, `emf`, `fspd`, `flux`. |
| `_w<n>` | Required when the array lives on a specific face or edge direction. `n` is 0, 1, or 2. |

Examples: `fc_a4_b_wcomp0`, `a4_emf_wcomp2_ave`, `cc_a4_cVars`.

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

Rule: `<quantity>_w<n>[_<qualifier>]`

- Always place an underscore between the quantity name and its index.
- Prefix the index with `w` when it is a world-direction index (0=x, 1=y, 2=z).
- Other index types use their own qualifier without `w`: `_iquad0`–`_iquad3` for quadrant (first array index, quadrant type), `_lo`/`_hi` for bounding edge position, `_m`/`_p` for minus/plus face side.

| Name | Meaning |
|---|---|
| `b_wcomp0`, `b_wcomp1`, `b_wcomp2` | b-field component in world direction n |
| `u_wcomp0`, `u_wcomp1` | velocity component in world direction n |
| `j_wcomp1`, `j_wcomp2` | current density component in world direction n |
| `b_wcomp0_T`, `b_wcomp0_B` | b_wcomp0 at top/bottom edge position |
| `b_wcomp1_L`, `b_wcomp1_R` | b_wcomp1 at left/right edge position |
| `emf_wcomp2_iquad0` | emf_wcomp2 at quadrant 0 (iquad == 0) |
| `eta_j_wcomp1_lo`, `eta_j_wcomp1_hi` | resistive EMF (eta*j) in wcomp1 direction at lo/hi bounding edge |
| `eta_wcomp1_lo` | resistivity scalar at the wcomp1-edge lo position |
| `ave_b_wcomp1_lo` | average of b_wcomp1 at the lo bounding edge |

---

## Plural arrays of Array4

When a variable is a `std::array` of `amrex::Array4` (one per quadrant or per edge side), attach the plural `s` directly to the quantity name, before the direction qualifier:

```
bs_wcomp0, bs_wcomp1    // arrays of b-field Array4 views
us_wcomp0, us_wcomp1    // arrays of velocity Array4 views
emfs_wcomp2         // array of EMF Array4 views
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

When a specific slot value is known, the variable name in the quantity name becomes `[letter][value]`:

```
b_icomp     // abstract: icomp is the loop variable
b_i0        // concrete: first component (icomp == 0)
b_wcomp0        // concrete: world direction 0 (wcomp == 0)
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

`icomp`, `ieside`, `iquad`, `jeside`, `jquad`, `wcomp`, `idx0`, `idx1`, `qi`, `wcomp0`, `wcomp1`, `wcomp2`

The underscore rule applies only to multi-concept physics names where `_w<n>` or other qualifiers are needed to distinguish quantity from direction.

---

## GPU lambda capture

- Never declare local copies of Array4 variables inside a `[=]` lambda body to re-alias outer variables. Capture by value directly; the outer name is available inside the lambda.
- Never capture raw host pointers inside `AMREX_GPU_DEVICE` lambdas.
