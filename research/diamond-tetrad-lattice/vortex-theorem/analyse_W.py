"""Exact analysis of W, the 4-dimensional part of the Triforce winding space (THEOREM.md, Part III),
symbolically in all Td-invariant parameters (sympy; independent of certify_vortices.py).
Run: python analyse_W.py"""
import contextlib, io, os
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
PASS = FAIL = 0
def check(label, ok):
    global PASS, FAIL
    PASS += bool(ok); FAIL += (not ok); print(("PASS " if ok else "FAIL ") + label)

ns = {"__name__": "setup"}
src = open(os.path.join(HERE, "..", "triforce-vortex", "verify_triforce_vortex.py")).read().split("# Theorem: stationary vortices")[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ns)
H, n, sites, cent, adj = ns["H"], ns["n"], ns["sites"], ns["cent"], ns["adj"]
params = list(ns["site_orb"].values()) + list(ns["bond_orb"].values())
C3p = ns["perm_of"](sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]]))
seen, orbits = set(), []
for i in range(n):
    if i in seen:
        continue
    o = [i]
    while C3p[o[-1]] != i:
        o.append(C3p[o[-1]])
    seen |= set(o); orbits.append(o)
full = [o for o in orbits if len(o) == 3]
w = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2
B = sp.zeros(n, 10)
for k, o in enumerate(full):
    for j, i in enumerate(o):
        B[i, k] = sp.expand(w ** (-j))
def S(z):
    """Exact simplification of expressions with sqrt(3) and i: rationalise, split into real and imaginary parts."""
    z = sp.expand_complex(sp.radsimp(sp.expand(z)))
    return sp.nsimplify(sp.simplify(sp.re(z))) + sp.I * sp.nsimplify(sp.simplify(sp.im(z)))
simp = lambda M: M.applyfunc(S)
A = simp(B.H * H * B)
cent_k = [k for k, o in enumerate(full) if sites[o[0]][0] == "central"]
out_k = [k for k in range(10) if k not in cent_k]
rows = [A.applyfunc(lambda z: sp.diff(z, p)).extract(cent_k, out_k) for p in params]
N = sp.Matrix.vstack(*rows).nullspace()
W = sp.zeros(10, len(N))
for c, v in enumerate(N):
    for a, k in enumerate(out_k):
        W[k, c] = v[a]
G = simp(W.H * W)
MW = simp(G.inv() * W.H * A * W)
check("W has dimension 4 and A maps W into itself, for all parameters",
      len(N) == 4 and simp(A * W - W * MW) == sp.zeros(10, 4))
# find the two invariant 2-dim pieces (coordinates that couple)
pairs = [(i, j) for i in range(4) for j in range(i + 1, 4) if S(MW[i, j]) != 0]
print("     couplings inside W:", pairs, "| restricted matrix:", MW.tolist())
b1, b2 = pairs[0], pairs[1]
M1, M2 = MW.extract(list(b1), list(b1)), MW.extract(list(b2), list(b2))
E = sp.symbols("E", real=True)
cp1, cp2 = S((E * sp.eye(2) - M1).det()), S((E * sp.eye(2) - M2).det())
check("W splits into two 2-dimensional pieces with the same characteristic polynomial: every energy on W is doubled, "
      "for all parameters", len(pairs) == 2 and S(cp1 - cp2) == 0 and set(b1) | set(b2) == {0, 1, 2, 3})
print("     each piece:", sp.factor(cp1))
# flux form on W, half-plane through the leg (exact, as in certify_vortices.py)
axis = sp.Matrix([1, 1, 1]); u = sp.Matrix([3, -1, -2]); vv = axis.cross(u)
s_ = [(vv.T * c)[0] for c in cent]
K = sp.zeros(n, n)
for (i, j) in adj:
    si, sj = s_[i], s_[j]
    if si * sj < 0:
        t = si / (si - sj); x = cent[i] + t * (cent[j] - cent[i])
        if (u.T * x)[0] > 0:
            sg = 1 if si < 0 else -1
            K[i, j] += -sp.I * sg * H[i, j]; K[j, i] += sp.I * sg * H[j, i]
KW = simp(W.H * B.H * K * B * W)
# eigenvectors of each piece at energy E: y1 in piece 1, y2 in piece 2
def eigvec(Mp, idx):
    a, b, c_ = Mp[0, 0], Mp[0, 1], Mp[1, 1]
    y = sp.zeros(4, 1); y[idx[0]] = b; y[idx[1]] = E - a      # (E - a) y0 = b y1 solves row 1
    return y
y1, y2 = eigvec(M1, b1), eigvec(M2, b2)
f11 = S((y1.H * KW * y1)[0]); f22 = S((y2.H * KW * y2)[0]); f12 = S((y1.H * KW * y2)[0])
g11 = S((y1.H * G * y1)[0]); g22 = S((y2.H * G * y2)[0])
print("     flux of piece 1:", sp.factor(f11), " | piece 2:", sp.factor(f22), " | cross term:", sp.factor(f12))
fl = S
g12 = S((y1.H * G * y2)[0])
Gm = sp.Matrix([[g11, g12], [sp.conjugate(g12), g22]])
print("     Gram of the two states:", [[sp.factor(x) for x in r] for r in Gm.tolist()])
check("they carry the same circulation (normalised flux of piece 1 = that of piece 2)", S(f11 * g22 - f22 * g11) == 0)
# circulation form on the doubled level, in the basis (y1, y2): F = [[f11, f12], [conj f12, f22]], Gram diag(g11, g22).
# Some combination carries no current iff F is indefinite iff det F < 0 (F is 2x2 Hermitian, Gram positive definite).
detF = S(f11 * f22 - f12 * sp.conjugate(f12))
cp = sp.Poly(sp.expand(cp1), E)
detF_red = sp.factor(sp.Poly(sp.expand(detF), E).rem(cp).as_expr())
print("     det F reduced on the doubled level (E a root of the piece polynomial):", detF_red)
red_f11 = sp.factor(sp.Poly(sp.expand(f11), E).rem(cp).as_expr())
print("     f11 reduced:", red_f11)
import random
random.seed(4)
signs = []
for trial in range(40):
    val = {p_: sp.Rational(random.randint(-30, 30), random.randint(1, 7)) for p_ in params}
    if val.get(sp.Symbol("t5", real=True), 1) == 0:
        continue
    roots = sp.solve(cp1.subs(val), E)
    for r in roots:
        d = sp.nsimplify(sp.simplify(detF.subs(val).subs(E, r)))
        signs.append(sp.sign(sp.N(d, 50)))
npos, nneg, nzero = sum(x == 1 for x in signs), sum(x == -1 for x in signs), sum(x == 0 for x in signs)
print(f"     40 random rational parameter points, {len(signs)} doubled levels (exact roots): det F > 0 at {npos} "
      f"(every combination circulates, one sense), det F < 0 at {nneg} (a standing combination exists), = 0 at {nzero}")
check("both cases occur: on W, whether every stationary winding state circulates depends on the parameters",
      npos > 0 and nneg > 0)
ring_k = next(k for k, o in enumerate(full) if sites[o[0]][0] == "outer" and ns["key"](ns["TA"][0]) in sites[o[0]][2])
check("W carries weight on the near star point's ring (orbit %d)" % ring_k, any(W[ring_k, c] != 0 for c in range(4)))
print(f"\n{PASS}/{PASS + FAIL} checks passed")
raise SystemExit(FAIL)
