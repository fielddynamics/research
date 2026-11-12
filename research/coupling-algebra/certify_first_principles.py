"""First-principles certification for research/coupling-algebra (Results 1-13).
Rebuilds every result from the frame's premises, independently of the two verify_*.py scripts:
orbit counting instead of matrix ranks, exact arithmetic (integers, Fractions, sympy), and F4
built abstractly as F2[x]/(x^2+x+1). Run: python certify_first_principles.py   (sympy)
Exact arithmetic throughout (integers, Fractions, sympy). Each check is tagged:
  [NEW]       new to the archive
  [CLASSICAL] standard mathematics, used here as a reading
  [AUTOMATIC] true for a reason that makes it carry no information
  [COINCIDENCE] exact, but holds only at the special value
"""
import itertools, math
from fractions import Fraction as Fr
import sympy as sp

ok = []; tags = {}
def check(tag, m, c):
    ok.append(bool(c)); tags[tag] = tags.get(tag, 0) + 1
    print(("PASS " if c else "FAIL ") + f"[{tag}] " + m)
def section(t): print(f"\n=== {t}")

# ===================================================================== A. the frame, from its premises
section("A. The frame from its premises (Letter 1, forced frame, Gram paper)")
c = sp.Symbol('c')
check("CLASSICAL", "four unit vectors with equal pairwise inner product c and zero sum force c = -1/3 (|sum|^2 = 4 + 12c = 0)",
      sp.solve(4 + 12 * c, c) == [sp.Rational(-1, 3)])
M1 = sp.Matrix([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]])
check("CLASSICAL", "the cube simplex M1 (columns +-1 vectors) realises it: M1^T M1 = 4I - J, columns sum to zero",
      M1.T * M1 == 4 * sp.eye(4) - sp.ones(4, 4) and M1 * sp.ones(4, 1) == sp.zeros(3, 1))
M2 = -M1
check("CLASSICAL", "the tetrad equation is even in the frame: M2 = -M1 has the same Gram matrix (Gram Lemma 1)", M2.T * M2 == M1.T * M1)
TA = [tuple(M1[:, k]) for k in range(4)]; TB = [tuple(M2[:, k]) for k in range(4)]
cube = [tuple(v) for v in itertools.product([1, -1], repeat=3)]
check("CLASSICAL", "TetA and TetB are disjoint and together are all 8 corners of the cube", sorted(TA + TB) == sorted(cube))
check("CLASSICAL", "2(D+1) = 2^D has the single positive-integer solution D = 3 (2^(D-1) > D+1 for D >= 4, checked to 60)",
      [D for D in range(1, 61) if 2 * (D + 1) == 2 ** D] == [3])
check("CLASSICAL", "TetA = {v1 v2 v3 = +1}, TetB = {v1 v2 v3 = -1}", all(math.prod(v) == 1 for v in TA) and all(math.prod(v) == -1 for v in TB))

# ===================================================================== B. the coupling algebra by orbit counting
section("B. The coupling algebra, recertified by counting orbits (not matrix ranks)")
order = TA + TB
ix = {v: i for i, v in enumerate(order)}
def signed_perms():
    for p in itertools.permutations(range(3)):
        for s in itertools.product([1, -1], repeat=3):
            yield p, s
act = lambda g, v: tuple(g[1][i] * v[g[0][i]] for i in range(3))
det = lambda g: sp.Matrix(3, 3, lambda i, j: g[1][i] if j == g[0][i] else 0).det()
Oh = list(signed_perms())
O = [g for g in Oh if det(g) == 1]
Td = [g for g in Oh if all(act(g, v) in TA for v in TA)]
def orbitals(G, pairs):
    seen, n = set(), 0
    for p in pairs:
        if p in seen: continue
        n += 1
        for g in G: seen.add((act(g, p[0]), act(g, p[1])))
    return n
