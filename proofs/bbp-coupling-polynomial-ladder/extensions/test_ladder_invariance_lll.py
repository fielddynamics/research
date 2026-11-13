"""Blind test of Theorem 9 (ladder invariance) by lattice reduction.

PREDICTION (fixed before the search, from Lemma 2 and Theorem 9): at period P = 2^m and base 2^(2^(m-1)), for m = 4, 5, 6,
  (a) the lattice of integer relations among pi and the P slot series has rank exactly 2 (one formula for pi, one relation
      among the slots), for coefficients below the search's noise floor;
  (b) every relation's numerator is divisible by (y^2 + 2)(y^2 + 2y + 2) prod_(4<=k<=m) (y^(2^(k-1)) + 2^(2^(k-2)));
  (c) every formula for pi found is a member of the period-8 family, lifted: integrand 16[(y - 1) - r(y^2 - 4y + 2)]/((y^2 - 2)(y^2 - 2y + 2)).
The search does not use the prediction: it reduces the lattice spanned by (e_i, round(10^N v_i)) for v = (pi, S_1, ..., S_P).
Requires fpylll (pip install fpylll cysignals).  Run: python test_ladder_invariance_lll.py
"""
import time
import mpmath
import sympy as sp
from fpylll import IntegerMatrix, LLL

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

y, r = sp.symbols('y r')
for m in (4, 5, 6):
    P, b = 2**m, 2**(2**(m - 1))
    digits = 22 * (P + 1)                                     # noise floor well above 10^20 for the coefficients
    mpmath.mp.dps = digits + 40
    S = [mpmath.nsum(lambda k: 1 / (mpmath.mpf(b)**k * (P * k + j)), [0, mpmath.inf]) for j in range(1, P + 1)]
    vals = [+mpmath.pi] + S
    n = len(vals); scale = mpmath.mpf(10)**digits
    rows = [[1 if i == j else 0 for j in range(n)] + [int(mpmath.nint(vals[i] * scale))] for i in range(n)]
    t = time.time(); M = IntegerMatrix.from_matrix(rows); LLL.reduction(M)
    red = [[M[i, j] for j in range(n + 1)] for i in range(n)]
    size = lambda row: max(abs(x) for x in row[:n])
    # an exact relation's residual, evaluated at the working precision (40 digits beyond the lattice scale), is ~10^-(digits+40);
    # a lattice-noise vector's residual is ~10^-digits
    exact = lambda row: abs(mpmath.fsum(mpmath.mpf(c) * v for c, v in zip(row[:n], vals))) < mpmath.mpf(10)**-(digits + 20)
    genuine = [row[:n] for row in red if exact(row)]
    floor = min(size(row) for row in red if not exact(row))
    biggest = max(size(g) for g in genuine) if genuine else 0
    print(f"period {P} (base 2^{2**(m - 1)}): reduction {time.time() - t:.1f}s, {len(genuine)} exact relations (largest coefficient "
          f"{float(biggest):.1e}), noise floor of the other vectors ~ {float(floor):.1e}")
    check(f"(a) period {P}: the relation lattice has rank exactly 2, far below the noise floor", len(genuine) == 2 and floor > 10**6 * biggest
          and sp.Matrix(genuine).rank() == 2)
    forced = sp.expand((y**2 + 2) * (y**2 + 2 * y + 2) * sp.prod([y**(2**(k - 1)) + 2**(2**(k - 2)) for k in range(4, m + 1)]))
    nums = [sp.expand(b * sum(rel[j + 1] * y**j for j in range(P))) for rel in genuine]
    check(f"(b) period {P}: every relation's numerator is divisible by the forced rungs", all(sp.expand(sp.rem(q, forced, y)) == 0 for q in nums))
    lift = sp.expand(sp.cancel(16 * ((y - 1) - r * (y**2 - 4 * y + 2)) / ((y**2 - 2) * (y**2 - 2 * y + 2)) * (b - y**P)))
    wl = [sp.Poly(lift, y).coeff_monomial(y**j) / b for j in range(P)]
    members = []
    for rel in genuine:
        if rel[0] == 0: continue
        w = [sp.Rational(-rel[j + 1], rel[0]) for j in range(P)]
        sol = sp.solve([w[j] - wl[j] for j in range(P)], r, dict=True)
        members.append(sol[0][r] if sol else None)
    print(f"     formulas for pi found, as members of the lifted family: r = {members}")
    check(f"(c) period {P}: every formula for pi found is a member of the lifted period-8 family", members and None not in members)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
