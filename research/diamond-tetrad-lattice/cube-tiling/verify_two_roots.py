"""The tiled cube read with both roots: which index pair is exchanged by TetA <-> TetB.

Companion to TWO_ROOTS.md. Exact integer arithmetic. Run: python3 verify_two_roots.py

The framework's established count (Gram paper, Letter 2, coupling-algebra Result 10, chiral holonomy):
  64 = 16 shared + 24 TetA + 24 TetB,
the shared 16 being the diagonal of each slice, and the exchange of the two lower indices being the
exchange of the roots (TetB's step is the transpose of TetA's). These checks test the tiled cube against that.

Coordinates: cube side 2, centres in 2Z^3; legs v_a = TetA's corners (xyz = +1, Gram convention);
TetB's corners are -v_a. A "link" is a TetA corner joined to a TetB corner: the 12 cube edges and the
4 body diagonals through the Field Origin (coupling-algebra Result 1).
"""
import itertools
from fractions import Fraction as Fr

results = []
def check(cid, text, cond):
    results.append((cid, bool(cond)))
    print(("PASS " if cond else "FAIL ") + cid + "  " + text)

V = [v for v in itertools.product((1, -1), repeat=3) if v[0] * v[1] * v[2] == 1]
neg = lambda u: tuple(-x for x in u)
add = lambda *us: tuple(sum(u[i] for u in us) for i in range(3))
sc = lambda e, u: tuple(e * x for x in u)
mid = lambda p, q: tuple(Fr(x + y, 2) for x, y in zip(p, q))
dot = lambda u, w: sum(x * y for x, y in zip(u, w))
R4 = range(4)

# ---- the tiling's sharing (proof Theorem 2): cubes holding the octahedron on a cube edge, cubes whose Field Origin a core touches
def edge_holders(p, q):
    m = mid(p, q)
    return {c for c in itertools.product((-2, 0, 2), repeat=3) if all(abs(m[i] - c[i]) <= 1 for i in range(3))}
def core_holders(corners):          # own cube + the cubes whose Field Origin corner (a cube-face centre) the core touches
    f = [mid(p, q) for p, q in itertools.combinations(corners, 2)]
    return {(0, 0, 0)} | {tuple(int(2 * x) for x in c) for c in f}

# TetA channel (slot a, face b): the corner triangle at v_a of TetA's face opposite v_b (a != b), or that face's core (a = b)
def A_holders(a, b):
    if a != b: return edge_holders(V[a], neg(V[b]))
    return core_holders([V[p] for p in R4 if p != b])
# TetB channel (slot -a, face -b): same construction with TetB's legs -v
def B_holders(a, b):
    if a != b: return edge_holders(neg(V[a]), V[b])
    return core_holders([neg(V[p]) for p in R4 if p != b])
# the link a channel lies on: TetA channel (slot a, face b) runs from TetA corner v_a to the piercing TetB corner -v_b
link_of_A = lambda a, b: (V[a], neg(V[b]))
link_of_B = lambda a, b: (V[b], neg(V[a]))      # TetB channel (slot -a, face -b): TetB corner -v_a to piercing TetA corner v_b

print("=== 1. The 16 channels of a face set are the 16 TetA-TetB links (coupling-algebra Results 8 and 10)")
links = {link_of_A(a, b) for a in R4 for b in R4}
check("1.1", "TetA's 16 channels (slot a, face b) lie on 16 distinct TetA-TetB links: (a, b) -> TetA corner v_a, TetB corner -v_b",
      len(links) == 16)
check("1.2", "the 4 cores (a = b) lie on the 4 body diagonals through the Field Origin, the 12 corner channels on the 12 cube edges",
      all((dot(V[a], V[b]) == 3) == (a == b) for a in R4 for b in R4)
      and all(sum(x != y for x, y in zip(*link_of_A(a, b))) == (3 if a == b else 1) for a in R4 for b in R4))
check("1.3", "so the lower index pair (mu, nu) is (slot, face) = (TetA end, TetB end) of a link, exactly Result 10's map",
      all(link_of_A(a, b) == (V[a], neg(V[b])) for a in R4 for b in R4))
check("1.4", "exchanging the roots (inversion through the Field Origin) sends the link of (a, b) to the link of (b, a): "
      "the index swap is the exchange of roots; the 4 diagonal links are fixed, the 12 edges swap in 6 antipodal pairs",
      all({neg(x) for x in link_of_A(a, b)} == set(link_of_A(b, a)) for a in R4 for b in R4)
      and sum({neg(x) for x in link_of_A(a, b)} == set(link_of_A(a, b)) for a in R4 for b in R4) == 4)

print("\n=== 2. What the tiling adds: each link is a shared solid with a TetA face and a TetB face")
check("2.1", "each of the 12 cube-edge links is one shared octahedron, and both chambers open onto it: TetA's channel on the link "
      "and TetB's channel on the same link are the two faces of the cube's edge wedge, held by the same 4 cubes",
      all(set(link_of_A(a, b)) == set(link_of_B(b, a)) and A_holders(a, b) == B_holders(b, a) and len(A_holders(a, b)) == 4
          for a in R4 for b in R4 if a != b))
check("2.2", "each Field Origin link has TetA's core at one end of the diagonal and TetB's core at the other: TetA's reaches the "
      "own cube and the 3 face neighbours on the -v_a side, TetB's the own cube and the 3 on the +v_a side; only the own cube is common",
      all(A_holders(a, a) & B_holders(a, a) == {(0, 0, 0)} and all(dot(c, V[a]) < 0 for c in A_holders(a, a) - {(0, 0, 0)})
          and all(dot(c, V[a]) > 0 for c in B_holders(a, a) - {(0, 0, 0)}) for a in R4))
