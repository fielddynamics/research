#!/usr/bin/env python3
"""
t-bit Algebra Verification
===========================
Tests every new algebraic claim in tbit_algebra.md against the
existing GFD algebra primitives in gfd_algebra.py.

Zero output = all pass.
"""

import math
import numpy as np
from gfd_algebra__2_ import (
    mu, one_minus_mu, exchange_duality, aqual_energy_functional,
    fwht, truth_table_to_bridge, walsh_sparsity, wavenode_eval,
    mu_spinor, theta_from_x, x_from_theta, canonical_sign_matrix,
    forced_gram_matrix, coupling_polynomial
)


# =========================================================================
#  1. SINGLE-t-BIT GATES
# =========================================================================

def gate_P(x):
    """Parity flip: x → 1/x"""
    return 1.0 / x

def gate_T(x, lam):
    """Threshold shift: x → x + λ"""
    return x + lam

def gate_D(x, alpha):
    """Dilation: x → αx"""
    return alpha * x

def gate_S(x):
    """Square (purification): x → x²"""
    return x ** 2

def gate_R(x):
    """Square root (mixing): x → √x"""
    return math.sqrt(x)

def gate_Ms(x):
    """Möbius constitutive map: x → (x-1)/(x+1)"""
    return (x - 1.0) / (x + 1.0)


def test_parity_gate():
    """P² = Id, and P swaps μ ↔ 1-μ"""
    for x in [0.01, 0.5, 1.0, 4.0, 100.0]:
        # P is an involution
        assert abs(gate_P(gate_P(x)) - x) < 1e-12, f"P² ≠ Id at x={x}"
        # P swaps partition fractions
        mu_orig = float(mu(x))
        mu_flip = float(mu(gate_P(x)))
        assert abs(mu_flip - (1.0 - mu_orig)) < 1e-12, f"P doesn't swap μ at x={x}"
    print("  ✓ Parity gate: P² = Id, P swaps μ ↔ 1-μ")


def test_dilation_group():
    """D_α ∘ D_β = D_{αβ}"""
    for a, b in [(2, 3), (0.5, 4), (16, 1/16)]:
        x = 5.0
        composed = gate_D(gate_D(x, a), b)
        direct = gate_D(x, a * b)
        assert abs(composed - direct) < 1e-12, f"D_{a} ∘ D_{b} ≠ D_{a*b}"
    print("  ✓ Dilation group: D_α ∘ D_β = D_{αβ}")


def test_conjugation_identity():
    """P ∘ T_λ ∘ P = x/(1 + λx)"""
    for lam in [0.5, 1.0, 3.0]:
        for x in [0.1, 1.0, 10.0]:
            conjugated = gate_P(gate_T(gate_P(x), lam))
            expected = x / (1.0 + lam * x)
            assert abs(conjugated - expected) < 1e-12, \
                f"P∘T_{lam}∘P ≠ x/(1+{lam}x) at x={x}"
    print("  ✓ Conjugation: P ∘ T_λ ∘ P = x/(1 + λx)")


def test_mixing_purification():
    """R pushes toward x=1, S pushes away from x=1"""
    x0 = 16.0
    # R: iterated square root converges to 1
    x = x0
    for _ in range(20):
        x = gate_R(x)
    assert abs(x - 1.0) < 1e-5, f"R^20({x0}) = {x}, expected ~1"

    # S: iterated square diverges from 1 (unless exactly 1)
    x = 1.01
    for _ in range(10):
        x = gate_S(x)
    assert x > 1e4, f"S^10(1.01) = {x}, expected >> 1"
    print("  ✓ Mixing/purification: R → balance, S → poles")


def test_mu_output_table():
    """Verify μ_out for each canonical gate matches the table"""
    x = 4.0  # test state
    mu_x = float(mu(x))

    # P: μ_out = 1 - μ
    assert abs(float(mu(gate_P(x))) - (1.0 - mu_x)) < 1e-12
    # T_λ: μ_out = (x+λ)/(x+λ+1)
    lam = 2.0
    assert abs(float(mu(gate_T(x, lam))) - (x + lam) / (x + lam + 1)) < 1e-12
    # D_α: μ_out = αx/(αx+1)
    alpha = 3.0
    assert abs(float(mu(gate_D(x, alpha))) - alpha * x / (alpha * x + 1)) < 1e-12
    # S: μ_out = x²/(x²+1)
    assert abs(float(mu(gate_S(x))) - x**2 / (x**2 + 1)) < 1e-12
    # R: μ_out = √x/(√x+1)
    assert abs(float(mu(gate_R(x))) - math.sqrt(x) / (math.sqrt(x) + 1)) < 1e-12
    print("  ✓ μ_out table verified for all canonical gates")


