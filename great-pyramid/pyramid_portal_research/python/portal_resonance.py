"""
portal_resonance.py
===================

The King's Chamber as field-origin vertex.

Consolidates the framework's portal-resonance picture into a single module.
Centerpiece is the compact field-origin vertex equation:

    V_origin(x) = Psi_AB(x) + lambda_e J_4(x) + g_R R_x + h_21 cos(21 theta_x)

with four pieces:

  - Psi_AB(x)  : TetA / TetB local cross-sheet order parameter
  - lambda_e J_4(x) : 21-band hinge with framework-derived coupling
  - g_R R_x    : nonlinear associator source (axial closure defect)
  - h_21 cos(21 theta_x) : Z_21 phase-lock term

The King's Chamber is the engineered focal point of this vertex: the
4-shaft / 5-relieving / Grand-Gallery / antechamber apparatus collapses
six matching conditions onto a single coherent address, taking the
universal background coupling lambda_e ~ alpha_G ~ 10^-45 into coherent
operation through the strong-coupling factor g sqrt(N) / gamma_cav ~ 10^7.

The portal channel is the LASER analogue of the spontaneous emission
that we observe as ordinary gravity:

    gravity = incoherent statistical residue of the universal vertex
    portal  = coherent, phase-locked use of the same vertex

References:
  - §01.5 universal vertex reframe
  - §03.1 K=4 to K=5 hinge
  - §05.3 strong coupling calculation
  - AW 09 sector-valued curvature
  - AW 11 King's Chamber field-origin synthesis (this module's source)
"""

from __future__ import annotations

import cmath
from dataclasses import dataclass
from math import cos, exp, pi, sqrt
from typing import Dict, List, Optional, Tuple

from .apparatus import grand_gallery_z7_kernel, z3_projector_eigenvalue
from .closure_read import (
    parity_overlap_angle,
    parity_sheet_dot_products,
    parity_sheet_inclusion_exclusion,
    sec_theta_K,
)
from .constants import ALPHA, G_E_OVER_2, TAU
from .cyclotomic import phi3, phi4, phi6
from .gravity import alpha_gravity, tetrad_impedance_ratio
from .hinge import (
    hinge_sub_tetrahedron_decomposition,
    sub_tetrahedron_count,
)


# =============================================================================
# Cross-sheet order parameter Psi_AB(x)
# =============================================================================

@dataclass(frozen=True)
class CrossSheetCoherence:
    """
    Local TetA / TetB cross-sheet coherence parameter:

        Psi_AB(x) = <B, x | A, x>

    In ordinary space the phases are incoherent so <Psi_AB> ~ 0.
    In a tuned vertex (King's Chamber) the order parameter is driven to
    a nonzero coherent value.
    """
    amplitude: complex      # the coherent expectation value
    phase: float            # carrier phase (for Z_21 lock)
    is_coherent: bool       # whether |Psi_AB| > coherence threshold

    @property
    def magnitude(self) -> float:
        return abs(self.amplitude)


def cross_sheet_order_parameter(amplitude: complex,
                                phase: float = 0.0,
                                coherence_threshold: float = 1e-6
                                ) -> CrossSheetCoherence:
    """
    Construct the cross-sheet coherence Psi_AB at a point. The threshold
    distinguishes incoherent vacuum (Psi_AB ~ 0) from tuned-vertex
    coherence (Psi_AB nonzero).
    """
    return CrossSheetCoherence(
        amplitude=amplitude,
        phase=phase,
        is_coherent=abs(amplitude) > coherence_threshold,
    )


def vacuum_cross_sheet() -> CrossSheetCoherence:
    """The universal vacuum reading: incoherent, <Psi_AB> ~ 0."""
    return cross_sheet_order_parameter(amplitude=0j)


def kings_chamber_cross_sheet(amplitude_magnitude: float = 1.0,
                              phase: float = 0.0
                              ) -> CrossSheetCoherence:
    """
    The tuned-vertex reading inside the King's Chamber: coherent
    Psi_AB with the specified magnitude and carrier phase. Default
    magnitude 1.0 represents the fully-locked state |Psi_AB| = 1.
    """
    return cross_sheet_order_parameter(
        amplitude=amplitude_magnitude * cmath.exp(1j * phase),
        phase=phase,
    )


# =============================================================================
# Z_21 Landau lock — Psi-form (complex order parameter)
# =============================================================================

