# Pre-registration 2: screening from the bound-state law

*Committed before the rule was evaluated. The rule, the data and the pass criteria below are fixed; the evaluation script is written to this specification.*

## Motivation

The first pre-registered screening rule ([`PREREGISTRATION_screening.md`](PREREGISTRATION_screening.md)) used the constitutive law in its one-directional form, $\mu(x) = x/(1+x)$. It failed narrowly: its effective charges were systematically low.

GFD's nuclear papers distinguish two forms of the same law ([Paper 11](../../papers/11-nuclear-shells-tetrahedral-packing/), [Paper XIII](../../papers/13-nuclear-binding-bidirectional-sst/)):

- **Unbound (one direction).** Matter sources the field and the field responds: $\mu = x/(1+x)$. This governs galaxies.
- **Bound (both directions).** Each partner is source and response at once, so the return coupling $(1-\mu)$ must reproduce $\mu$ through the same transition: $x(1-\mu)^2 = \mu$, with physical root

$$\mu_2(x) = \frac{(2x+1) - \sqrt{4x+1}}{2x}.$$

This governs nuclei, and Paper XIII uses it, unchanged, for both the shell structure and the binding curve.

Electrons in an atom are a bound system: each electron screens the others and is screened by them. On the framework's own terms, the bound form is the one that applies. The first rule used the unbound form. This document tests the bound form, with no other change.

**Disclosure.** The first rule's outcome is known: its same-radius screening, $\mu(1) = \tfrac12$, is stronger than Slater's empirical 0.35. The bound form gives $\mu_2(1) = (3-\sqrt5)/2 = 0.382$. The choice of the bound form is motivated by the nuclear papers, but it is made with knowledge of that first result. For that reason the decisive test is on new data, $Z = 21$–36, which no rule in this folder has been evaluated against. The Z = 21–36 reference values were retrieved before this document was written; no model output has been computed on them.

## The rule (primary)

Electron $j$ screens electron $i$ by the bound-state share at the radius ratio:

$$s_{ij} = \mu_2\!\left(\frac{r_i}{r_j}\right).$$

- An electron far inside ($r_j \ll r_i$, $x \to \infty$) screens fully, $s \to 1$.
- An electron far outside ($x \to 0$) does not screen, $s \approx x \to 0$.
- Two electrons at the same radius screen each other by $s = 0.382$.

Each group's effective charge and radius are solved self-consistently, exactly as in the first test:

$$Z_{\mathrm{eff},a} = Z - \sum_{j \ne i} s(r_a, r_{b(j)}), \qquad r_a = \frac{n_a^2\, a_0}{Z_{\mathrm{eff},a}}.$$

- **Groups** (as in Slater's rules): [1s], [2s 2p], [3s 3p], [3d], [4s 4p]. The 3d group has $n = 3$.
- **Configurations:** measured ground states (NIST), including Cr $3d^5 4s^1$ and Cu $3d^{10} 4s^1$.
- **Outermost value** compared with Clementi: the [4s 4p] group for $Z = 19$–36.
- **No fitted parameter.**

## Secondary analyses (pre-registered, reported, not part of the pass/fail)

- **B′:** the same rule with Paper XIII's position-to-acceleration mapping, $x = (r_i/r_j)^2$.
- **Covalent-radius sensitivity:** Mn, Fe and Co with Cordero's low-spin and with high-spin radii instead of their mean.

## Data

- $Z = 1$–20: `data/atomic_reference.csv` (unchanged).
- $Z = 21$–36: `data/atomic_reference_21_36.csv` (sources in `data/SOURCES.md`).

## Baseline

Slater's rules (1930): same group 0.35 (0.30 within 1s), next shell in 0.85, deeper 1.00; d electrons screened 1.00 by everything inside; effective principal numbers $n^* = 1, 2, 3, 3.7$.

## Pass criteria (fixed in advance)

1. **Screening, first 20 elements.** Mean absolute percentage error of the outermost $Z_{\mathrm{eff}}$ against Clementi below **10%**, $Z = 1$–20.
2. **Screening, out of sample.** Mean absolute percentage error against Clementi below **10%** on $Z = 21$–36, **and** lower than Slater's rules on the same elements.
3. **Ordering.** Spearman rank correlation with Clementi's $Z_{\mathrm{eff}}$ of at least **0.95** over $Z = 1$–36.
4. **Radii.** Against Cordero covalent radii, with one scale factor fitted per model, the log-RMS deviation over the non-noble elements of $Z = 1$–36 is **lower than Slater's rules**.

The rule passes only if all four hold. Whatever the outcome, it is reported in the README. If the rule fails, variants may be explored, but they will be labelled exploratory and will not be presented as predictions.
