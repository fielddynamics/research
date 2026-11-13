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
check("Theorem 5: after cancellation the integrand is 16 [(y - 1) - r (y^2 - 4y + 2)] / ((y^2 - 2)(y^2 - 2y + 2)), "
      "with poles +-sqrt2 (the rung Phi_1 Phi_2) and 1 +- i (the 45-degree half of Phi_8)",
      sp.simplify(red - 16 * ((y - 1) - r * (y**2 - 4 * y + 2)) / ((y**2 - 2) * (y**2 - 2 * y + 2))) == 0)
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

# ======================================================================== Part II
# ---- Theorem 6: the rung dictionary (exact, through the residue expansion with PROOF.md's logarithms)
J, L2s, Lus, Lps, Lms, Aps, Ams = sp.symbols('J L2 Lu Lp Lm Ap Am')   # J = i pi; Lp, Lm = log(2 +- i); Ap, Am = log(sqrt2 +- i)
Lw = {0: -Lus - L2s / 2, 1: -L2s / 2 + J / 4, 2: Aps - L2s / 2, 3: Lms - L2s / 2 + J / 4,
      4: Lus - L2s / 2, 5: Lps - L2s / 2 - J / 4, 6: Ams - L2s / 2, 7: -L2s / 2 - J / 4}
omx = [sp.expand_complex(sp.exp(sp.I * sp.pi * n / 4)) for n in range(8)]
def value(wt):
    return sp.expand(sum(-sp.Rational(1, 8) * sp.expand_complex(sp.expand(sum(wt[j - 1] * (sp.sqrt(2) * omx[n])**j for j in range(1, 9)))) * Lw[n]
                         for n in range(8)))
def same(e1, e2):
    d = sp.expand(e1 - e2)
    return all(sp.simplify(sp.expand_complex(d.coeff(t))) == 0 for t in (J, L2s, Lus, Lps, Lms, Aps, Ams))
DICT = {  # constant: (exact target in the seven logarithms, one formula w_c)
    "pi": (-sp.I * J, [4, 0, 0, -2, -1, -1, 0, 0]),
    "ln 2": (L2s, [1, 0, sp.Rational(-1, 2), sp.Rational(-1, 2), sp.Rational(-1, 4), 0, sp.Rational(1, 8), sp.Rational(1, 8)]),
    "ln 3": (Aps + Ams, [0, 2, 0, 0, 0, sp.Rational(1, 2), 0, 0]),
    "ln 5": (Lps + Lms, [2, 0, -1, 0, sp.Rational(-1, 2), 0, sp.Rational(1, 4), 0]),
    "arctan(1/2)": ((Lps - Lms) / (2 * sp.I), [0, 1, 0, 0, 0, sp.Rational(-1, 4), 0, 0]),
    "sqrt2 ln(1+sqrt2)": (sp.sqrt(2) * Lus, [0, 1, 1, 1, sp.Rational(1, 2), sp.Rational(1, 4), 0, 0]),
    "sqrt2 arctan(1/sqrt2)": (sp.sqrt(2) * (Aps - Ams) / (2 * sp.I), [0, 1, 0, 1, sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(-1, 4), 0]),
}
check("Theorem 6: the logarithm expansion reproduces the relation (a gives 0) and each of the seven formulas gives its constant exactly",
      same(value(A), 0) and all(same(value(wc), tgt) for tgt, wc in DICT.values()))
PAIRS = {"0/180": y**2 - 2, "45/315": y**2 - 2 * y + 2, "90/270": y**2 + 2, "135/225": y**2 + 2 * y + 2}
def status(wc, fac):
    numr = sp.expand(16 * sum((wc[j] + r * A[j]) * y**j for j in range(8)))
    rm = sp.expand(sp.rem(numr, sp.expand(fac), y))
    if rm == 0: return "dropped"
    sol = sp.solve(sp.Poly(rm, y).coeffs(), r, dict=True)
    return "one member drops it" if sol else "used"
