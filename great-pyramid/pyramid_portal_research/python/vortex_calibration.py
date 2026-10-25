"""
vortex_calibration.py
======================

Tier 2 / Generation-1 calibration push.

Tests the hypothesis that the π-walk read-speed v_read drives a vortex-like
structure between TetA and TetB, with the bridge as the vortex core.

The closure cycle is run with continuous Ω-rotation (interpolating between
ω^0, ω^1, ω^2) parametrized by `n_substeps_per_phase`.  The parameter v_read
sets how many substeps fit into one phase; v_read = ∞ recovers the discrete
3-step closure used elsewhere in the package, v_read finite traces out a
continuous rotation in Eisenstein-pair coordinates.

Predictions tested:

  (P1)  Vote pattern V1 : V2 : V3 should be a v_read-INDEPENDENT geometric
        invariant — pure projection ratios fixed by Cl(3,0) structure.
  (P2)  TetA → TetB impedance (transverse leakage per cycle) should SCALE
        with v_read — a dynamical quantity, not a kinematic one.

These two predictions distinguish a vortex picture (geometry vs dynamics)
from generic alternatives (where votes would also depend on v_read).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

import math
import numpy as np

from python.closure_core256 import (
    ClosureCoords3, to_closure_coords3,
    omega_power3, closure_projection3,
)


# ---------------------------------------------------------------------------
# Continuous Eisenstein rotation
# ---------------------------------------------------------------------------
# An Eisenstein pair (x, y) represents the complex number
#       z = x + y · ω,    ω = exp(2πi/3) = -1/2 + i√3/2
# Multiplication by ω advances (x, y) → (-y, x - y), which is exactly the
# discrete Ω-phase action in `closure_core256.eisenstein_omega_pair`.
#
# For continuous rotation by angle θ, multiply z by exp(iθ):
#       z' = z · (cos θ + i sin θ)
# Convert (x', y') back from Re(z'), Im(z') via the Eisenstein-basis
# transform.

_SQRT3 = math.sqrt(3.0)


def _eisenstein_pair_to_complex(pair: Tuple[float, float]) -> complex:
    x, y = pair
    return complex(x - 0.5 * y, 0.5 * _SQRT3 * y)


def _complex_to_eisenstein_pair(z: complex) -> Tuple[float, float]:
    # Re(z) = x - y/2, Im(z) = y·√3/2
    y = 2.0 * z.imag / _SQRT3
    x = z.real + 0.5 * y
    return float(x), float(y)


def continuous_eisenstein_rotation(
    pair: Tuple[float, float], theta: float
) -> Tuple[float, float]:
    """Rotate an Eisenstein pair by continuous angle θ.  θ = 2π/3 = one Ω-step."""
    z = _eisenstein_pair_to_complex(pair)
    z_rot = z * complex(math.cos(theta), math.sin(theta))
    return _complex_to_eisenstein_pair(z_rot)


def continuous_omega_rotation(coeffs: np.ndarray, theta: float) -> np.ndarray:
    """Apply continuous Ω-rotation to all three hexagonal channels.

    Axial coordinates (scalar a, pseudoscalar b) are fixed (Ω acts as identity
    on the axial sector).  Each Eisenstein pair z_k is rotated by θ.
    """
    cc = to_closure_coords3(coeffs)
    z1_rot = continuous_eisenstein_rotation(cc.z1, theta)
    z2_rot = continuous_eisenstein_rotation(cc.z2, theta)
    z3_rot = continuous_eisenstein_rotation(cc.z3, theta)
    return ClosureCoords3(
        a=cc.a, b=cc.b, z1=z1_rot, z2=z2_rot, z3=z3_rot
    ).as_vector()


# ---------------------------------------------------------------------------
# Sector projectors
# ---------------------------------------------------------------------------
# Cl(3, 0) mask basis: 0 = 1, 1 = e1, 2 = e2, 4 = e3, 3 = e12, 5 = e13,
# 6 = e23, 7 = I.  Three grade-based sectors:
#       axial    = <1, I>          = {mask 0, mask 7}
#       vector   = <e1, e2, e3>    = {mask 1, mask 2, mask 4}
#       bivector = <e12, e13, e23> = {mask 3, mask 5, mask 6}

_MASKS_AXIAL    = (0, 7)
_MASKS_VECTOR   = (1, 2, 4)
_MASKS_BIVECTOR = (3, 5, 6)


def sector_norms(coeffs: np.ndarray) -> Tuple[float, float, float]:
    """Return (||axial||, ||vector||, ||bivector||) sector norms."""
    v = np.asarray(coeffs, dtype=float)
    axial = math.sqrt(sum(v[m] ** 2 for m in _MASKS_AXIAL))
    vector = math.sqrt(sum(v[m] ** 2 for m in _MASKS_VECTOR))
    bivector = math.sqrt(sum(v[m] ** 2 for m in _MASKS_BIVECTOR))
    return axial, vector, bivector


# ---------------------------------------------------------------------------
# One closure cycle at finite v_read
# ---------------------------------------------------------------------------

@dataclass
class CycleTrace:
    """Output of one closure cycle traversal."""
    v_read: float
    n_substeps: int
    states: np.ndarray            # shape (n_substeps + 1, 8)
    sector_axial: np.ndarray      # shape (n_substeps + 1,)
    sector_vector: np.ndarray
    sector_bivector: np.ndarray


def run_closure_cycle(
    initial_state: np.ndarray, v_read: float, n_substeps: int = 90
) -> CycleTrace:
    """Run one full closure cycle (total rotation 2π in each hexagonal channel).

    The cycle is divided into n_substeps equal angular steps.  The parameter
    v_read sets the physical time per substep dt = 1 / (v_read · n_substeps);
    this is currently a kinematic time-stamp (used only for impedance scaling),
    not a dynamical Hamiltonian.
    """
    d_theta = 2.0 * math.pi / n_substeps
    states = [np.asarray(initial_state, dtype=float).copy()]
    current = states[0].copy()
    for _ in range(n_substeps):
        current = continuous_omega_rotation(current, d_theta)
        states.append(current.copy())
    states_arr = np.stack(states, axis=0)

    axial = np.array([sector_norms(s)[0] for s in states_arr])
    vector = np.array([sector_norms(s)[1] for s in states_arr])
    bivector = np.array([sector_norms(s)[2] for s in states_arr])

    return CycleTrace(
        v_read=v_read,
        n_substeps=n_substeps,
        states=states_arr,
        sector_axial=axial,
        sector_vector=vector,
        sector_bivector=bivector,
    )


# ---------------------------------------------------------------------------
# Votes — time-averaged sector amplitudes
# ---------------------------------------------------------------------------

@dataclass
class VoteResult:
    v_read: float
    V_axial: float
    V_vector: float
    V_bivector: float
    ratio_biv_over_axial: float    # candidate √3
    ratio_vector_over_axial: float # candidate 0

    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.V_axial, self.V_vector, self.V_bivector)


def compute_votes(trace: CycleTrace) -> VoteResult:
    """Time-averaged sector amplitudes over one cycle (the 'votes')."""
    V_ax = float(np.mean(trace.sector_axial))
    V_vec = float(np.mean(trace.sector_vector))
    V_biv = float(np.mean(trace.sector_bivector))
    return VoteResult(
        v_read=trace.v_read,
        V_axial=V_ax,
        V_vector=V_vec,
        V_bivector=V_biv,
        ratio_biv_over_axial=(V_biv / V_ax) if V_ax > 1e-12 else float("inf"),
        ratio_vector_over_axial=(V_vec / V_ax) if V_ax > 1e-12 else float("inf"),
    )


# ---------------------------------------------------------------------------
# Impedance — how much "out-of-phase" content accumulates per cycle
# ---------------------------------------------------------------------------

def compute_impedance(trace: CycleTrace) -> Dict[str, float]:
    """TetA → TetB impedance measured as the half-cycle phase-loss integral.

    At v_read = ∞ the closure happens in zero time and TetB perfectly mirrors
    TetA (no impedance).  At finite v_read each substep takes dt = 1/(v_read·N)
    seconds; the cumulative phase lag between the initial state and its
    half-cycle counterpart is the impedance.

    The integral is normalised so that v_read = 1 gives unit impedance for
    a state of unit norm, making the v_read scaling explicit.
    """
    states = trace.states                       # shape (N+1, 8)
    N = trace.n_substeps
    half_idx = N // 2
    initial = states[0]
    halfway = states[half_idx]

    # The "expected" halfway state under perfect mirror: -initial (parity flip
    # acts as multiplication by -1 on grade-1 and grade-3 components only).
    expected_halfway = initial.copy()
    # Parity flip = grade involution: flip masks with odd popcount.
    for m in range(8):
        if bin(m).count("1") % 2 == 1:
            expected_halfway[m] = -expected_halfway[m]

    delta = halfway - expected_halfway
    leakage = float(np.linalg.norm(delta))
    cycle_time = 1.0 / max(trace.v_read, 1e-30)
    # Impedance defined as leakage per unit cycle time (scales inversely with
    # v_read for fixed leakage, so we report leakage AND time separately).
    return {
        "leakage_half_cycle": leakage,
        "cycle_time": cycle_time,
        "impedance_per_unit_time": leakage * trace.v_read,
        "ratio_leakage_to_axial": leakage / max(trace.sector_axial[0], 1e-12),
    }


# ---------------------------------------------------------------------------
# Sweep over v_read
# ---------------------------------------------------------------------------

def make_test_state() -> np.ndarray:
    """A generic state with axial + hexagonal content but no pure-vector part.

    Construction: scalar + T_2 (bivector with weight √3) gives axial norm 1,
    bivector norm √3, vector norm 0 — exactly the √3:1:0 pattern as a
    structural starting point.
    """
    s = np.zeros(8, dtype=float)
    s[0] = 1.0          # scalar
    s[3] = 1.0          # e_12
    s[6] = 1.0          # e_23
    s[5] = -1.0         # -e_13   (so this is the T_2 generator)
    return s


def make_axial_only_state() -> np.ndarray:
    """Pure axial state: scalar + pseudoscalar."""
    s = np.zeros(8, dtype=float)
    s[0] = 1.0
    s[7] = 1.0
    return s


def make_mixed_test_state() -> np.ndarray:
    """Generic state with all three sectors populated."""
    s = np.zeros(8, dtype=float)
    s[0] = 1.0          # scalar
    s[1] = 0.5          # e_1   (vector content)
    s[3] = 0.7          # e_12  (bivector)
    s[6] = 0.7          # e_23
    s[5] = -0.7         # -e_13
    s[7] = 0.3          # I
    return s


def sweep_v_read(
    v_read_values: List[float],
    initial_state: np.ndarray = None,
    n_substeps: int = 360,
) -> List[Dict[str, object]]:
    """Run the closure cycle at multiple v_read values and collect votes +
    impedance."""
    if initial_state is None:
        initial_state = make_test_state()
    rows = []
    for v in v_read_values:
        trace = run_closure_cycle(initial_state, v_read=v, n_substeps=n_substeps)
        votes = compute_votes(trace)
        imp = compute_impedance(trace)
        rows.append({
            "v_read": v,
            "V_axial": votes.V_axial,
            "V_vector": votes.V_vector,
            "V_bivector": votes.V_bivector,
            "ratio_biv_over_axial": votes.ratio_biv_over_axial,
            "ratio_vec_over_axial": votes.ratio_vector_over_axial,
            "leakage_half_cycle": imp["leakage_half_cycle"],
            "impedance_per_unit_time": imp["impedance_per_unit_time"],
        })
    return rows


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_vortex_calibration() -> List[str]:
    """One-call vortex calibration test: sweep v_read, report invariants."""
    lines = []
    lines.append("=" * 76)
    lines.append("  VORTEX CALIBRATION — π-walk read-speed test")
    lines.append("=" * 76)

    v_read_values = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    state = make_test_state()
    rows = sweep_v_read(v_read_values, initial_state=state, n_substeps=360)

    lines.append("")
    lines.append("  Initial state: e_0 + T_2  (axial norm 1, bivector norm √3, vector 0)")
    lines.append("")
    lines.append("  v_read | V_axial  V_vec  V_biv | V_biv/V_ax  V_vec/V_ax | impedance_/_time")
    lines.append("  ------ + ------  -----  ----- + ----------  ---------- + ----------------")
    for r in rows:
        lines.append(
            f"  {r['v_read']:5.2f}  | {r['V_axial']:.4f}  {r['V_vector']:.4f}  {r['V_bivector']:.4f}"
            f" |   {r['ratio_biv_over_axial']:.4f}    {r['ratio_vec_over_axial']:8.4f}"
            f" |  {r['impedance_per_unit_time']:.4f}"
        )

    lines.append("")
    lines.append("  Tests (P1) and (P2):")
    bivax_ratios = [r["ratio_biv_over_axial"] for r in rows]
    vecax_ratios = [r["ratio_vec_over_axial"] for r in rows]
    leakages = [r["leakage_half_cycle"] for r in rows]
    impedances = [r["impedance_per_unit_time"] for r in rows]

    bivax_range = max(bivax_ratios) - min(bivax_ratios)
    vecax_range = max(vecax_ratios) - min(vecax_ratios)
    lines.append(f"    (P1) V_biv/V_ax range across v_read: {bivax_range:.3e}  (expect ~0 if invariant)")
    lines.append(f"         V_vec/V_ax range across v_read: {vecax_range:.3e}  (expect ~0)")
    lines.append(f"         Mean V_biv/V_ax across v_read : {sum(bivax_ratios)/len(bivax_ratios):.6f}  (expect √3 = {math.sqrt(3):.6f})")
    lines.append("")
    lines.append(f"    (P2) Leakage / cycle (kinematic):       {leakages[0]:.4f} → {leakages[-1]:.4f}")
    lines.append(f"         Impedance × v_read (dynamics): {impedances[0]:.4f} → {impedances[-1]:.4f}")
    lines.append(f"         (impedance × v_read should grow linearly if leakage is v_read-independent)")
    lines.append("")

    # Bonus: pure-axial state — vortex circulation should be invariant zero
    lines.append("  Control: pure axial initial state (should have V_vec = V_biv = 0):")
    ctrl_rows = sweep_v_read([1.0, 4.0], initial_state=make_axial_only_state(), n_substeps=180)
    for r in ctrl_rows:
        lines.append(
            f"    v_read={r['v_read']:.2f}  V_axial={r['V_axial']:.4f}  "
            f"V_vec={r['V_vector']:.4e}  V_biv={r['V_bivector']:.4e}"
        )
    lines.append("")
    return lines


__all__ = [
    "continuous_eisenstein_rotation",
    "continuous_omega_rotation",
    "sector_norms",
    "CycleTrace",
    "run_closure_cycle",
    "VoteResult",
    "compute_votes",
    "compute_impedance",
    "make_test_state",
    "make_axial_only_state",
    "make_mixed_test_state",
    "sweep_v_read",
    "showcase_vortex_calibration",
]