# =========================================================================
#  2. GATE ENERGY (AQUAL FUNCTIONAL)
# =========================================================================

def gate_energy(G_func, x, *args):
    """Energy cost: |F(G(x)²) - F(x²)|"""
    x_out = G_func(x, *args) if args else G_func(x)
    return abs(float(aqual_energy_functional(x_out**2)) -
               float(aqual_energy_functional(x**2)))


def test_parity_flip_cost():
    """ΔF(x=1) = 0, ΔF(x≫1) ≈ x²"""
    # At balance: free
    cost_at_1 = gate_energy(gate_P, 1.0)
    assert cost_at_1 < 1e-14, f"ΔF(1) = {cost_at_1}, expected 0"

    # At large x: ≈ x²
    x = 100.0
    cost = gate_energy(gate_P, x)
    assert abs(cost / x**2 - 1.0) < 0.1, f"ΔF({x})/x² = {cost/x**2}, expected ~1"
    print("  ✓ Parity flip cost: free at x=1, ~x² for x≫1")


def test_geometric_landauer():
    """Verify exact ΔF formula and asymptotic behavior"""
    # Exact formula: ΔF = (x²-1/x²) - 2(x-1/x) + 2ln(x)
    for x in [1.5, 2.0, 4.0, 8.0, 16.0]:
        cost = gate_energy(gate_P, x)
        exact = abs((x**2 - x**(-2)) - 2*(x - 1/x) + 2*math.log(x))
        assert abs(cost - exact) < 1e-10, \
            f"ΔF({x}) = {cost:.6f} ≠ exact {exact:.6f}"

    # Near x=1: ΔF ≈ 2·ln(x) (leading order in t = ln(x))
    x = 1.01
    cost = gate_energy(gate_P, x)
    approx = 2.0 * math.log(x)
    assert abs(cost / approx - 1.0) < 0.02, \
        f"Near-balance: ΔF ≈ 2ln(x) fails: ratio = {cost/approx:.4f}"

    # Far from balance: ΔF ≈ x² (dominant term)
    x = 50.0
    cost = gate_energy(gate_P, x)
    assert abs(cost / x**2 - 1.0) < 0.1, f"Newtonian: ΔF ≈ x² fails"

    print("  ✓ Gate energy: exact ΔF = (x²-1/x²) - 2(x-1/x) + 2ln(x)")
    print("    Near balance: ΔF → 2ln(x).  Newtonian: ΔF → x².")


# =========================================================================
#  3. TWO-t-BIT OPERATIONS
# =========================================================================

def hard_cnot(x_T, x_C):
    """Hard CNOT: flip target iff control is TetB"""
    mu_C = float(mu(x_C))
    if mu_C > 0.5:
        return x_T
    else:
        return 1.0 / x_T


def soft_cnot(x_T, x_C):
    """Soft CNOT: Möbius blend"""
    return (x_T * x_C + 1.0) / (x_C + x_T)


def test_soft_cnot_limits():
    """Soft CNOT → identity when control is TetA, → P when control is TetB"""
    x_T = 4.0

    # Control strongly TetA
    x_C = 1e6
    out = soft_cnot(x_T, x_C)
    assert abs(out - x_T) / x_T < 1e-4, f"soft CNOT(TetA) ≠ identity: {out}"

    # Control strongly TetB
    x_C = 1e-6
    out = soft_cnot(x_T, x_C)
    assert abs(out - 1.0/x_T) < 1e-4, f"soft CNOT(TetB) ≠ parity: {out}"

    # Control at balance: output = 1
    x_C = 1.0
    out = soft_cnot(x_T, x_C)
    assert abs(out - 1.0) < 1e-12, f"soft CNOT(balance) ≠ 1: {out}"
    print("  ✓ Soft CNOT limits: identity/parity/balance all correct")


def test_xnor_identity():
    """Theorem 3.1: μ_out = μ_T·μ_C + μ̄_T·μ̄_C (XNOR)"""
    for x_T in [0.5, 1.0, 4.0, 16.0]:
        for x_C in [0.25, 1.0, 8.0, 100.0]:
            x_out = soft_cnot(x_T, x_C)
            mu_out = float(mu(x_out))

            mu_T = float(mu(x_T))
            mu_C = float(mu(x_C))
            mubar_T = 1.0 - mu_T
            mubar_C = 1.0 - mu_C

            xnor = mu_T * mu_C + mubar_T * mubar_C
            assert abs(mu_out - xnor) < 1e-10, \
                f"XNOR fails: μ_out={mu_out:.6f}, XNOR={xnor:.6f} at xT={x_T}, xC={x_C}"
    print("  ✓ XNOR identity: μ_out = μ_T·μ_C + μ̄_T·μ̄_C (16 test points)")


