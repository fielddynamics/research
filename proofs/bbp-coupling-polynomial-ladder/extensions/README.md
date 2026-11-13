# Extensions

*Independent tests of the proof's theorems, by methods that do not use the proof*

The main script, [`../verify_bbp_coupling_polynomial_ladder.py`](../verify_bbp_coupling_polynomial_ladder.py), checks every step of the proof with exact algebra. The tests here check the same claims a different way: they search for the answer without being told it, after the answer has been written down as a prediction.

| Test | What it checks | Result |
|---|---|---|
| [`test_ladder_invariance_lll.py`](test_ladder_invariance_lll.py) | Theorem 9 (ladder invariance), blind, at periods 16, 32 and 64 (bases 2⁸, 2¹⁶, 2³²) | 9/9 |

## The ladder-invariance test

**The prediction.** It is written in the file's header before the search runs. At each period:
- (a) the integer relations among π and the slot series form a lattice of rank exactly 2: one formula for π and one relation among the slots;
- (b) every relation's numerator is divisible by the forced rungs: the Field Origin's y² + 2, the 135° half y² + 2y + 2, and each new rung y^(2^(k−1)) + 2^(2^(k−2));
- (c) every formula for π found belongs to the period-8 family, lifted.

**The search.** It doesn't use the prediction. It reduces the lattice spanned by (eᵢ, round(10^N vᵢ)), for v = (π, S₁, …, S_P), with fplll. A reduced vector counts as an exact relation when its residual, evaluated 40 digits beyond the lattice scale, vanishes.

**What it found:**

| Period | Exact relations | Their largest coefficient | Next vectors of the lattice | Formulas for π, as members of the lifted family |
|---|---|---|---|---|
| 16 | 2 | about 10² | about 10²⁴ | r = 0 (BBP), r = −1/2 |
| 32 | 2 | about 10⁴ | about 10²² | r = 0, r = −1/3 |
| 64 | 2 | about 10⁹ | about 10²² | r = 0, r = −1/2 |

So climbing the ladder adds no formula for π. The two genuine relations are always members of the period-8 family, lifted, and nothing else exists with coefficients anywhere near the size of the genuine ones.

```bash
pip install fpylll cysignals sympy mpmath
python test_ladder_invariance_lll.py      # 9/9
```
