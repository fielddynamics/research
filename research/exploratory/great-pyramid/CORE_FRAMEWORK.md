# The Great Pyramid Programme: Core Framework

*What is proved, what is inherited, what is observed and what is hypothesis, in one dependency structure · Gravity Field Dynamics (GFD) · Exploratory research programme · 27 November 2026*

---

## Purpose

The Great Pyramid folder holds a large exploratory programme: about 120 notes, 1,210 passing regression tests and a Stargate hypothesis. This document picks out the part of it that is solid and arranges it as a framework with explicit layers. Each statement sits in one of four layers, and each layer may use only the layers below it. Five new proofs ([`proofs/`](proofs/), 191 checks) supply the load-bearing theorems that were previously missing, stated only in a special case, or stated without their converse.

| Layer | Content | Tag |
|---|---|---|
| **0. Inherited** | Results proved elsewhere in the repository and used here unchanged | [T], [T+L], [D] as tagged at source |
| **1. Core theorems** | GP-1 to GP-5: geometry, flux, integers, phases, transfer | [T] |
| **2. Observations** | Survey-based comparisons with the monument | [O] |
| **3. Hypotheses** | Sector readings, resonator, address, portal | [E] |

A layer-3 claim may be motivated by layers 0–2, but it is never promoted by them. Tags follow llms.txt, Rule 11.

---

## Layer 0 — Inherited from the GFD repository

| Result | Source | Tag | Used in |
|---|---|---|---|
| The tetrad equation has two roots (TetA, TetB), forming the stellated octahedron with the Field Origin at its centre | `proofs/tetrad-scheme-two-bounded-regions/`, `proofs/half-space-two-bounded-regions/` | [T+L] | vocabulary |
| $2(D+1) = 2^D \Rightarrow D = 3$, $K = 4$ | `proofs/hadamard-cube-frame/` | [T+L] | GP-1 (why $D = 3$ matters), GP-3 |
| Coupling polynomial $f(K,s) = 1 + sK + K^2$; $(13, 17, 21)$ at $s = (-1, 0, +1)$ | llms.txt §3–4 | [D] | GP-3 |
| Graded traces of $\mathbf 1\oplus V\oplus V^{\otimes2}$ give $f(K,s)$; the 21 invariant contrasts | `proofs/recursive-field-closure-response/` (Thm 7) | [T+L] (finite) | GP-3 Thm 6 |
| Constitutive law $\mu(x) = x/(x+1)$ | `proofs/constitutive-law-tug-of-war/`, `proofs/constitutive-law-exchange-symmetry/` | [T+L] | GP-2 Thm 8 |
| **Net-field rule**: drainless systems are pure TetA, $\mu = 1$, bare $G$ | `proofs/net-field-rule/`, `proofs/sst-mountain-scale/` | [T+L] | GP-2 Thm 8 |
| Field equation $\nabla\cdot[\mu\nabla\Phi] = 4\pi G\rho$, i.e. the conserved current $\mathbf J = \mu\nabla\Phi/4\pi G$ | `proofs/sst-quasi-static-limit/`; note 01.7 Prop. 1 | [T] | GP-1, GP-2 (divergence-free fields) |

---

## Layer 1 — Core theorems (this folder)

### Geometry and flux: where the balance plane is, and what it is

**GP-1 · Half-section theorem** ([proof](proofs/gp1-half-section-balance-plane/)).

- In any cone ($D \ge 2$, any base, any apex offset), a uniform current with $J_z \ne 0$ has $\mu_B(u) = (1-u)^{D-1}$.
- The balance level $u^* = 1 - 2^{-1/(D-1)}$ is unique.
- In $D = 3$ it is $1 - 1/\sqrt2$. This is the **only** dimension in which it coincides with the halving of the meridional area, which is Petrie's "halving of the vertical area".
- Halving the volume gives $1 - 2^{-1/3}$, and halving the height gives $1/2$. These are separate, distinguishable planes.

**GP-2 · Robustness and constitutive status** ([proof](proofs/gp2-balance-plane-robustness/)).

- **Affine background.** $\mu_B = (1-u)^2(1+bu)$ exactly, where $b$ is the fractional change of $J_z$ from the base centroid to the apex.
- **Uniqueness.** The level is unique for every $b > -1$.
- **Shift.** $du^*/db = (\sqrt2-1)/4$.
- **Any non-uniformity.** A non-uniformity of size $\varepsilon$ confines the level to $\pm\varepsilon h/(2\sqrt2)$, and the bound is sharp.
- **Gravity at Giza.** The Earth's gravity moves the level by 0.70 mm. With the pyramid's self-gravity, the total is under 0.36 in.
- **Structural share ≠ constitutive share.** At Giza the constitutive share is $\mu = 1$ exactly (net-field rule), while $\mu_B$ covers $[0,1]$ inside the stone. So $\mu_B$ is not the TetA/TetB partition of gravity.

Together, GP-1 and GP-2 make the balance plane a **theorem of geometry with a computed error budget**. They also say exactly what it is *not*.

### Integers: why 13, 17, 21, and why the hinge