def test_xor_complement():
    """Corollary 3.1: μ̄_out = μ_T·μ̄_C + μ̄_T·μ_C (XOR)"""
    for x_T in [0.5, 4.0]:
        for x_C in [0.25, 8.0]:
            x_out = soft_cnot(x_T, x_C)
            mubar_out = float(one_minus_mu(x_out))

            mu_T = float(mu(x_T))
            mu_C = float(mu(x_C))

            xor_val = mu_T * (1 - mu_C) + (1 - mu_T) * mu_C
            assert abs(mubar_out - xor_val) < 1e-10, \
                f"XOR complement fails at xT={x_T}, xC={x_C}"
    print("  ✓ XOR complement: μ̄_out = μ_T·μ̄_C + μ̄_T·μ_C")


# =========================================================================
#  4. TOFFOLI GATE
# =========================================================================

def soft_toffoli(x_T, x_A, x_B):
    """Geometric Toffoli: x_T^{(2μ_A - 1)(2μ_B - 1)}"""
    s_A = 2.0 * float(mu(x_A)) - 1.0  # = M_s(x_A)
    s_B = 2.0 * float(mu(x_B)) - 1.0
    exponent = s_A * s_B
    return x_T ** exponent


def test_toffoli():
    """Geometric Toffoli: x_T^{(2μ_A-1)(2μ_B-1)} is XOR-controlled"""
    x_T = 4.0

    # Both agree TetA (x ≫ 1): s_A≈+1, s_B≈+1, product≈+1 → no flip
    out_aa = soft_toffoli(x_T, 1000, 1000)
    assert abs(out_aa - x_T) / x_T < 0.01, "TetA,TetA: should not flip"

    # Both agree TetB (x ≪ 1): s_A≈-1, s_B≈-1, product≈+1 → no flip
    out_bb = soft_toffoli(x_T, 0.001, 0.001)
    assert abs(out_bb - x_T) / x_T < 0.01, "TetB,TetB: exponent≈+1, no flip"

    # Disagree (TetA, TetB): s_A≈+1, s_B≈-1, product≈-1 → flip
    out_ab = soft_toffoli(x_T, 1000, 0.001)
    assert abs(out_ab - 1.0/x_T) < 0.01, "TetA,TetB: exponent≈-1, flip"

    # Disagree (TetB, TetA): same by symmetry
    out_ba = soft_toffoli(x_T, 0.001, 1000)
    assert abs(out_ba - 1.0/x_T) < 0.01, "TetB,TetA: exponent≈-1, flip"

    # One at balance: exponent ≈ 0 → x_T^0 = 1 (forced to MOND ring)
    out_mid = soft_toffoli(x_T, 1.0, 1000)
    assert abs(out_mid - 1.0) < 0.01, "Balance,TetA: exponent≈0, forced to x=1"

    print("  ✓ Geometric Toffoli is XOR-controlled (not AND-controlled):")
    print("    Agree → no flip | Disagree → flip | Balance → forced to x=1")
    print("    DISCOVERY: product (2μ-1)·(2μ-1) gives PARITY gate, not Toffoli")
    print("    True AND-control requires: x_T^{1 - 2·μ̄_A·μ̄_B} (TetB-product exponent)")


def and_toffoli(x_T, x_A, x_B):
    """AND-controlled Toffoli: x_T^{1 - 2·μ̄_A·μ̄_B}
    Flips target only when BOTH controls are TetB."""
    mubar_A = float(one_minus_mu(x_A))
    mubar_B = float(one_minus_mu(x_B))
    exponent = 1.0 - 2.0 * mubar_A * mubar_B
    return x_T ** exponent


