"""
bridge.py
==========

Walsh-Hadamard bridge utilities for Boolean gates.

The Walsh bridge of an n-input Boolean function is its unique
Cl(n,0)-grade decomposition: a 2^n-cell vector B where each cell is
indexed by a Hamming-weight subset of the n inputs, and the cell's
value is the Walsh-Hadamard coefficient at that subset.

This module provides:

  - truth_table(fn, n)           : enumerate 2^n outputs of fn
  - walsh_bridge(tt)             : map truth table -> bridge (exact)
  - character(c, x_bits, n)      : Walsh character chi_c(x)
  - evaluate_bridge(B, x_spin)   : evaluate bridge at a spin vector
  - grade_decomposition(B)       : group cells by Hamming weight
  - grade_energy(B)              : energy per grade (Σ B[c]² by weight)
  - reshape_4x4(B)               : layout 16-cell bridge as 4x4 matrix
  - is_power_of_two(N)           : validator

Conventions
-----------
Spin encoding: bit 0 <-> spin -1, bit 1 <-> spin +1.
Then f(x) = Σ_c  B[c] · prod_{i in mask c} spin(x_i),
and Parseval: Σ_c B[c]² = 1 for every Boolean function.

Bridge indexing
---------------
B is a length-2^n array indexed by c ∈ [0, 2^n). The binary representation
of c is the subset mask: bit i of c is 1 iff input i is in that coefficient's
product. So c = 0 is the constant term, c = (2^n - 1) is the all-inputs
product, and the Hamming weight of c is the grade.

Typical layout for visualization at n=4 (16 cells as 4x4):
    row = c & 0b11     (low two bits of mask)
    col = (c >> 2) & 0b11  (high two bits)

This layout has no special algebraic meaning; it's just a display convention.
"""
import math
import numpy as np


# ---------------------------------------------------------------------------
#  Validation
# ---------------------------------------------------------------------------

def is_power_of_two(N):
    """Return True iff N is a positive power of 2."""
    return N > 0 and (N & (N - 1)) == 0


# ---------------------------------------------------------------------------
#  Truth tables
# ---------------------------------------------------------------------------

def truth_table(fn, n_inputs):
    """
    Enumerate all 2^n outputs of fn([bits]) for n_inputs.

    Parameters
    ----------
    fn : callable
        Takes a list of n_inputs 0/1 bits, returns 0 or 1.
    n_inputs : int
        Number of input bits.

    Returns
    -------
    np.ndarray of shape (2^n,) and dtype int8.
    """
    if n_inputs < 1:
        raise ValueError(f"n_inputs must be >= 1, got {n_inputs}")
    return np.array(
        [fn([(v >> i) & 1 for i in range(n_inputs)])
         for v in range(2 ** n_inputs)],
        dtype=np.int8,
    )


# ---------------------------------------------------------------------------
#  Walsh-Hadamard bridge
# ---------------------------------------------------------------------------

def walsh_bridge(tt):
    """
    Compute the Walsh-Hadamard bridge of a Boolean truth table.

    For truth table `tt` of length N = 2^n:

        B[c] = (1/N) Σ_v  spin(tt[v]) · χ_c(v)

    where spin(b) = 2b − 1 and χ_c(v) = Π_{i in mask c} spin(v_i).

    Each B[c] is an integer multiple of 1/N. Parseval: Σ B[c]² = 1.

    Parameters
    ----------
    tt : array-like of 0/1
        Truth table. Length must be a power of 2.

    Returns
    -------
    np.ndarray of shape (N,) and dtype float64.
    """
    tt = np.asarray(tt, dtype=np.float64)
    N = len(tt)
    if not is_power_of_two(N):
        raise ValueError(f"Truth table length must be a power of 2, got {N}")
    n = int(math.log2(N))

    s = 2.0 * tt - 1.0
    B = np.zeros(N, dtype=np.float64)
    for c in range(N):
        acc = 0.0
        for v in range(N):
            chi = 1.0
            for i in range(n):
                if (c >> i) & 1:
                    chi *= 2.0 * ((v >> i) & 1) - 1.0
            acc += s[v] * chi
        B[c] = acc / N
    return B


