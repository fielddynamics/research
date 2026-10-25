#!/usr/bin/env python3
"""
gfd_oscillator_tetrahedral.py
=============================

n-node Network Flow with Joint (mu, phi) Dynamics
--------------------------------------------------

Extends gfd_oscillator_cbit.py to two n-node topologies:

    1. Fully connected tetrahedron (4 nodes)
    2. Linear cascade (n nodes)

Each node carries a c-bit state (mu_i, phi_i):

    tau_mu  * dmu_i/dt  = x_i(1 - mu_i)^2 - mu_i
    tau_phi * dphi_i/dt = omega_0 + K_pll Sum_j A_ij sin(phi_j - phi_i)

For the tetrahedron, x_i = x_ext + c_amp Sum_{j != i} A_ij (1 - mu_j)/mu_j.
For the cascade,    x_i = (1/pi) * T(mu_{i-1}) -> spatial-law inversion.

Predictions to verify (analytical):

  [§A]  4-node tetrahedron, x_ext=1, c_amp=0:   mu* = 1/phi^2 = (3-sqrt(5))/2
        Phases lock under K_pll > 0.
  [§B]  4-node tetrahedron, c_amp > 0:          mu* SHIFTS away from 1/phi^2.
        Solve 3 c_amp (1-mu*)^3 = mu*^2 and compare.
  [§C]  6-node cascade, cell 0 at x=1:           mu_0 = 1/phi^2, tail ratio
        mu_i / mu_{i+1} -> pi.
        Phase channel locks coherently down the chain.
  [§D]  Cascade phase propagation:               WITH vs WITHOUT K_pll.

All results compared numerically to closed-form predictions.

Author: Stephen Nelson / Field Dynamics Research
"""

import os
import math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.size"] = 11

OUT = "/mnt/user-data/outputs"
os.makedirs(OUT, exist_ok=True)

PHI = (1 + math.sqrt(5)) / 2.0
FIELD_ORIGIN_MU = 1.0 / PHI**2                  # (3 - sqrt(5))/2 approx 0.381966
INV_PI = 1.0 / math.pi                          # cascade attenuation


# ========================================================================
#   CORE PHYSICS (reused)
# ========================================================================

def transducer(mu):
    mu = np.clip(mu, 1e-10, 1 - 1e-10)
    return mu / (1.0 - mu + mu**2)


def mu_B_exact(x):
    x = max(float(x), 1e-10)
    return ((2*x + 1) - math.sqrt(4*x + 1)) / (2*x)


def cell_rhs_mu(mu_i, x_i, tau_mu=1.0):
    mu_i = np.clip(mu_i, 1e-10, 1 - 1e-10)
    return (x_i * (1 - mu_i)**2 - mu_i) / tau_mu


# ========================================================================
#   TETRAHEDRAL ODE
# ========================================================================

def tetra_joint_rhs(t, y, n, x_ext, omega_0, K_pll, c_amp, adj,
                    tau_mu=1.0, tau_phi=1.0):
    """Joint (mu, phi) dynamics on a fully-connected n-node graph."""
    mu = y[:n]
    phi = y[n:2*n]
    dmu = np.zeros(n)
    dphi = np.zeros(n)

    for i in range(n):
        x_i = x_ext
        for j in range(n):
            if j != i and adj[i, j] != 0.0:
                mu_j = np.clip(mu[j], 1e-10, 1 - 1e-10)
                x_i += c_amp * adj[i, j] * (1.0 - mu_j) / mu_j
        dmu[i] = cell_rhs_mu(mu[i], x_i, tau_mu=tau_mu)

    for i in range(n):
        d = omega_0
        for j in range(n):
            if j != i and adj[i, j] != 0.0:
                d += K_pll * adj[i, j] * math.sin(phi[j] - phi[i])
        dphi[i] = d / tau_phi

    return np.concatenate([dmu, dphi])