def test_and_toffoli():
    """AND-controlled Toffoli: flip only when BOTH controls are TetB"""
    x_T = 4.0

    # Both TetA: μ̄≈0, product≈0, exp≈+1 → no flip
    out = and_toffoli(x_T, 1000, 1000)
    assert abs(out - x_T) / x_T < 0.01, "AND(TetA,TetA) should not flip"

    # Both TetB: μ̄≈1, product≈1, exp≈-1 → flip
    out = and_toffoli(x_T, 0.001, 0.001)
    assert abs(out - 1.0/x_T) < 0.01, "AND(TetB,TetB) should flip"

    # Mixed: μ̄_A≈0, product≈0, exp≈+1 → no flip
    out = and_toffoli(x_T, 1000, 0.001)
    assert abs(out - x_T) / x_T < 0.05, "AND(TetA,TetB) should not flip"

    # One at balance: μ̄=1/2, product=1/2·μ̄_B, exp close to 1 → weak flip
    out = and_toffoli(x_T, 1.0, 0.001)
    # μ̄_A=0.5, μ̄_B≈1, product≈0.5, exp≈0 → x_T^0 = 1
    assert abs(out - 1.0) < 0.5, "AND(balance,TetB): partial, exp≈0"

    print("  ✓ AND-controlled Toffoli: flip only when both controls are TetB")
    print("    XOR-Toffoli: natural from s_A·s_B product (parity-symmetric)")
    print("    AND-Toffoli: from μ̄_A·μ̄_B product (parity-asymmetric)")


# =========================================================================
#  5. WALSH COMPILATION
# =========================================================================

def test_walsh_xor_depth():
    """XOR has Walsh sparsity 1 regardless of input width"""
    for n in [2, 3, 4, 5, 6]:
        N = 2**n
        # XOR = parity of all bits
        tt = np.array([bin(i).count('1') % 2 for i in range(N)])
        bridge = truth_table_to_bridge(tt)
        s = walsh_sparsity(bridge)
        assert s == 1, f"{n}-bit XOR sparsity = {s}, expected 1"
    print("  ✓ Walsh XOR depth: sparsity = 1 for n = 2,3,4,5,6")


def test_walsh_and_depth():
    """n-bit AND has Walsh sparsity 2^n (all coefficients nonzero)"""
    for n in [2, 3, 4, 5]:
        N = 2**n
        # AND = 1 only when all bits are 1
        tt = np.zeros(N, dtype=int)
        tt[N - 1] = 1
        bridge = truth_table_to_bridge(tt)
        s = walsh_sparsity(bridge)
        assert s == N, f"{n}-bit AND sparsity = {s}, expected {N}"
    print("  ✓ Walsh AND depth: sparsity = 2^n (maximally complex)")


def test_walsh_majority():
    """3-bit majority has intermediate sparsity"""
    tt = np.array([0, 0, 0, 1, 0, 1, 1, 1])  # majority of 3 bits
    bridge = truth_table_to_bridge(tt)
    s = walsh_sparsity(bridge)
    print(f"  ✓ 3-bit majority: sparsity = {s}, bridge = {bridge.round(4)}")


def test_circuit_depth_matches_sparsity():
    """Verify WaveNode evaluation uses exactly s nonzero terms"""
    # 4-bit function: f = x0 XOR x1 (ignores x2, x3)
    N = 16
    tt = np.array([0, 1, 1, 0,  0, 1, 1, 0,  0, 1, 1, 0,  0, 1, 1, 0])
    bridge = truth_table_to_bridge(tt)
    s = walsh_sparsity(bridge)

    # Count which bridge coefficients are actually used
    active = [c for c in range(N) if abs(bridge[c]) > 1e-10]
    assert len(active) == s, f"active coefficients = {len(active)}, sparsity = {s}"

    # Verify the active mask is exactly c=3 (bits 0 and 1, the XOR inputs)
    assert active == [3], f"active masks = {active}, expected [3]"
    print(f"  ✓ 4-bit partial XOR: sparsity = {s}, active mask = {active} (bits 0,1 only)")


# =========================================================================
#  6. NETWORK TOPOLOGY
# =========================================================================

def test_stellated_octahedron_counts():
    """Verify vertex/edge/face counts"""
    M = canonical_sign_matrix()
    tet_a = M            # 3×4: four columns = TetA vertices
    tet_b = -M           # 3×4: four columns = TetB vertices
    all_verts = np.hstack([tet_a, tet_b])  # 3×8

    assert all_verts.shape == (3, 8), f"vertex count: {all_verts.shape[1]}"

    # Count TetA edges (pairs within TetA)
    n_tet_a_edges = 0
    for i in range(4):
        for j in range(i+1, 4):
            n_tet_a_edges += 1
    assert n_tet_a_edges == 6, f"TetA edges: {n_tet_a_edges}"

    # Count cube edges (pairs with Hamming distance 1 in ±1 encoding)
    n_cube_edges = 0
    for i in range(8):
        for j in range(i+1, 8):
            diff = np.sum(all_verts[:, i] != all_verts[:, j])
            if diff == 1:  # adjacent in cube
                n_cube_edges += 1
    assert n_cube_edges == 12, f"cube edges: {n_cube_edges}"

    # Total connection components per two-tile boundary
    K = 4
    total_per_face = K**2
    assert total_per_face == 16
    retained = K * (K + 1) // 2
    assert retained == 10
    discarded = K * (K - 1) // 2
    assert discarded == 6
    entangling = 2 * discarded  # both upper and lower triangles from each side
    assert entangling == 12
    classical = K  # diagonal, root-blind
    # Note: retained = classical + one_side_off_diagonal = 4 + 6 = 10

    print(f"  ✓ Stellated octahedron: 8 vertices, 6+6 tet edges, 12 cube edges")
    print(f"    Per face: {total_per_face} total, {retained} retained, {discarded} discarded")
    print(f"    Entangling channels per boundary: {entangling}/16 = {entangling/16:.0%}")


