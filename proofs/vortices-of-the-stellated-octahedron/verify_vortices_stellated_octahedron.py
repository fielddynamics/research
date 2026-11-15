"""Verification for 'Vortices of the Stellated Octahedron' (proofs/vortices-of-the-stellated-octahedron).

Self-contained. Two independent parts:

Part I  (exact, no computer algebra): arithmetic in Q(i) and Q(omega) with Python fractions; the
        geometry, the group Td and the most general Td-invariant Hamiltonians are built from scratch.
        Certificates C1-C7 (and S1-S2 for the Triforce split) at random rational parameter points.
Part II (symbolic, sympy, all parameters at once): the pixel's winding block, its secular equation,
        the closed-form circulating current through any half-plane, the corollary without the
        octahedron, the Triforce split W + W' with doubled energies on W, and the standing-wave
        proposition.
Labels match the paper: L = lemma, T = theorem, C = corollary, P = proposition, X = certificate.
Run: python verify_vortices_stellated_octahedron.py
"""
import itertools
import random
from fractions import Fraction as Fr

PASS = FAIL = 0
def check(label, ok):
    global PASS, FAIL
    PASS += bool(ok); FAIL += (not ok)
    print(("PASS " if ok else "FAIL ") + label)


# ---------------------------------------------------------------- exact field Q(theta)
class Q:
    __slots__ = ("a", "b")
    c = -1                                    # theta^2 = c; set per model
    def __init__(self, a=0, b=0):
        self.a, self.b = Fr(a), Fr(b)
    def __add__(s, o): o = cv(o); return Q(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = cv(o); return Q(s.a - o.a, s.b - o.b)
    def __rsub__(s, o): return cv(o) - s
    def __neg__(s): return Q(-s.a, -s.b)
    def __mul__(s, o):
        o = cv(o); return Q(s.a * o.a + Q.c * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def conj(s): return Q(s.a, -s.b)          # theta is imaginary, so this is complex conjugation
    def norm(s): return s.a * s.a - Q.c * s.b * s.b
    def inv(s): n = s.norm(); return Q(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * cv(o).inv()
    def iszero(s): return s.a == 0 and s.b == 0
    def __eq__(s, o): o = cv(o); return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def __repr__(s): return f"({s.a}{'+' if s.b >= 0 else '-'}{abs(s.b)}t)"
def cv(x): return x if isinstance(x, Q) else Q(x, 0)
ZERO = lambda: Q(0, 0)


# ---------------------------------------------------------------- linear algebra over Q
def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum((A[i][k] * B[k][j] for k in range(m)), ZERO()) for j in range(p)] for i in range(n)]
def H_(A): return [[A[j][i].conj() for j in range(len(A))] for i in range(len(A[0]))]
def det_inv(M):
    n = len(M); A = [row[:] + [cv(int(i == j)) for j in range(n)] for i, row in enumerate(M)]; d = cv(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if not A[r][c].iszero()), None)
        if piv is None:
            return ZERO(), None
        if piv != c:
            A[c], A[piv] = A[piv], A[c]; d = -d
        d = d * A[c][c]; iv = A[c][c].inv()
        A[c] = [x * iv for x in A[c]]
        for r in range(n):
            if r != c and not A[r][c].iszero():
                f = A[r][c]; A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return d, [row[n:] for row in A]


def nullspace(M):
    """Exact basis of {x : M x = 0} for a matrix over Q (list of rows)."""
    rows, cols = len(M), len(M[0]); A = [r[:] for r in M]; piv = []; r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if not A[i][c].iszero()), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]; iv = A[r][c].inv(); A[r] = [x * iv for x in A[r]]
        for i in range(rows):
            if i != r and not A[i][c].iszero():
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for fc in free:
        v = [ZERO() for _ in range(cols)]; v[fc] = cv(1)
        for i, pc in enumerate(piv):
            v[pc] = -A[i][fc]
        basis.append(v)
    return basis


# ---------------------------------------------------------------- polynomials over Q (coefficient lists, low first)
def ptrim(p):
    while p and p[-1].iszero():
        p = p[:-1]
    return p
def pinterp(xs, ys):
    """Newton interpolation through (xs, ys); returns coefficients."""
    n = len(xs); coef = list(ys)
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / cv(xs[i] - xs[i - j])
    p = [ZERO()]
    for i in range(n - 1, -1, -1):          # p = p*(x - xs[i]) + coef[i]
        q = [ZERO()] + p
        for k in range(len(p)):
            q[k] = q[k] - p[k] * cv(xs[i])
        q[0] = q[0] + coef[i]; p = q
    return ptrim(p)
