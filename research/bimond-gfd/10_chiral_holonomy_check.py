"""10. Reproduces the chiral-holonomy proposition of Letter 3's supplement
(papers/letter-3-field-closure-of-tetrad-frame/Supplementary/supplementary_chiral_holonomy.tex), whose ~40-line script
is cited there but not in the repository.

Eight null directions = cube vertices (+-1,+-1,+-1)/sqrt3; TetA = odd popcount, TetB = even popcount (as in the note).
Each step v_i -> v_j along a cube edge rotates by theta = arccos(v_i.v_j) about v_i x v_j, with sign + from TetA, - from TetB.
Claims: (a) uniform transport gives identity holonomy on every Hamiltonian cycle; (b) chiral transport never does:
6 cycles give 135 deg and 6 give 155.8 deg (exactly arccos(-4639/6561) = 134.996 deg and
arccos(-5983/6561) = 155.770 deg; see 11, so 135 deg is not exactly 3pi/4).  Added here: the two angle classes are the two senses of circulation.  Each undirected cycle gives 135 deg traversed one
way and 155.8 deg traversed the other way, so the two senses are not equivalent: the closure is chiral (parity-broken)."""
import itertools, numpy as np
from collections import Counter
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
V = [(np.array([(i >> 2) & 1, (i >> 1) & 1, i & 1]) * 2 - 1) / np.sqrt(3) for i in range(8)]
tetA = lambda i: bin(i).count('1') % 2 == 1
adj = lambda i, j: bin(i ^ j).count('1') == 1
def R(n, a):
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
def hol(c, chiral):
    H = np.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]
        n = np.cross(V[a], V[b]); n /= np.linalg.norm(n)
        th = np.arccos(np.clip(V[a] @ V[b], -1, 1))
        H = R(n, (1 if (tetA(a) or not chiral) else -1) * th) @ H
    return H
ang = lambda H: np.degrees(np.arccos(np.clip((np.trace(H) - 1) / 2, -1, 1)))
cycles = [(0,) + p for p in itertools.permutations(range(1, 8)) if all(adj(((0,) + p)[k], ((0,) + p)[(k + 1) % 8]) for k in range(8))]
check("cube graph: %d directed Hamiltonian cycles through vertex 0 (6 undirected)" % len(cycles), len(cycles) == 12)
check("every cube edge joins TetA to TetB (bipartite), angle arccos(1/3) = 70.53 deg",
      all(tetA(i) != tetA(j) and np.isclose(V[i] @ V[j], 1/3) for i in range(8) for j in range(8) if adj(i, j)))
check("(a) uniform transport: identity holonomy on all 12 cycles", all(np.allclose(hol(c, False), np.eye(3)) for c in cycles))
cnt = Counter(round(ang(hol(c, True)), 2) for c in cycles)
check("(b) chiral transport: never identity; 6 cycles at 135.00 deg and 6 at 155.77 deg  %s" % dict(cnt),
      cnt == Counter({135.0: 6, 155.77: 6}))
pairs = []
for c in cycles:
    r = (c[0],) + tuple(reversed(c[1:]))
    pairs.append(tuple(sorted((round(ang(hol(c, True)), 2), round(ang(hol(r, True)), 2)))))
check("the two classes are the two senses of circulation: every cycle gives 135 deg one way and 155.77 deg the other",
      all(pr == (135.0, 155.77) for pr in pairs))
check("uniform transport cannot tell the senses apart (identity both ways); chiral transport can",
      all(np.allclose(hol((c[0],) + tuple(reversed(c[1:])), False), np.eye(3)) for c in cycles))
print(f"\n{sum(ok)}/{len(ok)} checks passed")
