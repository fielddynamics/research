"""
pyramid_portal_research.python
==============================

Algebra package for the GFD / Great Pyramid portal-engineering framework.

Modules:
    constants         physical constants (ALPHA, HBAR, M_E, ...)
    cyclotomic        Phi_n, shell, shift / scale-fusion identities,
                      Niven rigidity, norm-form, cyclotomic-integer norms
    closure_read      matrix utilities, shell Hamiltonian,
                      truncated tensor algebra T_<=2(V), parity projectors,
                      graded identity, Gram matrix, parity-overlap angle,
                      sec(theta_K), Hilbert polynomial
    hinge             K=4 <-> K=5 pyramid hinge and J_4 partial isometry
    gravity           alpha_G derivation, G prediction, four routes to K=4,
                      permutation discrimination of the shell
    mu_partition      gravitational partition mu(x), Born-rule map,
                      three interior Niven readings, logistic identity,
                      SST quadratic
    electromagnetism  Maxwell in Lambda^2(V) at K=4, F^{mu nu} as the six
                      edges of K_4, three perfect matchings,
                      self-dual / anti-self-dual decomposition,
                      Dirac quantization, Coulomb step
    apparatus         KC vertex, shafts, addresses, mirror M, portal P,
                      internal subsystem operators, K/Q interferometer,
                      Z_21 order parameter
    topology          Hopf, A_5, pentachoron, null-cone associator,
                      SU(2)_19 Chern-Simons, WRT invariant of Sigma(2,3,5)
    predictions       coffer step, Sierpinski hierarchy, K=2 Schwinger,
                      lepton anchor, golden impedance
    curvature_decomposition
                      sector-valued curvature G^{AB}_{mu nu} = G^LC + G^T +
                      G^P + G^J + G^R + G^M; ordinary GR as the Levi-Civita
                      projection Pi_GR; coupling tie-back to Newton's G

Regression test suite in `tests/`. Run with `python -m unittest discover python/tests`.

References: Active Work 03-09 and project sections 01-08, 99.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
from .constants import (
    ALPHA,
    G_E_OVER_2,
    HBAR,
    C_LIGHT,
    M_E,
    G_OBSERVED,
    TAU,
)

# ---------------------------------------------------------------------------
# Cyclotomic shell algebra (extended)
# ---------------------------------------------------------------------------
from .cyclotomic import (
    phi3, phi4, phi6, coupling_polynomial,
    Shell, shell,
    shift_identity, scale_fusion_identity,
    sphere_surface_area_unit,
    niven_rigidity_check, norm_form,
    cyclotomic_integer_norm, niven_partition_table,
)

# ---------------------------------------------------------------------------
# Closure-read representation (extended)
# ---------------------------------------------------------------------------
from .closure_read import (
    Matrix, diag, matmul, matrix_equal,
    shell_hamiltonian,
    truncated_tensor_algebra, parity_projector_dimensions,
    graded_identity_trace,
    gram_matrix_K, gram_eigenvalues,
    parity_overlap_angle, sec_theta_K, verify_17_over_13_is_sec_theta_4,
    hilbert_polynomial,
    parity_sheet_inclusion_exclusion,
    parity_sheet_dot_products,
    parity_overlap_angle_geometric,
)

# ---------------------------------------------------------------------------
# K=4 <-> K=5 hinge
# ---------------------------------------------------------------------------
from .hinge import (
    PyramidHinge, pyramid_k4_k5_hinge,
    j4_partial_isometry, interlevel_intertwiner_check,
    k5_band_assignment,
    sub_tetrahedron_count, s5_supset_s4_branching,
    hinge_sub_tetrahedron_decomposition,
)

# ---------------------------------------------------------------------------
# Gravity (extended)
# ---------------------------------------------------------------------------
from .gravity import (
    directed_complete_graph_edge_count, pentachoron_directed_edge_count,
    pentachoron_edge_product, edge_phase_closure,
    tetrad_impedance_ratio,
    alpha_gravity, alpha_gravity_parts,
    coupling_exponent_for_K, gravity_over_coulomb_gap_exponent,
    tetrad_renormalization_factor, alpha_G_for_K,
    predict_G_from_alpha, G_prediction_report,
    four_routes_select_K4,
    permutation_discrimination, best_permutation,
)

# ---------------------------------------------------------------------------
# mu partition  (Phase 3)
# ---------------------------------------------------------------------------
from .mu_partition import (
    mu, tetA_share, tetB_share, odds_ratio,
    mu_derivative, logistic_identity_check,
    born_rule_map, inverse_born_rule,
    x_from_theta, partition_to_x, x_to_partition,
    niven_partition_points, mond_transition_check,
    sst_quadratic, sst_static_solve_g,
)

# ---------------------------------------------------------------------------
# Electromagnetism  (Phase 3)
# ---------------------------------------------------------------------------
from .electromagnetism import (
    vv_decomposition,
    tetrahedral_edges, time_space_edges, space_space_edges,
    F_mu_nu_basis,
    perfect_matchings_K4, opposite_edge_pairs_K4,
    self_dual_part, anti_self_dual_part,
    self_dual_anti_self_dual_decomposition,
    hodge_star_squared_lorentzian,
    dirac_quantization_check,
    coulomb_step, gravity_as_21_coulomb_steps,
)

# ---------------------------------------------------------------------------
# Apparatus operators
# ---------------------------------------------------------------------------
from .apparatus import (
    Vector3, dot, norm, normalize,
    gram_matrix, determinant_3, chirality, phase_closed,
    KingsChamberVertex, kings_chamber_vertex,
    portal_scalar_amplitude,
    ShaftKey, triadic_phase, Address, make_address,
    permute_gram, gram_distance, mirror_match_functional,
    apex_top_collector, granite_isolation, ascending_passage_gain,
    grand_gallery_z7_kernel,
    z3_projector_eigenvalue, z21_phase_sectors, z21_comb_frequencies,
    big_void_balance_cavity, coffer_reflection_coefficient,
    KQInterferometer, kq_phase_lock,
    z21_order_parameter, landau_z21_potential, josephson_portal_current,
    PortalMachine, local_force_kernel, portal_address_kernel,
    reciprocal_two_apparatus_operator_scalar, apparatus_operator_stack,
    complement_projector_mode, well_shaft_feedback,
)

# ---------------------------------------------------------------------------
# Topology (extended)
# ---------------------------------------------------------------------------
from .topology import (
    Quaternion,
    q_normalize, q_conjugate, q_multiply,
    hopf_projection, hopf_fiber_phase, electron_hopf_fiber_holonomy,
    alternating_group_A5_order, pentachoron_cell_count, a5_address_sector_count,
    crystallographic_threshold_pentachoron,
    null_cone_associator_status,
    wrt_su2_level_to_k_plus_2, wrt_central_charge,
    wrt_su2_19_chern_simons, wrt_invariant_sigma235_target,
)

# ---------------------------------------------------------------------------
# Predictions
# ---------------------------------------------------------------------------
from .predictions import (
    coffer_chamber_alpha_step, relieving_chamber_volume_prediction,
    sierpinski_force_hierarchy, k2_schwinger_loop_structure,
    lepton_anchor_report, golden_impedance_split,
)

# ---------------------------------------------------------------------------
# Sector-valued curvature decomposition (G^AB_munu -> Pi_GR -> G^LC_munu)
# ---------------------------------------------------------------------------
from .curvature_decomposition import (
    CurvatureSector,
    levi_civita_sector, torsion_sector, parity_overlap_sector,
    hinge_sector, associator_sector, mirror_address_sector,
    master_decomposition, sector_table,
    gr_projector, gr_visible_sectors, gr_killed_sectors,
    gr_averaged_sectors, gr_renormalized_sectors,
    framework_gravitational_coupling_report,
    einstein_projection_summary,
    showcase_integration,
    consistency_check as curvature_consistency_check,
)

# ---------------------------------------------------------------------------
# Portal resonance at the field-origin vertex (King's Chamber synthesis)
# ---------------------------------------------------------------------------
from .portal_resonance import (
    CrossSheetCoherence,
    cross_sheet_order_parameter,
    vacuum_cross_sheet, kings_chamber_cross_sheet,
    z21_landau_psi, z21_lock_minima, z21_lock_strength,
    FieldOriginVertex, kings_chamber_vertex_compact,
    field_origin_vertex_equation,
    six_matching_conditions, algebraic_match_count,
    lock_strength_factor, effective_coupling,
    RelievingChamberSelector, relieving_chamber_selector,
    five_chamber_decomposition_info,
    portal_resonance_lorentzian, effective_linewidth,
    field_origin_summary, showcase_portal_resonance,
)

# ---------------------------------------------------------------------------
# Closure core 256 (exact algebra substrate)  +  field-origin dynamics bridge
# ---------------------------------------------------------------------------
from .closure_core256 import (
    ClosureNode3, SierpinskiTile64, ClosureCore256,
    ClosureCoords3, to_closure_coords3,
    walsh_matrix_3, truth_to_walsh3, walsh_to_truth3,
    clifford_product_3, sweep_product3, closure_projection3,
    omega_phase3, omega_power3,
    coupling_summary, sierpinski_S, projective_plane_q2_count,
    boolean_gate_atlas, hexagon_projection_summary,
)

from .field_origin_dynamics import (
    AXIAL_MASKS, axial_projection, axial_components, non_axial_residue_norm,
    associator, associator_axial_readout,
    walsh_bridge_step, three_sweep_update,
    FieldOriginTick, run_field_origin_ticks,
    tet_a_axial_seed, tet_b_axial_seed, mixed_axial_seed,
    m1_walsh_inversion_error, m2_eisenstein_closure_error,
    m3_projector_idempotent_error, m4_associator_axial_residue,
    m5_axial_defect_magnitude,
    nine_metric_diagnostic_panel, diagnostic_panel_run_validity,
    showcase_field_origin_dynamics,
)

# ---------------------------------------------------------------------------
# Unification algebra (Walsh + Clifford + Eisenstein + cyclotomic spine)
# ---------------------------------------------------------------------------
from .unification_algebra import (
    UnificationAlgebra,
    uniqueness_equation_residual,
    vertex_count_uniqueness_check,
    expected_eigenspectrum_multiplicities,
    eigenspectrum_matches_binomial_row,
    eigenspectrum_uniqueness_check,
    phi_at_negative_K, phi_at_K_minus_1, phi_n_value,
    parity_shift_collapse_at_phi3,
    parity_shift_collapse_fails_for,
    parity_shift_uniqueness_check,
    k_scaling_trace_on_channel,
    coupling_polynomial_trace_check,
    three_factorizations_of_S_3_K,
    connection_split_from_coupling,
    discriminant_constraint_scan,
    range_equals_2K_equals_2D,
    three_uniqueness_routes_to_D3,
    pipeline_stages_summary,
    showcase_unification_algebra,
    # R-block — core constructive theorems (Part III of appendix G)
    orientation_cocycle, twisted_product, clifford_relations_check_3,
    omega_permute_mask, omega_order_check, omega_fixed_masks, omega_cycled_masks,
    omega_decomposition_check,
    gaussian_norm_Z_i, eisenstein_norm_Z_omega,
    coupling_polynomial_as_norm_trace_check,
    divisors_above_two, cyclotomic_value_for_divisor, S_D_K_divisor_formula,
    cl_3_0_grade_dimensions, cl_3_0_grade_check,
    ClosureAlgebraReading, boolean_function_through_pipeline,
    showcase_core_constructive_theorems,
)

# ---------------------------------------------------------------------------
# Coupling shells (parity-pushout recursion and K=1..K=5 family)
# ---------------------------------------------------------------------------
from .coupling_shells import (
    parity_pushout_step, parity_pushout_orbit, parity_pushout_closed_form,
    CouplingShell, SHELL_NAMES,
    coupling_shell, coupling_shell_family, coupling_shell_table,
    adjacent_shell_lock_check, adjacent_shell_lock_scan,
    discriminant_identity_squared,
    directed_simplex_edge_identity,
    projective_plane_general, projective_plane_identity_check,
    is_prime_power,
    ParityPushoutMorphism, parity_pushout_category,
    star_transition_K3_to_K4, portal_transition_K4_to_K5,
    showcase_coupling_shells,
)


# Tier 1 closures (modules added during the Tier 1 push)
from .cyclotomic_12 import (
    z12, z12_add, z12_sub, z12_mul, z12_pow, z12_one, z12_zeta,
    phi_12_at,
    verify_minimal_polynomial, verify_powers_of_zeta,
    cl_3_0_mul, cl_basis_1, cl_basis_T1, cl_basis_T2, cl_basis_I,
    closure_fixed_subalgebra_multiplication_table,
    verify_closure_fixed_multiplication_table,
    zeta_12_in_clifford, cl_pow, verify_zeta_12_powers_in_clifford,
    galois_units_mod_12, galois_action_on_zeta,
    quadratic_subfield_fixed_points, parity_tag_to_subfield,
    verify_galois_group_structure,
    gaussian_imaginary_unit_as_zeta, eisenstein_omega_as_zeta,
    verify_gaussian_in_zeta12, verify_eisenstein_in_zeta12,
    divisors_above_two_of_12, divisors_above_two_of_2D,
    phi_n_value_extended, compositum_12_closure_tower,
    omega_action_on_clifford, is_omega_fixed,
    sweep_multiplication_on_omega_fixed,
    showcase_cyclotomic_12,
)

from .gfd_oscillator_jacobian import (
    s_4_cyclic_permutation, s_4_transposition, z_2_swap_TetA_TetB,
    build_jacobian,
    verify_jacobian_commutes_with_S4_cyclic,
    verify_jacobian_commutes_with_S4_transposition,
    verify_jacobian_commutes_with_Z2_swap,
    verify_full_S4_Z2_symmetry,
    jacobian_eigenvalues_and_multiplicities,
    verify_eigenspectrum_1_D_D_1,
    walsh_matrix_8, jacobian_in_walsh_basis, is_walsh_diagonal,
    showcase_gfd_oscillator_jacobian,
)

from .fine_structure_hierarchy import (
    multiplicative_order, ord_137_of_4,
    splits_in_Z_i, splits_in_Z_omega, splits_in_Z_zeta_12,
    splitting_summary,
    cyclotomic_value, divides_phi_d_K,
    first_phi_dividing_137, locate_137_in_hierarchy,
    is_prime_simple,
    alpha_inv_predicted, alpha_inv_residual, ALPHA_INV_CODATA,
    twenty_eight_structural_reading,
    showcase_fine_structure_hierarchy,
)

from .mirror_match_distribution import (
    random_unit_vector, random_shaft_keys, random_address, mirror_pair,
    DistributionStats,
    sample_mirror_match_distribution, sample_designed_mirror_pairs,
    chirality_gate, phase_gate, gram_gate,
    gate_decomposition_stats, tolerance_sweep,
    showcase_mirror_match_distribution,
)

from .mass_from_associator import (
    clifford_associator, sweep_associator, sweep_product, omega_on_clifford,
    AXIAL_MASKS_FIXED, axial_projector_8, axial_component,
    axial_residue_norm, non_axial_residue_norm_fixed,
    tet_a_axial_seed, tet_b_axial_seed, bridge_seed,
    hexagonal_eisenstein_seed,
    axial_residue_for_structured_triple,
    axial_residue_for_hexagonal_triple,
    MassResidueResult, mass_from_associator_residue,
    showcase_mass_from_associator,
)

from .vortex_calibration import (
    continuous_eisenstein_rotation, continuous_omega_rotation,
    sector_norms, CycleTrace, run_closure_cycle,
    VoteResult, compute_votes, compute_impedance,
    make_test_state, make_axial_only_state, make_mixed_test_state,
    sweep_v_read, showcase_vortex_calibration,
)

from .pyramid_resonance import (
    ROYAL_CUBIT_M, KC_L_CUBITS, KC_W_CUBITS, KC_H_CUBITS,
    V_AIR, V_GRANITE_P, V_GRANITE_S,
    Mode, enumerate_modes, lowest_modes,
    kc_dimensions_m, kc_space_diagonal_squared_cubits,
    kc_space_diagonal_cubits, verify_kc_K_squared_identity,
    cyclotomic_sector, omega_orbit, sector_distribution_audit,
    FrequencyPrediction, predict_21_mode_comb,
    vortex_omega_for_chamber, vortex_frequency_for_apparatus,
    bare_K4_K5_transition_bracket,
    showcase_pyramid_resonance,
)

from .chamber_polarization import (
    OMEGA, unit_k_vector, polarization_zeta,
    axial_weight, hexagonal_weight, polarization_sector,
    PolarizationInfo, polarization_info, polarization_audit,
    antechamber_filter, SpectrumEntry, predict_filtered_spectrum,
    transverse_basis, omega_rotation_matrix_3d,
    transverse_omega_action, transverse_purity,
    transverse_omega_eigenvalues, TransverseInfo, transverse_info,
    showcase_chamber_polarization,
)

from .kc_kinematics import (
    OMEGA_EARTH, GIZA_LATITUDE_DEG, OMEGA_EARTH_VERTICAL,
    k_vector_magnitude_m_inv,
    mode_wavelength_m, mode_period_s,
    mode_angular_frequency_rad_per_s, mode_phase_velocity_m_per_s,
    axis_roundtrip_time_s, all_axis_roundtrips,
    BeatEntry, adjacent_mode_beats,
    mode_circulation_m2_per_s,
    coriolis_split_rad_per_s, coriolis_split_hz,
    sagnac_phase_per_roundtrip_rad,
    KinematicEntry, mode_kinematics, all_modes_kinematics,
    showcase_kc_kinematics,
)

from .chamber_impedance_hierarchy import (
    PHI_4_AT_K4, K_FACES, SO_VERTICES, DIM_SPACE,
    IMP_GLOBAL, IMP_LOCAL, IMP_ROTATIONAL,
    TROPICAL_YEAR_DAYS, GIZA_LATITUDE_OBSERVED_DEG,
    predicted_year_days, year_match,
    vertex_impedance,
    predicted_coriolis_stretch,
    predicted_coriolis_latitude_deg,
    predicted_coriolis_period_s, predicted_coriolis_period_hours,
    coriolis_at_giza_period_s, coriolis_match,
    latitude_for_D, giza_offset_for_D,
    D_uniqueness_audit, D_minimizing_giza_offset,
    HierarchyResult, hierarchy_audit,
    showcase_chamber_impedance_hierarchy,
)

from .giza_three_pyramid_scaling import (
    KHUFU_BASE_M, KHAFRE_BASE_M, MENKAURE_BASE_M,
    predicted_khafre_ratio, predicted_menkaure_ratio,
    predicted_menkaure_khafre_ratio,
    observed_khafre_ratio, observed_menkaure_ratio,
    observed_menkaure_khafre_ratio,
    RatioMatch, all_audits as giza_scaling_audits,
    hierarchy_match_within_uncertainty,
    showcase_three_pyramid_scaling,
)


__all__ = [
    # constants
    "ALPHA", "G_E_OVER_2", "HBAR", "C_LIGHT", "M_E", "G_OBSERVED", "TAU",
    # cyclotomic
    "phi3", "phi4", "phi6", "coupling_polynomial", "Shell", "shell",
    "shift_identity", "scale_fusion_identity", "sphere_surface_area_unit",
    "niven_rigidity_check", "norm_form", "cyclotomic_integer_norm",
    "niven_partition_table",
    # closure_read
    "Matrix", "diag", "matmul", "matrix_equal", "shell_hamiltonian",
    "truncated_tensor_algebra", "parity_projector_dimensions",
    "graded_identity_trace", "gram_matrix_K", "gram_eigenvalues",
    "parity_overlap_angle", "sec_theta_K", "verify_17_over_13_is_sec_theta_4",
    "hilbert_polynomial",
    "parity_sheet_inclusion_exclusion", "parity_sheet_dot_products",
    "parity_overlap_angle_geometric",
    # hinge
    "PyramidHinge", "pyramid_k4_k5_hinge", "j4_partial_isometry",
    "interlevel_intertwiner_check", "k5_band_assignment",
    "sub_tetrahedron_count", "s5_supset_s4_branching",
    "hinge_sub_tetrahedron_decomposition",
    # gravity
    "directed_complete_graph_edge_count", "pentachoron_directed_edge_count",
    "pentachoron_edge_product", "edge_phase_closure", "tetrad_impedance_ratio",
    "alpha_gravity", "alpha_gravity_parts", "coupling_exponent_for_K",
    "gravity_over_coulomb_gap_exponent", "tetrad_renormalization_factor",
    "alpha_G_for_K", "predict_G_from_alpha", "G_prediction_report",
    "four_routes_select_K4", "permutation_discrimination", "best_permutation",
    # mu_partition
    "mu", "tetA_share", "tetB_share", "odds_ratio", "mu_derivative",
    "logistic_identity_check", "born_rule_map", "inverse_born_rule",
    "x_from_theta", "partition_to_x", "x_to_partition",
    "niven_partition_points", "mond_transition_check",
    "sst_quadratic", "sst_static_solve_g",
    # electromagnetism
    "vv_decomposition", "tetrahedral_edges", "time_space_edges",
    "space_space_edges", "F_mu_nu_basis", "perfect_matchings_K4",
    "opposite_edge_pairs_K4", "self_dual_part", "anti_self_dual_part",
    "self_dual_anti_self_dual_decomposition", "hodge_star_squared_lorentzian",
    "dirac_quantization_check", "coulomb_step", "gravity_as_21_coulomb_steps",
    # apparatus
    "Vector3", "dot", "norm", "normalize", "gram_matrix", "determinant_3",
    "chirality", "phase_closed", "KingsChamberVertex", "kings_chamber_vertex",
    "portal_scalar_amplitude", "ShaftKey", "triadic_phase", "Address",
    "make_address", "permute_gram", "gram_distance", "mirror_match_functional",
    "apex_top_collector", "granite_isolation", "ascending_passage_gain",
    "grand_gallery_z7_kernel", "z3_projector_eigenvalue", "z21_phase_sectors",
    "z21_comb_frequencies", "big_void_balance_cavity",
    "coffer_reflection_coefficient", "KQInterferometer", "kq_phase_lock",
    "z21_order_parameter", "landau_z21_potential", "josephson_portal_current",
    "PortalMachine", "local_force_kernel", "portal_address_kernel",
    "reciprocal_two_apparatus_operator_scalar", "apparatus_operator_stack",
    "complement_projector_mode", "well_shaft_feedback",
    # topology
    "Quaternion", "q_normalize", "q_conjugate", "q_multiply",
    "hopf_projection", "hopf_fiber_phase", "electron_hopf_fiber_holonomy",
    "alternating_group_A5_order", "pentachoron_cell_count",
    "a5_address_sector_count", "crystallographic_threshold_pentachoron",
    "null_cone_associator_status",
    "wrt_su2_level_to_k_plus_2", "wrt_central_charge",
    "wrt_su2_19_chern_simons", "wrt_invariant_sigma235_target",
    # predictions
    "coffer_chamber_alpha_step", "relieving_chamber_volume_prediction",
    "sierpinski_force_hierarchy", "k2_schwinger_loop_structure",
    "lepton_anchor_report", "golden_impedance_split",
    # curvature_decomposition
    "CurvatureSector",
    "levi_civita_sector", "torsion_sector", "parity_overlap_sector",
    "hinge_sector", "associator_sector", "mirror_address_sector",
    "master_decomposition", "sector_table",
    "gr_projector", "gr_visible_sectors", "gr_killed_sectors",
    "gr_averaged_sectors", "gr_renormalized_sectors",
    "framework_gravitational_coupling_report",
    "einstein_projection_summary",
    "showcase_integration",
    "curvature_consistency_check",
    # portal_resonance
    "CrossSheetCoherence", "cross_sheet_order_parameter",
    "vacuum_cross_sheet", "kings_chamber_cross_sheet",
    "z21_landau_psi", "z21_lock_minima", "z21_lock_strength",
    "FieldOriginVertex", "kings_chamber_vertex_compact",
    "field_origin_vertex_equation",
    "six_matching_conditions", "algebraic_match_count",
    "lock_strength_factor", "effective_coupling",
    "RelievingChamberSelector", "relieving_chamber_selector",
    "five_chamber_decomposition_info",
    "portal_resonance_lorentzian", "effective_linewidth",
    "field_origin_summary", "showcase_portal_resonance",
    # closure_core256
    "ClosureNode3", "SierpinskiTile64", "ClosureCore256",
    "ClosureCoords3", "to_closure_coords3",
    "walsh_matrix_3", "truth_to_walsh3", "walsh_to_truth3",
    "clifford_product_3", "sweep_product3", "closure_projection3",
    "omega_phase3", "omega_power3",
    "coupling_summary", "sierpinski_S", "projective_plane_q2_count",
    "boolean_gate_atlas", "hexagon_projection_summary",
    # field_origin_dynamics (bridge)
    "AXIAL_MASKS", "axial_projection", "axial_components", "non_axial_residue_norm",
    "associator", "associator_axial_readout",
    "walsh_bridge_step", "three_sweep_update",
    "FieldOriginTick", "run_field_origin_ticks",
    "tet_a_axial_seed", "tet_b_axial_seed", "mixed_axial_seed",
    "m1_walsh_inversion_error", "m2_eisenstein_closure_error",
    "m3_projector_idempotent_error", "m4_associator_axial_residue",
    "m5_axial_defect_magnitude",
    "nine_metric_diagnostic_panel", "diagnostic_panel_run_validity",
    "showcase_field_origin_dynamics",
    # unification_algebra
    "UnificationAlgebra",
    "uniqueness_equation_residual", "vertex_count_uniqueness_check",
    "expected_eigenspectrum_multiplicities",
    "eigenspectrum_matches_binomial_row", "eigenspectrum_uniqueness_check",
    "phi_at_negative_K", "phi_at_K_minus_1", "phi_n_value",
    "parity_shift_collapse_at_phi3", "parity_shift_collapse_fails_for",
    "parity_shift_uniqueness_check",
    "k_scaling_trace_on_channel", "coupling_polynomial_trace_check",
    "three_factorizations_of_S_3_K", "connection_split_from_coupling",
    "discriminant_constraint_scan", "range_equals_2K_equals_2D",
    "three_uniqueness_routes_to_D3", "pipeline_stages_summary",
    "showcase_unification_algebra",
    # R-block — core constructive theorems
    "orientation_cocycle", "twisted_product", "clifford_relations_check_3",
    "omega_permute_mask", "omega_order_check", "omega_fixed_masks", "omega_cycled_masks",
    "omega_decomposition_check",
    "gaussian_norm_Z_i", "eisenstein_norm_Z_omega",
    "coupling_polynomial_as_norm_trace_check",
    "divisors_above_two", "cyclotomic_value_for_divisor", "S_D_K_divisor_formula",
    "cl_3_0_grade_dimensions", "cl_3_0_grade_check",
    "ClosureAlgebraReading", "boolean_function_through_pipeline",
    "showcase_core_constructive_theorems",
    # coupling_shells
    "parity_pushout_step", "parity_pushout_orbit", "parity_pushout_closed_form",
    "CouplingShell", "SHELL_NAMES",
    "coupling_shell", "coupling_shell_family", "coupling_shell_table",
    "adjacent_shell_lock_check", "adjacent_shell_lock_scan",
    "discriminant_identity_squared", "directed_simplex_edge_identity",
    "projective_plane_general", "projective_plane_identity_check",
    "is_prime_power",
    "ParityPushoutMorphism", "parity_pushout_category",
    "star_transition_K3_to_K4", "portal_transition_K4_to_K5",
    "showcase_coupling_shells",
]