def pmod(a, b):
    a = ptrim(list(a)); b = ptrim(list(b))
    while len(a) >= len(b) and a:
        f = a[-1] / b[-1]; sh = len(a) - len(b)
        for k in range(len(b)):
            a[sh + k] = a[sh + k] - f * b[k]
        a = ptrim(a)
    return a
def pgcd_degree(a, b):
    a, b = ptrim(a), ptrim(b)
    while b:
        a, b = b, pmod(a, b)
    return len(a) - 1
def pderiv(p): return ptrim([p[k] * cv(k) for k in range(1, len(p))])


def block_polys(A, ops, G=None):
    """p(x) = det(xG - A) (G = I by default), and for each operator O: f_O(x) = Tr(O adj(xG - A)),
    by exact interpolation. For a simple root E with eigenvector y (A y = E G y):
    y^H O y / y^H G y = f_O(E) / p'(E), so the sign/nonvanishing of f_O at the roots decides."""
    n = len(A)
    if G is None:
        G = [[cv(int(i == j)) for j in range(n)] for i in range(n)]
    xs = [1000 + 7 * j for j in range(n + 1)]
    pv, fv = [], {k: [] for k in ops}
    for x in xs:
        M = [[cv(x) * G[i][j] - A[i][j] for j in range(n)] for i in range(n)]
        d, Minv = det_inv(M)
        assert not d.iszero()
        pv.append(d)
        for k, O in ops.items():
            tr = sum((O[i][j] * Minv[j][i] for i in range(n) for j in range(n)), ZERO())
            fv[k].append(d * tr)                                      # adj = det * inverse
    p = pinterp(xs, pv)
    return p, {k: pinterp(xs[:n], v[:n]) if True else None for k, v in fv.items()}


# ---------------------------------------------------------------- geometry and symmetry
def dot(u, v): return sum(Fr(a) * Fr(b) for a, b in zip(u, v))
def cross(u, v): return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
TA = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
isA = lambda c: c[0] * c[1] * c[2] == 1
def act(R, p): return tuple(sum(R[i][k] * p[k] for k in range(3)) for i in range(3))
signed_perms = []
for pm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        signed_perms.append([[sg[i] if pm[i] == k else 0 for k in range(3)] for i in range(3)])
Td = [R for R in signed_perms if {act(R, v) for v in TA} == set(TA)]


def build(model):
    """sites (as hashable descriptors), positions, edges, Td action on sites."""
    if model == "pixel":
        faces = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        corners = list(itertools.product((1, -1), repeat=3))
        sites = [("O", (0, 0, 0))] + [("F", f) for f in faces] + [("A" if isA(c) else "B", c) for c in corners]
        pos = [tuple(Fr(x) for x in s[1]) for s in sites]
        edges = [(0, i) for i in range(1, len(sites))]
        for i, (ki, fi) in enumerate(sites):
            for j, (kj, cj) in enumerate(sites):
                if ki == "F" and kj in "AB" and dot(fi, cj) == 1:
                    edges.append((i, j))
        def image(R, s): return (s[0], act(R, s[1]))
    else:
        tiles = []
        for name, T in (("A", TA), ("B", [tuple(-x for x in v) for v in TA])):
            for i in range(4):
                f = [T[j] for j in range(4) if j != i]
                mid = lambda p, q: tuple(Fr(a + b, 2) for a, b in zip(p, q))
                tiles.append(("C" + name, frozenset([mid(f[0], f[1]), mid(f[1], f[2]), mid(f[0], f[2])])))
                for k in range(3):
                    v = f[k]; o = [f[j] for j in range(3) if j != k]
                    tiles.append(("E" + name, frozenset([tuple(Fr(x) for x in v), mid(v, o[0]), mid(v, o[1])])))
        sites = [("O", frozenset([(Fr(0), Fr(0), Fr(0))]))] + tiles
        pos = [tuple(sum(p[c] for p in s[1]) / len(s[1]) for c in range(3)) for s in sites]
        edges = [(i, j) for i in range(1, len(sites)) for j in range(i + 1, len(sites)) if len(sites[i][1] & sites[j][1]) == 2]
        edges += [(0, i) for i in range(1, len(sites)) if sites[i][0][0] == "C"]
        def image(R, s): return (s[0], frozenset(act(R, p) for p in s[1]))
    index = {s: i for i, s in enumerate(sites)}
    perms = [[index[image(R, s)] for s in sites] for R in Td]
    return sites, pos, edges, perms, index, image


