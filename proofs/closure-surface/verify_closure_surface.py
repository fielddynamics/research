"""Machine checks for 'Where Closure Sits: the Field's Stagnation Surface and the Jacobi Surface'.

Every field object closes, locally, at every level (the mountain-scale proof). This proof asks where its closure
surface sits. A bound object of mass M on a near-circular orbit in its host: in the frame turning with the orbit, the
object's own field, the host's tide and the orbit's turning combine into one effective potential
    Phi_eff = -GM/r - (1/2) T x^2 + (1/2) nu^2 z^2,   T = 4 Omega^2 - kappa^2,
(x along the host's radius, z out of the plane). Two surfaces can be defined from it:
  Sigma_field  : the level set through the field's stagnation points (where the combined field vanishes), a property of
                 the field alone, with no orbits in it;
  Sigma_Jacobi : the surface that matter with Jacobi energy below the critical value can never leave: it stays in
                 the cell and cannot snap to a neighbouring cell.
They are the same surface, because the Coriolis force does no work. Matter above the critical value can snap to a
neighbouring cell, only through the necks that open at the two stagnation points. Without the host's tide there are
no stagnation points and no boundary: a cell is anchored by the field around it. A vortex in a strain has the same structure: its
closed streamlines are bounded by the separatrix through its stagnation points.

  Part A  the stagnation surface (field only)
  Part B  the surface matter cannot leave (orbits), that they coincide, and snapping to a neighbouring cell
  Part C  the vortex: a point vortex in a strain
  Part D  the shape and size of the surface
  Part E  self-consistency with ownership: the tide is the mountain's
  Part F  tests: planets, the Oort cloud, alpha Centauri, wide binaries, Palomar 14

Run: python verify_closure_surface.py"""
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ------------------------------------------------------------------ Part A: the stagnation surface (field only)
x, y, z = sp.symbols("x y z", real=True)
GM, T, nu2 = sp.symbols("GM T nu2", positive=True)
r = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
Phi = -GM / r - T * x ** 2 / 2 + nu2 * z ** 2 / 2
F = [-sp.diff(Phi, v) for v in (x, y, z)]
rJ = (GM / T) ** sp.Rational(1, 3)
# y- and z-components vanish only on y = z = 0 (their factors GM/r^3 and nu2 + GM/r^3 are positive), then x:
Fx_axis = sp.simplify(F[0].subs({y: 0, z: 0}).subs(x, sp.Symbol("s", positive=True)))
s_ = sp.Symbol("s", positive=True)
roots = sp.solve(sp.Eq(Fx_axis, 0), s_)
Ec = sp.simplify(Phi.subs({x: rJ, y: 0, z: 0}))
check("A1 the combined field (the object's own, the host's tide, the orbit's turning) vanishes only at two points, "
      "x = +- r_J on the host's radius with r_J^3 = GM/T, T = 4 Omega^2 - kappa^2: the Jacobi radius. The y and z "
      "components vanish only on y = z = 0, since GM/r^3 > 0 and nu^2 + GM/r^3 > 0",
      len(roots) == 1 and sp.simplify(roots[0] - rJ) == 0
      and sp.simplify(F[1] + GM * y / r ** 3) == 0 and sp.simplify(F[2] + (nu2 + GM / r ** 3) * z) == 0)
Hs = sp.hessian(Phi, (x, y, z)).subs({x: rJ, y: 0, z: 0})
Hs = sp.simplify(Hs)
check("A2 they are saddles (stagnation points): the curvature of Phi_eff there is (-3T, T, T + nu^2), one direction "
      "down and two up. The level through them is Phi_eff = E_c = -(3/2) GM/r_J. Sigma_field is the boundary of the "
      "part of {Phi_eff < E_c} around the object: defined by the field alone, with no orbits in it",
      sp.simplify(Hs - sp.diag(-3 * T, T, T + nu2)) == sp.zeros(3, 3)
      and sp.simplify(Ec + sp.Rational(3, 2) * GM / rJ) == 0)
