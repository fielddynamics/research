# Particle and Element Properties from the Coupling Polynomial
## A Teaching Companion to the Enterprise Validation Suite

**Stephen Nelson, Field Dynamics, March 2026**

---

## What This Document Covers

The enterprise validation suite `gfd_particle_properties.py` runs 81 tests across 10 sections, covering particle masses, decay modes, photon structure, gauge groups, electroweak mixing, charge quantization, and nuclear binding. Every test derives from the coupling polynomial f(K,s) = 1 + Ks + K^2 at K = 4. Zero fitted parameters. 81 out of 81 pass.

This document teaches the physics behind each section in plain language. It explains what the tests measure, why they matter, and how they connect to each other. The document follows the same P1 through P10 structure as the test suite.

---

## The Inputs

The entire framework uses five structural constants derived from one equation:

```
2(D+1) = 2^D    has unique integer solution    K = 4, D = 3
```

From K = 4 and D = 3, the coupling polynomial f(K,s) = 1 + Ks + K^2 gives three values:

```
F+ = 21    (full coupling, s = +1)
F0 = 17    (gate threshold, s = 0)
F- = 13    (deep field, s = -1)
```

One measured input:

```
m_e = 0.51100 MeV    (electron mass: the energy of one complete 2pi closure revolution)
```

From which:

```
b   = m_e / (F0 - 1/2) = m_e / 16.5 = 0.03097 MeV    (gate coupling per TetA channel)
eps = 2 / F0 = 2/17                                     (gate loss per crossing)
```

Everything else follows.

---

## P1. Framework Identities (10 tests)

These tests verify that the polynomial, the gate depth distribution, and the Sierpinski structure are internally consistent. They are regression tests. If any fail, the framework is broken.

The gate depth distribution [27, 27, 9, 1] comes from the binomial expansion (3+1)^3 = 64. It counts how many of the 64 walk positions encounter the Sierpinski gate in 0, 1, 2, or 3 of the three closure cycles.

The key identity is the endpoint symmetry of the polynomial. When evaluated at s = +1 and s = -1, the propagation term Ks cancels:

```
F+ + F- = (1 + K + K^2) + (1 - K + K^2) = 2 + 2K^2 = 2*F0 = 34
```

This cancellation is central to everything that follows. It means the full 2pi closure revolution (s from -1 to +1 and back) sees twice the symmetric content (1 + K^2) and none of the propagation. The binding content per half-cycle is (F+ + F- - 1)/2 = 33/2 = 16.5, which is what gives us the gate coupling b = m_e / 16.5.

---

## P2. Fine Structure Constant (7 tests)

The inverse fine structure constant 1/alpha = 137.036 decomposes as:

```
1/alpha = 137 + 1/28
```

The integer 137 has two equivalent decompositions:

**EM sector reading:** 137 = F0 x 2^D + 1 = 17 x 8 + 1. This is the gate threshold (17 coupling channels) distributed across all 8 binary vertices of the state space, plus 1 for the field origin (the point s = 0 where the vortex throat sits).

**Nuclear sector reading:** 137 = 128 + 9 = K^3(K-2) + (2^D + 1). This is the total photon mode count in the full vortex (128) plus the closure positions at the throat (9).

These two decompositions are connected by the bridge identity:

```
VERTICES x INTERACTIONS = POSITIONS x POLARIZATIONS
      8   x     16      =     64    x      2
                128      =          128
```

The field origin (the "+1" in the EM reading) is the 9th closure position. The 8 binary vertices plus the origin give 9, which is exactly the gd=2 count in the gate depth distribution.

The fractional part 1/28 comes from the f-vector sum of the stellated octahedron: 8 vertices + 12 edges + 8 faces = 28 geometric elements. Each element contributes 1/28 of a coupling channel.

Result: 1/alpha = 137 + 1/28 = 137.03571 versus measured 137.03600. Accuracy: 2 parts per million.

---

## P3. Particle Masses (10 tests)

Every measured particle mass, from the proton through the eta meson, is an integer multiple of the electron mass. The integer is a mode count built from {K, D, F+, F0, F-}.

| Particle | Measured (MeV) | Mode Count | Expression | Match |
|----------|---------------|------------|------------|-------|
| Proton | 938.272 | 1836 | K x 9 x (F++F0+F-) | 0.008% |
| Neutron | 939.565 | 1836 + 42b/m_e | m_p + 2F+ x b | 0.008% |
| Charged pion | 139.570 | 273 | F+ x F- | 0.05% |
| Neutral pion | 134.977 | 264 | K x (F++F--1) x (K-2) | 0.05% |
| Muon | 105.658 | 207 | 3 x F0 x K + D | 0.11% |
| Tau | 1776.86 | 3477 | (F++F0+F-) x K x F0 + 9 | 0.007% |
| Kaon | 493.677 | 966 | (F++F0+F-) x (F+-2) - D | 0.011% |
| Eta | 547.862 | 1072 | K^2 x (51 + K^2) | 0.013% |