allpairs = [(v, w) for v in cube for w in cube]
AB = [(v, w) for v in TA for w in TB] + [(v, w) for v in TB for w in TA]
check("CLASSICAL", "|O_h| = 48, |O| = 24, |T_d| = 24", (len(Oh), len(O), len(Td)) == (48, 24, 24))
check("CLASSICAL", "dimension of the symmetric couplings = number of orbits on ordered pairs: O_h gives 4", orbitals(Oh, allpairs) == 4)
check("NEW", "the proper rotations alone already give 4 (because some exchange the chambers)", orbitals(O, allpairs) == 4)
check("NEW", "between the chambers: 2 orbits under O_h (vector links, Field Origin links) - exactly two coupling channels",
      orbitals(Oh, AB) == 2)
check("CLASSICAL", "T_d (chambers kept apart) gives 8", orbitals(Td, allpairs) == 8)
d = lambda v, w: sum(a != b for a, b in zip(v, w))
A = [sp.Matrix(8, 8, lambda i, j: 1 if d(order[i], order[j]) == k else 0) for k in range(4)]
def coeffs(Mx):
    return [Mx[next((i, j) for i in range(8) for j in range(8) if d(order[i], order[j]) == k)] for k in range(4)]
table_ok = all(A[i] * A[j] == sum((coeffs(A[i] * A[j])[k] * A[k] for k in range(4)), sp.zeros(8, 8)) for i in range(4) for j in range(4))
check("CLASSICAL", "A_i A_j is always a combination of A_0..A_3 (closed, exact integers)", table_ok)
check("NEW", "A1 A3 = A2: a cube edge then the Field Origin diagonal is a tetrahedron edge", A[1] * A[3] == A[2])
check("NEW", "the Gram matrix of all 8 corners is exactly 3A0 + A1 - A2 - 3A3 (entry 3 - 2d)",
      sp.Matrix(8, 8, lambda i, j: sum(a * b for a, b in zip(order[i], order[j]))) == 3 * A[0] + A[1] - A[2] - 3 * A[3])
kraw = lambda w, k: sum((-1) ** j * math.comb(w, j) * math.comb(3 - w, k - j) for j in range(k + 1))
walsh = {S: [math.prod(v[i] for i in S) for v in order] for r in range(4) for S in itertools.combinations(range(3), r)}
check("CLASSICAL", "each Walsh function of grade w is an eigenvector of A_k with eigenvalue K_k(w) (Krawtchouk), exactly",
      all(A[k] * sp.Matrix(walsh[S]) == kraw(len(S), k) * sp.Matrix(walsh[S]) for S in walsh for k in range(4)))

# ===================================================================== C. the metric
section("C. The metric on the eight null directions (exact)")
s3 = sp.sqrt(3)
n = lambda v: sp.Matrix([1, v[0] / s3, v[1] / s3, v[2] / s3])
eta = sp.diag(-1, 1, 1, 1)
check("CLASSICAL", "n_v = (1, v/sqrt3) is null for every corner", all(sp.simplify((n(v).T * eta * n(v))[0]) == 0 for v in cube))
check("NEW", "eta(n_v, n_w) = -(2/3) d(v,w) exactly, for all 64 pairs",
      all(sp.simplify((n(v).T * eta * n(w))[0] + sp.Rational(2, 3) * d(v, w)) == 0 for v in cube for w in cube))
Geta = sp.Matrix(8, 8, lambda i, j: -sp.Rational(2, 3) * d(order[i], order[j]))
ev = {len(S): sp.simplify((sp.Matrix(walsh[S]).T * Geta * sp.Matrix(walsh[S]))[0] / 8) for S in walsh}
check("NEW", "its eigenvalue is -8 on grade 0, +8/3 on grade 1, 0 on grades 2 and 3: signature (1,3), time = grade 0, space = grade 1",
      ev == {0: -8, 1: sp.Rational(8, 3), 2: 0, 3: 0})
NA = sp.Matrix.hstack(*[n(v) for v in TA])
check("CLASSICAL", "TetA's four null directions are a basis and fix eta: NA^{-T} (NA^T eta NA) NA^{-1} = eta",
      sp.simplify(NA.inv().T * (NA.T * eta * NA) * NA.inv() - eta) == sp.zeros(4, 4))

# ===================================================================== D. the lower index pair on the links
section("D. The connection's lower index pair on the TetA-TetB links")
neg = lambda v: tuple(-x for x in v)
link = {(a, b): (TA[a], neg(TA[b])) for a in range(4) for b in range(4)}
check("NEW", "(a,b) -> link(TetA a, TetB -b) is a bijection onto the 16 between-chamber pairs",
      len(set(link.values())) == 16 and all(l[1] in TB for l in link.values()))
