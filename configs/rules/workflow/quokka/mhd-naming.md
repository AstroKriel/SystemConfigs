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

Examples: `fc_a4_b_w0`, `a4_emf_w2_ave`, `cc_a4_cVars`.

---

## World-direction index convention

The loop variable `w0` is the face-normal direction. `w1 = (w0+1)%3`, `w2 = (w0+2)%3`. This is established at the top of any direction loop:

```cpp
for (int w0 = 0; w0 < AMREX_SPACEDIM; ++w0) {
    const int w1 = (w0 + 1) % 3;
    const int w2 = (w0 + 2) % 3;
    ...
}
```

---

## Scalar field variable naming

Rule: `<quantity>_w<n>[_<qualifier>]`

- Always place an underscore between the quantity name and its index.
- Prefix the index with `w` when it is a world-direction index (0=x, 1=y, 2=z).
- Other index types use their own qualifier without `w`: `_q0`–`_q3` for quadrant, `_lo`/`_hi` for bounding edge position, `_m`/`_p` for minus/plus face side.

| Name | Meaning |
|---|---|
| `b_w0`, `b_w1`, `b_w2` | b-field component in world direction n |
| `u_w0`, `u_w1` | velocity component in world direction n |
| `j_w1`, `j_w2` | current density component in world direction n |
| `b_w0_T`, `b_w0_B` | b_w0 at top/bottom edge position |
| `b_w1_L`, `b_w1_R` | b_w1 at left/right edge position |
| `emf_w2_q0` | emf_w2 at quadrant 0 |
| `eta_j_w1_lo`, `eta_j_w1_hi` | resistive EMF (eta*j) in w1 direction at lo/hi bounding edge |
| `eta_w1_lo` | resistivity scalar at the w1-edge lo position |
| `ave_b_w1_lo` | average of b_w1 at the lo bounding edge |

---

## Plural arrays of Array4

When a variable is a `std::array` of `amrex::Array4` (one per quadrant or per edge side), attach the plural `s` directly to the quantity name, before the direction qualifier:

```
bs_w0, bs_w1    // arrays of b-field Array4 views
us_w0, us_w1    // arrays of velocity Array4 views
emfs_w2         // array of EMF Array4 views
```

---

## Direction arrays and scalars

| Name | Type | Meaning |
|---|---|---|
| `delta_w0`, `delta_w1`, `delta_w2` | `std::array<int,3>` | Unit stencil step in the w0/w1/w2 direction |
| `dx_w0`, `dx_w1`, `dx_w2` | `amrex::Real` | Cell size in the w0/w1/w2 direction |

---

## Index letter convention

Use the following letters consistently for loop variables and slot indices:

| Letter | Meaning | Examples |
|---|---|---|
| `i` | first (or only) array index; no world-direction meaning | `icomp`, `ieside`, `iquad` |
| `j` | second array index in a two-indexed array; distinguishes from `i` | `jquad`, `jeside` |
| `w` | world-direction index; array slot and world direction differ | `w0`, `w1`, `w2` |
| `x` | index where array slot and world direction are the same value | `x0`, `x1`, `x2`, `fc_a4_bx`, `fcx_mf_*` |

When a loop iterates over all three world directions and the loop variable doubles as both array index and world direction, use `x0`/`x1`/`x2` (parallel to the `w0`/`w1`/`w2` face-loop pattern):

```cpp
for (int x0 = 0; x0 < 3; ++x0) {
    int const x1 = (x0 + 1) % 3;
    int const x2 = (x0 + 2) % 3;
    ...
}
```

---

## Short index variables

Short conventional index variables do not require underscore separators:

`icomp`, `ieside`, `iquad`, `jeside`, `jquad`, `idx0`, `idx1`, `qi`, `x0`, `x1`, `x2`

The underscore rule applies only to multi-concept physics names where `_w<n>` or other qualifiers are needed to distinguish quantity from direction.

---

## GPU lambda capture

- Never declare local copies of Array4 variables inside a `[=]` lambda body to re-alias outer variables. Capture by value directly; the outer name is available inside the lambda.
- Never capture raw host pointers inside `AMREX_GPU_DEVICE` lambdas.