# ========================================================================
#   §A  TETRAHEDRON AT UNIT DRIVE, ZERO AMP COUPLING
# ========================================================================
#
# With c_amp = 0, every node is independently driven at x_ext = 1.  The
# interior law at unit drive has the closed-form fixed point
#     mu* = 1/phi^2  =  (3 - sqrt(5)) / 2
# independent of topology.  The phase channel still sees its Kuramoto
# coupling through the tetrahedral adjacency.  Prediction:
#   * all 4 amplitudes converge to 1/phi^2 from ANY initial configuration
#   * all 4 phases lock (Delta phi_ij -> 0 for every pair)
# with the amplitude trajectory essentially independent of K_pll.

def sim_tetrahedral_golden():
    n = 4
    adj = np.ones((n, n)) - np.eye(n)          # K_4 (fully connected)
    omega_0 = 1.0
    K_pll = 0.5
    c_amp = 0.0
    x_ext = 1.0                                # field origin drive

    # Asymmetric start
    y0 = np.zeros(2 * n)
    y0[:n] = np.array([0.9, 0.1, 0.5, 0.7])
    y0[n:] = np.array([0.0, 1.2, -0.8, 2.1])

    t_span = (0.0, 25.0)
    t_eval = np.linspace(*t_span, 2000)
    sol = solve_ivp(tetra_joint_rhs, t_span, y0, t_eval=t_eval, method="RK45",
                    args=(n, x_ext, omega_0, K_pll, c_amp, adj, 1.0, 1.0),
                    max_step=0.02)

    mus_final = sol.y[:n, -1]
    phases_u = np.unwrap(sol.y[n:2*n], axis=1)
    # Phase differences relative to node 0
    dphi = phases_u - phases_u[0:1, :]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    colors = ["#2c3e50", "#e74c3c", "#27ae60", "#8e44ad"]
    for i in range(n):
        ax.plot(sol.t, sol.y[i], color=colors[i], linewidth=1.6,
                label=fr"$\mu_{i}(t)$   $\mu_{{0,i}} = {y0[i]:.2f}$")
    ax.axhline(y=FIELD_ORIGIN_MU, color="gold", linestyle="--",
               linewidth=2, alpha=0.8,
               label=fr"$1/\varphi^2 = {FIELD_ORIGIN_MU:.6f}$")
    ax.set_xlabel("time")
    ax.set_ylabel(r"amplitude $\mu$")
    ax.set_ylim(0, 1)
    ax.set_title(r"Tetrahedron, $x_{\mathrm{ext}}=1$, $c_{\mathrm{amp}}=0$:"
                 r"  all nodes $\to 1/\varphi^2$", fontweight="bold")
    ax.legend(loc="upper right", fontsize=9); ax.grid(True, alpha=0.3)

    ax = axes[1]
    for i in range(1, n):
        ax.plot(sol.t, dphi[i], color=colors[i], linewidth=1.6,
                label=fr"$\phi_{i} - \phi_0$")
    ax.axhline(y=0, color="gold", linestyle="--", linewidth=2, alpha=0.8,
               label="lock")
    ax.set_xlabel("time")
    ax.set_ylabel(r"$\phi_i - \phi_0$ (rad)")
    ax.set_title(fr"Phase channel: Kuramoto ($K = {K_pll}$) locks all pairs",
                 fontweight="bold")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"{OUT}/tetra_golden_ratio.png"
    plt.savefig(path, dpi=200); plt.close()

    # Numerical verification
    mu_err = np.max(np.abs(mus_final - FIELD_ORIGIN_MU))
    phase_err = np.max(np.abs(dphi[:, -1]))
    print(f"  [§A] saved {os.path.basename(path)}")
    print(f"       all 4 final mu:      {[f'{v:.6f}' for v in mus_final]}")
    print(f"       prediction  1/phi^2 = {FIELD_ORIGIN_MU:.6f}")
    print(f"       max |Delta mu|       {mu_err:.2e}")
    print(f"       max |Delta phi|      {phase_err:.2e}   (both should be tiny)")
    passed = mu_err < 1e-5 and phase_err < 1e-3
    print(f"       Golden-ratio fixed point survives joint picture: {passed}")


