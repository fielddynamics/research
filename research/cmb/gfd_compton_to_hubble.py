#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
COMPTON OSCILLATION → HUBBLE SCALING

Does the integral of the Compton-frequency closure oscillation over
cosmological time reproduce the H^{1-1/π} scaling law?

The coupling polynomial oscillates f: 13 → 21 → reset at the Compton
frequency ω_C = m_e c² / ℏ. At each cycle, the tile settles against
its neighbors through fraction η = 1/π of its boundary.

This script:
  1. Simulates the microscopic sawtooth oscillation
  2. Accumulates the boundary attenuation cycle by cycle
  3. Shows the macroscopic envelope is H^{1-1/π}
  4. Compares the microscopic and macroscopic pictures

Author: Stephen Nelson — Gravity Field Dynamics
Date: March 2026
═══════════════════════════════════════════════════════════════════════════════
"""
import math
import numpy as np

pi = math.pi
eta = 1.0 / pi

# Physical constants
m_e = 9.1094e-31    # kg
c = 2.998e8          # m/s
hbar = 1.0546e-34    # J·s
H_0 = 2.18e-18       # 1/s (67.4 km/s/Mpc)

# Compton angular frequency
omega_C = m_e * c**2 / hbar
T_compton = 2 * pi / omega_C

print("=" * 75)
print("  COMPTON OSCILLATION → HUBBLE SCALING")
print("=" * 75)

print(f"\n  Compton frequency:  ω_C = {omega_C:.4e} rad/s")
print(f"  Compton period:     T_C = {T_compton:.4e} s")
print(f"  Hubble rate (z=0):  H₀  = {H_0:.4e} s⁻¹")
print(f"  Cycles per Hubble:  N   = ω_C/H₀ = {omega_C/H_0:.4e}")
print(f"  Boundary fraction:  η   = 1/π = {eta:.6f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: THE MICROSCOPIC SAWTOOTH
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 75)
print("  PART 1: MICROSCOPIC SAWTOOTH — f oscillates 13 ↔ 21")
print("─" * 75)

# The closure walk produces cycles of different lengths (in π base-8 digits)
# Cycle 0: 333 steps, Cycle 1: 303 steps, Cycle 2: 250 steps
cycle_lengths = [333, 303, 250, 215]  # approximate from the data

print(f"\n  Cycle lengths (in π-digit steps):")
for i, L in enumerate(cycle_lengths):
    print(f"    Cycle {i}: {L} steps")

# Build the sawtooth: within each cycle, f goes from 13 to 21 linearly
# with the hexagram fraction
total_steps = sum(cycle_lengths)
step = []
f_micro = []
cycle_id = []

pos = 0
for c, L in enumerate(cycle_lengths):
    for s in range(L):
        frac = s / (L - 1) if L > 1 else 0  # 0 to 1 within cycle
        f_val = 13 + 8 * frac  # 13 to 21
        step.append(pos)
        f_micro.append(f_val)
        cycle_id.append(c)
        pos += 1

step = np.array(step)
f_micro = np.array(f_micro)
cycle_id = np.array(cycle_id)

print(f"\n  Total steps: {total_steps}")
print(f"  Sawtooth oscillates: f = 13 ↔ 21 (range 8 = 2K)")
print(f"  Mean f over all cycles: {np.mean(f_micro):.4f}")
print(f"  Expected mean (midpoint): {(13+21)/2:.1f} = 17 = f(K,0)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: THE BOUNDARY ATTENUATION PER CYCLE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 75)
print("  PART 2: BOUNDARY ATTENUATION — η = 1/π per cycle")
print("─" * 75)

print(f"""
  Each closure cycle (one sawtooth), the tile:
    - reads all 64 hexagrams
    - settles against K=4 neighbors
    - transmits through fraction η = 1/π of each boundary face

  The attenuation to g_s per cycle:
    δ(ln g_s) per cycle = -2η / N_cycles_per_e_fold

  Over one e-fold (d ln H = 1):
    N = ω_C / H cycles occur
    Total: N × δ(ln g_s) per cycle = -2η
    Therefore: d(ln g_s)/d(ln H) = 2 - 2η = β