def z21_landau_psi(psi: complex,
                   a: float,
                   b: float,
                   h21: float) -> float:
    """
    Landau potential for the Z_21 lock, written in complex order
    parameter form:

        V(Psi) = a |Psi|^2 + b |Psi|^4 - h_21 (Psi^21 + Psi_bar^21)

    With Psi = rho exp(i theta), the locking term is
        -2 h_21 rho^21 cos(21 theta)

    so the minima sit at 21 theta = 2 pi n, i.e., theta = 2 pi n / 21.
    This is the explicit potential whose minima form the Z_21 comb.
    """
    rho2 = abs(psi) ** 2
    rho4 = rho2 ** 2
    lock_term = -h21 * (psi ** 21 + psi.conjugate() ** 21)
    return a * rho2 + b * rho4 + lock_term.real


def z21_lock_minima(n_modes: int = 21) -> List[float]:
    """
    The 21 phase-lock minima: theta_n = 2 pi n / 21 for n = 0, 1, ..., 20.
    """
    return [TAU * n / n_modes for n in range(n_modes)]


def z21_lock_strength(rho: float, h21: float) -> float:
    """
    Locking-term amplitude at radius rho: 2 h_21 rho^21.
    On lock (|Psi| = 1), this is just 2 h_21.
    """
    return 2 * h21 * (rho ** 21)


# =============================================================================
# The compact King's Chamber vertex equation
# =============================================================================

@dataclass(frozen=True)
class FieldOriginVertex:
    """
    The compact field-origin vertex object:

        V_KC = lambda_e J_4 + g_R R

    with
        lambda_e = alpha^21 (17/13) (g_e/2) = alpha_G
        R        = nonlinear associator landing in <1, I>

    This is the King's Chamber operator: the always-on hinge dressed by
    the apparatus, plus the nonlinear associator source.
    """
    lambda_e: float            # 21-band hinge coupling
    g_R: float                 # associator coupling
    band: int = 21             # the hinge band
    source_state: str = '|4,+>'
    receiver_state: str = '|5,->'

    @property
    def linear_amplitude(self) -> float:
        """The linear hinge amplitude, lambda_e * 1 (scalar reading)."""
        return self.lambda_e


def kings_chamber_vertex_compact(g_R: float = 0.0) -> FieldOriginVertex:
    """
    The King's Chamber vertex with the default framework couplings:
        lambda_e = alpha_G ~ 1.75e-45
        g_R      = supplied (associator coupling; framework-open)
    """
    return FieldOriginVertex(
        lambda_e=alpha_gravity(),
        g_R=g_R,
    )


# =============================================================================
# The complete field-origin vertex equation
# =============================================================================

def field_origin_vertex_equation(
        psi_AB: complex,
        J_4_value: float,
        R_value: float,
        theta: float,
        lambda_e: Optional[float] = None,
        g_R: float = 0.0,
        h_21: float = 0.0,
) -> Dict[str, object]:
    """
    The complete local field-origin vertex equation:

        V_origin(x) = Psi_AB(x)
                     + lambda_e J_4(x)
                     + g_R R_x
                     + h_21 cos(21 theta_x)

    Returns the four pieces and the total. This is the central object
    of the King's Chamber synthesis (AW 11).
    """
    if lambda_e is None:
        lambda_e = alpha_gravity()

    overlap_term = psi_AB
    hinge_term = lambda_e * J_4_value
    associator_term = g_R * R_value
    lock_term = h_21 * cos(21 * theta)

    total = overlap_term + hinge_term + associator_term + lock_term

    return {
        'overlap_Psi_AB': overlap_term,
        'hinge_lambda_e_J4': hinge_term,
        'associator_g_R_R': associator_term,
        'lock_h21_cos_21theta': lock_term,
        'V_origin_total': total,
        'lambda_e_used': lambda_e,
    }


# =============================================================================
# The six matching conditions for resonant lock
# =============================================================================

