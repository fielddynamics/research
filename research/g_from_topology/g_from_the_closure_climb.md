# G from the Closure Climb

*Why the formula takes 21 as an exponent and 17/13 as a ratio · Field Dynamics Research · November 2026*

---

## The question

Newton's constant in GFD is

$$\alpha_G = \frac{G\,m_e^2}{\hbar c} = \frac{17}{13}\,\alpha^{21}, \qquad G = \frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2}\Big(1 + \frac{\alpha}{2\pi}\Big).$$

The three integers are the coupling polynomial $f(K,s) = 1 + sK + K^2$ at $s = -1, 0, +1$, with $K = 4$. [`g_matrix_synthesis.md`](g_matrix_synthesis.md) obtains them as three reads of a graded operator, but its rule for combining them is not derived:
- the $s = +1$ value becomes an exponent;
- the other two become a ratio.

This note asks whether the combination rule follows from field closure: the climb in coupling as one closure reads from the bottom of the stellated octahedron to the top.

---

## 1. The climb

As the closure walk discovers new hexagrams, the notes ([`closure_vortex_synthesis`](../exploratory/i-ching/notes/), [`read_sweep_synthesis.md`](read_sweep_synthesis.md)) let $s$ run from $-1$ to $+1$:

$$s(n) = \frac{n}{32} - 1, \qquad f(n) = 13 + \frac{n}{8}, \qquad n = 0, 1, \ldots, 64 \text{ distinct hexagrams}.$$

| Stage | Hexagrams seen | $s$ | $f$ | Where |
|---|---|---|---|---|
| Start | 0 | −1 | 13 | TetB, the floor |
| Midpoint | 32 | 0 | 17 | the Field Origin |
| Closure | 64 | +1 | 21 | TetA, the ceiling |

Bottom to top is TetB → Field Origin → TetA. That is the TIME axis, from Kun through the centre to Qian. The coupling rises by one unit for every 8 new hexagrams.

## 2. A structural fact: the Field Origin is the average of the closure

Average the coupling over one closure, one term per new hexagram:

$$\langle f \rangle = \frac{1}{65}\sum_{n=0}^{64} f(n) = 17 \quad\text{exactly.}$$

Because $f$ climbs linearly, its average over the whole closure equals its value at the midpoint, the Field Origin. So 17 has two meanings at once:
- the coupling at the Field Origin;
- the mean coupling of a complete closure.

The measure matters:
- Averaged per *step* of an actual walk, the mean is about 19.2, for π's walk and for random digits alike. A walk spends more steps near the end of the climb, hunting for the last hexagrams.
- The geometric and harmonic means (16.8 and 16.7) are not 17 either.

Only the average **per new reading**, per hexagram, gives 17.

## 3. The closure rule

**Closure rule.** One closure climbs from $f_{\text{start}}$ to $f_{\text{end}}$. The gravitational coupling is

$$\alpha_G = \alpha^{\,f_{\text{end}}} \times \frac{\langle f \rangle}{f_{\text{start}}}.$$

1. **Exponent: the depth reached at closure.** The read completes at the top of the climb, $f_{\text{end}} = 21$, and attenuates by one factor of α per level (the folder's one physical assumption).
2. **Prefactor: the mean of the closure over its start.** $\langle f\rangle / f_{\text{start}} = 17/13$ is how much the closure's average read exceeds the TetB scaffold it starts from.

With the values of §1 this is exactly $\tfrac{17}{13}\alpha^{21}$. In this form the formula describes a single closure: its end sets the attenuation, and its average relative to its start sets the prefactor.

## 4. Is the rule forced?

No. Other rules are equally easy to write from the same three stages. Take every rule $\alpha^{E} \times A/B$ with $E, A, B \in \{\text{start}, \text{mean}, \text{end}\} = \{13, 17, 21\}$. That gives 21 rules. Of these, **only one lies within 1% of the measured $\alpha_G$**, and it is the closure rule (`closure_climb_G.py`):

| Rule | Tree level | With $1 + \alpha/2\pi$ |
|---|---|---|
| $\alpha^{\text{end}}\cdot\text{mean}/\text{start}$ | −0.117% | −12.1 ppm |
| the other 20 | more than 1% off | — |

How often would the same 21 rules fit a value of $\alpha_G$ that is not the real one? Over 100,000 fake values, log-uniform across one factor of α:

| Window | Fake values fitted |
|---|---|
| tree level, 0.117% | 0.34% (about 1 in 300) |
| with $1 + \alpha/2\pi$, 22 ppm | 0.004% (about 1 in 25,000) |

Compare the folder's broader search (1,953 formulas $(p/q)\alpha^n$), where 13.7% of fake values are fitted at tree level. **Reducing the menu to the closure's own stages is what would give the result weight.** Only 21 candidates exist, and one fits.

**The caveat, stated plainly.** This rule menu was written after the formula was known. A menu built knowing the answer always contains it, so the rates above are what a *pre-registered* test of the closure rule would carry. They are not evidence now. The same holds for the factor $1 + \alpha/2\pi$, which was identified after the tree-level gap was seen.

## 5. What is derived and what is assumed

| Step | Status |
|---|---|
| $f$ climbs 13 → 17 → 21 over one closure, linearly in new hexagrams | Follows from the notes' definition $s = n/32 - 1$ and the polynomial |
| The mean of the closure equals the Field Origin value, 17 | Exact, for averages per new reading; not for averages per step |
| The exponent is the depth at closure, one α per level | Assumed: the folder's photonic coupling assumption |
| The prefactor is mean over start | Proposed: one of 21 closure-stage rules, and the only one that fits |
| $\hbar c/m_e^2$, and $1 + \alpha/2\pi$ | Not addressed here |

## 6. How this connects to π

The climb runs **along** the TIME axis, from the bottom (Kun, TetB) to the top (Qian, TetA). The BBP formula for π is written **around** it, on four corners of the ring of six children, with both apices silent ([`BOOK_OF_CHANGES_AND_PI.md`](../exploratory/i-ching/BOOK_OF_CHANGES_AND_PI.md); `PROOF.md` §11 in the model repository). The walk that performs the climb is driven by π's digits step by step. The climb's three values belong to the closure of the 64 hexagrams itself, which any well-mixed sequence completes.

So the two results divide the stellated octahedron between them:
- G is read along the axis: floor, origin, ceiling.
- π is written around it.

## 7. What would make it a derivation

1. **Derive the prefactor rule from closure physics,** not from fit. Why should gravity weigh the closure's mean against its start, rather than its end? One candidate: gravity is the interaction *between* the chambers. Read that way, the prefactor is the closure's average relative to the TetB sector it begins in, and the exponent is the full depth into TetA where it completes.
2. **Fix the rule, then use it elsewhere.** Commit the closure rule in advance, apply it to a quantity not yet used, and compare. Any other result of the form $\alpha^{f}$ times a ratio of stages would test it.
3. **Pre-register the G comparison** with the 21-rule menu above, written down before any change to the inputs (for example, a new CODATA value of G).

---

**Run:** `python closure_climb_G.py` (standard library; mpmath optional).