**GP-3 · Signatures and hinge** ([proof](proofs/gp3-coupling-signatures-and-hinge/)).

- **Forced.** $f(K,s)$ is an irreducible integer norm form $|K + e^{i\theta}|^2$ of a root of unity iff $s \in \{-1,0,1\}$. So the three structural states are the only three; this is the converse of the cyclotomic identities in notes 01.1 and AW-05.
- **Unique hinge.** The **only** equalities between levels are the hinges $f(k,+1) = f(k+1,-1)$, and 17 belongs to $K = 4$ alone; this is the converse of note 01.4.
- **Coprime and fused.** The three values are pairwise coprime at every $K$, and they fuse along the tower $f(K^{2^n},1) = f(K,1)\prod_j f(K^{2^j},-1)$.
- **Geometry.** Exact enumeration identifies 13, 21, 17 and 273 as $|PG(2,3)|$, $|PG(2,4)|$, the ovoid of $PG(3,4)$, and $|PG(2,16)|$.

### Phases: what an address can and cannot be

**GP-4 · Registration and coherence** ([proof](proofs/gp4-registration-and-coherence/)).

- **Registration does not imply coherence.** Registration $C_N = 1$ means support on one $N$-gon coset, and it allows any coherence $C_1$.
- **Coherence forces registration.** $1 - \operatorname{Re}(e^{-iN\varphi}m_N) \le N^2(1-C_1)$, and the constant $N^2$ is sharp.
- **Stage-wise registration is coherence.** Registration at coprime orders (3 and 7) forces full coherence. So $\mathbb Z_3\times\mathbb Z_7\cong\mathbb Z_{21}$ does **not** factor the registration condition.
- **Exact selection needs all 21 characters.** Only the full character sum selects exactly. Every proper filter has sidelobes of at least $\sqrt{(N/|S|-1)/(N-1)}$, and the 14-character filter's are exactly ½.

### Transfer: the burden of proof for any remote claim

**GP-5 · Two-site transfer bound** ([proof](proofs/gp5-two-site-transfer-bound/)).

- **Coupling budget.** For any drive, $|c_y(t)| \le \sin\min(\int_0^t|\kappa|, \pi/2)$, attained at resonance.
- **No coupling, no transfer.** With $\kappa = 0$ there is no transfer under any frequency programme. Complete transfer needs $t \ge \pi/(2\sup|\kappa|)$.
- **Preregistration rule.** The detuning tolerance is $|\Delta| \le 2|\kappa|\sqrt{(1-\eta)/\eta}$.
- **The selector cannot add a channel.** The Gram mismatch $d_G$ is a pseudometric, and the mirror selector $M_{xy}\in[0,1]$ can only reduce the usable coupling.

### Dependency structure

```
 Layer 0 (repo)                         Layer 1 (this folder)
 ─────────────────────────────────────  ───────────────────────────────────────────
 D = 3 (Hadamard cube frame) ─────────► GP-1  half-section theorem ──┐
 conserved current J (SST limit) ─────► GP-1, GP-2                   ├─► balance plane: exact,
 net-field rule (μ = 1 locally) ──────► GP-2  robustness + status ───┘    budgeted, and not μ(x)
 f(K,s), graded traces (Proof 26) ────► GP-3  signatures, hinge ─────────► 13/17/21 forced; 21 the
                                                                          unique link between levels
                                        GP-4  registration/coherence ────► address = Z_21 registration,
                                                                          not Z_3 × Z_7 stages
                                        GP-5  transfer bound ────────────► every portal claim reduces
                                                                          to measuring ∫|κ| dt
```

GP-4 and GP-5 use no GFD premise at all. They are the mathematics that any sector, address or resonator model in Layer 3 must obey.

---

## Layer 2 — Observations [O]

| Observation | Value | Status after Layer 1 |
|---|---|---|
| King's Chamber floor against the area-balance level | +0.80 in, 0.30 σ (GP-1 O7) | Stands. It discriminates the area measure from the volume measure (186 σ) and the height measure (443 σ). Under a stated uniform-placement null, the chance of landing within 1 σ of one of the three canonical planes is < 0.6%. |
| Size of the residual against the field budget | 0.80 in against a gravitational budget of < 0.36 in (GP-2 T7) | The residual is survey-limited (height ±2.05 in). It cannot measure a field non-uniformity. |
| Coffer volume ratio near $1/\alpha$ | 137.17 or 140.2, depending on the height convention | Unchanged. It is a convention-sensitive correspondence (README §6). Nothing in Layer 1 supports or weakens it. |
| Relieving-chamber volumes $\propto 5\alpha V_{KC}$ | failed by ~×10 | Retained as a failed prediction. |
| Chamber polarisation sums 13/17/21 | retracted (AW-21) | Retained as a retraction. |

---

## Layer 3 — Hypotheses [E], restated against Layer 1

