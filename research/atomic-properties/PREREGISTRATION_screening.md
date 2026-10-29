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

---

## Outcome (added after evaluation)

Evaluated by [`screening_from_mu.py`](screening_from_mu.py) after this document was committed (commit `12f6f38`).

| Criterion | Threshold | Result | Verdict |
|---|---|---|---|
| 1. Mean error of outermost $Z_{\mathrm{eff}}$ vs Clementi | below 10% | 10.5% (Slater's rules: 7.1%) | **fail** |
| 2. Covalent-radius log-RMS vs Slater's rules | below 0.272 | 0.194 | pass |
| 3. Rank correlation with Clementi $Z_{\mathrm{eff}}$ | at least 0.95 | 0.991 | pass |

**The rule fails the pre-registered test**, narrowly, on criterion 1. Its effective charges are systematically low: the same-shell screening $s = \tfrac12$ is stronger than the standard 0.35, so $Z_{\mathrm{eff}}$ falls short by up to about 18% in the second row.

**Secondary analysis, not pre-registered.** Against the independent covalent radii, the rule's radii track the measured shape better than Slater's rules (log-RMS 0.194 against 0.272) and better than radii built from Clementi's own $Z_{\mathrm{eff}}$ (0.221). In 10,000 bootstrap resamples of the 17 non-noble elements, the rule is lower than Clementi-based radii in 96.8% and lower than Slater's in 100%. This is a single metric on a small sample, with one fitted scale factor per model, and it was not the pre-registered primary test. It is a lead worth testing on a pre-registered extension (for example $Z = 21$–36 against measured radii), not a result.

No variant of the rule has been tried. Any variant will be labelled exploratory.
