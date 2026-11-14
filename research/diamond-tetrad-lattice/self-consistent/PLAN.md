# Can the Lattice Produce μ? Plan

*Field Dynamics Research, research folder, 2026-11-14. Status: plan, with criteria fixed before any script was run. Part of the [diamond-lattice note](../README.md).*

## The question

In test T03 the diamond net reproduced GFD's field equation, but only because $\mu(x) = x/(1+x)$ was put on every bond by hand. Result 9 says what a bond needs in order to produce $\mu$ itself: a polar energy $V_3 = (g - a_0)/2$ and a coupling $V_2 = \sqrt{g a_0}$, two separate requirements. T06 found that the bond energy then does not give the field's energy.

This study asks:
- how much of that is forced;
- whether one mechanism supplies both requirements at once;
- whether the field's energy can be written in natural bond terms;
- whether the mechanism closes on the lattice with $\mu$ computed rather than inserted.

## Honesty note

The exact items S1, S2, S3 and S5 were worked out while designing this plan, so they are expected to pass; they are recorded as checks, not discoveries under test. The informative items are S4 (the lattice run) and the overall verdict: what is still assumed at the end.

## The tests

**S1. What the deep-field limit forces on any bond.**
- *Setup:* a two-level bond whose polar energy is driven linearly by the local field, $V_3 = \kappa(g - g_*)/2$ with $\kappa > 0$ and threshold $g_*$, and any positive coupling $V_2(g)$.
- *Claim:* GFD's limits, $\mu \to 1$ for $g \gg a_0$ and $\mu \to g/a_0$ for $g \to 0$, require $V_2(g)^2 \to \kappa^2 g_*^2\, g/a_0$ as $g \to 0$: the coupling must vanish as $\sqrt g$. So a fixed coupling, as in ordinary tight binding, cannot give the deep field. $\mu = g/(g+a_0)$ at every $g$ holds if and only if $g_* = a_0$ and $V_2 = \kappa\sqrt{g a_0}$.
- *Pass:* exact derivation, plus an exact demonstration that a constant $V_2$ gives $\mu \to$ a nonzero constant as $g \to 0$.

**S2. One mechanism for both requirements: the Λ system.**
- *Setup:* the TetA end and the TetB end, at equal energy, each couple to one common state, the Field Origin, at energy $\Delta$, with couplings $t_A$ and $t_B$. In quantum optics this is the Λ system.
- *Claims (exact, any $\Delta$):*
  1. The lowest state has TetA:TetB odds exactly $t_A^2 : t_B^2$, so its TetA share is $t_A^2/(t_A^2 + t_B^2)$.
  2. The orthogonal combination is a dark state: it decouples from the Field Origin, sits at zero energy, and has the exchanged shares $t_B^2 : t_A^2$. So exchange ($x \to 1/x$) is bright ↔ dark.
  3. With $t_A^2 = c\,g$ and $t_B^2 = c\,a_0$, the bright state's TetA share is $\mu(g/a_0)$ for every $\Delta$. Eliminating the Field Origin at large $\Delta$ gives result 9's polar energy $(g - a_0)/2$ and coupling $\sqrt{g a_0}$ together, both from the one assumption.
- *Pass:* exact.

**S3. The field's energy in bond terms.**
- *Claim:* the AQUAL Lagrangian density for $\mu = x/(1+x)$, $L(g)$ with $L'(g) = \mu g$, is $L = \tfrac12(g - a_0)^2 + a_0^2 \ln(1 + g/a_0) + $ const. In bond terms that is $2V_3^2 + a_0^2 \ln(\text{gap}/a_0)$ + const: a polarity term plus the logarithm of the bond gap $g + a_0$. Equivalently $2V_3^2 + \tfrac12 a_0^2 \ln\lvert\det H_{\rm bond}\rvert$ + const.
- *Also:* $\ln(1 + x)$ is the log partition function of a two-state system with odds $x$, whose occupancy is $\mu = \partial \ln Z/\partial \ln x$.
- *Pass:* exact identities. The reading, that the log term is a one-loop (log-determinant) contribution of the bond, is stated as a reading and not tested here.

**S4. The mechanism on the lattice, with μ computed, not inserted.**
- *Setup:* as T03 (diamond net, $n = 32$, Picard iteration, Dirichlet box). On each bond, build the 3×3 Λ Hamiltonian with $t_A^2 = g_b$ (the bond's local field) and $t_B^2 = a_0$. Compute its lowest eigenvector numerically, take the TetA:TetB share as the bond's conductance, and solve self-consistently.
- *Runs:* $\Delta/a_0 = 0.01$, 1 and 100 at the transition window ($a_0 = 10^{-2}$), and $\Delta/a_0 = 1$ at $a_0 = 10^{-4}$ and $a_0 = 1$.
- *Pass:* every run matches the analytic $g(r)$ to within 0.5% for $r \ge 8d$ (the window T03 established; fixed here before running), and the result is the same for every $\Delta$ to within $10^{-6}$.
- *Means:* μ is then an output of the bond's own spectrum on the lattice. The input has moved from "$\mu(x)$" to "$t_A^2 : t_B^2 = g : a_0$".

**S5. Is the one remaining assumption free?**
- *Setup:* in the Λ mechanism, try $t_A^2 \propto g^n$ with $t_B^2$ fixed, for $n = \tfrac12, 1, 2$ (for example, $n = 2$ would be a coupling amplitude proportional to the field).
- *Claim:* only $n = 1$ gives flat rotation curves with $v^4 \propto GM a_0$ (baryonic Tully–Fisher) in the deep field. $n = 2$ gives $g \propto g_N^{1/3}$, and $n = \tfrac12$ gives $g \propto g_N^{2/3}$. This matches the detailed-balance route's $n = 1$.
- *Pass:* exact deep-field exponents.

## What would count as success

- **Full success** would be the lattice fixing $t_A^2 : t_B^2 = g : a_0$ by itself. This study does not claim that.
- **The realistic aim:**
  - reduce result 9's two requirements to one stated mechanism (S2);
  - show the mechanism closes on the lattice (S4);
  - show its one remaining exponent is forced by observation (S5);
  - give the energy a natural bond form (S3).

That would leave GFD with one precise open question: why the TetA coupling to the Field Origin grows as $g$ while the TetB coupling is fixed at $a_0$.
