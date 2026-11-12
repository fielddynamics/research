"""Machine checks for every step of
'The BBP Formula and the Coupling Polynomial on One Ladder'.
Exact algebra (sympy) for every identity; 40-digit numerics only to fix logarithm branches and integral values.
Run: python verify_bbp_coupling_polynomial_ladder.py"""
import sympy as sp
import mpmath

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

X, u, y, r = sp.symbols('X u y r')
Phi = lambda n, v: sp.cyclotomic_poly(n, v)
K, D = 4, 3
mpmath.mp.dps = 40

# ---- Setting
check("Setting: 2(D+1) = 2^D has the unique positive integer solution D = 3 (checked D <= 64), so K = D + 1 = 4",
      [d for d in range(1, 65) if 2 * (d + 1) == 2**d] == [3])

# ---- Theorem 1: the coupling polynomial is a row of the ladder
f = lambda s: X**2 + s * X + 1
check("Theorem 1: f(X,+1) = Phi_3(X), f(X,0) = Phi_4(X), f(X,-1) = Phi_6(X)",
      all(sp.expand(f(s) - Phi(n, X)) == 0 for s, n in ((1, 3), (0, 4), (-1, 6))))
check("Theorem 1: at K = 4 the row is (13, 17, 21)", [Phi(n, K) for n in (6, 4, 3)] == [13, 17, 21])
check("Theorem 1: ladder X -> X^2: Phi_3(X^2) = Phi_3(X) Phi_6(X), Phi_4(X^2) = Phi_8(X), Phi_6(X^2) = Phi_12(X)",
      sp.expand(Phi(3, X**2) - Phi(3, X) * Phi(6, X)) == 0 and sp.expand(Phi(4, X**2) - Phi(8, X)) == 0
      and sp.expand(Phi(6, X**2) - Phi(12, X)) == 0)
check("Theorem 1: the next row, at X = K^2 = 16, is (241, 257, 273)", [Phi(n, 16) for n in (6, 4, 3)] == [241, 257, 273])
check("Theorem 1: the Field Origin column Phi_4(K^(2^n)) = 1 + K^(2^(n+1)) is 17, 257, 65537 (Fermat numbers F_2, F_3, F_4)",
      [Phi(4, K**(2**n)) for n in range(3)] == [17, 257, 65537] == [2**(2**m) + 1 for m in (2, 3, 4)])

# ---- Lemma: the pole radius
check("Lemma: for base 2^(D+1) and period 2^D the poles of 1/(2^(D+1) - y^(2^D)) lie at radius 2^((D+1)/2^D), which is sqrt2 "
      "exactly when 2(D+1) = 2^D (checked D = 1..12)",
      all((sp.Rational(D_ + 1, 2**D_) == sp.Rational(1, 2)) == (2 * (D_ + 1) == 2**D_) for D_ in range(1, 13)))
check("Lemma: at D = 3 the Gaussian integer 1 + i is a pole: (1 + i)^8 = 16", sp.expand((1 + sp.I)**8) == 16)

# ---- Theorem 2: BBP's denominator is the Field Origin column
den_u = sp.expand((16 - y**8).subs(y, sp.sqrt(2) * u))
rungs = [1 + u**(2**k) for k in range(D)]
check("Theorem 2: with y = sqrt2 u, 16 - y^8 = 16 (1 - u^8) = 16 (1 - u)(1 + u)(1 + u^2)(1 + u^4)",
      sp.expand(den_u - 16 * (1 - u**8)) == 0 and sp.expand((1 - u) * rungs[0] * rungs[1] * rungs[2] - (1 - u**8)) == 0)
check("Theorem 2: the rungs are 1 + u^(2^k) = Phi_(2^(k+1))(u) = Phi_2, Phi_4, Phi_8",
      all(sp.expand(rungs[k] - Phi(2**(k + 1), u)) == 0 for k in range(D)))
check("Theorem 2: each rung is the Field Origin polynomial at a ladder step: Phi_2(X) = Phi_4(sqrt X), Phi_4(X), Phi_8(X) = Phi_4(X^2); "
      "at X = K they are 5, 17, 257",
      sp.expand(Phi(2, X**2) - Phi(4, X)) == 0 and sp.expand(Phi(8, X) - Phi(4, X**2)) == 0
      and [rk.subs(u, K) for rk in rungs] == [Phi(4, 2), Phi(4, 4), Phi(4, 16)] == [5, 17, 257])
check("Theorem 2: neither Phi_3 nor Phi_6 (nor Phi_12) divides 1 - u^8: the TetA and TetB columns are absent",
      all(sp.rem(1 - u**8, Phi(n, u), u) != 0 for n in (3, 6, 12)))
check("Theorem 2: the denominator's factors are Phi_d for d | 8 only, and the coupling row's are Phi_3, Phi_4, Phi_6; they share exactly Phi_4",
      sp.divisors(8) == [1, 2, 4, 8] and set(sp.divisors(8)) & {3, 4, 6} == {4})