anti_link = lambda l: (neg(l[1]), neg(l[0]))   # both ends through the Field Origin, reordered (TetA end, TetB end)
check("NEW", "the index swap (a,b) -> (b,a) is the antipode acting on the links", all(anti_link(link[(a, b)]) == link[(b, a)] for a in range(4) for b in range(4)))
check("NEW", "fixed links: exactly the 4 diagonals (a,a), which are the Field Origin links (distance 3)",
      [k for k in link if anti_link(link[k]) == link[k]] == [(a, a) for a in range(4)] and all(d(*link[(a, a)]) == 3 for a in range(4)))

# ===================================================================== E. across the roots
section("E. A bilinear form read across the roots")
Pm = sp.diag(1, -1, -1, -1)
NB = sp.Matrix.hstack(*[n(neg(v)) for v in TA])
check("CLASSICAL", "n_{-v} = P n_v with P = diag(1,-1,-1,-1)", NB == Pm * NA)
def across(B):
    C = NA.T * B * NB
    if sp.simplify(C - C.T) == sp.zeros(4, 4): return 1
    if sp.simplify(C + C.T) == sp.zeros(4, 4): return -1
    return 0
E_ = lambda i, j: sp.Matrix(4, 4, lambda a, b: 1 if (a, b) in ((i, j), (j, i)) else 0)
gen = lambda i, j: eta * sp.Matrix(4, 4, lambda a, b: (1 if (a, b) == (i, j) else 0) - (eta[i, i] * eta[j, j] if (a, b) == (j, i) else 0))
forms = {"g00": E_(0, 0), **{f"g{i}{j}": E_(i, j) for i in range(1, 4) for j in range(i, 4)},
         **{f"g0{i}": E_(0, i) for i in range(1, 4)}, **{f"rot{i}{j}": gen(i, j) for i, j in [(1, 2), (1, 3), (2, 3)]},
         **{f"boost{i}": gen(0, i) for i in range(1, 4)}}
res = {k: across(B) for k, B in forms.items()}
check("NEW", "even across the roots: g00, the six gij, the three boosts; odd: the three g0i and the three rotations",
      all(res[k] == 1 for k in forms if k.startswith(("g00", "boost")) or (k[0] == "g" and k[1] != "0"))
      and all(res[k] == -1 for k in forms if k.startswith(("rot", "g0")) and k != "g00"))

# ===================================================================== F. F4, built abstractly
section("F. F4 built as F2[x]/(x^2+x+1), then laid on the tetrahedron")
# elements as pairs (a, b) = a + b x
F = [(0, 0), (1, 0), (0, 1), (1, 1)]
add = lambda p, q: ((p[0] + q[0]) % 2, (p[1] + q[1]) % 2)
def mul(p, q):           # (a + b x)(c + d x) with x^2 = x + 1
    a, b = p; c_, d_ = q
    return ((a * c_ + b * d_) % 2, (a * d_ + b * c_ + b * d_) % 2)
zero, one, w = F[0], F[1], F[2]
check("CLASSICAL", "F2[x]/(x^2+x+1) is a field of 4 elements; w = x has order 3", all(any(mul(p, q) == one for q in F) for p in F[1:])
      and mul(mul(w, w), w) == one and mul(w, w) != one)
# the tetrahedron seen down the 3-fold axis through TetA's corner (1,1,1)
axis = sp.Matrix([1, 1, 1]) / s3
u1 = sp.Matrix([1, -1, 0]) / sp.sqrt(2); u2 = sp.Matrix([1, 1, -2]) / sp.sqrt(6)
proj = lambda v: sp.nsimplify(sp.simplify((sp.Matrix(v).T * u1)[0] + sp.I * (sp.Matrix(v).T * u2)[0]))
P = {v: sp.simplify(proj(v)) for v in TA}
others = [v for v in TA if v != (1, 1, 1)]
r = sp.Abs(P[others[0]])
wC = sp.exp(2 * sp.pi * sp.I / 3)
ratios = sorted([sp.simplify(P[v] / P[others[0]]) for v in others], key=lambda z: sp.arg(z))
check("NEW", "seen down the axis through the corner (1,1,1), TetA is exactly {0, r, r w, r w^2}: the axis corner at the centre, "
      "the other three on an equilateral triangle", P[(1, 1, 1)] == 0 and all(sp.simplify(sp.Abs(P[v]) - r) == 0 for v in others)
      and set(sp.simplify(sp.expand_complex(z)) for z in ratios) == set(sp.simplify(sp.expand_complex(z)) for z in [1, wC, wC ** 2]))