table = {c: tuple(status(wc, f) for f in PAIRS.values()) for c, (tgt, wc) in DICT.items()}
expected = {"pi": ("one member drops it", "used", "dropped", "dropped"),
            "ln 2": ("one member drops it", "one member drops it", "dropped", "dropped"),
            "ln 3": ("one member drops it", "one member drops it", "used", "dropped"),
            "ln 5": ("one member drops it", "one member drops it", "dropped", "used"),
            "arctan(1/2)": ("one member drops it", "used", "dropped", "used"),
            "sqrt2 ln(1+sqrt2)": ("used", "one member drops it", "dropped", "dropped"),
            "sqrt2 arctan(1/sqrt2)": ("one member drops it", "one member drops it", "used", "dropped")}
for c in table: print(f"     {c:22s} 0/180: {table[c][0]:20s} 45/315: {table[c][1]:20s} 90/270 (Phi4): {table[c][2]:20s} 135/225: {table[c][3]}")
check("Theorem 6: the dictionary. The Field Origin pair (90/270) is used by ln 3 and sqrt2 arctan(1/sqrt2) and dropped by every other "
      "constant; the 135-degree pair is used by ln 5 and arctan(1/2); the 45-degree pair by pi and arctan(1/2); the 0/180 pair by "
      "sqrt2 ln(1+sqrt2); every other entry is dropped by exactly one member of the family", table == expected)

# ---- Theorem 7: pi on one rung
wq = [BBP[j] - sp.Rational(1, 4) * A[j] for j in range(8)]
check("Theorem 7: the member r = -1/4 is (2, 2, 1, 0, -1/2, -1/2, -1/4, 0), the base -4 formula "
      "pi = sum (-1/4)^k [2/(4k+1) + 2/(4k+2) + 1/(4k+3)] written with base 16 and period 8",
      wq == [2, 2, 1, 0, sp.Rational(-1, 2), sp.Rational(-1, 2), sp.Rational(-1, 4), 0]
      and abs(mpmath.nsum(lambda k: (-mpmath.mpf(1) / 4)**k * (2 / (4 * k + 1) + mpmath.mpf(2) / (4 * k + 2) + mpmath.mpf(1) / (4 * k + 3)),
                          [0, mpmath.inf]) - mpmath.pi) < mpmath.mpf(10)**-35)
bracket = (y - 1) - r * (y**2 - 4 * y + 2)
check("Theorem 7: it is the only member with no poles at +-sqrt2: the bracket (y - 1) - r (y^2 - 4y + 2) vanishes at both +-sqrt2 "
      "exactly when r = -1/4", sp.solve([bracket.subs(y, sp.sqrt(2)), bracket.subs(y, -sp.sqrt(2))], r, dict=True) == [{r: sp.Rational(-1, 4)}])
check("Theorem 7: its integrand is 4/(y^2 - 2y + 2), whose integral is 4 arctan 1 = pi; its natural denominator 4 + y^4 = 4 Phi_8(u) "
      "is a single rung, and its numerator 4 (y^2 + 2y + 2) removes the 135-degree half",
      sp.simplify(sp.cancel(num(wq) / (16 - y**8)) - 4 / (y**2 - 2 * y + 2)) == 0
      and sp.integrate(4 / (y**2 - 2 * y + 2), (y, 0, 1)) == sp.pi
      and sp.expand((4 + y**4).subs(y, sp.sqrt(2) * u) - 4 * Phi(8, u)) == 0
      and sp.expand(4 * (y**2 + 2 * y + 2) * (y**2 - 2 * y + 2) - 4 * (4 + y**4)) == 0)

# ---- Lemma 2 and Theorem 8: rung norms are the Field Origin column (Fermat numbers)
def pole_alpha(n, k, t):            # sigma_t applied to 1 - conj(omega)/sqrt2, omega = zeta_(2^k)^n, sqrt2 = zeta_8 + zeta_8^-1
    z = mpmath.exp(2j * mpmath.pi * t / 2**k)
    return 1 - z**(-n) / (z**(2**(k - 3)) + z**(-2**(k - 3)))
mpmath.mp.dps = 50
def orbit_and_norm(n, k):
    vals = [pole_alpha(n, k, t) for t in range(1, 2**k, 2)]
    idx = set()
    for v in vals:                  # identify each conjugate with the pole whose alpha it equals
        for m in range(2**k):
            if abs(v - pole_alpha(m, k, 1)) < 1e-40: idx.add(m)
    N = mpmath.fprod(vals)
    return idx, sp.nsimplify(float(mpmath.re(N)), rational=True, tolerance=1e-12)