Gs, Ss = sp.symbols("Gamma S", positive=True)
check("A3 the cell is anchored by its surroundings: as the host's tide T -> 0, r_J = (GM/T)^(1/3) -> infinity and the "
      "stagnation points recede without limit; with no surrounding flow there is no boundary. The same holds for the "
      "vortex: as the strain S -> 0 its stagnation points (a^2 = Gamma/(4 pi S)) recede to infinity",
      sp.limit(rJ, T, 0, "+") == sp.oo and sp.limit(sp.sqrt(Gs / (4 * sp.pi * Ss)), Ss, 0, "+") == sp.oo)

# ------------------------------------------------------------------ Part B: held in the cell, or snapping out
W = sp.symbols("Omega", positive=True)
vx, vy, vz = sp.symbols("v_x v_y v_z", real=True)
cor = sp.Matrix([2 * W * vy, -2 * W * vx, 0])                 # -2 Omega x v, Omega along z
check("B1 the Coriolis force does no work: v . (-2 Omega x v) = 0. So the Jacobi energy E_J = v^2/2 + Phi_eff is "
      "conserved, and since v^2/2 >= 0 an orbit can only go where Phi_eff <= E_J",
      sp.simplify(sp.Matrix([vx, vy, vz]).dot(cor)) == 0)
# numerical orbits, units GM = 1, T = 1 (r_J = 1), Sun-like nu^2/T
NU2 = 3.8
Om = math.sqrt(1 / 2)                                          # flat curve: T = 2 Omega^2
def rhs(t, s):
    X, Y, Z, VX, VY, VZ = s
    R3 = (X * X + Y * Y + Z * Z) ** 1.5
    return [VX, VY, VZ, 2 * Om * VY + X - X / R3, -2 * Om * VX - Y / R3, -NU2 * Z - Z / R3]
PhiN = lambda X, Y, Z: -1 / math.sqrt(X * X + Y * Y + Z * Z) - X * X / 2 + NU2 * Z * Z / 2
EJ = lambda s: 0.5 * (s[3] ** 2 + s[4] ** 2 + s[5] ** 2) + PhiN(*s[:3])
ECn = -1.5
rng = np.random.default_rng(7)
def sample(Elo, Ehi, n, retro=None):
    out = []
    while len(out) < n:
        p = rng.uniform(-0.6, 0.6, 3); p[2] *= 0.5
        if np.linalg.norm(p) < 0.05 or PhiN(*p) >= Ehi: continue
        E = rng.uniform(Elo, Ehi)
        if E <= PhiN(*p): continue
        vmag = math.sqrt(2 * (E - PhiN(*p)))
        d = rng.normal(size=3); d /= np.linalg.norm(d)
        if retro is not None:                                   # sense of the orbit about z
            Lz = p[0] * d[1] - p[1] * d[0]
            if (Lz < 0) != retro: d[:2] = -d[:2]
        out.append(np.concatenate([p, vmag * d]))
    return out
Tend = 40 * 2 * math.pi / Om                                    # forty host orbits
esc = lambda t, s: s[0] ** 2 + s[1] ** 2 + s[2] ** 2 - 9; esc.terminal = True
cross = lambda t, s: s[0] ** 2 + s[1] ** 2 + s[2] ** 2 - 1.1     # just past r_J: where matter leaves the cell
def run(s0):
    return solve_ivp(rhs, [0, Tend], s0, events=[esc, cross], rtol=1e-10, atol=1e-12, method="DOP853")
below = sample(-3.0, ECn - 1e-3, 40)
res_b = [run(s0) for s0 in below]
maxr = max(np.max(np.linalg.norm(sol.y[:3], axis=0)) for sol in res_b)
drift = max(abs(EJ(sol.y[:, -1]) - EJ(sol.y[:, 0])) for sol in res_b)
check(f"B2 matter with E_J below E_c, started inside Sigma_field, stays in the cell: 40 orbits over forty host orbits "
      f"each, the farthest reaching {maxr:.3f} r_J (the surface reaches r_J only at the saddles); E_J conserved to "
      f"{drift:.0e}. None snaps to a neighbouring cell. So Sigma_Jacobi = Sigma_field: one surface, read by the field or "
      "by the orbits",
      maxr < 1.0 and drift < 1e-4 and all(sol.status == 0 for sol in res_b))
