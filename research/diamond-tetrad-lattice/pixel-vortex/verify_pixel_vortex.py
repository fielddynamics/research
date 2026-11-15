"""Exact checks for PROOF.md: vortices in the pixel.

Pixel graph: Field Origin O; the octahedron's 6 vertices (the cube's face centres); the cube's
8 corners (4 TetA, xyz = +1; 4 TetB, xyz = -1). The most general nearest-neighbour Hamiltonian
with the tetrahedral symmetry Td (the symmetry that keeps TetA and TetB, so any x):
  on-site     Delta (O), Delta_f (faces), eps_A, eps_B (corners)
  couplings   t_f (O - face), t_A, t_B (O - corner legs), c_A, c_B (face - adjacent corner)
Axis: z, through the octahedron vertices +-z. S = S4 rotoreflection (x, y, z) -> (-y, x, -z);
C = C4 rotation (x, y, z) -> (-y, x, z).
Run: python verify_pixel_vortex.py
"""
import itertools
import random
import sympy as sp

passed = failed = 0
def check(label, ok):
    global passed, failed
    passed += bool(ok); failed += (not ok)
    print(("PASS " if ok else "FAIL ") + label)

D, Df, eA, eB, tf, tA, tB, cA, cB = sp.symbols("Delta Delta_f epsilon_A epsilon_B t_f t_A t_B c_A c_B", real=True)
faces = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
corners = list(itertools.product((1, -1), repeat=3))
sites = [(0, 0, 0)] + faces + corners
n = len(sites)
isA = lambda c: c[0] * c[1] * c[2] == 1
kind = ["O"] + ["F"] * 6 + ["A" if isA(c) else "B" for c in corners]
pos = {s: i for i, s in enumerate(sites)}

H = sp.zeros(n)
H[0, 0] = D
for i in range(1, n):
    k = kind[i]
    H[i, i] = {"F": Df, "A": eA, "B": eB}[k]
    H[0, i] = H[i, 0] = -{"F": tf, "A": tA, "B": tB}[k]
for f in faces:
    for c in corners:
        if sum(a * b for a, b in zip(f, c)) == 1:          # corner on that face
            i, j = pos[f], pos[c]
            H[i, j] = H[j, i] = -(cA if isA(c) else cB)

def perm(R):
    P = sp.zeros(n)
    for s in sites:
        P[pos[tuple(int(v) for v in R * sp.Matrix(s))], pos[s]] = 1
    return P

S = perm(sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, -1]]))
C = perm(sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))

# --- Lemma 1: symmetry -------------------------------------------------------------
Td = []
for p in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        R = sp.zeros(3)
        for r in range(3):
            R[r, p[r]] = sg[r]
        if all(isA(tuple(int(v) for v in R * sp.Matrix(c))) == isA(c) for c in corners):
            Td.append(R)
check("L1 Td has 24 elements and every one commutes with H, for all parameters",
      len(Td) == 24 and all(perm(R) * H == H * perm(R) for R in Td))
check("L1 the rotoreflection S is in Td, so SH = HS for every x", S * H == H * S)
check("L1 the quarter turn C is not: it swaps TetA and TetB corners",
      all(isA(tuple(int(v) for v in sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) * sp.Matrix(c))) != isA(c) for c in corners))
ring = {D: Df, eA: eB, tA: tB, cA: cB}
HC = (C * H - H * C)
check("L1 CH = HC exactly when the TetA and TetB parameters are equal (the ring, x = 1)",
      sp.simplify(HC.subs({eB: eA, tB: tA, cB: cA})) == sp.zeros(n) and HC != sp.zeros(n))
check("L1 H is real symmetric, so complex conjugation K commutes with H", H == H.T and all(v.is_real is not False for v in H))
check("L1 S^4 = 1, S^2 = C^2 (the half turn), S is not a rotation (det -1)",
      S**4 == sp.eye(n) and S**2 == C**2 and sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, -1]]).det() == -1)

