# Pre-registration: a screening rule from the constitutive law

*Committed before the rule was evaluated. The rule, the data and the pass criteria below are fixed; the evaluation script is written to this specification.*

## Motivation

Every atomic result in this folder takes its effective nuclear charge $Z_{\mathrm{eff}}$ from Clementi's self-consistent-field tables (see the README, *Baselines*). Deriving the screening from GFD's own structure is the step that would make the chain predictive. This document fixes one candidate rule in advance.

## The rule

GFD's constitutive law partitions a field between two sectors as $\mu(x) = x/(x+1)$. Apply it to screening: the fraction of electron $j$'s charge that screens electron $i$ is the constitutive share set by the ratio of their radii,

$$s_{ij} = \mu\!\left(\frac{r_i}{r_j}\right) = \frac{r_i}{r_i + r_j}.$$

- An electron far inside ($r_j \ll r_i$) screens fully, $s \to 1$.
- An electron far outside ($r_j \gg r_i$) does not screen, $s \to 0$.
- Two electrons at the same radius screen each other by $s = \tfrac12$.

Each shell's effective charge and radius are then solved self-consistently:

$$Z_{\mathrm{eff},a} = Z - \sum_{j \ne i} s(r_a, r_{b(j)}), \qquad r_a = \frac{n_a^2\, a_0}{Z_{\mathrm{eff},a}},$$

with $s$ and $p$ electrons of the same principal shell treated as one group, as in Slater's rules, integer $n$, and ground-state configurations for $Z = 1$–20. The rule contains **no fitted parameter**.

## Data

`data/atomic_reference.csv`: Clementi's $Z_{\mathrm{eff}}$ (outermost orbital), and Cordero et al. (2008) covalent radii as an independent empirical scale. Noble gases are excluded from the covalent-radius comparison, as in `baseline_comparison.py`.

## Pass criteria (fixed in advance)

1. **Screening accuracy.** Mean absolute percentage error of the outermost $Z_{\mathrm{eff}}$ against Clementi's values below **10%** across $Z = 1$–20.
2. **Beats the standard rule.** Against the covalent radii, with one scale factor fitted per model, the log-RMS deviation is **lower than Slater's rules** (0.272, non-noble elements, effective $n^*$).
3. **Ordering.** Spearman rank correlation with Clementi's $Z_{\mathrm{eff}}$ of at least **0.95**.

The rule passes only if all three hold. Whatever the outcome, the result is reported in the README. If the rule fails, variants may be explored, but they will be labelled exploratory and will not be presented as predictions.
