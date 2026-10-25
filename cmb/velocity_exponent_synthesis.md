# The Velocity Exponent, the Field Origin, and the Time-Face Lattice

## A Structural Synthesis of the 0.17

**Stephen Nelson — Gravity Field Dynamics**
**March 2026**

---

## 1. What This Document Explores

The Tully-Fisher velocity evolution exponent is $(1 - 1/\pi)/4 \approx 0.17$. It appears in two independent derivations, matches nine IFU survey measurements with zero fitted parameters, and shares three significant digits with the Field Origin coupling depth $f(K,0) = 17$.

This document synthesizes three threads that converged during the CMB gravitational enhancement session:

1. The exponent as a partition of the naive $1/K$ evolution budget between TetA and TetB at the tiling boundary.
2. The physical meaning of the exponent in the unbound CMB regime, where neither chamber carries bound matter and the field sits at the Field Origin threshold.
3. The possibility that CMB photons, propagating through time-face stratification channels in the $K = 4$ lattice, experience the same $1/\pi$ geometric filtering that governs the gravitational source — the Buffon needle connection.

Items 1 and 2 are structural results within the framework. Item 3 is a specific physical proposal that has not been computed but has a well-defined mathematical structure.

---

## 2. Two Routes to the Same Exponent

### 2.1 The Paper Route (2025 JCAP Submission)

The submitted paper derives the exponent through the covariant action:

1. The saturation scale is $a_0 = cH/(2\pi) \times \sqrt{K/\pi}$, with the $\sqrt{K/\pi}$ factor as a geometric correction between discrete field packing and the spherical Hubble horizon.
2. The naive velocity exponent from the BTFR ($v^4 = GMa_0$) is $1/4 = 0.25$.
3. The disformal coupling in the covariant action modifies the effective photon metric. Rotation velocities at high redshift are inferred from Doppler shifts of photons that have propagated through the scalar field. The paper states: "The aperture factor $\sqrt{K/\pi} = 1.128$ governs the fraction of the acceleration-scale evolution that is absorbed into the photon propagation path rather than appearing as a kinematic velocity shift."
4. The effective exponent is 0.17.

In this framing, the correction lives in the **observation channel**. The saturation scale $a_0$ still scales linearly with $H$. What changes is what the observer sees, because the disformal coupling absorbs part of the evolution into the photon metric.

### 2.2 The API Route (CMB Derivation, 2026)

The CMB gravitational enhancement derivation obtains the exponent through the boundary coupling integral:

1. $K = 4$ gravitational fields tile spacetime with 2-sphere closure boundaries in $D = 3$.
2. The average coupling fraction across all field separations is exactly $\eta = 1/\pi$ (from $\int_0^1 \arccos(u)\,du = 1$).
3. Field closure ($\det(e) \neq 0$) requires the TetA/TetB partition at every boundary. The uncoupled fraction $(1 - 1/\pi)$ compounds across independent boundary traversals, modifying the scaling to $a_0 \propto H^{1-1/\pi}$.
4. The BTFR gives the velocity exponent: $(1 - 1/\pi)/4 = 0.17$.

In this framing, the correction lives in the **source**. The saturation scale itself scales as $H^{1-1/\pi}$, not linearly.

### 2.3 Why the API Route Is Primary

The CMB enhancement at $z = 1100$ is 6.46, not 28. The acoustic peaks are gravitational potential wells, not photon propagation artifacts. The wells are genuinely shallower than naive $a_0 \propto H$ predicts because $a_0$ genuinely scales as $H^{1-1/\pi}$. If the correction were only in the photon path, the wells themselves would still be 28 times deeper than baryonic matter alone could produce, and no photon-metric adjustment could change the well depth after the fact.

The CMB locks it: the correction is in $a_0$ itself.

### 2.4 But the Paper Route May Also Be Present

This is the central proposal of this document: both may be operating simultaneously. The same $K = 4$ tiling geometry that modifies the gravitational source also structures the channels through which photons propagate. If both produce $1/\pi$, the observation is consistent with either, both, or some partition between them. Section 6 develops this possibility.