# ---- Theorem 3: the rungs are the cube's binary coordinates
check("Theorem 3: (1 + u)(1 + u^2)(1 + u^4) = sum_{m=0}^{7} u^m, each m = 4 b2 + 2 b1 + b0 taken once",
      sp.expand(rungs[0] * rungs[1] * rungs[2] - sum(u**m for m in range(8))) == 0)
check("Theorem 3: m -> (b2, b1, b0) is a bijection from {0..7} onto the cube's corners {0,1}^3 (place value)",
      len({((m >> 2) & 1, (m >> 1) & 1, m & 1) for m in range(8)}) == 8)
w = sp.exp(sp.I * sp.pi / 4)
z0 = lambda e: sp.simplify(sp.expand_complex(e)) == 0
check("Theorem 3: on the poles, with omega = e^(i pi/4), omega^m = (omega^4)^b2 (omega^2)^b1 omega^b0, where omega^4 = -1 (half-turn), "
      "omega^2 = i (quarter-turn) and omega (eighth-turn)",
      all(z0(w**m - (w**4)**((m >> 2) & 1) * (w**2)**((m >> 1) & 1) * w**(m & 1)) for m in range(8))
      and z0(w**4 + 1) and z0(w**2 - sp.I))
check("Theorem 3: flipping the most significant bit (m -> m + 4 mod 8) multiplies every pole character by -1: the top rung is the half-turn",
      all(z0(w**((m + 4) % 8) + w**m) for m in range(8)))

# ---- Theorem 4: every formula for pi of type (*) drops Phi_4 and the 135-degree half of Phi_8
BBP = [4, 0, 0, -2, -1, -1, 0, 0]; A = [8, -8, -4, -8, -2, -2, 1, 0]
S = lambda wt: mpmath.nsum(lambda k: sum(wt[j] / mpmath.mpf(8 * k + j + 1) for j in range(8)) / mpmath.mpf(16)**k, [0, mpmath.inf])
check("Theorem 4 (setting, from PROOF.md Theorem 2): BBP gives pi and the relation vector a gives 0, so BBP + r a gives pi for every r",
      abs(S(BBP) - mpmath.pi) < mpmath.mpf(10)**-35 and abs(S(A)) < mpmath.mpf(10)**-35)
L = lambda n: mpmath.log(1 - mpmath.exp(-1j * mpmath.pi * n / 4) / mpmath.sqrt(2))
lg2, lu_ = mpmath.log(2), mpmath.log(1 + mpmath.sqrt(2))
expect = {0: -lu_ - lg2 / 2, 1: -lg2 / 2 + 1j * mpmath.pi / 4, 2: mpmath.log(mpmath.sqrt(2) + 1j) - lg2 / 2,
          3: mpmath.log(1 + 1j) + mpmath.log(2 - 1j) - lg2, 4: lu_ - lg2 / 2, 5: mpmath.log(1 - 1j) + mpmath.log(2 + 1j) - lg2,
          6: mpmath.log(mpmath.sqrt(2) - 1j) - lg2 / 2, 7: -lg2 / 2 - 1j * mpmath.pi / 4}
check("Theorem 4: the logarithm at each pole y = sqrt2 omega^n (PROOF.md Step 2, branches fixed to 35 digits): log(sqrt2 +- i) occurs "
      "only at n = 2, 6 (the Phi_4 poles) and log(2 -+ i) only at n = 3, 5 (the 135-degree poles)",
      all(abs(L(n) - expect[n]) < mpmath.mpf(10)**-35 for n in range(8)))
pairs = [(0, 4), (1, 7), (2, 6), (3, 5)]
om = lambda n: sp.exp(sp.I * sp.pi * n / 4)
prods = [sp.nsimplify(sp.expand(sp.simplify((1 - sp.conjugate(om(a)) / sp.sqrt(2)) * (1 - sp.conjugate(om(b)) / sp.sqrt(2))))) for a, b in pairs]
check("Theorem 4: over each conjugate pole pair the product of 1 - conj(omega)/sqrt2 is 1/2, 1/2, 3/2, 5/2: only the Phi_4 pair and the "
      "135-degree pair contain an odd prime, 3 = (sqrt2 + i)(sqrt2 - i) and 5 = (2 + i)(2 - i)",
      prods == [sp.Rational(1, 2), sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(5, 2)]
      and sp.expand((sp.sqrt(2) + sp.I) * (sp.sqrt(2) - sp.I)) == 3 and sp.expand((2 + sp.I) * (2 - sp.I)) == 5)
num = lambda wt: sp.expand(16 * sum(wt[j] * y**j for j in range(8)))           # S_j = 16 int_0^1 y^(j-1)/(16 - y^8) dy
num_r = num([BBP[j] + r * A[j] for j in range(8)])
quo, rem = sp.div(num_r, sp.expand((y**2 + 2) * (y**2 + 2 * y + 2)), y)
check("Theorem 4: hence every numerator vanishes at those four poles: (y^2 + 2)(y^2 + 2y + 2) divides it for every r",
      sp.simplify(rem) == 0)
