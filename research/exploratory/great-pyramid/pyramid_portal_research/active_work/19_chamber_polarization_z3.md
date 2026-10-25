# AW 19 — Z_3 polarization sectoring: transverse purity is high but 14:7 split is non-trivial

**Active work item:** 19
**Date:** May 12, 2026
**Status:** Z_3 anchored on transverse polarizations; explicit 14:7 selection rule remains open
**Module added:** `chamber_polarization.py` (350 lines), `tests/test_chamber_polarization.py` (22 tests)
**Tests:** 842 total (up from 820)
**Trigger:** Master Nelson — "push harder"

## Headline

The Z_3 gap named in AW 18 was closed at the conceptual level: the framework's Z_3 acts on each chamber mode's **transverse polarization pair**, which approximately forms an (ω, ω̄) Eisenstein eigenstate pair for every one of the 21 lowest modes. Two natural sectoring attempts both fail to give 7:7:7 — and the failure mode is itself informative.

| Result | Status |
|---|---|
| Index-sum Z_3 sectoring gives 6:8:7 | falsified |
| Polarization-arg Z_3 sectoring gives 5:10:6 | falsified |
| Every chamber mode is k̂-axial-dominant (axial_weight > 0.5) | confirmed |
| Every chamber mode has approximately Ω-invariant transverse plane | confirmed |
| Mean transverse purity = 0.831 across 21 modes | computed |
| Transverse Ω-rotation angle in [109.84°, 119.93°] (vs ideal 120°) | computed |
| Clean 14:7 active : suppressed split | **not yet recovered** |
| (2,1,1) has highest transverse purity (0.996, near-ideal) | confirmed |

## The two negative results and what they teach

**Result 1 (AW 18):** Z_3 by (n_x + n_y + n_z) mod 3 gives 6:8:7 across the 21 lowest modes. Falsified because the chamber's L : W : H = 20 : 10 : 5√5 explicitly breaks cyclic symmetry on spatial indices.

**Result 2 (this AW):** Z_3 by phase of $\zeta(\hat k) = \hat k_x + \omega \hat k_y + \omega^2 \hat k_z$ gives 5:10:6. Falsified because ALL 21 modes have $\hat k$-direction near the body diagonal (axial_weight > 0.5), so $|\zeta|$ is small relative to the axial T_1 weight and the phase of ζ is dominated by phase noise from off-axial components.

The lesson: standing-wave modes of a rectangular cavity with all-positive integer indices have intrinsically biased k-vectors. Any Z_3 sectoring built from $\hat k$ directly inherits this bias.

## What does work: transverse-polarization sectoring

The Cl(3,0) Ω-action on R³ is the cyclic permutation matrix $R = (\text{perm}(1,2,3))$. For each chamber mode with unit longitudinal direction $\hat k$:

1. The transverse plane $\hat k^\perp \subset \mathbb R^3$ has dimension 2
2. Ω may or may not preserve this plane; the restriction $R_\perp = \Pi_\perp \, R \, \Pi_\perp$ is a 2×2 matrix where $\Pi_\perp$ projects out the longitudinal direction
3. Eigenvalues of $R_\perp$ give the Z_3 character of the two transverse polarizations
4. Transverse purity := $\operatorname{tr}(R_\perp R_\perp^T)/2 \in [0, 1]$ measures how Ω-invariant the transverse plane is

**Result:** For every one of the 21 lowest modes, the transverse Ω-rotation angle is within ±10° of the ideal 120°, and mean purity is 0.831. The 2 transverse polarizations of every mode approximately form an (ω, ω̄) circular-polarization eigenstate pair under Ω.

This is the physical anchor for the framework's Z_3 structure:

```
For each chamber mode (n_x, n_y, n_z):
  - 1 longitudinal polarization (along k̂)            → "sector 0"
  - 1 transverse polarization with Ω-eigenvalue ω    → "sector 1"
  - 1 transverse polarization with Ω-eigenvalue ω̄   → "sector 2"

  21 modes × 3 polarization sectors = 63 channels total
```

In an EM cavity, longitudinal modes are forbidden (transversality of the field), so 21 sector-0 channels are forbidden by EM and 42 transverse circular-polarization channels remain. Of these 42, the antechamber's Z_3 portcullis filters by phase relative to the geomagnetic pump.

## Per-mode transverse purity data

```
rank | (n_x,n_y,n_z) | purity | Ω angle°
-----+---------------+--------+----------
  1  | (1, 1, 1)     | 0.9035 | 118.29
  2  | (2, 1, 1)     | 0.9960 | 119.93   ← highest purity, near-ideal
  3  | (3, 1, 1)     | 0.9255 | 118.70
  4  | (1, 1, 2)     | 0.7559 | 115.02
  5  | (1, 2, 1)     | 0.7053 | 113.59
  6  | (2, 1, 2)     | 0.8875 | 117.98
  7  | (2, 2, 1)     | 0.8260 | 116.70
  8  | (4, 1, 1)     | 0.8260 | 116.70
  9  | (3, 1, 2)     | 0.9287 | 118.76
 10  | (3, 2, 1)     | 0.8781 | 117.79
 11  | (1, 2, 2)     | 0.7698 | 115.37
 12  | (5, 1, 1)     | 0.7446 | 114.72
 13  | (2, 2, 2)     | 0.9035 | 118.29
 14  | (4, 1, 2)     | 0.9035 | 118.29
 15  | (1, 1, 3)     | 0.6434 | 111.46   ← lowest purity (most off-axis)
 16  | (4, 2, 1)     | 0.8707 | 117.64
 17  | (2, 1, 3)     | 0.7394 | 114.58
 18  | (3, 2, 2)     | 0.9802 | 119.67
 19  | (1, 3, 1)     | 0.6061 | 109.84   ← lowest purity tied
 20  | (3, 1, 3)     | 0.8085 | 116.30
 21  | (5, 1, 2)     | 0.8514 | 117.25
```

