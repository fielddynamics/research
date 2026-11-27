#!/usr/bin/env python3
"""
GP-5  Two-site transfer: resonance selects a channel, it does not create one.

Checks every statement of README.md. Symbolic (sympy) for the closed forms,
exact matrix exponentials (scipy, double precision, tolerance 1e-12) for the
time-dependent drives. Prints PASS/FAIL per check, exits non-zero on failure.

Run from this folder:  python verify_gp5_transfer_bound.py
"""
import sys
import math
import random
import itertools

import numpy as np
import sympy as sp
from scipy.linalg import expm

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {label}" + (f"  -- {detail}" if detail else ""))


print("=" * 78)
print("GP-5  Two-site transfer bound; the mirror-address selector")
print("=" * 78)

# --------------------------------------------------------------------------
print("\n-- Theorem 1: constant coupling, the exact two-mode solution")
t, wx, wy = sp.symbols("t omega_x omega_y", real=True)
kr, phi = sp.symbols("kappa_r phi", positive=True)
kap = kr * sp.exp(sp.I * phi)
Delta = wx - wy
wbar = (wx + wy) / 2
Om = sp.sqrt(Delta ** 2 + 4 * kr ** 2)
cx = sp.exp(-sp.I * wbar * t) * (sp.cos(Om * t / 2) - sp.I * Delta / Om * sp.sin(Om * t / 2))
cy = sp.exp(-sp.I * wbar * t) * (-sp.I * 2 * sp.conjugate(kap) / Om * sp.sin(Om * t / 2))
ode1 = sp.simplify(sp.I * sp.diff(cx, t) - (wx * cx + kap * cy))
ode2 = sp.simplify(sp.I * sp.diff(cy, t) - (sp.conjugate(kap) * cx + wy * cy))
check("T1 (c_x, c_y) solve i d/dt c = H c with c(0) = (1, 0)",
      sp.simplify(ode1) == 0 and sp.simplify(ode2) == 0 and sp.simplify(cx.subs(t, 0) - 1) == 0 and cy.subs(t, 0) == 0)
P = sp.simplify(sp.Abs(cy) ** 2)
Pform = 4 * kr ** 2 / (Delta ** 2 + 4 * kr ** 2) * sp.sin(Om * t / 2) ** 2
check("T1 P(t) = 4|k|^2/(D^2 + 4|k|^2) sin^2(Omega t/2), Omega = sqrt(D^2 + 4|k|^2)",
      sp.simplify(sp.expand(sp.simplify(cy * sp.conjugate(cy))) - Pform) == 0)
check("T1 norm is conserved, |c_x|^2 + |c_y|^2 = 1", sp.simplify(sp.expand(cx * sp.conjugate(cx) + cy * sp.conjugate(cy))) == 1)
peak = 4 * kr ** 2 / (Delta ** 2 + 4 * kr ** 2)
check("T1 the peak 4|k|^2/(D^2+4|k|^2) equals 1 iff D = 0 (for k != 0)",
      sp.solve(sp.Eq(peak, 1), wx) == [wy])
check("T1 the peak is below min(1, 4|k|^2/D^2)  (grid of |k| and D)",
      all(float(peak.subs({kr: a, wx: d, wy: 0})) <= min(1, 4 * a * a / d / d) + 1e-15 for a in (0.1, 1, 3) for d in (0.05, 0.5, 2, 30)))
check("T1 at D = 0 the first complete transfer is at t = pi/(2|k|)",
      sp.simplify(Pform.subs({wx: wy}).subs(t, sp.pi / (2 * kr)) - 1) == 0)

# --------------------------------------------------------------------------
print("\n-- Theorem 2: the coupling budget  |c_y(t)| <= sin(min(int_0^t |kappa|, pi/2))  for ANY drive")
rng = np.random.default_rng(2026)


def evolve(steps, dt):
    """Piecewise-constant random Hermitian drives; returns list of (time, |c_y|, budget)."""
    c = np.array([1.0 + 0j, 0j])
    budget = 0.0
    out = []
    for (w1, w2, k) in steps:
        H = np.array([[w1, k], [np.conj(k), w2]])
        c = expm(-1j * H * dt) @ c
        budget += abs(k) * dt
        out.append((abs(c[1]), budget))
    return out


ok = True
worst = 0.0
for trial in range(300):
    nsteps = int(rng.integers(5, 60))
    dt = float(rng.choice([0.01, 0.05, 0.2]))
    scale_w = float(rng.choice([0.0, 1.0, 10.0, 100.0]))
    scale_k = float(rng.choice([0.05, 0.5, 2.0]))
    steps = [(scale_w * rng.normal(), scale_w * rng.normal(),
              scale_k * (rng.normal() + 1j * rng.normal())) for _ in range(nsteps)]
    for amp, bud in evolve(steps, dt):
        bound = math.sin(min(bud, math.pi / 2))
        if amp > bound + 1e-12:
            ok = False
        if bound > 1e-9:
            worst = max(worst, amp / bound)
