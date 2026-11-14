"""
Hourglass vortex lemma: spiral -> throat -> spiral under spatial parity.

Exact sympy checks. Run:  python verify_hourglass_lemma.py   (exit 0 if all pass)

Parity acts on a velocity field v by (Pi v)(x) = -v(-x), the push-forward by -I.
"""
from __future__ import annotations

import sys

import sympy as sp

CHECKS: list[tuple[str, bool]] = []


def check(name, ok):
    CHECKS.append((name, bool(ok)))


x, y, z = sp.symbols("x y z", real=True)
r = sp.sqrt(x ** 2 + y ** 2)
X = sp.Matrix([x, y, z])
rhat = sp.Matrix([x / r, y / r, 0])
phat = sp.Matrix([-y / r, x / r, 0])
zhat = sp.Matrix([0, 0, 1])


def field(vr, vphi, vz):
    """Cartesian field from cylindrical components given as expressions in (x, y, z)."""
    return vr * rhat + vphi * phat + vz * zhat


def at(expr, point):
    return expr.subs({x: point[0], y: point[1], z: point[2]}, simultaneous=True)


def parity(V):
    return -at(V, -X)


def curl(V):
    return sp.Matrix([sp.diff(V[2], y) - sp.diff(V[1], z),
                      sp.diff(V[0], z) - sp.diff(V[2], x),
                      sp.diff(V[1], x) - sp.diff(V[0], y)])


def div(V):
    return sp.diff(V[0], x) + sp.diff(V[1], y) + sp.diff(V[2], z)


def zero(M):
    return all(sp.simplify(e) == 0 for e in M)


# General axisymmetric field: components are arbitrary functions of (r, z)
R, Z = sp.symbols("R Z", real=True)
fr, fp, fz = (sp.Function(n) for n in ("f_r", "f_phi", "f_z"))
V = field(fr(r, z), fp(r, z), fz(r, z))
PV = parity(V)

check("(a) Pi is an involution: Pi(Pi v) = v", zero(parity(PV) - V))
check("(a) Pi in cylindrical components: (v_r, v_phi, v_z)(r, z) -> (v_r, v_phi, -v_z)(r, -z)",
      zero(PV - field(fr(r, -z), fp(r, -z), -fz(r, -z))))
check("(e) the throat (origin) is the only fixed point of x -> -x",
      sp.solve(list(X + X), [x, y, z], dict=True) == [{x: 0, y: 0, z: 0}])

# Concrete smooth hourglass: inflow above, throat, outflow below, one swirl sense
a, w, Om = sp.symbols("a w Omega", positive=True)
vr_d = -a * r * z                     # inward for z > 0, outward for z < 0
vz_d = a * z ** 2 - w                 # downward through the throat
vphi_d = Om * r / (1 + r ** 2)        # swirl, vanishing on the axis
Vd = field(vr_d, vphi_d, vz_d)
check("hourglass example is incompressible (div v = 0)", sp.simplify(div(Vd)) == 0)
check("hourglass: inflow above, outflow below, down through the throat",
      sp.simplify(at(vr_d, (1, 0, 1))) < 0 and sp.simplify(at(vr_d, (1, 0, -1))) > 0
      and sp.simplify(at(vz_d, (0, 0, 0))) < 0)

PVd = parity(Vd)
check("(c) Pi keeps the swirl and reverses the through-flow (drain -> fountain)",
      zero(PVd - field(-vr_d, vphi_d, -vz_d)))
check("(c) so Pi exchanges which spiral feeds which: above is now outflow",
      sp.simplify(at((PVd.T * rhat)[0], (1, 0, 1))) > 0)

# Vorticity: carried as omega(-x); the sense of rotation is preserved
check("(b) curl(Pi v)(x) = omega(-x) for the general axisymmetric field",
      zero(curl(PV) - at(curl(V), -X)))