above_p = [run(s0) for s0 in sample(ECn + 0.02, ECn + 0.3, 30, retro=False)]
above_r = [run(s0) for s0 in sample(ECn + 0.02, ECn + 0.3, 30, retro=True)]
fp = sum(sol.status == 1 for sol in above_p) / 30
fr = sum(sol.status == 1 for sol in above_r) / 30
exits = [sol.y_events[1][0] for sol in above_p + above_r if sol.status == 1]
ang = [math.degrees(math.acos(min(1.0, abs(p_[0]) / np.linalg.norm(p_[:3])))) for p_ in exits]
check(f"B3 above E_c matter can snap to a neighbouring cell, and only through the necks that open at the two "
      f"stagnation points: every one of the {len(exits)} that left passed 1.05 r_J within {max(ang):.0f} degrees of the host's "
      f"radius. The energy condition is sufficient, not necessary: just above E_c, {fp:.0%} of prograde and {fr:.0%} of "
      "retrograde orbits snap out within forty host orbits; retrograde ones stay longer, as known for Hill's problem",
      fp > fr and fr < 1.0 and len(exits) > 0 and max(ang) < 45)

# ------------------------------------------------------------------ Part C: the vortex
# A point vortex of circulation G in a pure strain of rate S: streamfunction psi = -(G/2 pi) ln r + S x y
# (u = d psi/dy, v = -d psi/dx). Fluid moves along psi = const: psi plays Phi_eff's role exactly.
Gc, Sc = 2 * math.pi, 1.0
psi = lambda X, Y: -(Gc / (2 * math.pi)) * 0.5 * math.log(X * X + Y * Y) + Sc * X * Y
def vel(t, p):
    X, Y = p; r2 = X * X + Y * Y
    return [-Gc * Y / (2 * math.pi * r2) + Sc * X, Gc * X / (2 * math.pi * r2) - Sc * Y]
# stagnation points: on the diagonal X = Y = a, u = v = 0 gives a^2 = G/(4 pi S)
a_s = math.sqrt(Gc / (4 * math.pi * Sc))
stag = np.array([a_s, a_s])
psi_c = psi(*stag)
e = 1e-4
H2 = np.array([[(psi(stag[0] + e, stag[1]) - 2 * psi_c + psi(stag[0] - e, stag[1])) / e ** 2,
                (psi(stag[0] + e, stag[1] + e) - psi(stag[0] + e, stag[1] - e) - psi(stag[0] - e, stag[1] + e)
                 + psi(stag[0] - e, stag[1] - e)) / (4 * e * e)],
               [0, (psi(stag[0], stag[1] + e) - 2 * psi_c + psi(stag[0], stag[1] - e)) / e ** 2]])
H2[1, 0] = H2[0, 1]
pred_in, outcome = [], []
for p0 in rng.uniform(-1.2, 1.2, (60, 2)):
    if np.linalg.norm(p0) < 0.05: continue
    if abs(psi(*p0) - psi_c) < 0.02: continue                   # too close to the separatrix to settle in finite time
    inside = all(psi(*(f_ * p0)) > psi_c for f_ in np.linspace(0.02, 1, 200))   # joined to the vortex above psi_c
    out = lambda t, p: p[0] ** 2 + p[1] ** 2 - 25; out.terminal = True
    sol = solve_ivp(vel, [0, 60], p0, events=out, rtol=1e-10, atol=1e-12)
    pred_in.append(inside); outcome.append(sol.status == 0)
