"""Machine checks for every step of "G's Graded Operator Is a Null Rotation".
Exact algebra (sympy) throughout; 30-digit numerics only for one determinant of a matrix exponential and one size estimate.
Run: python verify_g_null_rotation.py"""
import re, pathlib
import sympy as sp
import mpmath

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

def kp(M, n):
    R = sp.eye(1)
    for _ in range(n): R = sp.kronecker_product(R, M)
    return R
A = sp.Matrix([[1, 0], [1, 1]]); N = sp.Matrix([[0, 0], [1, 0]]); H2 = sp.Matrix([[1, 1], [1, -1]])
def Ltot(m):                                   # total "remove one bit" operator on m bits
    return sum((kp(sp.eye(2), i).__class__(sp.kronecker_product(sp.kronecker_product(kp(sp.eye(2), i), N), kp(sp.eye(2), m - i - 1)))
                for i in range(m)), sp.zeros(2**m))
S = {m: kp(A, m) for m in (0, 2, 4)}
popc = lambda x: bin(x).count("1")

# ---- Theorem 1: the blocks of the archive's diagram are the Sierpinski matrices S_m = A^(x m) = e^L
html = pathlib.Path(__file__).resolve().parents[2] / "research" / "g_from_topology" / "g_three_sierpinski_blocks.html"
if html.exists():
    cells = re.findall(r'<rect x="(\d+)" y="(\d+)" width="28"[^>]*fill="(#\w+)" opacity="([\d.]+)"', html.read_text())
    def block(col):
        filled = [(int(x), int(y)) for x, y, c, o in cells if c == col]
        xs, ys = sorted({x for x, _ in filled}), sorted({y for _, y in filled})
        M = sp.zeros(len(ys), len(xs))
        for x, y in filled: M[ys.index(y), xs.index(x)] = 1
        return M
    check("Theorem 1: the diagram's 4x4 and 16x16 blocks (g_three_sierpinski_blocks.html) are exactly A^(x2) and A^(x4), A = [[1,0],[1,1]] "
          "(Pascal's triangle mod 2)", block("#378ADD") == S[2] and block("#D85A30") == S[4])
else:
    check("Theorem 1: (diagram file not found; skipping the cell-by-cell comparison) A^(x m) is Pascal's triangle mod 2",
          all(S[4][i, j] == (sp.binomial(i, j) % 2) for i in range(16) for j in range(16)))
check("Theorem 1: entry (i, j) of S_m is 1 exactly when the bits of j are a subset of the bits of i (Lucas), i.e. C(i, j) is odd",
      all(S[m][i, j] == (1 if (j & ~i) == 0 else 0) == sp.binomial(i, j) % 2 for m in (2, 4) for i in range(2**m) for j in range(2**m)))
check("Theorem 1: S_m = e^L with L the sum over bits of 'remove that bit'; L is nilpotent, L^(m+1) = 0, Tr L = 0",
      all((Ltot(m)**(m + 1)).is_zero_matrix and Ltot(m).trace() == 0
          and S[m] == sum((Ltot(m)**k / sp.factorial(k) for k in range(m + 1)), sp.zeros(2**m)) for m in (2, 4)))
check("Theorem 1: traces 1, 4, 16 (the diagonal); filled cells 1, 9, 81 = 3^m",
      [S[m].trace() for m in (0, 2, 4)] == [1, 4, 16] and [sum(S[m]) for m in (0, 2, 4)] == [1, 9, 81])

# ---- Theorem 2: G is unchanged, and reads the diagonal only
s = sp.symbols("s")
M = lambda v: sp.diag(S[0], v * S[2], S[4])
check("Theorem 2: Tr(S_0 + s S_2 + S_4) = 1 + 4s + 16 = f(K, s): 21, 17, 13 at s = +1, 0, -1",
      sp.expand(M(s).trace() - (1 + 4 * s + 16)) == 0 and [M(v).trace() for v in (1, 0, -1)] == [21, 17, 13])