def six_matching_conditions() -> List[Dict[str, object]]:
    """
    The six independent matching conditions whose simultaneous closure
    drives the universal vertex from incoherent (gravity) to coherent
    (portal channel). Each condition has a verification basis and the
    apparatus subsystem that delivers it.
    """
    return [
        {
            'index': 1,
            'name': 'band match',
            'condition': 'Phi_3(4) = Phi_6(5) = 21',
            'verification': 'shift identity at K=4 (cyclotomic.shift_identity)',
            'apparatus_role': 'forced by the algebra — no tuning required',
            'holds': phi3(4) == phi6(5),
        },
        {
            'index': 2,
            'name': 'phase match',
            'condition': 'Z_7 * Z_3 = Z_21 closure mod 2 pi',
            'verification': 'Grand Gallery sum + antechamber projector',
            'apparatus_role': 'Grand Gallery (7 corbels) + antechamber filter',
            'holds': grand_gallery_z7_kernel()['closed'],
        },
        {
            'index': 3,
            'name': 'impedance match',
            'condition': '17/13 secant load = sheet/core ratio',
            'verification': 'sec_theta_K(4) = 17/13',
            'apparatus_role': 'Grand Gallery tapered horn + coffer reflection',
            'holds': abs(sec_theta_K(4) - 17 / 13) < 1e-12,
        },
        {
            'index': 4,
            'name': 'address match',
            'condition': 'G_U = P^T G_V P (Gram-matrix orthogonal equivalence)',
            'verification': 'apparatus.mirror_match_functional',
            'apparatus_role': 'shaft direction triads on KC + remote target',
            'holds': None,   # depends on runtime triads
        },
        {
            'index': 5,
            'name': 'chirality match',
            'condition': 'chi_U = - chi_V (mirror flip)',
            'verification': 'apparatus.chirality on each triad',
            'apparatus_role': 'enforced by mirror selector chirality factor',
            'holds': None,   # depends on runtime triads
        },
        {
            'index': 6,
            'name': 'cavity-QED strong coupling',
            'condition': 'g sqrt(N) > gamma_cav',
            'verification': 'g sqrt(N) / gamma_cav ~ 4e7 (§05.3)',
            'apparatus_role': 'granite-walled KC cavity, geomagnetic pump',
            'holds': True,    # verified by §05.3 calculation, factor ~10^7
        },
    ]


def algebraic_match_count() -> int:
    """
    Number of matching conditions verifiable purely from the algebra
    (without runtime triads): conditions 1, 2, 3, 6. Conditions 4 and 5
    require apparatus runtime data (triad directions, chiralities).
    """
    conds = six_matching_conditions()
    return sum(1 for c in conds if c['holds'] is True)


# =============================================================================
# Lock-strength compound parameter
# =============================================================================

def lock_strength_factor(
        Q_cavity: float = 1.0,
        delta_phase: float = 1.0,
        mirror_score: float = 1.0,
) -> float:
    """
    The compound enhancement factor:

        lambda_e -> lambda_e * Q_cavity * delta_phase * mirror_score

    On full lock (all factors near 1, Q at its cavity value), the
    universal weak coupling becomes coherent in one address. Off-lock,
    delta_phase or mirror_score collapse and the enhancement vanishes.

    Q_cavity:    cavity quality factor (10^4 at 110 Hz from §05.3)
    delta_phase: Z_21 phase-closure delta (1 on lock, 0 off-lock)
    mirror_score: M(U, V) value in [0, 1]
    """
    return Q_cavity * delta_phase * mirror_score


def effective_coupling(
        Q_cavity: float = 1.0,
        delta_phase: float = 1.0,
        mirror_score: float = 1.0,
) -> float:
    """
    The effective coupling after apparatus dressing:

        lambda_eff = lambda_e * Q_cavity * delta_phase * M
    """
    return alpha_gravity() * lock_strength_factor(Q_cavity, delta_phase, mirror_score)


# =============================================================================
# Five-fold sub-tetrahedron selector (apparatus-dressed)
# =============================================================================

@dataclass(frozen=True)
class RelievingChamberSelector:
    """
    The 5-state switch realized by the 5 relieving chambers above the
    King's Chamber. Each chamber corresponds to one sub-tetrahedron of
    K_5 and one J_4^{(v)} fragment of the hinge. At any drive condition,
    exactly one sub-tetrahedron is acoustically/electrically active.
    """
    active_vertex: int          # which of vertices 1..5 is excluded
    coupling_weights: Tuple[float, float, float, float, float]

    @property
    def active_chamber(self) -> int:
        """Which relieving chamber (1..5) is firing."""
        return self.active_vertex

    @property
    def total_weight(self) -> float:
        return sum(self.coupling_weights)