check(f"C1 a point vortex in a strain: the flow stagnates at two points (a^2 = Gamma/(4 pi S)), saddles of psi "
      f"(Hessian determinant {np.linalg.det(H2):.2f} < 0). Fluid follows psi = const, so the closed streamlines are "
      f"bounded by the separatrix through the stagnation points ({sum(pred_in)} parcels inside, {len(pred_in) - sum(pred_in)} outside). Predicting each parcel's fate from psi alone agrees "
      f"with integrating it in {sum(a == b for a, b in zip(pred_in, outcome))}/{len(outcome)} cases. "
      "The same structure as Part A-B, one dimension lower (log for 1/r, strain for tide)",
      np.linalg.det(H2) < 0 and all(a == b for a, b in zip(pred_in, outcome)) and any(pred_in) and not all(pred_in))

# ------------------------------------------------------------------ Part D: the shape and size
u = sp.Symbol("u", positive=True)
y_ext = sp.solve(sp.Eq(-1 / u, sp.Rational(-3, 2)), u)[0]
check("D1 Sigma_field is not a sphere: it reaches r_J along the host's radius (at the saddles) and 2/3 r_J along the "
      "orbit (on the y axis Phi_eff = -GM/y = -(3/2) GM/r_J)", y_ext == sp.Rational(2, 3))
def z_extent(n2):
    f = lambda w: -1 / w + 0.5 * n2 * w * w + 1.5
    lo, hi = 1e-3, 2 / 3
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return lo
zS = z_extent(NU2)
Nm = 400000
P = rng.uniform(-1, 1, (Nm, 3))
R_ = np.linalg.norm(P, axis=1)
inside_lobe = (-1 / R_ - P[:, 0] ** 2 / 2 + NU2 * P[:, 2] ** 2 / 2 < -1.5) & (np.abs(P[:, 0]) < 1)
vol = 8 * inside_lobe.mean()
r_eq = (3 * vol / (4 * math.pi)) ** (1 / 3)
check(f"D2 out of the plane it reaches {zS:.3f} r_J for the Sun's vertical frequency (nu^2 = {NU2} T, local density "
      f"0.1 Msun/pc^3). Its volume is that of a sphere of radius {r_eq:.3f} r_J. The mountain-scale proof's sphere "
      "of radius r_J is therefore an outer bound; its results hold for any closed surface (balayage), and Theorem 9 "
      "bounds the non-spherical correction", 0.5 < zS < 2 / 3 and 0.55 < r_eq < 0.75)

# ------------------------------------------------------------------ Part E: the tide is the mountain's
Rg, X_ = sp.symbols("R X", positive=True)
Om2 = sp.Function("Om2")                                        # Omega^2(R) = (1/R) dPhi_host/dR
Phih = sp.Function("Phi_h")
# effective potential of the host in the turning frame, along the radius: Phi_h(R) - (1/2) Omega0^2 R^2
Om0sq = sp.diff(Phih(Rg), Rg) / Rg
eff = Phih(Rg + X_) - Om0sq * (Rg + X_) ** 2 / 2
c2 = sp.simplify(sp.diff(eff, X_, 2).subs(X_, 0))
kap2 = Rg * sp.diff(Om0sq, Rg) + 4 * Om0sq
check("E1 the coefficient T is the host field's own: expanding the host's potential in the turning frame about the "
      "orbit, the radial curvature is Phi_h'' - Omega^2 = -(4 Omega^2 - kappa^2), with kappa^2 = R dOmega^2/dR + "
      "4 Omega^2. Under ownership the host field is the mountain (it obeys the law), and the object's own field is "
      "Newtonian (the split): so Phi_eff is exactly the potential the object's members move in, and the surface they "
      "cannot cross is the one the field defines. Ownership reproduces itself",
      sp.simplify(c2 + (4 * Om0sq - kap2)) == 0)
vflat = sp.Symbol("v", positive=True)
Tflat = sp.simplify((4 * Om0sq - kap2).subs(Phih(Rg), vflat ** 2 * sp.log(Rg)).doit())
check("E2 for a flat rotation curve (Phi_h = v^2 ln R, the deep-law mountain), T = 2 Omega^2: the mountain-scale "
      "proof's radius r_J^3 = GM/(2 Omega^2)", sp.simplify(Tflat - 2 * vflat ** 2 / Rg ** 2) == 0)

