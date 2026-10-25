#!/usr/bin/env python3
"""
demo.py
=======

Runnable end-to-end demonstration of the GFD / pyramid-portal algebra package.

Walks through all current modules, printing key results from each:
hinge identities, alpha_G derivation, apparatus operators, address structures,
order parameters, and predictions.

Run from the project root:

    python -m pyramid_portal_research.python.demo

or, with the project python directory on sys.path:

    python python/demo.py
"""

from __future__ import annotations

from math import pi

# Handle both package-relative and direct-script invocation
try:
    from . import (
        # cyclotomic
        phi3,
        # hinge
        pyramid_k4_k5_hinge, interlevel_intertwiner_check, k5_band_assignment,
        # gravity
        pentachoron_directed_edge_count, alpha_gravity_parts,
        pentachoron_edge_product, G_prediction_report, four_routes_select_K4,
        # apparatus
        kings_chamber_vertex, ShaftKey, make_address, mirror_match_functional,
        portal_scalar_amplitude, apex_top_collector, granite_isolation,
        ascending_passage_gain, grand_gallery_z7_kernel, z3_projector_eigenvalue,
        z21_phase_sectors, z21_comb_frequencies, KQInterferometer,
        kq_phase_lock, z21_order_parameter, landau_z21_potential,
        josephson_portal_current, PortalMachine, local_force_kernel,
        portal_address_kernel, alpha_gravity, reciprocal_two_apparatus_operator_scalar,
        apparatus_operator_stack, complement_projector_mode, well_shaft_feedback,
        # topology
        q_normalize, hopf_projection, electron_hopf_fiber_holonomy,
        alternating_group_A5_order, pentachoron_cell_count,
        a5_address_sector_count, crystallographic_threshold_pentachoron,
        null_cone_associator_status,
        # predictions
        coffer_chamber_alpha_step, relieving_chamber_volume_prediction,
        sierpinski_force_hierarchy, k2_schwinger_loop_structure,
        golden_impedance_split,
    )
except ImportError:
    # direct script invocation: add parent of this file to sys.path
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from python import (  # type: ignore  # noqa: E402
        phi3,
        pyramid_k4_k5_hinge, interlevel_intertwiner_check, k5_band_assignment,
        pentachoron_directed_edge_count, alpha_gravity_parts,
        pentachoron_edge_product, G_prediction_report, four_routes_select_K4,
        kings_chamber_vertex, ShaftKey, make_address, mirror_match_functional,
        portal_scalar_amplitude, apex_top_collector, granite_isolation,
        ascending_passage_gain, grand_gallery_z7_kernel, z3_projector_eigenvalue,
        z21_phase_sectors, z21_comb_frequencies, KQInterferometer,
        kq_phase_lock, z21_order_parameter, landau_z21_potential,
        josephson_portal_current, PortalMachine, local_force_kernel,
        portal_address_kernel, alpha_gravity, reciprocal_two_apparatus_operator_scalar,
        apparatus_operator_stack, complement_projector_mode, well_shaft_feedback,
        q_normalize, hopf_projection, electron_hopf_fiber_holonomy,
        alternating_group_A5_order, pentachoron_cell_count,
        a5_address_sector_count, crystallographic_threshold_pentachoron,
        null_cone_associator_status,
        coffer_chamber_alpha_step, relieving_chamber_volume_prediction,
        sierpinski_force_hierarchy, k2_schwinger_loop_structure,
        golden_impedance_split,
    )


def print_section(title: str) -> None:
    print("\n" + "=" * 96)
    print(title)
    print("=" * 96)


def demo_k4_k5_hinge() -> None:
    print_section("1. K=4 -> K=5 cyclotomic hinge")
    hinge = pyramid_k4_k5_hinge()
    print("K=4 shell:", hinge.source_shell.tuple)
    print("K=5 shell:", hinge.receiver_shell.tuple)
    print("Shared band:", hinge.shared_band)
    print("Identity:", hinge.statement, "holds=", hinge.identity_holds)
    print("Intertwiner H5 J4 = J4 H4:", interlevel_intertwiner_check()["holds"])


