# Can the Lattice Produce μ? Results

*Run 2026-11-14 against the criteria in [`PLAN.md`](PLAN.md), which was committed before any script ran. Outputs are in [`output/`](output/).*

## Answer in brief

**Not from nothing, but it narrows to a single assumption.** μ(x) comes out of each bond's own spectrum once one thing is assumed: the TetA end and the TetB end both couple to a common state, the Field Origin, with squared couplings in the ratio $g : a_0$.
- **The exponent is forced.** Baryonic Tully–Fisher fixes it (S5).
- **The share is exact.** It holds for any energy of the Field Origin state (S2, S4).
- **Exchange has a meaning.** It is the swap between the coupled ("bright") state and the decoupled ("dark") state (S2).
- **The field's energy has a bond form.** It is a polarity term plus the logarithm of the bond gap (S3). That answers, in form, what T06 found missing.

What is still assumed is why the TetA coupling grows with $g$ while the TetB coupling stays fixed at $a_0$.

| Test | Verdict | Result |
|---|---|---|
| S1 what the deep field forces | **PASS** (expected) | With polarity driven linearly by the field, a fixed coupling gives $\mu \to$ a nonzero constant as $g \to 0$: no deep field. The coupling must vanish as $\sqrt g$. Exactness forces the threshold $a_0$ and the coupling $\kappa\sqrt{ga_0}$; any other threshold would need a negative coupling somewhere. |
| S2 the Λ system | **PASS** (expected) | TetA and TetB ends at equal energy, both coupled to the Field Origin at energy $\Delta$. The lowest ("bright") state has TetA:TetB odds exactly $t_A^2 : t_B^2$, for every $\Delta$. The orthogonal combination is a dark state: decoupled, at zero energy, with the exchanged shares. With $t_A^2 : t_B^2 = g : a_0$ the bright share is $\mu(g/a_0)$. Eliminating the Field Origin gives result 9's polar energy $(g - a_0)/2$ and coupling $\sqrt{ga_0}$ together. |
| S3 the field's energy | **PASS** (expected) | $L = \tfrac12(g - a_0)^2 + a_0^2\ln(1 + g/a_0)$ has $L' = \mu g$ and equals AQUAL's $a_0^2F/2$ up to a constant. In bond terms, $L = 2V_3^2 + a_0^2\ln(\text{gap}/a_0)$, or $2V_3^2 + \tfrac12 a_0^2\ln\lvert\det H_{\rm bond}\rvert$, plus constants. $\ln(1+x)$ is the log partition function of a two-state system whose occupancy is $\mu$. |
| S4 the mechanism on the lattice | **FAIL** (by 0.11 points) | With each bond's share taken from the numerical lowest eigenvector of its own 3×3 Λ Hamiltonian, the lattice reproduces the field law within 0.38% (transition), 0.39% (deep field) and 0.61% (strong field, $x \approx 8$–50) for $r \ge 8d$. The criterion was 0.5%. The field is the same for $\Delta/a_0 = 0.01$, 1 and 100 to $2\times10^{-14}$. *Diagnostic:* the Λ-computed field equals the field with $\mu$ inserted by formula (T03's model) to $2\times10^{-14}$. The 0.61% is the lattice graininess already seen in T03 at the window's inner edge, not the mechanism. |
| S5 the remaining exponent | **PASS** (expected) | With $t_A^2 \propto g^n$, the deep field gives $g \propto g_N^{1/(n+1)}$: exponents 2/3, 1/2, 1/3 for $n = \tfrac12, 1, 2$. Only $n = 1$ gives flat rotation curves, with $v^4 = GMa_0$. This is the same $n = 1$ that the detailed-balance route needs. |

## What this adds

1. **Result 9's two requirements are one.** A polar energy $(g - a_0)/2$ and a coupling $\sqrt{ga_0}$ both follow from two degenerate ends coupled to one common state. That is the standard Λ system of quantum optics, the setting of coherent population trapping and dark states, which fits the photonic reading.
2. **The share is a branching ratio.** $\mu = t_A^2/(t_A^2 + t_B^2)$ is the bright state's weight on the TetA end, exact for any $\Delta$. In optics terms, it is the TetA drive's share of the total drive intensity.
3. **Exchange is bright ↔ dark.** The dark state carries $1 - \mu$ on TetA. Swapping TetA and TetB ($x \to 1/x$) swaps the two states.
4. **The energy has a bond form.** T06 showed the bond energy is the wrong object. The field's energy is instead a polarity term plus the log of the bond gap, or the bond's log-determinant.
5. **The lattice closes with μ computed.** S4 shows μ need not be inserted by hand, given the one assumption.

## What is still assumed

- **Why $t_A^2 : t_B^2 = g : a_0$.** That the TetA coupling to the Field Origin grows linearly with the local field, while the TetB coupling stays fixed at $a_0$. S5 shows the linearity is forced by observation, but the mechanism for it is not derived.
- **The readings.** That the common state is the Field Origin, and that the log term is a one-loop (log-determinant) contribution of the bond. Both are stated, not tested.
- **The lattice spacing and the absolute scale.** As in T20, these need a constant the framework does not yet supply.

## Notes on the run

- **S3** first failed one check because sympy could not simplify the square root of an unfactored square. It now compares the squares; both sides are positive. No criterion changed.
- **S4's script was refactored** so the diagnostic could import its functions. It was rerun after the refactor, and the output matched apart from round-off (Δ-difference $2.0$ against $2.2 \times 10^{-14}$).