# ========================================================================
#   §B  TETRAHEDRON WITH AMP COUPLING ON -> SHIFTED FIXED POINT
# ========================================================================
#
# At symmetric equilibrium mu_i = mu* on all 4 nodes with c_amp > 0:
#     x* = x_ext  +  3 c_amp (1 - mu*)/mu*
# and the interior law x* (1 - mu*)^2 = mu* becomes
#     [x_ext + 3 c_amp (1 - mu*)/mu*] (1 - mu*)^2  =  mu*
# i.e.
#     x_ext mu* (1 - mu*)^2  +  3 c_amp (1 - mu*)^3  =  mu*^2.
#
# For x_ext = 1, this is a cubic in mu*.  Solve numerically and compare
# to the simulation.  Demonstrates that the golden-ratio fixed point is
# a SPECIAL CASE (c_amp = 0); switching amplitude coupling on shifts it.

def tetra_symmetric_fixed_point(x_ext, c_amp, n_neighbors=3):
    """Solve  x_ext mu (1-mu)^2 + n_nb c_amp (1-mu)^3 = mu^2  on (0, 1).

    Bisection between 1e-6 and 1 - 1e-6.
    """
    def f(mu):
        return x_ext * mu * (1 - mu)**2 + n_neighbors * c_amp * (1 - mu)**3 - mu**2

    lo, hi = 1e-6, 1 - 1e-6
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if abs(fm) < 1e-14:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def sim_tetrahedral_coupled():
    n = 4
    adj = np.ones((n, n)) - np.eye(n)
    omega_0 = 1.0
    K_pll = 0.5
    x_ext = 1.0

    # Test several coupling strengths; tabulate fixed-point shifts.
    c_values = [0.0, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0]
    rows = []

    for c_amp in c_values:
        y0 = np.zeros(2 * n)
        y0[:n] = np.array([0.9, 0.1, 0.5, 0.7])
        y0[n:] = np.array([0.0, 1.2, -0.8, 2.1])

        t_span = (0.0, 40.0)
        t_eval = np.linspace(*t_span, 1500)
        sol = solve_ivp(tetra_joint_rhs, t_span, y0, t_eval=t_eval, method="RK45",
                        args=(n, x_ext, omega_0, K_pll, c_amp, adj, 1.0, 1.0),
                        max_step=0.02)

        mu_measured = np.mean(sol.y[:n, -1])
        mu_predicted = tetra_symmetric_fixed_point(x_ext, c_amp, n_neighbors=3)
        err = abs(mu_measured - mu_predicted)
        rows.append((c_amp, mu_measured, mu_predicted, err))

    # Plot: fixed-point shift vs c_amp
    c_arr = np.array([r[0] for r in rows])
    mu_meas = np.array([r[1] for r in rows])
    mu_pred = np.array([r[2] for r in rows])

    # Dense theoretical curve
    c_dense = np.linspace(0.0, 2.0, 200)
    mu_dense = np.array([tetra_symmetric_fixed_point(x_ext, c, 3) for c in c_dense])

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(c_dense, mu_dense, "-", color="#e74c3c", linewidth=1.8,
            label=r"predicted $\mu^*(c_{\mathrm{amp}})$")
    ax.plot(c_arr, mu_meas, "o", color="#2c3e50", markersize=9,
            label=r"measured at $t = 40$")
    ax.axhline(y=FIELD_ORIGIN_MU, color="gold", linestyle="--",
               linewidth=1.8, alpha=0.8,
               label=fr"$1/\varphi^2 = {FIELD_ORIGIN_MU:.4f}$ "
                     r"(golden at $c_{\mathrm{amp}}=0$)")
    ax.set_xlabel(r"amp coupling $c_{\mathrm{amp}}$")
    ax.set_ylabel(r"symmetric fixed-point $\mu^*$")
    ax.set_title(r"Tetrahedron: amp coupling shifts the fixed point "
                 r"away from $1/\varphi^2$", fontweight="bold")
    ax.legend(); ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"{OUT}/tetra_coupled_shift.png"
    plt.savefig(path, dpi=200); plt.close()

    print(f"  [§B] saved {os.path.basename(path)}")
    print(f"       c_amp    measured mu*       predicted mu*       |err|")
    print(f"       -----    -------------       --------------      -----")
    for c_amp, mu_m, mu_p, err in rows:
        marker = "  <- golden ratio" if c_amp == 0 else ""
        print(f"       {c_amp:<5.2f}    {mu_m:.8f}          "
              f"{mu_p:.8f}          {err:.2e}{marker}")