check("Theorem 2: the spectra equal those of the graded identity: all 21 eigenvalues 1 at s = +1; 17 x (+1) and 4 x (-1) at s = -1; "
      "rank 17 at s = 0", M(1).eigenvals() == {1: 21} and M(-1).eigenvals() == {1: 17, -1: 4} and M(0).rank() == 17)
mpmath.mp.dps = 30
alpha = mpmath.mpf(1) / mpmath.mpf("137.035999177")
dets = []
for v in (1, 0, -1):
    Mn = mpmath.matrix([[float(x) for x in M(v).row(i)] for i in range(21)])
    dets.append(mpmath.det(mpmath.expm(mpmath.log(alpha) * Mn)))
check("Theorem 2: det(alpha^M) = alpha^(Tr M) = alpha^21, alpha^17, alpha^13 (30-digit matrix exponential), so G = (17/13) alpha^21 hbar c/m_e^2 "
      "follows exactly as with identity blocks", all(abs(d / alpha**t - 1) < mpmath.mpf(10)**-20 for d, t in zip(dets, (21, 17, 13))))
check("Theorem 2: reading the filled cells instead (1 + 9 + 81 = 91) would change G by alpha^70, about 10^-150",
      sum(sum(S[m]) for m in (0, 2, 4)) == 91 and abs(mpmath.log10(alpha**70) + 149.6) < 0.2)

# ---- Theorem 3: the two bits are the spinor indices of a 4-vector; the Sierpinski block is a null rotation
I2 = sp.eye(2); sx = sp.Matrix([[0, 1], [1, 0]]); sy = sp.Matrix([[0, -sp.I], [sp.I, 0]]); sz = sp.Matrix([[1, 0], [0, -1]])
sig = [I2, sx, sy, sz]; eta = sp.diag(1, -1, -1, -1)
t, x, y, z = sp.symbols("t x y z", real=True)
X = t * I2 + x * sx + y * sy + z * sz
def Lam(Mx):          # Lorentz matrix of X -> Mx X Mx^dagger
    return sp.Matrix(4, 4, lambda a, b: sp.nsimplify(sp.simplify(sp.Rational(1, 2) * (sig[a] * Mx * sig[b] * Mx.H).trace())))
check("Theorem 3: det X = t^2 - x^2 - y^2 - z^2 for X = t + x sx + y sy + z sz; X_00 = t + z, X_11 = t - z, so |00> and |11> are null",
      sp.expand(X.det() - (t**2 - x**2 - y**2 - z**2)) == 0 and sp.expand(X[0, 0] - (t + z)) == 0 and sp.expand(X[1, 1] - (t - z)) == 0)
Xg = sp.Matrix(2, 2, sp.symbols("X00 X01 X10 X11"))
check("Theorem 3: on the bit basis, vec(A X A^T) = (A (x) A) vec(X): the 4-block Sierpinski matrix S_2 is X -> A X A^T",
      sp.expand(sp.Matrix(list(A * Xg * A.T)) - S[2] * sp.Matrix(list(Xg))) == sp.zeros(4, 1))
LA = Lam(A)
check("Theorem 3: Lambda(A) is a real Lorentz transformation (Lambda^T eta Lambda = eta, det +1, Lambda_00 > 0), not the identity, "
      "with (Lambda - 1)^3 = 0: a null rotation", (LA.T * eta * LA - eta).is_zero_matrix and LA.det() == 1 and LA[0, 0] > 0
      and LA != sp.eye(4) and ((LA - sp.eye(4))**3).is_zero_matrix and not ((LA - sp.eye(4))**2).is_zero_matrix)
fix = (LA - sp.eye(4)).nullspace()
a_, b_ = sp.symbols("a b", real=True)
w = a_ * sp.Matrix([1, 0, 0, -1]) + b_ * sp.Matrix([0, 0, 1, 0])
check("Theorem 3: its fixed vectors are the plane spanned by k = (1, 0, 0, -1) (the state |11>) and y; the only light ray in it is k",
      len(fix) == 2 and sp.Matrix.hstack(*fix, sp.Matrix([1, 0, 0, -1]), sp.Matrix([0, 0, 1, 0])).rank() == 2
      and sp.solve(sp.Eq((w.T * eta * w)[0], 0), b_) == [0])