lemma_ok = True
for k in (4, 5, 6):
    prim = {n for n in range(2**k) if n % 2 == 1}
    for n in (1, 3):
        idx, Nr = orbit_and_norm(n, k)
        lemma_ok &= idx == prim and Nr == sp.Rational(2**(2**(k - 2)) + 1, 2**(2**(k - 2)))
check("Lemma 2: for k = 4, 5, 6 the 2^(k-1) poles of the rung Phi_(2^k) form one Galois orbit, and the norm of 1 - conj(omega)/sqrt2 "
      "is Phi_(2^k)(1/sqrt2) = 1 + 2^(-2^(k-2)): 17/16, 257/256, 65537/65536", lemma_ok)
idx3, _ = orbit_and_norm(1, 3)
check("Lemma 2: at k = 3 the orbit of the 45-degree pole is only {45, 315} degrees (sqrt2 changes sign under half the Galois group), "
      "which is why Phi_8 splits into its two halves", idx3 == {1, 7})
check("Theorem 8: Phi_(2^k)(1/sqrt2) * 2^(2^(k-2)) = F_(k-2) = Phi_4(K^(2^(k-4))) for k = 2..6: 3, 5, 17, 257, 65537, the Field Origin "
      "column at X = K^(1/4), K^(1/2), K, K^2, K^4; the rung Phi_16 carries f(K,0) = 17",
      all(Phi(2**k, 1 / sp.sqrt(2)) * 2**(2**(k - 2)) == 2**(2**(k - 2)) + 1 == sp.expand(Phi(4, sp.Integer(4)**sp.Rational(2**k, 16)))
          for k in range(2, 7)) and Phi(16, 1 / sp.sqrt(2)) * 16 == Phi(4, K) == 17)
check("Theorem 8 (remark): at the Field Origin column's level -1 the value is K + 1 for every K (Phi_4(sqrt X) = X + 1); at level -2 it "
      "is sqrt K + 1, which equals D = K - 1 only at K = 4",
      sp.expand(Phi(4, sp.sqrt(X)) - (X + 1)) == 0 and sp.solve(sp.sqrt(X) + 1 - (X - 1), X) == [4])

# ---- Theorem 9: ladder invariance
check("Theorem 9 (step): every prime factor of F_j is 1 mod 2^(j+2) (Euler-Lucas), checked for j = 2..5, including 641 and 6700417 | F_5",
      all(p % 2**(j + 2) == 1 for j in range(2, 6) for p in sp.factorint(2**(2**j) + 1)))
check("Theorem 9 (step): F_2 = 17, F_3 = 257, F_4 = 65537 are prime, so the rungs Phi_16, Phi_32, Phi_64 each carry a prime to the first "
      "power; the Fermat numbers are pairwise coprime", all(sp.isprime(2**(2**j) + 1) for j in (2, 3, 4))
      and all(sp.gcd(2**(2**i) + 1, 2**(2**j) + 1) == 1 for i in range(6) for j in range(i)))
check("Theorem 9 (step): a prime p = 1 mod 2^k splits completely in Q(zeta_(2^k)) (its order mod 2^k is 1): 17 for k = 4, 257 for k = 5, "
      "65537 for k = 6", all(pow(p, 1, 2**k) == 1 for p, k in ((17, 4), (257, 5), (65537, 6))))
def lifted_numerator(m):
    P_, b_ = 2**m, 2**(2**(m - 1))
    return sp.expand(sp.cancel(16 * ((y - 1) - r * (y**2 - 4 * y + 2)) / ((y**2 - 2) * (y**2 - 2 * y + 2)) * (b_ - y**P_))), P_, b_
inv_ok = True
for m in (4, 5, 6):
    numm, P_, b_ = lifted_numerator(m)
    forced = sp.expand((y**2 + 2) * (y**2 + 2 * y + 2) * sp.prod([y**(2**(k - 1)) + 2**(2**(k - 2)) for k in range(4, m + 1)]))
    inv_ok &= sp.degree(numm, y) <= P_ - 1 and sp.expand(sp.rem(numm, forced, y)) == 0
    inv_ok &= sp.expand((b_ - y**P_) + (y**2 - 2) * (y**2 - 2 * y + 2) * forced) == 0
