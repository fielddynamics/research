# The Tetrahedral Bit (t-bit) Algebra

## A Quantum Computation Framework Derived from GFD Geometric Primitives

**Stephen Nelson / Field Dynamics Research**
**Draft Framework — April 2026**

---

## 0. Motivation

Standard quantum computing rests on three axioms: (1) states live in complex Hilbert space ℂ², (2) gates are unitary matrices U(2), (3) measurement collapses superpositions probabilistically. Every one of these is imported from quantum mechanics wholesale. None is derived from geometry.

GFD provides a complete alternative substrate. The constitutive law μ = cos²(θ/2) IS a qubit state. The exchange symmetry x → 1/x IS a bit-flip gate. The Walsh–Hadamard transform IS the multi-bit Fourier analysis. But translating standard QM into GFD notation is worthless — it adds notation without adding structure.

This document derives a **new** gate algebra directly from the k = 4 geometric boundaries. The primitive is the **tetrahedral bit (t-bit)**: a tile whose internal acceleration ratio x ∈ (0, ∞) encodes a continuously variable logic state via the stellated octahedron's parity partition. Gates are Möbius maps on x. Multi-bit operations use the affine connection decomposition. Circuit compilation goes through the Walsh spectrum. Energy cost is computed from the AQUAL functional.

Nothing below requires Hilbert space, Born's rule, or the Schrödinger equation.

---

## 1. The Primitive: The Tetrahedral Bit

### Definition 1.1 (t-bit state)

A **t-bit** is a system whose state is a dimensionless acceleration ratio

$$x \in (0, \infty)$$

The state x determines two partition fractions via the forced constitutive law:

$$\mu(x) = \frac{x}{x+1}, \qquad \bar{\mu}(x) = \frac{1}{x+1}$$

with $\mu + \bar{\mu} = 1$ identically.

$\mu$ is the **TetA fraction** (identity component). $\bar{\mu}$ is the **TetB fraction** (parity component).

### Definition 1.2 (Spinor encoding)

The bijection $\theta = 2\arctan(1/\sqrt{x})$ maps $(0, \infty) \to (0, \pi)$. In spinor coordinates:

$$\mu = \cos^2(\theta/2), \qquad \bar{\mu} = \sin^2(\theta/2), \qquad x = \cot^2(\theta/2)$$

### Definition 1.3 (Logical states)

| State | $x$ | $\theta$ | $\mu$ | $\bar{\mu}$ | Name |
|-------|-----|----------|-------|-------------|------|
| $\|0\rangle_g$ | $\infty$ | $0$ | $1$ | $0$ | Pure TetA (Newtonian) |
| $\|?\rangle_g$ | $1$ | $\pi/2$ | $1/2$ | $1/2$ | Balanced (MOND ring) |
| $\|1\rangle_g$ | $0$ | $\pi$ | $0$ | $1$ | Pure TetB (deep field) |

The balanced state $|?\rangle_g$ is the **geometric superposition** — both chambers contribute equally. It is not a probability mixture; it is a deterministic partition.

### Definition 1.4 (Readout)

Measurement of a t-bit returns the **partition triple**:

$$\mathcal{R}(x) = \bigl(\mu(x),\; \bar{\mu}(x),\; \mu\bar{\mu}\bigr) = \left(\frac{x}{x+1},\; \frac{1}{x+1},\; \frac{x}{(x+1)^2}\right)$$

The third component $\mu\bar{\mu}$ is the **transition rate** — the simultaneous presence of both chambers. It peaks at $x = 1$ where $\mu\bar{\mu} = 1/4$. In spinor form: $\mu\bar{\mu} = \sin^2(\theta)/4$.

### Remark (Departure from QM)

The readout is **deterministic**, not probabilistic. There is no wavefunction collapse. The partition fraction $\mu$ is an observable geometric property of the tile, like the position of a needle on a gauge. "Randomness" in this framework arises from computational irreducibility of the multi-tile SAT evaluation (§6), not from a measurement postulate.

---

## 2. Single-t-bit Gate Algebra

### 2.1 The Gate Group: Möbius Maps on the Acceleration Line

The exchange symmetry $x \to 1/x$ lives in $\operatorname{Aut}(\mathbb{P}^1) = \operatorname{PGL}_2(\mathbb{R})$. This is the natural gate group.

**Definition 2.1 (Möbius gate).** A single-t-bit gate is a Möbius transformation

$$G_{[a,b,c,d]}(x) = \frac{ax + b}{cx + d}, \qquad ad - bc \neq 0, \quad G(x) > 0 \;\forall\; x > 0$$

The positivity constraint restricts to the **positive Möbius semigroup** $\operatorname{PGL}_2^+(\mathbb{R})$.

### 2.2 The Canonical Gate Set

Six gates derived directly from GFD structural identities:

**Gate P (Parity flip):** $[0, 1, 1, 0]$

$$P(x) = \frac{1}{x}$$

- $\theta \to \pi - \theta$
- $\mu \to 1 - \mu = \bar{\mu}$
- Swaps TetA ↔ TetB. Order 2: $P^2 = \mathrm{Id}$.
- Analog: Pauli-X

