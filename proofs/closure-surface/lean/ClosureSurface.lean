import MountainScale

/-!
# Where Closure Sits: the Field's Stagnation Surface and the Jacobi Surface

Every field object closes, locally, at every level (the mountain-scale proof). In the frame turning
with a bound object's orbit, its own field, the host's tide `T = 4Ω² − κ²` and the vertical
restoring term combine into `Φ_eff = −GM/r − ½ T x² + ½ ν² z²`.

* `stagnation_radius`: on the host's radius the combined field vanishes exactly at `r³ = GM/T`,
  the Jacobi radius;
* `critical_level`: the level through those stagnation points is `E_c = −(3/2) GM/r_J`;
* `coriolis_no_work`: the Coriolis force does no work, so the Jacobi energy is conserved;
* `trapped`: with kinetic energy non-negative, an orbit with `E_J < E_c` keeps `Φ_eff < E_c`, so it
  never reaches the stagnation level: the trapping surface is the field's own surface;
* `orbit_extent`: along the orbit the surface reaches `2/3` of `r_J`;
* `held_for_good`: a Kepler orbit is held when `a < r_J/3` (the outer Oort cloud scale);
* `binary_edge`: a pair is one cell when `v² < (GM/s)(2 − 3s/r_J)`.
-/

namespace ClosureSurface

/-- On the host's radius the combined field `T r − GM/r²` vanishes exactly at `r³ = GM/T`. -/
theorem stagnation_radius (GM T r : ℝ) (hT : 0 < T) (hr : 0 < r) :
    T * r - GM / r ^ 2 = 0 ↔ r ^ 3 = GM / T := by
  have hr2 : r ^ 2 ≠ 0 := by positivity
  constructor
  · intro h
    have : T * r = GM / r ^ 2 := by linarith
    field_simp at this ⊢
    nlinarith [this]
  · intro h
    have hGM : GM = T * r ^ 3 := by field_simp at h; linarith
    rw [hGM]; field_simp; ring

/-- The level through the stagnation points: with `GM = T r³`, `−GM/r − ½ T r² = −(3/2) GM/r`. -/
theorem critical_level (GM T r : ℝ) (hr : 0 < r) (hJ : GM = T * r ^ 3) :
    -GM / r - T * r ^ 2 / 2 = -(3 / 2) * GM / r := by
  have hr0 : r ≠ 0 := hr.ne'
  rw [hJ]; field_simp; ring

/-- The Coriolis force does no work. With the frame turning at `Ω` about `z`, the Coriolis
acceleration is `(2Ω v_y, −2Ω v_x, 0)`, and its rate of work `v ⬝ a` is zero. -/
theorem coriolis_no_work (Ω vx vy vz : ℝ) :
    vx * (2 * Ω * vy) + vy * (-2 * Ω * vx) + vz * 0 = 0 := by
  ring

/-- Trapping. With `E = ½ k + P`, `k ≥ 0` (twice the kinetic energy) and `E < E_c`, the potential
stays below the stagnation level, `P < E_c`: the orbit never reaches the field's surface. -/
theorem trapped (E k P Ec : ℝ) (hE : E = k / 2 + P) (hk : 0 ≤ k) (hlt : E < Ec) : P < Ec := by
  linarith

/-- Along the orbit (the y axis) `Φ_eff = −GM/y`; it reaches the stagnation level at `y = 2/3 r_J`. -/
theorem orbit_extent (GM rJ : ℝ) (hGM : 0 < GM) (hr : 0 < rJ) :
    -GM / (2 / 3 * rJ) = -(3 / 2) * GM / rJ := by
  have hr0 : rJ ≠ 0 := hr.ne'
  field_simp

/-- A Kepler orbit of semi-major axis `a` (energy `−GM/2a`) is held for good when `a < r_J/3`. -/
theorem held_for_good (GM a rJ : ℝ) (hGM : 0 < GM) (ha : 0 < a) (hr : 0 < rJ) :
    -GM / (2 * a) < -(3 / 2) * GM / rJ ↔ a < rJ / 3 := by
  rw [div_lt_div_iff₀ (by positivity) hr]
  constructor <;> intro h <;> nlinarith

/-- A pair with separation `s` and relative speed `v` is one cell when its energy is below the
stagnation level: `v²/2 − GM/s < −(3/2) GM/r_J ↔ v² < (GM/s)(2 − 3s/r_J)`. -/
theorem binary_edge (GM s rJ v : ℝ) (hs : 0 < s) (hr : 0 < rJ) :
    v ^ 2 / 2 - GM / s < -(3 / 2) * GM / rJ ↔ v ^ 2 < GM / s * (2 - 3 * s / rJ) := by
  have hs0 : s ≠ 0 := hs.ne'
  have hr0 : rJ ≠ 0 := hr.ne'
  have key : GM / s * (2 - 3 * s / rJ) = 2 * (GM / s) - 3 * GM / rJ := by field_simp
  rw [key]
  constructor
  · intro h
    have : v ^ 2 / 2 - GM / s < -(3 / 2) * GM / rJ := h
    have e1 : -(3 / 2) * GM / rJ = -(3 / 2) * (GM / rJ) := by ring
    have e2 : 3 * GM / rJ = 3 * (GM / rJ) := by ring
    rw [e1] at this; rw [e2]; linarith
  · intro h
    have e1 : -(3 / 2) * GM / rJ = -(3 / 2) * (GM / rJ) := by ring
    have e2 : 3 * GM / rJ = 3 * (GM / rJ) := by ring
    rw [e2] at h; rw [e1]; linarith

end ClosureSurface

#print axioms ClosureSurface.stagnation_radius
#print axioms ClosureSurface.critical_level
#print axioms ClosureSurface.coriolis_no_work
#print axioms ClosureSurface.trapped
#print axioms ClosureSurface.orbit_extent
#print axioms ClosureSurface.held_for_good
#print axioms ClosureSurface.binary_edge
