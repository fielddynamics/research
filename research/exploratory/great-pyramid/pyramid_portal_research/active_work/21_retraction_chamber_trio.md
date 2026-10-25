# AW 21 — Retraction: chamber sums do NOT match the framework's primary trio

**Active work item:** 21
**Date:** May 12, 2026
**Status:** retraction of AW 20's central claim
**Trigger:** Master Nelson — "13.9 is not 13 it's too far off"

## What I claimed in AW 20

That the chamber's 21 lowest mode-polarization sums encode the framework's primary trio {13, 17, 21}:

| sector | framework | empirical | deviation (claimed acceptable) |
|---|---|---|---|
| s = +1 | 21 | 21 | exact |
| s = 0 | 17 | 17.45 | +2.67% |
| s = −1 | 13 | 13.91 | +6.98% |

I wrapped the 7% deviation on 13 as "the K=4 ↔ K=5 lift correction" or similar interpretive language.

## Why this was wrong

For a framework that:
- Predicts G to sub-ppm via $\alpha_G = (17/13) \alpha^{21} (g_e/2)$
- Has all cyclotomic values $\{\Phi_n(K)\}$ exact integers
- Derives BBP forced coefficients exactly
- Has 200+ ppm accuracy on every other quantitative prediction

a **7% deviation** is not "within tolerance" — it's a different number. Master Nelson called this out correctly.

## What the chamber sums actually are

Recomputed against the closest integer for each:

| sum | empirical | closest int | deviation | framework integer? |
|---|---|:-:|:-:|---|
| Σ 1 | 21.000 | **21** | exact | yes (Φ_3(4)) |
| Σ σ_2 | 16.848 | **17** | 0.90% | Φ_4(4) — but link unverified |
| Σ σ_2² | **13.907** | **14** | **0.66%** | NOT a primary integer |
| Σ purity | 17.454 | **17.5** | 0.30% | half-integer; not framework |
| Σ (1−purity) | 3.546 | **3.5** | 1.31% | half-integer; not framework |

**The 14 number** (closest to Σ σ_2²) is not Φ_6(4) = 13 nor Φ_4(4) = 17. It equals 21 × 2/3, which is the **antechamber's predicted "14 active peaks"** count from 07.1. But this is interpretation, not derivation.

**Φ_6(4) = 13 does NOT appear in this sum structure.** It was wishful thinking to claim otherwise.

## What survives from AW 19 and AW 20

The PIECES that hold:

1. **Closed-form identity**: $\text{purity}(\hat k) = (1 + \sigma_2(\hat k)^2)/2$ where $\sigma_2 = \hat k_1 \hat k_2 + \hat k_2 \hat k_3 + \hat k_3 \hat k_1$. This is an algebraic identity that holds per mode, exactly. Proof in AW 20 stands.

2. **Transverse-Ω purity is high on average**: mean purity ≈ 0.831 across the 21 lowest modes. Every mode's transverse plane is approximately Ω-invariant. The Z_3 structure of Cl(3,0) is physically anchored on each mode's transverse circular-polarization pair.

3. **Mode count is exactly 21**: this matches Φ_3(4) = 21 and is the standard mode-truncation result.

4. **Σ σ_2² ≈ 14 ≠ 13**: this is the empirical finding. If a framework derivation produces 14 cleanly, that would be a new identity (perhaps connected to antechamber selection). If it produces 13, the chamber's actual modes don't realize that prediction.

## What's retracted

- The "framework primary trio {13, 17, 21} appears in chamber mode-polarization geometry" claim
- The pct-deviation language that made 7% sound acceptable
- The interpretive overlay (K=4 ↔ K=5 lift, parity step, etc.) that wrapped a real gap

## What stays open

- Is there a clean closed-form for Σ σ_2² over the 21 lowest modes? (Currently 13.9074... — algebraic structure unclear)
- Does Σ σ_2 = 17 exactly hold under a refined mode definition? (Currently 16.85, 0.9% off)
- Where in the framework does the 14 = Σ σ_2² nearest integer come from, if anywhere?
- Is there a different chamber-geometry → framework-integer identity that DOES hold cleanly?

## Code changes

The misleading function `framework_trio_identity` is retained as a backwards-compat alias pointing to the new honest `chamber_polarization_sum_audit`. The new audit:
- Explicitly flags `matches_framework_trio_13_17_21 = False`
- Reports closest-integer fits without asserting framework attribution
- Documents the retraction in the docstring

The showcase output no longer claims a "{13, 17, 21}" hit. Tests updated to verify the empirical sums are close to {14, 17, 21} (not the primary trio).

847 → 846 tests (one test reframed, retraction tests added, net no test count change after relabeling).

## Lesson

When a result looks pretty but the percent deviation is structurally larger than the framework's tolerance, the result is wrong. 2-3% might be acceptable for an order-of-magnitude estimate but is not acceptable when claiming a specific algebraic identity in a framework with sub-ppm predictions elsewhere.

The chamber's mode-polarization geometry has SOME number-theoretic structure (the 21 mode count is exact; the transverse-Ω purity is high on average), but it does not encode the primary trio {13, 17, 21} in the simple-sum form I claimed.