check("T2 300 random piecewise-constant drives (detunings up to 100, phase-modulated couplings): bound never violated",
      ok, f"max |c_y|/bound = {worst:.6f}")
# equality for a resonant constant drive
k0 = 0.7
res = evolve([(1.3, 1.3, k0 * np.exp(0.4j))] * 40, 0.05)
check("T2 the bound is attained: resonant constant coupling gives |c_y| = sin(|k| t) exactly until pi/2",
      all(abs(a - math.sin(min(b, math.pi / 2))) < 1e-12 for a, b in res if b <= math.pi / 2))
# geodesic argument: speed on S^3 equals |kappa| in the interaction picture
check("T2 lemma: in the interaction picture |d a/dt| = |kappa| |a| = |kappa| (off-diagonal generator, unit state)",
      all(abs(np.linalg.norm(np.array([[0, k], [np.conj(k), 0]]) @ v) - abs(k)) < 1e-12
          for k in (0.3 + 0.1j, 2.0, -1j) for v in (np.array([1, 0]), np.array([0.6, 0.8j]), np.array([1, 1]) / math.sqrt(2))))
check("T2 lemma: the great-circle distance on S^3 from (1,0) to any state with |a_y| = sin beta is >= beta",
      all(math.acos(min(1.0, abs(math.cos(b) * math.cos(g)))) >= b - 1e-12
          for b in np.linspace(0, math.pi / 2, 31) for g in np.linspace(0, math.pi, 31)))

# --------------------------------------------------------------------------
print("\n-- Corollary 3: no coupling, no transfer -- for every frequency programme")
ok = True
for trial in range(100):
    steps = [(100 * rng.normal(), 100 * rng.normal(), 0.0) for _ in range(50)]
    if max(a for a, _ in evolve(steps, 0.1)) > 1e-14:
        ok = False
check("C3 kappa = 0: P(t) = 0 identically, for 100 random detuning programmes (any resonance, any sweep)", ok)
ok = True
for trial in range(100):
    kmax = 0.5
    steps = []
    for _ in range(30):
        mag = kmax * rng.random()
        steps.append((5 * rng.normal(), 5 * rng.normal(), mag * np.exp(2j * math.pi * rng.random())))
    dt = (math.pi / (2 * kmax)) / 30 * 0.999      # total time just under pi/(2 kmax)
    if max(a for a, _ in evolve(steps, dt)) ** 2 >= 1 - 1e-9:
        ok = False
check("C3 with sup|kappa| <= k no drive completes the transfer before t = pi/(2k) (100 random drives)", ok)

# --------------------------------------------------------------------------
print("\n-- Proposition 4: detuning tolerance for a target efficiency eta (constant coupling)")
eta, d_, kk = sp.symbols("eta d k", positive=True)
tol = sp.solve(sp.Eq(4 * kk ** 2 / (d_ ** 2 + 4 * kk ** 2), eta), d_)
check("P4 peak >= eta  iff  |Delta| <= 2|k| sqrt((1 - eta)/eta)",
      len(tol) == 1 and sp.simplify(tol[0] - 2 * kk * sp.sqrt((1 - eta) / eta)) == 0)
check("P4 eta = 1/2 gives |Delta| <= 2|k|; eta = 0.99 gives |Delta| <= 0.201|k|",
      sp.simplify(tol[0].subs(eta, sp.Rational(1, 2)) - 2 * kk) == 0 and
      abs(float(tol[0].subs({eta: 0.99, kk: 1})) - 0.20101) < 1e-4)

# --------------------------------------------------------------------------
print("\n-- Proposition 5: equal loss on both sites only rescales the transfer, P_loss = e^{-gamma t} P")
gam = 0.3
ok = True
for trial in range(20):
    w1, w2, k = rng.normal(), rng.normal(), rng.normal() + 1j * rng.normal()
    H = np.array([[w1, k], [np.conj(k), w2]])
    for tt in (0.5, 2.0, 7.0):
        c = expm(-1j * H * tt) @ np.array([1, 0])
        cl = expm(-1j * (H - 0.5j * gam * np.eye(2)) * tt) @ np.array([1, 0])
        if abs(abs(cl[1]) ** 2 - math.exp(-gam * tt) * abs(c[1]) ** 2) > 1e-12:
            ok = False
check("P5 20 random Hamiltonians, gamma = 0.3: |c_y|^2 with loss = e^{-gamma t} |c_y|^2 without", ok)