def demo_coulomb_edge_network() -> None:
    print_section("2. Coulomb edge network and alpha_G")
    print("Pentachoron directed edges:", pentachoron_directed_edge_count())
    print("Phi_3(4)-1:", phi3(4) - 1)
    print("Directed edge count identity:", phi3(4) - 1 == pentachoron_directed_edge_count())

    parts = alpha_gravity_parts()
    for k, v in parts.items():
        print(f"{k}: {v:.16e}")

    product_zero_phase = pentachoron_edge_product()
    print(f"pentachoron_edge_product(zero phase): {product_zero_phase.real:.16e}")


def demo_vertex_and_bands() -> None:
    print_section("3. King's Chamber vertex and K=5 bands")
    print(kings_chamber_vertex().as_string())
    print("K=5 band assignment:")
    for name, info in k5_band_assignment().items():
        print(f"  {name}: {info}")


def demo_address_and_mirror() -> None:
    print_section("4. Shaft address and mirror selector")
    source_keys = [
        ShaftKey(direction=(1, 0, 0), length=0, impedance=1, omega=1, phase=0, band=21),
        ShaftKey(direction=(0, 1, 0), length=0, impedance=1, omega=1, phase=0, band=21),
        ShaftKey(direction=(0, 0, 1), length=0, impedance=1, omega=1, phase=0, band=21),
    ]
    target_keys = [
        ShaftKey(direction=(1, 0, 0), length=0, impedance=1, omega=1, phase=0, band=21),
        ShaftKey(direction=(0, 1, 0), length=0, impedance=1, omega=1, phase=0, band=21),
        ShaftKey(direction=(0, 0, -1), length=0, impedance=1, omega=1, phase=0, band=21),
    ]
    src = make_address(source_keys)
    tgt = make_address(target_keys)
    M = mirror_match_functional(src, tgt)
    print("Source Gram:", src.gram)
    print("Target Gram:", tgt.gram)
    print("Source chirality:", src.chirality)
    print("Target chirality:", tgt.chirality)
    print("Mirror selector M:", M)
    print("Portal scalar alpha_G*M:", portal_scalar_amplitude(M))


def demo_internal_subsystems() -> None:
    print_section("5. Internal subsystem operators")
    print("Apex collector sample:", apex_top_collector(env_flux_derivative=10, capacitance=2, eta=0.5))
    print("Granite isolation sample:", granite_isolation(leak_gamma=0.2, wall_length=10))
    print("Ascending passage gain sample:", ascending_passage_gain(gamma=0.01, length=100, phase_k=0.1))
    print("Grand Gallery Z7 k=0..6:", grand_gallery_z7_kernel(index_from_zero=True))
    print("Grand Gallery Z7 k=1..7:", grand_gallery_z7_kernel(index_from_zero=False))
    print("Z3 projector eigenvalues m=0,1,2:", [z3_projector_eigenvalue(m) for m in range(3)])
    print("Z21 sectors:", len(z21_phase_sectors()))
    print("First five ideal comb freqs for f0=110 Hz:", [round(f, 4) for f in z21_comb_frequencies(110)[:5]])


def demo_kq_hopf_a5() -> None:
    print_section("6. K/Q interferometer, Hopf projection, A5 address")
    king_keys = [
        ShaftKey(direction=(1, 0, 0), length=1, impedance=1, omega=0, phase=0.1, band=21),
        ShaftKey(direction=(0, 1, 0), length=1, impedance=1, omega=0, phase=0.2, band=21),
        ShaftKey(direction=(0, 0, 1), length=1, impedance=1, omega=0, phase=0.3, band=21),
    ]
    queen_keys = [
        ShaftKey(direction=(1, 0, 0), length=1, impedance=1, omega=0, phase=0.05, band=26),
        ShaftKey(direction=(0, 1, 0), length=1, impedance=1, omega=0, phase=0.10, band=26),
        ShaftKey(direction=(0, 0, 1), length=1, impedance=1, omega=0, phase=0.15, band=26),
    ]
    kq = KQInterferometer(make_address(king_keys), make_address(queen_keys))
    print("K/Q address phase:", kq.address_phase)
    print("K/Q phase lock against target 0.3:", kq_phase_lock(kq, target_phase=0.3, tolerance=1e-9))

    q = q_normalize((1, 1, 0, 0))
    print("Hopf projection of q=(1,1,0,0):", tuple(round(x, 6) for x in hopf_projection(q)))
    print("electron Hopf fiber holonomy g_e/2:", electron_hopf_fiber_holonomy())
    print("A5 order:", alternating_group_A5_order())
    print("Pentachoron tetrahedral cells:", pentachoron_cell_count())
    print("A5 x Z21 discrete sectors:", a5_address_sector_count())