The proton mass has the cleanest structure: 1836 = 36 x 51. The factor 36 = K x 9 counts the host's energy-carrying positions (27 at gd=0 plus 9 at gd=2). The factor 51 = F+ + F0 + F- is the total coupling content of the polynomial evaluated at all three structural states. The proton's mass is its structural positions times its total coupling content, each at energy m_e.

The charged-minus-neutral pion mass difference is exactly 9 m_e, the closure position count. The charge costs exactly 9 closure modes.

---

## P4. Decay Mode Conservation (7 tests)

If particles are structural projections rather than independent objects, their decay must conserve the total mode count (the integer multiple of m_e). Every decay tested conserves modes exactly.

**Neutron decay:** n(1839) = p(1836) + e(1) + nu(2 kinetic modes). The 3 excess modes (1839 - 1836 = D = 3) are spatial modes that leak through the gate.

**Charged pion decay:** pi+(273) = mu(207) + nu_mu(66). The neutrino carries 66 = (K-2) x (2F0-1) = 2 x 33 modes. This is two polarizations times the binding content per half-cycle.

**Neutral pion decay:** pi0(264) = gamma(132) + gamma(132). Each photon gets exactly K x (2F0-1) = 4 x 33 = 132 modes. The neutral pion splits into two equal photon packets.

**Full pion chain:** pi+(273) decays to mu(207) which decays to e(1). The total neutrino radiation across both decays is 273 - 1 = 272 = K^2 x F0 = 16 x 17 modes. This is face positions times gate threshold.

---

## P5. Stability and Closure (8 tests)

Why is the proton stable? Why does the neutron decay? Why is the pion short-lived? The answer is structural closure.

**Complete closure = stable.** The proton's mode count 1836 = 36 x 51 factors into two structural integers. Both factors (host positions and polynomial content) are clean framework numbers. The proton achieves complete closure: every position carries the full polynomial content. There is no incomplete mode. Nothing needs to leak.

**Incomplete closure = unstable.** The neutron's mode count 1839 = 3 x 613. The factor 613 is prime. It has no structural factorization. The D = 3 excess modes have no home in the closure structure. They must leak through the gate. The leakage takes 878 seconds (the neutron lifetime).

**Product vs sum.** The pion's mass 273 = F+ x F- is a product of polynomial endpoints. A product couples two states across the vortex but does not unify them into one closure cycle. The pion is structurally a bridge between TetA (F+) and TetB (F-). Bridges are transient. They must hand off their modes to something that can close.

**The fermion/boson distinction follows from this.** Fermions (proton, neutron, electron, muon) have mass formulas built from addition of polynomial values. They close. Bosons (pion, kaon, eta) have mass formulas built from multiplication of polynomial values. They couple but do not close. Sums are homes. Products are bridges.

The pion discriminant identity F+ x F- = F0^2 - K^2 = 289 - 16 = 273 is algebraically forced. The pion mass is the discriminant of the coupling polynomial. This is not a numerical coincidence. It is a structural identity of the trinomial 1 + Ks + K^2.

---

## P6. Photon Structure (10 tests)

Each subchannel has 4 positions: 3 active corners (D spatial directions) plus 1 gate (the removed Sierpinski center). A wave propagating through the subchannel uses 1 position for the longitudinal direction and 1 for the gate. The remaining K - 2 = 2 positions are transverse oscillation modes.

These 2 modes are the two polarizations of the photon.

The counting builds upward:

```
Subchannel:  K - 2 = 2 polarization states
Face:        K^2 x (K-2) = 16 x 2 = 32 photon states
Full vortex: K^3 x (K-2) = 64 x 2 = 128 = 2^7 total photon modes
TetA half:   128 / 2 = 64 = K^3 = walk shell capacity
```

The connection to electrons: each walk shell has K^3/2 = 32 independent photon mode pairs. This equals the electron capacity per period pair: s(2) + p(6) + d(10) + f(14) = 32. Each "electron" (gravity tile excitation) corresponds to one coupled photon pair.

The angular degeneracies (2l+1) for l = 0 through K-1 sum to K^2 = 16, which is the number of subchannel positions per face. The angular structure of the outward vortex maps exactly onto the subchannel geometry.

Through 7 periods, the total electron capacity is 2 + 8 + 8 + 18 + 18 + 32 + 32 = 118. This is why the periodic table has 118 elements.

---

