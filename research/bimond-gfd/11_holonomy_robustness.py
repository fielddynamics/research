"""11. How robust is the chiral-holonomy proposition (Letter 3 supplement), and what generates the winding?

Model of the note: each step v_i -> v_j is a rotation by +-theta about v_i x v_j, the sign of the WHOLE step set by the
source chirality (+ TetA, - TetB).  Checks here:
 E. Exact values: cos(Theta) = -4639/6561 and -5983/6561 (6561 = 3^8).  So Theta = 134.996 deg, not exactly 3 pi/4.
 P. Parity (swapping the TetA/TetB labels) exchanges the two classes, as does taking the sign from the target.
    The asymmetry between the two senses of circulation is therefore mirror-odd: a genuine chirality.
 RC. Riemann-Cartan reading: the connection is Levi-Civita + contortion.  Levi-Civita transport carries v_i to v_j;
    torsion adds a small rotation epsilon (here a spin about the local null direction) whose sign is the chirality.
    - Alternating signs (+ on TetA steps, - on TetB steps) cancel exactly around every cycle.
    - One sign accumulates: 8 epsilon if every step carries it.
 TB. GFD's own assignment (40/24): TetA is torsion-free (the 40), torsion carries TetB (the 24).  Torsion then sits only on
    the four TetB steps, all of one sign: holonomy = 4 epsilon about the base direction, the same for both senses of
    traversal, reversed by parity.  With strength weighted by the TetB share, 4 (1 - mu) epsilon: suppressed at the
    centre (x -> oo) and full at the rim (x -> 0), the radial behaviour the note states.
"""
import itertools, numpy as np, sympy as sp
ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
V = [(np.array([(i >> 2) & 1, (i >> 1) & 1, i & 1]) * 2 - 1) / np.sqrt(3) for i in range(8)]
tetA = lambda i: bin(i).count('1') % 2 == 1
adj = lambda i, j: bin(i ^ j).count('1') == 1
def R(n, a):
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(a) * K + (1 - np.cos(a)) * K @ K
cycles = [(0,) + p for p in itertools.permutations(range(1, 8)) if all(adj(((0,) + p)[k], ((0,) + p)[(k + 1) % 8]) for k in range(8))]
rev = lambda c: (c[0],) + tuple(reversed(c[1:]))
ang = lambda H: np.degrees(np.arccos(np.clip((np.trace(H) - 1) / 2, -1, 1)))
def step_geom(a, b):
    n = np.cross(V[a], V[b]); n /= np.linalg.norm(n); return n, np.arccos(np.clip(V[a] @ V[b], -1, 1))

# ---- E: exact holonomy angles of the note's model
Vs = [sp.Matrix([(i >> 2) & 1, (i >> 1) & 1, i & 1]) * 2 - sp.Matrix([1, 1, 1]) for i in range(8)]
def Rx(n, s):
    K = sp.Matrix([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]]); return sp.eye(3) + s * K + (1 - sp.Rational(1, 3)) * K * K
def hol_exact(c, sign):
    H = sp.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]
        n = Vs[a].cross(Vs[b]); n = n / sp.sqrt(n.dot(n))
        H = sp.simplify(Rx(n, sign(a, b) * 2 * sp.sqrt(2) / 3) * H)
    return sp.nsimplify(sp.simplify((H.trace() - 1) / 2))
src = lambda a, b: 1 if tetA(a) else -1
c0 = cycles[0]
cf, cr = hol_exact(c0, src), hol_exact(rev(c0), src)
check("E: exact cos(Theta) = %s and %s (denominator 3^8)" % (cf, cr), {cf, cr} == {sp.Rational(-4639, 6561), sp.Rational(-5983, 6561)})
th135 = float(sp.acos(sp.Rational(-4639, 6561)) * 180 / sp.pi)
check("E: Theta = %.4f deg, not exactly 3pi/4 (cos 3pi/4 = -0.70711 vs -4639/6561 = %.5f)" % (th135, -4639/6561),
      sp.Rational(-4639, 6561) != -sp.sqrt(2) / 2 and abs(th135 - 135) > 1e-3)
# ---- P: parity and target-sign exchange the classes
par = lambda a, b: -1 if tetA(a) else 1
tgt = lambda a, b: 1 if tetA(b) else -1
check("P: swapping the TetA/TetB labels (parity) exchanges the forward and reverse classes",
      hol_exact(c0, par) == cr and hol_exact(rev(c0), par) == cf)
check("P: taking the sign from the target instead of the source also exchanges them", hol_exact(c0, tgt) == cr)

# ---- RC: Levi-Civita transport + small torsion rotation with a chirality sign
def hol_rc(c, sgn, eps):
    H = np.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]; n, th = step_geom(a, b)
        H = R(n, th) @ R(V[a], sgn(a) * eps) @ H
    return H
alt = lambda a: 1 if tetA(a) else -1
one = lambda a: 1
for eps in (1e-3, 0.1):
    check("RC: eps = %g: alternating chirality cancels exactly on all 12 cycles" % eps,
          all(np.allclose(hol_rc(c, alt, eps), np.eye(3)) for c in cycles))
    check("RC: eps = %g: one sign on every step accumulates to 8 eps = %.4f deg" % (eps, np.degrees(8 * eps)),
          all(np.isclose(ang(hol_rc(c, one, eps)), np.degrees(8 * eps)) for c in cycles))
check("RC: Levi-Civita transport alone (eps = 0) has identity holonomy: it is the note's 'uniform' case",
      all(np.allclose(hol_rc(c, one, 0.0), np.eye(3)) for c in cycles))

# ---- TB: torsion only on TetB steps (TetA torsion-free), one sign
def hol_tb(c, eps, on=lambda a: not tetA(a), s=-1):
    H = np.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]; n, th = step_geom(a, b)
        H = R(n, th) @ (R(V[a], s * eps) if on(a) else np.eye(3)) @ H
    return H
def signed_about(H, axis):
    K = (H - H.T) / 2; return np.degrees(np.arcsin(np.clip(np.array([K[2, 1], K[0, 2], K[1, 0]]) @ axis, -1, 1)))
for eps in (1e-3, 0.05):
    check("TB: eps = %g: holonomy = 4 eps = %.4f deg on every cycle and in both senses of traversal" % (eps, np.degrees(4 * eps)),
          all(np.isclose(ang(hol_tb(c, eps)), np.degrees(4 * eps)) and np.isclose(ang(hol_tb(rev(c), eps)), np.degrees(4 * eps)) for c in cycles))
base = V[cycles[0][0]]
sB = signed_about(hol_tb(cycles[0], 0.05), base); sP = signed_about(hol_tb(cycles[0], 0.05, on=tetA, s=+1), base)
check("TB: the rotation is about the base direction, and parity (torsion on TetA with + sign) reverses its sense (%.3f vs %.3f deg)" % (sB, sP),
      np.isclose(sB, -sP) and abs(sB) > 1)
mu = lambda x: x / (1 + x)
w = [4 * (1 - mu(x)) for x in (1e3, 1.0, 1e-3)]
check("TB: weighted by the TetB share, 4(1 - mu) eps: %.4f eps at x = 1e3 (centre), %.1f eps at x = 1 (ring), %.4f eps at x = 1e-3 (rim)" % tuple(w),
      w[0] < 0.01 and np.isclose(w[1], 2) and w[2] > 3.99)
print(f"\n{sum(ok)}/{len(ok)} checks passed")