**Gate $T_\lambda$ (Threshold shift):** $[1, \lambda, 0, 1]$

$$T_\lambda(x) = x + \lambda$$

- Shifts the acceleration ratio by $\lambda$. Moves the MOND transition point.
- Physically: inject/extract external field of magnitude $\lambda \cdot a_0$.
- Generates a one-parameter continuous subgroup: $T_\lambda \circ T_\mu = T_{\lambda + \mu}$.

**Gate $D_\alpha$ (Dilation):** $[\alpha, 0, 0, 1]$

$$D_\alpha(x) = \alpha x$$

- Scales the acceleration ratio by $\alpha > 0$.
- In θ-space: $\theta \to 2\arctan(1/\sqrt{\alpha x})$. Nonlinear squeeze/stretch.
- $D_\alpha \circ D_\beta = D_{\alpha\beta}$. Log-linear in the parameter.
- At $\alpha = K^2 = 16$: the isotropic coupling dilation (all channels simultaneously).

**Gate $S$ (Square / spectral doubling):** $[1, 0, 0, 1]$ composed with itself in log-space

$$S(x) = x^2$$

- Not a Möbius map. Belongs to the **power-map extension** $x \mapsto x^\alpha$.
- In θ-space: doubles the cot argument. $\cot^2(\theta/2) \to \cot^4(\theta/2)$.
- Squeezes the partition fraction toward the poles: amplifies small deviations from $\mu = 1/2$.
- This is the **purification gate**: iterating $S$ drives any mixed state toward a pure state.

**Gate $R$ (Square root / spectral halving):**

$$R(x) = \sqrt{x}$$

- Inverse of $S$: $R \circ S = \mathrm{Id}$.
- Pushes any state toward the balanced point $\mu = 1/2$.
- This is the **mixing gate**: iterating $R$ drives any pure state toward the geometric superposition.

**Gate $M_s$ (Möbius constitutive map):** $[1, -1, 1, 1]$

$$M_s(x) = \frac{x - 1}{x + 1}$$

- This is the function $s(x)$ from the GFD framework that connects the coupling polynomial to the constitutive law.
- Maps $x \in (0, \infty) \to (-1, +1)$.
- At $x = 1$: $M_s = 0$ (field origin).
- At $x \to \infty$: $M_s \to +1$ (TetA).
- At $x \to 0^+$: $M_s \to -1$ (TetB).
- Compresses the infinite acceleration line into the finite interval where the coupling polynomial's state parameter $s$ lives.

### 2.3 Gate Composition Rules

**Theorem 2.1 (Closure).** The set $\{P, T_\lambda, D_\alpha\}$ generates all of $\operatorname{PGL}_2^+(\mathbb{R})$.

*Proof sketch.* Any $[a,b,c,d]$ with $ad - bc > 0$ and mapping $(0,\infty) \to (0,\infty)$ can be decomposed as:
$$G_{[a,b,c,d]} = D_{a/c} \circ T_{(bc-ad)/(ac)} \circ P \circ T_{c/1} \circ \ldots$$
The key identity: $P \circ T_\lambda \circ P = x \mapsto 1/(1/x + \lambda) = x/(1 + \lambda x)$, which is the gate $[1, 0, \lambda, 1]$. This plus $T_\lambda$ and $D_\alpha$ spans the group. ∎

**Theorem 2.2 (P generates the exchange group).** The subgroup of $\operatorname{PGL}_2^+(\mathbb{R})$ commuting with the exchange symmetry $x \to 1/x$ is $\{D_\alpha \;|\; \alpha > 0\} \cup P \cdot \{D_\alpha\}$.

In other words: the only gates that **preserve** the exchange symmetry are dilations and parity-conjugated dilations. Any gate that shifts or mixes $x$ **breaks** the exchange symmetry locally — this is the geometric cost of computation.

### 2.4 Effect on the Constitutive Law

For any Möbius gate $G$, the output constitutive fraction is:

$$\mu_{\text{out}} = \mu\bigl(G(x)\bigr) = \frac{G(x)}{G(x) + 1}$$

Explicitly for the canonical gates:

| Gate | $\mu_{\text{out}}$ | Effect on partition |
|------|-------------------|-------------------|
| $P$ | $1 - \mu$ | Full flip |
| $T_\lambda$ | $(x + \lambda)/(x + \lambda + 1)$ | Bias toward TetA by $\lambda/(x + \lambda + 1)$ |
| $D_\alpha$ | $\alpha x/(\alpha x + 1)$ | Squeeze toward TetA if $\alpha > 1$, toward TetB if $\alpha < 1$ |
| $S$ | $x^2/(x^2 + 1)$ | Amplify — push toward nearest pole |
| $R$ | $\sqrt{x}/(\sqrt{x} + 1)$ | Attenuate — push toward $\mu = 1/2$ |
| $M_s$ | $(x-1)/(2x)$ | Compress to linear regime |

### 2.5 Gate Cost from the AQUAL Functional