def orbit_params(n, edges, perms, rng):
    """One random rational value per Td-orbit of sites and of bonds: the most general Td-invariant H."""
    val_site, val_bond = {}, {}
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        o = frozenset(pm[i] for pm in perms)
        val_site.setdefault(o, Fr(rng.randint(-40, 40), rng.randint(1, 9)))
        H[i][i] = val_site[o]
    eset = {frozenset(e) for e in edges}
    for (i, j) in edges:
        o = frozenset(frozenset((pm[i], pm[j])) for pm in perms)
        assert all(e in eset for e in o)
        val_bond.setdefault(o, Fr(rng.choice([1, -1]) * rng.randint(1, 40), rng.randint(1, 9)))
        H[i][j] = H[j][i] = -val_bond[o]
    return H, len(val_site), len(val_bond)


def param_mats(n, edges, perms):
    """One 0/1 matrix per Td-orbit of sites and of bonds: H = sum over orbits of parameter x matrix."""
    out = []; done = set()
    for i in range(n):
        o = frozenset(pm[i] for pm in perms)
        if o not in done:
            done.add(o); M = [[0] * n for _ in range(n)]
            for k in o:
                M[k][k] = 1
            out.append((M, "site"))
    for (i, j) in edges:
        o = frozenset(frozenset((pm[i], pm[j])) for pm in perms)
        if o not in done:
            done.add(o); M = [[0] * n for _ in range(n)]
            for b in o:
                a, c = tuple(b); M[a][c] = M[c][a] = 1
            out.append((M, "bond"))
    return out


