# Pre-registration 3: does the breath depend on the field? (SPARC)

*Written and committed before any computation.*

## Hypothesis H_breath

Part XIII reads G's prefactor as (mean capacity of a closure)/(field-free floor) = 17/13, with the closure breathing from the floor 13 to the ceiling 21. Only a Newtonian field reaches 21. In a field of strength x = g_t/a₀ the capacity reaches f(x) = (21x + 13)/(x + 1). If the breath runs only from 13 to f(x), the mean capacity is (13 + f(x))/2, and the effective coupling relative to the laboratory value is

  G_eff/G = (13 + f(x))/34 = (x + 13/17)/(x + 1).

That is 1 in the laboratory (x ~ 10¹¹; the deviation is 3 × 10⁻¹²) and 13/17 in deep MOND.

## The test (fixed in advance)

- **Data:** `papers/letter-radial-acceleration-relation-sparc/supplementary/sparc_rar.csv` (3284 points, 164 galaxies), unchanged.
- **Baseline:** the letter's relation, μ(x) g_t = g_bar with μ = x/(x+1) and a₀ = 1.2 × 10⁻¹⁰ m/s², solved for g_t.
- **H_breath:** μ(x) g_t = g_bar · (x + 13/17)/(x + 1), with x = g_t/a₀ and the same a₀, solved for g_t numerically.
- **Statistic:** residuals r = log₁₀ g_obs − log₁₀ g_pred; report the mean and standard deviation σ for both.
- **Criteria:**
  - **Supported** if σ_H < σ_base − 0.002 dex.
  - **Rejected** if σ_H > σ_base + 0.002 dex.
  - **Undecided** otherwise.

  The mean residual is reported but not used for the decision, since it depends on the stellar mass-to-light ratios.
- No parameter is adjusted. a₀ stays at its conventional value in both.

## What each outcome means

- **Supported:** G's prefactor is field-dependent, and the breath reading predicts structure in the radial acceleration relation beyond μ.
- **Rejected:** the breath is the full 13 → 21 cycle independent of the local field, and 17/13 is a universal constant.
- **Undecided:** SPARC cannot tell. Wide binaries (x ~ 1, where the effect is about 12%) become the decisive test.