# ------------------------------------------------------------------ Part F: tests
GMs, PCm, AU, KPC = 1.32712e20, 3.0857e16, 1.495979e11, 3.0857e19
OmS = 2.2e5 / (8.2 * KPC)
rJs = (GMs / (2 * OmS ** 2)) ** (1 / 3)
check(f"F1 the planets: for Neptune (30 AU) E/E_c = r_J/(3a) = {rJs / (3 * 30.07 * AU):.0f}: deep inside. The Sun's "
      f"surface sits at r_J = {rJs / PCm:.2f} pc along the Galactic radius and {2 / 3 * rJs / PCm:.2f} pc along its orbit",
      rJs / (3 * 30.07 * AU) > 1000)
a_edge = rJs / 3
check(f"F2 the Oort cloud: a Kepler orbit is held for good when -GM/2a < E_c, i.e. a < r_J/3 = {a_edge / AU:,.0f} AU "
      f"({a_edge / PCm:.2f} pc). That is the scale usually quoted for the outer Oort cloud (~10^5 AU). Comets beyond it "
      "are not held for good: the Galactic tide strips them over time, as observed in the injection of new comets",
      0.9e5 < a_edge / AU < 1.1e5)
v_rel = 32e3                                                    # alpha Cen relative to the Sun (radial -22, total ~32 km/s)
d_ac = 1.34 * PCm
GMpair = 3.0 * GMs                                              # Sun + alpha Cen A + B
E_rel = 0.5 * v_rel ** 2 - GMpair / d_ac
rJpair = (GMpair / (2 * OmS ** 2)) ** (1 / 3)
Ec_pair = -1.5 * GMpair / rJpair
check(f"F3 alpha Centauri: its closure surface and the Sun's overlap, but its energy relative to the Sun is "
      f"{E_rel:.1e} J/kg against the critical {Ec_pair:.1e}: far above, positive. Neither belongs to the other. Each "
      "is its own cell; they read each other's fields through the overlap (Paper II), and ownership is single-valued",
      E_rel > 0 and E_rel > 1e4 * abs(Ec_pair))
Mb = 1.5
rJb = (Mb * GMs / (2 * OmS ** 2)) ** (1 / 3)
seps = np.array([0.005, 0.02, 0.05, 0.1, 0.2]) * PCm
vt_max = np.sqrt(2 - 3 * seps / rJb)
check("F4 wide binaries: a pair of separation s and relative speed v is one cell when v^2/2 - GM/s < E_c, i.e. "
      "v/sqrt(GM/s) < sqrt(2 - 3 s/r_J) (tide (s/r_J)^3 neglected). For 1.5 Msun pairs the edge is " +
      ", ".join(f"{t:.3f}" for t in vt_max) + " at s = 0.005, 0.02, 0.05, 0.1, 0.2 pc. Inside, the pair is drainless "
      "and its relative motion Newtonian with G_N. The prediction: the 3D speed ratio of bound pairs stops at this "
      "edge, set before any velocity is inspected; a theory that strengthens gravity inside the pair moves the edge up",
      all(vt_max < math.sqrt(2)) and vt_max[0] > 1.41 and vt_max[-1] > 1.2)
rJp14 = (1.2e4 * GMs / (2 * (1.84e5 / (71 * KPC)) ** 2)) ** (1 / 3) / PCm
check(f"F5 Palomar 14: its surface reaches {rJp14:.0f} pc along the Galactic radius and {2 / 3 * rJp14:.0f} pc along "
      "its orbit, around a 26 pc body: one cell, Newtonian inside (drainless), as the net-field rule's analysis of its "
      "dispersion requires", 2 / 3 * rJp14 > 4 * 26)

print(f"\n{sum(ok)}/{len(ok)} checks passed")