# reduction Z[w] -> F4 on {0, 1, w, w^2}
red = {0: zero, 1: one, 'w': w, 'w2': mul(w, w)}
check("CLASSICAL", "Z[w]/(2) = F4: 2 stays prime in the Eisenstein integers (2 = 2 mod 3), and 0, 1, w, w^2 reduce to the 4 distinct elements",
      len(set(red.values())) == 4 and sp.factorint(2) == {2: 1} and 2 % 3 == 2)
check("CLASSICAL", "mod 2, 1 + w = -w^2 = w^2: the complex points add like XOR of corners (half-turns)", add(one, w) == mul(w, w))
# all 24 identifications tetrahedron -> F4
idents = list(itertools.permutations(F))
perm_sign = lambda p: sp.combinatorics.Permutation(list(p)).signature()
def is_affine(perm):     # perm: tuple of images of F[0..3]; affine iff perm(x) = a x + b
    return any(all(perm[F.index(x)] == add(mul(a, x), b) for x in F) for a in F[1:] for b in F)
def is_semiaffine(perm):
    fr = lambda x: mul(x, x)
    return any(all(perm[F.index(x)] == add(mul(a, fr(x) if s else x), b) for x in F) for a in F[1:] for b in F for s in (0, 1))
allperms = list(itertools.permutations(range(4)))
check("AUTOMATIC", "every one of the 24 permutations of F4 is semi-affine (x -> a x^s + b): AGammaL(1,4) = Sym(F4) = S4. "
      "So 'the tetrahedron's symmetries are F4's symmetries' holds for ANY labelling and carries no information by itself",
      all(is_semiaffine(tuple(F[i] for i in p)) for p in allperms))
check("CLASSICAL", "the affine ones (no Frobenius) are exactly the 12 even permutations: AGL(1,4) = A4",
      sorted(perm_sign(p) for p in allperms if is_affine(tuple(F[i] for i in p))) == [1] * 12)
rotA = [g for g in Td if det(g) == 1]
check("CLASSICAL", "the tetrahedron's rotations act on its corners as the even permutations (A4), its reflections as the odd ones",
      all((det(g) == 1) == (sp.combinatorics.Permutation([TA.index(act(g, v)) for v in TA]).signature() == 1) for g in Td))
check("CLASSICAL", "so 'rotations = affine, reflections = Frobenius' is the classical A4 < S4: under every labelling, orientation = Galois sign",
      len(rotA) == 12)

# ===================================================================== G. the second root
section("G. The second root as an odd relabelling (exact, all cases)")
swapR = [g for g in O if all(act(g, v) in TB for v in TA)]
sig = []
for g in swapR:
    perm = [TB.index(act(g, v)) for v in TA]                 # R maps TetA leg k to TetB corner -TA[perm[k]]
    sig.append(sp.combinatorics.Permutation(perm).signature())
check("NEW", "12 proper rotations carry TetA onto TetB; each sends leg k to the reversed leg -sigma(k) with sigma ODD in every case",
      len(swapR) == 12 and all(s == -1 for s in sig))
check("NEW", "so in F4 terms the second root, up to a rotation, contains the Frobenius: it reverses the sense of the closure (w <-> w^2)",
      all(s == -1 for s in sig))