**Definition 2.2 (Gate energy).** The energy cost of applying gate $G$ to a t-bit in state $x$ is:

$$\mathcal{E}(G, x) = \bigl|F(G(x)^2) - F(x^2)\bigr|$$

where $F(y) = y - 2\sqrt{y} + 2\ln(1 + \sqrt{y})$ is the AQUAL energy functional.

**Theorem 2.3 (Parity flip cost).** The energy cost of the parity gate $P$ applied to state $x$ is:

$$\mathcal{E}(P, x) = \left|x^2 - \frac{1}{x^2} - 2x + \frac{2}{x} + 2\ln(x^2)\right|$$

For $x \gg 1$ (strongly Newtonian tile): $\mathcal{E}(P, x) \approx x^2$ — flipping a deeply committed tile is expensive.
For $x = 1$ (balanced tile): $\mathcal{E}(P, 1) = 0$ — flipping the balanced state is free.

This is the **geometric Landauer principle**: the cost of a bit-flip is not $k_B T \ln 2$ universally — it depends on the geometric state of the tile. Erasure at the MOND ring costs nothing; erasure deep in the Newtonian regime costs $\sim x^2$ units of the kinetic functional.

---

## 3. Two-t-bit Operations

### 3.1 The Geometric CNOT

**Definition 3.1 (CNOT).** Let Control have state $x_C$ and Target have state $x_T$. The geometric CNOT is:

$$\mathbf{X}_{\text{geo}}(x_T \,|\, x_C) = x_T^{\,\operatorname{sgn}(\mu_C - 1/2)}$$

Expanded:

$$\mathbf{X}_{\text{geo}}(x_T \,|\, x_C) = \begin{cases} x_T & \text{if } x_C > 1 \;\;(\mu_C > 1/2,\; \text{Control in TetA}) \\ x_T^{-1} & \text{if } x_C < 1 \;\;(\mu_C < 1/2,\; \text{Control in TetB}) \end{cases}$$

At $x_C = 1$ (Control at balance): the gate is **undefined**. This is the geometric singularity of conditional logic — you cannot conditionally flip a target when the control carries no parity bias.

### 3.2 The Soft CNOT (Continuous Extension)

To handle the singularity, define the **soft CNOT** using the Möbius map:

$$\mathbf{X}_{\text{soft}}(x_T \,|\, x_C) = \frac{x_T \cdot x_C + 1}{x_C + x_T}$$

**Verification of limits:**
- $x_C \to \infty$: $\to x_T \cdot x_C / x_C = x_T$ ✓ (no flip)
- $x_C \to 0$: $\to 1/x_T$ ✓ (full flip)
- $x_C = 1$: $\to (x_T + 1)/(1 + x_T) = 1$ → output is always balanced

This is a **Möbius blend**: the output smoothly interpolates between identity and parity as the control sweeps from TetA to TetB. When the control is at the MOND ring, the output is forced to the balanced state regardless of the target's input — the geometric superposition propagates.

### 3.3 Partition Algebra of the Soft CNOT

**Theorem 3.1.** The output constitutive fraction of the soft CNOT is:

$$\mu_{\text{out}} = \frac{x_T x_C + 1}{2(x_T x_C + 1) + (x_T + x_C - x_T x_C - 1)}$$

Simplifying by substituting $\mu_T = x_T/(x_T + 1)$, $\mu_C = x_C/(x_C+1)$:

$$\mu_{\text{out}} = \mu_T \mu_C + \bar{\mu}_T \bar{\mu}_C$$

**This is the XNOR of the two partition fractions.** The output TetA fraction equals the probability that both tiles agree (both TetA or both TetB). This is exactly the correlation function of the two-tile system.

**Corollary 3.1.** The CNOT output's TetB fraction is:

$$\bar{\mu}_{\text{out}} = \mu_T \bar{\mu}_C + \bar{\mu}_T \mu_C$$

which is the **XOR** of the partition fractions. The CNOT's TetB output measures the **disagreement** between the two tiles.

### 3.4 Entanglement Measure

**Definition 3.2 (Geometric entanglement).** For a two-t-bit system with states $(x_C, x_T)$ connected by the soft CNOT, define:

$$\mathcal{G}(x_C, x_T) = \mu_C \bar{\mu}_C \cdot \mu_T \bar{\mu}_T$$

This is the product of the two transition rates. It is maximised when **both** tiles are at the MOND ring ($x_C = x_T = 1$), where $\mathcal{G} = 1/16$.

**Theorem 3.2 (Entanglement from connection decomposition).** For two t-bits sharing a $K = 4$ boundary, the number of entangling connection components is:

$$N_{\text{ent}} = K(K-1)/2 \times 2 = 12$$

(six antisymmetric components per face, from each side of the boundary). The entangling fraction of the total $K^2 = 16$ boundary components is $12/16 = 3/4$.

The total entanglement capacity across all $K = 4$ faces of the joint boundary is:

$$C_{\text{ent}} = 4 \times 12 = 48 \text{ entangling channels}$$

out of $4 \times 16 = 64$ total. The **non-entangling** (diagonal, root-blind) channels number $4 \times 4 = 16 = K^2$.

