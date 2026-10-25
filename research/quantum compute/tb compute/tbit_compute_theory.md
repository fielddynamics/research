# The t-bit Compute Algebra, Part III

## Classification, Structure, and the Complex Extension

**Stephen Nelson / Field Dynamics Research**
**Draft — April 2026**

---

## 0. Scope

Parts I (`tbit_algebra.md`) and II (`tbit_network_algebra.md`) establish the state space, the gate algebra, and the network flow. Three items remain unresolved as a *computational* framework:

1. **Class.** The framework is called "quantum" but renounces Hilbert space, Born's rule, and Schrödinger evolution. The v2 §7.4 table explicitly shows state space ℝ^N and O(N²) simulation — that is a **classical** model. What is the actual computational class?
2. **Gate group closure.** S and R are power maps, not Möbius. The full generated group is PGL₂⁺(ℝ) together with the power-map subgroup, and these do not commute. No presentation is given.
3. **Clifford vs. magic.** Theorem 3.3 of v1 flags that the natural (2μ−1)(2μ−1) product gives XOR, not AND; the AND-controlled gate must break into the parity-asymmetric sector. This hints at a Clifford/magic split but does not formalise it.

This Part III closes all three.

**Structural results** (each verified in `tbit_compute.py`):

- **T1 (Rebit classification).** The t-bit is a rebit, modulo the sign of one amplitude.
- **T2 (Gate group).** The single-t-bit gate monoid is PGL₂⁺(ℝ) ⋊ (ℝ*, ×) with intertwining relation p_α ∘ D_β = D_{β^α} ∘ p_α. In log-coordinates u = ln x, the sub-group ⟨P, D_α, p_α⟩ is the full orientation-preserving affine group Aff(ℝ) extended by ℤ₂; T_λ is the one Möbius gate nonlinear in u.
- **T3 (SAC theorem).** The parity-symmetric sector acts on the Walsh bridge by signs only ("sign-action on characters"). It is efficiently classically simulable. Magic elements: T_λ, M_s, AND-Toffoli.
- **T4 (c-bit extension).** Promoting the complex coupling polynomial f(K, e^{iθ}) to a dynamical object yields a genuine complex-amplitude element with a proper Hadamard, S, and controlled phase. The t-bit is the phase-zero slice of the c-bit.

Honest accounting of the circuit-depth claims finishes the classification.

---

## 1. The Rebit Classification Theorem

### 1.1 Definition (Rebit)

A *rebit* is a two-level system with real amplitudes: |ψ⟩ = a|0⟩ + b|1⟩, a, b ∈ ℝ, a² + b² = 1. The state space is the real Bloch circle (one-dimensional), not the Bloch sphere.

### 1.2 Theorem (T1)

The t-bit bijection

$$x = \cot^2(\theta/2), \qquad \mu = \cos^2(\theta/2) = a^2, \qquad \bar{\mu} = \sin^2(\theta/2) = b^2$$

identifies a t-bit with a rebit up to the sign of b. The map x ↔ (|a|, |b|) is one-to-one on the non-negative quadrant; the pairs (+a, +b) and (+a, −b) are both mapped to the same x.

### 1.3 Consequence (Phase-blindness)

The t-bit cannot distinguish |+⟩ = (|0⟩+|1⟩)/√2 from |−⟩ = (|0⟩−|1⟩)/√2. Both are x = 1 in the t-bit description. This is *exactly* why the framework has "no phase" and "no Born rule" — not an additional choice but a consequence of the parametrisation.

**Computational import.** Rebit quantum computing is BQP-universal (Aharonov, 2003), provided CCZ (or equivalent) is available. The t-bit framework is therefore **at most** as strong as rebit QC, and strictly weaker if the phase-sign is unrecoverable — which it is, for the bare t-bit.

The complex extension in §5 restores the phase and closes this gap.

---

## 2. Gate Group Structure

### 2.1 The Two Sectors

- **Möbius sector:** PGL₂⁺(ℝ), 3-parameter. Generators {P, T_λ, D_α} (v1 Thm 2.1).
- **Power-map sector:** (ℝ*, ×), 1-parameter. Generators p_α : x ↦ x^α. This contains S = p_2 and R = p_{1/2}.

### 2.2 Commutation Relations (verified)

$$P \circ p_\alpha = p_\alpha \circ P \qquad \text{(parity commutes with power)}$$
$$p_\alpha \circ D_\beta = D_{\beta^\alpha} \circ p_\alpha \qquad \text{(intertwining)}$$
$$[p_\alpha, T_\lambda] \neq 0 \qquad \text{(power does NOT normalise shift)}$$

The full gate monoid is therefore **not** a semidirect product of Möbius and power-maps; it is a subgroup of the analytic transformation group of (0, ∞) that properly contains both.