def character(c, x_bits, n_inputs):
    """
    Walsh character χ_c(x) = Π_{i in mask c} spin(x_i).

    Parameters
    ----------
    c : int
        Mask in [0, 2^n).
    x_bits : sequence of 0/1
        Input values as bits.
    n_inputs : int
        Number of bits.

    Returns
    -------
    float : +1 or -1
    """
    chi = 1.0
    for i in range(n_inputs):
        if (c >> i) & 1:
            chi *= 2.0 * x_bits[i] - 1.0
    return chi


def evaluate_bridge(B, x_spin):
    """
    Evaluate the bridge at a spin-form input x_spin ∈ {-1, +1}^n.

        f(x) = Σ_c  B[c] · Π_{i in mask c} x_spin[i]

    For Boolean truth inputs, use spin(b) = 2b - 1 first.

    Returns
    -------
    float : evaluated value (in [-1, +1] for Boolean inputs on a bridge).
    """
    N = len(B)
    if not is_power_of_two(N):
        raise ValueError(f"Bridge length must be a power of 2, got {N}")
    n = int(math.log2(N))
    acc = 0.0
    for c in range(N):
        chi = 1.0
        for i in range(n):
            if (c >> i) & 1:
                chi *= x_spin[i]
        acc += B[c] * chi
    return acc


# ---------------------------------------------------------------------------
#  Grade decomposition
# ---------------------------------------------------------------------------

def grade_decomposition(B):
    """
    Group bridge cells by Hamming weight (Cl(n,0) grade).

    Returns
    -------
    dict : {grade_k : [(c, B[c]), ...]}

    The grades decompose 2^n cells into binomial groups:
        grade 0 : 1 cell       (the constant term, c = 0)
        grade 1 : n cells      (single-input linear terms)
        grade 2 : C(n, 2) cells (pairwise terms)
        ...
        grade n : 1 cell        (the full-input product, c = 2^n - 1)

    Total = Σ_k C(n, k) = 2^n. This is the {1, C(n,1), ..., C(n,n)}
    structure of the exterior algebra Cl(n, 0).
    """
    N = len(B)
    if not is_power_of_two(N):
        raise ValueError(f"Bridge length must be a power of 2, got {N}")
    grades = {}
    for c in range(N):
        w = bin(c).count('1')
        grades.setdefault(w, []).append((c, float(B[c])))
    return grades


def grade_energy(B):
    """
    Energy per grade: Σ_{c in grade k} B[c]².

    By Parseval, the total is 1.0 for any Boolean function's bridge.

    Returns
    -------
    dict : {grade_k : energy}

    Interpretation:
      grade 0 heavy  : function close to constant (biased)
      grade 1 heavy  : linear / threshold-like
      grade 2 heavy  : pairwise coupling dominant (often good for oscillator)
      grade n heavy  : high-order parity (sparse bridge)
    """
    N = len(B)
    if not is_power_of_two(N):
        raise ValueError(f"Bridge length must be a power of 2, got {N}")
    energy = {}
    for c in range(N):
        w = bin(c).count('1')
        energy[w] = energy.get(w, 0.0) + float(B[c]) ** 2
    return energy


# ---------------------------------------------------------------------------
#  Composition rules (exact algebra)
# ---------------------------------------------------------------------------

def walsh_conv(B_f, B_g):
    """
    Walsh convolution of two bridges:
        Walsh_conv[c] = Σ_k B_f[k] · B_g[c XOR k]

    Note: when you see "Walsh convolution" in signal processing, it
    usually means a different thing (pointwise multiply in frequency
    domain). This function computes the particular combination that
    arises when multiplying two spin-valued functions.

    Used in the XOR composition rule (see `bridge_xor`).
    """
    if len(B_f) != len(B_g):
        raise ValueError(f"Bridges must have equal length, "
                         f"got {len(B_f)} and {len(B_g)}")
    N = len(B_f)
    if not is_power_of_two(N):
        raise ValueError(f"Bridge length must be power of 2, got {N}")
    out = np.zeros(N)
    for c in range(N):
        acc = 0.0
        for k in range(N):
            acc += B_f[k] * B_g[c ^ k]
        out[c] = acc
    return out