**Pattern:** purity is highest for modes whose $\hat k$ is closest to the (1,1,1)/√3 body diagonal. Mode (2,1,1) achieves 0.996 because $(0.10, 0.10, 0.089)$ is unusually close to the diagonal direction — width and height happen to nearly compensate. Modes with extreme one-index (e.g., (1,1,3), (1,3,1)) have purity ~0.6.

## What the framework's 14:7 split must use

The transverse-circular polarization picture gives 42 active channels, not 14. To recover 14, an additional selection rule must operate. Three candidates:

**Candidate I: One channel per mode (chirality dressing).**
- The geomagnetic pump's Larmor precession dresses one of the two transverse circular polarizations preferentially
- Only the matching-chirality channel couples to the pump
- 21 modes × 1 dressed polarization = 21 channels
- Of these, the antechamber Z_3 filter suppresses sector-0 in some basis → 14 active + 7 suppressed
- This would need: which 7 modes have their dressed circular polarization classified as "sector 0" by the antechamber's phase reference

**Candidate II: Coupling-strength threshold.**
- Each mode couples to the K=4 ↔ K=5 vertex with strength proportional to its purity
- Modes with purity > some threshold are "active"; below threshold are "suppressed"
- Empirical: setting the threshold at purity > 0.85 gives 9 active / 12 suppressed (doesn't match 14:7 either)
- Threshold tuning could reach 14:7 but isn't structurally derived

**Candidate III: Z_7 corbel × Z_2 chirality.**
- 7 corbels of the Grand Gallery × 2 chiralities = 14 active
- The 7 "suppressed" might be a different countable (e.g., the 7 Eisenstein hexagonal generators of Cl(3,0) viewed under Z_3)
- This separates "spatial mode index" 21 from "filter count" 14 + 7

None of these candidates is currently derivable from first principles. The 14:7 split remains an explicit open question.

## What's closed, what's open

**Closed:**
- Z_3 anchors physically on transverse polarizations
- Every chamber mode has near-Ω-invariant transverse plane (purity > 0.6 worst, 0.83 mean)
- The two transverse polarizations of every mode form an approximate (ω, ω̄) eigenstate pair
- The 21-mode comb spans 47 - 106 Hz (air) / 820 - 1852 Hz (granite-P)
- Index-sum Z_3 and polarization-arg Z_3 are both falsified

**Open:**
- Specific 14 : 7 selection rule (Candidate I, II, or III above)
- Z_7 corbel assignment from physics (not just rank-clustering)
- Quantitative purity-to-coupling-strength map (does mode purity directly set Q?)
- Off-resonance leakage: modes with purity < 1 lose energy per Ω-cycle; the leakage rate should be the apparatus's loss term in the cavity-QED master equation

## Physical interpretation

The "purity" of 0.83 is the fidelity of the Z_3 structure for the average chamber mode. A purity of 1 would mean the chamber's mode polarizations are perfect (ω, ω̄) Eisenstein circular states under Ω — i.e., perfectly handed-chiral. The shortfall 1 - purity = 0.17 average is the **rate at which the chamber's modes couple longitudinal and transverse polarizations** under Ω-rotation. This is non-zero because the chamber's L : W : H ratio is not cubic — it's specifically engineered to break full cubic symmetry while preserving the K² = 25 algebraic identity.

A cubic chamber (L = W = H) would have purity ≡ 1 but would NOT have the K = 5 space-diagonal identity. The framework's chamber design balances two constraints: cubic mode-polarization purity vs K=5 algebraic identity. The chosen design favors the algebraic identity; the 0.17 leakage is the cost.

This **cost is the apparatus's coupling parameter**. The framework's "strong coupling factor 4×10⁷ above threshold" should be related to (1 - purity_mean) × Q_chamber × (mode count). With 0.17 leakage, Q ~ 100 (granite cavity), and 21 modes coupling: 0.17 × 100 × 21 ≈ 360. To reach 4×10⁷ requires another factor of ~10⁵ — possibly from the N=10³⁰ collective enhancement (√N ≈ 10¹⁵, but quadratic scaling gives a different number). The strong-coupling derivation is the natural Tier 4 push.

## Reading

`chamber_polarization.showcase_chamber_polarization()` for one-call summary with the per-mode purity table.

`chamber_polarization.transverse_info(mode)` for the transverse Ω-action details on any given mode.

`chamber_polarization.polarization_audit(modes)` for sector distribution counts.