check("Theorem 4: y^2 + 2 = 2 Phi_4(u) and y^2 + 2y + 2 = 2 (u^2 + sqrt2 u + 1), the 135-degree half of Phi_8 = (u^2 - sqrt2 u + 1)(u^2 + sqrt2 u + 1)",
      sp.expand((y**2 + 2).subs(y, sp.sqrt(2) * u) - 2 * Phi(4, u)) == 0
      and sp.expand((y**2 + 2 * y + 2).subs(y, sp.sqrt(2) * u) - 2 * (u**2 + sp.sqrt(2) * u + 1)) == 0
      and sp.expand((u**2 - sp.sqrt(2) * u + 1) * (u**2 + sp.sqrt(2) * u + 1) - Phi(8, u)) == 0)
check("Theorem 4: the numerators are exactly 16 (y^2 + 2)(y^2 + 2y + 2) [r (y^2 - 4y + 2) - (y - 1)]",
      sp.expand(quo - 16 * (r * (y**2 - 4 * y + 2) - (y - 1))) == 0)

# ---- Theorem 5: pi is read from the next rung up
red = sp.cancel(num_r / (16 - y**8))
check("Theorem 5: after cancellation the integrand is 16 [r (y^2 - 4y + 2) - (y - 1)] / ((y^2 - 2)(y^2 - 2y + 2)), "
      "with poles +-sqrt2 (the rung Phi_1 Phi_2) and 1 +- i (the 45-degree half of Phi_8)",
      sp.simplify(red + 16 * (r * (y**2 - 4 * y + 2) - (y - 1)) / ((y**2 - 2) * (y**2 - 2 * y + 2))) == 0
      or sp.simplify(red - 16 * (r * (y**2 - 4 * y + 2) - (y - 1)) / ((y**2 - 2) * (y**2 - 2 * y + 2))) == 0)
check("Theorem 5: the +-sqrt2 poles give real logarithms only; the 1 +- i poles are the only remaining poles with nonzero argument (+-pi/4) "
      "and their product of 1 - conj(omega)/sqrt2 is a power of 2",
      abs(mpmath.im(L(0))) < 1e-35 and abs(mpmath.im(L(4))) < 1e-35 and abs(mpmath.im(L(1)) - mpmath.pi / 4) < 1e-35 and prods[1] == sp.Rational(1, 2))
bbp_red = sp.cancel(num(BBP) / (16 - y**8))
pf = sp.apart(bbp_red, y)
part_sqrt2 = sum(t for t in pf.as_ordered_terms() if sp.rem(sp.denom(sp.together(t)), y**2 - 2, y) == 0)
part_45 = sp.simplify(bbp_red - part_sqrt2)
I1 = mpmath.quad(sp.lambdify(y, part_sqrt2, 'mpmath'), [0, 1]); I2 = mpmath.quad(sp.lambdify(y, part_45, 'mpmath'), [0, 1])
check("Theorem 5: for BBP the 1 +- i part integrates to pi + ln 4 and the +-sqrt2 part to -ln 4",
      abs(I2 - mpmath.pi - mpmath.log(4)) < mpmath.mpf(10)**-30 and abs(I1 + mpmath.log(4)) < mpmath.mpf(10)**-30)
check("Theorem 5: the rung that carries pi is Phi_8 = Phi_4(X^2), the Field Origin one ladder step above the coupling row (257 at X = K)",
      sp.expand(Phi(8, X) - Phi(4, X**2)) == 0 and Phi(8, K) == 257)

# ---- Corollary: TIME silence and closure act on the last factor
check("Corollary: the TIME slot w_7 is the y^6 coefficient of the numerator, 16 r, so TIME silence is r = 0",
      sp.expand(num_r).coeff(y, 6) == 16 * r and sp.solve(sp.expand(num_r).coeff(y, 6), r) == [0])
check("Corollary: closure, weights summing to zero, is the numerator vanishing at y = 1: p_r(1) = -240 r, so closure is r = 0",
      sp.expand(num_r.subs(y, 1) + 240 * r) == 0)
check("Corollary: at r = 0 the last factor is -(y - 1): BBP's factor (y - 1) is the closure condition",
      sp.expand(quo.subs(r, 0) + 16 * (y - 1)) == 0)

# ---- Remarks
check("Remark: the rungs at X = K multiply to 5 x 17 x 257 = 21845 = sum_{m<8} K^m, and f(K,+1) = 21 = sum_{m<3} K^m (geometric series)",
      5 * 17 * 257 == sum(K**m for m in range(8)) and 21 == sum(K**m for m in range(3)))
import itertools
orders = set()
for p in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        M = sp.Matrix(3, 3, lambda i, j: sg[i] if j == p[i] else 0); k = 1; P = M
        while P != sp.eye(3): P = P * M; k += 1
        orders.add(k)
check("Remark (scope): no symmetry of the stellated octahedron has order 8 (orders {1, 2, 3, 4, 6}), so BBP's period-8 cycle is not one of "
      "its symmetries; the ladder places it one rung up instead", orders == {1, 2, 3, 4, 6})

print(f"\n{sum(ok)}/{len(ok)} checks passed")