# --- Lemma 2: the winding subspaces ------------------------------------------------
I = sp.I
proj = lambda lam: sum((lam ** (-k) * S ** k for k in range(4)), sp.zeros(n)) / 4
Pp, Pm = proj(I), proj(-I)
check("L2 P(+i), P(-i) are projectors onto the S-eigenspaces with eigenvalues +i, -i",
      sp.simplify(Pp * Pp - Pp) == sp.zeros(n) and sp.simplify(S * Pp - I * Pp) == sp.zeros(n)
      and sp.simplify(S * Pm + I * Pm) == sp.zeros(n))
check("L2 each has dimension 3", Pp.rank() == 3 and Pm.rank() == 3)
axis = [pos[(0, 0, 0)], pos[(0, 0, 1)], pos[(0, 0, -1)]]
check("L2 every vector with winding +-i vanishes at the Field Origin and on both axial vertices",
      all(Pp[a, j] == 0 and Pm[a, j] == 0 for a in axis for j in range(n)))
orbits = []
seen = set()
for s in sites:
    if s in seen:
        continue
    orb = [s]
    while True:
        t = tuple(int(v) for v in sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, -1]]) * sp.Matrix(orb[-1]))
        if t == s:
            break
        orb.append(t)
    seen |= set(orb); orbits.append(orb)
sizes = sorted(len(o) for o in orbits)
check("L2 S-orbits: O (1), the axial pair (2), the equatorial ring (4), TetA corners (4), TetB corners (4)",
      sizes == [1, 2, 4, 4, 4] and any(set(o) == {f for f in faces[:4]} for o in orbits)
      and any(all(c in corners and isA(c) for c in o) and len(o) == 4 for o in orbits)
      and any(all(c in corners and not isA(c) for c in o) and len(o) == 4 for o in orbits))
tetA_orbit = [o for o in orbits if len(o) == 4 and all(c in corners and isA(c) for c in o)][0]
check("L2 the TetA orbit alternates above and below the equator (z = +, -, +, -)",
      [c[2] for c in tetA_orbit] in ([1, -1, 1, -1], [-1, 1, -1, 1]))

# --- Theorem 1: vortex eigenstates exist for every parameter value ------------------
def orbit_vec(orb, lam):
    v = sp.zeros(n, 1)
    for k, s in enumerate(orb):
        v[pos[s]] = lam ** (-k)          # S maps orb[k] -> orb[k+1]; (S v)[orb[k+1]] = v[orb[k]]
    return v / 2
ringorb = [o for o in orbits if set(o) == set(faces[:4])][0]
tetB_orbit = [o for o in orbits if len(o) == 4 and all(c in corners and not isA(c) for c in o)][0]
B = sp.Matrix.hstack(orbit_vec(ringorb, I), orbit_vec(tetA_orbit, I), orbit_vec(tetB_orbit, I))
check("T1 the three orbit vectors with phase i^-k are an orthonormal basis of the +i space",
      sp.simplify(S * B - I * B) == sp.zeros(n, 3) and sp.simplify(B.H * B) == sp.eye(3))
Hp = sp.simplify(B.H * H * B)
check("T1 H maps the +i space into itself (block form), so H has eigenvectors in it", 
      sp.simplify(H * B - B * Hp) == sp.zeros(n, 3))
check("T1 the +i block is Hermitian", sp.simplify(Hp - Hp.H) == sp.zeros(3))
print("     +i block (basis: ring, TetA corners, TetB corners):", Hp.tolist())
Bm = B.applyfunc(sp.conjugate)
check("T1 complex conjugation maps the +i space onto the -i space with the same block: vortex and "
      "antivortex at the same energy", sp.simplify(S * Bm + I * Bm) == sp.zeros(n, 3)
      and sp.simplify(Bm.H * H * Bm - Hp.applyfunc(sp.conjugate)) == sp.zeros(3))

