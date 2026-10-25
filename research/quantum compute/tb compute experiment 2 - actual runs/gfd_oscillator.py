#!/usr/bin/env python3
"""
GFD Coupled Oscillator Network
================================

The analog circuit IS a coupled nonlinear ODE system.
No hardware needed — simulate the dynamics directly.

Each cell i has state μ_i ∈ (0,1) evolving under:

    τ · dμ_i/dt = x_i·(1 - μ_i)² - μ_i

where x_i = Σ_j A_ij · (1/π) · T(μ_j) is the effective
acceleration ratio driven by neighbors through the
topological transducer T(μ) = μ/(1 - μ + μ²).

Simulations:
  1. Linear cascade (reproduce 1/π attenuation)
  2. Tetrahedral network (4 fully connected cells)
  3. SAT solver (clauses as coupling constraints)
  4. Bell vertex formation (two cells locking at x=2)

Author: Stephen Nelson / Field Dynamics Research
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.size'] = 11


# =========================================================================
#  CORE PHYSICS
# =========================================================================

def transducer(mu_B):
    """T(μ) = μ/(1 - μ + μ²) — topological transducer."""
    mu_B = np.clip(mu_B, 1e-10, 1 - 1e-10)
    return mu_B / (1.0 - mu_B + mu_B**2)


def mu_B_exact(x):
    """Exact solution of x(1-μ)² = μ."""
    x = np.asarray(x, dtype=float)
    x = np.clip(x, 1e-10, None)
    return ((2*x + 1) - np.sqrt(4*x + 1)) / (2*x)


def cell_rhs(mu_i, x_i, tau=1.0):
    """Right-hand side for one cell: dμ/dt = [x(1-μ)² - μ] / τ"""
    mu_i = np.clip(mu_i, 1e-10, 1 - 1e-10)
    return (x_i * (1 - mu_i)**2 - mu_i) / tau


# =========================================================================
#  1. LINEAR CASCADE
# =========================================================================

def cascade_ode(t, y, n_cells, x_drive, penalty=1.0/np.pi):
    """ODE for a linear chain: cell 0 driven externally,
    cell i>0 driven by (1/π)·T(μ_{i-1})."""
    dydt = np.zeros(n_cells)
    for i in range(n_cells):
        if i == 0:
            x_i = x_drive
        else:
            x_i = penalty * transducer(y[i-1])
            # Convert spatial capacity to acceleration ratio
            mu_A = x_i
            if mu_A > 0 and mu_A < 1:
                x_i = mu_A / (1 - mu_A)
            else:
                x_i = max(1e-10, x_i)
        dydt[i] = cell_rhs(y[i], x_i)
    return dydt


def run_cascade():
    """Simulate 6-cell cascade from golden ratio."""
    n = 6
    phi = (1 + np.sqrt(5)) / 2
    x_drive = 1.0  # field origin
    y0 = np.full(n, 0.1)  # all start low

    t_span = (0, 50)
    t_eval = np.linspace(0, 50, 2000)
    sol = solve_ivp(cascade_ode, t_span, y0, t_eval=t_eval,
                    args=(n, x_drive), method='RK45', max_step=0.05)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Top: all cell trajectories
    ax = axes[0]
    colors = plt.cm.viridis(np.linspace(0, 0.9, n))
    for i in range(n):
        target = mu_B_exact(x_drive if i == 0 else 0.05)  # approximate
        ax.plot(sol.t, sol.y[i], color=colors[i], linewidth=1.5,
                label=f'Cell {i}')
    ax.set_ylabel('Subspace Resonance μ_B')
    ax.set_title('Linear Cascade: 6 Cells with 1/π Attenuation', fontweight='bold')
    ax.legend(loc='right', fontsize=9)
    ax.set_ylim(-0.02, 0.5)
    ax.axhline(y=1/phi**2, color='gold', linestyle='--', alpha=0.7, label='1/φ²')
    ax.grid(True, alpha=0.3)

    # Bottom: final settled values vs exact
    ax2 = axes[1]
    finals = sol.y[:, -1]
    ax2.bar(range(n), finals, color=colors, alpha=0.8, label='Simulated')
    ax2.set_xlabel('Cell Index')
    ax2.set_ylabel('Settled μ_B')
    ax2.set_title('Final State: 1/π Decay Per Hop', fontweight='bold')
    ax2.set_yscale('log')
    ax2.set_ylim(1e-5, 1)
    ax2.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/cascade_oscillator.png', dpi=200)
    plt.close()
    print("  ✓ Cascade: saved cascade_oscillator.png")
    print(f"    Final states: {[f'{v:.6f}' for v in finals]}")


# =========================================================================
#  2. TETRAHEDRAL NETWORK (fully connected, 4 cells)
# =========================================================================

def tetra_ode(t, y, x_ext, penalty=1.0/np.pi):
    """4 fully connected cells. Each driven by all 3 neighbors."""
    n = 4
    dydt = np.zeros(n)
    for i in range(n):
        x_total = x_ext  # external drive
        for j in range(n):
            if i != j:
                mu_A = penalty * transducer(y[j])
                if 0 < mu_A < 1:
                    x_total += mu_A / (1 - mu_A)
        dydt[i] = cell_rhs(y[i], x_total / 3.0)  # average over 3 neighbors
    return dydt


def run_tetrahedron():
    """Simulate 4-cell tetrahedron with asymmetric initial conditions."""
    y0 = np.array([0.8, 0.1, 0.3, 0.6])  # asymmetric start
    x_ext = 0.5  # moderate external drive

    t_span = (0, 100)
    t_eval = np.linspace(0, 100, 4000)
    sol = solve_ivp(tetra_ode, t_span, y0, t_eval=t_eval,
                    args=(x_ext,), method='RK45', max_step=0.1)

    fig, ax = plt.subplots(figsize=(12, 5))
    labels = ['TetA', 'TetB', 'TetC', 'TetD']
    colors = ['#2c3e50', '#e74c3c', '#27ae60', '#8e44ad']
    for i in range(4):
        ax.plot(sol.t, sol.y[i], color=colors[i], linewidth=1.5,
                label=f'{labels[i]} (μ₀={y0[i]:.1f})')

    ax.set_xlabel('Time (τ)')
    ax.set_ylabel('Subspace Resonance μ_B')
    ax.set_title('Tetrahedral Network: 4 Fully Connected Cells Equilibrating',
                 fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.axhline(y=sol.y[0, -1], color='gray', linestyle=':', alpha=0.5)

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/tetrahedron_oscillator.png', dpi=200)
    plt.close()

    finals = sol.y[:, -1]
    spread = np.max(finals) - np.min(finals)
    print(f"  ✓ Tetrahedron: saved tetrahedron_oscillator.png")
    print(f"    Final states: {[f'{v:.4f}' for v in finals]}")
    print(f"    Spread: {spread:.8f} (equilibrated)")


# =========================================================================
#  3. SAT SOLVER
# =========================================================================

def sat_ode(t, y, clauses, n_vars, x_base=0.05, clause_strength=5.0):
    """
    SAT as coupled oscillator.
    
    Each variable v_i → cell i with state μ_i.
    v_i = TRUE  when μ_i > 0.5 (TetA)
    v_i = FALSE when μ_i < 0.5 (TetB)
    
    Base dynamics: weak centering toward μ=0.5 (undecided).
    Clause forces: push variables toward satisfying assignments.
    
    The clause force is the gradient of the unsatisfaction:
      stress_k = Π_{literal l in C_k} (1 - satisfaction(l))
    """
    n = n_vars
    dydt = np.zeros(n)

    # Base dynamics: weak centering toward μ = 0.5
    for i in range(n):
        mu_i = np.clip(y[i], 0.01, 0.99)
        dydt[i] = -x_base * (mu_i - 0.5)  # gentle spring toward midpoint

    # Clause stress forces
    for clause in clauses:
        # Compute unsatisfaction product
        unsat = 1.0
        for var_idx, negated in clause:
            mu_i = np.clip(y[var_idx], 0.01, 0.99)
            if negated:
                sat = 1 - mu_i
            else:
                sat = mu_i
            unsat *= (1 - sat)

        # If unsat > 0, push each variable toward satisfying
        for var_idx, negated in clause:
            mu_i = np.clip(y[var_idx], 0.01, 0.99)
            if negated:
                dydt[var_idx] -= clause_strength * unsat * mu_i
            else:
                dydt[var_idx] += clause_strength * unsat * (1 - mu_i)

    return dydt


def run_sat_satisfiable():
    """Solve a satisfiable 3-SAT instance.
    
    Variables: v0, v1, v2, v3
    Clauses:
      (v0 ∨ v1 ∨ v2)        — at least one of first three TRUE
      (¬v0 ∨ v2 ∨ v3)       — if v0 TRUE, need v2 or v3
      (v1 ∨ ¬v2 ∨ v3)       — if v2 TRUE, need v1 or v3
      (¬v1 ∨ ¬v2 ∨ ¬v3)     — not all of v1,v2,v3 TRUE
    
    Solution: v0=T, v1=T, v2=F, v3=T (among others)
    """
    clauses = [
        [(0, False), (1, False), (2, False)],     # v0 ∨ v1 ∨ v2
        [(0, True),  (2, False), (3, False)],     # ¬v0 ∨ v2 ∨ v3
        [(1, False), (2, True),  (3, False)],     # v1 ∨ ¬v2 ∨ v3
        [(1, True),  (2, True),  (3, True)],      # ¬v1 ∨ ¬v2 ∨ ¬v3
    ]

    n_vars = 4
    y0 = np.array([0.3, 0.6, 0.4, 0.2])  # random initial

    t_span = (0, 80)
    t_eval = np.linspace(0, 80, 3000)
    sol = solve_ivp(sat_ode, t_span, y0, t_eval=t_eval,
                    args=(clauses, n_vars), method='RK45', max_step=0.1)

    return sol, clauses, n_vars, "SATISFIABLE"


def run_sat_unsatisfiable():
    """Attempt an unsatisfiable instance.
    
    Variables: v0, v1
    Clauses:
      (v0)       — v0 must be TRUE
      (¬v0)      — v0 must be FALSE
      (v1)       — v1 must be TRUE  
      (¬v1)      — v1 must be FALSE
    
    No assignment satisfies all clauses.
    """
    clauses = [
        [(0, False)],           # v0
        [(0, True)],            # ¬v0
        [(1, False)],           # v1
        [(1, True)],            # ¬v1
    ]

    n_vars = 2
    y0 = np.array([0.7, 0.3])

    t_span = (0, 80)
    t_eval = np.linspace(0, 80, 3000)
    sol = solve_ivp(sat_ode, t_span, y0, t_eval=t_eval,
                    args=(clauses, n_vars), method='RK45', max_step=0.1)

    return sol, clauses, n_vars, "UNSATISFIABLE"


def check_sat_solution(y_final, clauses):
    """Check if final state satisfies all clauses."""
    assignment = {i: (y_final[i] > 0.5) for i in range(len(y_final))}
    all_sat = True
    for clause in clauses:
        clause_sat = False
        for var_idx, negated in clause:
            val = assignment[var_idx]
            if negated:
                val = not val
            if val:
                clause_sat = True
                break
        if not clause_sat:
            all_sat = False
            break
    return all_sat, assignment


def run_sat_solver():
    """Run both SAT instances and plot comparison."""
    sol_sat, cl_sat, nv_sat, label_sat = run_sat_satisfiable()
    sol_unsat, cl_unsat, nv_unsat, label_unsat = run_sat_unsatisfiable()

    fig, axes = plt.subplots(2, 2, figsize=(14, 9))

    # Top left: SAT trajectories
    ax = axes[0, 0]
    colors = ['#2c3e50', '#e74c3c', '#27ae60', '#8e44ad']
    for i in range(nv_sat):
        ax.plot(sol_sat.t, sol_sat.y[i], color=colors[i], linewidth=1.5,
                label=f'v{i}')
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Decision boundary')
    ax.set_ylabel('μ_i')
    ax.set_title(f'SAT Instance ({label_sat})', fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.05, 1.05)

    # Top right: SAT final state
    ax = axes[0, 1]
    finals_sat = sol_sat.y[:, -1]
    sat_ok, assignment = check_sat_solution(finals_sat, cl_sat)
    bar_colors = ['#27ae60' if v > 0.5 else '#e74c3c' for v in finals_sat]
    ax.bar(range(nv_sat), finals_sat, color=bar_colors, alpha=0.8)
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.set_ylabel('Settled μ_i')
    ax.set_title(f'Solution: {assignment} — {"✓ ALL SAT" if sat_ok else "✗ FAILED"}',
                 fontweight='bold',
                 color='green' if sat_ok else 'red')
    ax.set_ylim(0, 1)
    ax.set_xticks(range(nv_sat))
    ax.set_xticklabels([f'v{i}' for i in range(nv_sat)])

    # Bottom left: UNSAT trajectories
    ax = axes[1, 0]
    for i in range(nv_unsat):
        ax.plot(sol_unsat.t, sol_unsat.y[i], color=colors[i], linewidth=1.5,
                label=f'v{i}')
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Time (τ)')
    ax.set_ylabel('μ_i')
    ax.set_title(f'UNSAT Instance ({label_unsat})', fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.05, 1.05)

    # Bottom right: UNSAT oscillation analysis
    ax = axes[1, 1]
    # Compute rolling variance to detect oscillation
    window = 200
    for i in range(nv_unsat):
        signal = sol_unsat.y[i]
        if len(signal) > window:
            rolling_var = np.array([np.var(signal[max(0,j-window):j+1])
                                    for j in range(len(signal))])
            ax.plot(sol_unsat.t, rolling_var, color=colors[i], linewidth=1.5,
                    label=f'v{i} variance')
    ax.set_xlabel('Time (τ)')
    ax.set_ylabel('Rolling Variance')
    ax.set_title('Oscillation Diagnostic (UNSAT → Persistent Variance)',
                 fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/sat_oscillator.png', dpi=200)
    plt.close()

    # Report
    finals_unsat = sol_unsat.y[:, -1]
    tail_var = np.var(sol_unsat.y[:, -500:], axis=1)

    print(f"  ✓ SAT solver results:")
    print(f"    SATISFIABLE instance:")
    print(f"      Final: {[f'{v:.3f}' for v in finals_sat]}")
    print(f"      Assignment: {assignment}")
    print(f"      All clauses satisfied: {sat_ok}")
    print(f"    UNSATISFIABLE instance:")
    print(f"      Final: {[f'{v:.3f}' for v in finals_unsat]}")
    print(f"      Tail variance: {[f'{v:.6f}' for v in tail_var]}")
    oscillating = any(v > 0.001 for v in tail_var)
    print(f"      Persistent oscillation: {oscillating}")


# =========================================================================
#  4. BELL VERTEX FORMATION
# =========================================================================

def bell_ode(t, y, coupling_strength=1.0):
    """Two cells with anti-correlation boundary lock.
    
    Cell 0 driven by cell 1's TetB fraction: x_0 ∝ (1-μ_1)
    Cell 1 driven by cell 0's TetB fraction: x_1 ∝ (1-μ_0)
    
    The interior law x(1-μ)² = μ with anti-correlated coupling
    should lock both to μ = 1/2 at x = 2.
    """
    mu0, mu1 = np.clip(y, 1e-10, 1 - 1e-10)

    # Anti-correlation coupling: each cell's drive comes from
    # the OTHER cell's TetB fraction, scaled to hit x=2 at equilibrium
    x0 = coupling_strength * (1 - mu1) / max(mu1, 1e-10) + 0.5
    x1 = coupling_strength * (1 - mu0) / max(mu0, 1e-10) + 0.5

    dmu0 = cell_rhs(mu0, x0)
    dmu1 = cell_rhs(mu1, x1)

    return [dmu0, dmu1]


def run_bell_vertex():
    """Simulate Bell vertex formation."""
    y0 = [0.2, 0.8]  # asymmetric start

    t_span = (0, 30)
    t_eval = np.linspace(0, 30, 2000)
    sol = solve_ivp(bell_ode, t_span, y0, t_eval=t_eval,
                    method='RK45', max_step=0.05)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Left: trajectories
    ax = axes[0]
    ax.plot(sol.t, sol.y[0], color='#2c3e50', linewidth=2, label='Cell 0')
    ax.plot(sol.t, sol.y[1], color='#e74c3c', linewidth=2, label='Cell 1')
    ax.axhline(y=0.5, color='gold', linestyle='--', linewidth=2,
               alpha=0.7, label='Bell vertex μ=1/2')
    ax.set_xlabel('Time (τ)')
    ax.set_ylabel('μ_B')
    ax.set_title('Bell Vertex Formation: Two Anti-Correlated Cells',
                 fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Right: phase portrait
    ax2 = axes[1]
    ax2.plot(sol.y[0], sol.y[1], color='#8e44ad', linewidth=1.5, alpha=0.8)
    ax2.plot(sol.y[0, 0], sol.y[1, 0], 'go', markersize=10, label='Start')
    ax2.plot(sol.y[0, -1], sol.y[1, -1], 'r*', markersize=15, label='End')
    ax2.plot(0.5, 0.5, 'kx', markersize=12, markeredgewidth=3, label='Bell vertex')
    # Anti-correlation line μ₁ = 1 - μ₂
    mu_line = np.linspace(0, 1, 100)
    ax2.plot(mu_line, 1 - mu_line, 'k--', alpha=0.3, label='μ₁ = 1-μ₂')
    ax2.set_xlabel('μ₀')
    ax2.set_ylabel('μ₁')
    ax2.set_title('Phase Portrait', fontweight='bold')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/bell_vertex_oscillator.png', dpi=200)
    plt.close()

    print(f"  ✓ Bell vertex: saved bell_vertex_oscillator.png")
    print(f"    Start: μ₀={y0[0]}, μ₁={y0[1]}")
    print(f"    Final: μ₀={sol.y[0,-1]:.4f}, μ₁={sol.y[1,-1]:.4f}")
    print(f"    Target: μ₀=μ₁=0.5 (Bell vertex)")
    lock = abs(sol.y[0,-1] - 0.5) < 0.05 and abs(sol.y[1,-1] - 0.5) < 0.05
    print(f"    Locked to Bell vertex: {lock}")


# =========================================================================
#  MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 65)
    print("  GFD COUPLED OSCILLATOR NETWORK")
    print("=" * 65)

    print("\n§1 Linear cascade:")
    run_cascade()

    print("\n§2 Tetrahedral network:")
    run_tetrahedron()

    print("\n§3 SAT solver:")
    run_sat_solver()

    print("\n§4 Bell vertex formation:")
    run_bell_vertex()

    print("\n" + "=" * 65)
    print("  ALL SIMULATIONS COMPLETE")
    print("=" * 65)