### 3.5 Two-Control Gates from Three Tiles

**Definition 3.3 (Parity-controlled gate).** The natural product of two signed partition deviations:

$$\mathbf{T}_{\text{XOR}}(x_T \,|\, x_A, x_B) = x_T^{\,(2\mu_A - 1)(2\mu_B - 1)}$$

where $(2\mu - 1) = (x-1)/(x+1) = M_s(x)$ is the Möbius constitutive map.

**Theorem 3.3 (XOR discovery).** This gate is **XOR-controlled, not AND-controlled**:

| Control A | Control B | Exponent | Action |
|-----------|-----------|----------|--------|
| TetA ($s \approx +1$) | TetA ($s \approx +1$) | $+1$ | No flip |
| TetB ($s \approx -1$) | TetB ($s \approx -1$) | $+1$ | No flip |
| TetA ($s \approx +1$) | TetB ($s \approx -1$) | $-1$ | **Flip** |
| TetB ($s \approx -1$) | TetA ($s \approx +1$) | $-1$ | **Flip** |
| Balance ($s = 0$) | Any | $0$ | **Force to $x = 1$** |

The target flips when the controls **disagree**, not when both are TetB. The product $s_A \cdot s_B$ is the **parity correlation** — it detects disagreement.

This is a structural consequence: the Möbius map $M_s$ is the parity-symmetric projection of the constitutive law. Multiplying two such projections measures parity alignment, not joint occupation.

**Definition 3.4 (AND-controlled gate).** To flip the target only when **both** controls are in TetB, use the TetB-product exponent:

$$\mathbf{T}_{\text{AND}}(x_T \,|\, x_A, x_B) = x_T^{\,1 - 2\bar{\mu}_A \bar{\mu}_B}$$

where $\bar{\mu} = 1/(x+1)$ is the TetB fraction.

| Control A | Control B | $\bar{\mu}_A \bar{\mu}_B$ | Exponent | Action |
|-----------|-----------|-------------------------|----------|--------|
| TetA | TetA | $\approx 0$ | $+1$ | No flip |
| TetA | TetB | $\approx 0$ | $+1$ | No flip |
| TetB | TetA | $\approx 0$ | $+1$ | No flip |
| TetB | TetB | $\approx 1$ | $-1$ | **Flip** |
| Balance | Balance | $1/4$ | $+1/2$ | Partial (to $\sqrt{x_T}$) |

The AND-controlled gate breaks the exchange symmetry — it distinguishes TetB from TetA by using $\bar{\mu}$ (the parity-asymmetric fraction) instead of $M_s$ (the parity-symmetric projection). This asymmetry is the algebraic signature of irreversible logic: AND is not its own inverse, while XOR is.

**Corollary 3.2 (Gate taxonomy).** The GFD framework generates two natural gate families from the constitutive law:

| Construction | Exponent | Gate | Reversible? |
|-------------|----------|------|-------------|
| $s_A \cdot s_B = (2\mu_A - 1)(2\mu_B - 1)$ | Parity correlation | XOR-controlled | Yes ($P^2 = \text{Id}$) |
| $1 - 2\bar{\mu}_A \bar{\mu}_B$ | TetB joint fraction | AND-controlled | No |

Reversible gates emerge from the parity-symmetric sector of the algebra. Irreversible gates require breaking into the asymmetric sector.

**Theorem 3.4 (Universality).** The gate set $\{P, D_\alpha, \mathbf{X}_{\text{soft}}\}$ is **universal for GFD computation** — any Boolean function on $n$ t-bits can be implemented as a finite sequence of these gates.

*Proof.* $\{P, D_\alpha\}$ generates all single-t-bit Möbius maps (Theorem 2.1). The soft CNOT provides conditional parity coupling. Together they generate the XNOR/XOR correlation (Theorem 3.1), which combined with single-bit gates is classically universal. The continuous parameter $\alpha$ provides the analog extension. ∎

---

## 4. Multi-t-bit Circuits via Walsh Compilation

### 4.1 The Walsh–Hadamard Bridge

The Walsh–Hadamard transform connects the t-bit algebra (continuous, nonlinear, Möbius) to the Boolean circuit model (discrete, linear, FWHT). The bridge is:

**Theorem 4.1 (Walsh = Hadamard on t-bit arrays).** Let $\mathbf{x} = (x_0, \ldots, x_{N-1})$ be an array of $n = \log_2 N$ t-bits, each clamped to the logical poles $x_i \in \{0^+, +\infty\}$ (i.e., $\mu_i \in \{0, 1\}$). Encode the joint state as the integer $j = \sum_i \mu_i \cdot 2^i$. Then the Walsh character

$$\chi_c(j) = (-1)^{\operatorname{popcount}(c \,\&\, j)}$$

is the **parity readout** of the t-bit array: the product of $\operatorname{sgn}(\mu_i - 1/2)$ over all bits $i$ where $c$ has a 1.

### 4.2 Compiling Boolean Functions to t-bit Circuits

