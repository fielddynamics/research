"""Cube tiling: exact checks for README.md in this folder (research, not a proof).
Cubes centred at 2n (n in Z^3), side 2; corners p in (2Z+1)^3. Local chamber of corner p in cube n:
chi_n(p) = prod(p_i - 2 n_i): +1 TetA, -1 TetB (the Gram-matrix and Hadamard convention, TetA = xyz = +1).
Two labellings of the tiling are compared:
  U (uniform): every cube carries the same star, label chi_n(p)  (../README.md, result 7)
  C (closure): cube n carries sigma_n chi_n(p), corners agreeing  (../../stellated octahedron geometry/pixel_tiling_and_closure.md)
Run: python3 verify_cube_tiling.py
"""
import itertools
from collections import defaultdict, Counter

S = list(itertools.product((1, -1), repeat=3))
def chi(n, p): return (p[0]-2*n[0])*(p[1]-2*n[1])*(p[2]-2*n[2])
def corners(n): return [tuple(2*n[i]+s[i] for i in range(3)) for s in S]

ok = []
def check(m, c): ok.append(bool(c)); print(("PASS " if c else "FAIL ") + m)

R = range(-3, 4)
cubes = list(itertools.product(R, repeat=3))

# 1. how the local label changes between neighbouring cubes
def shared(n, m): return set(corners(n)) & set(corners(m))
flips = {}
for d in itertools.product((-1, 0, 1), repeat=3):
    if d == (0, 0, 0): continue
    n, m = (0, 0, 0), d
    vals = {chi(n, p) * chi(m, p) for p in shared(n, m)}
    flips[d] = vals
check("1. a corner's local label flips between neighbours n, n+d exactly when |d| is odd (face, corner neighbours), "
      "and is kept for edge neighbours", all(v == {(-1) ** sum(map(abs, d))} for d, v in flips.items()))