## P7. Gauge Groups (6 tests)

The Standard Model gauge group SU(3) x SU(2) x U(1) emerges from the tetrahedron at three structural levels:

**Subchannel level: SU(3).** The 3 active corners of the subchannel triangle generate an SU(3) symmetry with (K-1)^2 - 1 = 8 generators. These are the 8 gluons. The 6 directed edges between corners (3 x 2 = 6) plus 2 traceless diagonal generators give 8. Colour confinement is the structural requirement that the Sierpinski triangle needs all 3 corners to exist. Remove one corner and the triangle collapses. This IS confinement.

**Face level: SU(2).** Each tetrahedral face has K-1 = 3 edges. These 3 edges generate an SU(2) symmetry: the W+, W-, and Z bosons. The face structure mediates the weak interaction.

**Whole tetrahedron level: U(1).** The overall phase of the tetrahedron is a single degree of freedom. This is the photon. U(1) has 1 generator.

Total: 8 + 3 + 1 = 12 = D x K. The number of gauge generators equals spatial dimensions times branching factor. This is the same 12 that appears as the pairing coefficient in the nuclear binding formula.

The A4 alternating group (rotation symmetry of the tetrahedron) has conjugacy classes of size {1, 3, 8}, which map directly onto the gauge boson content {U(1), SU(2), SU(3)}.

---

## P8. Electroweak Sector (5 tests)

The Weinberg angle sin^2(theta_W) measures how electromagnetic and weak forces mix. It appears at two scales in the framework:

**UV (geometric scale):** sin^2(theta_W) = 1/K = 1/4 = 0.250. This comes from the V4 subgroup of A4. V4 has 4 elements: 1 identity (the photon) + 3 double transpositions (W+, W-, Z). The electromagnetic fraction is 1/4.

**IR (mass scale):** sin^2(theta_W) = 9/(9+27+D) = 9/39 = 0.2308. This comes from the gate depth distribution. The 9 closure positions (which carry the weak interaction through the throat) out of 39 total responsive positions (9 closure + 27 spatial + 3 propagation dimensions). Measured at M_Z: 0.2312. Match: 0.19%.

The RG running from 0.250 (UV) to 0.231 (IR) is a 7.7% shift, consistent with the Standard Model beta functions over the energy range from the geometric scale down to the Z mass.

The W/Z mass ratio follows: m_W/m_Z = sqrt(1 - 9/39) = sqrt(30/39) = 0.877, versus measured 0.881 (0.5% match).

Three particle generations correspond to D = 3 closure cycles. Each generation is the same tile excitation seen through progressively deeper closure: electron (1 mode, direct), muon (207 modes, gd=2 excitation), tau (3477 modes, full polynomial excitation). Deeper closure means more vortex structure is involved, which means more modes, which means heavier mass.

---

## P9. Charge Quantization (8 tests)

Electric charge is quantized in multiples of 1/D = 1/3 because there are D = 3 spatial faces on the tetrahedron.

In the subchannel triangle, the 3 active corners are the colour charges (red, green, blue). Quark charges come from how many corners a quark occupies:

```
Up quark:   2 of 3 corners = +2/3 e
Down quark: 1 of 3 corners, reversed = -1/3 e
Proton:     uud = +2/3 +2/3 -1/3 = +1 e
Neutron:    udd = +2/3 -1/3 -1/3 = 0
Electron:   full triangle, reversed = -3/3 = -1 e
```

The electron's charge is -1 because the gravity tile excitation covers all 3 subchannel corners in the direction opposite to the proton's outward vortex. It is a complete inward response to the outward electric field.

Colour confinement follows from the Sierpinski structure: the triangle requires all 3 corners to exist as a complete geometric object. A free quark (one isolated corner) would leave an incomplete triangle, which the Sierpinski hierarchy cannot sustain.

---

## P10. Nuclear Binding (10 tests)

The Bethe-Weizsacker semi-empirical mass formula has five coefficients. All five derive from the polynomial and the gate attenuation:

| Coefficient | BW Fitted | GFD Derived | Expression | Match |
|-------------|-----------|-------------|------------|-------|
| Volume | 15.56 | 15.588 | F+ x D/(D+K) x sqrt(D) | 0.18% |
| Surface | 17.23 | 17.235 | F0 x (1 + eps^2) | 0.03% |
| Coulomb | 0.697 | 0.720 | b x (F+ + F-/K - 1) | 3.3% |
| Asymmetry | 23.29 | 23.250 | F+ + F-/K - 1 | 0.17% |
| Pairing | 12 | 12 | D x K | exact |

The surface coefficient's gate correction eps^2 = (2/17)^2 is the second-order attenuation at the nuclear boundary. Surface nucleons sit at the codimension-1 boundary where one coupling dimension is truncated, exposing them to an additional gate crossing.