**Input:** A Boolean function $f: \{0,1\}^n \to \{0,1\}$ given as a truth table of length $N = 2^n$.

**Step 1 (Spectral analysis):** Compute the Walsh bridge coefficients:

$$b[c] = \frac{1}{N} \sum_{j=0}^{N-1} (1 - 2f(j)) \cdot \chi_c(j)$$

via the FWHT. Cost: $O(N \log N)$.

**Step 2 (Sparsity identification):** Count the nonzero bridge coefficients $s = |\{c : b[c] \neq 0\}|$. This is the **Walsh sparsity** — the intrinsic complexity of $f$ in the spectral basis.

**Step 3 (Circuit synthesis):** For each nonzero coefficient $b[c]$:
  - The mask $c$ identifies which t-bits participate (which bits of $c$ are 1)
  - The coefficient $b[c]$ sets the coupling strength
  - Implement as: multi-controlled dilation $D_{|b[c]|}$ gated on the participating t-bits

**Step 4 (Accumulation):** Sum all $s$ WaveNode contributions:

$$\text{output}(j) = \sum_{c: b[c] \neq 0} b[c] \cdot \chi_c(j)$$

This is the WaveNode formula. Each term is one multi-controlled Möbius gate.

### 4.3 Circuit Depth Bounds

**Theorem 4.2 (Depth = Walsh sparsity).** The circuit depth of a Boolean function $f$ in the t-bit architecture is exactly $s$, the Walsh sparsity of $f$.

| Function | Sparsity $s$ | t-bit Depth | Classical Depth |
|----------|-------------|-------------|----------------|
| XOR (parity) | 1 | 1 | $n$ |
| AND | $2^n$ | $2^n$ | $n$ |
| Majority | $O(2^n / \sqrt{n})$ | $O(2^n/\sqrt{n})$ | $O(n)$ |
| 7-segment digit | 4–8 per segment | 4–8 | ~12 gates |
| Random function | $2^n$ | $2^n$ | $2^n$ |

XOR achieves **exponential speedup** over classical serial evaluation: depth 1 regardless of $n$. This is not quantum parallelism — it is spectral sparsity. The Walsh transform reveals that XOR has exactly one nonzero Fourier coefficient (the all-ones mask $c = 2^n - 1$), so it evaluates in one WaveNode operation.

### 4.4 The LUT-6 Boundary

On an FPGA (Kria KR260), any Boolean function of ≤ 6 inputs maps to exactly one LUT-6 cell. In the t-bit framework, this corresponds to a **6-t-bit register** with at most $2^6 = 64$ bridge coefficients.

The bridge representation and the LUT-6 INIT value encode the **same function** in dual bases:
- LUT-6: truth table (spatial domain) → lookup
- Bridge: Walsh spectrum (frequency domain) → polynomial evaluation

The FWHT converts between them in $64 \times 6 = 384$ additions. This is the **compilation cost** of translating between the computational and spectral representations.

---

## 5. Energy Accounting: The Geometric Landauer Bound

### 5.1 Gate Energy from the AQUAL Functional

**Definition 5.1.** The **geometric action** of a t-bit in state $x$ is $F(x^2)$ where:

$$F(y) = y - 2\sqrt{y} + 2\ln(1 + \sqrt{y})$$

**Theorem 5.1 (Parity flip cost).** The energy difference between a state and its parity-flipped image is:

$$\Delta F(x) \equiv F(x^2) - F(x^{-2}) = x^2 - x^{-2} - 2(x - x^{-1}) + 4\ln x$$

**Corollary 5.1 (Free erasure at the MOND ring).** $\Delta F(1) = 0$. A t-bit at the geometric superposition point can be flipped at zero energy cost.

**Corollary 5.2 (Quadratic cost in the Newtonian regime).** For $x \gg 1$: $\Delta F(x) \approx x^2$. Flipping a deeply Newtonian tile costs energy quadratic in its acceleration ratio.

**Corollary 5.3 (Logarithmic cost at moderate acceleration).** For $x$ of order unity but $x \neq 1$: $\Delta F(x) \approx 4\ln x + O(x - 1)$. The leading cost is logarithmic.

### 5.2 Circuit Energy

**Definition 5.2.** The total energy of a circuit with gates $G_1, \ldots, G_d$ applied to t-bits with input states $x_1, \ldots, x_d$ is:

$$\mathcal{E}_{\text{circuit}} = \sum_{i=1}^d \mathcal{E}(G_i, x_i) = \sum_{i=1}^d \bigl|F(G_i(x_i)^2) - F(x_i^2)\bigr|$$

**Theorem 5.2 (Geometric Landauer bound).** The exact parity flip cost is:

$$\Delta F(x) = \left(x^2 - \frac{1}{x^2}\right) - 2\left(x - \frac{1}{x}\right) + 2\ln x$$

Asymptotic regimes:
- Near balance ($x \to 1$, $t = \ln x \to 0$): $\Delta F \approx 2\ln x$ — logarithmic
- Deep Newtonian ($x \gg 1$): $\Delta F \approx x^2$ — quadratic
- At balance ($x = 1$): $\Delta F = 0$ — free

