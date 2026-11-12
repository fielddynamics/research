"""BBP and the coupling polynomial as one cyclotomic family, and how much the slot -> vertex labelling matters.
Exact checks for bbp_cyclotomic_structure.md.  Run: python3 verify_bbp_cyclotomic_and_labelling.py

Part 1: f(K,s) = 1 + sK + K^2 is Phi_3, Phi_4, Phi_6 at K; BBP's integrand is built from Phi_1, Phi_2, Phi_4, Phi_8 in u = y/sqrt2;
        BBP's numerator cancels Phi_4 (the Field Origin polynomial) and one half of Phi_8, and pi comes from the other half.
Part 2: the octahedral reading of BBP (PROOF.md Theorem 3) under all 8! slot -> vertex labellings; the labelling-free selection.
Part 3: why every formula for pi of BBP's type cancels Phi_4 and the 135-degree half (primes 3 and 5); (y - 1) is closure.
"""
import itertools
from fractions import Fraction as Fr
from collections import Counter
import sympy as sp
import mpmath

ok = []
def check(m, c): ok.append(bool(c)); print(("PASS " if c else "FAIL ") + m)

y, u, K = sp.symbols('y u K')
Phi = {n: sp.cyclotomic_poly(n, u) for n in (1, 2, 3, 4, 6, 8)}

print("=== 1. One cyclotomic family")
check("1a. the coupling polynomial's three states are cyclotomic polynomials at K: f(K,+1) = Phi_3(K), f(K,0) = Phi_4(K), "
      "f(K,-1) = Phi_6(K), the cube's planar rotations of order 3, 4, 6; at K = 4: 21, 17, 13",
      all(sp.expand(K**2 + s * K + 1 - Phi[n].subs(u, K)) == 0 for s, n in ((1, 3), (0, 4), (-1, 6)))
      and [Phi[n].subs(u, 4) for n in (3, 4, 6)] == [21, 17, 13])
w = [4, 0, 0, -2, -1, -1, 0, 0]                                    # BBP slot weights, slots 1..8
p = 16 * sum(wj * y**j for j, wj in enumerate(w))                   # S_j = 16 int_0^1 y^(j-1)/(16 - y^8) dy
mpmath.mp.dps = 40
val = mpmath.quad(sp.lambdify(y, p / (16 - y**8), 'mpmath'), [0, 1])
check("1b. BBP is the integral of p(y)/(16 - y^8) over [0,1] (PROOF.md Theorem 2, Step 1), equal to pi to 35 digits",
      abs(val - mpmath.pi) < mpmath.mpf(10)**-35)
den = sp.expand((16 - y**8).subs(y, sp.sqrt(2) * u))
check("1c. in u = y/sqrt2 the denominator is 16 - y^8 = -16 Phi_1 Phi_2 Phi_4 Phi_8(u): the rotations of order 1, 2, 4, 8",
      sp.expand(den + 16 * Phi[1] * Phi[2] * Phi[4] * Phi[8]) == 0)
half_m, half_p = u**2 - sp.sqrt(2) * u + 1, u**2 + sp.sqrt(2) * u + 1
check("1d. Phi_8 splits over Q(sqrt2) into u^2 - sqrt2 u + 1 (poles at 45 and 315 degrees) and u^2 + sqrt2 u + 1 (135 and 225)",
      sp.expand(half_m * half_p - Phi[8]) == 0)
check("1e. BBP's numerator is p = -16 (y - 1)(y^2 + 2)(y^2 + 2y + 2)", sp.expand(p + 16 * (y - 1) * (y**2 + 2) * (y**2 + 2 * y + 2)) == 0)
red = sp.cancel(p / (16 - y**8))
check("1f. it cancels exactly y^2 + 2 = 2 Phi_4(u) (the Field Origin polynomial, poles at +-90 degrees) and y^2 + 2y + 2 = "
      "2 (u^2 + sqrt2 u + 1) (the 135-degree half of Phi_8), leaving 16 (y - 1) / ((y^2 - 2)(y^2 - 2y + 2))",
      sp.simplify(red - 16 * (y - 1) / ((y**2 - 2) * (y**2 - 2 * y + 2))) == 0
      and sp.expand((y**2 + 2).subs(y, sp.sqrt(2) * u) - 2 * Phi[4]) == 0
      and sp.expand((y**2 + 2 * y + 2).subs(y, sp.sqrt(2) * u) - 2 * half_p) == 0)