check("Theorem 3 (remark): every real A with det A = 1 fixes y (the antisymmetric part i sy of X), so the Sierpinski blocks act as the "
      "2+1 Lorentz group on (t, x, z)", all((Lam(Mx) * sp.Matrix([0, 0, 1, 0]) - sp.Matrix([0, 0, 1, 0])).is_zero_matrix
                                             for Mx in (A, A.T, sp.diag(2, sp.Rational(1, 2)))))

# ---- Theorem 4: the Walsh-Hadamard read is a rotation by pi, and factors through the Sierpinski block
Hn = H2 / sp.sqrt(2); LH = Lam(Hn)
ax_ = sp.Matrix([0, 1, 0, 1])
check("Theorem 4: normalised H_2 acts on X as a rotation of space by pi about (x + z)/sqrt2 (Lorentz, Lambda_00 = 1, spatial trace -1, "
      "axis fixed)", (LH.T * eta * LH - eta).is_zero_matrix and LH[0, 0] == 1 and LH[1:, 1:].trace() == -1 and (LH * ax_ - ax_).is_zero_matrix)
check("Theorem 4: H_(2^m) = S_m diag((-2)^popcount) S_m^T for m = 0, 2, 4 (the 1-, 4- and 16-blocks)",
      all(S[m] * sp.diag(*[(-2)**popc(i) for i in range(2**m)]) * S[m].T == kp(H2, m) for m in (0, 2, 4)))
check("Theorem 4: (-2)^popcount = e^((ln 2 + i pi) popcount), so H = e^L e^((ln 2 + i pi) popcount) e^(L^T)",
      all(sp.simplify(sp.exp((sp.log(2) + sp.I * sp.pi) * k) - (-2)**k) == 0 for k in range(5)))
Dn = sp.diag(1, -2) / sp.sqrt(2); LD = Lam(Dn)
boost = sp.Matrix([[sp.Rational(5, 4), 0, 0, -sp.Rational(3, 4)], [0, -1, 0, 0], [0, 0, -1, 0], [-sp.Rational(3, 4), 0, 0, sp.Rational(5, 4)]])
check("Theorem 4: the middle factor is a boost of rapidity ln 2 along z (cosh ln2 = 5/4, sinh ln2 = 3/4) with a rotation by pi about z",
      LD == boost and sp.simplify(sp.cosh(sp.log(2)).rewrite(sp.exp)) == sp.Rational(5, 4) and sp.simplify(sp.sinh(sp.log(2)).rewrite(sp.exp)) == sp.Rational(3, 4))
check("Theorem 4: so rotation by pi = null rotation x (boost ln 2, pi twist) x reverse null rotation, as Lorentz matrices",
      (Lam(A) * LD * Lam(A.T) - LH).is_zero_matrix)

# ---- Theorem 5: the graded character, and K = 4 as the trace of a null rotation
chi = lambda Mx: sp.simplify(sp.Abs(Mx.trace())**2)
check("Theorem 5: Tr Lambda(M) = |Tr M|^2 for the null rotation (4), the pi-rotation (0) and the middle factor (1/2)",
      all(sp.simplify(Lam(Mx).trace() - chi(Mx)) == 0 for Mx in (A, Hn, Dn)) and chi(A) == 4 and chi(Hn) == 0 and chi(Dn) == sp.Rational(1, 2))
check("Theorem 5: on the rank-2 tensor block the trace is chi^2 (Tr(L (x) L) = (Tr L)^2): 16 for the null rotation, 0 for H",
      sp.kronecker_product(LA, LA).trace() == 16 and sp.simplify(sp.kronecker_product(LH, LH).trace()) == 0)
check("Theorem 5: the graded character 1 + s chi + chi^2 = f(chi, s) gives 21, 17, 13 for the null rotation and 1, 1, 1 for the pi-read",
      [1 + v * 4 + 16 for v in (1, 0, -1)] == [21, 17, 13] and [1 + v * 0 + 0 for v in (1, 0, -1)] == [1, 1, 1])