check("Theorem 9: at periods 16, 32 and 64 (bases 2^8, 2^16, 2^32) the denominator is -(y^2 - 2)(y^2 - 2y + 2) times the forced factors "
      "(y^2 + 2)(y^2 + 2y + 2) prod_(4<=k<=m) (y^(2^(k-1)) + 2^(2^(k-2))), and the lifted period-8 family fits with numerator degree < period: "
      "the formulas for pi are the same one-parameter family at every level", inv_ok)
mpmath.mp.dps = 40
S16 = [mpmath.nsum(lambda k: 1 / (mpmath.mpf(256)**k * (16 * k + j)), [0, mpmath.inf]) for j in range(1, 17)]
n16, _, _ = lifted_numerator(4)
w16 = [sp.Poly(n16.subs(r, 0), y).coeff_monomial(y**j) / 256 for j in range(16)]
check("Theorem 9: the lifted BBP at period 16 is pi = sum_k 256^-k [4/(16k+1) - 2/(16k+4) - 1/(16k+5) - 1/(16k+6) + 1/4/(16k+9) - 1/8/(16k+12) "
      "- 1/16/(16k+13) - 1/16/(16k+14)], i.e. BBP with its terms paired", abs(sum(float(w16[j]) * S16[j] for j in range(16)) - mpmath.pi) < 1e-30
      and w16 == [4, 0, 0, -2, -1, -1, 0, 0, sp.Rational(1, 4), 0, 0, sp.Rational(-1, 8), sp.Rational(-1, 16), sp.Rational(-1, 16), 0, 0])


# ======================================================================
# Part III: the octahedral derivation of BBP
import itertools, random
corners = list(itertools.product((-1, 1), repeat=3))
TA = [c for c in corners if c[0] * c[1] * c[2] == 1]
TB = [c for c in corners if c[0] * c[1] * c[2] == -1]
# a regular tetrahedron with vertices v in a set T is {x : -v.x <= 1 for every v in T}
planes = lambda T: {tuple(-ci for ci in v) for v in T}
check("Theorem 10: TetA ∩ TetB is cut out by the 8 planes ±x ± y ± z <= 1, i.e. it is the core octahedron |x| + |y| + |z| <= 1, "
      "whose 6 vertices are the cube's face centres and whose centre is the Field Origin",
      planes(TA) | planes(TB) == set(corners) and not planes(TA) & planes(TB))
inA = lambda p: all(sum(n * x for n, x in zip(v, p)) <= 1 for v in planes(TA))
inB = lambda p: all(sum(n * x for n, x in zip(v, p)) <= 1 for v in planes(TB))
mids = [m for m in itertools.product((-1, 0, 1), repeat=3) if sorted(map(abs, m)) == [0, 1, 1]]
l1 = lambda p, c: sum(abs(a - b) for a, b in zip(p, c))
random.seed(7)
pts = [tuple(sp.Rational(random.randint(-10**4, 10**4), 10**4) for _ in range(3)) for _ in range(20000)]
check("Theorem 10: inside the cube, the points outside the star are exactly the points inside one of 12 unit octahedra centred at the "
      "cube-edge midpoints (exact rational arithmetic on 20,000 random points)",
      len(mids) == 12 and all((not (inA(p) or inB(p))) == any(l1(p, m) < 1 for m in mids) for p in pts if not any(l1(p, m) == 1 for m in mids)))
check("Theorem 10: volumes agree exactly: cube 8 = star 4 (2·8/3 − 4/3) + 12 quarter-octahedra of 1/3 each",
      8 == 2 * sp.Rational(8, 3) - sp.Rational(4, 3) + 12 * sp.Rational(4, 3) / 4)
check("Theorem 10: so in the tiling by cubes the neighbouring octahedra are congruent to the core; each sits on a cube edge, the "
      "midpoint of exactly one TetA corner and one TetB corner (a vector link); the 12 are the core's nearest neighbours in the lattice "
      "of octahedron centres (even coordinate sum)",
      all(sum(1 for a in TA for b in TB if all(sp.Rational(x + z, 2) == w for x, z, w in zip(a, b, m))) == 1 for m in mids)
      and sorted(m for m in itertools.product((-2, -1, 0, 1, 2), repeat=3) if sum(m) % 2 == 0 and 0 < sum(x * x for x in m) <= 2) == sorted(mids))