# --- Theorem 2: a vortex carries a persistent circulating current ---------------------
# Bond current J_ij = 2 Im(psi_i* H_ij psi_j); circulation about the axis L = sum_edges J_ij (r_i x r_j)_z.
r_, p_, q_ = sp.symbols("r p q")
wv = sp.Matrix([r_, p_, q_])
M = sp.zeros(3)
for a_, b_ in [(a_, b_) for a_ in range(n) for b_ in range(a_ + 1, n) if H[a_, b_] != 0]:
    cr = sites[a_][0] * sites[b_][1] - sites[a_][1] * sites[b_][0]
    if cr:
        M += cr * (-I) * H[a_, b_] * (B[a_, :].H * B[b_, :] - B[b_, :].H * B[a_, :])
M = sp.simplify(M)
V = Hp - sp.diag(Df, eA, eB)                          # the ring-corner coupling part of the +i block
check("T2 for every psi = B w in the +i space, the circulation is L = -w^H V w: minus the ring-corner coupling energy",
      sp.simplify(M + V) == sp.zeros(3))
a_c, b_c = Hp[0, 1], Hp[0, 2]                          # -c_A(1+i), -c_B(1+i)
E = sp.symbols("E", real=True)
rr = sp.symbols("r", positive=True)
pv = sp.conjugate(a_c) * rr / (E - eA); qv = sp.conjugate(b_c) * rr / (E - eB)
w_e = sp.Matrix([rr, pv, qv])
secular = sp.Eq(E - Df, (a_c * sp.conjugate(a_c)) / (E - eA) + (b_c * sp.conjugate(b_c)) / (E - eB))
rows = sp.simplify(Hp * w_e - E * w_e)
check("T2 the eigenvectors are w = (r, conj(a) r/(E - eps_A), conj(b) r/(E - eps_B)) with E a root of "
      "E - Delta_f = 2c_A^2/(E - eps_A) + 2c_B^2/(E - eps_B)",
      sp.simplify(rows[1]) == 0 and sp.simplify(rows[2]) == 0
      and sp.simplify(rows[0] - (Df - E) * rr - (a_c * pv + b_c * qv)) == 0
      and sp.simplify(a_c * sp.conjugate(a_c) - 2 * cA**2) == 0)
Lform = sp.simplify(-(w_e.H * V * w_e)[0])
Lclosed = sp.simplify(Lform - (-2 * (E - Df) * rr**2)).subs(
    Df, sp.solve(secular, Df)[0])
check("T2 on an eigenvector, L = -2 (E - Delta_f) |r|^2 exactly (r: the core ring's amplitude)", sp.simplify(Lclosed) == 0)
Bm_ = B.applyfunc(sp.conjugate)
Mm = sp.zeros(3)
for a_, b_ in [(a_, b_) for a_ in range(n) for b_ in range(a_ + 1, n) if H[a_, b_] != 0]:
    cr = sites[a_][0] * sites[b_][1] - sites[a_][1] * sites[b_][0]
    if cr:
        Mm += cr * (-I) * H[a_, b_] * (Bm_[a_, :].H * Bm_[b_, :] - Bm_[b_, :].H * Bm_[a_, :])
check("T2 the -i antivortex (complex conjugate) has the same energy and the opposite circulation",
      sp.simplify(Mm + M.applyfunc(sp.conjugate)) == sp.zeros(3))
Ep = sp.Poly(sp.together((E - Df) * (E - eA) * (E - eB) - 2 * cA**2 * (E - eB) - 2 * cB**2 * (E - eA)), E)
check("T2 three vortex energies (a cubic), so three vortices with +i winding and three antivortices with -i",
      Ep.degree() == 3)