| Hypothesis | What Layer 1 now requires of it |
|---|---|
| **H-A. The balance plane is a TetA/TetB interface ("local Field Origin").** | It cannot be the gravitational partition: by GP-2 T8, $\mu = 1$ at Giza. It must be stated for a *named non-gravitational driven field* (EM, acoustic), with its own sector identification, and tagged [E]. Per the naming rules, the $\mu_B = \tfrac12$ level is the analogue of $\sigma = 0$ (the ring), not of the Field Origin. Any use of "Field Origin" for it must say so. |
| **H-B. The chamber operates at the neutral signature 17.** | The integer 17 is forced and unique (GP-3), but GP-1 P6 is a labelling. A physical observable that reads 17 at the plane must be specified and measured. |
| **H-C. An interlevel hinge $K = 4 \to 5$ at 21.** | GP-3 proves it is the **only** possible such link, which sharpens the hypothesis. A Hamiltonian, an energy scale and a transition rate are still needed. |
| **H-D. A 21-sector phase architecture (3 grooves × 7 corbel courses).** | It must say whether it requires $C_{21} = 1$ (registration, possibly incoherent) or stage-wise $C_3 = C_7 = 1$, which is full coherence by GP-4 T4. A 14-active-mode filter cannot be an exact address selector (GP-4 T5). |
| **H-E. Mirror-matched remote coupling (Stargate).** | By GP-5, transfer is bounded by $\int|\kappa|$ for every drive, and matching can only reduce $\kappa$. The only evidence that counts is a measured $\kappa_0 \neq 0$ after conventional channels are excluded, with the peak width fixed in advance by P4. A covariant, causal theory of $\kappa$ is required before any distance-independent claim. |

---

## Corrections to the existing notes

These follow from Layer 1 and the repository's own naming rules. The notes themselves are left unchanged, and the corrections are recorded here.

1. **01.6 §1 and AW-05 §4** call the $\mu_B = \tfrac12$ level, or $x = 1$, "the Field Origin". llms.txt says $\sigma = 0$ is the ring $x = 1$, not the Field Origin, and it reserves $s$ for the discrete label. Read "local Field Origin" in those notes as "balance plane, $\sigma_B = 0$". The identification is [E].
2. **01.7 §8, A3** says that "axial ↔ TetA, lateral ↔ TetB" is "part of GFD itself". For gravity this contradicts the net-field rule (GP-2 T8). It is a hypothesis about a driven field.
3. **01.7 §7** gives the shift numerically (599 in per unit gradient). The exact value is $\frac{\sqrt2-1}{4}h = 598.1$ in, with second coefficient $1 - 11\sqrt2/16$ (GP-2 T4).
4. **01.7 §7** says the field must be uniform to 0.1%. In fact the residual does not constrain the field at all: the survey uncertainty (±2.05 in) is larger than the residual, and the gravitational budget is < 0.36 in (GP-2 T5–T7). Once the survey reaches sub-inch precision, a residual $\delta$ attributed to the field says two things. For an affine driven field it fixes $b = 4\delta/((\sqrt2-1)h)$ (GP-2 T4). For an arbitrary field, Theorem 5 gives the minimum non-uniformity needed to produce it, $\varepsilon \ge 2\sqrt2\,|\delta|/h$.
5. **README §6** reads $\mathbb Z_3\times\mathbb Z_7\cong\mathbb Z_{21}$ as a phase architecture. The group identity is exact, but the registration conditions do not factor (GP-4 T4).
6. **`field_origin_geometry/` tests** import a package `gravity_field_model` that is not in the repository, so they cannot be collected. This is pre-existing. The 1,210 tests in `pyramid_portal_research/python/tests` pass once `scipy` is installed.

---

## Open problems, in priority order

1. **A named driven field.** Specify the non-gravitational field whose flux partition H-A refers to, and compute its $b$ or $\varepsilon$ in the real geometry, including chambers and shafts. GP-2 Theorems 2 and 5 then give the plane's position with an error bar.
2. **Sub-inch survey.** The 0.80 in residual is survey-limited. A laser survey of the floor and of the casing-reconstructed height turns GP-1 O7 into a test of the area measure at the 0.1 in level.
3. **An observable for 17.** H-B needs a measurable quantity that equals the neutral signature at the plane, beyond the labelling of GP-1 P6.
4. **A hinge Hamiltonian.** GP-3 makes the $K = 4\to5$ hinge the unique candidate. The next step is an operator with a physical scale.
5. **A coupling measurement.** GP-5 reduces every remote claim to $\int|\kappa|$. The laboratory test is two characterised resonators, with $\kappa_0$ bounded from above by experiment.
6. **Lean.** GP-1 T1–T5, GP-2 T2–T4 and GP-3 T2–T4 are finite algebra and could be formalised in the style of the main `proofs/` chain.

---

## Reproduction

```bash
cd research/exploratory/great-pyramid/proofs
python run_all.py                      # 191 checks, ~45 s (sympy, mpmath, numpy, scipy)

cd ../pyramid_portal_research
python -m pytest python/tests -q       # 1210 regression tests of the existing programme
```

*Scope: the five proofs are mathematics with stated premises. The observations are comparisons with a 19th-century survey. The hypotheses are hypotheses. The framework's purpose is to keep the three apart.*