def certify(model, axis, Rsym, order, c, lam, us, seeds, split=False):
    Q.c = c
    sites, pos, edges, perms, index, image = build(model)
    n = len(sites)
    print(f"\n=== {model}: {n} sites, {len(edges)} bonds; axis {axis}; symmetry of order {order}; eigenvalue {lam} ===")
    Sperm = [index[image(Rsym, s)] for s in sites]
    check(f"[{model}] the axis symmetry is in Td (keeps TetA): a symmetry of every Td-invariant H",
          any(Rsym == R for R in Td))
    # orbits of the axis symmetry
    seen, orbits = set(), []
    for i in range(n):
        if i in seen:
            continue
        orb = [i]
        while Sperm[orb[-1]] != i:
            orb.append(Sperm[orb[-1]])
        seen |= set(orb); orbits.append(orb)
    on_axis = [i for i in range(n) if cross(pos[i], axis) == (0, 0, 0)]
    full = [o for o in orbits if len(o) == order]
    check(f"[{model}] every site off the axis lies in an orbit of full length {order}; the axis sites lie in shorter orbits, "
          f"so no winding state can live there", all(len(o) < order for o in orbits if set(o) & set(on_axis))
          and all(len(o) == order for o in orbits if not set(o) & set(on_axis)))
    # unnormalised orthogonal basis of the winding space: v[S^j x0] = lam^-j
    lam_pows = [cv(1)]
    for _ in range(order):
        lam_pows.append(lam_pows[-1] * lam)
    check(f"[{model}] the eigenvalue is a primitive {order}th root of unity", lam_pows[order] == cv(1)
          and all(not (lam_pows[k] == cv(1)) for k in range(1, order)))
    linv = lam.inv()
    B = [[ZERO() for _ in full] for _ in range(n)]
    for k, orb in enumerate(full):
        w = cv(1)
        for j, i in enumerate(orb):
            B[i][k] = w; w = w * linv
    m = len(full)
    BB = matmul(H_(B), B)
    check(f"[{model}] winding space has dimension {m}, basis orthogonal with B^H B = {order} I",
          all(BB[i][j] == (cv(order) if i == j else ZERO()) for i in range(m) for j in range(m)))
    P = [[cv(int(Sperm[j] == i)) for j in range(n)] for i in range(n)]
    PB = matmul(P, B)
    check(f"[{model}] each basis vector is an eigenvector of the symmetry with eigenvalue {lam}",
          all(PB[i][k] == lam * B[i][k] for i in range(n) for k in range(m)))
    check(f"[{model}] every winding vector vanishes on the axis (sites {on_axis})",
          all(B[i][k].iszero() for i in on_axis for k in range(m)))
    ring = next(k for k, orb in enumerate(full) if (model == "pixel" and sites[orb[0]][0] == "F")
                or (model == "triforce" and sites[orb[0]][0] == "EA" and (Fr(1), Fr(1), Fr(1)) in sites[orb[0]][1]))

    # half-plane flux operators
    def flux_op(u):
        v = cross(axis, u)
        s = [dot(v, p) for p in pos]
        for i in range(n):
            if s[i] == 0 and i not in on_axis:
                assert dot(u, pos[i]) <= 0, "a site lies on the half-plane: choose another u"
        K = [[ZERO() for _ in range(n)] for _ in range(n)]
        for (i, j) in edges:
            si, sj = s[i], s[j]
            if si * sj < 0:
                t = si / (si - sj)
                x = tuple(pi + t * (pj - pi) for pi, pj in zip(pos[i], pos[j]))
                if dot(u, x) > 0:
                    sg = 1 if si < 0 else -1                 # crossing in the positive sense about the axis, i -> j
                    th = Q(0, 1)                             # theta = i (c = -1) or i*sqrt3 (c = -3): a positive multiple of i
                    K[i][j] = K[i][j] + (-th) * cv(sg)       # J_ij = -i(psi_i* H_ij psi_j - c.c.); H_ij folded in below
                    K[j][i] = K[j][i] + th * cv(sg)
        return K
    for seed in seeds:
        rng = random.Random(seed)
        Hr, nso, nbo = orbit_params(n, edges, perms, rng)
        Hq = [[cv(x) for x in row] for row in Hr]
        commutes = all(Hr[Sperm[i]][Sperm[j]] == Hr[i][j] for i in range(n) for j in range(n))
        td = all(Hr[pm[i]][pm[j]] == Hr[i][j] for pm in perms for i in range(n) for j in range(n))
        sym = all(Hr[i][j] == Hr[j][i] for i in range(n) for j in range(n))
        A = matmul(H_(B), matmul(Hq, B))
        A_full = A
        Ks = []
        for u in us:
            K0 = flux_op(u)
            Kfull = [[K0[i][j] * cv(Hr[i][j]) for j in range(n)] for i in range(n)]
            Ks.append(matmul(H_(B), matmul(Kfull, B)))
        Rop = [[cv(int(i == j == ring)) for j in range(m)] for i in range(m)]
        ops = {"flux": Ks[0], "ring": Rop}
        for t in range(1, len(Ks)):
            ops[f"diff{t}"] = [[Ks[0][i][j] - Ks[t][i][j] for j in range(m)] for i in range(m)]
        G = None
        if split:
            # W: winding vectors on outer tiles that no parameter couples to a central tile; W' its complement
            cent_k = [k for k, orb in enumerate(full) if sites[orb[0]][0][0] == "C"]
            out_k = [k for k in range(m) if k not in cent_k]
            rowsC = []
            for (Hk, _) in param_mats(n, edges, perms):
                Ak = matmul(H_(B), matmul([[cv(x) for x in row] for row in Hk], B))
                rowsC += [[Ak[i][j] for j in out_k] for i in cent_k]
            Nn = nullspace(rowsC)
            Wb = [[ZERO() for _ in Nn] for _ in range(m)]
            for cidx, vec in enumerate(Nn):
                for a, k in enumerate(out_k):
                    Wb[k][cidx] = vec[a]
            AW = matmul(A, Wb)
            # A W inside W: W'^T-test: the component of A W orthogonal to W vanishes
            Wp_rows = nullspace(H_(Wb))                                  # basis of the orthogonal complement W'
            Wp = [[Wp_rows[c][r] for c in range(len(Wp_rows))] for r in range(m)]
            invariant = all(x.iszero() for row in matmul(H_(Wp), AW) for x in row)
            check(f"[{model}/{seed}] S1 W (winding vectors on outer tiles uncoupled to every central tile) has dimension "
                  f"{len(Nn)} and A maps it into itself; so does its orthogonal complement W' (dimension {len(Wp_rows)})",
                  len(Nn) == 4 and invariant)
            pW, _ = block_polys(matmul(H_(Wb), AW), {}, matmul(H_(Wb), Wb))
            check(f"[{model}/{seed}] S2 on W every energy is doubled: det(xG - A_W) is the square of a quadratic "
                  f"(gcd(p_W, p_W') has degree 2)", pgcd_degree(pW, pderiv(pW)) == 2 and len(pW) - 1 == 4)
            proj = lambda O: matmul(H_(Wp), matmul(O, Wp))
            A, G = proj(A), matmul(H_(Wp), Wp)
            ops = {k: proj(O) for k, O in ops.items()}
            m_eff = len(Wp_rows)
        p, f = block_polys(A, ops, G)
        real_coeffs = all(cf.b == 0 for cf in p)
        sqfree = pgcd_degree(p, pderiv(p)) == 0
        indep = all(not pmod(f[f"diff{t}"], p) for t in range(1, len(Ks)))
        flux_ok = pgcd_degree(p, f["flux"]) == 0
        ring_ok = pgcd_degree(p, f["ring"]) == 0
        # antivortex: conjugate basis gives conjugate block; flux operator flips sign
        Bc = [[x.conj() for x in row] for row in B]
        Ac = matmul(H_(Bc), matmul(Hq, Bc))
        Kc = matmul(H_(Bc), matmul([[flux_op(us[0])[i][j] * cv(Hr[i][j]) for j in range(n)] for i in range(n)], Bc))
        anti = all(Ac[i][j] == A_full[i][j].conj() for i in range(m) for j in range(m)) and \
               all(Kc[i][j] == -(Ks[0][i][j].conj()) for i in range(m) for j in range(m))
        print(f"  seed {seed}: {nso} site and {nbo} bond parameters (random rationals); deg p = {len(p) - 1}")
        check(f"[{model}/{seed}] C1 H is real symmetric, Td-invariant, and commutes with the axis symmetry", commutes and td and sym)
        where = "on W'" if split else "on the winding space"
        check(f"[{model}/{seed}] C3 {where} the characteristic polynomial is real and squarefree "
              f"(gcd(p, p') = 1: {len(p) - 1} distinct vortex energies)", real_coeffs and sqfree)
        check(f"[{model}/{seed}] C4 {where}: the flux through the half-plane is the same for {len(us)} different half-planes "
              f"(p divides each difference)", indep)
        check(f"[{model}/{seed}] C5 {where}: every eigenstate carries a nonzero circulating current (gcd(p, flux) = 1)", flux_ok)
        check(f"[{model}/{seed}] C6 {where}: the ring turns in every eigenstate (gcd(p, ring) = 1)", ring_ok)
        check(f"[{model}/{seed}] C7 the complex conjugate is an antivortex: conjugate block, opposite flux", anti)