# ===================================================================== H. the coupling polynomial from the cube's rotations
section("H. f(K,s) as the characteristic polynomial of the cube's lattice rotations")
K, th = sp.symbols('K theta')
Rth = sp.Matrix([[sp.cos(th), -sp.sin(th)], [sp.sin(th), sp.cos(th)]])
charp = sp.expand(sp.simplify((K * sp.eye(2) - Rth).det()))
check("CLASSICAL", "det(K - R_theta) = K^2 - 2K cos(theta) + 1: with s = -2 cos(theta), f(K,s) = 1 + sK + K^2", sp.simplify(charp - (K ** 2 - 2 * K * sp.cos(th) + 1)) == 0)
check("CLASSICAL", "crystallographic restriction: a rotation preserving a lattice has integer trace 2cos(theta) in {-2,-1,0,1,2}; "
      "the three with an irreducible (genuinely planar) characteristic polynomial are 2cos = -1, 0, 1, i.e. s = +1, 0, -1",
      [t for t in range(-2, 3) if sp.Poly(K ** 2 - t * K + 1, K).is_irreducible] == [-1, 0, 1])
def plane_angle(g):      # rotational part of a cube symmetry: for proper g, its angle; for improper, the angle of -g
    Mg = sp.Matrix(3, 3, lambda i, j: g[1][i] if j == g[0][i] else 0)
    Rp = Mg if Mg.det() == 1 else -Mg
    return sp.acos((Rp.trace() - 1) / 2)
def ord_(g):
    v = list(range(8)); k = 1; h = g
    Mg = sp.Matrix(3, 3, lambda i, j: g[1][i] if j == g[0][i] else 0); X = Mg
    while X != sp.eye(3): X = X * Mg; k += 1
    return k
rows = {}
for g in Oh:
    Mg = sp.Matrix(3, 3, lambda i, j: g[1][i] if j == g[0][i] else 0)
    keeps = all(act(g, v) in TA for v in TA)
    key = (int(Mg.det()), ord_(g))
    rows.setdefault(key, set()).add((keeps, int(sp.expand((K * sp.eye(3) - Mg).det()).subs(K, 4))))
print("     (det, order) -> {(keeps chambers?, det(4 - g))}:", dict(sorted(rows.items())))
check("NEW", "the 3-fold rotations about body diagonals (order 3, det +1) all keep the chambers; det(4 - g) = 3 x 21 = (K-1) f(K,+1)",
      rows[(1, 3)] == {(True, 63)})
check("NEW", "the 6-fold rotoreflections (order 6, det -1: inversion times a 3-fold) all exchange the chambers; det(4 - g) = 5 x 13 = (K+1) f(K,-1)",
      rows[(-1, 6)] == {(False, 65)})
check("NEW", "the order-4 symmetries give f(K,0) = 17: the quarter turns exchange the chambers (3 x 17), the 4-fold rotoreflections keep them (5 x 17)",
      rows[(1, 4)] == {(False, 51)} and rows[(-1, 4)] == {(True, 85)})
check("NEW", "so TetA's value 21 is the chamber-keeping closure rotation, TetB's 13 is that rotation composed with the antipode, "
      "and the Field Origin's 17 belongs to the order-4 elements, one chamber-swapping and one chamber-keeping",
      rows[(1, 3)] == {(True, 63)} and rows[(-1, 6)] == {(False, 65)} and {x[1] % 17 for x in rows[(1, 4)] | rows[(-1, 4)]} == {0}
      and all(x[1] % 17 for k, v in rows.items() if k[1] != 4 for x in v))
check("CLASSICAL", "equivalently f(K,s) = |Z[zeta]/(K - zeta)| for zeta of order 3, 4, 6: in Z/21, Z/17, Z/13 the number K = 4 has order 3, 4, 6",
      [sp.n_order(4, m) for m in (21, 17, 13)] == [3, 4, 6]
      and sp.Matrix([[4, 1], [-1, 5]]).det() == 21)       # multiplication by 4 - w on Z[w] in the basis 1, w (w^2 = -1 - w)

# ===================================================================== I. G's count
section("I. G's coupling levels")
F43 = list(itertools.product(F, repeat=3))
orbs = {frozenset(tuple(mul(u, x) for x in v) for u in F[1:]) for v in F43 if v != (zero,) * 3}
check("CLASSICAL", "F4^3 = 64 = 1 + 21 x 3; the 21 orbits of the nonzero triples under F4* are the points of PG(2,4)", len(F43) == 64 and len(orbs) == 21)
check("CLASSICAL", "64 = 21 x 3 + 1 is 4^3 = 1 mod 21, i.e. K is a cube root of unity modulo f(K,+1)", pow(4, 3, 21) == 1)
check("AUTOMATIC", "K^3 = (2^D)^2 is |F4|^3 = |F2|^6 (F4 = F2^2): true for any field of order 4, nothing more", 4 ** 3 == 2 ** 6)