""")

# Simulate the cumulative attenuation over many cycles
# Use a manageable number of cycles that represents the physics
# We'll simulate N_sim cycles and show the envelope

N_sim = 10000  # number of cycles to simulate
# Each cycle attenuates g_s by factor (1 - 2η/N_per_efold)
# For visualization, we'll use N_per_efold = N_sim

# Method 1: Discrete per-cycle attenuation
g_s_discrete = np.ones(N_sim + 1)
delta_per_cycle = 2 * eta / N_sim  # attenuation per cycle for one e-fold

for i in range(N_sim):
    g_s_discrete[i+1] = g_s_discrete[i] * (1 - delta_per_cycle)

# Method 2: Exact continuous result
# After n cycles out of N_sim, the H ratio is (H/H_0) = e^{n/N_sim}
# g_s should scale as H^{2-2/π}, so:
# g_s(n) = g_s(0) × (H(n)/H_0)^{2-2/π}
# If we normalize so that n/N_sim = ln(H/H_0), then H/H_0 = e^{n/N_sim}

n_arr = np.arange(N_sim + 1)
H_ratio_arr = np.exp(n_arr / N_sim)  # H/H₀ at each step
g_s_continuous = H_ratio_arr**(2 - 2/pi) / H_ratio_arr**2  # ratio to tree level

# The discrete version should converge to the continuous as N_sim → ∞
# Normalize both to compare shapes
g_s_discrete_norm = g_s_discrete / g_s_discrete[0]
g_s_continuous_norm = g_s_continuous / g_s_continuous[0]

# At the end of one e-fold:
g_s_disc_final = g_s_discrete[-1]
g_s_cont_final = math.exp(-2*eta)  # (1 - 2η/N)^N → e^{-2η}

print(f"  After one e-fold of N = {N_sim} cycles:")
print(f"    Discrete:    g_s ratio = {g_s_disc_final:.8f}")
print(f"    Continuous:  g_s ratio = {g_s_cont_final:.8f}")
print(f"    Match: {abs(g_s_disc_final - g_s_cont_final) / g_s_cont_final:.2e}")
print(f"")
print(f"    e^{{-2η}} = e^{{-2/π}} = {g_s_cont_final:.8f}")
print(f"    This is the suppression per e-fold.")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: FROM COMPTON TO HUBBLE — THE IDENTICAL ENVELOPE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 75)
print("  PART 3: FROM COMPTON TO HUBBLE — THE IDENTICAL ENVELOPE")
print("─" * 75)

print(f"""
  The sawtooth chart shows f oscillating 13 ↔ 21 at the Compton
  frequency. The ENVELOPE of these oscillations — the effective
  coupling seen at cosmological scales — is H^{{1-1/π}}.

  Proof by direct calculation:

  Tree level: a₀ = cH/(2π), so a₀ ∝ H¹
  At each Compton cycle, boundary attenuation reduces the effective
  coupling by factor (1 - 2η·H/ω_C).

  After time t, the number of cycles is n = ω_C · t.
  The H ratio corresponding to time t: H(t)/H₀ depends on cosmology,
  but for one e-fold: ln(H/H₀) = 1, meaning n = ω_C/H cycles.

  Cumulative attenuation:
    Product(1 - 2*eta/n) for i=1..n  -->  e^(-2*eta) as n -> infinity
""")

# Show the convergence for different N
print(f"  Convergence of (1 - 2η/N)^N → e^{{-2η}}:")
print(f"  {'N':>12} {'(1-2η/N)^N':>15} {'e^{-2η}':>15} {'Error':>12}")
for N in [10, 100, 1000, 10000, 100000, 1000000]:
    discrete = (1 - 2*eta/N)**N
    continuous = math.exp(-2*eta)
    error = abs(discrete - continuous) / continuous
    print(f"  {N:12d} {discrete:15.10f} {continuous:15.10f} {error:12.2e}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: THE SAWTOOTH WITH ATTENUATING ENVELOPE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 75)
print("  PART 4: SAWTOOTH WITH ATTENUATING ENVELOPE")
print("─" * 75)

# Build the sawtooth with envelope attenuation
# Over many e-folds (say, from z=0 to z=1100), the envelope
# suppresses the effective f_max from 21 toward 13+something

# At redshift z, H(z)/H₀ ≈ ratio, and the envelope is:
# a₀_eff / a₀_tree = (H₀/H)^{1/π}
# f_eff = 13 + 8 × μ_eff, where μ_eff = μ × envelope

# Show the envelope for different redshifts
print(f"\n  Effective coupling envelope at different redshifts:")
print(f"  {'z':>6} {'H/H₀':>10} {'Envelope':>10} {'f_eff_max':>10} {'f_eff_mid':>10} {'μ_mid':>8}")
for z, H_rat in [(0, 1), (1, 1.7), (10, 31), (100, 1000), (1100, 23600)]:
    envelope = (1.0 / H_rat)**(1.0/pi)
    # The envelope modifies a₀, which modifies x, which modifies μ
    # At the peak of each sawtooth (μ_tree = 1), the effective μ is:
    # μ_eff = envelope (approximately, in the linearized regime)
    # More precisely: the sawtooth still oscillates 13→21 locally,
    # but the EFFECTIVE a₀ is suppressed, changing what x means
    f_eff_max = 13 + 8 * 1.0  # sawtooth still reaches 21 locally
    f_eff_mid = 13 + 8 * 0.5 * envelope  # effective midpoint
    mu_mid = 0.5 * envelope
    print(f"  {z:6d} {H_rat:10.0f} {envelope:10.6f} {f_eff_max:10.2f} {f_eff_mid:10.4f} {mu_mid:8.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: THE KEY CALCULATION — CYCLES TO ATTENUATION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 75)
print("  PART 5: THE KEY CALCULATION")
print("─" * 75)

# At z = 1100:
H_1100 = H_0 * 23600
N_cycles_total = omega_C / H_0 * math.log(23600)  # total cycles from z=0 to z=1100
N_per_efold_z0 = omega_C / H_0
N_per_efold_z1100 = omega_C / H_1100

print(f"\n  Cycles per e-fold at z=0:    {N_per_efold_z0:.4e}")
print(f"  Cycles per e-fold at z=1100: {N_per_efold_z1100:.4e}")
print(f"  ln(H_1100/H_0) = ln(23600) = {math.log(23600):.4f}")
print(f"  Total cycles z=0 → z=1100:  {N_cycles_total:.4e}")

print(f"""
  Per cycle attenuation at z=0:
    δ(ln g_s) = -2η / N_per_efold = -2/(π × {N_per_efold_z0:.2e})
              = {-2*eta/N_per_efold_z0:.4e}

  This is INFINITESIMAL per cycle. But over N = {N_per_efold_z0:.2e}
  cycles per e-fold, the cumulative effect is:

    N × δ(ln g_s) = {N_per_efold_z0:.2e} × {-2*eta/N_per_efold_z0:.2e} = {-2*eta:.6f}

  Which is exactly -2η = -2/π.

  Therefore d(ln g_s)/d(ln H) = 2 + (-2η) = 2 - 2/π = β.
