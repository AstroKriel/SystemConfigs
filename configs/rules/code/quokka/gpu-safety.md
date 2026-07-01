# Quokka: GPU Safety

Conventions for writing GPU-safe code in quokka.

---

## GPU lambda capture

- Never declare local copies of Array4 variables inside a `[=]` lambda body to re-alias outer variables. Capture by value directly; the outer name is available inside the lambda.
- Never capture raw host pointers inside `AMREX_GPU_DEVICE` lambdas.