plane_mids = [sp.Integer(m[0]) + sp.I * m[1] for m in mids if m[2] == 0]
check("Theorem 10: in the mirror plane z = 0 (coordinate y = x1 + i x2) the core's vertices are ±1, ±i and its 4 in-plane neighbours "
      "are centred at ±1 ± i, the roots of y^4 + 4 = 4 Phi_8(u), the four poles of BBP on the rung Phi_8",
      sp.expand(sp.prod([y - c for c in plane_mids]) - (y**4 + 4)) == 0
      and sp.expand((y**4 + 4).subs(y, sp.sqrt(2) * u) - 4 * Phi(8, u)) == 0
      and sp.expand(sp.rem(16 - y**8, y**4 + 4, y)) == 0)
check("Theorem 10: BBP's other four poles ±sqrt2, ±i sqrt2 are not lattice points; they are the neighbour centres turned by 45 degrees, "
      "which is not a symmetry of the cube",
      all(sp.simplify(sp.expand_complex(c * sp.exp(sp.I * sp.pi / 4))) in (sp.sqrt(2), -sp.sqrt(2), sp.sqrt(2) * sp.I, -sp.sqrt(2) * sp.I)
          for c in plane_mids))
# Theorem 11: the angles
allpoles = [sp.sqrt(2) * sp.exp(sp.I * sp.pi * n / 4) for n in range(8)]
def tan2(p):                         # exact tan^2 of the angle at p subtended by the segment [0, 1]
    z = sp.expand_complex(sp.conjugate(-p) * (1 - p))
    re_, im_ = sp.simplify(sp.re(z)), sp.simplify(sp.im(z))
    return sp.nsimplify(sp.simplify(im_**2 / re_**2)) if re_ != 0 else sp.oo
t2 = [tan2(sp.expand_complex(p)) for p in allpoles]
check("Theorem 11: integral_0^1 dy/(y - p) = Log(1 - 1/p), whose argument is the angle at p subtended by the walk from the Field Origin "
      "(0) to the core vertex (1); tan^2 of that angle at the poles 0, 45, ..., 315 degrees is 0, 1, 1/2, 1/9, 0, 1/9, 1/2, 1",
      t2 == [0, 1, sp.Rational(1, 2), sp.Rational(1, 9), 0, sp.Rational(1, 9), sp.Rational(1, 2), 1]
      and all(abs(mpmath.quad(lambda t: 1 / (t - pm), [0, 1]) - mpmath.log(1 - 1 / pm)) < 1e-35
              for pm in (mpmath.mpc(sp.N(sp.re(sp.expand_complex(p)), 45), sp.N(sp.im(sp.expand_complex(p)), 45)) for p in allpoles)))
check("Theorem 11: 45 degrees at the near neighbours 1 ± i; arctan(1/sqrt2) at ±i sqrt2, the angle at a star point in the triangle "
      "Field Origin - face centre - corner (legs 1, sqrt2); arctan(1/3) at the far neighbours -1 ± i",
      t2[1] == t2[7] == 1 and t2[2] == t2[6] == sp.Rational(1, 2) and t2[3] == t2[5] == sp.Rational(1, 9)
      and abs(mpmath.atan(1 / mpmath.sqrt(2)) - mpmath.acos(2 / (mpmath.sqrt(3) * mpmath.sqrt(2)))) < 1e-35)
check("Theorem 11 (Niven): cos 2θ = (1 - t^2)/(1 + t^2) is 0, 1/3, 4/5 for t^2 = 1, 1/2, 1/9; a rational cosine of a rational multiple of "
      "pi is 0, ±1/2 or ±1, so only the 45-degree angle is a rational multiple of pi",
      [(1 - t) / (1 + t) for t in (1, sp.Rational(1, 2), sp.Rational(1, 9))] == [0, sp.Rational(1, 3), sp.Rational(4, 5)])