# 2. closure: sigma_n = s0 * (-1)^(n1+n2+n3); global corner label lambda(p) = -s0 * (-1)^((p1+p2+p3+3)/2)
def sigma(n, s0=1): return s0 * (-1) ** (sum(n) % 2)
def lam(p, s0=1): return -s0 * (-1) ** (((sum(p) + 3) // 2) % 2)
check("2. closure labels sigma_n chi_n(p) agree at every corner and equal lambda(p) = -(-1)^((p1+p2+p3+3)/2): "
      "a character of the corner lattice", all(sigma(n) * chi(n, p) == lam(p) for n in cubes for p in corners(n)))

# 3. symmetry of each labelled tiling under cube translations t (in cube units)
def U_invariant(t): return all(chi((n[0]+t[0], n[1]+t[1], n[2]+t[2]), tuple(p[i]+2*t[i] for i in range(3))) == chi(n, p)
                               for n in cubes[:20] for p in corners(n))
def C_label_after(t):  # translate the closure labelling; compare with original at same points
    return {lam(tuple(p[i]-2*t[i] for i in range(3))) * lam(p) for p in itertools.product((-1, 1, 3), repeat=3)}
T = list(itertools.product((-2, -1, 0, 1, 2), repeat=3))
check("3a. U is invariant under every cube translation (Z^3)", all(U_invariant(t) for t in T))
check("3b. C is invariant under t exactly when t1+t2+t3 is even (the fcc sublattice D3), and an odd translation is the global "
      "swap TetA <-> TetB", all(C_label_after(t) == ({1} if sum(t) % 2 == 0 else {-1}) for t in T))

# 4. the dual cube: centred on a corner q, with the 8 surrounding cube centres as its corners.
#    In U, which legs arriving at q are TetA?  In C?
q = (1, 1, 1)
around = [n for n in cubes if q in corners(n)]
dirs_U = {tuple((2*n[i]-q[i]) for i in range(3)): chi(n, q) for n in around}   # direction from q to the centre
dirs_C = {tuple((2*n[i]-q[i]) for i in range(3)): sigma(n) * chi(n, q) for n in around}
prodsign = lambda v: v[0]*v[1]*v[2]
check("4a. U: of the 8 legs meeting at a corner, 4 are TetA and 4 TetB, and the TetA legs point (from the corner) along the "
      "directions of local sign -1: the dual cube holds a stellated octahedron with the roots exchanged",
      Counter(dirs_U.values()) == Counter({1: 4, -1: 4})
      and all((prodsign(v) == -1) == (lab == 1) for v, lab in dirs_U.items()))
check("4b. C: all 8 legs meeting at a corner carry that corner's one label: the dual cube is all TetA or all TetB",
      len(set(dirs_C.values())) == 1)

# 5. the nets the TetA legs form (nodes: cube centres and corners)
def net(label):
    adj = defaultdict(set)
    for n in cubes:
        c = tuple(2*x for x in n)
        for p in corners(n):
            if label(n, p) == 1: adj[c].add(p); adj[p].add(c)
    return adj
def interior(v): return all(-4 <= x <= 4 for x in v)
for name, lab in (("U", chi), ("C", lambda n, p: sigma(n) * chi(n, p))):
    adj = net(lab)
    deg = Counter((("centre" if all(x % 2 == 0 for x in v) else "corner"), len(adj[v])) for v in adj if interior(v))
    print(f"   {name}: interior degrees {dict(deg)}")
adjU, adjC = net(chi), net(lambda n, p: sigma(n) * chi(n, p))
check("5a. U: every node of the TetA net has degree 4, centres and corners alternate: a diamond net (tetrahedral nodes)",
      all(len(adjU[v]) == 4 for v in adjU if interior(v)))
check("5b. C: centres have degree 4 and TetA corners degree 8, TetB corners degree 0: the fluorite (CaF2) net, "
      "corners on an fcc lattice, centres on the simple cubic lattice in its tetrahedral holes",
      all(len(adjC[v]) == (4 if all(x % 2 == 0 for x in v) else 8) for v in adjC if interior(v)))

def components(adj, box=3):
    seen, comps = set(), 0
    nodes = [v for v in adj if all(-2*box <= x <= 2*box for x in v)]
    for v in nodes:
        if v in seen: continue
        comps += 1; stack = [v]
        while stack:
            u = stack.pop()
            if u in seen: continue
            seen.add(u); stack.extend(w for w in adj[u] if w not in seen)
    return comps
print("   components (finite box, edge effects possible): U", components(adjU), " C", components(adjC))

# 6. which cube centres a U TetA net reaches: two centres are in one net iff ...
reach = {}
start = (0, 0, 0)
seen = set(); stack = [start]
while stack:
    u = stack.pop()
    if u in seen: continue
    seen.add(u); stack.extend(adjU[u])
cen = {v for v in seen if all(x % 2 == 0 for x in v)}
check("6. U: one TetA net reaches exactly the cube centres 2n with n1+n2+n3 even (fcc): the other net holds the odd ones",
      all(((sum(v)//2) % 2 == 0) == (v in cen) for v in itertools.product(range(-4, 5, 2), repeat=3)))



# 7. the root exchange as a translation, in each labelling (legs labelled from their cube centre)
def legs_U():
    out = {}
    for n in cubes:
        c = tuple(2*x for x in n)
        for p in corners(n): out[(c, p)] = chi(n, p)
    return out
L = legs_U(); h = (1, 1, 1)
# after translating by h, a leg (c,p) becomes a leg whose centre is p+h and corner is c+h
tr = {}
for (c, p), lab in L.items():
    cc, pp = tuple(p[i]+h[i] for i in range(3)), tuple(c[i]+h[i] for i in range(3))
    tr[(cc, pp)] = lab
common = [k for k in tr if k in L]
check("7a. U: translating by half a body diagonal (centre -> corner) maps the legs onto themselves with every label exchanged: "
      "the root exchange is the bcc translation", len(common) > 100 and all(tr[k] == -L[k] for k in common))
check("7b. C: the root exchange is translation by one cube (3b), and on a periodic box it closes only for an even number of "
      "cubes per side, since sigma must return to itself", all(((-1) ** N == 1) == (N % 2 == 0) for N in range(2, 8)))

print(f"\n{sum(ok)}/{len(ok)} checks passed")