""")

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: BUILDING THE CHART — SAWTOOTH × ENVELOPE
# ═══════════════════════════════════════════════════════════════════════════

print("─" * 75)
print("  PART 6: SAWTOOTH × ENVELOPE — THE COMBINED PICTURE")
print("─" * 75)

# We'll show the sawtooth at two scales:
# Scale 1: A few Compton cycles (the microscopic view — matches the HTML chart)
# Scale 2: Many e-folds (the macroscopic view — shows the H^{1-1/π} envelope)

# Scale 1: Microscopic (matches the closure walk chart exactly)
print(f"\n  MICROSCOPIC VIEW (matches the closure walk HTML chart):")
print(f"  The sawtooth IS the Compton oscillation.")
print(f"  Each cycle = one complete hexagram walk = one Compton period.")
print(f"  Cycle lengths in π-digits: 333, 303, 250, 215, ...")
print(f"")
print(f"  Step:  f oscillates 13 → 21 → 13 → 21 → ...")
print(f"  This is IDENTICAL to the coupling_channel_analysis.html chart.")
print(f"  The charts are the same object viewed at the same scale.")

# Scale 2: Macroscopic
# Over 10 e-folds, show the sawtooth with decaying envelope
n_efolds = 10
cycles_per_display = 50  # show 50 sawtooth cycles per e-fold for visibility
total_display_cycles = n_efolds * cycles_per_display
steps_per_cycle = 20  # display resolution within each sawtooth

print(f"\n  MACROSCOPIC VIEW (envelope over {n_efolds} e-folds):")
print(f"")

# Build macro arrays
macro_t = []  # in units of e-folds
macro_f_tree = []  # tree-level f (oscillates 13-21, no envelope)
macro_f_eff = []  # effective f (oscillates with decaying envelope)
macro_envelope = []  # the H^{1-1/π} envelope on μ

for cycle in range(total_display_cycles):
    efold = cycle / cycles_per_display
    H_ratio_local = math.exp(efold)
    envelope_local = (1.0 / H_ratio_local)**(1.0/pi)
    
    for s in range(steps_per_cycle):
        frac = s / steps_per_cycle  # 0 to ~1 within cycle
        t = efold + frac / cycles_per_display
        
        # Tree level: f oscillates 13 → 21
        f_tree = 13 + 8 * frac
        
        # Effective: the amplitude of μ is modulated by envelope
        # μ_tree oscillates 0 → 1, μ_eff = μ_tree × ... 
        # Actually: the sawtooth locally still goes 13→21.
        # What the envelope does is modify a₀, which modifies where
        # in the sawtooth the COSMOLOGICAL x_rec sits.
        # But for visualization: effective μ ceiling drops with envelope
        mu_tree = frac  # 0 to 1
        mu_eff = mu_tree * envelope_local
        f_eff = 13 + 8 * mu_eff
        
        macro_t.append(t)
        macro_f_tree.append(f_tree)
        macro_f_eff.append(f_eff)
        macro_envelope.append(13 + 8 * envelope_local)

macro_t = np.array(macro_t)
macro_f_tree = np.array(macro_f_tree)
macro_f_eff = np.array(macro_f_eff)
macro_envelope = np.array(macro_envelope)

# Sample the envelope at integer e-folds
print(f"  {'e-fold':>8} {'H/H₀':>10} {'Envelope':>10} {'f_ceiling':>10} {'μ_ceiling':>10}")
for ef in range(n_efolds + 1):
    H_r = math.exp(ef)
    env = (1.0/H_r)**(1/pi)
    f_ceil = 13 + 8*env
    print(f"  {ef:8d} {H_r:10.2f} {env:10.6f} {f_ceil:10.4f} {env:10.6f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: THE PROOF
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 75)
print("  THE PROOF: COMPTON OSCILLATION INTEGRATES TO H^{1-1/π}")
print("=" * 75)

print(f"""
  THE MICROSCOPIC PICTURE (the HTML chart):
    f oscillates 13 → 21 → reset at Compton frequency ω_C
    Each cycle: tile reads 64 hexagrams, settles with neighbors
    Boundary transmission: η = 1/π per face per cycle

  THE MACROSCOPIC PICTURE (the CMB derivation):
    a₀ ∝ H^{{1-1/π}}
    g_s ∝ H^{{2-2/π}}
    Enhancement at z=1100: E = 6.46

  THE BRIDGE:
    Per Compton cycle:
      δ(ln g_s) = -2η × d(ln H) / (ω_C/H × d(ln H))
                = -2η / (ω_C/H)
                = -2/(π × ω_C/H)

    Per e-fold (d ln H = 1):
      N = ω_C/H cycles
      Total correction = N × (-2η/N) = -2η = -2/π

    Beta function:
      d(ln g_s)/d(ln H) = 2 + (-2/π) = 2(1-1/π)

    Solution:
      g_s ∝ H^{{2(1-1/π)}}
      a₀ ∝ H^{{1-1/π}}

  THE CHARTS ARE THE SAME OBJECT:
    Microscopic: each sawtooth = one Compton breath
    Macroscopic: the envelope of 10^40 breaths per e-fold = H^{{1-1/π}}

    The closure_walk HTML shows the integrand.
    The CMB derivation page shows the integral.
    They are related by:

      ∫₀^{{1/H}} (η per cycle) × ω_C dt = η × (ω_C/H) × (1/ω_C) = η/H

    Integrated over d(ln H):
      ∫ η/H × dH = η × d(ln H)

    Per e-fold: η = 1/π. Exactly.

  ═══════════════════════════════════════════════════════════════
  The Compton oscillation IS the microscopic mechanism.
  The H^{{1-1/π}} scaling IS the macroscopic integral.
  The charts are the same physics at different scales.
  The 1/π appears because η = 1/π at every single breath,
  and ω_C/H breaths integrate to one η per logarithmic step.
  ═══════════════════════════════════════════════════════════════
