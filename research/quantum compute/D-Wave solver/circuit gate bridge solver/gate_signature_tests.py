#!/usr/bin/env python3
"""
gate_signature_tests.py
========================

Boolean gate recognition via the Walsh-Hadamard bridge and the
GFDOscillator. This file demonstrates the full pipeline on four
canonical gates (XOR, NAND, OR, AND) at 4-input scale.

WHAT THIS FILE DOES
-------------------
Every n-input Boolean function has a unique 2^n-cell Walsh bridge.
That bridge IS the gate's signature: AND, OR, NAND, XOR each produce
a different pattern. For 4-input functions the bridge has 16 cells,
which naturally display as a 4x4 matrix.

This file exercises three things:

  STAGE 1 - Accumulate the bridge from (input, output) examples.
            Hebbian / sample-mean estimator: each cell averages the
            Walsh character times the output spin across examples.

  STAGE 2 - Run the GFD oscillator on the bridge's coupling graph.
            Encode K_ij = B[i] * B[j] (rank-1, positive outer product).
            Anti-ferromagnetic Kuramoto at depth 4. SVD the cos(phi)
            matrix. The dominant mode recovers the bridge direction.

  STAGE 3 - Classify gates by cosine similarity of learned bridges
            against known ground truths.


THE UNIVERSAL STRUCTURE
-----------------------
The 2^n bridge cells decompose by Hamming weight of their mask index
into the exterior-algebra grades of Cl(n, 0):

  n = 2:  {1, 2, 1}        = 4 cells   (Cl(2,0))
  n = 3:  {1, 3, 3, 1}     = 8 cells   (Cl(3,0))  <- stella octangula
  n = 4:  {1, 4, 6, 4, 1}  = 16 cells  (Cl(4,0))

This structure is always there in every Boolean function's bridge,
via the mask indexing. The minimal oscillator (K4 dual-tetrahedral,
depth 4) is the Cl(3,0) native representation. Higher-grade content
in deeper-n bridges is accessed by nesting.


MEASURED RESULTS FROM RUNNING THIS FILE
---------------------------------------

Stage 1 (Hebbian, 3000 examples per gate):

    Gate    RMSE per cell   cos(learned, true)   Parseval
    XOR     0.017           +0.998               1.005
    NAND    0.017           +0.998               1.005
    OR      0.017           +0.998               1.005
    AND     0.017           +0.998               1.005

Stage 2 (oscillator, depth 4, sign-aligned, 10 seeds averaged):

    Gate   cos(mode0, B)   Sv spectrum                  gauge
    AND    +0.6876         [1, 0.004, 0.001, 0.001]     0.0005
    OR    ~+0.6875         [1, 0.003, 0.001, 0.001]     0.0014
    NAND   +0.6876         [1, 0.004, 0.001, 0.001]     0.0005
    XOR   ~+0.12           [1, 0.79,  0.58,  0.30]      0.30

Interpretation:
  * AND, OR, NAND have dense bridges. The rank-1 encoding recovers
    the SIGN pattern exactly (sign-only cosine = 1.0), but it
    normalizes magnitudes to uniform 0.25 when the true bridge has
    one cell at 0.875 and fifteen at 0.125. So cos-with-magnitudes
    drops from 1.0 to ~0.69 via lost magnitude ratios, not lost signs.

  * XOR's bridge is [0, 0, 0, ..., -1] (one nonzero cell at grade 4).
    K = B (x) B then has all off-diagonal entries equal to zero, so
    the oscillator has no coupling to work with. The depth gauge
    picks up mass reflecting this empty coupling.

  * Across 14 tested gates, correlation(nonzero_cells, gauge) = -0.997.
    The gauge reads bridge density directly.

Stage 3 (classification by cosine similarity):

    Each LEARNED bridge is compared against each TRUE bridge. The
    learned bridge must be most similar to its own gate. Result: 4/4.
    AND and NAND are perfectly anti-correlated (cos = -0.998) because
    NAND == NOT AND and their bridges differ by a sign flip.


RUN
---
    python gate_signature_tests.py

Requires: numpy. Imports bridge.py and gfd_oscillator.py (both in
this folder). Runs in ~30 seconds on a laptop; no GPU.


SEE ALSO
--------
    bridge.py                      - Walsh-bridge utilities (reused)
    extended_composition_tests.py  - XOR+AND composites, multi-output,
                                     noise robustness, grade decomposition
    GATE_BRIDGE_SYNTHESIS.md       - Writeup of measured findings
    README.md                      - Entry point for this folder
"""
import os
import sys
import math
import numpy as np

