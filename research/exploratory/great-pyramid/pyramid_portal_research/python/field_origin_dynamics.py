"""
field_origin_dynamics.py
=========================

Bridge module: the closure-node engine drives the resonance wrapper.

The field-origin equation in portal_resonance.py models four pieces:

    V_origin(x) = Psi_AB(x) + lambda_e J_4(x) + g_R R_x + h_21 cos(21 theta_x)

In portal_resonance.py the cross-sheet order parameter Psi_AB(x) and the
associator source g_R R_x are *postulated* amplitudes carrying the right
algebraic shape.  The field-origin synthesis (May 2026 canonical doc)
correctly identifies them as derivable from an exact closure-node
dynamics on A_3 = <1,I> + Z[omega]^3 (closure_core256).

This bridge implements the derivation chain:

      x_t in A_3 (8-state Walsh coeffs)
              |  three-sweep update T_{b3} T_{b2} T_{b1}
              v
      x_{t+1} = P_Omega T_{b3} T_{b2} T_{b1} x_t        (closure dynamics)
              |  associator on three consecutive states
              v
      R(x_t, x_{t+1}, x_{t+2}) = (x_t * x_{t+1}) * x_{t+2}
                                 - x_t * (x_{t+1} * x_{t+2})
              |  axial projection Pi_<1,I>
              v
      y_t = a + b*I  in  <1,I>                          (axial defect readout)
              |  complex lift
              v
      Psi_AB(t) := a + i b                              (the driver)
              |  arg
              v
      theta(t) = arg(Psi_AB(t))                         (the phase lift)
              |  Z_21 Landau evolution from portal_resonance
              v
      Omega_21 lock when theta(t) = 2*pi*n/21

The closure-node theorem from section 01.5 of the framework -- that
R(a,b,c) lands in <1,I> -- is now a *runtime invariant* checked every
tick rather than a cited theorem.  Off-axial residue is the M_4 metric
from the field-origin simulator architecture (Stephen's 9-metric panel).

Nothing in this module re-derives algebra that closure_core256 already
verifies.  This is purely the bridge layer.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

import math
import numpy as np

from python.closure_core256 import (
    MASKS3,
    walsh_matrix_3,
    clifford_product_3,
    closure_projection3,
    sweep_product3,
    to_closure_coords3,
    mask_grade,
)


# ---------------------------------------------------------------------------
# Axial / non-axial projections at the closure-node level
# ---------------------------------------------------------------------------

# In mask order (0..7) the axial sector <1, I> corresponds to mask 0
# (scalar 1) and mask 7 (pseudoscalar I = e_123).  Everything else
# is the parity-odd / Eisenstein middle sector.
AXIAL_MASKS = (0, 7)


def axial_projection(coeffs: np.ndarray) -> np.ndarray:
    """
    Pi_<1,I>: project an 8-coeff closure-node state onto the axial sector
    <1, I>, zeroing the 6 middle coordinates.
    """
    coeffs = np.asarray(coeffs, dtype=float)
    if coeffs.shape != (8,):
        raise ValueError("coeffs must have shape (8,)")
    out = np.zeros(8, dtype=float)
    out[0] = coeffs[0]
    out[7] = coeffs[7]
    return out


def axial_components(coeffs: np.ndarray) -> Tuple[float, float]:
    """Return (a, b) with a = scalar coefficient, b = pseudoscalar coefficient."""
    coeffs = np.asarray(coeffs, dtype=float)
    return float(coeffs[0]), float(coeffs[7])


def non_axial_residue_norm(coeffs: np.ndarray) -> float:
    """
    The L^2 norm of the non-axial (middle Eisenstein) component.
    This is Stephen's M_4 metric: |(I - Pi_axial) R| for the associator.
    Must be 0 (within tolerance) if the closure-node theorem holds.
    """
    coeffs = np.asarray(coeffs, dtype=float)
    middle = np.array([coeffs[m] for m in MASKS3 if m not in AXIAL_MASKS])
    return float(np.linalg.norm(middle))


# ---------------------------------------------------------------------------
# Associator and axial readout
# ---------------------------------------------------------------------------

def associator(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    """
    Associator R(a, b, c) = (a * b) * c - a * (b * c)

    where * is the closure / sweep product (Clifford then P_Omega project).
    """
    left = sweep_product3(sweep_product3(a, b), c)
    right = sweep_product3(a, sweep_product3(b, c))
    return left - right


def associator_axial_readout(
    a: np.ndarray, b: np.ndarray, c: np.ndarray
) -> Tuple[complex, float]:
    """
    Compute the axial-projected associator and return (y, residual)
    where:
        y = scalar + i * pseudoscalar       (complex axial value)
        residual = ||Pi_non_axial R||       (M_4 invariant; should be ~0)
    """
    R = associator(a, b, c)
    a_scalar, b_pseudo = axial_components(R)
    residue = non_axial_residue_norm(R)
    y = complex(a_scalar, b_pseudo)
    return y, residue


# ---------------------------------------------------------------------------
# Three-sweep update with bridge filters
# ---------------------------------------------------------------------------

# The Walsh matrix on the 3-cube.  H @ H.T = N * I with N = 8.
H3 = walsh_matrix_3()


def walsh_bridge_step(state: np.ndarray, bridge: np.ndarray) -> np.ndarray:
    """
    Single sweep T_b(x): forward Walsh, multiply by diagonal bridge, inverse Walsh.

    closure_core256's convention:
        forward (truth -> walsh):  s = H.T @ x / N
        inverse (walsh -> truth):  x = H @ s

    Composing gives  T_b(x) = H @ diag(b) @ H.T @ x / N.

    With b = (1,...,1) this is the Walsh round-trip identity.
    """
    state = np.asarray(state, dtype=float)
    bridge = np.asarray(bridge, dtype=float)
    if state.shape != (8,) or bridge.shape != (8,):
        raise ValueError("state and bridge must have shape (8,)")
    N = 8
    spectrum = H3.T @ state / N
    filtered = bridge * spectrum
    return H3 @ filtered


def three_sweep_update(
    state: np.ndarray,
    bridges: Tuple[np.ndarray, np.ndarray, np.ndarray],
) -> np.ndarray:
    """
    x_{t+1} = P_Omega T_{b_3} T_{b_2} T_{b_1} x_t

    Three Walsh-bridge sweeps, then project onto Omega-invariants.
    """
    b1, b2, b3 = bridges
    x1 = walsh_bridge_step(state, b1)
    x2 = walsh_bridge_step(x1, b2)
    x3 = walsh_bridge_step(x2, b3)
    return closure_projection3(x3)


# ---------------------------------------------------------------------------
# The driver: Psi_AB(t) as the derived axial readout
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class FieldOriginTick:
    """
    One discrete tick of the field-origin dynamics.

    Fields:
        t              : tick index
        state          : closure-node state (8-vector)
        psi_ab         : complex axial readout of R(x_{t-2}, x_{t-1}, x_t)
        theta          : arg(psi_ab) (radians; 0 if |psi_ab| < eps)
        residue_m4     : ||Pi_non_axial R||; should be ~0 by closure theorem
        amplitude      : |psi_ab|
    """
    t: int
    state: np.ndarray
    psi_ab: complex
    theta: float
    residue_m4: float
    amplitude: float


def run_field_origin_ticks(
    initial_state: np.ndarray,
    bridges: Tuple[np.ndarray, np.ndarray, np.ndarray],
    n_ticks: int = 8,
) -> List[FieldOriginTick]:
    """
    Evolve a closure-node state through n_ticks of three-sweep update
    and return the axial-readout trace.

    For each tick t >= 2, computes Psi_AB(t) as the axial component of
    R(x_{t-2}, x_{t-1}, x_t).  Earlier ticks have psi_ab = 0 (no
    associator window available yet).

    The trace is the input to the resonance lift in portal_resonance.py:
    arg(psi_ab) is fed into the Z_21 Landau potential, |psi_ab| modulates
    the cross-sheet coherence amplitude, and residue_m4 is a per-tick
    diagnostic that the closure-node theorem holds in this regime.
    """
    if n_ticks < 1:
        raise ValueError("n_ticks must be >= 1")
    initial_state = np.asarray(initial_state, dtype=float)
    if initial_state.shape != (8,):
        raise ValueError("initial_state must have shape (8,)")

    history: List[np.ndarray] = [initial_state.copy()]
    ticks: List[FieldOriginTick] = []

    # Tick 0: no associator window yet
    ticks.append(FieldOriginTick(
        t=0, state=history[0].copy(), psi_ab=0+0j,
        theta=0.0, residue_m4=0.0, amplitude=0.0
    ))

    for step in range(1, n_ticks):
        x_prev = history[-1]
        x_next = three_sweep_update(x_prev, bridges)
        history.append(x_next)

        if step >= 2:
            y, residue = associator_axial_readout(
                history[step - 2], history[step - 1], history[step]
            )
            amp = abs(y)
            theta = math.atan2(y.imag, y.real) if amp > 1e-15 else 0.0
            ticks.append(FieldOriginTick(
                t=step, state=x_next.copy(), psi_ab=y,
                theta=theta, residue_m4=residue, amplitude=amp,
            ))
        else:
            ticks.append(FieldOriginTick(
                t=step, state=x_next.copy(), psi_ab=0+0j,
                theta=0.0, residue_m4=0.0, amplitude=0.0,
            ))

    return ticks


# ---------------------------------------------------------------------------
# Convenience: the canonical TetA-only and TetB-only initial states
# ---------------------------------------------------------------------------

def tet_a_axial_seed() -> np.ndarray:
    """An axial-only seed on the +1 parity tetrahedron (scalar component)."""
    seed = np.zeros(8, dtype=float)
    seed[0] = 1.0  # scalar
    return seed


def tet_b_axial_seed() -> np.ndarray:
    """An axial-only seed on the -1 parity tetrahedron (pseudoscalar I)."""
    seed = np.zeros(8, dtype=float)
    seed[7] = 1.0  # pseudoscalar I = e_123
    return seed


def mixed_axial_seed(scalar: float = 1.0, pseudoscalar: float = 1.0) -> np.ndarray:
    """
    A coherent superposition of TetA and TetB axial components.
    Represents an initial state with cross-sheet character.
    """
    seed = np.zeros(8, dtype=float)
    seed[0] = float(scalar)
    seed[7] = float(pseudoscalar)
    return seed


# ---------------------------------------------------------------------------
# The nine-metric diagnostic panel (M_1 .. M_9 from the field-origin spec)
# ---------------------------------------------------------------------------

def m1_walsh_inversion_error() -> float:
    """M_1 = ||H^2 - N I||.  Walsh inversion exactness; should be 0."""
    N = 8
    HH = H3 @ H3.T  # H is symmetric on the 3-cube, so H^2 = H H^T
    target = N * np.eye(8)
    return float(np.linalg.norm(HH - target))


def m2_eisenstein_closure_error() -> float:
    """
    M_2 = ||Omega^3 - I||.  Eisenstein 3-cycle exactness; should be 0.

    Tested by acting Omega three times on a random middle-sector state
    and comparing to the identity.
    """
    rng = np.random.default_rng(42)
    test = rng.standard_normal(8)
    from python.closure_core256 import omega_power3
    once = omega_power3(test, 1)
    twice = omega_power3(once, 1)
    thrice = omega_power3(twice, 1)
    return float(np.linalg.norm(thrice - test))


def m3_projector_idempotent_error() -> float:
    """M_3 = ||P_Omega^2 - P_Omega||.  Projector idempotence; should be 0."""
    rng = np.random.default_rng(43)
    test = rng.standard_normal(8)
    P_once = closure_projection3(test)
    P_twice = closure_projection3(P_once)
    return float(np.linalg.norm(P_twice - P_once))


def m4_associator_axial_residue(
    a: np.ndarray = None,
    b: np.ndarray = None,
    c: np.ndarray = None,
) -> float:
    """
    M_4 = ||(I - Pi_axial) R(a,b,c)||.  Associator axial landing.

    The closure-node theorem (section 01.5) says R lands in <1,I>.
    M_4 must be ~0 for the theorem to hold at this point in state space.

    With no arguments, runs on a default seed triple to give a single
    representative number.
    """
    if a is None:
        a = mixed_axial_seed(1.0, 0.5)
    if b is None:
        b = mixed_axial_seed(0.5, 1.0)
    if c is None:
        c = mixed_axial_seed(0.25, 0.75)
    R = associator(a, b, c)
    return non_axial_residue_norm(R)


def m5_axial_defect_magnitude(
    a: np.ndarray = None,
    b: np.ndarray = None,
    c: np.ndarray = None,
) -> float:
    """
    M_5 = |R_axial|.  Magnitude of the axial associator defect.

    This is the *signal* once M_1..M_4 are confirmed zero.  Nonzero M_5
    means the closure-node has genuine source/curvature content; zero
    M_5 means trivial vacuum.
    """
    if a is None:
        a = mixed_axial_seed(1.0, 0.5)
    if b is None:
        b = mixed_axial_seed(0.5, 1.0)
    if c is None:
        c = mixed_axial_seed(0.25, 0.75)
    y, _ = associator_axial_readout(a, b, c)
    return float(abs(y))


def nine_metric_diagnostic_panel(
    omega_21_lock_quality: float = 0.0,
    mirror_match_quality: float = 0.0,
    output_correlation: float = 0.0,
    pentachoron_edge_residue: float = 0.0,
) -> dict:
    """
    Compute the field-origin nine-metric panel (M_1 .. M_9).

    M_1..M_5 are computed from the closure-node engine.
    M_6..M_9 are passed in from the resonance / apparatus layer.

    Per the spec: a run is valid only if M_1, M_2, M_3, M_4 are ~0.
    Then M_5..M_8 become meaningful engineering controls.  Then M_9
    is allowed to matter.
    """
    return {
        "M_1_walsh_inversion": m1_walsh_inversion_error(),
        "M_2_eisenstein_closure": m2_eisenstein_closure_error(),
        "M_3_projector_idempotent": m3_projector_idempotent_error(),
        "M_4_associator_axial_residue": m4_associator_axial_residue(),
        "M_5_axial_defect_magnitude": m5_axial_defect_magnitude(),
        "M_6_pentachoron_edge_residue": pentachoron_edge_residue,
        "M_7_z21_lock_inverse": 1.0 - omega_21_lock_quality,
        "M_8_mirror_match_error": 1.0 - mirror_match_quality,
        "M_9_output_correlation": output_correlation,
    }


def diagnostic_panel_run_validity(panel: dict, tol_exact: float = 1e-9) -> dict:
    """
    Decide whether a diagnostic panel describes a valid run.

    A run is *valid* iff M_1, M_2, M_3, M_4 are all below tol_exact.
    Returns a dict with:
        valid: bool
        reason: str (which metric failed, or "all exact invariants pass")
    """
    for key in ("M_1_walsh_inversion", "M_2_eisenstein_closure",
                "M_3_projector_idempotent", "M_4_associator_axial_residue"):
        v = panel.get(key, float("inf"))
        if v > tol_exact:
            return {"valid": False, "reason": f"{key} = {v:.3e} > tol {tol_exact:.0e}"}
    return {"valid": True, "reason": "all exact invariants pass"}


def showcase_field_origin_dynamics() -> List[str]:
    """One-shot audit trail for the bridge layer."""
    lines: List[str] = []
    lines.append("=" * 70)
    lines.append("  Field-Origin Dynamics: bridge from closure-node to resonance")
    lines.append("=" * 70)
    lines.append("")
    lines.append("Architecture (Stephen's correction):")
    lines.append("  closure_core256 (exact) -> bridge (derived Psi_AB) -> portal_resonance (lift)")
    lines.append("")
    lines.append("Nine-metric panel:")
    panel = nine_metric_diagnostic_panel(
        omega_21_lock_quality=1.0,
        mirror_match_quality=1.0,
        output_correlation=0.81,    # |tau_21| -ish placeholder
        pentachoron_edge_residue=0.0,
    )
    for k, v in panel.items():
        lines.append(f"  {k:38s} = {v:.6e}")
    lines.append("")
    valid = diagnostic_panel_run_validity(panel)
    lines.append(f"Run validity: {valid['valid']}  ({valid['reason']})")
    lines.append("")
    # Demonstrate a short tick trace
    bridges = (np.ones(8), np.ones(8), np.ones(8))
    trace = run_field_origin_ticks(mixed_axial_seed(1.0, 0.7), bridges, n_ticks=4)
    lines.append("Sample tick trace (mixed axial seed, identity bridges):")
    lines.append("  t | amplitude | theta(rad) | residue_M4")
    lines.append("  " + "-" * 50)
    for tick in trace:
        lines.append(f"  {tick.t} | {tick.amplitude:9.4f} | {tick.theta:10.4f} | {tick.residue_m4:11.3e}")
    lines.append("")
    return lines