### 2.3 The Clean Presentation: Log Coordinates

In u = ln x:

| Gate | Action on u |
|------|-------------|
| P | u → −u (reflection) |
| D_α | u → u + ln α (translation) |
| p_α | u → αu (dilation) |
| S = p_2 | u → 2u |
| R = p_{1/2} | u → u/2 |
| T_λ | u → ln(e^u + λ) **(nonlinear)** |

The subgroup ⟨P, D_α, p_α⟩ is the orientation-preserving affine group Aff(ℝ) = ℝ ⋊ ℝ*, extended by the ℤ₂ reflection P.

Every element in this subgroup acts on u as

$$u \mapsto \pm \alpha \cdot u + c$$

for some α > 0, c ∈ ℝ, sign ∈ {+, −}. This is the **affine sector** and it is the natural "clean" subgroup of the t-bit algebra.

**T_λ is outside the affine sector.** This is the source of all nonlinearity in the single-t-bit algebra and the origin of irreversibility (§3).

---

## 3. The SAC Theorem (Clifford / Magic Split)

### 3.1 Definition (Sign-Action on Characters)

Let f : {0,1}^n → {0,1} have Walsh bridge b[c] = (1/N) Σ_j (1 − 2f(j)) χ_c(j).

A gate G acts on truth tables by G : tt ↦ tt'. We say G is **sign-acting on characters (SAC)** iff G induces on the bridge a transformation of the form

$$b'[c] = s(c) \cdot b[\pi(c)]$$

for some sign assignment s : 2^n → {+, −} and some permutation π of 2^n.

The SAC transformations form a group: the semidirect product of sign patterns and character permutations.

### 3.2 Theorem (T3)

The following gates are SAC:

- Single-t-bit: **P** (bit-flip), **D_α**, **p_α** — under pole-clamped inputs, these either preserve the pole set or act by a rescaling that is invisible once the input is re-clamped.
- Two-t-bit: **soft CNOT**, **XOR-Toffoli** — verified by bridge-magnitude preservation on random 4-bit truth tables.
- c-bit (§5): **H**, **S_Clifford**, **CPhase_δ**.

The following gates are **not** SAC (magic):

- **T_λ** — takes a pole state (x = 0) to an off-pole state (x = λ), which cannot be encoded as a truth-table permutation.
- **M_s** — same obstruction; the constitutive map's image is (−1, +1), outside the pole lattice.
- **AND-Toffoli** — verified: applying AND-Toffoli to the identity truth table tt(j) = (j & 1) takes sparsity 1 → 4, changing the bridge magnitudes. It is not a sign-action.

### 3.3 Corollary (Efficient Classical Simulation)

Any circuit built entirely from SAC gates can be simulated in O(n·s) time, where s is the Walsh sparsity of the output. Track the sign pattern and the permutation of characters; the truth table is never materialised.

### 3.4 The Magic Bound

A circuit with k invocations of {T_λ, M_s, AND-Toffoli} can be simulated in O(n · s · C^k) time for some constant C, by branching over the magic-gate output at each invocation. This mirrors the Bravyi-Gosset magic-state count for standard Clifford+T.

**This is the first concrete computational-complexity statement of the t-bit framework.** The "exchange symmetry breaking = irreversibility" discovery in v1 §9.6 is now operationalised: the parity-symmetric sector is SAC = classically simulable, and exchange-breaking gates are exactly the magic elements.

---

## 4. The c-bit: Complex Extension

### 4.1 Motivation

The complex coupling polynomial

$$f(K, e^{i\theta}) = 1 + K e^{i\theta} + K^2$$

already appears in the framework (`tbit_verify.py` §7): at K=4 it traces a circle of radius 4 centred on 17, and the transition rate μ(1−μ) equals |Im f|²/(4K²) = sin²θ / 4.

The phase θ that is lost in the t-bit reduction (→ x = cot²(θ/2)) is precisely the phase of e^{iθ} in the complex polynomial. Promoting θ from a derived angle to an **independent state variable** yields the c-bit.

### 4.2 Definition (c-bit)

A **c-bit** is a normalised amplitude pair (α, β) ∈ ℂ², |α|² + |β|² = 1, with the phase convention that α ∈ ℝ_{≥0}. Display coordinates:

$$x = |\alpha|^2 / |\beta|^2, \qquad \phi = \arg \beta.$$

The bare t-bit is the slice φ ∈ {0, π}; the c-bit captures the full Bloch sphere.

### 4.3 c-bit Gate Primitives

| Gate | Action | Matrix (in {|0⟩, |1⟩}) |
|------|--------|------------------------|
| P | α ↔ β | [[0,1],[1,0]] |
| D_α | x → αx | (nonlinear, preserves phase) |
| Φ_δ | β → e^{iδ} β | diag(1, e^{iδ}) |
| H | standard Hadamard | (1/√2)[[1,1],[1,−1]] |
| S_Clifford | β → iβ | diag(1, i) |
| Z | β → −β | diag(1, −1) |