ph, et = sp.symbols("phi eta", real=True)
Rz = sp.diag(sp.exp(sp.I * ph / 2), sp.exp(-sp.I * ph / 2)); Bz = sp.diag(sp.exp(et / 2), sp.exp(-et / 2))
check("Theorem 5: a rotation by phi has chi = 4 cos^2(phi/2) <= 4 and a boost of rapidity eta has chi = 4 cosh^2(eta/2) >= 4; equality "
      "only at phi = 0 or eta = 0, so chi = 4 is the boundary on which the null rotations lie",
      sp.simplify(sp.expand_complex(chi(Rz)) - 4 * sp.cos(ph / 2)**2) == 0 and sp.simplify(chi(Bz) - 4 * sp.cosh(et / 2)**2) == 0
      and sp.simplify(Lam(Rz).trace() - 4 * sp.cos(ph / 2)**2) == 0)

# ---- Theorem 6: the chains
def jordan_sizes(Mx):
    n = Mx.shape[0]; Nm = Mx - sp.eye(n)
    r = [n] + [(Nm**k).rank() for k in range(1, n + 1)]
    ge = [r[k - 1] - r[k] for k in range(1, n + 1)] + [0]
    return sorted([k for k in range(1, n + 1) for _ in range(ge[k - 1] - ge[k])], reverse=True)
check("Theorem 6: Jordan chains of S_2: 3 + 1; of S_4: 5 + 3 + 3 + 3 + 1 + 1; together 1 + (3+1) + (5+3+3+3+1+1) = 21",
      jordan_sizes(S[2]) == [3, 1] and jordan_sizes(S[4]) == [5, 3, 3, 3, 1, 1])