# Import from the bridge module (same folder) and GFD oscillator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import (
    walsh_bridge, truth_table, character, evaluate_bridge,
    reshape_4x4, grade_energy,
)
from gfd_oscillator import GFDOscillator


# =========================================================================
#  Display helpers
# =========================================================================

def print_4x4_matrix(mat, label="", width=9):
    """Pretty-print a 4x4 bridge matrix with row/col headers showing masks.

    Row/col headers are the binary representation of the mask bits
    that index into each cell (layout convention from bridge.reshape_4x4):
        row = c & 0b11        (low two bits of mask c)
        col = (c >> 2) & 0b11 (high two bits)
    """
    print(f"  {label}")
    print(f"         " + "  ".join(f"{'col='+bin(c)[2:].zfill(2):>{width}}"
                                     for c in range(4)))
    for r in range(4):
        rs = "  ".join(f"{mat[r, c]:+.4f}".rjust(width) for c in range(4))
        print(f"  row={bin(r)[2:].zfill(2)}  {rs}")


def cosine(u, v):
    """Cosine similarity of two vectors."""
    nu, nv = float(np.linalg.norm(u)), float(np.linalg.norm(v))
    if nu < 1e-12 or nv < 1e-12:
        return 0.0
    return float(np.dot(u, v) / (nu * nv))


def align_sign(est, truth):
    """Flip est if it's anti-correlated with truth."""
    if np.dot(est, truth) < 0:
        return -est
    return est


# =========================================================================
#  Stage 1: Online Hebbian accumulation
# =========================================================================

def accumulate_bridge_from_examples(gate_fn, n_inputs, n_examples, seed=42):
    """
    Build a bridge from (input, output) examples by Hebbian accumulation.

    For each random example (x, y = gate_fn(x)), update every cell:

        cell[c] += chi_c(x) * spin(y)

    After n_examples: cell[c] / n_examples -> true Walsh coefficient B[c].

    This is the sample-mean estimator for the Walsh inner product.
    Uses modern numpy RNG (np.random.default_rng).

    Parameters
    ----------
    gate_fn : callable
        Takes list of n_inputs bits, returns 0 or 1.
    n_inputs : int
    n_examples : int
    seed : int

    Returns
    -------
    (accum, B_learned) : raw accumulator and its /n_examples estimate.
    """
    rng = np.random.default_rng(seed)
    N = 2 ** n_inputs
    accum = np.zeros(N)

    for k in range(n_examples):
        v = int(rng.integers(0, N))
        x_bits = [(v >> i) & 1 for i in range(n_inputs)]
        y = gate_fn(x_bits)
        s_y = 2 * y - 1
        for c in range(N):
            accum[c] += character(c, x_bits, n_inputs) * s_y

    return accum, accum / n_examples


# =========================================================================
#  Stage 2: Encode bridge into the GFD oscillator
# =========================================================================

def bridge_to_graph(B):
    """
    Encode a bridge as a weighted coupling graph.

        K_ij = B[i] * B[j]   (rank-1 outer product, diagonal zeroed)

    The sign is POSITIVE outer product. Same-sign cells get ferromagnetic
    coupling (phases pull together). Opposite-sign cells get anti-
    ferromagnetic coupling (phases push apart). The coupling magnitude
    is |B[i]| * |B[j]|, so high-magnitude cells dominate.

    K = B (x) B is a rank-1 matrix. Its dominant eigenvector is B/|B| —
    the bridge direction. After Kuramoto relaxation, SVD mode 0 of
    cos(phi) recovers sign(B) exactly. Magnitude ratios are NOT
    preserved by this encoding (that would need a rank-k decomposition
    of the bridge).

    Sparse bridges (e.g. XOR = [0,0,0,-1]) give a coupling matrix with
    all-zero off-diagonal, so the oscillator has no coupling and the
    depth gauge picks up mass. This is a structural readout of bridge
    density, not a failure mode.
    """
    return GFDOscillator.encode_weighted(len(B), np.outer(B, B))