check("(b) on the axis the vorticity points the same way above and below the throat",
      sp.simplify(at(curl(Vd)[2], (0, 0, 1)) - at(curl(Vd)[2], (0, 0, -1))) == 0
      and sp.simplify(at(curl(Vd)[2], (0, 0, 1))) > 0)

# Helicity: pseudoscalar, flips; exactly the swirl x through-flow cross term
h = (V.T * curl(V))[0]
hP = (PV.T * curl(PV))[0]
check("(d) helicity density: h[Pi v](x) = -h[v](-x)", sp.simplify(hP + at(h, -X)) == 0)
Vs = field(0, fp(r, z), 0)
Vt = field(fr(r, z), 0, fz(r, z))
check("(d) pure swirl is achiral: v . curl v = 0", sp.simplify((Vs.T * curl(Vs))[0]) == 0)
check("(d) pure through-flow is achiral: v . curl v = 0", sp.simplify((Vt.T * curl(Vt))[0]) == 0)
check("(d) helicity density = swirl . curl(through-flow) + through-flow . curl(swirl)",
      sp.simplify(h - (Vs.T * curl(Vt))[0] - (Vt.T * curl(Vs))[0]) == 0)
hd = (Vd.T * curl(Vd))[0]
check("(d) the hourglass is chiral: helicity density on the axis at the throat is nonzero",
      sp.simplify(at(hd, (0, 0, 0))) != 0)
check("(d) and its mirror has the opposite helicity there",
      sp.simplify(at((PVd.T * curl(PVd))[0], (0, 0, 0)) + at(hd, (0, 0, 0))) == 0)
check("(d) reversing the swirl alone also flips the helicity",
      sp.simplify(at((field(vr_d, -vphi_d, vz_d).T * curl(field(vr_d, -vphi_d, vz_d)))[0], (0, 0, 0))
                  + at(hd, (0, 0, 0))) == 0)

# (f) The two chambers turn the same way at different rates
Ob, d = sp.symbols("Omega_bar delta", real=True)
step = z / sp.sqrt(1 + z ** 2)                 # smooth, odd: -> +1 above, -1 below
vphi_db = r / (1 + r ** 2) * (Ob + d * step)   # mean rate Ob, half-difference d
Vdb = field(vr_d, vphi_db, vz_d)
PVdb = parity(Vdb)
check("(f) Pi keeps the mean swirl rate and flips the half-difference (delta -> -delta)",
      zero(PVdb - field(-vr_d, vphi_db.subs(d, -d), -vz_d)))
far_A = sp.limit(Ob + d * step, z, sp.oo)
far_B = sp.limit(Ob + d * step, z, -sp.oo)
check("(f) far from the throat TetA turns at Ob + delta, TetB at Ob - delta",
      sp.simplify(far_A - (Ob + d)) == 0 and sp.simplify(far_B - (Ob - d)) == 0)
ex = {Ob: 1, d: sp.Rational(1, 4)}
check("(f) slower co-rotation: with 0 < delta < Ob both chambers turn the same way, TetB slower",
      far_B.subs(ex) > 0 and far_B.subs(ex) < far_A.subs(ex))
check("(f) the pure parity image co-rotates at one rate: delta = 0 is the only Pi-invariant case",
      sp.solve(sp.Eq(d, -d), d) == [0])
omega_r = (curl(Vdb).T * rhat)[0]
check("(f) the rate difference is a shear across the throat: radial vorticity there is nonzero iff delta != 0",
      sp.simplify(at(omega_r, (1, 0, 0)).subs(d, 0)) == 0
      and sp.simplify(at(omega_r, (1, 0, 0))).has(d)
      and sp.simplify(at(omega_r, (1, 0, 0)).subs(ex)) != 0)

if __name__ == "__main__":
    for name, ok in CHECKS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    n = sum(ok for _, ok in CHECKS)
    print(f"\n{n}/{len(CHECKS)} checks passed")
    sys.exit(0 if n == len(CHECKS) else 1)
