# Plan: GFD with power output (throat) as a new mass-panel curve

## Goal

On the second chart (enclosed mass vs radius), add a new data series that shows how the **mismatch** between photometric mass and velocity-decoded mass can be attributed to vortex "power output" (throat/interior), so that:

- We quantify the mass that "isn't a match" exactly.
- We tie it to the power output that would need to be applied (or that is in the throat).
- We plot a curve (e.g. "GFD (with power output)") that demonstrates the match when this contribution is included.

---

## Step 1: Define the mismatch exactly

**Quantities we already have:**

- **M_dec(r)** = velocity-decoded enclosed mass [kg] on grid `r_decode` (from observed v only).
- **M_phot(r)** = photometric enclosed mass [kg] on grid `r_model` (from mass model).

**Mismatch:**

- Put both on a common radial grid (e.g. `r_common` = `r_decode`, or a fine grid from 0.1 to r_max).
- Interpolate so we have M_dec and M_phot on the same r.
- Define:
  - **Delta M(r) = M_phot(r) - M_dec(r)**  
  (Signed: positive when photometric > decoded, e.g. CamB.)

So we get a profile **Delta M(r)** [kg] (or in M_sun) that is the "mass that isn't a match" at each radius.

---

## Step 2: Relate mismatch to "power output" (vortex dynamics)

**Interpretation:** Delta M is the enclosed-mass difference between what we see (photometric) and what the rotation implies (decoded). In the hourglass picture, that difference can be attributed to the throat: structure that has been pulled in and still affects the field but doesn't show up in the kinematic decode of the visible rotation.

**Power output in vortex terms:**

- For circular rotation, the "power" that sustains speed v at radius r is related to the centripetal acceleration: g = v^2/r. The mass that would produce that in Newtonian gravity is M = g * r^2 / G. So the **power output** (effective mass contributing to the field at r) could be:
  - **Option A (minimal):** Throat contribution = Delta M(r). So "GFD (with power output)" = M_dec(r) + Delta M(r) = M_phot(r) by construction. The new curve is just the photometric mass, but labeled as "GFD (with power output)" to show that adding the throat closes the gap.
  - **Option B (explicit throat curve):** Plot Delta M(r) as a separate curve: "Throat / power output contribution" or "Delta M (phot - decoded)". Then "GFD (with power output)" = M_dec + Delta M = M_phot, so we add one line that is the sum and one that is the throat alone.
  - **Option C (vortex equation):** Use a vortex dynamics equation (e.g. circulation Gamma = 2*pi*r*v, or vorticity) to convert Delta M into an "effective power" profile. For example, if we define an effective acceleration from Delta M via g_throat = G * Delta M / r^2, then the extra velocity support from the throat is v_throat^2 = g_throat * r. So v_total^2 = v_dec^2 + v_throat^2 (Pythagorean, like CDM). Then we could back out an "effective M from power output" and plot that. This would require choosing a consistent vortex rule (e.g. additive in v^2 or in M).

**Recommendation for a first implementation:** Start with **Option B**: compute Delta M(r) on a common grid, plot it as "Throat contribution (photometric - decoded)", and add "GFD (with power output)" = M_dec + Delta M so the new line exactly matches M_phot and shows the reconciliation. No extra vortex equation yet. Once that is on the chart, we can replace the simple Delta M with a vortex-dynamics-derived profile if desired.

---

## Step 3: What to plot on the second chart

**Current curves (keep):**

- LambdaCDM (baryons + NFW)
- GFD (photometric)
- GFD velocity decoded

**New curve(s):**

1. **Throat / power output contribution:** Delta M(r) = M_phot(r) - M_dec(r) on a common r (e.g. r_decode). Plot as a distinct style (e.g. dash-dot, or different color) so it is clear this is the "missing" or "excess" mass that closes the gap.
2. **GFD (with power output):** M_dec(r) + Delta M(r) = M_phot(r) on the same grid. Plot so it overlays or nearly overlays the photometric curve, demonstrating that photometric = decoded + throat contribution.

So the second chart would show that **photometric = velocity decoded + throat (power output)**, and we see the throat contribution explicitly.

**Grid choice:** M_dec is on `r_decode` (starts at first observation). M_phot is on `r_model` (starts at 0.1 kpc). For Delta M we need both on the same r. Easiest: evaluate M_phot on `r_decode` via interpolation (we have M_phot on r_model, so interpolate M_phot(r_decode)). Then Delta M = M_phot_interp - M_dec on r_decode. "GFD (with power output)" = M_phot_interp (same as photometric but only on r_decode range). Alternatively use r_model and interpolate M_dec onto r_model; then Delta M and the new curve are on r_model. Either is fine; r_decode keeps the new curve in the observed range only.

---

## Step 4: Implementation outline

1. **Common grid:** Use `r_decode` so the new series is in the observation range. Compute `M_phot_on_decode = np.interp(r_decode, r_model, M / MSUN)` (in M_sun for plotting).
2. **Delta M:** `M_dec_Msun = M_dec / MSUN` already on r_decode. So `Delta_M_Msun = M_phot_on_decode - M_dec_Msun`. Clip or allow negative (for galaxies where decoded > photometric).
3. **GFD (with power output):** `M_with_power = M_dec_Msun + Delta_M_Msun = M_phot_on_decode` (on r_decode).
4. **Plot on ax2:**
   - Add: `ax2.semilogy(r_decode, Delta_M_Msun, ...)` labeled "Throat contribution (phot - decoded)" or "Power output (throat)".
   - Add: `ax2.semilogy(r_decode, M_with_power, ...)` labeled "GFD (with power output)".
5. **Optional:** Only show these curves when max(|Delta M|) is above a small threshold, so we don't clutter galaxies where phot and decoded already match.

---

## Step 5: Later refinement (vortex equation)

If we want to go from "Delta M = phot - decoded" to a vortex-dynamics-based "power output" profile:

- Introduce a relation between Delta M and an effective acceleration or circulation (e.g. g_throat = G * Delta M / r^2, or a vorticity integral).
- Compute an effective M_profile from that relation and plot it instead of (or in addition to) raw Delta M.
- Document the chosen vortex equation in the script and in the figure caption.

---

## Summary

| Item | Action |
|------|--------|
| Mismatch | Delta M(r) = M_phot(r) - M_dec(r) on common r (e.g. r_decode). |
| Power output | Initially: throat contribution = Delta M. Optionally later: vortex equation. |
| New curve 1 | Throat contribution: Delta M(r). |
| New curve 2 | GFD (with power output): M_dec + Delta M = M_phot. |
| Implementation | Interpolate M_phot onto r_decode; compute Delta M and M_with_power; add two semilogy lines in generate_fig2_galaxy.py. |

This gives a clear, quantitative picture: we can read off exactly how much mass "isn't a match" and show that adding it as the throat/power output reconciles photometric with the decoded curve.