# ========================================================================
#   CASCADE ODE
# ========================================================================

def cascade_joint_rhs(t, y, n, x_drive, omega_0, K_pll,
                      penalty=INV_PI, tau_mu=1.0, tau_phi=1.0):
    """Linear cascade: cell 0 externally driven; cell i>0 driven by
    (1/pi) * T(mu_{i-1}) interpreted through the spatial-law inverse.

    Phase dynamics: bidirectional Kuramoto along the chain adjacency.
    """
    mu = y[:n]
    phi = y[n:2*n]
    dmu = np.zeros(n)
    dphi = np.zeros(n)

    for i in range(n):
        if i == 0:
            x_i = x_drive
        else:
            # Neighbour's spatial capacity via transducer, attenuated by 1/pi
            mu_A = penalty * transducer(mu[i-1])
            mu_A = float(np.clip(mu_A, 1e-10, 1 - 1e-10))
            x_i = mu_A / (1.0 - mu_A)          # TetA inversion
        dmu[i] = cell_rhs_mu(mu[i], x_i, tau_mu=tau_mu)

    for i in range(n):
        d = omega_0
        if i > 0:
            d += K_pll * math.sin(phi[i-1] - phi[i])
        if i < n - 1:
            d += K_pll * math.sin(phi[i+1] - phi[i])
        dphi[i] = d / tau_phi

    return np.concatenate([dmu, dphi])


# ========================================================================
#   §C  CASCADE JOINT DYNAMICS  ->  GOLDEN RATIO + 1/pi + PHASE LOCK
# ========================================================================