**Operational consequence:** The most energy-efficient computation routes all bit-flips through the balanced state $x = 1$. This is the geometric analog of adiabatic quantum computation — you reduce the gate energy by first mixing (attenuating) the t-bit toward balance, performing the flip there (for free), then amplifying back.

### 5.3 The Clock Tick

The fundamental gate time for a single electron tile:

$$\tau = \frac{\hbar}{m_e c^2} \approx 1.288 \times 10^{-21} \text{ s}$$

This is the **Zitterbewegung period** — the hardware clock of the tetrahedral SAT evaluator. Each $\tau$ evaluates the 32-channel parity closure condition across all $K^2 = 16$ TetA and $16$ TetB connection components.

**Gate rate:** $\nu = 1/\tau \approx 7.76 \times 10^{20}$ Hz.

**Power per t-bit:** $\mathcal{P} = m_e c^2 / \tau \cdot \Delta F \cdot (a_0^2 / 8\pi G)$. The dimensionful power depends on the coupling constant combination $a_0^2/(8\pi G)$ from the covariant action.

---

## 6. Network Topology

### 6.1 The Stellated Octahedron Graph

The natural network topology for t-bits is the **stellated octahedron graph** $\Gamma_{\text{SO}}$:

- **8 vertices** = 8 qubit registers (cube vertices = $\{-1, +1\}^3$)
- **TetA edges** (6) = intra-sector links connecting the 4 TetA vertices
- **TetB edges** (6) = intra-sector links connecting the 4 TetB vertices
- **Cross edges** (12) = cube edges connecting TetA ↔ TetB vertices
- **Total:** 24 edges

Each edge carries a connection with $K^2 = 16$ components, split 10/6 (retained/discarded). Across all edges:

$$\text{Total connection components} = 24 \times 16 = 384 = 6 \times K^3$$

### 6.2 Channel Partition

For a two-t-bit link in the network:

| Channel type | Count per face | × 4 faces | Role |
|-------------|---------------|-----------|------|
| Diagonal (root-blind) | $K = 4$ | 16 | Classical channel (no parity distinction) |
| Upper-triangle (TetA) | $K(K-1)/2 = 6$ | 24 | TetA → TetA coherent transfer |
| Lower-triangle (TetB) | $K(K-1)/2 = 6$ | 24 | TetB → TetB coherent transfer |
| **Total** | $K^2 = 16$ | **64** | |

The 24 + 24 = 48 off-diagonal components are the **entangling channels**. The 16 diagonal components are the **classical channels**. Entangling fraction: 48/64 = 3/4.

### 6.3 Network Scaling

**Theorem 6.1.** An $n$-t-bit network on the stellated octahedron graph requires:

- $\lceil n/8 \rceil$ octahedral cells
- $6 \lceil n/8 \rceil$ intra-cell links per sector
- Inter-cell links determined by the packing geometry

**Theorem 6.2 (Dimensional constraint).** The Diophantine equation $2(D+1) = 2^D$ at $D = 3$ constrains the network:

- Maximum **native** register width per cell: $2^D = 8$ t-bits
- Maximum **entangling faces** per cell: $2(D+1) = 8$ faces
- These two counts are **equal** only at $D = 3$: every vertex has exactly one face, and every face has exactly one vertex. This is the **self-dual packing** condition.

For $D < 3$: more faces than vertices → over-constrained (no room for independent states).
For $D > 3$: more vertices than faces → under-constrained (dangling states with no closure).

---

## 7. Operational Protocols

### 7.1 State Preparation

**Protocol: Prepare t-bit in state $x_{\text{target}}$**

1. Start with t-bit at natural rest state $x_0$ (determined by local gravitational environment)
2. Apply dilation $D_\alpha$ with $\alpha = x_{\text{target}} / x_0$
3. Readout: verify $\mu(x_{\text{target}})$ matches expected value
4. Cost: $\mathcal{E} = |F(\alpha^2 x_0^2) - F(x_0^2)|$

**Protocol: Prepare balanced state $|?\rangle_g$**

1. Apply attenuation gate $R$ iteratively: $x \to \sqrt{x} \to x^{1/4} \to \ldots$
2. After $k$ iterations: $x_k = x_0^{1/2^k}$
3. Convergence: $x_k \to 1$ as $k \to \infty$ (for any $x_0 > 0$)
4. Cost per iteration decreases geometrically: $\mathcal{E}_k \approx 4|\ln x_0| / 2^k$
5. Total cost: $\mathcal{E}_{\text{total}} \approx 8|\ln x_0|$

### 7.2 Entanglement Generation

**Protocol: Entangle two t-bits**

1. Prepare both t-bits at balanced state $x_C = x_T = 1$
2. Apply soft CNOT: $x_T' = (x_T x_C + 1)/(x_C + x_T) = 1$
3. Apply dilation $D_\alpha$ to Control: $x_C \to \alpha$
4. Apply soft CNOT again: $x_T' = (\alpha + 1)/(\alpha + 1) = 1$