# --- Theorem 3: the corners drive the core (flywheel) --------------------------------
cp_block = sp.factor((Hp - E * sp.eye(3)).det())
check("T3 if c_A, c_B != 0 and eps_A != eps_B, no vortex energy equals eps_A or eps_B "
      "(det(H+ - E) at E = eps_A is 2 c_A^2 (eps_A - eps_B), at E = eps_B it is 2 c_B^2 (eps_B - eps_A): nonzero)",
      sp.simplify(cp_block.subs(E, eA) - 2 * cA**2 * (eA - eB)) == 0
      and sp.simplify(cp_block.subs(E, eB) - 2 * cB**2 * (eB - eA)) == 0)
check("T3 so every vortex has r != 0: the octahedron ring always turns, and the corners are locked to it, "
      "p = conj(a) r/(E - eps_A), q = conj(b) r/(E - eps_B) (if r = 0 then p = q = 0)",
      sp.simplify(pv.subs(rr, 0)) == 0 and sp.simplify(qv.subs(rr, 0)) == 0)
check("T3 and L != 0 unless E = Delta_f, which needs c_A^2 (Delta_f - eps_B) + c_B^2 (Delta_f - eps_A) = 0 "
      "(a single condition on the parameters, not an identity)",
      sp.simplify(Ep.as_expr().subs(E, Df) - (-2 * cA**2 * (Df - eB) - 2 * cB**2 * (Df - eA))) == 0)
check("T3 at eps_A = eps_B (TetA and TetB corners alike, the ring x = 1) one vortex has a still core: "
      "E = eps_A is then a root with r = 0, and that vortex carries no current",
      sp.simplify(cp_block.subs({eB: eA}).subs(E, eA)) == 0)
import numpy as np
rng = np.random.default_rng(3)
okn = True
Hf = sp.lambdify((D, Df, eA, eB, tf, tA, tB, cA, cB), H, "numpy")
Bf = np.array(B.evalf(), dtype=complex)
for _ in range(20):
    pr = rng.normal(size=9); pr[7:] = np.abs(pr[7:]) + 0.1
    Hn = np.array(Hf(*pr), dtype=float)
    Hb = Bf.conj().T @ Hn @ Bf
    Ew, W = np.linalg.eigh(Hb)
    for k in range(3):
        psi = Bf @ W[:, k]
        okn &= np.allclose(Hn @ psi, Ew[k] * psi, atol=1e-10)
        L = sum(2 * np.imag(np.conj(psi[a_]) * Hn[a_, b_] * psi[b_]) * (sites[a_][0]*sites[b_][1] - sites[a_][1]*sites[b_][0])
                for a_ in range(n) for b_ in range(a_ + 1, n) if Hn[a_, b_] != 0)
        okn &= abs(L - (-2 * (Ew[k] - pr[1]) * abs(W[0, k])**2)) < 1e-10 and abs(W[0, k]) > 1e-8
check("T3 numerical cross-check, 20 random parameter sets: every vortex is a stationary state of the full pixel, "
      "its core ring turns, and L = -2 (E - Delta_f)|r|^2", okn)

# --- Corollary: the plain Lambda pixel (no octahedron) -----------------------------
keep = [0] + list(range(7, n))
H9 = H.extract(keep, keep).subs({cA: 0, cB: 0})
S9 = S.extract(keep, keep)
P9 = sum((I ** (-k) * S9 ** k for k in range(4)), sp.zeros(9)) / 4
check("C1 the 9-site Lambda pixel (Field Origin + corners) also has vortices (+i space of dimension 2)",
      P9.rank() == 2 and S9 * H9 == H9 * S9)
check("C1 but they vanish at the Field Origin, and every bond of the 9-site pixel touches the Field Origin",
      all(P9[0, j] == 0 for j in range(9)) and all(H9[i, j] == 0 for i in range(1, 9) for j in range(1, 9) if i != j))
check("C1 so they carry no current at all: without the octahedron, winding states exist but nothing circulates",
      all(sp.simplify(P9[0, j]) == 0 for j in range(9)))

print(f"\n{passed}/{passed + failed} checks passed")
raise SystemExit(failed)