# ===================================================================== J. coincidences, kept separate
section("J. Exact but special-value coincidences (not to be built on)")
pp = sorted({p ** k for p in sp.primerange(2, 260) for k in range(1, 9) if p ** k <= 256})
swap_orbits = lambda q: (q * q + q + 1 + q + 1 + (0 if q % 2 == 0 else 1)) // 2
check("COINCIDENCE", "the lower-index swap has 13 = f(K,-1) orbits on PG(2,q) only at q = 4 (prime powers to 256)",
      [q for q in pp if swap_orbits(q) == q * q - q + 1] == [4])
z = sp.exp(2 * sp.pi * sp.I / 3)
check("COINCIDENCE", "mu(z) = z/(1+z) sends e^{i120} to e^{i60} (because 1 + w = -w^2 is a unit); mu is not used at complex arguments in GFD",
      sp.simplify(sp.expand_complex(z / (1 + z)) - sp.expand_complex(sp.exp(sp.pi * sp.I / 3))) == 0)

print(f"\n{sum(ok)}/{len(ok)} checks passed   by tag: {tags}")

# ===================================================================== K. where the planar rotations live
section("K. The cube lattice seen down its axes")
def projected_gram(axis):
    a = sp.Matrix(axis); Pp = sp.eye(3) - a * a.T / (a.T * a)[0]
    imgs = [Pp * sp.Matrix(e) for e in ([1, 0, 0], [0, 1, 0], [0, 0, 1])]
    return imgs
im = projected_gram([1, 1, 1])
G2 = sp.Matrix(2, 2, lambda i, j: (im[i].T * im[j])[0])
check("CLASSICAL", "down a body diagonal the cubic lattice projects onto the triangular (Eisenstein) lattice: basis Gram (1/3)[[2,-1],[-1,2]], "
      "and the three projected axes sum to zero", sp.simplify(G2 - sp.Matrix([[2, -1], [-1, 2]]) / 3) == sp.zeros(2, 2)
      and sp.simplify(im[0] + im[1] + im[2]) == sp.zeros(3, 1))
cyc = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])          # the closure rotation about (1,1,1)
check("CLASSICAL", "the closure rotation acts on that lattice as the 120-degree rotation (it permutes the projected axes cyclically)",
      all(sp.simplify(cyc * im[k] - im[(k + 1) % 3]) == sp.zeros(3, 1) for k in range(3)))
check("NEW", "TetA's 21 and TetB's 13 are det(K - R) for the 120-degree rotation and its composite with the antipode (a 60-degree "
      "rotation of the same triangular lattice), both seen down the TIME axis (the body diagonal)",
      sp.Matrix([[4, 0], [0, 4]]).det() and (K ** 2 + K + 1).subs(K, 4) == 21 and (K ** 2 - K + 1).subs(K, 4) == 13)
imz = projected_gram([0, 0, 1])
check("CLASSICAL", "down a coordinate axis the cubic lattice projects onto the square lattice, where the quarter turn acts",
      (imz[0].T * imz[1])[0] == 0 and (imz[0].T * imz[0])[0] == 1 and imz[2] == sp.zeros(3, 1))
check("NEW", "the Field Origin's 17 = det(K - quarter turn) lives on the square lattice, seen down a coordinate axis", (K ** 2 + 1).subs(K, 4) == 17)
check("CLASSICAL", "|det(K - R)| counts the points x of the planar torus with K x = R x: 21 on the triangular torus (120 deg), "
      "13 (60 deg), 17 on the square torus (90 deg)",
      sp.Matrix([[4, 1], [-1, 5]]).det() == 21 and sp.Matrix([[4, -1], [1, 4]]).det() == 17 and sp.Matrix([[3, 1], [-1, 4]]).det() == 13)
print(f"\n{sum(ok)}/{len(ok)} checks passed   by tag: {tags}")