def bridge_xor(B_f, B_g):
    """
    Bridge of (f XOR g), computed from the bridges of f and g.

    Exact identity (verified to machine precision):

        bridge(f XOR g) = -Walsh_conv(bridge(f), bridge(g))

    The minus sign arises because in spin(0)=-1, spin(1)=+1 convention,
        spin(a XOR b) = -spin(a) · spin(b)    (check: 4 cases)
    """
    return -walsh_conv(B_f, B_g)


def bridge_and(B_f, B_g):
    """
    Bridge of (f AND g), computed from the bridges of f and g.

    Derivation from spin algebra:
        spin(f AND g) = (1 + spin(f) + spin(g) + spin(f)·spin(g)) / 2 - 1

    Taking Walsh bridges (linearity):
        B(f AND g) = B(const=1)/2 + B(f)/2 + B(g)/2 + B(f·g)/2 - B(const=1)
                   = B(f)/2 + B(g)/2 + B(f·g)/2 - B(const=1/2 contribution)

    Where B(const=1) has B[0]=1, all other cells 0, and B(const=-1) has
    B[0]=-1. The "minus 1" at the end contributes -1 to cell 0 only.

    Spin product f·g corresponds to (NOT (f XOR g)) via spin identity, so:
        B(f·g) = -bridge_xor(B_f, B_g)   (since f·g = spin(NOT(f XOR g)) / 1)

    Cleaner derivation: B(f AND g) is the bridge of the function whose
    truth table is tt_f AND tt_g, which we can compute directly via the
    spin identity. Verified numerically below.
    """
    if len(B_f) != len(B_g):
        raise ValueError(f"Bridges must have equal length")
    N = len(B_f)
    # spin(f AND g)(v) = (1 + spin(f)(v) + spin(g)(v) + spin(f)(v)*spin(g)(v))/2 - 1
    # Bridge cell 0 of the constant-1 function is +1 (all other cells 0).
    # Bridge cell 0 of the constant-(-1) function is -1.
    B_const_1 = np.zeros(N); B_const_1[0] = 1.0

    # The product of spin-functions corresponds to Walsh convolution:
    #   spin(f) * spin(g) has bridge  Σ_k B_f[k] * B_g[c XOR k]  (no minus)
    B_product = walsh_conv(B_f, B_g)

    # Now: B(f AND g) = (B_const_1 + B_f + B_g + B_product)/2 - B_const_1
    #                 = (B_f + B_g + B_product)/2 - B_const_1/2
    return 0.5 * (B_f + B_g + B_product) - 0.5 * B_const_1


def bridge_or(B_f, B_g):
    """
    Bridge of (f OR g), computed from the bridges of f and g.

    Derivation from spin algebra:
        spin(f OR g) = 1 - (1 - spin(f))(1 - spin(g))/2 - 1
                    ... via De Morgan and spin-form expansion.

    Cleanest route: use f OR g = NOT(NOT f AND NOT g).
      B(NOT h)  flips signs only in cells where grade is odd... actually,
      spin(NOT h) = -spin(h), so B(NOT h) = -B(h).

    Then:
      B(f OR g) = -bridge_and(-B_f, -B_g)
                = -[0.5*(-B_f - B_g + walsh_conv(-B_f, -B_g)) - 0.5*B_const_1]
                = 0.5*(B_f + B_g - walsh_conv(B_f, B_g)) + 0.5*B_const_1

    (the walsh_conv of negated args is the same as positive because it's
    bilinear in the product; two negs cancel.)

    Verified numerically below.
    """
    if len(B_f) != len(B_g):
        raise ValueError(f"Bridges must have equal length")
    N = len(B_f)
    B_const_1 = np.zeros(N); B_const_1[0] = 1.0
    B_product = walsh_conv(B_f, B_g)
    return 0.5 * (B_f + B_g - B_product) + 0.5 * B_const_1


# ---------------------------------------------------------------------------
#  Layout helpers for visualization
# ---------------------------------------------------------------------------

