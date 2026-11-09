# Pre-registered Prediction for G

*Registered 9 November 2026, by the commit that adds this file · Field Dynamics Research*

---

## The prediction

$$G = \frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2}\left(1 + \frac{\alpha}{2\pi}\right) = 6.674219 \times 10^{-11}\ \mathrm{m^3\,kg^{-1}\,s^{-2}}$$

with CODATA 2022 values of $\alpha$ and $m_e$ and the exact values of $\hbar$ and $c$. The inputs carry a relative uncertainty of about $4 \times 10^{-9}$, so the prediction is effectively exact: it is about ten thousand times sharper than the best measurement of G.

The formula is fixed in every part, as described in [`g_from_the_closure_climb.md`](g_from_the_closure_climb.md):

| Part | Fixed as |
|---|---|
| Coupling polynomial | $f(K, s) = 1 + sK + K^2$, $K = 4$: start $f(-1) = 13$, mean $17$, end $f(+1) = 21$ |
| Combination rule | $\alpha^{f_{\text{end}}} \times \langle f \rangle / f_{\text{start}}$ |
| Scale | $\hbar c / m_e^2$ |
| One-loop factor | $1 + \alpha/2\pi$ |

No part may be changed in response to new data. If any part is changed, this registration no longer applies, and the changed formula needs a registration of its own.

## What counts as a test

Only measurements published after the registration date count. For each, record $z = (G_{\text{pred}} - G_{\text{meas}})/\sigma_{\text{meas}}$ using the experiment's own stated uncertainty.

- **A pass:** a new CODATA recommended value, or two independent new measurements each with relative uncertainty below 10 ppm, within 2σ of the prediction.
- **A failure:** two independent new measurements, each below 10 ppm, that agree with each other and both lie more than 3σ from the prediction; or a new CODATA recommended value more than 3σ from it.
- A single new measurement in conflict is recorded but does not decide. Past measurements of G disagree with each other by up to 500 ppm, so one experiment is not enough.

## Status at registration

[`compare_G_measurements.py`](compare_G_measurements.py) compares the prediction with all 16 measurements of the CODATA 2022 adjustment (Table XXX of Mohr et al., arXiv:2409.03787):

| | Result |
|---|---|
| CODATA 2022 recommended value, $6.67430(15)$ | −12 ppm, z = −0.5 |
| Within 1σ of | HUST time-of-swing 2018, Washington 2000, Zurich 2006, UC Irvine 2014 |
| In conflict with | BIPM 2014 (z = −8.3), HUST angular-acceleration 2018 (−3.4), HUST 2009 (+4.1) |

**This agreement is not evidence for the formula.** The combination rule was chosen from a menu written after the formula was known, and the one-loop factor was identified after the tree-level gap was seen against the CODATA value, which these same measurements produce. The registration exists so that the next measurements are a genuine test.

## A second test, not yet possible

A stronger test would apply the same combination rule to a different closure and predict a quantity not yet used. The framework does not yet define a second closure with its own start, mean and end, independent of G: electromagnetism is a single level, and $H_0$, $a_0$ and $m_e$ are derived through G. Defining such a closure is the framework's next step. Choosing one now, knowing the results, would repeat the problem this registration avoids.

---

**Run:** `python compare_G_measurements.py` (standard library only).
