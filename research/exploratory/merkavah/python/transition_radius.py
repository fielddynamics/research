"""
The field chariot of a bounded mass: its GFD transition sphere.

For an isolated mass M, the Newtonian field g = GM/r^2 falls to the
acceleration scale a0 at the transition radius

    r_t = sqrt(G M / a0),

where x = g/a0 = 1, mu = 1/2, s = 0 and f = 17: the Field Origin state,
at which TetA and TetB carry equal shares. Inside r_t the TetA share
dominates; outside it the TetB share does. r_t scales as M^(1/2) and
the construction is the same at every mass: the scale-invariant
statement of the merkavah thesis (CORE_THINKING.md, Proposition 2).

Run:  python transition_radius.py
"""
from __future__ import annotations

import math

G = 6.67430e-11          # m^3 kg^-1 s^-2
A0 = 1.2e-10             # m s^-2, conventional value
M_E = 9.1093837139e-31   # kg
R_E = 2.8179403205e-15   # m, classical electron radius
K = 4
AU = 1.495978707e11
PC = 3.0856775814913673e16
M_SUN = 1.98892e30

# (name, mass [kg], characteristic radius of the body [m])
BODIES = [
    ("electron",          M_E,           R_E),
    ("proton",            1.67262192e-27, 0.8414e-15),
    ("human (70 kg)",     70.0,          (3 * 0.070 / (4 * math.pi)) ** (1 / 3)),  # equal-volume sphere
    ("Great Pyramid",     5.9e9,         146.6 / 2),
    ("Earth",             5.9722e24,     6.371e6),
    ("Sun",               M_SUN,         6.957e8),
    ("Milky Way baryons", 6.0e10 * M_SUN, 15e3 * PC),
]


def transition_radius(m: float, a0: float = A0) -> float:
    return math.sqrt(G * m / a0)


def mu(x: float) -> float:
    return x / (x + 1.0)


def surface_x(m: float, r: float, a0: float = A0) -> float:
    return G * m / r ** 2 / a0


def fmt_len(r: float) -> str:
    if r < 1e-9:
        return f"{r * 1e15:.3g} fm"
    if r < 1e3:
        return f"{r:.3g} m"
    if r < 1e10:
        return f"{r / 1e3:.3g} km"
    if r < 1e16:
        return f"{r / AU:.3g} AU"
    return f"{r / (1e3 * PC):.3g} kpc"


if __name__ == "__main__":
    print(f"{'body':<20}{'r_t = sqrt(GM/a0)':>20}{'r_t / R_body':>15}{'x at surface':>15}{'TetB share 1-mu':>18}")
    for name, m, r in BODIES:
        rt = transition_radius(m)
        xs = surface_x(m, r)
        print(f"{name:<20}{fmt_len(rt):>20}{rt / r:>15.3g}{xs:>15.3g}{1 - mu(xs):>18.3g}")
    a0_e = K ** 2 * G * M_E / R_E ** 2
    print(f"\na0 from K^2 G m_e / r_e^2 = {a0_e:.4e} m/s^2; with it r_t(electron) = r_e / K exactly")
    print(f"human on Earth's surface: x = {9.81 / A0:.3g}, TetB share = {1 - mu(9.81 / A0):.3g}")
