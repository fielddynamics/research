# Lean audit: gp1-half-section-balance-plane

| | |
|---|---|
| **File** | [`lean/HalfSection.lean`](lean/HalfSection.lean) |
| **Imports** | `Mathlib` (v4.36.0, the same version as the root `proofs/` chain) |
| **Theorems** | 9 |
| **Axioms** | every `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound` (some fewer); no `sorry` |
| **CI** | [`.github/workflows/lean-great-pyramid-gp1.yml`](../../../../../.github/workflows/lean-great-pyramid-gp1.yml): builds, then fails on any warning, error, `sorry` or non-standard axiom |

## Statements formalised

| README | Lean | Statement |
|---|---|---|
| Theorem 3 | `share_strictAntiOn` | `u ↦ (1-u)^n` is strictly decreasing on `[0,1]` (`n ≠ 0`) |
| Theorem 3 | `balance_unique` | at most one level in `[0,1]` has `(1-u)^n = 1/2` |
| Theorem 3 | `balance_level_rpow` | `(1-u)^n = 1/2` at `u = 1 - (1/2)^(1/n)`, every `n ≠ 0` |
| Theorem 3 | `balance_level_mem` | that level lies in `[0,1]` |
| Theorem 3 (D = 3) | `balance_level_D3` | on `[0,1]`: `(1-u)^2 = 1/2 ↔ u = 1 - 1/√2` |
| Theorem 4 | `halvings_coincide_iff` | horizontal (`(1-u)^m`) and meridional (`(1-u)^2`) halvings share a level iff `m = 2` (D = 3) |
| Theorem 5 | `canonical_levels_ordered` | volume level < area level < height level |
| Theorem 5 | `volume_above_area_plane` | volume fraction above the area plane is `(1/√2)^3 = √2/4 < 1/2` |
| Proposition 6 | `labelling` | `f_B = 13 + 8μ_B` reads 21, 17, 13 (a labelling) |

## Checked by script, not formalised

- Theorem 1 (measure scaling of homothetic sections) and Theorem 2 (divergence theorem / face-by-face flux): script, exact rational polygons.
- Observation 7 (Petrie comparison): script; it is an observation, not a theorem.

A Lean proof can be wrong only in its statements; a referee should check the statements above against the README, not the proofs.