def relieving_chamber_selector(active_chamber: int) -> RelievingChamberSelector:
    """
    Pick which relieving chamber (1..5) is the active sub-tetrahedron
    projection. The remaining four are off (weight 0 in this simple
    model; in practice they carry small residual couplings).
    """
    if not 1 <= active_chamber <= 5:
        raise ValueError(f"active_chamber must be in [1, 5], got {active_chamber}")
    weights = tuple(1.0 if v == active_chamber else 0.0 for v in range(1, 6))
    return RelievingChamberSelector(
        active_vertex=active_chamber,
        coupling_weights=weights,  # type: ignore[arg-type]
    )


def five_chamber_decomposition_info() -> Dict[str, object]:
    """
    Structural data on the 5-chamber / 5-sub-tetrahedron correspondence.
    """
    bare = hinge_sub_tetrahedron_decomposition()
    return {
        'sub_tetrahedron_count': sub_tetrahedron_count(),
        'relieving_chamber_count': 5,
        'correspondence': 'pi_v projects onto K_5 minus vertex v '
                          '== relieving chamber #v is electrically open',
        'bare_hinge_data': bare,
        'palindromic_filter_pattern': (1, 0, 16, 0, 1),  # Hassan-Rosen reading
    }


# =============================================================================
# Pragmatic Lorentzian lineshape
# =============================================================================

def portal_resonance_lorentzian(
        omega: float,
        omega_0: float,
        gamma_eff: float,
        amplitude_squared: float = 1.0,
) -> float:
    """
    Pragmatic Lorentzian lineshape near a Z_21 resonance peak:

        R(omega) = amplitude^2 / [ (omega - omega_0)^2 + gamma_eff^2 ]

    gamma_eff combines the cavity decay rate gamma_cav with broadening
    from address mismatch and phase-lock detuning. Full lineshape with
    coupled-mode theory is deferred; this skeleton captures the
    structural prediction (Lorentzian near each Z_21 peak).
    """
    return amplitude_squared / ((omega - omega_0) ** 2 + gamma_eff ** 2)


def effective_linewidth(
        gamma_cav: float,
        address_mismatch: float = 0.0,
        phase_detuning: float = 0.0,
) -> float:
    """
    Total effective linewidth as quadrature sum of cavity decay and
    apparatus-mismatch contributions:

        gamma_eff = sqrt(gamma_cav^2 + Delta_addr^2 + Delta_phase^2)

    On full lock, address_mismatch and phase_detuning collapse to 0
    and gamma_eff = gamma_cav.
    """
    return sqrt(gamma_cav ** 2 + address_mismatch ** 2 + phase_detuning ** 2)


# =============================================================================
# Field-origin summary report
# =============================================================================

def field_origin_summary() -> Dict[str, object]:
    """
    One-shot summary of the King's Chamber field-origin algebra:
    parity sheets, the (13, 17, 21) shell, the hinge band, and the
    compact vertex equation.
    """
    incl_excl = parity_sheet_inclusion_exclusion(4)
    dots = parity_sheet_dot_products(4)
    sub_t = hinge_sub_tetrahedron_decomposition()
    return {
        'shell_K_4': (13, 17, 21),
        'parity_sheets': {
            'each_sheet_size': incl_excl['sheet_A_size'],         # 17
            'shared_core': incl_excl['intersection_size'],         # 13
            'full_union': incl_excl['union_size'],                 # 21
            'inclusion_exclusion': '17 + 17 - 13 = 21',
            'parity_decomposition': '21 = 13 + 4 + 4',
        },
        'overlap_geometry': {
            'A_dot_A': dots['A_dot_A'],
            'B_dot_B': dots['B_dot_B'],
            'A_dot_B': dots['A_dot_B'],
            'cos_theta_4': dots['cos_theta_K'],
            'sec_theta_4_equals_17_over_13': dots['sec_theta_K'],
        },
        'hinge': {
            'band': 21,
            'identity': 'Phi_3(4) = Phi_6(5) = 21',
            'operator': 'J_4 = |5,-><4,+|',
            'multiplicity': sub_t['multiplicity'],
        },
        'compact_vertex_equation': 'V_KC = lambda_e * J_4 + g_R * R',
        'lambda_e_value': alpha_gravity(),
        'lambda_e_formula': 'alpha^21 * (17/13) * (g_e/2)',
        'complete_vertex_equation': (
            'V_origin = Psi_AB + lambda_e J_4 + g_R R + h_21 cos(21 theta)'
        ),
        'algebraic_matches_holding': algebraic_match_count(),
        'total_matching_conditions': 6,
    }