def sim_cascade_joint():
    n = 6
    x_drive = 1.0                              # cell 0 at field origin drive
    omega_0 = 1.0
    K_pll = 0.5

    y0 = np.zeros(2 * n)
    y0[:n] = np.full(n, 0.1)                    # low initial amplitudes
    y0[n:] = np.array([0.0, 0.9, -1.3, 2.2, -0.5, 1.8])

    t_span = (0.0, 60.0)
    t_eval = np.linspace(*t_span, 3000)
    sol = solve_ivp(cascade_joint_rhs, t_span, y0, t_eval=t_eval, method="RK45",
                    args=(n, x_drive, omega_0, K_pll, INV_PI, 1.0, 1.0),
                    max_step=0.03)

    mus_final = sol.y[:n, -1]
    phases_u = np.unwrap(sol.y[n:2*n], axis=1)
    dphi_rel0 = phases_u - phases_u[0:1, :]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # (0,0) Amplitude trajectories
    ax = axes[0, 0]
    colors = plt.cm.viridis(np.linspace(0, 0.9, n))
    for i in range(n):
        ax.plot(sol.t, sol.y[i], color=colors[i], linewidth=1.5,
                label=f"cell {i}")
    ax.axhline(y=FIELD_ORIGIN_MU, color="gold", linestyle="--",
               linewidth=1.8, alpha=0.8,
               label=fr"$1/\varphi^2 = {FIELD_ORIGIN_MU:.3f}$")
    ax.set_xlabel("time")
    ax.set_ylabel(r"amplitude $\mu$")
    ax.set_title("Cascade amplitudes", fontweight="bold")
    ax.legend(loc="right", fontsize=9); ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.02, 0.45)

    # (0,1) Final amplitudes vs 1/pi^i prediction from cell 1
    ax = axes[0, 1]
    idx = np.arange(n)
    ax.bar(idx, mus_final, color=colors, alpha=0.8, label="simulated")
    # pi-decay reference from mu_1
    mu_pred_tail = mus_final[1] * np.array([INV_PI**(i-1) for i in range(1, n)])
    ax.plot(idx[1:], mu_pred_tail, "ko--", alpha=0.8,
            label=r"$\mu_1 \cdot (1/\pi)^{i-1}$")
    ax.axhline(y=FIELD_ORIGIN_MU, color="gold", linestyle="--", alpha=0.6,
               label=r"$1/\varphi^2$")
    ax.set_xlabel("cell index")
    ax.set_ylabel(r"settled $\mu$")
    ax.set_title(r"Final amplitudes and $1/\pi$ tail prediction",
                 fontweight="bold")
    ax.set_yscale("log"); ax.set_ylim(1e-5, 1)
    ax.legend(); ax.grid(True, alpha=0.3, which="both")

    # (1,0) Phase differences rel to cell 0
    ax = axes[1, 0]
    for i in range(1, n):
        ax.plot(sol.t, dphi_rel0[i], color=colors[i], linewidth=1.5,
                label=fr"$\phi_{i} - \phi_0$")
    ax.axhline(y=0, color="gold", linestyle="--", linewidth=1.8, alpha=0.8)
    ax.set_xlabel("time")
    ax.set_ylabel(r"$\phi_i - \phi_0$ (rad)")
    ax.set_title(fr"Phase lock down the chain ($K = {K_pll}$)",
                 fontweight="bold")
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

    # (1,1) Consecutive ratios mu_i / mu_{i+1} vs pi
    ax = axes[1, 1]
    ratios = mus_final[:-1] / mus_final[1:]
    bar_pos = np.arange(len(ratios))
    ax.bar(bar_pos, ratios, color=colors[:-1], alpha=0.8,
           label=r"$\mu_i / \mu_{i+1}$")
    ax.axhline(y=math.pi, color="red", linestyle="--", linewidth=1.8, alpha=0.8,
               label=fr"$\pi = {math.pi:.4f}$")
    ax.set_xticks(bar_pos)
    ax.set_xticklabels([f"{i} / {i+1}" for i in range(len(ratios))])
    ax.set_xlabel("cell index pair")
    ax.set_ylabel(r"$\mu_i / \mu_{i+1}$")
    ax.set_title(r"Consecutive cell ratio $\to \pi$ in the tail",
                 fontweight="bold")
    ax.legend(); ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"{OUT}/cascade_joint.png"
    plt.savefig(path, dpi=200); plt.close()

    # Numerical verification
    mu0_err = abs(mus_final[0] - FIELD_ORIGIN_MU)
    tail_ratios = ratios[-3:]
    tail_err = max(abs(r - math.pi) for r in tail_ratios)
    phase_err = np.max(np.abs(dphi_rel0[:, -1]))
    print(f"  [§C] saved {os.path.basename(path)}")
    print(f"       mu_0 final         = {mus_final[0]:.6f}  "
          f"(prediction 1/phi^2 = {FIELD_ORIGIN_MU:.6f})")
    print(f"       |Delta mu_0|        = {mu0_err:.2e}")
    print(f"       tail ratios 3..5   = {[f'{r:.4f}' for r in ratios[2:]]}  "
          f"(prediction pi = {math.pi:.4f})")
    print(f"       max |tail - pi|    = {tail_err:.4f}")
    print(f"       max |Delta phi|    = {phase_err:.2e}")
    passed = mu0_err < 1e-5 and tail_err < 0.1 and phase_err < 1e-3
    print(f"       cascade predictions survive joint picture: {passed}")


# ========================================================================
#   §D  AMPLITUDE INDEPENDENCE OF PHASE LOCK (CONTROL TEST)
# ========================================================================
#
# Confirm that amplitude dynamics is independent of K_pll by running the
# cascade with K_pll = 0 (phases drift freely) and K_pll = 0.5 (phases
# locked), and verifying that the amplitude trajectories are IDENTICAL
# to numerical precision.  This is the formal statement of the
# channel-separation claim in the circuit model.

