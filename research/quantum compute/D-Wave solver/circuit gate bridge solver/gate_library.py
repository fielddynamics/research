"""
gate_library.py
================

Canonical reference library of Boolean gate bridges.

Contains:
  * All 16 two-input Boolean functions (exhaustive)
  * Common 3-input gates (AND, OR, XOR, MAJ, MUX, Ch, NOR, NAND)
  * Common 4-input gates (AND, OR, XOR, MAJ, threshold-2, parity variants,
    compositional patterns)

Each entry is a (name, truth_table, bridge) record, with the bridge
precomputed and verified against the closed-form walsh_bridge(tt).

Usage
-----
    from gate_library import GATES_2, GATES_3, GATES_4, lookup, all_gates

    B_and = lookup("AND", 2)             # get the 2-input AND bridge
    for (name, tt, B) in all_gates(4):   # iterate all 4-input gates
        ...

Why this exists
---------------
Recomputing the bridge for common gates every time wastes cycles and
introduces mistakes (sign conventions, spin encoding drift). This
library fixes the canonical reference data once.
"""
import math
import numpy as np
from bridge import walsh_bridge, truth_table


# ---------------------------------------------------------------------------
#  Truth-table factory helpers
# ---------------------------------------------------------------------------

def _tt_from_int(value, n_inputs):
    """Truth table from a packed integer.

    For n_inputs, the truth table has 2^n entries. `value` is an integer
    in [0, 2^(2^n)), where bit v of value is the function's output at
    input pattern v.

    This enumerates all 2^(2^n) Boolean functions compactly.
    """
    N = 1 << n_inputs
    return np.array([(value >> v) & 1 for v in range(N)], dtype=np.int8)


def _tt_from_fn(fn, n_inputs):
    """Truth table from a Python function of n_inputs bits."""
    return truth_table(fn, n_inputs)


# ---------------------------------------------------------------------------
#  n = 2: all 16 Boolean functions, in canonical order
# ---------------------------------------------------------------------------

# Convention: input pattern v encodes bits as (a=v&1, b=(v>>1)&1).
# So truth table indexed by v = a | (b<<1).
#
# The 16 two-input Boolean functions, numbered by their truth-table integer:
#   value  binary (tt[0..3])   common name
#       0  0 0 0 0             FALSE (constant 0)
#       1  1 0 0 0             NOR
#       2  0 1 0 0             A AND (NOT B)
#       3  1 1 0 0             NOT B
#       4  0 0 1 0             (NOT A) AND B
#       5  1 0 1 0             NOT A
#       6  0 1 1 0             XOR
#       7  1 1 1 0             NAND
#       8  0 0 0 1             AND
#       9  1 0 0 1             XNOR
#      10  0 1 0 1             A          (pass-through A)
#      11  1 1 0 1             A OR (NOT B)
#      12  0 0 1 1             B          (pass-through B)
#      13  1 0 1 1             (NOT A) OR B   (IMPLIES: A -> B)
#      14  0 1 1 1             OR
#      15  1 1 1 1             TRUE (constant 1)

_TWO_INPUT_NAMES = {
    0:  "FALSE",
    1:  "NOR",
    2:  "A_AND_NB",
    3:  "NOT_B",
    4:  "NA_AND_B",
    5:  "NOT_A",
    6:  "XOR",
    7:  "NAND",
    8:  "AND",
    9:  "XNOR",
    10: "A",
    11: "A_OR_NB",
    12: "B",
    13: "IMPLIES",   # A -> B  == (NOT A) OR B
    14: "OR",
    15: "TRUE",
}


def _build_n2_gates():
    out = {}
    for value in range(16):
        name = _TWO_INPUT_NAMES[value]
        tt = _tt_from_int(value, 2)
        B = walsh_bridge(tt)
        out[name] = (tt, B)
    return out


GATES_2 = _build_n2_gates()


# ---------------------------------------------------------------------------
#  n = 3: named gates
# ---------------------------------------------------------------------------

def _build_n3_gates():
    defs = {
        "AND3":  lambda x: x[0] & x[1] & x[2],
        "OR3":   lambda x: x[0] | x[1] | x[2],
        "XOR3":  lambda x: x[0] ^ x[1] ^ x[2],
        "NAND3": lambda x: 1 - (x[0] & x[1] & x[2]),
        "NOR3":  lambda x: 1 - (x[0] | x[1] | x[2]),
        "MAJ3":  lambda x: int((x[0] + x[1] + x[2]) >= 2),
        "MUX":   lambda x: x[1] if x[2] else x[0],           # c ? b : a
        "Ch":    lambda x: (x[0] & x[1]) | ((1 - x[0]) & x[2]),  # SHA256 Ch(e,f,g)
        "PASS_A": lambda x: x[0],
        "PASS_B": lambda x: x[1],
        "PASS_C": lambda x: x[2],
    }
    out = {}
    for name, fn in defs.items():
        tt = _tt_from_fn(fn, 3)
        out[name] = (tt, walsh_bridge(tt))
    return out


GATES_3 = _build_n3_gates()


# ---------------------------------------------------------------------------
#  n = 4: named gates and common compositional patterns
# ---------------------------------------------------------------------------