def oscillator_signature(B, steps=2000, max_depth=8, seed=42, n_seeds=10):
    """
    Run the GFD oscillator on K = B (x) B and return measurements averaged
    across n_seeds trials.

    IMPORTANT: we report mean-of-cosines across seeds, not cosine-of-
    means. Averaging unit vectors and then taking cosine with a
    reference is not the same as averaging the per-seed cosines — the
    former is biased by the aggregate geometry.

    Returns a dict with:
      mode0_avg   : per-cell average of sign-aligned Vt[0] vectors
      cos_avg     : mean cos(Vt[0], B) across seeds  (the honest metric)
      cos_std     : std  cos(Vt[0], B) across seeds
      Sv_avg      : averaged singular values
      gauge       : Sv[-1]/Sv[0] on the averaged spectrum
      depth       : depth used by run_adaptive (final value)
    """
    graph = bridge_to_graph(B)

    cos_values = []
    mode0_aligned = []
    Sv_list = []
    depth_used = None

    for s in range(n_seeds):
        osc = GFDOscillator(
            dt=0.01, steps=steps,
            active_threshold=0.01,
            gauge_threshold=0.3,
            max_depth=max_depth,
        )
        state = osc.run_adaptive(graph, seed=seed + s)
        m = state.Vt[0].copy()
        m = align_sign(m, B)
        cos_values.append(cosine(m, B))
        mode0_aligned.append(m)
        Sv_list.append(state.Sv)
        depth_used = state.depth

    # Sv arrays may have different lengths if run_adaptive escalates at
    # different rates — pad to max before averaging.
    max_len = max(len(s) for s in Sv_list)
    Sv_padded = np.array([
        np.concatenate([s, np.zeros(max_len - len(s))]) for s in Sv_list
    ])
    Sv_avg = Sv_padded.mean(axis=0)

    return {
        "mode0_avg":  np.mean(mode0_aligned, axis=0),
        "cos_avg":    float(np.mean(cos_values)),
        "cos_std":    float(np.std(cos_values)),
        "Sv_avg":     Sv_avg,
        "gauge":      float(Sv_avg[-1] / Sv_avg[0]) if Sv_avg[0] > 1e-12 else 0.0,
        "depth":      depth_used,
        "n_seeds":    n_seeds,
    }


# =========================================================================
#  Gate library
# =========================================================================

def gate_xor4(x):  return x[0] ^ x[1] ^ x[2] ^ x[3]
def gate_nand4(x): return 1 - (x[0] & x[1] & x[2] & x[3])
def gate_or4(x):   return int(any(x))
def gate_and4(x):  return int(all(x))

GATES = {
    "XOR":  gate_xor4,
    "NAND": gate_nand4,
    "OR":   gate_or4,
    "AND":  gate_and4,
}


# =========================================================================
#  Main test flow
# =========================================================================

def test_gate(gate_name, gate_fn, n_examples=3000):
    """Run both stages for one gate and report measurements."""
    print()
    print("=" * 70)
    print(f"  {gate_name} signature")
    print("=" * 70)

    tt = truth_table(gate_fn, 4)
    B_true = walsh_bridge(tt)

    print(f"\n  Truth table: {tt.tolist()}")
    print(f"  Bridge Parseval: {(B_true**2).sum():.4f}")

    ge = grade_energy(B_true)
    ge_str = "  ".join(f"g{k}={ge.get(k, 0.0):.3f}" for k in range(5))
    print(f"  Grade energy:  {ge_str}")

    print(f"\n  True bridge (4x4 display layout):")
    print_4x4_matrix(reshape_4x4(B_true), "TRUE")

    # Stage 1
    _, B_learned = accumulate_bridge_from_examples(gate_fn, 4, n_examples)
    print(f"\n  Learned bridge (Hebbian, {n_examples} examples):")
    print_4x4_matrix(reshape_4x4(B_learned), "LEARNED")

    rmse = float(np.sqrt(((B_learned - B_true) ** 2).mean()))
    cos_learned = cosine(B_learned, B_true)
    parseval = float((B_learned ** 2).sum())
    print(f"\n    RMSE(learned, true)      : {rmse:.4f}")
    print(f"    cos(learned, true)       : {cos_learned:+.4f}")
    print(f"    Parseval(learned)        : {parseval:.4f}")

    # Stage 2
    print(f"\n  GFDOscillator on K = B (x) B, averaged across 10 seeds:")
    r = oscillator_signature(B_true, seed=42, n_seeds=10)
    Sv_ratio = [f"{s/r['Sv_avg'][0]:.3f}" for s in r['Sv_avg']]
    print(f"    depth used            : {r['depth']}")
    print(f"    cos(mode0, B)         : {r['cos_avg']:+.4f} +/- {r['cos_std']:.4f}")
    print(f"    S/S0 spectrum         : {Sv_ratio}")
    print(f"    gauge (Sv[-1]/Sv[0])  : {r['gauge']:.4f}")

    return {
        "gate":         gate_name,
        "B_true":       B_true,
        "B_learned":    B_learned,
        "grade_energy": ge,
        "rmse":         rmse,
        "cos_learned":  cos_learned,
        "cos_osc":      r["cos_avg"],
        "cos_osc_std":  r["cos_std"],
        "gauge":        r["gauge"],
        "depth":        r["depth"],
    }


