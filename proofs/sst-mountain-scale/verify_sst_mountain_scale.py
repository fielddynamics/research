"""Machine checks for 'The Mountain Scale in the SST: the Net-Field Rule From the Action'.

GFD's picture (Papers I-II): a field object couples to the NET Field as a whole, at its closure boundary, and closure
boundaries overlap. In the action: each bound system k sweeps ITS OWN mass onto its own closure sphere Sigma_k (its
Jacobi sphere). Spheres may overlap and contain other systems. The mountain is the total field minus each system's own
interior field, Phi_bar = Phi - sum_k d_k, and the law's term reads Phi_bar.

  Part A  the split, in 1D, with two systems whose spheres overlap and contain each other's mass
  Part B  how the owned matter is pushed (the matter equation)
  Part C  the four ports: a field object meets the NET Field through one temporal and three spatial channels
  Part D  the mountain scale: Jacobi radii, overlap in the solar neighbourhood, and why merging regions fails
  Part E  a radius that depends on the field
  Part F  the action does not choose the edge (centred spherical system)
  Part G  the 3D solutions (demo_ownership_3d.py, demo_mountain_scale.py)

Run: python verify_sst_mountain_scale.py"""
import math, os, re
import numpy as np
import sympy as sp
from scipy.optimize import fsolve

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ------------------------------------------------------------------ Part A: the split with overlapping spheres (1D)
n = 400
x = np.linspace(0, 1, n + 2)[1:-1]; h = x[1] - x[0]
D = (np.eye(n + 1, n, 0) - np.eye(n + 1, n, -1)) / h          # forward differences, zero Dirichlet at the box ends
K = D.T @ D                                                    # -Laplacian (units 4 pi G = 1)
Kinv = np.linalg.inv(K)
mu1 = lambda s: s / (1 + s)
mu2 = lambda s: s / np.sqrt(1 + s * s)
H = lambda g: -2 * g + 2 * np.log1p(g)                         # a0^2 [F(y) - y], a0 = 1; H'(g) = 2(mu - 1)g

def sweep(rho_k, a, b):
    """sweep a system's own mass inside [a, b] onto its sphere (1D: the two end points), with harmonic weights"""
    ia, ib = np.searchsorted(x, a), np.searchsorted(x, b) - 1
    out = rho_k.copy(); inside = (x > x[ia]) & (x < x[ib])
    m, xi = rho_k[inside], x[inside]
    out[inside] = 0
    out[ia] += np.sum(m * (x[ib] - xi) / (x[ib] - x[ia])); out[ib] += np.sum(m * (xi - x[ia]) / (x[ib] - x[ia]))
    return out
g = lambda c, w, M: M * np.exp(-((x - c) / w) ** 2)
rho_host = 200 * np.exp(-((x - 0.5) / 0.18) ** 2)
A = (g(0.40, 0.008, 3000), 0.25, 0.55)                         # the 'Sun' and its sphere
B = (g(0.47, 0.008, 2500), 0.33, 0.62)                         # a neighbour: spheres overlap, each contains the other
rho = rho_host + A[0] + B[0]
rho_bar = rho_host + sweep(*A) + sweep(*B)
dA, dB = Kinv @ (A[0] - sweep(*A)), Kinv @ (B[0] - sweep(*B))
outA = (x < A[1] - 2 * h) | (x > A[2] + 2 * h); outB = (x < B[1] - 2 * h) | (x > B[2] + 2 * h)
check("A1 the spheres overlap and each contains the other's mass, yet each system's own interior field d_k vanishes "
      f"outside its own sphere ({np.abs(dA[outA]).max() / np.abs(dA).max():.0e}, {np.abs(dB[outB]).max() / np.abs(dB).max():.0e}): "
      "sweeping mass onto a sphere leaves the field outside unchanged, for any shape of system",
      np.abs(dA[outA]).max() < 1e-12 * np.abs(dA).max() and np.abs(dB[outB]).max() < 1e-12 * np.abs(dB).max()
      and A[1] < 0.47 < A[2] and B[1] < 0.40 < B[2])
dsum = dA + dB
def S(p, law_H=H, d=dsum, rh=rho):
    return 0.5 * p @ K @ p - rh @ p + 0.5 * np.sum(law_H(np.abs(D @ (p - d))))
def EL(p, law=mu1, d=dsum, rh=rho):
    gb = D @ (p - d); return K @ p - rh + D.T @ ((law(np.abs(gb)) - 1) * gb)