check("Theorem 6: these are the Clebsch-Gordan decompositions of m spin-1/2s (C(m,k) - C(m,k-1) multiplets of dimension m - 2k + 1): 2 x 2 = 3 + 1, 2^4 = 5 + 3(3) + 2(1)",
      all(sorted([m - 2 * k + 1 for k in range(m // 2 + 1) for _ in range(sp.binomial(m, k) - (sp.binomial(m, k - 1) if k else 0))], reverse=True)
          == jordan_sizes(S[m]) for m in (2, 4)))
P = sp.zeros(16)
for a in range(4):
    for b in range(4): P[4 * b + a, 4 * a + b] = 1
def restricted_sizes(Proj):
    B = sp.Matrix.hstack(*Proj.columnspace())
    R = (B.T * B).inv() * B.T * S[4] * B
    return jordan_sizes(R)
check("Theorem 6: S_4 commutes with the exchange of the two vector factors; on the symmetric 10 the chains are 5 + 3 + 1 + 1, on the "
      "antisymmetric 6 they are 3 + 3",
      (S[4] * P - P * S[4]).is_zero_matrix and restricted_sizes((sp.eye(16) + P) / 2) == [5, 3, 1, 1]
      and restricted_sizes((sp.eye(16) - P) / 2) == [3, 3])


# ---- Theorem 7: the tetrad frame is the 4-block's Walsh-Hadamard read
corners = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1) if a * b * c == 1]
H4 = sp.kronecker_product(H2, H2)
frame = sp.Matrix([[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])     # hadamard-cube-frame's bordered frame
Prow = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
check("Theorem 7: the archive's tetrad frame (a row of ones over the four TetA corners) is H_2 (x) H_2 with its 2nd and 3rd rows exchanged; "
      "its legs point at the four corners with xyz = +1",
      Prow * H4 == frame and sorted(tuple(frame[1:, c]) for c in range(4)) == sorted(corners))
check("Theorem 7: so the frame factors through the Sierpinski block: frame = P S_2 diag((-2)^popcount) S_2^T, a null rotation, a boost of "
      "rapidity ln 2 with a pi twist, and the reverse null rotation", frame == Prow * S[2] * sp.diag(*[(-2)**popc(i) for i in range(4)]) * S[2].T)
check("Theorem 7: read in (t, x, y, z) the frame is not a Lorentz structure: frame^T eta frame = 2J - 4I (legs of norm -2, pairwise 2), the "
      "archive's forced Gram matrix up to sign and scale", frame.T * eta * frame == 2 * sp.ones(4, 4) - 4 * sp.eye(4))

# ---- Theorem 8: in the spinor reading the legs are a Newman-Penrose null tetrad
hcol = [H2[:, 0], H2[:, 1]]
leg = {(a, b): hcol[a] * hcol[b].T for a in (0, 1) for b in (0, 1)}
check("Theorem 8: the leg (a, b) of H_2 (x) H_2, read as the 2x2 matrix X, is the outer product h_a h_b^T of two columns of H_2, so det X = 0: "
      "every leg is null", all(sp.Matrix(2, 2, list(H4[:, 2 * a + b])) == leg[(a, b)] and leg[(a, b)].det() == 0 for a in (0, 1) for b in (0, 1)))
mink = lambda Xm: sp.Matrix([sp.simplify((sg * Xm).trace() / 2) for sg in sig])
l_, n_, m_, mb_ = leg[(0, 0)], leg[(1, 1)], leg[(0, 1)], leg[(1, 0)]
check("Theorem 8: in Minkowski components l = (1,1,0,0) and n = (1,-1,0,0) are real light rays along ±x; m = (0,0,-i,1) and its complex "
      "conjugate m-bar = (0,0,i,1) are the other two legs",
      mink(l_) == sp.Matrix([1, 1, 0, 0]) and mink(n_) == sp.Matrix([1, -1, 0, 0]) and mink(m_) == sp.Matrix([0, 0, -sp.I, 1])
      and mink(mb_) == mink(m_).conjugate())
ipr = lambda U, V: sp.Rational(1, 2) * ((U + V).det() - U.det() - V.det())
legs4 = [l_, n_, m_, mb_]
G4 = sp.Matrix(4, 4, lambda i, j: ipr(legs4[i], legs4[j]))
check("Theorem 8: their products are l.n = 2, m.m-bar = -2 and all others 0: a Newman-Penrose null tetrad (normalisation x2, from |h_a|^2 = 2)",
      G4 == sp.Matrix([[0, 2, 0, 0], [2, 0, 0, 0], [0, 0, 0, -2], [0, 0, -2, 0]]))
check("Theorem 8: the Hadamard combinations of the legs, l + n, l - n, m + m-bar, i(m - m-bar), are 2t, 2x, 2z, 2y: the orthonormal frame",
      [mink(l_ + n_), mink(l_ - n_), mink(m_ + mb_), mink(sp.I * (m_ - mb_))]
      == [sp.Matrix([2, 0, 0, 0]), sp.Matrix([0, 2, 0, 0]), sp.Matrix([0, 0, 0, 2]), sp.Matrix([0, 0, 2, 0])])
# lemma: p q^T (p != 0) is Hermitian exactly when q = lambda conj(p) with lambda real
p1, p2 = sp.Rational(3, 7) + 2 * sp.I, -sp.Rational(5, 3) + sp.I / 4
qr = sp.symbols("q1r q1i q2r q2i", real=True)
q = sp.Matrix([qr[0] + sp.I * qr[1], qr[2] + sp.I * qr[3]]); pv = sp.Matrix([p1, p2])
Mh = pv * q.T - (pv * q.T).H
eqs = [e for entry in Mh for e in sp.expand(entry).as_real_imag() if e != 0]
Jac = sp.Matrix([[sp.diff(e, v) for v in qr] for e in eqs])
nullv = Jac.nullspace()
conjp = sp.Matrix([sp.re(p1), -sp.im(p1), sp.re(p2), -sp.im(p2)])
check("Theorem 8 (lemma): for p != 0, p q^T is Hermitian exactly when q is a real multiple of conj(p) (the solution space is one real line "
      "through conj(p)); so, with B, C invertible, the legs B h_a (C h_b)^T for a fixed a and both b cannot both be Hermitian, and at most "
      "two of the four legs are real light rays in any spinor reading",
      len(nullv) == 1 and sp.Matrix.hstack(nullv[0], conjp).rank() == 1)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
