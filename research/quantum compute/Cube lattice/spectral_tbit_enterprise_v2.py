#!/usr/bin/env python3
"""
Spectral t-bit Enterprise Engine
================================

A single-file, well-commented implementation of the spectral/Walsh compute
algebra discussed in the t-bit compute-node design.

What this file provides
-----------------------

1. Boolean / hard spectral mode
   - Compile a truth table or Python function into Walsh bridge coefficients.
   - Evaluate exactly at Boolean pole states.
   - Convert hard Boolean input bits into signed pole states {-1,+1}.

2. Continuous / soft t-bit mode
   - Evaluate the same Walsh bridge inside the continuous cube s_i in [-1,+1].
   - This computes the exact multilinear expectation extension of the Boolean
     function when each bit has expectation s_i.

3. t-bit node operators
   - signed coordinate s = 2μ - 1
   - soft CNOT / XNOR as multiplication: s_out = s_a * s_b
   - hyperbolic amplification A_rho(s) = tanh(rho * atanh(s))
   - deterministic stress descent with tau(s) = (1 - s^2) / 4

4. Factor-lattice / SAT-style constraint dynamics
   - Clause unsatisfied weight U_C = Π_i (1 - sigma_i s_i)/2
   - Exact derivative message m_{C -> i} = -dU_C/ds_i
   - Residual load, pressure, confidence, adaptive amplification
   - A minimal lattice update loop for soft constraint solving

5. Test harness
   - Run this file directly: python spectral_tbit_enterprise.py
   - Tests verify the algebraic identities and practical behavior.

Design principles
-----------------

- No GPU dependency. This file is intentionally portable and enterprise-friendly.
- NumPy is used for clarity and reliable vector math.
- All public functions have docstrings.
- Tests are deterministic and do not rely on random pass/fail behavior.

Notation
--------

Hard Boolean bits are represented as 0/1.
Signed t-bit poles use +1 / -1.

Important convention:
    bit 0 maps to signed +1
    bit 1 maps to signed -1

This matches the standard spectral convention used by:
    signed = 1 - 2 * bit

For a subset mask c, the Walsh character is:
    chi_c(x) = (-1) ** popcount(x & c)

For a soft signed vector s in [-1,+1]^n, the continuous character is:
    chi_c(s) = Π_{i where bit_i(c)=1} s_i

At the Boolean poles, these are the same object.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple
import math
import unittest

import numpy as np


# =============================================================================
# Basic helpers
# =============================================================================


def popcount(x: int) -> int:
    """Return the number of 1 bits in a non-negative integer."""
    return int(x).bit_count()


def bit_to_signed(bit: int) -> float:
    """Map Boolean bit 0/1 to signed pole +1/-1."""
    return 1.0 - 2.0 * (int(bit) & 1)


def signed_to_bit(s: float) -> int:
    """Map signed value to Boolean bit using the spectral convention.

    s >= 0 -> bit 0
    s <  0 -> bit 1
    """
    return 0 if s >= 0 else 1


def int_to_signed_vector(x: int, n_bits: int) -> np.ndarray:
    """Convert integer x into signed pole vector of length n_bits.

    bit_i = 0 gives s_i = +1
    bit_i = 1 gives s_i = -1
    """
    return np.array([bit_to_signed((x >> i) & 1) for i in range(n_bits)], dtype=np.float64)


def signed_vector_to_int(s: Sequence[float]) -> int:
    """Convert signed vector to integer by thresholding each component."""
    out = 0
    for i, value in enumerate(s):
        out |= signed_to_bit(float(value)) << i
    return out


def clamp_unit(x: np.ndarray | float, eps: float = 1e-12):
    """Clamp value(s) safely to (-1, 1) for atanh-based operations."""
    return np.clip(x, -1.0 + eps, 1.0 - eps)


# =============================================================================
# Walsh-Hadamard spectral algebra
# =============================================================================


def walsh_hadamard_matrix(n_bits: int) -> np.ndarray:
    """Build the 2^n x 2^n Walsh-Hadamard matrix.

    H[c, x] = (-1)^popcount(c & x)

    Rows are spectral characters indexed by c.
    Columns are Boolean inputs indexed by x.
    """
    if n_bits < 0:
        raise ValueError("n_bits must be non-negative")
    size = 1 << n_bits
    H = np.empty((size, size), dtype=np.float64)
    for c in range(size):
        for x in range(size):
            H[c, x] = 1.0 if (popcount(c & x) % 2 == 0) else -1.0
    return H


def walsh_character_hard(mask: int, x: int) -> float:
    """Evaluate hard Walsh character chi_mask(x)."""
    return 1.0 if (popcount(mask & x) % 2 == 0) else -1.0


def walsh_character_soft(mask: int, s: Sequence[float]) -> float:
    """Evaluate continuous Walsh character chi_mask(s) = product selected s_i."""
    result = 1.0
    i = 0
    m = int(mask)
    while m:
        if m & 1:
            result *= float(s[i])
        i += 1
        m >>= 1
    return result


def bridge_from_values(values: Sequence[float]) -> np.ndarray:
    """Compile function values on the Boolean cube into Walsh bridge coefficients.

    Args:
        values: length 2^n sequence. values[x] is f(x).

    Returns:
        bridge coefficients b[c] such that:
            f(x) = Σ_c b[c] * (-1)^popcount(c & x)
    """
    values_np = np.asarray(values, dtype=np.float64)
    size = values_np.size
    if size == 0 or (size & (size - 1)) != 0:
        raise ValueError("values length must be a positive power of two")
    n_bits = int(math.log2(size))
    H = walsh_hadamard_matrix(n_bits)
    return (H @ values_np) / size


def bridge_from_function(func: Callable[[int], float], n_bits: int) -> np.ndarray:
    """Compile a Python function f(x) into Walsh bridge coefficients."""
    size = 1 << n_bits
    values = [float(func(x)) for x in range(size)]
    return bridge_from_values(values)


def bridge_from_truth_table_01(truth_table: Sequence[int]) -> np.ndarray:
    """Compile a Boolean 0/1 truth table into signed Walsh bridge coefficients.

    This uses signed output convention:
        bit 0 -> +1
        bit 1 -> -1

    Therefore the signed function values are:
        f_signed[x] = 1 - 2 * truth_table[x]
    """
    tt = np.asarray(truth_table, dtype=np.float64)
    if not np.all((tt == 0) | (tt == 1)):
        raise ValueError("truth_table must contain only 0/1 values")
    signed_values = 1.0 - 2.0 * tt
    return bridge_from_values(signed_values)


def evaluate_bridge_hard(bridge: Sequence[float], x: int) -> float:
    """Evaluate a bridge at hard Boolean input x, returning a real signed value."""
    b = np.asarray(bridge, dtype=np.float64)
    result = 0.0
    for c, coeff in enumerate(b):
        result += coeff * walsh_character_hard(c, x)
    return float(result)


def evaluate_bridge_bit(bridge: Sequence[float], x: int) -> int:
    """Evaluate a bridge at hard input x and threshold to Boolean bit 0/1."""
    return signed_to_bit(evaluate_bridge_hard(bridge, x))


def evaluate_bridge_soft(bridge: Sequence[float], s: Sequence[float]) -> float:
    """Evaluate a bridge inside the continuous signed cube.

    Args:
        bridge: Walsh coefficients of length 2^n.
        s: soft signed vector of length n with values in [-1,+1].

    Returns:
        F(s) = Σ_c bridge[c] Π_{i in c} s_i

    This is the exact multilinear extension of the function represented
    by the bridge.
    """
    b = np.asarray(bridge, dtype=np.float64)
    n_bits = int(math.log2(len(b)))
    if len(s) != n_bits:
        raise ValueError(f"expected s length {n_bits}, got {len(s)}")
    result = 0.0
    for c, coeff in enumerate(b):
        result += coeff * walsh_character_soft(c, s)
    return float(result)


def reconstruct_values(bridge: Sequence[float]) -> np.ndarray:
    """Reconstruct all hard-cube function values from bridge coefficients."""
    b = np.asarray(bridge, dtype=np.float64)
    size = b.size
    n_bits = int(math.log2(size))
    H = walsh_hadamard_matrix(n_bits)
    return b @ H


def bridge_margin_report(bridge: Sequence[float], threshold: float = 0.1) -> Dict[str, object]:
    """Inspect hard-cube output margins for a bridge.

    Margin is min_x |f(x)|. A zero margin means hard sign readout is ambiguous.
    This is the discrete counterpart of high transition stress.
    """
    values = reconstruct_values(bridge)
    abs_values = np.abs(values)
    margin = float(np.min(abs_values))
    weak_indices = np.where(abs_values < threshold)[0].astype(int).tolist()
    dead_indices = np.where(abs_values < 1e-12)[0].astype(int).tolist()
    return {
        "margin": margin,
        "threshold": threshold,
        "weak_count": len(weak_indices),
        "weak_indices": weak_indices,
        "dead_count": len(dead_indices),
        "dead_indices": dead_indices,
        "status": "FAIL" if dead_indices else ("WARN" if weak_indices else "PASS"),
    }


# =============================================================================
# t-bit coordinate algebra and node operators
# =============================================================================


def mu_from_x(x: np.ndarray | float):
    """Constitutive fraction mu = x / (x + 1)."""
    return np.asarray(x, dtype=np.float64) / (np.asarray(x, dtype=np.float64) + 1.0)


def s_from_mu(mu: np.ndarray | float):
    """Signed partition coordinate s = 2*mu - 1."""
    return 2.0 * np.asarray(mu, dtype=np.float64) - 1.0


def mu_from_s(s: np.ndarray | float):
    """Recover mu from signed coordinate: mu = (1+s)/2."""
    return (1.0 + np.asarray(s, dtype=np.float64)) / 2.0


def s_from_x(x: np.ndarray | float):
    """Map physical x in (0,∞) to signed coordinate s in (-1,+1)."""
    x_np = np.asarray(x, dtype=np.float64)
    return (x_np - 1.0) / (x_np + 1.0)


def x_from_s(s: np.ndarray | float):
    """Map signed coordinate s in (-1,+1) back to physical x."""
    s_np = np.asarray(s, dtype=np.float64)
    if np.any(np.abs(s_np) >= 1.0):
        raise ValueError("x_from_s requires |s| < 1")
    return (1.0 + s_np) / (1.0 - s_np)


def r_from_s(s: np.ndarray | float):
    """Rapidity/logit coordinate r = ln(x) = 2 atanh(s)."""
    return 2.0 * np.arctanh(clamp_unit(np.asarray(s, dtype=np.float64)))


def s_from_r(r: np.ndarray | float):
    """Signed coordinate from rapidity: s = tanh(r/2)."""
    return np.tanh(np.asarray(r, dtype=np.float64) / 2.0)


def soft_cnot_xnor_s(s_target: float, s_control: float) -> float:
    """Soft CNOT/XNOR in signed coordinates.

    Algebraic identity:
        s_out = s_target * s_control
    """
    return float(s_target) * float(s_control)


def xor_fraction_from_s(s_a: float, s_b: float) -> float:
    """Return XOR/TetB fraction for two signed states."""
    return (1.0 - float(s_a) * float(s_b)) / 2.0


def xnor_fraction_from_s(s_a: float, s_b: float) -> float:
    """Return XNOR/TetA fraction for two signed states."""
    return (1.0 + float(s_a) * float(s_b)) / 2.0


def amplify(s: np.ndarray | float, rho: np.ndarray | float = 2.0, eps: float = 1e-12):
    """Hyperbolic amplification / measurement operator.

    A_rho(s) = tanh(rho * atanh(s))

    - rho > 1 amplifies toward poles ±1.
    - rho = 1 leaves state unchanged.
    - 0 < rho < 1 mixes toward balance 0.

    rho may be either a scalar or an array broadcastable to s.
    """
    rho_np = np.asarray(rho, dtype=np.float64)
    if np.any(rho_np <= 0):
        raise ValueError("rho must be positive")
    s_np = clamp_unit(np.asarray(s, dtype=np.float64), eps=eps)
    return np.tanh(rho_np * np.arctanh(s_np))

def amplify2(s: np.ndarray | float):
    """Fast closed-form A_2(s) = 2s / (1+s^2)."""
    s_np = np.asarray(s, dtype=np.float64)
    return (2.0 * s_np) / (1.0 + s_np * s_np)


def mix_half(s: np.ndarray | float):
    """Fast closed-form A_{1/2}(s), which pulls state toward balance."""
    s_np = clamp_unit(np.asarray(s, dtype=np.float64))
    return s_np / (1.0 + np.sqrt(1.0 - s_np * s_np))


def transition_stress(s: np.ndarray | float):
    """Transition stress tau(s) = (1 - s^2) / 4.

    tau is maximal at s=0 and zero at the poles ±1.
    """
    s_np = np.asarray(s, dtype=np.float64)
    return (1.0 - s_np * s_np) / 4.0


def tbit_node_from_bridge(bridge: Sequence[float], s: Sequence[float], rho: float = 1.0) -> float:
    """Evaluate one soft spectral t-bit node.

    Steps:
        1. Evaluate Walsh bridge inside continuous cube.
        2. Bound via tanh(y/2) to keep state in (-1,+1).
        3. Optionally amplify/mix using A_rho.
    """
    y = evaluate_bridge_soft(bridge, s)
    bounded = math.tanh(0.5 * y)
    return float(amplify(bounded, rho=rho))


# =============================================================================
# Boolean gate coefficient helpers
# =============================================================================


GATE_COEFFS_2_INPUT: Dict[str, Tuple[float, float, float, float]] = {
    # Coefficients for signed output F(a,b) = c0 + ca*a + cb*b + cab*a*b.
    # Convention: Boolean bit 0 -> signed +1, bit 1 -> signed -1.
    "XOR": (0.0, 0.0, 0.0, 1.0),      # signed output +1 when bits equal? See tests.
    "XNOR": (0.0, 0.0, 0.0, -1.0),
    "AND": (0.5, 0.5, 0.5, -0.5),
    "NAND": (-0.5, -0.5, -0.5, 0.5),
    "OR": (-0.5, 0.5, 0.5, 0.5),
    "NOR": (0.5, -0.5, -0.5, -0.5),
}


def bridge_from_2_input_coeffs(coeffs: Tuple[float, float, float, float]) -> np.ndarray:
    """Convert two-input coefficient tuple to 4-value bridge array.

    Bridge order: [constant, a, b, a*b]
    when signed vector order is bit0=a, bit1=b.
    """
    if len(coeffs) != 4:
        raise ValueError("two-input coeffs must have four values")
    return np.asarray(coeffs, dtype=np.float64)


# =============================================================================
# Factor-lattice / SAT algebra
# =============================================================================


@dataclass(frozen=True)
class Literal:
    """A signed literal in a factor/clause.

    index: variable index i
    sigma: +1 for positive literal s_i, -1 for negated literal -s_i
    """

    index: int
    sigma: int = 1

    def __post_init__(self):
        if self.sigma not in (-1, 1):
            raise ValueError("sigma must be +1 or -1")
        if self.index < 0:
            raise ValueError("literal index must be non-negative")


@dataclass
class ClauseFactor:
    """A soft OR-clause factor over signed t-bit states.

    For each literal ell_i = sigma_i * s_i:
        false fraction q_i = (1 - ell_i) / 2

    Clause unsatisfied weight:
        U_C = Π_i q_i

    At Boolean poles, U_C is exactly 1 if the clause is false and 0 otherwise.
    Inside the cube, U_C is the probability the clause is false under
    independent signed-bias semantics.
    """

    literals: Tuple[Literal, ...]
    weight: float = 1.0

    def __post_init__(self):
        if not self.literals:
            raise ValueError("clause must contain at least one literal")

    def false_fraction(self, s: Sequence[float], literal: Literal) -> float:
        """Return q_i = (1 - sigma_i s_i)/2 for one literal."""
        return (1.0 - literal.sigma * float(s[literal.index])) / 2.0

    def unsatisfied(self, s: Sequence[float]) -> float:
        """Return weighted unsatisfied weight w_C * U_C."""
        u = 1.0
        for lit in self.literals:
            u *= self.false_fraction(s, lit)
        return self.weight * u

    def raw_unsatisfied(self, s: Sequence[float]) -> float:
        """Return unweighted U_C."""
        u = 1.0
        for lit in self.literals:
            u *= self.false_fraction(s, lit)
        return u

    def message_to(self, s: Sequence[float], target_index: int) -> float:
        """Return exact pressure message m_{C -> i} = -d(wU_C)/ds_i.

        For a literal i in C:
            m_{C->i} = w * sigma_i/2 * Π_{j!=i} (1 - sigma_j s_j)/2

        If target_index is not in the clause, returns 0.
        """
        target_lit: Optional[Literal] = None
        for lit in self.literals:
            if lit.index == target_index:
                target_lit = lit
                break
        if target_lit is None:
            return 0.0

        product = 1.0
        for lit in self.literals:
            if lit.index != target_index:
                product *= self.false_fraction(s, lit)
        return self.weight * (target_lit.sigma / 2.0) * product

    def involved_indices(self) -> Tuple[int, ...]:
        """Return variable indices touched by this clause."""
        return tuple(lit.index for lit in self.literals)


@dataclass
class TBitLattice:
    """A minimal factor-lattice runtime for soft t-bit computation."""

    n_vars: int
    clauses: List[ClauseFactor]
    bias: Optional[np.ndarray] = None
    eta: float = 1.0
    rho_max: float = 1.0
    epsilon: float = 1e-9

    def __post_init__(self):
        if self.bias is None:
            self.bias = np.zeros(self.n_vars, dtype=np.float64)
        else:
            self.bias = np.asarray(self.bias, dtype=np.float64)
        if self.bias.shape != (self.n_vars,):
            raise ValueError("bias must have shape (n_vars,)")

    def residual_total(self, s: Sequence[float]) -> float:
        """Return total weighted unsatisfied residual R(s)."""
        return float(sum(clause.unsatisfied(s) for clause in self.clauses))

    def residual_loads(self, s: Sequence[float]) -> np.ndarray:
        """Return R_i = sum of residuals for clauses touching variable i."""
        loads = np.zeros(self.n_vars, dtype=np.float64)
        for clause in self.clauses:
            u = clause.unsatisfied(s)
            for idx in clause.involved_indices():
                loads[idx] += u
        return loads

    def pressures(self, s: Sequence[float]) -> np.ndarray:
        """Return p_i = sum_C m_{C->i}."""
        p = np.zeros(self.n_vars, dtype=np.float64)
        for clause in self.clauses:
            for idx in clause.involved_indices():
                p[idx] += clause.message_to(s, idx)
        return p

    def confidence(self, s: Sequence[float]) -> np.ndarray:
        """Return local confidence C_i = |p_i| / (R_i + epsilon)."""
        p = self.pressures(s)
        loads = self.residual_loads(s)
        return np.abs(p) / (loads + self.epsilon)

    def stress_total(self, s: Sequence[float]) -> float:
        """Return total transition stress Σ_i tau(s_i)."""
        return float(np.sum(transition_stress(np.asarray(s, dtype=np.float64))))

    def step(self, s: Sequence[float]) -> np.ndarray:
        """Perform one adaptive factor-lattice update.

        The update uses exact residual pressure plus local confidence-based
        amplification:

            p_i = Σ_C m_{C->i}
            C_i = |p_i| / (R_i + eps)
            rho_i = 1 + rho_max * C_i
            s_i' = A_{rho_i}(tanh((bias_i + eta p_i)/2))
        """
        s_np = np.asarray(s, dtype=np.float64)
        p = self.pressures(s_np)
        loads = self.residual_loads(s_np)
        conf = np.abs(p) / (loads + self.epsilon)
        rho = 1.0 + self.rho_max * conf
        pre = np.tanh(0.5 * (self.bias + self.eta * p))
        return amplify(pre, rho=rho)

    def solve(self, s0: Sequence[float], steps: int = 100) -> Tuple[np.ndarray, List[Dict[str, float]]]:
        """Run a fixed number of lattice update steps and return history."""
        s = np.asarray(s0, dtype=np.float64).copy()
        history: List[Dict[str, float]] = []
        for _ in range(steps):
            history.append({
                "residual": self.residual_total(s),
                "stress": self.stress_total(s),
            })
            s = self.step(s)
        history.append({
            "residual": self.residual_total(s),
            "stress": self.stress_total(s),
        })
        return s, history


# =============================================================================
# Tests
# =============================================================================


class TestSpectralTBitEnterprise(unittest.TestCase):
    """Unit tests proving the algebraic claims."""

    def test_walsh_exact_reconstruction(self):
        """Any function on the Boolean cube has exact Walsh reconstruction."""
        values = [3, -2, 7, 0, 5, 4, -1, 9]
        bridge = bridge_from_values(values)
        reconstructed = reconstruct_values(bridge)
        self.assertTrue(np.allclose(reconstructed, values, atol=1e-10))

    def test_truth_table_boolean_and(self):
        """Boolean bridge compiles AND exactly under 0/1 convention."""
        tt_and = [0, 0, 0, 1]  # input order: 00,01,10,11 by integer index
        bridge = bridge_from_truth_table_01(tt_and)
        got = [evaluate_bridge_bit(bridge, x) for x in range(4)]
        self.assertEqual(got, tt_and)

    def test_soft_expectation_property(self):
        """Soft Walsh eval equals expectation over independent pole variables."""
        # Function: XOR in 0/1 output, converted to signed output.
        tt_xor = [0, 1, 1, 0]
        bridge = bridge_from_truth_table_01(tt_xor)

        # Soft biases for bits a,b. E[A]=s0, E[B]=s1.
        s = np.array([0.25, -0.6], dtype=np.float64)
        soft_value = evaluate_bridge_soft(bridge, s)

        # Direct expectation over four pole states.
        expected = 0.0
        for x in range(4):
            prob = 1.0
            for i in range(2):
                bit = (x >> i) & 1
                prob *= (1.0 + s[i]) / 2.0 if bit == 0 else (1.0 - s[i]) / 2.0
            signed_output = bit_to_signed(tt_xor[x])
            expected += prob * signed_output

        self.assertAlmostEqual(soft_value, expected, places=12)

    def test_s_coordinate_bijection(self):
        """x <-> s coordinate maps round-trip."""
        xs = np.array([0.1, 0.5, 1.0, 2.0, 10.0], dtype=np.float64)
        s = s_from_x(xs)
        xs_back = x_from_s(s)
        self.assertTrue(np.allclose(xs, xs_back, atol=1e-12))
        self.assertTrue(np.all(s > -1.0))
        self.assertTrue(np.all(s < 1.0))

    def test_soft_cnot_is_multiplication(self):
        """XNOR partition identity reduces exactly to s_out = s_T * s_C."""
        for s_t in [-1.0, -0.4, 0.0, 0.7, 1.0]:
            for s_c in [-1.0, -0.2, 0.0, 0.5, 1.0]:
                mu_t = mu_from_s(s_t)
                mu_c = mu_from_s(s_c)
                mubar_t = 1.0 - mu_t
                mubar_c = 1.0 - mu_c
                mu_out = mu_t * mu_c + mubar_t * mubar_c
                s_out = s_from_mu(mu_out)
                self.assertAlmostEqual(float(s_out), s_t * s_c, places=12)

    def test_amplification_stress_descent(self):
        """A_rho with rho>1 increases |s| and reduces stress."""
        for s in [-0.9, -0.5, -0.1, 0.1, 0.5, 0.9]:
            out = float(amplify(s, rho=2.0))
            self.assertGreater(abs(out), abs(s))
            self.assertLess(float(transition_stress(out)), float(transition_stress(s)))

    def test_amplify2_closed_form(self):
        """A_2 closed form matches tanh(2 atanh(s))."""
        vals = np.array([-0.8, -0.2, 0.0, 0.3, 0.9], dtype=np.float64)
        self.assertTrue(np.allclose(amplify(vals, rho=2.0), amplify2(vals), atol=1e-12))

    def test_clause_unsatisfied_at_poles(self):
        """Clause unsatisfied weight is exact Boolean false indicator at poles."""
        # Clause: (x0 OR not x1). With signed convention:
        # positive x0 literal satisfied when bit0=0 -> s0=+1
        # negated x1 literal satisfied when bit1=1 -> s1=-1, so sigma=-1.
        clause = ClauseFactor((Literal(0, +1), Literal(1, -1)))

        # Only false when x0 is false and not x1 is false:
        # x0 bit=1 -> s0=-1; x1 bit=0 -> s1=+1.
        for bit0 in [0, 1]:
            for bit1 in [0, 1]:
                s = np.array([bit_to_signed(bit0), bit_to_signed(bit1)])
                u = clause.raw_unsatisfied(s)
                expected_false = (bit0 == 1 and bit1 == 0)
                self.assertAlmostEqual(u, 1.0 if expected_false else 0.0)

    def test_clause_message_matches_numeric_derivative(self):
        """Clause message equals negative derivative of unsatisfied energy."""
        clause = ClauseFactor((Literal(0, +1), Literal(1, -1), Literal(2, +1)), weight=2.0)
        s = np.array([0.2, -0.3, 0.4], dtype=np.float64)
        eps = 1e-6
        for idx in [0, 1, 2]:
            s_plus = s.copy(); s_plus[idx] += eps
            s_minus = s.copy(); s_minus[idx] -= eps
            derivative = (clause.unsatisfied(s_plus) - clause.unsatisfied(s_minus)) / (2 * eps)
            message = clause.message_to(s, idx)
            self.assertAlmostEqual(message, -derivative, places=6)

    def test_lattice_pressure_direction_reduces_simple_residual(self):
        """For a simple one-literal clause, the update moves toward satisfaction."""
        # Clause: x0 should be true in signed sense (+1). U=(1-s0)/2.
        lattice = TBitLattice(
            n_vars=1,
            clauses=[ClauseFactor((Literal(0, +1),), weight=1.0)],
            eta=2.0,
            rho_max=0.0,
        )
        s0 = np.array([-0.5])
        r0 = lattice.residual_total(s0)
        s1 = lattice.step(s0)
        r1 = lattice.residual_total(s1)
        self.assertLess(r1, r0)
        self.assertGreater(s1[0], s0[0])

    def test_bridge_margin_report(self):
        """Margin report catches an ambiguous all-zero function."""
        bridge = np.zeros(4, dtype=np.float64)
        report = bridge_margin_report(bridge)
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["dead_count"], 4)

    def test_tbit_node_from_bridge(self):
        """Soft node produces bounded output and amplification sharpens it."""
        # Two-input AND bridge, evaluated at soft inputs.
        bridge = bridge_from_truth_table_01([0, 0, 0, 1])
        s = np.array([0.6, 0.7])
        out_soft = tbit_node_from_bridge(bridge, s, rho=1.0)
        out_amp = tbit_node_from_bridge(bridge, s, rho=2.0)
        self.assertLessEqual(abs(out_soft), 1.0)
        self.assertLessEqual(abs(out_amp), 1.0)
        self.assertGreaterEqual(abs(out_amp), abs(out_soft))


# =============================================================================
# Demonstration helpers
# =============================================================================


def demo() -> None:
    """Print a compact demo when run as a script after tests."""
    print("\n" + "=" * 72)
    print("Spectral t-bit Enterprise Engine Demo")
    print("=" * 72)

    # Compile XOR and evaluate hard + soft.
    xor_bridge = bridge_from_truth_table_01([0, 1, 1, 0])
    print("\nXOR bridge coefficients:")
    print(np.round(xor_bridge, 4).tolist())

    print("\nHard XOR truth table via bridge:")
    for x in range(4):
        print(f"  input {x:02b} -> bit {evaluate_bridge_bit(xor_bridge, x)}")

    soft_state = np.array([0.25, -0.6])
    print("\nSoft XOR signed expectation:")
    print(f"  s = {soft_state.tolist()}")
    print(f"  F(s) = {evaluate_bridge_soft(xor_bridge, soft_state):+.6f}")

    print("\nAmplification A2 examples:")
    for v in [-0.5, -0.1, 0.1, 0.5]:
        print(f"  s={v:+.2f} -> A2={float(amplify2(v)):+.4f}, stress {float(transition_stress(v)):.4f} -> {float(transition_stress(amplify2(v))):.4f}")

    # Tiny SAT-like example: clauses (x0) and (not x0 OR x1).
    clauses = [
        ClauseFactor((Literal(0, +1),), weight=1.0),
        ClauseFactor((Literal(0, -1), Literal(1, +1)), weight=1.0),
    ]
    lattice = TBitLattice(n_vars=2, clauses=clauses, eta=2.0, rho_max=0.5)
    s0 = np.array([-0.4, -0.2])
    s_final, hist = lattice.solve(s0, steps=8)
    print("\nTiny factor lattice:")
    print(f"  start s = {np.round(s0, 4).tolist()}, residual={hist[0]['residual']:.4f}")
    print(f"  final s = {np.round(s_final, 4).tolist()}, residual={hist[-1]['residual']:.4f}")
    print(f"  readout bits = {[signed_to_bit(x) for x in s_final]}")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSpectralTBitEnterprise)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        demo()
    else:
        raise SystemExit(1)