---

## 3. The Partition of the Naive Exponent

The naive velocity exponent is $1/K = 1/4 = 0.25$. This is the total evolution budget per face from the BTFR. At the tiling boundary, this budget partitions through the same $K = 4$ ports that both chambers share:

$$\frac{1}{K} = \frac{1 - 1/\pi}{K} + \frac{1}{K\pi}$$

$$0.25 = 0.1704 + 0.0796$$

This is exact. It is the partition $1 = (1 - 1/\pi) + 1/\pi$ distributed across $K$ faces.

The TetA contribution $1/(K\pi) = 0.0796$ is the fraction of the per-face evolution that the boundary coupling absorbs into tiling interactions. It does not appear in the observed velocity evolution.

The TetB contribution $(1 - 1/\pi)/K = 0.1704$ is what survives as the observable exponent.

Both chambers operate through the same $K = 4$ active ports. The observable is TetB's share after TetA's share has been absorbed into boundary coupling.

---

## 4. The Unbound Regime and the Field Origin Threshold

### 4.1 Galaxies vs the CMB

In a galaxy, TetA is occupied. Baryonic mass sits in the vortex interior. TetA actively drives the dynamics through the coupling throat. The rotation curve is the combined work of both chambers: TetA carrying the baryonic source, TetB carrying the enhanced response. The full polynomial sweeps from $f = 13$ in the deep field exterior to $f = 21$ in the Newtonian core.

At the CMB, nothing is bound. No galaxies exist. No vortex interiors have formed. No baryonic mass is concentrated in TetA. Both chambers are empty, unbound fields tiling a nearly homogeneous plasma. TetA has no dynamical content to contribute. Its coupling fraction goes entirely into boundary tiling, not into driving observable evolution.

### 4.2 The $s = 0$ Condition

When neither chamber is preferentially active, the state parameter is $s = 0$. The flow term $sK$ vanishes. The coupling polynomial reads:

$$f(K, 0) = K^2 + 0 + K^0 = 16 + 1 = 17$$

This is the Field Origin. The threshold of spacetime. The $3+1$ decomposition lives between $f = 17$ (the state-independent capacity) and $f = 21$ (full TetA activation). Below 17, the field is in pure TetB territory with no structured spacetime dynamics.

The velocity exponent $(1 - 1/\pi)/K = 0.17042...$ measures the same physical condition: the $K = 4$ topology at zero occupancy. The polynomial reads 17 because the flow is off. The exponent reads 0.17 because TetA is empty.

### 4.3 The Numerical Relationship

The exponent is $(\pi - 1)/(4\pi) = 0.17042...$, while $17/100 = 0.17000...$. The gap is $4.2 \times 10^{-4}$.

This gap has a structural interpretation. The exponent involves $\pi$ from the continuous boundary integral. The integer 17 is the discrete channel count. The difference between $(\pi - 1)/(4\pi)$ and $17/100$ is the difference between the continuous geometry and the discrete topology — the same tetrahedral-to-spherical aperture mismatch that produces the $\pm 6.2\%$ measurement band in the Hubble constant prediction.

An algebraic identity connecting $(\pi - 1)/(4\pi) = (K^2 + 1)/N$ for some topologically meaningful $N$ has not been found. The physical parallelism is clear: both are state-independent readings of $K = 4$ geometry at $s = 0$. Whether the numerical proximity is coincidence or structure remains open.

---

## 5. The $3+1$ Decomposition at the Topology Level

Each tetrahedron in the stellated octahedron has $K = 4$ faces. In the $3+1$ decomposition, these partition as:

- **3 spatial faces**: each opposite a spatial vertex, carrying spatial coupling
- **1 time face**: opposite the temporal vertex, carrying temporal coupling

This is the tetrad's $3+1$ structure realized at the face level. The time face is not a metaphor. In the vierbein formalism, one of the four basis vectors is timelike. The face opposite that basis vector is the time face.