The nuclear radius parameter r0 = 1.2 fm derives as r0 = D/(D+K) x r_e = 3/7 x 2.818 fm = 1.208 fm, matching experiment to 0.6%.

The bridge identity connecting the EM and nuclear sectors:

```
F0 x 2^D + 1 = K^3 x (K-2) + 9 = 137
```

The field origin in the EM coupling formula IS the 9th closure position in the nuclear gate depth distribution. The number 2^D + 1 = 9 appears in both contexts because 9 = 8 binary vertices + 1 origin point = C(3,2) x 3 closure positions.

---

## How the 10 Sections Connect

The 81 tests are not 81 independent results. They are 81 readings of one geometric object. The connections:

**P1 provides P2 through P10.** Every test uses {K, D, F+, F0, F-, m_e, b, eps} from P1.

**P2 (alpha) connects P6 (photons) to P10 (nuclear).** The integer 137 is simultaneously photon modes + closure (nuclear reading) and gate threshold x vertices + origin (EM reading). The bridge identity shows these are the same count.

**P3 (masses) proves P5 (stability).** The structural factorization of each mass determines whether the particle achieves closure (stable) or not (decays). Mass is mode count. Stability is factorization quality.

**P4 (decay) validates P3 (masses).** If the mass mode counts are correct, decay must conserve them. Every tested decay conserves modes exactly. This is a cross-check that the mode counts are physically real, not numerical coincidences.

**P6 (photons) provides P7 (gauge groups).** The subchannel's 3 active corners give SU(3). The face's 3 edges give SU(2). The tetrahedron's 1 phase gives U(1). The photon structure at the subchannel level generates the gauge group at the face level.

**P7 (gauge groups) feeds P8 (electroweak).** The V4 subgroup gives the Weinberg angle at the UV scale. The gate depth distribution gives it at the IR scale. Both derive from the same K = 4 tetrahedron at different resolutions.

**P9 (charge) connects P6 (photons) to P7 (gauge groups).** Charge quantization in thirds comes from D = 3 spatial faces, which are the same D = 3 active subchannel corners that generate SU(3) colour. The face IS the subchannel at a coarser Sierpinski level.

**P10 (nuclear binding) uses P1 (constants) and P2 (alpha) to predict B/A.** The nuclear binding coefficients use the same F+, F0, F-, b, eps that appear everywhere else. The 3-scale decomposition B/A = 27a + 27b + 9c distributes binding energy across the same [27, 27, 9, 1] gate depth structure that generates the photon count (128 + 9 = 137).

---

## Summary Table

| Section | Tests | Topic | Key Result |
|---------|-------|-------|------------|
| P1 | 10/10 | Framework Identities | K=4, D=3, polynomial, gate depth [27,27,9,1] |
| P2 | 7/7 | Fine Structure Constant | 1/alpha = 137 + 1/28, 2 ppm accuracy |
| P3 | 10/10 | Particle Masses | 8 particles, all integer x m_e, < 0.12% error |
| P4 | 7/7 | Decay Conservation | Mode counts conserve exactly in every decay |
| P5 | 8/8 | Stability | Closure (sum) = stable, coupling (product) = unstable |
| P6 | 10/10 | Photon Structure | K-2 = 2 polarizations, 128 = 2^7 total modes |
| P7 | 6/6 | Gauge Groups | SU(3)xSU(2)xU(1) from subchannel/face/whole |
| P8 | 5/5 | Electroweak | sin^2(theta_W) = 9/39 = 0.231, W/Z ratio |
| P9 | 8/8 | Charge Quantization | 1/D = 1/3 quanta, quark charges, confinement |
| P10 | 10/10 | Nuclear Binding | 5 BW coefficients derived, bridge identity |
| **Total** | **81/81** | | **Zero fitted parameters** |

---

## Files

| File | Purpose |
|------|---------|
| `gfd_particle_properties.py` | Enterprise validation suite (81 tests) |
| `gfd_particle_properties_synthesis.md` | This teaching document |
| `gfd_3scale_binding.py` | Nuclear binding prediction script |
| `gfd_bethe_weizsacker.py` | BW coefficient derivation and comparison |
| `gfd_vortex_binding_teaching.md` | Physical picture of the gravity vortex |

```bash
python gfd_particle_properties.py       # run all 81 tests
python gfd_3scale_binding.py 26 56      # predict Iron-56 binding energy
python gfd_bethe_weizsacker.py 82 208   # predict Lead-208 with BW comparison
```

---

*Stephen Nelson, 2025-2026, Field Dynamics. CC BY 4.0.*