print("PART I: exact certificates (pure Python, no computer algebra)")
omega = Q(Fr(-1, 2), Fr(1, 2))     # (-1 + theta)/2 with theta^2 = -3
certify("pixel", axis=(0, 0, 1), Rsym=[[0, -1, 0], [1, 0, 0], [0, 0, -1]], order=4, c=-1, lam=Q(0, 1),
        us=[(2, 1, 0), (1, 3, 0), (-1, 2, 0)], seeds=[1, 2, 3])
Q.c = -3
certify("triforce", axis=(1, 1, 1), Rsym=[[0, 0, 1], [1, 0, 0], [0, 1, 0]], order=3, c=-3, lam=omega,
        us=[(3, -1, -2), (1, 4, -5), (-2, 5, -3)], seeds=[1, 2, 3], split=True)


# ======================================================================================
print("\nPART II: symbolic, all parameters at once (sympy)")
import sympy as sp


def Ssimp(z):
    """Exact simplification for expressions in sqrt(3) and i: rationalise, split real and imaginary parts."""
    z = sp.expand_complex(sp.radsimp(sp.expand(z)))
    return sp.nsimplify(sp.simplify(sp.re(z))) + sp.I * sp.nsimplify(sp.simplify(sp.im(z)))


def symbolic(model, names_site, names_bond):
    sites, pos, edges, perms, index, image = build(model)
    n = len(sites)
    H = sp.zeros(n, n); site_sym, bond_sym = {}, {}
    for i in range(n):
        o = frozenset(pm[i] for pm in perms)
        if o not in site_sym:
            site_sym[o] = sp.Symbol(names_site(sites[i], len(site_sym)), real=True)
        H[i, i] = site_sym[o]
    for (i, j) in edges:
        o = frozenset(frozenset((pm[i], pm[j])) for pm in perms)
        if o not in bond_sym:
            bond_sym[o] = sp.Symbol(names_bond(sites[i], sites[j], len(bond_sym)), real=True)
        H[i, j] = H[j, i] = -bond_sym[o]
    return sites, pos, edges, perms, index, image, H, list(site_sym.values()), list(bond_sym.values())