When adjacent tetrahedra tile spacetime, their faces couple. Spatial faces couple to spatial faces. Time faces couple to time faces. In isotropic $K = 4$ packing, the time faces of vertically adjacent tetrahedra align into stratification layers: continuous sheets of time-face coupling running through the lattice.

Photons propagate on null geodesics, which are the boundary between the spatial and temporal sectors. In the tetrad topology, this boundary is the time face. Photon propagation follows the time-face stratification channels.

---

## 6. The Buffon Needle Connection

### 6.1 The Classic Problem

In 1777, the Comte de Buffon posed a problem: drop a needle of length $L$ onto lined paper with line spacing $d$. What is the probability that the needle crosses a line?

The answer is $P = 2L/(\pi d)$. When $L = d$, the crossing probability is $2/\pi$.

The $\pi$ appears because the needle has an angle $\theta$ relative to the lines, and the crossing condition depends on $\cos\theta$. Averaging over all angles produces:

$$P = \frac{2}{d} \int_0^{\pi/2} L\cos\theta \, d\theta = \frac{2L}{\pi d}$$

The integral $\int_0^{\pi/2} \cos\theta \, d\theta = 1$ is the same definite integral (by substitution) that produces the $1/\pi$ in the boundary coupling fraction. Both compute the average geometric overlap of a linear object with a periodic structure.

### 6.2 CMB Photons as Buffon Needles

CMB photons have been propagating for 13.8 billion years. Their paths are linear (null geodesics on the cosmological background). The time-face stratification layers of the $K = 4$ lattice are periodic boundaries running through the lattice.

A photon crossing this lattice is a needle crossing lined paper. At each layer crossing, the photon interacts with the time-face boundary geometry. The probability of interaction depends on the angle of the photon path relative to the stratification layer, and averaging over all angles produces the same $1/\pi$ geometric factor.

This is a specific, testable proposal: CMB photons accumulate a geometric filtering of $1/\pi$ per boundary traversal as they propagate through the time-face lattice. After $N$ crossings, the cumulative filtering modifies the observed signal by the compounded surviving fraction, producing a power-law correction with the same $1/\pi$ exponent that appears in the gravitational source.

### 6.3 Why Both Could Be Present

The gravitational source correction (API route) says: the saturation scale $a_0$ evolves as $H^{1-1/\pi}$ because the spatial boundary coupling compounds across the tiling lattice.

The photon-path correction (paper route) would say: the observed signal is additionally filtered by $1/\pi$ per time-face layer crossing because the photon's Buffon interaction with the stratification geometry compounds across the propagation path.

If both are present, they produce the same $1/\pi$ because they arise from the same $K = 4$ tiling geometry. The spatial boundaries produce $1/\pi$ for the gravitational source. The temporal boundaries produce $1/\pi$ for the photon channel. One lattice, two sectors, same geometric fraction.

The CMB measurement would then be reading two $1/\pi$ effects superimposed:

- The gravitational wells are shallower than naive linear scaling predicts (source correction)
- The photons propagating from those wells are geometrically filtered by the time-face lattice (channel correction)

Whether these are independent contributions that add, multiply, or are somehow the same effect counted once through two projections is an open question. The fact that the CMB enhancement matches the source-only prediction (6.46 vs $6.36 \pm 0.10$) suggests that the source correction alone accounts for the observation, and the photon-path effect, if present, is either subdominant or already included in the source calculation through the disformal coupling.

### 6.4 What Would Distinguish Them

A source-only correction predicts that the gravitational wells themselves are 6.46 times deeper than baryonic matter alone. A combined source-plus-channel correction would predict slightly different well depths, with the photon filtering making up the difference. The distinguishing observable would be gravitational lensing of background sources by CMB-era structure: lensing depends on the well depth directly, without photon-path filtering, because the lensing deflection is geometric.

If CMB lensing measures the same 6.46 enhancement as the acoustic peaks, the correction is in the source alone. If lensing measures a different enhancement, the photon-path contribution is real and separate.

This is a prediction that future CMB lensing measurements (CMB-S4, Simons Observatory) could test.