Wait — this doesn't entangle at balanced states because the CNOT output at $x_C = x_T = 1$ is always 1. The entanglement protocol requires **asymmetric** preparation:

1. Prepare Control at $x_C = K^2 = 16$ (strongly TetA)
2. Prepare Target at $x_T = 1$ (balanced)
3. Apply soft CNOT: $x_T' = (16 + 1)/(16 + 1) = 1$ — still balanced
4. Now apply **hard CNOT**: since $\mu_C = 16/17 > 1/2$, target is unchanged
5. Flip Control with P: $x_C \to 1/16$
6. Apply hard CNOT: since $\mu_C = 1/17 < 1/2$, target flips: $x_T' = 1$... → $1/1 = 1$

The balanced state is a **fixed point** of the CNOT. Entanglement requires states with $x \neq 1$.

**Corrected Protocol:**

1. Prepare Control at $x_C = K^2 = 16$ (TetA)
2. Prepare Target at $x_T = K = 4$ (weakly TetA)
3. Apply soft CNOT: $x_T' = (64 + 1)/(16 + 4) = 65/20 = 3.25$
4. The output is **not** a product of the input partition fractions — the states are now **correlated through the geometric boundary**

The correlation is quantified by:

$$\mathcal{G} = \mu_C \bar{\mu}_C \cdot \mu_T' \bar{\mu}_T' = \frac{16}{17^2} \cdot \frac{3.25}{4.25^2} \approx 0.0554 \cdot 0.180 \approx 0.010$$

Maximum entanglement ($\mathcal{G} = 1/16 = 0.0625$) requires both tiles at the MOND ring **after** the gate, not before.

### 7.3 Circuit Execution

**Protocol: Evaluate Boolean function $f$ on $n$ t-bit inputs**

1. **Prepare** input t-bits at logical poles: $x_i = K^2$ for $f_i = 0$, $x_i = 1/K^2$ for $f_i = 1$
2. **Compile** $f$ via FWHT: extract bridge coefficients $b[c]$
3. **For each** nonzero $b[c]$:
   a. Identify participating t-bits from mask $c$
   b. Compute character $\chi_c(j) = (-1)^{\operatorname{popcount}(c \,\&\, j)}$ from participating t-bit states
   c. Accumulate $b[c] \cdot \chi_c(j)$ into output register
4. **Threshold** the accumulated output: positive → TetA ($f = 0$), negative → TetB ($f = 1$)
5. **Total cost:** $s$ WaveNode evaluations, each at cost $\mathcal{E} \leq 4\ln(K^2) = 8\ln K$

### 7.4 Error Detection via S₄ Symmetry

**Protocol: Detect single-t-bit errors**

The stellated octahedron has $S_4$ symmetry (24 elements). Any single-t-bit error (deviation from the intended $x$) breaks the Gram matrix identity $M^T M = G$.

1. After each gate, compute $G_{\text{actual}} = M^T M$ for the current tile configuration
2. Compare with forced Gram matrix $G_{\text{expected}} = \alpha I + \beta J$
3. Any off-diagonal deviation $|G_{ab} - (-c^2/3)| > \epsilon$ flags the error
4. The S₄ orbit of the error identifies which vertex (t-bit) is corrupted
5. **Correction:** apply $D_\alpha$ to the corrupted t-bit with $\alpha = x_{\text{expected}} / x_{\text{actual}}$

**Error detection rate:** The S₄ symmetry provides $|S_4| - 1 = 23$ independent parity checks per octahedral cell. For an 8-t-bit register, this gives check density $23/8 \approx 2.9$ checks per t-bit — higher than the surface code at comparable distance.

---

## 8. The t-bit Algebra at a Glance

| Standard QM | t-bit Framework | Origin |
|------------|----------------|--------|
| State $\|\psi\rangle \in \mathbb{C}^2$ | State $x \in (0, \infty)$ | Acceleration ratio |
| Pauli-X | Parity gate $P: x \to 1/x$ | Exchange symmetry |
| Pauli-Z | Dilation $D_{-1}$: identity on $\mu$ | Trivial (already diagonal) |
| Hadamard $H$ | Mixing gate $R: x \to \sqrt{x}$ | Spectral halving |
| CNOT | Soft CNOT: $(x_T x_C + 1)/(x_C + x_T)$ | Möbius blend |
| XOR-Toffoli | $x_T^{(2\mu_A - 1)(2\mu_B - 1)}$ | Parity correlation (symmetric) |
| AND-Toffoli | $x_T^{1 - 2\bar{\mu}_A\bar{\mu}_B}$ | TetB joint fraction (asymmetric) |
| Born probability | Partition fraction $\mu = x/(x+1)$ | Forced constitutive law |
| Entanglement | $\mathcal{G} = \prod \mu_i \bar{\mu}_i$ | Joint transition rate |
| Gate energy | $\Delta F = (x^2 - x^{-2}) - 2(x - x^{-1}) + 2\ln x$ | AQUAL functional difference |
| Clock rate | $\tau = \hbar / m_e c^2$ | Zitterbewegung / SAT tick |
| Circuit depth | Walsh sparsity $s$ | FWHT of truth table |
| Error detection | $S_4$ Gram matrix check | Tetrahedral symmetry |
| Decoherence | Connection components lost to torsion (24/64) | 40/24 decomposition |
| Hilbert space dimension | $2^D = 8$ per octahedral cell | Diophantine uniqueness |
| Reversible gates | Parity-symmetric sector ($M_s$ products) | Exchange-invariant |
| Irreversible gates | Parity-asymmetric sector ($\bar{\mu}$ products) | Exchange-breaking |