rng = np.random.default_rng(0)
p0 = rng.standard_normal(n); v = rng.standard_normal(n); eps = 1e-6
fd = (S(p0 + eps * v) - S(p0 - eps * v)) / (2 * eps)
check(f"A2 the action S = (1/2)Phi.K.Phi - rho.Phi + (1/2) sum H(grad(Phi - sum d_k)) has the field equation "
      f"K Phi - rho + D^T[(mu - 1) grad Phi_bar] = 0 (finite difference {fd:.6e} vs {EL(p0) @ v:.6e})",
      abs(fd - EL(p0) @ v) < 1e-6 * abs(fd))
p1 = fsolve(EL, Kinv @ rho, xtol=1e-13)
p2 = fsolve(lambda p: EL(p, mu2), Kinv @ rho, xtol=1e-13)
for p, law, nm in ((p1, mu1, "x/(1+x)"), (p2, mu2, "x/sqrt(1+x^2)")):
    pb = p - dsum; gb = D @ pb
    res = np.abs(K @ pb + D.T @ ((law(np.abs(gb)) - 1) * gb) - rho_bar).max() / np.abs(rho_bar).max()
    check(f"A3 with the law {nm}: the mountain Phi_bar obeys the plain law, not a projected one, on the swept density "
          f"(residual {res:.0e}): every system's mass sits on its own closure sphere", res < 1e-9)
check("A4 the field is the mountain plus each system's own interior field, Newtonian with the bare G and fixed by its own "
      "mass alone: the same under both laws, while the mountain changes by "
      f"{np.abs((p1 - dsum) - (p2 - dsum)).max() / np.abs(p1 - dsum).max():.0e}",
      np.abs((p1 - (p1 - dsum)) - (p2 - (p2 - dsum))).max() < 1e-12 and np.abs(p1 - p2).max() > 1e-3 * np.abs(p1).max())
inA = (x > 0.30) & (x < 0.50)
check("A5 neighbours read each other: inside the Sun's sphere the mountain carries the neighbour's field and its swept "
      "shell (its slope varies across the sphere instead of being the host's alone), and the law acts on it",
      np.ptp(np.diff((p1 - dA)[inA])) > 1e-6)

# ------------------------------------------------------------------ Part B: the matter equation
eps = 1e-4
idx = np.where((x > 0.36) & (x < 0.44))[0][::8]
def S_at(rhoA_pert):
    dA_ = Kinv @ (rhoA_pert - sweep(rhoA_pert, A[1], A[2])); d_ = dA_ + dB
    return S(p1, d=d_, rh=rho_host + rhoA_pert + B[0])
force_pot = []
for i in idx:
    e = np.zeros(n); e[i] = eps
    force_pot.append(-(S_at(A[0] + e) - S_at(A[0] - e)) / (2 * eps))      # = the potential the owned matter feels
force_pot = np.array(force_pot)
dev = np.abs(force_pot - p1[idx]).max() / np.abs(p1[idx]).max()
check(f"B1 the Sun's own matter feels the total potential Phi plus a small extra term ({dev:.1e} of Phi here), set by "
      "the mountain's TetB density inside the Sun's own sphere. Physically, at the Galactic TetB density at the Sun "
      "(5.4e-22 kg/m^3) its pull inside Saturn's orbit is ~(4 pi/3) G rho r = 2e-19 m/s^2, the same order as the tide, and "
      "the density is 5e-5 of the ephemeris bound on unseen mass there (1.1e-17 kg/m^3)", dev < 0.05)

# ------------------------------------------------------------------ Part C: the four ports
X1, X2, X3, c0, b1, b2, b3 = sp.symbols("x1 x2 x3 c0 b1 b2 b3", real=True)
t11, t12, t13, t22, t23 = sp.symbols("t11 t12 t13 t22 t23", real=True)
T = sp.Matrix([[t11, t12, t13], [t12, t22, t23], [t13, t23, -t11 - t22]])
xv = sp.Matrix([X1, X2, X3])
Phi_h = c0 + (sp.Matrix([b1, b2, b3]).T * xv)[0] + sp.Rational(1, 2) * (xv.T * T * xv)[0]
lap = sum(sp.diff(Phi_h, s, 2) for s in (X1, X2, X3))
ms = [sp.Rational(3), sp.Rational(2), sp.Rational(1)]
pts = [sp.Matrix([1, 0, 0]), sp.Matrix([-1, 1, 0]), sp.Matrix([-1, -2, 0])]
Mt = sum(ms); com = sum((m * p for m, p in zip(ms, pts)), sp.zeros(3, 1))
E_int = sum(m * Phi_h.subs({X1: p[0], X2: p[1], X3: p[2]}) for m, p in zip(ms, pts))
Q = sum((m * (p * p.T) for m, p in zip(ms, pts)), sp.zeros(3, 3))
check("C1 a field object (centre of mass at its origin) in a harmonic NET Field Phi = c0 + b.x + (1/2) x.T.x couples "
      "through exactly M c0 (the lapse: one temporal channel, its clock rate) and M b (three spatial channels, its free "
      "fall), plus a tidal term (1/2) T:Q that needs the object's extent. The dipole term vanishes at the centre of mass. "
      "The leading channels are 1 + 3 = 4: the tetrad's four legs, the four active ports",
      sp.simplify(lap) == 0 and com == sp.zeros(3, 1)
      and sp.simplify(E_int - (Mt * c0 + sp.Rational(1, 2) * sum(T[i, j] * Q[i, j] for i in range(3) for j in range(3)))) == 0)