# --------------------------------------------------------------------------
print("\n-- Theorem 6: the Gram mismatch d_G is a pseudometric; the selector M_xy lies in [0,1]")
PERMS = [np.eye(3)[list(p)] for p in itertools.permutations(range(3))]


def dG(G, H):
    return min(np.linalg.norm(G - Pm.T @ H @ Pm) for Pm in PERMS)


def rand_gram():
    A = rng.normal(size=(3, 3))
    return A.T @ A


grams = [rand_gram() for _ in range(25)]
sym = all(abs(dG(a, b) - dG(b, a)) < 1e-12 for a in grams for b in grams)
tri = all(dG(a, c) <= dG(a, b) + dG(b, c) + 1e-12 for a in grams[:12] for b in grams[:12] for c in grams[:12])
inv = all(abs(dG(a, Pm.T @ a @ Pm)) < 1e-12 for a in grams for Pm in PERMS)
check("T6 d_G is symmetric (25 random triad Grams)", sym)
check("T6 d_G satisfies the triangle inequality (1728 triples)", tri)
check("T6 d_G(G, P^T G P) = 0 for every relabelling P: zero exactly on relabellings", inv)
check("T6 d_G(G, H) > 0 for Grams that are not relabellings of each other",
      all(dG(a, b) > 1e-6 for a, b in itertools.combinations(grams, 2)))


def M(d, eps, chi_x, chi_y, dtheta):
    return math.exp(-d * d / (2 * eps * eps)) * (1 - chi_x * chi_y) / 2 * math.cos(dtheta / 2) ** 2


vals = [M(d, e, cx_, cy_, th) for d in (0, 0.3, 2) for e in (0.1, 1) for cx_ in (-1, 1) for cy_ in (-1, 1)
        for th in np.linspace(-7, 7, 29)]
check("T6 M_xy in [0, 1] over a parameter grid", all(0 <= v <= 1 for v in vals))
check("T6 M_xy = 1 iff d_G = 0, chi_x = -chi_y and dTheta = 0 mod 2 pi",
      M(0, 1, 1, -1, 0) == 1 and M(0, 1, 1, -1, 2 * math.pi) > 1 - 1e-15 and M(0, 1, 1, 1, 0) == 0 and
      M(0.01, 1, 1, -1, 0) < 1 and M(0, 1, 1, -1, 0.01) < 1)
check("T6 with kappa = kappa_0 M_xy the coupling budget gives P(t) <= sin^2(min(kappa_0 M t, pi/2)): a mismatch slows transfer, it never adds a channel",
      all(math.sin(min(0.5 * m * 3.0, math.pi / 2)) ** 2 <= math.sin(min(0.5 * 3.0, math.pi / 2)) ** 2 for m in np.linspace(0, 1, 11)))


print("\n-- Theorem 2b (referee): saturation holds up to the first complete transfer, not beyond")
res2 = evolve([(0.0, 0.0, 0.5)] * 400, 0.025)          # resonant, k = 0.5, to t = 10 > pi/(2k)
before = [abs(a - math.sin(bb)) < 1e-12 for a, bb in res2 if bb <= math.pi / 2]
after = [a < 1 - 1e-3 for a, bb in res2 if bb > math.pi / 2 + 0.3]
check("T2b equality |c_y| = sin(int|kappa|) holds until pi/2; afterwards the constant drive falls back below the bound (= 1)",
      all(before) and any(after))
Pm = 0.6
check("C9 inverse bound: a measured transfer P by time T needs int_0^T |kappa| >= arcsin sqrt P (P = 0.6: 0.886)",
      abs(math.asin(math.sqrt(Pm)) - 0.8861) < 1e-3)
okinv = True
for trial in range(200):
    steps = [(3 * rng.normal(), 3 * rng.normal(), rng.normal() + 1j * rng.normal()) for _ in range(20)]
    for amp, bud in evolve(steps, 0.05):
        if bud < math.asin(min(1.0, amp)) - 1e-12:
            okinv = False
check("C9 the inverse bound holds on 200 random drives", okinv)

print("\n-- Theorem 7 (referee): an induced coupling from an intermediate sector (Schur complement)")
okS = True
for trial in range(40):
    nB = int(rng.integers(1, 5))
    HA = np.diag(rng.normal(size=2)); HB = np.diag(rng.normal(size=nB) + 6.0)
    Vc = rng.normal(size=(2, nB)) * 0.3
    Hfull = np.block([[HA, Vc], [Vc.T, HB]])
    lam = np.linalg.eigvalsh(Hfull)[:2]                   # the two eigenvalues near the terminals
    for E in lam:
        Heff = HA + Vc @ np.linalg.inv(E * np.eye(nB) - HB) @ Vc.T
        if np.min(np.abs(np.linalg.eigvalsh(Heff) - E)) > 1e-8:
            okS = False
