"""
Verification for 'Singularities, Information and Holography in GFD'.

Part A  Symbolic: the four GFD identities used in the note.
Part B  Numerical: the Raychaudhuri equation for a metric-compatible
        connection with torsion (the full 64-component connection),
        and the decomposition of its torsion term into vector, totally
        antisymmetric (axial) and tensor parts.
Part C  The black-hole regime: where horizons sit on the mu scale, and
        the size of torsion terms bounded by a0/c^2 against focusing.

Run:  python verify_identities.py      (exit code 0 if all checks pass)
"""
from __future__ import annotations

import itertools
import sys

import numpy as np
import sympy as sp

CHECKS: list[tuple[str, bool]] = []


def check(name: str, ok: bool) -> None:
    CHECKS.append((name, bool(ok)))


# ---------------------------------------------------------------- Part A
g, a0, x, u, y, t, r, G = sp.symbols("g a0 x u y t r G", positive=True)
mu = x / (x + 1)

gB = sp.simplify((g * (1 - mu)).subs(x, g / a0))
check("A1 torsion-sector acceleration g(1-mu) = a0 g/(g+a0)", sp.simplify(gB - a0 * g / (g + a0)) == 0)
check("A1 limit g -> oo of g(1-mu) is a0", sp.limit(gB, g, sp.oo) == a0)

F = y - 2 * sp.sqrt(y) + 2 * sp.log(1 + sp.sqrt(y))
check("A2 dF/dy = mu(sqrt y)", sp.simplify(sp.diff(F, y) - mu.subs(x, sp.sqrt(y))) == 0)
check("A2 log term = integral of 2(1-mu(u)) du", sp.simplify(sp.integrate(2 * (1 - mu.subs(x, u)), u) - 2 * sp.log(1 + u)) == 0)
s_t = ((x - 1) / (x + 1)).subs(x, sp.exp(t))
check("A2 s(x) = tanh(t/2) with t = ln x",
      all(abs(float((s_t - sp.tanh(t / 2)).subs(t, v))) < 1e-14 for v in (-5, -0.3, 0.7, 4)))

mut = mu.subs(x, sp.exp(t))
check("A3 d mu / d ln x = mu (1 - mu)", sp.simplify(sp.diff(mut, t) - mut * (1 - mut)) == 0)
beta = lambda m: m * (1 - m)
mm = sp.symbols("m")
check("A3 fixed points mu = 0, 1 with exponents +1, -1",
      sp.diff(beta(mm), mm).subs(mm, 0) == 1 and sp.diff(beta(mm), mm).subs(mm, 1) == -1)
check("A3 maximum running 1/4 at mu = 1/2", beta(sp.Rational(1, 2)) == sp.Rational(1, 4))

Mx = (g * (1 - mu)).subs(x, g / a0) * r ** 2 / G
check("A4 extra mass = a0 r^2 mu / G", sp.simplify(Mx - a0 * r ** 2 / G * mu.subs(x, g / a0)) == 0)

# ---------------------------------------------------------------- Part B
# Tangent space at a point, orthonormal frame: eta = diag(-1,1,1,1), u = (1,0,0,0).
rng = np.random.default_rng(7)
eta = np.diag([-1.0, 1.0, 1.0, 1.0])
uu = np.array([1.0, 0.0, 0.0, 0.0])
h = eta + np.outer(eta @ uu, eta @ uu)            # projector h_ab (lower indices)