def winding_basis(sites, index, image, R, lam, order):
    n = len(sites); Sp = [index[image(R, s)] for s in sites]
    seen, orbits = set(), []
    for i in range(n):
        if i in seen:
            continue
        o = [i]
        while Sp[o[-1]] != i:
            o.append(Sp[o[-1]])
        seen |= set(o); orbits.append(o)
    full = [o for o in orbits if len(o) == order]
    B = sp.zeros(n, len(full))
    for k, o in enumerate(full):
        for j, i in enumerate(o):
            B[i, k] = sp.expand(lam ** (-j))
    P = sp.zeros(n, n)
    for i in range(n):
        P[Sp[i], i] = 1
    return B, full, P


def flux_matrix(H, pos, edges, axis, u, n):
    axis, u = sp.Matrix(axis), sp.Matrix(u); v = axis.cross(u)
    P_ = [sp.Matrix([sp.Rational(c) for c in p]) for p in pos]
    s_ = [(v.T * p)[0] for p in P_]
    K = sp.zeros(n, n)
    for (i, j) in edges:
        if s_[i] * s_[j] < 0:
            t = s_[i] / (s_[i] - s_[j]); x = P_[i] + t * (P_[j] - P_[i])
            if (u.T * x)[0] > 0:
                sg = 1 if s_[i] < 0 else -1
                K[i, j] += -sp.I * sg * H[i, j]; K[j, i] += sp.I * sg * H[j, i]
    return K


# ---------------- the pixel ----------------
pix_site = lambda s, k: {"O": "Delta", "F": "Delta_f", "A": "epsilon_A", "B": "epsilon_B"}[s[0]]
pix_bond = lambda a, b, k: {frozenset("OF"): "t_f", frozenset("OA"): "t_A", frozenset("OB"): "t_B",
                            frozenset("FA"): "c_A", frozenset("FB"): "c_B"}[frozenset(a[0] + b[0])]
sites, pos, edges, perms, index, image, Hs, ssyms, bsyms = symbolic("pixel", pix_site, pix_bond)
n = len(sites)
D_, Df, eA, eB = [sp.Symbol(x, real=True) for x in ("Delta", "Delta_f", "epsilon_A", "epsilon_B")]
tf_, tA_, tB_, cA, cB = [sp.Symbol(x, real=True) for x in ("t_f", "t_A", "t_B", "c_A", "c_B")]
S4 = [[0, -1, 0], [1, 0, 0], [0, 0, -1]]
B, full, P = winding_basis(sites, index, image, S4, sp.I, 4)
kinds = [sites[o[0]][0] for o in full]
order_idx = [kinds.index("F"), kinds.index("A"), kinds.index("B")]
B = B.extract(list(range(n)), order_idx)
check("T1 [pixel] the most general Td-invariant H has 9 parameters and commutes with the rotoreflection S",
      len(ssyms) + len(bsyms) == 9 and P * Hs == Hs * P)
Ap = (B.H * Hs * B / 4).applyfunc(sp.simplify)
a_, b_ = Ap[0, 1], Ap[0, 2]
check("T1 [pixel] the winding block (ring, TetA, TetB) is [[Delta_f, a, b], [conj a, eps_A, 0], [conj b, 0, eps_B]] "
      "with |a|^2 = 2 c_A^2, |b|^2 = 2 c_B^2; Delta, t_f, t_A, t_B drop out",
      Ap[0, 0] == Df and Ap[1, 1] == eA and Ap[2, 2] == eB and Ap[1, 2] == 0 and Ap[2, 1] == 0
      and sp.simplify(a_ * sp.conjugate(a_) - 2 * cA**2) == 0 and sp.simplify(b_ * sp.conjugate(b_) - 2 * cB**2) == 0
      and not (Ap.free_symbols & {D_, tf_, tA_, tB_}))
E = sp.Symbol("E", real=True); rr = sp.Symbol("r", positive=True)
charp = sp.expand((E * sp.eye(3) - Ap).det())
check("T1 [pixel] its characteristic polynomial is (E - Delta_f)(E - eps_A)(E - eps_B) - 2c_A^2(E - eps_B) - 2c_B^2(E - eps_A)",
      sp.simplify(charp - ((E - Df) * (E - eA) * (E - eB) - 2 * cA**2 * (E - eB) - 2 * cB**2 * (E - eA))) == 0)