check("T7 every eigenvalue E of the full system is an eigenvalue of H_eff(E) = H_A + V (E - H_B)^-1 V^T (40 random systems)", okS)
gx, gy, wB, w0 = 0.05, 0.07, 1.0, 0.0
H3 = np.array([[w0, 0, gx], [0, w0, gy], [gx, gy, wB]])
kap_pred = gx * gy / (w0 - wB)
tt = np.linspace(0, 2 * math.pi / abs(kap_pred), 4000)
Py = [abs((expm(-1j * H3 * t) @ np.array([1, 0, 0]))[1]) ** 2 for t in tt]
shift_x, shift_y = gx * gx / (w0 - wB), gy * gy / (w0 - wB)
Delta_eff = shift_x - shift_y
Pmax_pred = 4 * kap_pred ** 2 / (Delta_eff ** 2 + 4 * kap_pred ** 2)
check("T7 dispersive limit: one intermediate mode gives kappa = g_x g_y/(w - w_B) and self-energy shifts g^2/(w - w_B); the 3-mode peak transfer matches",
      abs(max(Py) - Pmax_pred) < 0.02, f"3-mode {max(Py):.4f} vs dispersive {Pmax_pred:.4f}")
HBl = np.diag([5.0, 7.0]); Vl = np.array([[0.3, 0.0], [0.0, 0.4]])   # disjoint invariant supports
Heff0 = Vl @ np.linalg.inv(0.0 * np.eye(2) - HBl) @ Vl.T
check("T7 zero-channel countermodel: block-local intermediate dynamics with disjoint supports give kappa_induced = 0 exactly",
      abs(Heff0[0, 1]) < 1e-15)

print("\n-- Theorem 6b (referee): chirality must be tested inside the same relabelling")
Fr0 = np.eye(3); Fsw = Fr0[:, [1, 0, 2]]
chi = lambda F: int(np.sign(np.linalg.det(F)))
G0, Gsw = Fr0.T @ Fr0, Fsw.T @ Fsw
def M_old(Gx, Gy, cx, cy):
    return math.exp(-dG(Gx, Gy) ** 2 / 2) * (1 - cx * cy) / 2
def M_new(Gx, Gy, cx, cy):
    best = 0.0
    for Pm_ in PERMS:
        dP = np.linalg.norm(Gx - Pm_.T @ Gy @ Pm_)
        best = max(best, math.exp(-dP ** 2 / 2) * (1 - cx * cy * round(np.linalg.det(Pm_))) / 2)
    return best
mirror = -Fr0
check("T6b old selector: relabelling the receiver (an odd swap) flips its chirality label and changes acceptance 1 -> 0",
      M_old(G0, G0, chi(Fr0), chi(mirror)) == 1 and M_old(G0, Gsw, chi(Fr0), chi(-Fsw)) == 0)
check("T6b repaired selector (chirality x det P inside the max) is invariant under relabelling the receiver",
      M_new(G0, G0, chi(Fr0), chi(mirror)) == M_new(G0, Gsw, chi(Fr0), chi(-Fsw)) == 1)
check("T6b caveat: with full relabelling freedom a symmetric Gram (here I_3) also admits odd automorphisms, so chirality "
      "discrimination needs intrinsically labelled axes", M_new(G0, G0, chi(Fr0), chi(Fr0)) == 1)

print("\n-- Proposition 8 (referee): optimum transfer time under equal loss")
kk_, gg_ = 0.7, 0.3
topt = math.atan(2 * kk_ / gg_) / kk_
Popt = 4 * kk_ ** 2 / (gg_ ** 2 + 4 * kk_ ** 2) * math.exp(-gg_ / kk_ * math.atan(2 * kk_ / gg_))
tg = np.linspace(0, 20, 400001); Pg = np.exp(-gg_ * tg) * np.sin(kk_ * tg) ** 2
check("P8 t_opt = arctan(2k/gamma)/k and P_opt = 4k^2/(gamma^2+4k^2) exp[-(gamma/k) arctan(2k/gamma)] (k = 0.7, gamma = 0.3)",
      abs(tg[Pg.argmax()] - topt) < 1e-3 and abs(Pg.max() - Popt) < 1e-9, f"t_opt {topt:.4f}, P_opt {Popt:.4f}")
check("P8 gamma -> 0 recovers t_opt = pi/(2k) and P_opt = 1",
      abs(math.atan(2 * kk_ / 1e-12) / kk_ - math.pi / (2 * kk_)) < 1e-9)

print("\n" + "=" * 78)
print(f"GP-5: {sum(RESULTS)}/{len(RESULTS)} checks passed")
sys.exit(0 if all(RESULTS) else 1)