def sim_cascade_amp_independence():
    n = 6
    x_drive = 1.0
    omega_0 = 1.0
    y0 = np.zeros(2 * n)
    y0[:n] = np.full(n, 0.1)
    y0[n:] = np.array([0.0, 0.9, -1.3, 2.2, -0.5, 1.8])

    t_span = (0.0, 60.0)
    t_eval = np.linspace(*t_span, 3000)

    sol_locked = solve_ivp(cascade_joint_rhs, t_span, y0, t_eval=t_eval,
                           method="RK45",
                           args=(n, x_drive, omega_0, 0.5, INV_PI, 1.0, 1.0),
                           max_step=0.03)
    sol_free = solve_ivp(cascade_joint_rhs, t_span, y0, t_eval=t_eval,
                         method="RK45",
                         args=(n, x_drive, omega_0, 0.0, INV_PI, 1.0, 1.0),
                         max_step=0.03)

    # Amplitude channel comparison
    amp_max_diff = np.max(np.abs(sol_locked.y[:n] - sol_free.y[:n]))

    # Phase channel demonstration
    phi_locked = np.unwrap(sol_locked.y[n:2*n], axis=1)
    phi_free = np.unwrap(sol_free.y[n:2*n], axis=1)
    dphi_locked = phi_locked - phi_locked[0:1, :]
    dphi_free = phi_free - phi_free[0:1, :]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    ax = axes[0]
    colors = plt.cm.viridis(np.linspace(0, 0.9, n))
    for i in range(n):
        ax.plot(sol_locked.t, sol_locked.y[i], color=colors[i], linewidth=1.5,
                alpha=0.95, label=(f"cell {i}" if i == 0 else None))
        ax.plot(sol_free.t, sol_free.y[i], color=colors[i], linewidth=1.5,
                linestyle=":", alpha=0.85)
    ax.set_xlabel("time")
    ax.set_ylabel(r"$\mu$")
    ax.set_title("Amplitudes: $K=0.5$ (solid) vs $K=0$ (dotted)  -- identical",
                 fontweight="bold")
    ax.grid(True, alpha=0.3); ax.legend()

    ax = axes[1]
    for i in range(1, n):
        ax.plot(sol_locked.t, dphi_locked[i], color=colors[i], linewidth=1.5,
                alpha=0.95)
        ax.plot(sol_free.t, dphi_free[i], color=colors[i], linewidth=1.5,
                linestyle=":", alpha=0.85)
    ax.set_xlabel("time")
    ax.set_ylabel(r"$\phi_i - \phi_0$ (rad)")
    ax.set_title(r"Phases: $K=0.5$ (solid, locked) vs $K=0$ (dotted, drift)",
                 fontweight="bold")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"{OUT}/cascade_channel_separation.png"
    plt.savefig(path, dpi=200); plt.close()

    print(f"  [§D] saved {os.path.basename(path)}")
    print(f"       max |mu(K=0.5) - mu(K=0)|  =  {amp_max_diff:.2e}")
    print(f"       (channel separation: amplitude ODE independent of K_pll)")
    print(f"       phase under K=0.5:  locks to 0 to within "
          f"{np.max(np.abs(dphi_locked[:, -1])):.2e}")
    drift = np.max(np.abs(dphi_free[:, -1]))
    print(f"       phase under K=0:    free drift, max dev = {drift:.2f} rad")


# ========================================================================
#   MAIN
# ========================================================================

def run_all():
    print("=" * 72)
    print("  n-NODE NETWORK WITH JOINT (mu, phi) DYNAMICS")
    print("=" * 72)
    print(f"  constants:  1/phi^2 = {FIELD_ORIGIN_MU:.12f}")
    print(f"              pi      = {math.pi:.12f}")

    print("\n[§A] Tetrahedron at unit drive, c_amp=0 -> golden-ratio fixed point:")
    sim_tetrahedral_golden()

    print("\n[§B] Tetrahedron with amp coupling on -> shifted fixed point:")
    sim_tetrahedral_coupled()

    print("\n[§C] Cascade with joint (mu, phi) dynamics -> 1/pi and phase lock:")
    sim_cascade_joint()

    print("\n[§D] Amplitude / phase channel separation (control test):")
    sim_cascade_amp_independence()

    print("\n" + "=" * 72)
    print("  ALL TETRAHEDRAL / CASCADE SIMULATIONS COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    run_all()