def demo_order_and_coffer() -> None:
    print_section("7. Universal vertex order parameter and coffer alpha step")
    locked = z21_order_parameter([0, 0, 0, 0])
    mixed = z21_order_parameter([0, 0.1, 0.7, 1.3, 2.0])
    print("|Omega_21 locked|:", abs(locked))
    print("|Omega_21 mixed|:", abs(mixed))
    print("Landau V sample:", landau_z21_potential(rho=1, theta=0, a=1, b=0.1, h21=0.05))
    print("Josephson current sample:", josephson_portal_current(Ic=1, theta_x=0, theta_y=0.01, address_holonomy=0))

    coffer = coffer_chamber_alpha_step()
    print("Coffer/chamber alpha step:")
    for k, v in coffer.items():
        print(f"  {k}: {v:.12g}")
    print("Relieving chamber total volume prediction:", relieving_chamber_volume_prediction())


def demo_portal_machine() -> None:
    print_section("8. Full portal machine scalar comparison")
    alphaG = alpha_gravity()
    M_good = 1.0
    M_bad = 0.0
    machine_good = PortalMachine(alpha_G=alphaG, mirror_selector=M_good)
    machine_bad = PortalMachine(alpha_G=alphaG, mirror_selector=M_bad)

    print("Local force kernel alpha_G/r at r=10:", local_force_kernel(alphaG, r=10))
    print("Portal address kernel alpha_G*M, M=1:", portal_address_kernel(alphaG, M_good))
    print("Portal address kernel alpha_G*M, M=0:", portal_address_kernel(alphaG, M_bad))
    print("PortalMachine amplitude M=1:", machine_good.amplitude)
    print("PortalMachine amplitude M=0:", machine_bad.amplitude)


def demo_recovered_blocks() -> None:
    print_section("9. Recovered algebra blocks")

    print("\nCrystallographic / S5 pentachoron threshold:")
    for k, v in crystallographic_threshold_pentachoron().items():
        print(f"  {k}: {v}")

    print("\nSierpinski force hierarchy:")
    for row in sierpinski_force_hierarchy():
        print(" ", row)

    print("\nK=2 -> Schwinger 2π structure:")
    for k, v in k2_schwinger_loop_structure().items():
        print(f"  {k}: {v}")

    print("\nG prediction report:")
    for k, v in G_prediction_report().items():
        print(f"  {k}: {v:.12g}")

    print("\nFour routes selecting K=4:")
    for route in four_routes_select_K4():
        print(" ", route)

    print("\nReciprocal apparatus scalar test:")
    source_gain = apparatus_operator_stack(
        top=1,
        asc=1,
        plug_iso=1,
        gallery=grand_gallery_z7_kernel()["determinant_phase"],
        z3_gate=z3_projector_eigenvalue(0),
        coffer_load=1,
        granite=1,
        kc_vertex=1,
    )
    receiver_gain = source_gain
    print("  source_gain:", source_gain)
    print("  transfer:", reciprocal_two_apparatus_operator_scalar(source_gain, receiver_gain, mirror_selector=1.0))

    print("\nComplement projector / failed-lock sink:")
    print(" ", complement_projector_mode(selected_21_component=0.72))

    print("\nWell shaft feedback:")
    print(" ", well_shaft_feedback(beta=0.1, theta=pi / 3))

    print("\nNull-cone associator status:")
    for k, v in null_cone_associator_status().items():
        print(f"  {k}: {v}")

    print("\nGolden impedance split:")
    for k, v in golden_impedance_split().items():
        print(f"  {k}: {v}")


def main() -> None:
    print_section("Great Pyramid Portal Algebra — Modular Package Demonstration")
    print("End-to-end walkthrough of all currently-implemented modules.")
    demo_k4_k5_hinge()
    demo_coulomb_edge_network()
    demo_vertex_and_bands()
    demo_address_and_mirror()
    demo_internal_subsystems()
    demo_kq_hopf_a5()
    demo_order_and_coffer()
    demo_portal_machine()
    demo_recovered_blocks()
    print_section("Done")
    print("Use the individual modules to explore the framework algebraically.")


if __name__ == "__main__":
    main()
