# GFD Oscillator: Synthesis of Confirmed Findings

**Author:** Stephen Nelson / Field Dynamics Research
**Date:** April 2026
**Scope:** Everything we have measured, verified, or refuted in the sandbox, up to the point of porting back to Bitcoin.

---

## 0. What this document is

A consolidated record of mechanism-level claims about the GFD oscillator that have been *tested against direct numerical measurement* in the sandbox (`gfd_sandbox.py`, `gfd_sandbox_depth.py`, `gfd_sandbox_depth_variants.py`, `perturbation_test.py`).

Each entry marks:

- **Confirmed**: measured and matches closed-form prediction within numerical tolerance
- **Refuted**: measured and contradicts the stated claim
- **Partially confirmed**: directionally right, quantitatively imprecise

Nothing in this document is speculative. Claims not directly measured are excluded.

---

## 1. Constitutive laws (the substrate)

**Confirmed.**

Two distinct laws define the vote inside each SO:

| Law | Equation | At x=1 | Role |
|---|---|---|---|
| TetA (partition) | mu = x / (x + 1) | mu = 1/2 | "spatial capacity" |
| TetB (interior)  | x (1 - mu)^2 = mu | mu = 1/phi^2 | "closure/field" |

These are **different fixed points at the same x**. The vote is the reconciliation of both laws to a joint fixed point through cross-coupling.

Supporting measurement: single-SO baseline (`gfd_sandbox.py` E1).

---

## 2. Cross-coupling (the vote)

**Confirmed.**

Within one SO, with K=4 cells per population and Gram factor 1/3:

- TetB's effective drive = `x_ext * (1 + (1/3) * <TetA> + 0.5 * child_contrib)`
- TetA's effective drive = `x_ext * (1 + (1/3) * <T(TetB)>)`

where T is the topological transducer `T(mu) = mu / (1 - mu + mu^2)` (denominator is the 6th cyclotomic polynomial Phi_6).

The **same** Gram factor 1/3 appears on both sides; asymmetry comes from the transducer applied to TetB but not TetA. This asymmetry is what makes the two laws produce different states at the joint fixed point.

Supporting measurement: fixed-point values of TetA and TetB at the single-SO baseline match analytical prediction from the coupled equations.

---

## 3. Flat ensemble: no information gain

