# Lean audit: Where Closure Sits

| | |
|---|---|
| **File** | [`lean/ClosureSurface.lean`](lean/ClosureSurface.lean) |
| **Imports** | `MountainScale` (and through it the khronon, net-field and constitutive-law formalisations, Mathlib v4.36.0) |
| **Theorems** | 7 |
| **Axioms** | All 7 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **CI** | [`.github/workflows/lean-closure-surface.yml`](../../.github/workflows/lean-closure-surface.yml) |

**Verdict.** The algebra of Theorems 1, 2 and 4 and of Proposition 6 is proved. The geometry (that the level set through the saddles bounds a region around the object), the orbit integrations, the vortex and the host-field expansion are checked by the script.

## Statements used by the paper

| Paper | Lean | Notes |
|---|---|---|
| Theorem 1 | `stagnation_radius` | `T > 0`, `r > 0`: `T r − GM/r² = 0 ↔ r³ = GM/T` |
| Theorem 1 | `critical_level` | `GM = T r³` ⇒ `−GM/r − ½ T r² = −(3/2) GM/r` |
| Theorem 2 | `coriolis_no_work` | the Coriolis acceleration `(2Ω v_y, −2Ω v_x, 0)` does no work |
| Theorem 2 | `trapped` | `E = k/2 + P`, `k ≥ 0`, `E < E_c` ⇒ `P < E_c` |
| Theorem 4 | `orbit_extent` | `−GM/((2/3) r_J) = −(3/2) GM/r_J` |
| Proposition 6 (b) | `held_for_good` | `−GM/2a < −(3/2) GM/r_J ↔ a < r_J/3` |
| Proposition 6 (d) | `binary_edge` | `v²/2 − GM/s < −(3/2) GM/r_J ↔ v² < (GM/s)(2 − 3s/r_J)` |

## Checked by script, not formalised

- The saddles' curvatures and that no other stagnation point exists: script A1–A2 (symbolic).
- Orbits below and above E_c: script B2–B3 (numerical).
- The vortex separatrix: script C1.
- The shape and volume: script D1–D2.
- T from the host's potential: script E1–E2 (symbolic).