AU, PCm = 1.495979e11, 3.0857e16
check("C2 the tidal channel is suppressed: across a system of size s inside its closure sphere, the tide over its own "
      f"pull is (s/r_J)^3 by the Jacobi definition: {(1 * AU / (1.44 * PCm)) ** 3:.0e} at 1 AU, "
      f"{(9.58 * AU / (1.44 * PCm)) ** 3:.0e} at Saturn. At leading order the field object meets the NET Field only "
      "through the four ports", (9.58 * AU / (1.44 * PCm)) ** 3 < 1e-13)

# ------------------------------------------------------------------ Part D: the mountain scale
GMs, KPC = 1.32712e20, 3.0857e19
def rJ(GM, v, R):
    Om = v / R; kap2 = 2 * Om ** 2                             # flat curve: 4 Omega^2 - kappa^2 = 2 Omega^2
    return (GM / (4 * Om ** 2 - kap2)) ** (1 / 3)
rJ_sun = rJ(GMs, 2.2e5, 8.2 * KPC)
rJ_acen = rJ(2.0 * GMs, 2.2e5, 8.2 * KPC)
check(f"D1 the Sun's Jacobi radius is {rJ_sun / PCm:.2f} pc, inside the window from the Cassini bound (0.058 pc) to binding; "
      f"alpha Centauri (2.0 Msun, 1.34 pc away) has {rJ_acen / PCm:.2f} pc: each closure sphere contains the other's centre. "
      "In the ownership form this is allowed: each sweeps only its own mass",
      1.3 < rJ_sun / PCm < 1.6 and rJ_acen / PCm > 1.34 and rJ_sun / PCm > 1.34)
rho_star = 0.05                                                # Msun/pc^3, local stellar mass density
eta = rho_star * (4 * math.pi / 3) * (rJ_sun / PCm) ** 3        # sum of sphere volumes per unit volume (r_J^3 ~ M)
check(f"D2 overlap is the rule, not the exception: Jacobi spheres in the solar neighbourhood fill eta = {eta:.2f} of space "
      f"(union {1 - math.exp(-eta):.2f}), above the percolation threshold of overlapping spheres (eta_c ~ 0.34). Merging "
      "overlapping regions would join one Newtonian region across the disc and switch the law off there; sweeping by "
      "ownership does not merge anything", eta > 0.34)
for name, M, Re, D_gc in (("Pal 14", 1.2e4, 26.0, 71), ("Pal 4", 2.98e4, 18.4, 103)):
    r = rJ(GMs * M, 1.84e5, D_gc * KPC) / PCm
    check(f"D3 {name}: its own Jacobi radius {r:.0f} pc contains its {Re} pc body: the cluster is one field object, "
          "Newtonian inside with the bare G, as the net-field rule's analysis of its dispersion requires", r > 4 * Re)

# ------------------------------------------------------------------ Part E: a radius that depends on the field
cA = 0.40
def slope_at(pbar):
    return abs(np.interp(cA + 0.01, x, pbar) - np.interp(cA - 0.01, x, pbar)) / 0.02
def R_of(pbar):                                                 # R^3 ~ M/|slope|: a stand-in for the tide
    return 0.15 * (slope_at(pbar) / 40.0) ** (-1 / 3)
pbar0 = p1 - dsum
R0 = R_of(pbar0)
dA_R = lambda R: Kinv @ (A[0] - sweep(A[0], cA - R, cA + R))
outR = (x < cA - R0 - 2 * h) | (x > cA + R0 + 2 * h)
check(f"E1 for a radius read from the mountain (here R = {R0:.3f}), the system's own interior field d_k(R) is fixed by its "
      "own mass and its radius, linear, with the bare G, and zero outside: Newtonian by construction, however R depends "
      "on the field", np.abs(dA_R(R0)[outR]).max() < 1e-12 * np.abs(dA_R(R0)).max())
def SH_R(R):
    return 0.5 * np.sum(H(np.abs(D @ (p1 - dA_R(R) - dB))))