Verified relations: **H² = I**, **S² = Z**, **S⁴ = I**. These are the exact Clifford algebra of a single qubit, restricted to the basis of the c-bit.

### 4.4 The Bell Vertex in the c-bit Framework

The interior law's x = 2 result becomes interpretable. Construct |Φ+⟩ = (|00⟩ + |11⟩)/√2 via (H ⊗ I) followed by CNOT. Trace out one c-bit. The reduced density matrix has diagonal entries (1/2, 1/2), so:

- **Spatial (TetA) law:** μ_A = 1/2 ⟹ x_A = 1 (MOND ring).
- **Subspace (TetB) law:** μ_B = 1/2 ⟹ x_B = 2 (Bell vertex).

The scalar x = 2 from the interior law is **the subspace-law acceleration ratio of the maximally-entangled marginal**. It is not a two-body invariant; it is the one-body TetB reading of a one-body TetA MOND state.

---

## 5. Density-Matrix Formalism

A c-bit state induces the 2×2 Hermitian density

$$\rho = \begin{pmatrix} \mu & \sqrt{\mu \bar\mu}\, e^{-i\phi} \\ \sqrt{\mu \bar\mu}\, e^{i\phi} & \bar\mu \end{pmatrix}$$

Verified: Tr ρ = 1, ρ = ρ†, rank 1 (pure), Tr(ρ²) = 1.

**Off-diagonal magnitude:** |ρ_{01}|² = μ · μ̄ = sin²θ / 4. The transition rate **is** the squared coherence. This is the structural result that the "transition rate" from v1 §1.4 is a 2×2-density off-diagonal, not a third probability.

**Rebit slice:** φ = 0 ⟹ ρ ∈ M_2(ℝ). The t-bit is the real-density restriction.

---

## 6. POVM Measurement

The v1 "partition triple" R(x) = (μ, μ̄, μμ̄) does not sum to 1 and is not a POVM.

The correct POVM is the two-outcome projective measurement

$$E_0 = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}, \qquad E_1 = \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}, \qquad E_0 + E_1 = I.$$

- Tr(ρ E_0) = μ, Tr(ρ E_1) = μ̄ — verified, phase-invariant.
- Transition rate is **not** a measurement outcome; it is an **observable** in its own right, namely the squared modulus of the off-diagonal.

The framework is deterministic in the sense that a pure state gives a sharp POVM outcome iff μ ∈ {0, 1} — i.e. iff the state is at a pole. For balanced states (x = 1, μ = 1/2), the POVM outcomes are 50/50, matching Born's rule trivially. **This is not an additional postulate**; it is the trace inner-product of the density and the projector.

---

## 7. Circuit Depth, Honest

### 7.1 The Overclaim

v1 §4.3 gives the table

| Function | t-bit Depth | Classical Depth |
|----------|-------------|-----------------|
| XOR | 1 | n |
| AND | 2^n | n |

The "classical depth = n" column silently assumes *serial* evaluation. Parallel classical depth for XOR is O(log n) via a binary tree of 2-input gates.

### 7.2 Honest Comparison

| Function | t-bit (WaveNode count) | Classical parallel depth | Advantage |
|----------|------------------------|--------------------------|-----------|
| XOR | 1 | ⌈log₂ n⌉ | **log n** |
| AND | 2^n | ⌈log₂ n⌉ | **t-bit is exp. WORSE** |
| Majority | O(2^n / √n) | ⌈log₂ n⌉ | t-bit worse |
| Random | ≈ 2^n | ≈ n | t-bit worse |

Verified in `tbit_compute.py` §7.

### 7.3 Where the t-bit Architecture Genuinely Wins

The WaveNode evaluates a Boolean function as a single parallel sum of Walsh characters. For functions of **low Walsh sparsity** (the parity-structured class: XOR, affine, linear over GF(2)), the WaveNode count is O(1) to O(n), beating the classical log-depth tree by a constant factor.

The advantage is **constant-factor on sparse inputs**, not exponential. The framework's value as a compute architecture is in the **sparsity-adaptive evaluation model**, not in a BQP-class speedup.

### 7.4 What the t-bit Framework Costs

For monotone Boolean functions (AND, majority, threshold), Walsh sparsity is worst-case 2^n. The t-bit architecture is exponentially worse than classical parallel circuits on these.

This exactly matches the intuition: monotone = exchange-breaking = magic-dominated. The framework pays an exponential price precisely in the sector where exchange symmetry fails.

---

## 8. Computational Classification Summary