---

## 9. Open Directions

**9.1 Quantum advantage characterization.** Which functions have Walsh sparsity $s \ll 2^n$? The t-bit framework predicts that functions with **high parity structure** (XOR-like, linear over GF(2)) are exponentially cheaper than functions with **high correlation structure** (AND-like, monotone). This is a concrete, testable prediction about circuit complexity.

**9.2 Continuous-variable extension.** The t-bit state $x$ is continuous, not discrete. The "clamping" to logical poles $x \in \{0^+, \infty\}$ throws away the intermediate structure. A **continuous-variable t-bit protocol** that exploits the full $(0, \infty)$ range could encode $\log_2$ bits of precision per t-bit, giving an analog advantage over binary computation.

**9.3 Thermodynamic verification.** The exact gate cost $\Delta F(x) = (x^2 - x^{-2}) - 2(x - x^{-1}) + 2\ln x$ is a concrete prediction. For an electron tile at $x = K^2 = 16$: $\Delta F(16) \approx 16^2 = 256$ (deep Newtonian regime, quadratic dominance). Near the MOND ring at $x = 1.01$: $\Delta F \approx 2\ln(1.01) \approx 0.02$ — nearly free. The crossover from logarithmic to quadratic regimes occurs at $x \sim 2$–$3$, where all three terms of $\Delta F$ contribute comparably. This crossover scale is an observable: it determines the computational temperature at which bit-flip energy transitions from "cheap" (reversible, adiabatic) to "expensive" (irreversible, dissipative).

**9.4 Walsh sparsity of physical laws.** The gravitational constitutive law $\mu(x) = x/(x+1)$, when discretized to $n$ bits of precision, has a specific Walsh spectrum. The sparsity of this spectrum determines the computational complexity of gravity itself — how many WaveNode operations nature requires per clock tick to evaluate the field equation.

**9.5 Network capacity from torsion.** The 24 discarded torsion components per $K = 4$ boundary represent quantum channel capacity that GR throws away. In the t-bit framework, these components are available as **entangling resources**. A t-bit network that retains torsion has $64/64 = 100\%$ of its channel capacity; the torsion-free projection reduces this to $40/64 = 62.5\%$. The missing $37.5\%$ is what appears as "dark" coupling in torsion-free observations.

**9.6 Reversibility from exchange symmetry (Theorem 3.3 discovery).** The verification revealed that the natural two-control gate from the Möbius constitutive map $M_s = (2\mu - 1)$ is XOR-controlled, not AND-controlled. This is not a bug — it is a structural theorem:

> **The parity-symmetric sector of the t-bit algebra generates only reversible gates.**

The product $s_A \cdot s_B = (2\mu_A - 1)(2\mu_B - 1)$ is invariant under the exchange $\mu \to 1 - \mu$ applied to **both** inputs simultaneously. Reversibility follows from this joint exchange invariance. To build irreversible (AND-controlled) gates, one must break into the parity-asymmetric sector using $\bar{\mu}$ directly. This connects the second law of thermodynamics to the geometry: entropy production requires breaking the exchange symmetry of the stellated octahedron.

**9.7 The soft CNOT as correlator.** The XNOR identity $\mu_{\text{out}} = \mu_T \mu_C + \bar{\mu}_T \bar{\mu}_C$ (Theorem 3.1) identifies the soft CNOT output as the **classical correlation function** of the two-tile system. This is the connected two-point function $\langle \mu_T \mu_C \rangle + \langle \bar{\mu}_T \bar{\mu}_C \rangle = 1 - 2\mu_T\bar{\mu}_C - 2\bar{\mu}_T\mu_C + \ldots$ — the standard quantum information measure of how aligned two systems are. The XOR complement $\bar{\mu}_{\text{out}} = \mu_T \bar{\mu}_C + \bar{\mu}_T \mu_C$ is the **anti-correlation function**. Together they partition unity: agreement + disagreement = 1. The soft CNOT is not just a gate — it is a **measurement of parity alignment** between two tiles.

**9.8 Continuous-variable logic.** The t-bit framework's most radical departure from standard quantum computing is that the state $x \in (0, \infty)$ is continuous. The gates $D_\alpha$ and $T_\lambda$ have continuous parameters. The soft CNOT and soft Toffoli produce continuous outputs even from discrete inputs. This means the t-bit architecture is natively a **continuous-variable** system that can be clamped to discrete logic as a special case — the inverse of standard quantum computing, which starts discrete and must engineer continuous control. The implications for analog quantum simulation and variational algorithms deserve exploration.