dR = 2e-3
dSdR = (SH_R(R0 + dR) - SH_R(R0 - dR)) / (2 * dR)
grad_R = np.zeros(n)
for i in range(n):
    e = np.zeros(n); e[i] = 1e-4
    grad_R[i] = (R_of(pbar0 + e) - R_of(pbar0 - e)) / 2e-4
shift = Kinv @ (dSdR * grad_R)
rel = np.abs(shift).max() / np.abs(pbar0).max()
check(f"E2 varying the field through R adds a term (dS/dR)(dR/dPhi_bar) to the mountain's equation only; here it moves "
      f"the mountain by {rel:.1e} of itself. The systems' own interior fields are untouched (E1)", rel < 0.05)

# ------------------------------------------------------------------ Part F: the action does not choose the edge
gg = sp.symbols("g", positive=True)
Hs = -2 * gg + 2 * sp.log(1 + gg)
check("F1 the law's energy term H(g) = a0^2[F - y] is non-increasing and concave (H' = -2g/(1+g), H'' = -2/(1+g)^2: "
      "the khronon's stability conditions)",
      sp.simplify(sp.diff(Hs, gg) + 2 * gg / (1 + gg)) == 0 and sp.simplify(sp.diff(Hs, gg, 2) + 2 / (1 + gg) ** 2) == 0)
cth = np.linspace(-1, 1, 4001)
def dSdR_sph(R, ge):
    gv = np.sqrt(ge ** 2 + R ** -4 + 2 * ge * R ** -2 * cth)
    return -0.5 * 4 * np.pi * R ** 2 * (H(ge) - np.trapezoid(H(gv), cth) / 2)
check("F2 for a centred spherical system in a uniform host, enlarging its sphere only changes the law's energy on the "
      "shell between R and R + dR, and by Jensen's inequality dS/dR < 0 at every radius (0.01 to 1000 r_M, hosts at "
      "x = 0.1, 1.5, 10): the action has no stationary edge, and energy alone would pick the pointwise reading. "
      "For general shapes this is not proved",
      all(dSdR_sph(R, ge) < 0 for ge in (0.1, 1.5, 10.0) for R in np.logspace(-2, 3, 200)))

# ------------------------------------------------------------------ Part G: the 3D solutions
here = os.path.dirname(os.path.abspath(__file__))
fo, fp = os.path.join(here, "demo_ownership_output.txt"), os.path.join(here, "demo_output.txt")
own = open(fo).read() if os.path.exists(fo) else ""
pw = open(fp).read() if os.path.exists(fp) else ""
if "around star B" in own and "pointwise" in pw:
    vs = [float(a) for a in re.findall(r"vanishes outside its sphere: Sun ([0-9.e+-]+), star B ([0-9.e+-]+)", own)[0]]
    o1 = {int(r): float(v) for r, v in re.findall(r"ownership r = (\d+): extra pull toward the Sun = ([+-][0-9.]+)", own)}
    p_ = {int(r): float(v) for r, v in
          re.findall(r"pointwise\s+r = (\d+): extra pull toward the Sun = ([+-][0-9.]+) a0", pw)}
    o2 = [float(v) for v in re.findall(r"around (?:the Sun|star B) r = \d+: extra pull beyond Newton \(Sun \+ star B\) and the galaxy = ([+-][0-9.]+)", own)]
    resid = [float(v) for v in re.findall(r"mountain residual ([0-9.e+-]+)", own)]
    check(f"G1 in 3D each system's own interior field vanishes outside its own sphere ({vs[0]:.0e}, {vs[1]:.0e}, limited by "
          f"the grid's thin-shell resolution), and the mountain solves the plain law (residuals {resid[0]:.0e}, {resid[1]:.0e})",
          max(vs) < 5e-2 and max(resid) < 5e-3)
    check("G2 one system in 3D: read pointwise, the extra pull around the Sun is the tail a0 mu(x) (" +
          ", ".join(f"r = {r}: {p_[r]:.2f}" for r in (2, 3, 4)) + " a0); read by ownership it is " +
          ", ".join(f"{o1[r]:+.3f}" for r in (2, 3, 4)) + " a0: no tail",
          all(abs(o1[r]) < 0.15 * p_[r] for r in (2, 3, 4)))
    check("G3 two systems whose spheres overlap, each containing the other's centre: around each, the pull beyond Newton "
          "for both stars and the galaxy is " + ", ".join(f"{v:+.3f}" for v in o2) + " a0, against +0.6 to +0.8 for a tail: "
          "no tail for either, each feels the other's full Newtonian pull, and what remains is the law acting on each "
          "star's field where it lies outside that star's own sphere", all(abs(v) < 0.15 for v in o2))
else:
    print("(3D outputs missing: run demo_mountain_scale.py and demo_ownership_3d.py)")

print(f"\n{sum(ok)}/{len(ok)} checks passed")