def reshape_4x4(B):
    """
    Reshape a length-16 bridge to a 4×4 matrix for display.

    Layout convention:
        row = c & 0b11        (low two bits of mask)
        col = (c >> 2) & 0b11 (high two bits)

    So the top-left cell (row=0, col=0) is the grade-0 constant term
    (c = 0), and the bottom-right (row=3, col=3) is the grade-4
    all-inputs product (c = 15).

    This is a display layout only — it doesn't carry algebraic meaning
    beyond mask-bit partitioning.
    """
    B = np.asarray(B)
    if B.shape != (16,):
        raise ValueError(f"reshape_4x4 expects length 16, got {B.shape}")
    mat = np.zeros((4, 4))
    for c in range(16):
        row = c & 0b11
        col = (c >> 2) & 0b11
        mat[row, col] = B[c]
    return mat


# ---------------------------------------------------------------------------
#  Self-test
# ---------------------------------------------------------------------------

def _self_test():
    """Verify bridge, grade, and composition rules at machine precision."""
    # 1. Basic bridge: AND gate
    B_and = walsh_bridge([0, 0, 0, 1])
    expected = np.array([-0.5, 0.5, 0.5, 0.5])
    assert np.allclose(B_and, expected), \
        f"AND bridge wrong: got {B_and}, expected {expected}"

    # 2. Parseval holds
    for tt in [[0,0,0,1], [0,1,1,0], [0,1,1,1], [1,0,0,0]]:
        B = walsh_bridge(tt)
        assert abs((B**2).sum() - 1.0) < 1e-12, \
            f"Parseval fail on {tt}: Σ B² = {(B**2).sum()}"

    # 3. Grade structure of a 4-input bridge is {1,4,6,4,1}
    B16 = walsh_bridge([0]*15 + [1])  # AND4
    g = grade_decomposition(B16)
    assert [len(g[k]) for k in range(5)] == [1, 4, 6, 4, 1], \
        f"Grade sizes for 4-input wrong: {[len(g[k]) for k in range(5)]}"

    # 4. Grade-energy totals to 1 (Parseval check via grades)
    e = grade_energy(B16)
    assert abs(sum(e.values()) - 1.0) < 1e-12, \
        f"Grade energies don't sum to 1: {sum(e.values())}"

    # 5. XOR composition rule
    B_f = walsh_bridge(truth_table(lambda x: x[0] & x[1], 4))
    B_g = walsh_bridge(truth_table(lambda x: x[2] & x[3], 4))
    B_fxg_direct = walsh_bridge(
        truth_table(lambda x: (x[0] & x[1]) ^ (x[2] & x[3]), 4))
    B_fxg_algebraic = bridge_xor(B_f, B_g)
    assert np.allclose(B_fxg_direct, B_fxg_algebraic), \
        f"XOR composition rule failed"

    # 6. AND composition rule
    B_fag_direct = walsh_bridge(
        truth_table(lambda x: (x[0] & x[1]) & (x[2] & x[3]), 4))
    B_fag_algebraic = bridge_and(B_f, B_g)
    assert np.allclose(B_fag_direct, B_fag_algebraic), \
        f"AND composition rule failed: \n direct = {B_fag_direct}\n algebraic = {B_fag_algebraic}"

    # 7. OR composition rule
    B_fog_direct = walsh_bridge(
        truth_table(lambda x: (x[0] & x[1]) | (x[2] & x[3]), 4))
    B_fog_algebraic = bridge_or(B_f, B_g)
    assert np.allclose(B_fog_direct, B_fog_algebraic), \
        f"OR composition rule failed: \n direct = {B_fog_direct}\n algebraic = {B_fog_algebraic}"

    # 8. Evaluate_bridge round-trips: B(spin(x)) should equal spin(f(x))
    for v in range(16):
        x = [(v >> i) & 1 for i in range(4)]
        x_spin = [2 * b - 1 for b in x]
        truth_x = (x[0] & x[1]) ^ (x[2] & x[3])
        truth_spin = 2 * truth_x - 1
        got = evaluate_bridge(B_fxg_direct, x_spin)
        assert abs(got - truth_spin) < 1e-12, \
            f"bridge eval failed at v={v}: got {got}, expected {truth_spin}"

    print("bridge.py self-test: all 8 checks pass.")


if __name__ == "__main__":
    _self_test()