def kinematic_B(theta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """B^a_d = nabla_d u^a for an autoparallel congruence: theta/3 h + sigma + omega, all spatial."""
    S = rng.normal(size=(3, 3)); S = S + S.T; S -= np.trace(S) / 3 * np.eye(3)
    W = rng.normal(size=(3, 3)); W = W - W.T
    sig = np.zeros((4, 4)); om = np.zeros((4, 4))
    sig[1:, 1:] = S; om[1:, 1:] = W
    exp = np.zeros((4, 4)); exp[1:, 1:] = theta / 3 * np.eye(3)
    return exp, sig, om                              # mixed components B^a_d (spatial block)


def torsion_parts(T: np.ndarray):
    """T[d,a,b] = T^d_{ab}, antisymmetric in a,b. Return vector, totally antisymmetric, tensor parts."""
    Tl = np.einsum("de,eab->dab", eta, T)          # T_{dab}
    Tv = np.einsum("aab->b", T)                    # T_b = T^a_{ab}
    vec_l = (np.einsum("da,b->dab", eta, Tv) - np.einsum("db,a->dab", eta, Tv)) / 3.0
    ax_l = np.zeros_like(Tl)
    for p in itertools.permutations(range(3)):
        sgn = np.linalg.det(np.eye(3)[list(p)])
        ax_l += sgn * np.transpose(Tl, p)
    ax_l /= 6.0
    ten_l = Tl - vec_l - ax_l
    up = lambda L: np.einsum("de,eab->dab", np.linalg.inv(eta), L)
    return up(vec_l), up(ax_l), up(ten_l), Tv


ok_dec = ok_vec = ok_ax = ok_ten = ok_ray = True
for trial in range(200):
    T = rng.normal(size=(4, 4, 4)); T = T - np.transpose(T, (0, 2, 1))   # 24 independent components
    theta = rng.normal()
    E, Sg, W = kinematic_B(theta); B = E + Sg + W
    Tvec, Tax, Tten, Tv = torsion_parts(T)
    term = lambda TT, BB: np.einsum("dab,b,ad->", TT, uu, BB)          # T^d_{ab} u^b B^a_d
    ok_dec &= np.allclose(Tvec + Tax + Tten, T)
    # vector part couples only to expansion: (1/3)(T_b u^b) theta
    ok_vec &= np.isclose(term(Tvec, B), (Tv @ uu) * theta / 3.0)
    # totally antisymmetric part couples only to vorticity
    ok_ax &= np.isclose(term(Tax, E), 0) and np.isclose(term(Tax, Sg), 0) and np.isclose(term(Tax, B), term(Tax, W))
    # tensor part: no coupling to expansion
    ok_ten &= np.isclose(term(Tten, E), 0)
    # Raychaudhuri algebra: -(nabla_a u^b)(nabla_b u^a) = -theta^2/3 - sigma^2 + omega^2
    lhs = -np.einsum("ab,ba->", B, B)
    Sl = eta @ Sg; Wl = eta @ W
    sig2 = np.einsum("ab,ab->", Sl, Sl); om2 = np.einsum("ab,ab->", Wl, Wl)
    ok_ray &= np.isclose(lhs, -theta ** 2 / 3 - sig2 + om2)

check("B0 torsion = vector + totally antisymmetric + tensor (4 + 4 + 16 = 24)", ok_dec)
check("B1 vector torsion term = (1/3)(T.u) theta  (couples to expansion only)", ok_vec)
check("B2 totally antisymmetric (axial) torsion couples to vorticity only", ok_ax)
check("B3 tensor torsion does not couple to expansion", ok_ten)
check("B4 -(nabla u)(nabla u) = -theta^2/3 - sigma^2 + omega^2", ok_ray)

# ---------------------------------------------------------------- Part C
Gn, c, Msun, A0 = 6.674e-11, 2.998e8, 1.989e30, 1.2e-10
rows = []
for name, M in (("10 M_sun", 10 * Msun), ("Sgr A*", 4.3e6 * Msun), ("M87*", 6.5e9 * Msun)):
    kappa = c ** 4 / (4 * Gn * M)                 # horizon surface gravity
    X = kappa / A0
    rs = 2 * Gn * M / c ** 2
    focus = 1 / rs ** 2                           # focusing scale R_ab u^a u^b ~ 1/r_s^2  [m^-2]
    tors = (A0 / c ** 2) * (1 / rs)               # bounded torsion term ~ (a0/c^2) * theta, theta ~ 1/r_s
    rows.append((name, kappa, X, 1 / (X + 1), tors / focus))
check("C1 horizons lie deep in the TetA regime (1 - mu < 1e-13)", all(r_[3] < 1e-13 for r_ in rows))
check("C2 a0-bounded torsion terms are < 1e-13 of focusing at every horizon", all(r_[4] < 1e-13 for r_ in rows))

if __name__ == "__main__":
    for name, ok in CHECKS:
        print(("PASS  " if ok else "FAIL  ") + name)
    print("\nBlack-hole regime:")
    print(f"  {'body':<10}{'kappa [m/s^2]':>15}{'x':>11}{'1 - mu':>11}{'torsion/focus':>15}")
    for n_, k_, X_, b_, rr in rows:
        print(f"  {n_:<10}{k_:>15.2e}{X_:>11.1e}{b_:>11.1e}{rr:>15.1e}")
    n_ok = sum(ok for _, ok in CHECKS)
    print(f"\n{n_ok}/{len(CHECKS)} checks passed")
    sys.exit(0 if n_ok == len(CHECKS) else 1)