sec = (E - Df) - 2 * cA**2 / (E - eA) - 2 * cB**2 / (E - eB)
check("T1 [pixel] the secular function is strictly increasing between its poles, so the three energies are distinct "
      "(derivative 1 + 2c_A^2/(E - eps_A)^2 + 2c_B^2/(E - eps_B)^2 > 0)",
      sp.simplify(sp.diff(sec, E) - (1 + 2 * cA**2 / (E - eA)**2 + 2 * cB**2 / (E - eB)**2)) == 0)
check("T1 [pixel] det(H+ - E) is 2c_A^2(eps_A - eps_B) at E = eps_A and 2c_B^2(eps_B - eps_A) at E = eps_B",
      sp.simplify((Ap - E * sp.eye(3)).det().subs(E, eA) - 2 * cA**2 * (eA - eB)) == 0
      and sp.simplify((Ap - E * sp.eye(3)).det().subs(E, eB) - 2 * cB**2 * (eB - eA)) == 0)
w = sp.Matrix([rr, sp.conjugate(a_) * rr / (E - eA), sp.conjugate(b_) * rr / (E - eB)])
psi = B * w
Dfsol = E - 2 * cA**2 / (E - eA) - 2 * cB**2 / (E - eB)                    # Delta_f from the secular equation
check("T1 [pixel] on a root of the secular equation, psi = B w is an exact stationary state of the full 15-site H, "
      "with amplitude r on every ring site and the corners locked to it",
      sp.simplify((Hs * psi - E * psi).subs(Df, Dfsol)) == sp.zeros(n, 1)
      and all(sp.simplify(sp.Abs(psi[i]) - rr) == 0 for i in range(n) if sites[i][0] == "F" and sites[i][1][2] == 0))
ok_I = True
for u in ([2, 1, 0], [1, 3, 0], [-1, 2, 0]):
    K = flux_matrix(Hs, pos, edges, (0, 0, 1), u, n)
    Iu = sp.simplify((psi.H * K * psi)[0])
    ok_I &= sp.simplify((Iu - (-(E - Df) * rr**2)).subs(Df, Dfsol)) == 0
check("T1 [pixel] the circulating current through each of three half-planes is I = -(E - Delta_f) r^2 "
      "(r: amplitude on each site of the octahedron's ring)", ok_I)
check("T1 [pixel] so I != 0 unless E = Delta_f, which needs c_A^2 (Delta_f - eps_B) + c_B^2 (Delta_f - eps_A) = 0",
      sp.simplify(charp.subs(E, Df) - (-2 * cA**2 * (Df - eB) - 2 * cB**2 * (Df - eA))) == 0)
check("T1 [pixel] at eps_A = eps_B, E = eps_A is a vortex energy with r = 0 (no current)",
      sp.simplify(charp.subs(eB, eA).subs(E, eA)) == 0)
keep = [i for i in range(n) if sites[i][0] != "F"]
H9 = Hs.extract(keep, keep); B9 = B.extract(keep, [1, 2])
check("C1 [pixel without the octahedron] winding states exist (dimension 2) but vanish at the Field Origin, and every "
      "bond touches it: no current, no vortex",
      all(B9[0, k] == 0 for k in range(2)) and all(H9[i, j] == 0 for i in range(1, 9) for j in range(1, 9) if i != j))

# standing waves
tt = sp.Symbol("t", real=True)
psi_t = sp.exp(-sp.I * E * tt) * psi
tau = sp.pi / (2 * E)
check("P1 [standing wave] applying the quarter-turn symmetry to the evolving vortex equals shifting it in time: "
      "S psi(t) = psi(t - pi/(2E)), so the stationary pattern rotates",
      sp.simplify(P * psi_t - sp.exp(-sp.I * E * (tt - tau)) * psi) == sp.zeros(n, 1))
phi = (psi + psi.applyfunc(sp.conjugate)).applyfunc(sp.simplify)
check("P1 [standing wave] vortex + antivortex is real, stationary at the same energy, and carries no current on any bond",
      all(sp.simplify(sp.im(x)) == 0 for x in phi)
      and sp.simplify((Hs * phi - E * phi).subs(Df, Dfsol)) == sp.zeros(n, 1)
      and all(sp.simplify(sp.im(sp.conjugate(phi[i]) * Hs[i, j] * phi[j])) == 0 for (i, j) in edges))