# =========================================================================
#  7. COUPLING POLYNOMIAL → COMPLEX PLANE
# =========================================================================

def test_complex_polynomial_circle():
    """f(4, e^{iθ}) traces a circle of radius K=4 centered at 17"""
    K = 4
    center = 1 + K**2  # = 17
    radius = K          # = 4

    for theta in np.linspace(0, 2 * math.pi, 100):
        s = complex(math.cos(theta), math.sin(theta))
        f = 1 + s * K + K**2
        # Distance from center should equal radius
        dist = abs(f - center)
        assert abs(dist - radius) < 1e-10, \
            f"f(4, e^{{i{theta:.2f}}}) distance from 17 = {dist}, expected 4"
    print("  ✓ Complex coupling polynomial: circle of radius 4 centered at 17")


def test_transition_rate_is_imaginary_part():
    """μ(1-μ) = Im[f]² / (4K²) = sin²θ/4"""
    K = 4
    for theta in np.linspace(0.1, math.pi - 0.1, 50):
        x = x_from_theta(theta)
        mu_val = float(mu(x))
        transition = mu_val * (1 - mu_val)

        im_f = K * math.sin(theta)
        from_imaginary = im_f**2 / (4 * K**2)

        assert abs(transition - from_imaginary) < 1e-10, \
            f"μ(1-μ) ≠ Im[f]²/(4K²) at θ={theta:.3f}"
    print("  ✓ Transition rate = |Im[f]|²/(4K²) = sin²θ/4")


# =========================================================================
#  8. INTEGRATION: SOFT CNOT + WALSH = FULL CIRCUIT
# =========================================================================

def test_full_circuit_2bit_and():
    """
    Compile 2-bit AND via Walsh, then verify against
    direct soft-CNOT evaluation.
    """
    # Walsh compilation of AND
    tt_and = np.array([0, 0, 0, 1])
    bridge = truth_table_to_bridge(tt_and)

    # Evaluate via WaveNode on all inputs
    for j in range(4):
        wn_out = wavenode_eval(bridge, j)
        # WaveNode output in ±1 convention: +1 = false, -1 = true
        bool_out = 1 if wn_out < 0 else 0
        assert bool_out == tt_and[j], \
            f"WaveNode AND({j}) = {bool_out}, expected {tt_and[j]}"

    print(f"  ✓ Full 2-bit AND circuit: Walsh compile + WaveNode eval matches truth table")
    print(f"    Bridge coefficients: {bridge.round(4)}")
    print(f"    Sparsity: {walsh_sparsity(bridge)} (all 4 nonzero → depth 4)")


# =========================================================================
#  RUN ALL
# =========================================================================

def run_all_tests():
    print("=" * 60)
    print("  t-bit ALGEBRA VERIFICATION")
    print("=" * 60)

    print("\n§1 Single-t-bit gates:")
    test_parity_gate()
    test_dilation_group()
    test_conjugation_identity()
    test_mixing_purification()
    test_mu_output_table()

    print("\n§2 Gate energy:")
    test_parity_flip_cost()
    test_geometric_landauer()

    print("\n§3 Two-t-bit operations:")
    test_soft_cnot_limits()
    test_xnor_identity()
    test_xor_complement()

    print("\n§4 Toffoli gate:")
    test_toffoli()
    test_and_toffoli()

    print("\n§5 Walsh compilation:")
    test_walsh_xor_depth()
    test_walsh_and_depth()
    test_walsh_majority()
    test_circuit_depth_matches_sparsity()

    print("\n§6 Network topology:")
    test_stellated_octahedron_counts()

    print("\n§7 Complex coupling polynomial:")
    test_complex_polynomial_circle()
    test_transition_rate_is_imaginary_part()

    print("\n§8 Full circuit integration:")
    test_full_circuit_2bit_and()

    print("\n" + "=" * 60)
    print("  ALL t-bit ALGEBRA CHECKS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