# Theorem 12: the octahedral formula
T = lambda j: mpmath.nsum(lambda k: (-mpmath.mpf(1) / 4)**k / (4 * k + j), [0, mpmath.inf])
check("Theorem 12: 4 y^(j-1)/(4 + y^4) = sum_k (-1/4)^k y^(4k+j-1), so the formulas with poles exactly at the four in-plane neighbours are "
      "sum_j c_j T_j = integral_0^1 4 p_c(y)/(4 + y^4), T_j = sum_k (-1/4)^k/(4k+j), base -4 and period 4",
      sp.expand(sp.series(4 / (4 + y**4), y, 0, 17).removeO() - sum((-sp.Rational(1, 4))**k * y**(4 * k) for k in range(5))) == 0
      and all(abs(T(j) - mpmath.quad(lambda t: 4 * t**(j - 1) / (4 + t**4), [0, 1])) < 1e-35 for j in range(1, 5)))
check("Theorem 12: at the far neighbours 1 - 1/p = (3 ± i)/2 = (1 ± i)(2 ∓ i)/2 carries the prime 5; at the near ones (1 ± i)/2 does not",
      sp.expand((1 + sp.I) * (2 - sp.I)) == 3 + sp.I and sp.expand_complex(1 - 1 / (-1 + sp.I)) == sp.Rational(3, 2) + sp.I / 2
      and sp.expand_complex(1 - 1 / (1 + sp.I)) == sp.Rational(1, 2) + sp.I / 2)
al, be = sp.symbols('alpha beta')
valab = sp.simplify(sp.integrate(4 * (al * y + be) / (y**2 - 2 * y + 2), (y, 0, 1)))
check("Theorem 12: so p_c vanishes at -1 ± i, p_c = (y^2 + 2y + 2)(alpha y + beta), and the value is (alpha + beta) pi - 2 alpha ln 2",
      sp.simplify(valab - ((al + be) * sp.pi - 2 * al * sp.log(2))) == 0
      and sp.expand(sp.cancel(4 * (y**2 + 2 * y + 2) * (al * y + be) / (4 + y**4)) - sp.cancel(4 * (al * y + be) / (y**2 - 2 * y + 2))) == 0)
cvec = sp.Poly(y**2 + 2 * y + 2, y).all_coeffs()[::-1] + [0]
check("Theorem 12: pi/ln 2 is irrational (e^pi is transcendental, Gelfond), so alpha = 0, beta = 1: the unique formula is "
      "pi = sum_k (-1/4)^k [2/(4k+1) + 2/(4k+2) + 1/(4k+3)], with its fourth slot silent",
      cvec == [2, 2, 1, 0] and abs(sum(c * T(j + 1) for j, c in enumerate(cvec)) - mpmath.pi) < 1e-35)
w_lift = [2, 2, 1, 0, sp.Rational(-1, 2), sp.Rational(-1, 2), sp.Rational(-1, 4), 0]
check("Theorem 12: doubling, k -> (2m, 2m+1), turns base -4 into base 16 = (-4)^2: T_j = S_j - S_(j+4)/4, i.e. "
      "4(4 - y^4)(y^2 + 2y + 2) = 16 sum_j w_j y^(j-1) with w = (2, 2, 1, 0, -1/2, -1/2, -1/4, 0) = w_BBP - a/4",
      sp.expand(4 * (4 - y**4) * (y**2 + 2 * y + 2) - 16 * sum(w_lift[j] * y**j for j in range(8))) == 0
      and w_lift == [b_ - sp.Rational(1, 4) * a_ for b_, a_ in zip([4, 0, 0, -2, -1, -1, 0, 0], [8, -8, -4, -8, -2, -2, 1, 0])])
pw = lambda w: 16 * sum(w[j] * y**j for j in range(8))
check("Theorem 12: closure, the integrand vanishing at the core vertex y = 1, holds for no member but r = 0: the octahedral formula's "
      "integrand is 4 there, its lift's weights sum to 15/4, and p_(w(r))(1) = -240 r; so closure selects BBP",
      sp.cancel(4 * (y**2 + 2 * y + 2) / (4 + y**4)).subs(y, 1) == 4 and sum(w_lift) == sp.Rational(15, 4)
      and sp.expand(pw([b_ + r * a_ for b_, a_ in zip([4, 0, 0, -2, -1, -1, 0, 0], [8, -8, -4, -8, -2, -2, 1, 0])]).subs(y, 1) + 240 * r) == 0)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