check("P1 [standing wave] the vortex's density |psi(t)|^2 is the same at all times", all(
      sp.simplify(sp.Abs(psi_t[i])**2 - sp.Abs(psi[i])**2) == 0 for i in range(n)))

# ---------------- the Triforce ----------------
tri_site = lambda s, k: f"e{k}"
tri_bond = lambda a, b, k: f"t{k}"
sites, pos, edges, perms, index, image, Ht, ssyms, bsyms = symbolic("triforce", tri_site, tri_bond)
n = len(sites)
w3 = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2
C3 = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
B, full, P = winding_basis(sites, index, image, C3, w3, 3)
params = ssyms + bsyms
check("T2 [Triforce] the most general Td-invariant H has 15 parameters and commutes with the 120-degree rotation about the leg",
      len(params) == 15 and P * Ht == Ht * P)
A = (B.H * Ht * B).applyfunc(Ssimp)
cent_k = [k for k, o in enumerate(full) if sites[o[0]][0][0] == "C"]
out_k = [k for k in range(len(full)) if k not in cent_k]
rows = [A.applyfunc(lambda z: sp.diff(z, p)).extract(cent_k, out_k) for p in params]
N = sp.Matrix.vstack(*rows).nullspace()
W = sp.zeros(len(full), len(N))
for c_, v in enumerate(N):
    for a, k in enumerate(out_k):
        W[k, c_] = v[a]
G = (W.H * W).applyfunc(Ssimp)
MW = (G.inv() * W.H * A * W).applyfunc(Ssimp)
check("T2 [Triforce] W (winding vectors on outer tiles that no parameter couples to a central tile) has dimension 4 and "
      "every H maps it into itself", len(N) == 4 and (A * W - W * MW).applyfunc(Ssimp) == sp.zeros(len(full), 4))
pairs = [(i, j) for i in range(4) for j in range(i + 1, 4) if Ssimp(MW[i, j]) != 0]
b1, b2 = pairs[0], pairs[1]
M1, M2 = MW.extract(list(b1), list(b1)), MW.extract(list(b2), list(b2))
cp1, cp2 = Ssimp((E * sp.eye(2) - M1).det()), Ssimp((E * sp.eye(2) - M2).det())
check("T2 [Triforce] on W, H is two copies of the same 2x2 problem: every energy on W is doubled, for all parameters",
      len(pairs) == 2 and set(b1) | set(b2) == {0, 1, 2, 3} and Ssimp(cp1 - cp2) == 0)
Wp_ = (W.H).nullspace()
check("T2 [Triforce] the orthogonal complement W' has dimension 6 and every H maps it into itself",
      len(Wp_) == 6 and all(Ssimp(x) == 0 for x in (sp.Matrix.hstack(*Wp_).H * A * W)))

# circulation on W's doubled levels depends on the parameters: exact points of both signs
Kt = flux_matrix(Ht, pos, edges, (1, 1, 1), (3, -1, -2), n)
KW = (W.H * B.H * Kt * B * W)
def piece_vec(Mp, idx, Ev):
    y = sp.zeros(4, 1); y[idx[0]] = Mp[0, 1]; y[idx[1]] = Ev - Mp[0, 0]
    return y
rngW = random.Random(17); found = set(); tries = 0
while found != {1, -1} and tries < 60:
    tries += 1
    val = {p_: sp.Rational(rngW.randint(-30, 30), rngW.randint(1, 7)) for p_ in params}
    M1v, M2v, KWv, Gv = M1.subs(val), M2.subs(val), KW.subs(val), G
    for Ev in sp.solve(sp.expand(cp1.subs(val)), E):
        y1, y2 = piece_vec(M1v, b1, Ev), piece_vec(M2v, b2, Ev)
        F = sp.Matrix([[(y1.H * KWv * y1)[0], (y1.H * KWv * y2)[0]], [(y2.H * KWv * y1)[0], (y2.H * KWv * y2)[0]]])
        d = sp.N(Ssimp(F.det()), 60)
        if abs(d) > 1e-30:
            found.add(1 if d > 0 else -1)
check("T2 [Triforce] on W, the circulation form of a doubled level is definite at some parameter points (every "
      "combination circulates) and indefinite at others (a standing combination exists): exact roots, both found",
      found == {1, -1})
print(f"\n{PASS}/{PASS + FAIL} checks passed")
raise SystemExit(FAIL)