# partial fractions of what is left: the y^2 - 2 part (poles 0, 180 deg) and the y^2 - 2y + 2 part (poles 45, 315 deg)
pf = sp.apart(red, y, full=False)
parts = pf.as_ordered_terms()
real_part = sum(t for t in parts if sp.Poly(sp.denom(sp.together(t)), y).degree() and
                sp.rem(sp.denom(sp.together(t)), y**2 - 2, y) == 0)
rot_part = sp.simplify(red - real_part)
I1 = mpmath.quad(sp.lambdify(y, real_part, 'mpmath'), [0, 1]); I2 = mpmath.quad(sp.lambdify(y, rot_part, 'mpmath'), [0, 1])
check("1g. pi comes from the 45-degree half of Phi_8: the poles 1 +- i give pi + ln 4 and the poles +-sqrt2 give -ln 4, which cancels it "
      "(PROOF.md Theorem 4, read cyclotomically)",
      abs(I1 + mpmath.log(4)) < 1e-30 and abs(I2 - mpmath.pi - mpmath.log(4)) < 1e-30)
check("1h. the two sets share exactly one member, Phi_4: the coupling polynomial's Field Origin, which BBP's numerator removes",
      {3, 4, 6} & {1, 2, 4, 8} == {4})
check("1i. Phi_8(K) = K^4 + 1 = Phi_4(K^2): the Field Origin one step up the archive's Sierpinski ladder K -> K^2, 257 at K = 4",
      Phi[8].subs(u, 4) == 257 and sp.expand(Phi[8] - Phi[4].subs(u, u**2)) == 0)

print("\n=== 2. The slot -> vertex labelling")
BBP = {1: 4, 2: 0, 3: 0, 4: -2, 5: -1, 6: -1, 7: 0, 8: 0}
A = {1: 8, 2: -8, 3: -4, 4: -8, 5: -2, 6: -2, 7: 1, 8: 0}            # Adamchik-Wagon direction: every formula is BBP + r A
S = lambda wt: mpmath.nsum(lambda k: sum(wt[j] / (8 * k + j) for j in range(1, 9)) / 16**k, [0, mpmath.inf])
check("2a. the family BBP + r A gives pi for every r (A sums to zero as a series)", abs(S(A)) < mpmath.mpf(10)**-30)
check("2b. its weights sum to -15 r, so closure (weights summing to zero) alone selects BBP, with no labelling at all",
      sum(A.values()) == -15 and sum(BBP.values()) == 0)
par = lambda v: bin(v).count('1') % 2
diags = [(0, 7), (1, 6), (2, 5), (3, 4)]
def selecting(phi):
    inv = {v: s for s, v in phi.items()}; out = []
    for d in diags:
        sols = None
        for s in (inv[d[0]], inv[d[1]]):
            if A[s] == 0:
                if BBP[s] == 0: continue
                sols = set(); break
            c = {Fr(-BBP[s], A[s])}; sols = c if sols is None else sols & c
        if not sols or len(sols) != 1: continue
        r = next(iter(sols)); act = [s for s in range(1, 9) if BBP[s] + r * A[s] != 0]
        if len(act) == 4 and sum(BBP[s] + r * A[s] for s in act) == 0 and Counter(par(phi[s]) for s in act) == Counter({0: 2, 1: 2}):
            out.append(d)
    return out
tot = some = one = time_only = 0
for perm in itertools.permutations(range(8)):
    sel = selecting({s: perm[s - 1] for s in range(1, 9)}); tot += 1
    some += bool(sel); one += len(sel) == 1; time_only += sel == [(0, 7)]
print(f"     {tot} labellings: some diagonal selects BBP with the octahedral shape {some}; exactly one diagonal {one}; that one is Kun-Qian {time_only}")
check("2c. over all 8! = 40320 slot -> vertex labellings, 17280 (42.9%) let some body diagonal select BBP with the octahedral shape "
      "(TIME-silent, 4 active slots, 2 + 2, zero sum), 13824 exactly one diagonal, 3456 exactly the Kun-Qian diagonal",
      (tot, some, one, time_only) == (40320, 17280, 13824, 3456))
check("2d. the I Ching place-value labelling (slot j -> vertex j mod 8) selects through the Kun-Qian (TIME) diagonal only",
      selecting({s: s % 8 for s in range(1, 9)}) == [(0, 7)])
