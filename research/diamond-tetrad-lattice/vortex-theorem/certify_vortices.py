"""Exact certificates for THEOREM.md, written independently of the sympy scripts.

No computer-algebra system: exact arithmetic in Q(theta), theta^2 = -1 (the field Q(i)) or
theta^2 = -3 (the field Q(omega), omega = (-1 + theta)/2), with Python Fractions. The geometry,
the symmetry group, the Hamiltonians and every certificate are built here from scratch.

For each model (the 15-site pixel about an octahedron axis; the 33-tile Triforce model about a leg)
and for several random rational parameter points it certifies, exactly:
  C1  the axis symmetry commutes with H, H is real symmetric, the symmetry group Td is respected;
  C2  the winding space (symmetry eigenvalue i or omega) and that every vector in it vanishes on the axis;
  C3  the winding block A = B^H H B has a squarefree characteristic polynomial p (gcd(p, p') = 1);
  C4  current conservation makes the half-plane flux the same for every half-plane: p divides
      Tr((K_u - K_v) adj(xI - A)) for three different half-planes u, v;
  C5  the circulating current is nonzero in every vortex eigenstate: gcd(p, Tr(K adj(xI - A))) = 1;
  C6  the ring turns in every vortex eigenstate: gcd(p, adj(xI - A)[ring, ring]) = 1;
  C7  complex conjugation gives the antivortex: same p (real coefficients), opposite flux.
Run: python certify_vortices.py
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


omega = Q(Fr(-1, 2), Fr(1, 2))     # (-1 + theta)/2 with theta^2 = -3
certify("pixel", axis=(0, 0, 1), Rsym=[[0, -1, 0], [1, 0, 0], [0, 0, -1]], order=4, c=-1, lam=Q(0, 1),
        us=[(2, 1, 0), (1, 3, 0), (-1, 2, 0)], seeds=[1, 2, 3])
Q.c = -3
certify("triforce", axis=(1, 1, 1), Rsym=[[0, 0, 1], [1, 0, 0], [0, 1, 0]], order=3, c=-3, lam=omega,
        us=[(3, -1, -2), (1, 4, -5), (-2, 5, -3)], seeds=[1, 2, 3], split=True)
print(f"\n{PASS}/{PASS + FAIL} certificates passed")
raise SystemExit(FAIL)