---

## 7. The Framing for the API Documentation

The velocity exponent in the API documentation should use the source framing (the API route), because the CMB enhancement confirms the correction lives in $a_0$:

The exponent $(1-1/\pi)/4$ is the TetB surviving fraction per face per closure revolution. The $1/\pi$ is the boundary coupling fraction from the $K = 4$ tiling integral. The $1-1/\pi$ is the TetB retention — what the uncoupled boundary carries after TetA's share has been absorbed into tiling interactions. The $K = 4$ in the denominator distributes this across the tetrahedral face channels.

The paper's disformal coupling language should be retired in the documentation. The $\sqrt{K/\pi}$ aperture factor remains in the $H_0$ prediction and the measurement band, where it belongs as the discrete-to-continuous geometric mismatch. But the velocity exponent comes from the partition, not from photon screening.

The Buffon/time-face proposal is a research direction, not a documentation claim. It belongs in the synthesis and extensions literature, not in the API docstring.

---

## 8. Summary Table

| Quantity | Value | Origin | Status |
|:---|:---|:---|:---|
| Naive velocity exponent | $1/K = 0.25$ | BTFR with $a_0 \propto H$ | Level A |
| Boundary coupling fraction | $\eta = 1/\pi$ | Exact continuum overlap integral | Level A |
| Corrected velocity exponent | $(1-1/\pi)/K = 0.17$ | Partition of naive budget | Level A |
| TetA share absorbed | $1/(K\pi) = 0.08$ | Boundary coupling per face | Level A |
| Field Origin coupling depth | $f(0) = K^2 + 1 = 17$ | Polynomial at $s = 0$ | Level A |
| Connection: 0.17 to 17 | Physical parallelism | Both are $s = 0$ readings of $K = 4$ | Level C |
| Buffon filtering of CMB photons | $1/\pi$ per time-face crossing | Angle-averaged layer interaction | Level C |
| Testable prediction | Lensing vs acoustic enhancement | Source-only vs source-plus-channel | Future work |

---

## 9. What This Synthesis Establishes

**Established.** The velocity exponent $(1-1/\pi)/4$ is the TetB surviving fraction per face, with TetA's share absorbed into boundary coupling through the shared $K = 4$ ports. Both chambers participate. The observable is what TetB retains.

**Established.** At the CMB, both chambers are unbound. The field sits at the Field Origin, $s = 0$, $f = 17$. The velocity exponent measures the $K = 4$ topology at zero occupancy. The numerical proximity of 0.17042 to 17/100 reflects the shared physical condition: state-independent $K = 4$ geometry.

**Established.** The API route (source correction, $a_0 \propto H^{1-1/\pi}$) is the primary framing, confirmed by the CMB enhancement. The paper route (photon-path correction via disformal coupling) describes a real physical mechanism but places the correction in the observation channel rather than the source.

**Proposed.** CMB photons propagating through the time-face stratification of the $K = 4$ lattice may experience Buffon-type geometric filtering with the same $1/\pi$ factor. This would mean the source and the channel both carry $1/\pi$ corrections from the same tiling geometry, operating simultaneously on different sectors of the tetrad.

**Testable.** If the photon-path correction is present and independent of the source correction, CMB lensing should measure a different enhancement than the acoustic peaks. If lensing matches acoustic peaks, the correction is source-only.

---

## References

Bekenstein, J. D. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? *Astrophys. J.* 286, 7.

Buffon, G.-L. L., Comte de (1777). "Essai d'arithmétique morale." *Supplément à l'Histoire Naturelle*, vol. 4.

Gibbons, G. W. and Hawking, S. W. (1977). Cosmological event horizons, thermodynamics, and particle creation. *Phys. Rev. D* 15, 2738.

Planck Collaboration (2020). Planck 2018 results. VI. Cosmological parameters. *Astron. Astrophys.* 641, A6.

---

*Copyright © 2025–2026 Stephen Nelson. Documentation: CC BY 4.0. Code: MIT.*