check("2e. the Gray-code labelling (consecutive slots one cube edge apart) also selects BBP, through a different diagonal; "
      "reverse place value (j -> -j mod 8) selects none (PROOF.md extension test 07)",
      selecting({s: (s % 8) ^ ((s % 8) >> 1) for s in range(1, 9)}) == [(3, 4)] and selecting({s: (-s) % 8 for s in range(1, 9)}) == [])

print("\n=== 3. Why Phi_4 and the 135-degree half cancel: the primes 3 and 5")
s2 = sp.sqrt(2)
om = lambda n: sp.exp(sp.I * sp.pi * n / 4)                         # pole at y = sqrt2 * omega, omega = e^{i pi n/4}
pairs = [(0, 4), (1, 7), (2, 6), (3, 5)]                           # 0/180, 45/315, 90/270 (Phi_4), 135/225 degrees
prod = [sp.nsimplify(sp.expand(sp.simplify((1 - sp.conjugate(om(m)) / s2) * (1 - sp.conjugate(om(n)) / s2)))) for m, n in pairs]
check("3a. multiplying 1 - conj(omega)/sqrt2 over each conjugate pole pair: 0/180 -> 1/2, 45/315 -> 1/2, 90/270 (Phi_4) -> 3/2, "
      "135/225 -> 5/2; only the Field Origin pair and the 135-degree pair bring in an odd prime (3 and 5)",
      prod == [sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(5, 2)])
Lg = lambda n: mpmath.log(1 - mpmath.exp(-1j * mpmath.pi * n / 4) / mpmath.sqrt(2))
lg2, lu = mpmath.log(2), mpmath.log(1 + mpmath.sqrt(2))
expect = {0: -lu - lg2 / 2, 1: -lg2 / 2 + 1j * mpmath.pi / 4, 2: mpmath.log(mpmath.sqrt(2) + 1j) - lg2 / 2,
          3: mpmath.log(1 + 1j) + mpmath.log(2 - 1j) - lg2, 4: lu - lg2 / 2, 5: mpmath.log(1 - 1j) + mpmath.log(2 + 1j) - lg2,
          6: mpmath.log(mpmath.sqrt(2) - 1j) - lg2 / 2, 7: -lg2 / 2 - 1j * mpmath.pi / 4}
check("3b. the logarithm at each pole (PROOF.md Theorem 2, Step 2): log(sqrt2 +- i) occurs only at the 90 and 270-degree poles and "
      "log(2 -+ i) only at the 135 and 225-degree poles, each at exactly one pole",
      all(abs(Lg(n) - expect[n]) < mpmath.mpf(10)**-35 for n in range(8)))
r = sp.Symbol('r')
a_vec = [A[j] for j in range(1, 9)]
num_r = sp.expand(16 * sum((w[j] + r * a_vec[j]) * y**j for j in range(8)))
quo, rem = sp.div(num_r, sp.expand((y**2 + 2) * (y**2 + 2 * y + 2)), y)
check("3c. so (Baker: those logarithms are independent of pi, log 2, log(1 + sqrt2)) every formula BBP + r a must have zero residue at "
      "those four poles: its numerator is divisible by (y^2 + 2)(y^2 + 2y + 2) for every r", sp.simplify(rem) == 0)
check("3d. the remaining factor is m_r(y) = 16 [r (y^2 - 4y + 2) - (y - 1)], and its y^2 coefficient 16 r is exactly the TIME slot w_7 = r",
      sp.expand(quo - 16 * (r * (y**2 - 4 * y + 2) - (y - 1))) == 0 and sp.expand(num_r).coeff(y, 6) == 16 * r)
check("3e. TIME silence (w_7 = 0) <=> m_r is linear <=> r = 0", sp.solve(sp.Poly(quo, y).coeff_monomial(y**2), r) == [0])
check("3f. closure (weights summing to zero) <=> the numerator vanishes at y = 1 <=> r = 0, leaving m_0 = -16 (y - 1): "
      "BBP's factor (y - 1) is the closure condition",
      sp.solve(num_r.subs(y, 1), r) == [0] and sp.expand(quo.subs(r, 0) + 16 * (y - 1)) == 0)
check("3g. of the poles that remain, only the 45/315-degree pair carries pi: (1 +- i)/2 has argument +-pi/4; the 0/180 pair is real",
      abs(mpmath.im(Lg(0))) < 1e-35 and abs(mpmath.im(Lg(4))) < 1e-35 and abs(mpmath.im(Lg(1)) - mpmath.pi / 4) < 1e-35)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