def _build_n4_gates():
    defs = {
        # Singleton 4-input
        "AND4":       lambda x: x[0] & x[1] & x[2] & x[3],
        "OR4":        lambda x: x[0] | x[1] | x[2] | x[3],
        "XOR4":       lambda x: x[0] ^ x[1] ^ x[2] ^ x[3],
        "NAND4":      lambda x: 1 - (x[0] & x[1] & x[2] & x[3]),
        "NOR4":       lambda x: 1 - (x[0] | x[1] | x[2] | x[3]),
        "MAJ4":       lambda x: int(sum(x) >= 2),
        "THRESHOLD3": lambda x: int(sum(x) >= 3),

        # Compositional patterns (useful references)
        "AND12_XOR_AND34": lambda x: (x[0] & x[1]) ^ (x[2] & x[3]),   # bent
        "OR12_XOR_OR34":   lambda x: (x[0] | x[1]) ^ (x[2] | x[3]),   # bent
        "XOR12_AND34":     lambda x: (x[0] ^ x[1]) & (x[2] & x[3]),
        "MAJ123_XOR_X4":   lambda x: int(sum(x[0:3]) >= 2) ^ x[3],
    }
    out = {}
    for name, fn in defs.items():
        tt = _tt_from_fn(fn, 4)
        out[name] = (tt, walsh_bridge(tt))
    return out


GATES_4 = _build_n4_gates()


# ---------------------------------------------------------------------------
#  Lookup helpers
# ---------------------------------------------------------------------------

_REGISTRY = {
    2: GATES_2,
    3: GATES_3,
    4: GATES_4,
}


def lookup(name, n_inputs):
    """Return the bridge for a named gate with n_inputs inputs.

    Raises KeyError if the gate is not in the registry.
    """
    if n_inputs not in _REGISTRY:
        raise KeyError(f"No library for n_inputs={n_inputs}")
    if name not in _REGISTRY[n_inputs]:
        available = ", ".join(sorted(_REGISTRY[n_inputs].keys()))
        raise KeyError(
            f"Unknown {n_inputs}-input gate '{name}'. "
            f"Available: {available}"
        )
    return _REGISTRY[n_inputs][name][1]


def lookup_tt(name, n_inputs):
    """Return the truth table for a named gate."""
    if n_inputs not in _REGISTRY or name not in _REGISTRY[n_inputs]:
        raise KeyError(f"Unknown gate: {name} at n={n_inputs}")
    return _REGISTRY[n_inputs][name][0]


def all_gates(n_inputs):
    """Iterate (name, truth_table, bridge) for all registered n-input gates."""
    if n_inputs not in _REGISTRY:
        return
    for name, (tt, B) in _REGISTRY[n_inputs].items():
        yield name, tt, B


def gate_names(n_inputs):
    """List the names of registered gates for a given n_inputs."""
    if n_inputs not in _REGISTRY:
        return []
    return list(_REGISTRY[n_inputs].keys())


# ---------------------------------------------------------------------------
#  Self-test
# ---------------------------------------------------------------------------

def _self_test():
    # 1. Every gate's bridge satisfies Parseval
    for n in [2, 3, 4]:
        for name, tt, B in all_gates(n):
            parseval = float((B ** 2).sum())
            assert abs(parseval - 1.0) < 1e-10, \
                f"Parseval fail on {name} (n={n}): got {parseval}"

    # 2. All 16 two-input functions have distinct bridges
    bridges_2 = [tuple(B.round(8)) for (_, B) in GATES_2.values()]
    assert len(set(bridges_2)) == 16, \
        "Two-input bridges should be distinct"

    # 3. Known-value checks
    assert np.allclose(lookup("AND", 2), [-0.5, 0.5, 0.5, 0.5])
    assert np.allclose(lookup("XOR", 2), [0, 0, 0, -1])
    assert np.allclose(lookup("NOR", 2), [-0.5, -0.5, -0.5, 0.5])
    assert np.allclose(lookup("XNOR", 2), [0, 0, 0, 1])

    # 4. Constants
    assert np.allclose(lookup("FALSE", 2), [-1, 0, 0, 0])
    assert np.allclose(lookup("TRUE", 2),  [ 1, 0, 0, 0])

    # 5. NOT relations: B(NOT f) = -B(f)
    #    NAND vs AND, NOR vs OR, etc.
    pairs = [("AND", "NAND"), ("OR", "NOR"), ("XOR", "XNOR")]
    for p, q in pairs:
        assert np.allclose(lookup(p, 2), -lookup(q, 2)), \
            f"NOT relation fails for {p}/{q}"

    # 6. n=3 gates exist and all distinct
    bridges_3 = [tuple(B.round(8)) for _, _, B in all_gates(3)]
    assert len(set(bridges_3)) == len(bridges_3), \
        "3-input bridges should be distinct"

    # 7. n=4: bent-function check
    #    (a AND b) XOR (c AND d) should have all 16 cells at magnitude 0.25
    B_bent = lookup("AND12_XOR_AND34", 4)
    mags = np.abs(B_bent)
    assert np.all(np.abs(mags - 0.25) < 1e-10), \
        "Canonical bent function should have uniform magnitude 0.25"

    print("gate_library.py self-test: all checks pass.")


if __name__ == "__main__":
    _self_test()

    # Print a summary table of what's in the library
    print()
    print("Canonical gate library")
    print("=" * 60)
    for n in [2, 3, 4]:
        names = gate_names(n)
        print(f"\n  n = {n} inputs ({len(names)} gates):")
        for name in names:
            B = lookup(name, n)
            nz = int(np.sum(np.abs(B) > 1e-6))
            print(f"    {name:<20s}  nonzero cells: {nz:>3d}/{len(B):>3d}")