| Property | t-bit (bare) | c-bit | Classical bit | Standard qubit |
|----------|--------------|-------|---------------|----------------|
| State space | (0, ∞) | ℂ² / U(1) | {0, 1} | ℂ² / U(1) |
| Dimension | 1 real | 2 real | 1 bit | 2 real |
| Phase | absent | arg β | absent | present |
| Gate group | PGL₂⁺(ℝ) ⋊ ℝ* | U(2) / U(1) | S_2 | U(2) / U(1) |
| Clifford sector | SAC = parity-symmetric | ⟨H, S, CNOT⟩ | reversible logic | ⟨H, S, CNOT⟩ |
| Magic | {T_λ, M_s, AND-Tof} | {T, Toffoli} | — | {T, Toffoli} |
| Measurement | POVM on pole set | POVM {E_0, E_1} | deterministic | POVM |
| Simulation | O(n·s) Clifford | O(n·s·C^k) with magic | O(n) | O(n·s·C^k) with magic |

**The t-bit framework is a rebit restricted to the amplitude-only slice, equipped with a power-map sector that the standard rebit lacks.** It is polynomially equivalent to a classical-Clifford circuit model for parity-symmetric inputs; magic elements are required for universality, at which point the class is BQP-matchable *only if the c-bit extension is adopted*.

---

## 9. Open Directions

**9.1 Bravyi-Gosset magic bound for T_λ.** Quantify the exact rate at which T_λ invocations amplify classical-simulation cost. Conjecture: a k-fold T_λ-cascade on the pole set generates at most 2^k distinct off-pole values, so classical simulation is O(n · s · 2^k) — matching the standard magic state count.

**9.2 The transducer as entanglement routing.** The topological transducer μ_A = μ_B/Φ_6(μ_B) has gain 1.464 at the golden-ratio operating point (v2 §6.4). In the c-bit framework, this is an explicit amplifier of off-diagonal coherence across a TetA/TetB boundary. The transducer is a passive (unitary) entanglement distributor — no active gate required.

**9.3 The 24 torsion components as ancilla.** v1 §9.5 notes that the 24 discarded torsion components carry 37.5% of channel capacity. In the SAC framework, these are the **magic resource**: the ancillary register needed to break out of the parity-symmetric sector and implement AND-Toffoli. Working out the exact encoding of magic states into torsion components is the natural next step.

**9.4 Bell vertex = Pauli exclusion as Jacobian saturation.** The eigenvalue λ_repul = −1/4 at the Bell vertex saturates the transition-rate bound μ(1−μ) ≤ 1/4. In the c-bit framework, this is the statement that |Φ⁺⟩ has maximal off-diagonal coherence |ρ_{01}|² = 1/4 on each reduced density. The "Pauli exclusion" is the **maximum-coherence constraint**, not a principle separate from the geometry.

**9.5 Hadamard in the t-bit (bare).** The t-bit cannot support a true Hadamard (Thm T1). The closest thing is the "mixing gate" R with asymptotic convergence to balance. This is a structural limitation of the bare framework, not a choice — and it is resolved in the c-bit.

**9.6 Measurement determinism as pole-clamping.** The v1 claim "measurement is deterministic, no wavefunction collapse" is correct **only for pole-clamped inputs** (x ∈ {0⁺, ∞}). For balanced or intermediate states, the POVM gives a genuine probability distribution matching the Born rule exactly. Determinism is a property of the input set, not of the measurement.

---

## 10. Corrections to Parts I and II

The following claims should be revised in v3 printings of `tbit_algebra.md` and `tbit_network_algebra.md`:

1. **v1 Thm 3.4 (Universality).** "{P, D_α, X_soft} is universal for GFD computation" — true for Boolean reversible universality, **not** for BQP or any quantum-complexity class. Revise to: "... is universal for classical reversible Boolean computation; quantum-class universality requires the c-bit extension and CPhase_δ."

2. **v1 §1.4 Readout triple.** "R(x) = (μ, μ̄, μμ̄)" — the third component is a coherence magnitude, not a probability. Revise to two-outcome POVM {E_0, E_1} with μμ̄ as the separate coherence observable |ρ_{01}|².

3. **v1 §4.3 depth table.** Classical column is *serial* depth. Add parallel column; note that t-bit advantage is log n for XOR and exp-worse for AND.

4. **v1 §2.2 gate list.** S and R are power maps, not Möbius. Clarify: the single-t-bit gate monoid is PGL₂⁺(ℝ) ⋊ (ℝ*, ×); the two sectors do not commute cleanly (intertwining relation §2.2 of Part III).

5. **v2 §7.4 scaling table.** "State space ℝ^N, simulation O(N²)" — this describes a **classical** model, not quantum. Revise to: "The bare t-bit network is a classical analog computing model; the c-bit extension (Part III) provides the genuine complex-amplitude structure needed for quantum-class advantage."

---

*End Part III.*
