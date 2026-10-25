# Appendix A — Notation

**Status:** Reference
**Reading time:** 3 minutes (skim as needed)

---

## Constants

| Symbol | Value | Description |
|--------|-------|-------------|
| $\alpha$ | $7.2973525693 \times 10^{-3}$ | Fine structure constant |
| $1/\alpha$ | $137.0359991$ | Inverse fine structure constant |
| $g_e/2$ | $1.00115965218128$ | Electron gyromagnetic ratio (anomalous, half $g_e$) |
| $G$ | $6.67430 \times 10^{-11}$ m³/kg/s² | Newton's constant |
| $\hbar$ | $1.054571817 \times 10^{-34}$ J·s | Reduced Planck constant |
| $c$ | $2.99792458 \times 10^8$ m/s | Speed of light |
| $m_e$ | $9.1093837 \times 10^{-31}$ kg | Electron rest mass |
| $\mu_B$ | $9.274010 \times 10^{-24}$ J/T | Bohr magneton |
| $e$ | $1.602176634 \times 10^{-19}$ C | Elementary charge |
| royal cubit | $0.5236$ m | Egyptian royal cubit |
| $B_{0,\text{Giza}}$ | $\approx 45$ μT | Geomagnetic field strength at Giza |

## Framework symbols

### Algebra

| Symbol | Meaning |
|--------|---------|
| $K$ | Tetrad order; $K=4$ for spacetime, $K=5$ for portal shell |
| $D$ | Spatial dimension; $D=3$ in physical space |
| $\zeta_n$ | Primitive $n$-th root of unity, $e^{2\pi i / n}$ |
| $\Phi_n(x)$ | $n$-th cyclotomic polynomial |
| $\mathbb Q(\zeta_n)$ | $n$-th cyclotomic number field |
| $\mathbb Z_n$ | Cyclic group of order $n$ |
| $A_n$ | Alternating group on $n$ letters |
| $S_n$ | Symmetric group on $n$ letters |
| $\langle 1, I \rangle$ | Two-element parity sector (identity, involution) |

### Closure-read representation

| Symbol | Meaning |
|--------|---------|
| $V$ | Carrier space of the wave-read representation, $\dim V = K$ |
| $\Lambda^K V$ | $K$-th exterior power, $\dim = 1$ |
| $V \otimes V$ | Tensor square, $\dim = K^2$ |
| $C_K$ | Closure space $\Lambda^K V \oplus V \oplus V \otimes V$, $\dim = 1 + K + K^2$ |
| $P_0, P_1, P_2$ | Idempotent projectors onto $\Lambda^K V$, $V$, $V \otimes V$ |
| $I_s$ | Graded identity $P_0 + s P_1 + P_2$ for $s \in \{+1, 0, -1\}$ |
| $\text{Tr}(I_s)$ | Trace, giving $\{21, 17, 13\}$ at $K=4$ |

### Hinge and portal

| Symbol | Meaning |
|--------|---------|
| $J_4$ | Hinge operator $|5, -\rangle\langle 4, +|$ |
| $H_K$ | Hamiltonian of shell $K$ (cyclotomic units) |
| $V_\text{univ}$ | Universal vertex operator |
| $P_{y \leftarrow x}^{(e)}$ | Portal operator from $x$ to $y$ for species $e$ |
| $M_\text{Hopf,21,A_5}$ | Mirror address functional |
| $R(a, b, c)$ | Associator residue, $\in \langle 1, I \rangle$ |

### Couplings

| Symbol | Meaning |
|--------|---------|
| $\alpha_G$ | Gravitational coupling $(17/13)\alpha^{21}(g_e/2)$ |
| $g_\text{NL}$ | Nonlinear (associator) coupling (open question, [08.2](../08_open_questions/08.2_associator_nonlinearity.md)) |

### Hopf/icosahedral structure

| Symbol | Meaning |
|--------|---------|
| $S^n$ | $n$-sphere |
| $S^1 \to S^3 \to S^2$ | Hopf fibration |
| $2A_5$ | Binary icosahedral group (order 120) |
| $\Sigma(2,3,5)$ | Poincaré homology sphere $SU(2)/2A_5$ |
| $G_U, \chi_U, \Theta_U$ | Address triplet: base, deck, fiber |

### Chern-Simons

| Symbol | Meaning |
|--------|---------|
| $SU(2)_k$ | $SU(2)$ Chern-Simons theory at level $k$ |
| $\tau_n$ | Witten-Reshetikhin-Turaev invariant at level $n-2$ |
| $\tau_{21}(M)$ | WRT invariant of 3-manifold $M$ at level $19$ (so $k+2=21$) |

## Apparatus symbols

| Symbol | Meaning |
|--------|---------|
| KC | King's Chamber |
| QC | Queen's Chamber |
| $V_\text{KC}$ | Internal volume of King's Chamber, $1000\sqrt 5$ c³ |
| $V_\text{coffer}$ | External volume of granite coffer |
| Davison, Wellington, Nelson, Lady Arbuthnot, Campbell | The five relieving chambers (low to high) |

## Notational conventions

- **Inline math:** `$...$` for short expressions.
- **Display math:** `$$...$$` for set-off equations.
- **Boxed result:** load-bearing equations are wrapped in `\boxed{...}`.
- **Status tags:** every file begins with `**Status:** derived / structural / conjecture / open`.
- **Reading time:** rough estimate of how long a careful reader will spend on the document.
- **Cross-references:** relative paths to other files in the project.

## Sign conventions

- Metric signature: $(-, +, +, +)$ (mostly-plus).
- Parity action: $e^a \to -e^a$ for the tetrad.
- Cyclotomic primitive: $\zeta_n = e^{+2\pi i / n}$.
- Hopf orientation: $S^1 \to S^3$ via $(z_1, z_2) \mapsto z_1/z_2 \in S^2 \cup \{\infty\}$.

## Units

Where unstated, **SI**. Cyclotomic ring elements are **dimensionless**; physical quantities derived from them carry SI units via the dimensional anchors discussed in [08.1](../08_open_questions/08.1_transition_frequency.md).

Royal cubit lengths are used for chamber and coffer dimensions where the framework's apparatus interpretation is in play; converted to meters as $1\,\text{c} = 0.5236$ m.

---

**Cross-references:**
- [99/B Numerical constants](B_numerical_constants.md)
- [99/C Cyclotomic field decomposition](C_cyclotomic_field_decomposition.md)
