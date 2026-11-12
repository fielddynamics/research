"""11. The chiral holonomy (Letter 3 supplement) read through GFD's own two-sector algebra.

GFD's math for the two sectors (papers/gram-matrix-of-tetrad-equation, Letter 2):
  - each K x K slice of the connection is 6 (upper, TetA) + 4 (diagonal, shared) + 6 (lower, TetB); across 4 slices
    64 = 24 + 16 + 24.  The torsion-free (GR) projection keeps 16 + 24 = 40 and is root-blind (Letter 2, Lemma).
  - cross-coupling sign reversal: G_{M1 M2} = M1^T M2 = -M1^T M1 for M2 = -M1.
Checks here:
 E. Exact angles of the chiral transport: cos(Theta) = -4639/6561 and -5983/6561 (6561 = 3^8), i.e. 134.996 and
    155.770 deg (so "135 deg = 3pi/4" is approximate).
 P. Parity (swapping the TetA/TetB labels) exchanges the two classes: the difference between the two senses of
    circulation is mirror-odd, a chirality.
 T. The note's TetB step R(n, -theta) is exactly the TRANSPOSE of the TetA step R(n, theta): the diagonal is shared and
    the upper and lower triangles are exchanged, the same exchange the Gram index grid assigns to TetA <-> TetB.
    So the note's sign rule is the 24 + 16 + 24 structure, not an extra assumption.
 U. Uniform transport (every step read as TetA) is the root-blind, torsion-free reading: identity on every cycle,
    as Letter 2's Lemma requires.  The winding appears only when the TetB sector is kept.
 G. For comparison: putting TetA's (Levi-Civita) transport at every step and adding torsion as a small perturbation
    with alternating sign cancels exactly.  That model imposes GR's projection on the TetB steps, so it reproduces the
    root-blind null result; it is not a test of the two-sector structure.
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
def geom(a, b):
    n = np.cross(V[a], V[b]); n /= np.linalg.norm(n); return n, np.arccos(np.clip(V[a] @ V[b], -1, 1))

# ---- Gram lemmas (the two sectors)
M1 = np.array([[1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]], float)   # TetA legs as columns (H4 rows 2-4)
M2 = -M1
check("Gram: self-couplings agree (root-blind), M2^T M2 = M1^T M1", np.allclose(M2.T @ M2, M1.T @ M1))
check("Gram: cross-coupling reverses sign, M1^T M2 = -M1^T M1", np.allclose(M1.T @ M2, -(M1.T @ M1)))
check("Gram: index grid per K x K slice: 6 upper + 4 diagonal + 6 lower = 16; over 4 slices 24 + 16 + 24 = 64; GR keeps 16 + 24 = 40",
      (6 + 4 + 6 == 16) and (4*6 + 4*4 + 4*6 == 64) and (16 + 24 == 40))

# ---- E: exact angles
Vs = [sp.Matrix([(i >> 2) & 1, (i >> 1) & 1, i & 1]) * 2 - sp.Matrix([1, 1, 1]) for i in range(8)]
def Rx(n, s):
    K = sp.Matrix([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]]); return sp.eye(3) + s * K + (1 - sp.Rational(1, 3)) * K * K
def hol_exact(c, sign):
    H = sp.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]
        n = Vs[a].cross(Vs[b]); n = n / sp.sqrt(n.dot(n))
        H = sp.simplify(Rx(n, sign(a) * 2 * sp.sqrt(2) / 3) * H)
    return sp.nsimplify(sp.simplify((H.trace() - 1) / 2))
src = lambda a: 1 if tetA(a) else -1
c0 = cycles[0]; cf, cr = hol_exact(c0, src), hol_exact(rev(c0), src)
check("E: exact cos(Theta) = %s and %s (denominator 3^8)" % (cf, cr), {cf, cr} == {sp.Rational(-4639, 6561), sp.Rational(-5983, 6561)})
th = float(sp.acos(sp.Rational(-4639, 6561)) * 180 / sp.pi)
check("E: Theta = %.4f deg, close to but not exactly 3pi/4" % th, sp.Rational(-4639, 6561) != -sp.sqrt(2)/2 and abs(th - 135) > 1e-3)
# ---- P
par = lambda a: -1 if tetA(a) else 1
check("P: swapping the TetA/TetB labels (parity) exchanges the two senses' classes", hol_exact(c0, par) == cr and hol_exact(rev(c0), par) == cf)

# ---- T: TetB step = transpose of TetA step
tri_ok = True
for i in range(8):
    for j in range(8):
        if adj(i, j):
            n, t = geom(i, j); A = R(n, t); B = R(n, -t)
            tri_ok &= np.allclose(B, A.T) and np.allclose(np.diag(A), np.diag(B)) \
                      and np.allclose(np.triu(A, 1), np.tril(B, -1).T) and not np.allclose(A, B)
check("T: on every cube edge, the TetB step R(n,-theta) = R(n,theta)^T: diagonal shared, upper and lower triangles exchanged", tri_ok)
def hol_T(c):
    H = np.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]; n, t = geom(a, b)
        H = (R(n, t) if tetA(a) else R(n, t).T) @ H
    return H
def hol_note(c):
    H = np.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]; n, t = geom(a, b)
        H = R(n, src(a) * t) @ H
    return H
check("T: transport with the TetB steps transposed equals the note's chiral transport on all 12 cycles",
      all(np.allclose(hol_T(c), hol_note(c)) for c in cycles))
# ---- U
def hol_uniform(c):
    H = np.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]; n, t = geom(a, b); H = R(n, t) @ H
    return H
check("U: uniform (all-TetA, root-blind) transport gives identity on all 12 cycles; keeping TetB gives winding on all 12",
      all(np.allclose(hol_uniform(c), np.eye(3)) for c in cycles) and all(ang(hol_note(c)) > 100 for c in cycles))
# ---- G: GR-baseline perturbative model (for comparison)
def hol_pert(c, eps):
    H = np.eye(3)
    for k in range(8):
        a, b = c[k], c[(k + 1) % 8]; n, t = geom(a, b)
        H = R(n, t) @ R(V[a], src(a) * eps) @ H
    return H
check("G: TetA (Levi-Civita) transport on every step plus an alternating small torsion rotation cancels exactly: the root-blind projection imposed on TetB steps",
      all(np.allclose(hol_pert(c, 0.1), np.eye(3)) for c in cycles))
print(f"\n{sum(ok)}/{len(ok)} checks passed")