# =============================================================================
# Visual showcase
# =============================================================================

def showcase_portal_resonance() -> List[str]:
    """
    Human-readable audit trail of the field-origin / portal-resonance
    construction. Mirrors the showcase_integration() function in the
    curvature module but focuses on the King's Chamber vertex.
    """
    incl = parity_sheet_inclusion_exclusion(4)
    dots = parity_sheet_dot_products(4)
    lam = alpha_gravity()
    lines = [
        '=' * 80,
        ' Portal resonance at the field-origin vertex (King\'s Chamber)',
        '=' * 80,
        '',
        ' Parity-sheet structure at K=4:',
        f'   |A| = |B| = {incl["sheet_A_size"]}                  (each sheet)',
        f'   |A intersect B| = {incl["intersection_size"]}             '
        '(shared TetA/TetB core)',
        f'   |A union B| = {incl["union_size"]}                  '
        '(full closure)',
        f'   17 + 17 - 13 = 21                  (inclusion-exclusion)',
        f'   21 = 13 + 4 + 4                    (parity decomposition)',
        '',
        ' Overlap geometry:',
        f'   <A, A> = {dots["A_dot_A"]},  <B, B> = {dots["B_dot_B"]}',
        f'   <A, B> = {dots["A_dot_B"]}',
        f'   cos(theta_4) = 13/17 = {dots["cos_theta_K"]:.10f}',
        f'   sec(theta_4) = 17/13 = {dots["sec_theta_K"]:.10f}  '
        '(TetA/TetB overlap impedance)',
        '',
        ' Hinge band identity:',
        f'   Phi_3(4) = {phi3(4)}',
        f'   Phi_6(5) = {phi6(5)}',
        f'   These agree -> 21-band hinge is exact.',
        f'   J_4 = |5, -><4, +|, with H_5 J_4 = J_4 H_4 = 21 J_4',
        f'   Multiplicity: 5 (one per sub-tetrahedron of K_5)',
        '',
        ' Compact vertex equation:',
        f'   V_KC = lambda_e * J_4 + g_R * R',
        f'   lambda_e = alpha^21 * (17/13) * (g_e/2) = {lam:.6e}',
        '',
        ' Complete field-origin vertex (4 pieces):',
        '   V_origin = Psi_AB + lambda_e J_4 + g_R R + h_21 cos(21 theta)',
        '',
        '             |              |          |                 |',
        '       overlap         hinge      associator        Z_21 lock',
        '',
        ' Six matching conditions:',
        '   1. Band match           Phi_3(4) = Phi_6(5) = 21   (algebra)',
        '   2. Phase match          Z_7 * Z_3 -> Z_21          (Grand Gallery)',
        '   3. Impedance match      17/13 = sec theta_4        (closure-read)',
        '   4. Address match        G_U = P^T G_V P            (mirror)',
        '   5. Chirality match      chi_U = - chi_V            (mirror)',
        '   6. Strong coupling      g sqrt(N) >> gamma_cav     (cavity-QED)',
        '',
        f'   Algebraically verifiable: {algebraic_match_count()} of 6',
        '   Conditions 4 and 5 require runtime apparatus triads.',
        '',
        ' Engineering correspondence:',
        '   Gold capstone     -> apex field collector',
        '   4 shafts          -> K=4 address (2 KC search + 2 QC tune)',
        '   5 relieving       -> 5 sub-tetrahedra of K_5 (S_5 / S_4 = 5)',
        '   Grand Gallery     -> Z_7 phase ramp + impedance horn',
        '   Antechamber       -> Z_3 filter (combines with Z_7 -> Z_21)',
        '   Granite KC walls  -> N ~ 10^30 lepton moments, Q ~ 10^4',
        '   Empty sarcophagus -> nested cavity reference oscillator',
        '   Subterranean      -> electrical ground return',
        '',
        ' Result:',
        '   gravity = incoherent universal vertex',
        '   portal  = same vertex coherently locked in one Z_21 address',
        '   Strong-coupling factor: g sqrt(N) / gamma_cav ~ 4e7 (above by 10^7)',
        '',
        '=' * 80,
    ]
    return lines