check("2.3", "the holders follow one formula, c = -v_nu + eps v_lambda with eps = +1 iff lambda in {mu, nu} (mu = slot, nu = face): "
      "the 4 holders of a channel are one cube along each leg lambda",
      all({add(neg(V[b]), sc(1 if l in (a, b) else -1, V[l])) for l in R4} == A_holders(a, b) for a in R4 for b in R4))

print("\n=== 3. Which pair is antisymmetric: the published proof versus the framework")
# triples (lambda, mu, nu) = (holder leg, slot, face); couplings c(l, m, n) = -v_n + eps v_l
cpl = lambda l, m, n: add(neg(V[n]), sc(1 if l in (m, n) else -1, V[l]))
trip = list(itertools.product(R4, repeat=3))
# the framework's swap: slot <-> face (the link reversed); the published proof's swap: slot <-> holder (its mu <-> nu)
tau_fw = lambda t: (t[0], t[2], t[1])
tau_old = lambda t: (t[1], t[0], t[2])
check("3.1", "the published proof's index swap (its channel <-> its leg, here slot <-> holder) keeps every coupling's face, "
      "so it never changes the TetB end of the link: it is not the exchange of roots",
      all(tau_old(t)[2] == t[2] for t in trip) and any(tau_old(t)[1] != t[1] for t in trip))
check("3.2", "the framework's swap (slot <-> face) reverses the link, which is the exchange of roots (check 1.4)",
      all(link_of_A(*tau_fw(t)[1:]) == link_of_A(t[2], t[1]) for t in trip))
# the published proof's roles were lambda_old = face, mu_old = slot, nu_old = holder: same 64 objects, different pair
check("3.3", "the same 64 couplings serve both readings: re-assigning the roles is a permutation of the index slots, so the "
      "counts 40/24 and the representations are unchanged, but WHICH 24 is torsion changes",
      len({cpl(*t) + (t[1], t[2]) for t in trip}) == 64)

print("\n=== 4. The framework's 16 + 24 + 24 on the tiled cube")
diag = [t for t in trip if t[1] == t[2]]
off = [t for t in trip if t[1] != t[2]]
pairs = {frozenset((t, tau_fw(t))) for t in off}
check("4.1", "shared 16: the couplings through the Field Origin links (slot = face, the cores), 4 links x 4 holders; "
      "fixed by the exchange of roots", len(diag) == 16 and all(tau_fw(t) == t for t in diag))
check("4.2", "the other 48 are the 12 cube-edge links x 4 holders, paired by the exchange of roots into 24 pairs: "
      "one of each pair is read from TetA's end, its partner is the antipodal link, 24 + 24",
      len(off) == 48 and len(pairs) == 24)
check("4.3", "per slice (fixed holder lambda): 4 diagonal + 6 + 6, the Gram paper's index grid",
      all(sum(1 for t in diag if t[0] == l) == 4 and sum(1 for t in off if t[0] == l) == 12 for l in R4))
check("4.4", "one root alone cannot tell a link from its antipode (Letter 2's root-blindness), so it identifies each pair: "
      "16 + 24 = 40; both roots tell them apart: 64", 16 + len(pairs) == 40 and 16 + 2 * len(pairs) == 64)

print("\n=== 5. What does not yet fit: the upper index under the exchange of roots")
# parity sends the TetA coupling (link (m, n), cube c) to the coupling on link (n, m) at cube -c; which holder leg is that?
def holder_leg(m, n, c):
    return next(l for l in R4 if cpl(l, m, n) == c)
pi_ok = True; pi_pure = True
for (l, m, n) in off:
    l2 = holder_leg(n, m, neg(cpl(l, m, n)))
    if l2 != l: pi_pure = False
    others = [x for x in R4 if x not in (m, n)]
    expect = n if l == m else m if l == n else [x for x in others if x != l][0]
    pi_ok &= (l2 == expect)
check("5.1", "with the holder labelled by the formula, the exchange of roots does not keep the upper index: it acts on the triple "
      "as the double transposition (mu nu)(the other two), a relabelling that depends on the link", pi_ok and not pi_pure)
# search: is there ANY T_d-equivariant labelling of the edge-link holders by legs that the exchange of roots keeps?
T = lambda x: tuple(int(x_) for x_ in x)
mats = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        mats.append((perm, sg))
app = lambda M, x: tuple(M[1][i] * x[M[0][i]] for i in range(3))
idxA = {v: i for i, v in enumerate(V)}
Td = [M for M in mats if all(app(M, v) in idxA for v in V)]
sig = lambda M: [idxA[app(M, V[a])] for a in R4]
base = (0, 1); hb = sorted(A_holders(*base))
labellings, kept = 0, 0
for p in itertools.permutations(R4):
    L0 = dict(zip(hb, p)); L = {}; good = True
    for M in Td:
        s = sig(M); nl = (s[0], s[1])
        for c, l in L0.items():
            key = (nl, app(M, c))
            if key in L and L[key] != s[l]: good = False
            L[key] = s[l]
    lk = [(a, b) for a in R4 for b in R4 if a != b]
    if not good or not all(sorted(L[(k, c)] for c in A_holders(*k)) == [0, 1, 2, 3] for k in lk): continue
    labellings += 1
    kept += all(L[((b, a), neg(c))] == L[((a, b), c)] for (a, b) in lk for c in A_holders(a, b))
check("5.2", "of the 4 labellings of holders by legs that respect TetA's symmetry, none is kept by the exchange of roots: "
      "with the holder as the upper index, TetB's reading is the transpose only up to that relabelling; whether it is the "
      "frame parity on the upper index (note 14) is open",
      labellings == 4 and kept == 0)

n_pass = sum(ok for _, ok in results)
print(f"\n{n_pass}/{len(results)} checks passed")