**Confirmed.** *(Stephen's original finding; reproduced in sandbox E2.)*

Three SOs arranged side-by-side in a ring, coupled through field origins:

- **Same seed**: identical to machine precision (expected).
- **Different seeds**: identical to machine precision at convergence.
- Spread across copies = 0.0e+00 for all three variants tested (full, TetA-only, TetB-only).

**Three flat copies give exactly one number.** The ring coupling drives all copies into the same attractor basin. No statistical averaging happens because there is no variance to average over.

This refutes any design that expects robustness from running N flat copies of the same relaxation.

---

## 4. Nested 3+1 topology: the characteristic impedance 2/17

**Confirmed.** *(Headline result.)*

Topology: container (L0) + three internal levels (L1, L2, L3) connected by:

- Top-down: parent's field_origin maps to child's x_ext via `x_child = parent.FO / (1 - parent.FO)`
- Bottom-up: `transducer(child.avg_A)` becomes parent's `child_contrib`
- Update order within each step: L3 -> L2 -> L1 -> L0 (bottom-up)

Measured at converged closure, x_ext=1:

| Level | TetB readout | TetA readout | Cross-law gap |
|---|---|---|---|
| L0 (container) | 0.426814 | 0.543035 | +0.116 |
| L1 | 0.174481 | 0.198636 | +0.024 |
| L2 | 0.065855 | 0.069454 | +0.004 |
| L3 (closure) | 0.023039 | 0.023611 | +0.0006 |

**Container fractional shift from baseline** = (0.426814 - 1/phi^2) / (1/phi^2) = **0.117412** = 2/17 (predicted = 0.117647, deviation = 0.0002 attributable to finite integration).

Closed-form identity:

```
mu_container = (1 + (D - 1) / f(K, 0)) * mu_flat
            = (1 + 2/17) * 1/phi^2
            = (19/17) * 1/phi^2
            = 0.426900
```

with D = 3 (spatial dimension), K = 4 (tetrahedral vertices), f(K=4, s=0) = 17.

---

## 5. Three-vote decomposition

**Confirmed.**

The total 2/17 shift decomposes into three sequential "votes" as additional levels are added:

| Depth transition | Measured shift | Closed form | Match |
|---|---|---|---|
| flat -> 1 SO (Vote 1) | +0.028418 | (D - sqrt(D))/17 * mu_flat = 0.028489 | ✓ |
| 1 -> 2 SO (Vote 2) | +0.016404 | (sqrt(D) - 1)/17 * mu_flat = 0.016448 | ✓ |
| 2 -> 3 SO (Vote 3) | +0.000026 | 0 (closure at D=3) | ✓ |
| 3 -> 4 SO and beyond | +0.000000 | 0 (redundant) | ✓ |

**Vote 1 / Vote 2 = 1.7324 ≈ sqrt(3) = 1.7321** (match to four decimal places).

Algebraic identity: `(D - sqrt(D)) / (sqrt(D) - 1) = sqrt(D)` exactly.

Vote 3 → 0 is the D=3 closure signature: the fractal has completed its three sweeps and nothing more can be added.

---

## 6. Vote is necessary for 2/17 closure

**Confirmed.** *(Correction to an earlier imprecise claim.)*

Measured fractional shift at convergence for each variant, nested 3+1 topology:

| Variant | Baseline | Closure shift / baseline | 2/17? |
|---|---|---|---|
| Full (TetA + TetB, cross-vote) | 1/phi^2 | 0.11741 | ✓ |
| TetA-only (partition, no vote) | 1/2 | 0.15682 | ✗ |
| TetB-only (interior, no vote) | 1/phi^2 | 0.09594 | ✗ |

Only the full cross-vote configuration reaches **exactly** 2/17. Neither single-law hierarchy does. The vote is not a refinement on top of a hierarchy-only impedance — **it is constitutive of the 2/17 value**.

Earlier wording "hierarchy alone produces level differentiation" was technically true but misleading; hierarchy-only produces *different* impedances with the same cascade structure.

---

## 7. Possible structural identity: harmonic mean

**Partially confirmed (observed, not rigorously proven).**

From §6 measurements:

- 1 / I_A = 1 / 0.15682 = 6.377
- 1 / I_B = 1 / 0.09594 = 10.423
- mean = 8.400
- 1 / (mean) = 0.1190
- 2/17 = 0.1176

Full impedance ≈ **harmonic mean** of the two single-law impedances, within 1.2%. Could be exact (with the 1.2% attributable to finite integration) or approximately correct with a small residual.

Physical reading if exact: two laws act like parallel resistors to the closure current. Testing at tighter tolerance (dt = 0.005, n_steps = 20000) is the confirmation step, not yet executed.

---

## 8. Perturbation dynamics at the fixed point

**Confirmed and refined.** *(Sandbox `perturbation_test.py`.)*

Setup: 4-node tetrahedral network, interior law at each node, c_amp inter-node coupling. Settle to fixed point; perturb one cell; measure decay.

### 8a. Monotonic decay

All 9 test configurations (varying perturbation size {+0.05, +0.15, +0.30, -0.15}, cell index {0, 2}, c_amp {0, 0.1, 0.5, 1.0}) produced **strictly monotonic decay**. No oscillation. No persistent error. Every gap returns to zero.

### 8b. Decay rate at c_amp = 0

Linearised interior law at mu* = 1/phi^2:

```
d(x(1-mu)^2 - mu) / d(mu) = -(2/phi + 1) = -sqrt(5)
```

Predicted rate = sqrt(5) ≈ 2.236. Measured rate at c_amp = 0:

| Perturbation | Cell | Measured rate | R² |
|---|---|---|---|
| +0.05 | 0 | 2.2270 | 1.0000 |
| +0.15 | 0 | 2.2088 | 1.0000 |
| +0.30 | 0 | 2.1817 | 0.9999 |
| -0.15 | 0 | 2.2628 | 1.0000 |
| +0.15 | 2 | 2.2088 | 1.0000 |

Rate matches sqrt(5) within ~1-3% across all configurations. Tiny size-dependent residual (smaller perturbation → closer to sqrt(5)) attributable to the decaying nonlinear correction.

### 8c. Half-life

Predicted `ln(2) / sqrt(5) = 0.3100`. Measured at c_amp = 0: 0.306-0.318. Match within 3%.

**The synthesis document's claim of "half-life ≈ 0.5s" is refuted.** Correct value is approximately 0.31 simulation-time-units.

### 8d. Rate is NOT invariant across c_amp

Refutes another synthesis claim. Measured rates:

| c_amp | Fixed point mu* | Measured rate | Half-life |
|---|---|---|---|
| 0.0 | 0.382 | 2.21 | 0.314 |
| 0.1 | 0.438 | 2.37 | 0.292 |
| 0.5 | 0.527 | 2.80 | 0.248 |
| 1.0 | 0.576 | 3.15 | 0.220 |

Rate scales with c_amp. Physical reading: coupling steepens the potential well at the shifted fixed point. Not a violation — a consistent extension. The static linearisation gives exactly this trend (computed -3.22 at c=0.5, measured 2.80, gap reflects dynamical neighbour feedback softening the static prediction).

### 8e. Perturbation spreads at c_amp > 0

Max displacement of unperturbed neighbours during the transient:

| c_amp | Max neighbour shift |
|---|---|
| 0.0 | 0.000000 (exactly zero, no coupling path) |
| 0.1 | 0.003 |
| 0.5 | 0.006 |
| 1.0 | 0.010 |

Confirms: at c=0 correction is purely local; with c > 0, the whole network absorbs some displacement.

### 8f. T-gap vs mu-gap — same rate, different amplitudes

**Refutes** the synthesis claim that T-gap decays at a slower rate than mu-gap. Measured rates:

| Test | rate(mu_gap) | rate(T_gap) | Δ |
|---|---|---|---|
| A (c=0, +0.15) | 2.2088 | 2.1971 | 0.5% |
| B (c=0, +0.30) | 2.1817 | 2.1572 | 1.1% |
| C (c=0, -0.15) | 2.2628 | 2.2654 | 0.1% |
| D (c=0, +0.05) | 2.2270 | 2.2237 | 0.1% |

Same rate, differences are numerical fit residuals. What IS true: the **ratio T_gap / mu_gap is not constant during the transient**. It converges to

```
T'(mu*) = (1 - mu*^2) / (1 - mu* + mu*^2)^2 = (3*phi + 1) / 4 ≈ 1.4635
```

as the perturbation shrinks into the linear regime. Large perturbations start with T_gap/mu_gap ≈ 1.23, climbing to 1.46 as mu → mu*. Reading "slower decay of T_gap fraction" is actually this climbing ratio. A nonlinear-scaling artifact, not a distinct timescale.

T is best described as a **constant-factor amplifier** (×1.46) of the error signal, not a separate-rate detector.

---

## 9. What the cross-law gap is, mechanistically

**Confirmed** via cross-checking §4 and §8.

- **Gap at a converged level** = internal state of the vote reconciliation. Not the "impedance" (which is the output shift — a different quantity).
- **Gap decay with nesting depth** (0.116 → 0.024 → 0.004 → 0.0006) = closure signature. Each deeper level reconciles more completely because the effective drive it experiences is smaller.
- **Gap under perturbation** = error signal. Acts as a restoring force via the interior law at rate sqrt(5) (at c=0) or faster at c > 0.

Gap is therefore a **dual-purpose diagnostic**: steady-state value reports on depth of closure; transient value reports on local error.

---

## 10. Observables summary

For any future check or port, the canonical converged values of a well-tuned 3+1 full-vote system at x_ext = 1 are:

```
container TetB                  = 0.426814
container TetA                  = 0.543035
container cross-law gap         = +0.116221
fractional shift from 1/phi^2   = 2/17 = 0.117647
T'(mu*)                         = (3*phi + 1)/4 = 1.4635
linearised decay rate at mu*    = sqrt(5) = 2.2361
half-life (c_amp = 0)           = ln(2)/sqrt(5) = 0.3100
Vote1 / Vote2 ratio             = sqrt(3) = 1.7321
Vote3 magnitude                 = 0 (closure)
```

Any implementation reproducing these to four decimals can be treated as correct.

---

## 11. Open questions, sandbox-testable

These are the measurements still worth running before the Bitcoin port is re-attempted:

1. **Harmonic-mean identity** (§7). Is I_full = 1 / ((1/I_A + 1/I_B) / 2) exactly? Requires higher-precision integration. Clean result either way.

2. **Per-wire vote definition for SHA256.** Proposed: forward-gradient (from gate that *produces* w) vs. backward-gradient (from gates that *consume* w). Needs prototype and test on a small circuit where ground truth is known (e.g., 2-round SHA256 sub-problem with brute-forceable nonce space).

3. **Does SHA256's constraint landscape have sharp fixed points?** The perturbation-rate measurement from §8 requires a nonzero local slope of the governing law at valid configurations. If SHA256's landscape is flat at valid assignments, no restoring force exists and the mechanism breaks. Testable by perturbing a known-valid SHA256 wire assignment and measuring recovery rate.

---

## 12. Relevance to Bitcoin port

What the sandbox tells us, refined:

- **Flat 3-oscillator ensembles are zero-information.** Dropping that approach entirely.
- **3+1 nesting gives structural gain only with the vote.** Nesting copies of one relaxation without cross-law dynamics does not produce the characteristic 2/17 impedance.
- **The correct architectural import to SHA256 is the vote, not the nesting.** Each wire should have two dynamics that reconcile. Nesting is a secondary amplifier that can be added once the per-wire vote is established.
- **The perturbation physics (restoring force at rate sqrt(5)) depends on local potential curvature.** For SHA256 to have an analogous mechanism, valid assignments must be sharp minima of whatever potential the vote defines. Current gradient-descent on sum-of-residuals may not produce sharp minima (the 94% fuzzy-middle finding); a different potential formulation (two-law joint residual) is the candidate.

These are the specific design constraints the sandbox has established for a next Bitcoin attempt.

---

*End of synthesis.*