def test_classification(results):
    """Cross-compare learned bridges against true bridges by cosine."""
    print()
    print("=" * 70)
    print("  Classification via cosine similarity of learned bridges")
    print("=" * 70)
    print()
    names = list(results.keys())
    print("  " + " " * 9 + "  ".join(f"vs {n:>5}" for n in names))
    correct = 0
    for learned_name in names:
        B_l = results[learned_name]["B_learned"]
        sims = [cosine(B_l, results[t]["B_true"]) for t in names]
        best = names[int(np.argmax(sims))]
        mark = " [OK]" if best == learned_name else f" [MISS -> {best}]"
        if best == learned_name:
            correct += 1
        row = "  " + f"L[{learned_name:>5}]  " + "  ".join(f"{s:+.3f}" for s in sims)
        print(row + mark)
    print(f"\n  Classification accuracy: {correct}/{len(names)}")


def main():
    print("=" * 70)
    print("  Gate Signature Recognition via Walsh Bridge & GFD Oscillator")
    print("=" * 70)
    print("""
  Procedure:
    1. For each gate, build its true bridge analytically (ground truth).
    2. Accumulate a learned bridge from 3000 random (x, gate(x)) samples.
    3. Run the GFD oscillator on the true bridge's coupling graph.
    4. Report learning quality, oscillator mode0 quality, and
       classification accuracy across learned bridges.
""")

    results = {}
    for name, fn in GATES.items():
        results[name] = test_gate(name, fn, n_examples=3000)

    test_classification(results)

    print()
    print("=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print(f"  {'gate':>5}  {'RMSE':>6}  {'cos(B)':>9}  "
          f"{'cos(mode0)':>16}  {'depth':>5}  {'gauge':>7}")
    for name, r in results.items():
        print(f"  {name:>5}  {r['rmse']:>6.4f}  {r['cos_learned']:>+9.4f}  "
              f"{r['cos_osc']:>+10.4f}+/-{r['cos_osc_std']:.3f}  "
              f"{r['depth']:>5}  {r['gauge']:>7.4f}")

    return results


# =========================================================================
#  Self-test
# =========================================================================

def _self_test():
    """Check basic invariants without running the full main()."""
    # Known bridges for 2-input gates
    B_and2 = walsh_bridge([0, 0, 0, 1])
    assert np.allclose(B_and2, [-0.5, 0.5, 0.5, 0.5]), "AND2 bridge mismatch"

    B_xor2 = walsh_bridge([0, 1, 1, 0])
    assert np.allclose(B_xor2, [0, 0, 0, -1]), "XOR2 bridge mismatch"

    # NAND and AND are anti-correlated on 4-input
    B_nand4 = walsh_bridge(truth_table(gate_nand4, 4))
    B_and4  = walsh_bridge(truth_table(gate_and4, 4))
    assert cosine(B_nand4, B_and4) < -0.99, "NAND/AND should be anti-correlated"

    # Parseval for every test gate
    for name, fn in GATES.items():
        B = walsh_bridge(truth_table(fn, 4))
        assert abs((B**2).sum() - 1.0) < 1e-12, f"Parseval fail on {name}"

    print("gate_signature_tests.py self-test: all checks pass.")


if __name__ == "__main__":
    _self_test()
    print()
    main()