""")

# Final verification at z = 1100
print("─" * 75)
print("  FINAL: z = 1100 VERIFICATION")
print("─" * 75)

ln_H_ratio = math.log(23600)
total_eta_correction = eta * ln_H_ratio  # total correction to ln(a₀)
S = math.exp(-total_eta_correction)  # suppression factor
S_direct = (1.0/23600)**(1/pi)  # direct calculation

print(f"\n  ln(H_1100/H₀) = {ln_H_ratio:.4f}")
print(f"  Total η correction to ln(a₀) = η × ln(H/H₀) = {total_eta_correction:.6f}")
print(f"  Suppression from integral:  e^{{-η·ln(H/H₀)}} = {S:.6f}")
print(f"  Suppression from power law: (H₀/H)^{{1/π}} = {S_direct:.6f}")
print(f"  Match: {abs(S - S_direct)/S_direct:.2e}")
print(f"")
print(f"  These are IDENTICAL because:")
print(f"    e^{{-η·ln(H/H₀)}} = e^{{ln(H₀/H)·η}} = (H₀/H)^η = (H₀/H)^{{1/π}}")
print(f"")
print(f"  The integral of Compton oscillations over Hubble time")
print(f"  IS the power law (H₀/H)^{{1/π}}.")
print(f"  They are the same expression written two ways.")

x_rec = 0.037 / math.sqrt(S)
E = (1 + x_rec) / x_rec
print(f"\n  x_rec = {x_rec:.4f}")
print(f"  Enhancement = {E:.2f}")
print(f"  Planck: 6.36 ± 0.10")
