#!/usr/bin/env python3
"""
extended_composition_tests.py
==============================

Extended tests of the GFD oscillator on composite Boolean functions.

THE KEY POINT
-------------
Every 4-input Boolean function has a 16-cell Walsh bridge, regardless
of how the function is constructed. Composition — XOR, AND, OR of
sub-results — produces a different bridge, but it's still 16 cells in
the {1, 4, 6, 4, 1} grade decomposition of Cl(4,0).

So XOR(x0, x1) xor AND(x2, x3) is still a 4-input 1-output function
with a 16-cell bridge. The question is what that bridge looks like
spectrally — and whether it combines cleanly from the bridges of its
constituents.


TESTS IN THIS FILE
------------------

TEST A - XOR composition rule
  Verified to machine precision:
      bridge(f XOR g) = -Walsh_conv(bridge(f), bridge(g))
  where Walsh_conv[c] = sum_k bridge(f)[k] * bridge(g)[c XOR k]
  (See bridge.bridge_xor; the minus is from the spin identity
   spin(a XOR b) = -spin(a) * spin(b).)

TEST A2 - AND composition rule
  Verified to machine precision:
      bridge(f AND g) = (1/2)(B_f + B_g + Walsh_conv(B_f, B_g))
                        - (1/2) e_0
  where e_0 is the delta at the constant cell.
  (See bridge.bridge_and.)

TEST A3 - OR composition rule
  Also verified.
  (See bridge.bridge_or.)

TEST B - Composite-gate signatures
  For a range of composite 4-input functions, measure:
    * bridge shape (magnitudes, sparsity)
    * cos(mode0, B)   [mean over 10 seeds, with std]
    * depth gauge
    * grade-energy distribution
  Reveals which compositional forms are dense (grade-2 heavy) and
  which are sparse (grade-4 heavy like pure parity).

TEST C - Multi-output functions
  A 4-in 4-out function has FOUR 16-cell bridges (one per output).
  Show that each output's bridge is separately recoverable and the
  cross-output cosine-similarity matrix distinguishes them.

TEST D - Recoverability vs bridge sparsity
  Across all tested composite gates, measure:
    correlation(nonzero_cells, gauge)
    correlation(nonzero_cells, cos(mode0, B))
  Group gates by dominant grade.

TEST E - Composition self-organization under noise
  For the composite (x0 XOR x1) XOR (x2 AND x3), present examples
  with some fraction eta of labels flipped. Measure cos with true
  bridge as a function of n_examples and noise level eta.
"""
import os
import sys
import math
import time
import numpy as np
from itertools import combinations
from collections import defaultdict

# Shared utilities
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import (
    walsh_bridge, truth_table, character, evaluate_bridge,
    grade_energy, grade_decomposition,
    walsh_conv, bridge_xor, bridge_and, bridge_or,
)
from gfd_oscillator import GFDOscillator


# =====================================================================
# Oscillator helper — uses shared bridge module
# =====================================================================

def bridge_to_graph(B):
    """K = B (x) B, diagonal zeroed, wrapped as a GFD graph."""
    K = np.outer(B, B)
    np.fill_diagonal(K, 0)
    return GFDOscillator.encode_weighted(len(B), K)


def run_oscillator(B, depth=4, n_seeds=10, steps=3000):
    """Run the GFD oscillator on K = B (x) B.

    Returns per-seed statistics and the cos(mode0, B) with MEAN OVER
    SEEDS (NOT cos of mean — that's a geometric artifact when averaging
    unit vectors).
    """
    graph = bridge_to_graph(B)
    osc = GFDOscillator(dt=0.01, steps=steps)

    cos_per_seed = []
    Sv_per_seed = []
    for seed in range(n_seeds):
        state = osc.run_phase(graph, depth=depth, seed=seed)
        m = state.Vt[0].copy()
        if np.dot(m, B) < 0:
            m = -m
        # Cosine of this seed's recovered direction against the bridge
        nm, nB = float(np.linalg.norm(m)), float(np.linalg.norm(B))
        if nm < 1e-12 or nB < 1e-12:
            cos_per_seed.append(0.0)
        else:
            cos_per_seed.append(float(np.dot(m, B) / (nm * nB)))
        Sv_per_seed.append(state.Sv)

    Sv_avg = np.mean(Sv_per_seed, axis=0)
    gauge = float(Sv_avg[-1] / Sv_avg[0]) if Sv_avg[0] > 1e-10 else 0.0
    n_active = (int(np.sum(Sv_avg / Sv_avg[0] > 0.01))
                if Sv_avg[0] > 1e-10 else 0)

    return {
        "cos_mean":  float(np.mean(cos_per_seed)),
        "cos_std":   float(np.std(cos_per_seed)),
        "Sv":        Sv_avg,
        "gauge":     gauge,
        "n_active":  n_active,
    }


# =====================================================================
# Composite gate library (expanded)
# =====================================================================

COMPOSITES = {
    # Singleton 4-input references
    "AND4":     lambda x: x[0] & x[1] & x[2] & x[3],
    "OR4":      lambda x: x[0] | x[1] | x[2] | x[3],
    "XOR4":     lambda x: x[0] ^ x[1] ^ x[2] ^ x[3],
    "MAJ4":     lambda x: int(sum(x) >= 2),

    # Pairwise compositions — the "XOR + AND" family
    "XOR12_AND34_XOR": lambda x: (x[0] ^ x[1]) ^ (x[2] & x[3]),
    "XOR12_AND34_AND": lambda x: (x[0] ^ x[1]) & (x[2] & x[3]),
    "XOR12_AND34_OR":  lambda x: (x[0] ^ x[1]) | (x[2] & x[3]),

    # Bent-like compositions (dense bridges, grade-2 dominant)
    "AND12_XOR_AND34": lambda x: (x[0] & x[1]) ^ (x[2] & x[3]),
    "OR12_XOR_OR34":   lambda x: (x[0] | x[1]) ^ (x[2] | x[3]),
    "XOR12_AND_XOR34": lambda x: (x[0] ^ x[1]) & (x[2] ^ x[3]),

    # Decomposition to XOR4
    "XOR12_XOR_XOR34": lambda x: (x[0] ^ x[1]) ^ (x[2] ^ x[3]),  # = XOR4

    # Mixed-depth / asymmetric
    "MAJ123_XOR_X4":  lambda x: int(sum(x[0:3]) >= 2) ^ x[3],
    "AND123_OR_X4":   lambda x: (x[0] & x[1] & x[2]) | x[3],
    "NAND123_AND_X4": lambda x: (1 - (x[0] & x[1] & x[2])) & x[3],
}


# =====================================================================
# TEST A: XOR, AND, OR composition rules
# =====================================================================

def test_a_composition_rules():
    print("=" * 72)
    print("  TEST A: Walsh composition rules (XOR, AND, OR)")
    print("=" * 72)
    print("""
  Three exact algebraic identities, each verified to machine precision:

    XOR:  bridge(f XOR g) = -Walsh_conv(bridge(f), bridge(g))
    AND:  bridge(f AND g) = (1/2)(B_f + B_g + Walsh_conv(B_f, B_g))
                            - (1/2) e_0
    OR :  bridge(f OR  g) = (1/2)(B_f + B_g - Walsh_conv(B_f, B_g))
                            + (1/2) e_0

  where e_0 is the delta at cell 0. The derivations come from the spin
  identities
      spin(a XOR b) = -spin(a) spin(b)
      spin(a AND b) = (1 + spin(a) + spin(b) + spin(a) spin(b))/2 - 1
      spin(a OR  b) = 1 - (1 - spin(a))(1 - spin(b))/2 - 1
""")

    f = lambda x: x[0] & x[1]
    g = lambda x: x[2] & x[3]

    B_f = walsh_bridge(truth_table(f, 4))
    B_g = walsh_bridge(truth_table(g, 4))

    test_cases = [
        ("XOR", lambda a, b: a ^ b, bridge_xor),
        ("AND", lambda a, b: a & b, bridge_and),
        ("OR",  lambda a, b: a | b, bridge_or),
    ]

    for name, bool_op, bridge_op in test_cases:
        composite_fn = lambda x, op=bool_op: op(f(x), g(x))
        tt_composite = truth_table(composite_fn, 4)
        B_direct = walsh_bridge(tt_composite)
        B_algebraic = bridge_op(B_f, B_g)
        err = float(np.max(np.abs(B_direct - B_algebraic)))
        ok = "OK" if err < 1e-10 else "FAIL"
        print(f"  {name:>3s} composition err: {err:.2e}  [{ok}]")

    # Cross-check XOR on more pairs
    print("\n  Additional XOR composition checks:")
    pairs = [
        ("(x0|x1) XOR (x2^x3)",
            lambda x: x[0] | x[1], lambda x: x[2] ^ x[3]),
        ("MAJ(x0,x1,x2) XOR x3",
            lambda x: int(sum(x[0:3]) >= 2), lambda x: x[3]),
    ]
    for label, fa, fb in pairs:
        Bf = walsh_bridge(truth_table(fa, 4))
        Bg = walsh_bridge(truth_table(fb, 4))
        composite = lambda x, fa=fa, fb=fb: fa(x) ^ fb(x)
        Bc_direct = walsh_bridge(truth_table(composite, 4))
        Bc_alg = bridge_xor(Bf, Bg)
        err = float(np.max(np.abs(Bc_direct - Bc_alg)))
        ok = "OK" if err < 1e-10 else "FAIL"
        print(f"    {label:40s} err: {err:.2e}  [{ok}]")

    print("""
  Practical consequence: compound gate signatures are built from
  component signatures by these algebraic operations. No truth-table
  re-sampling needed. This is how the Walsh bridge factors gate
  composition.
""")


# =====================================================================
# TEST B: Composite gate signatures
# =====================================================================

def test_b_composites():
    print("=" * 72)
    print("  TEST B: Oscillator on composite 4-input gates")
    print("  (cos(mode0, B) = mean +/- std over 10 seeds)")
    print("=" * 72)
    print(f"\n  {'gate':>22s}  {'shape':>22s}  {'nz':>3s}  "
          f"{'cos(m0,B)':>16s}  {'gauge':>7s}  {'dominant grade':>14s}")

    results = []
    for name, fn in COMPOSITES.items():
        tt = truth_table(fn, 4)
        B = walsh_bridge(tt)
        nz = int(np.sum(np.abs(B) > 1e-6))
        r = run_oscillator(B, depth=4, n_seeds=10)

        ge = grade_energy(B)
        top_grade = max(ge.items(), key=lambda kv: kv[1])[0]

        # Compact bridge shape (unique magnitudes with counts)
        unique = {}
        for c in range(16):
            m = round(abs(B[c]), 4)
            unique[m] = unique.get(m, 0) + 1
        shape_str = ",".join(f"{count}x{mag:.3f}"
                             for mag, count in sorted(unique.items(), reverse=True)
                             if mag > 1e-6)[:22]

        cos_str = f"{r['cos_mean']:>+7.4f}+/-{r['cos_std']:.3f}"
        print(f"  {name:>22s}  {shape_str:>22s}  {nz:>3d}  "
              f"{cos_str:>16s}  {r['gauge']:>7.4f}  {top_grade:>14d}")
        results.append({
            "name": name, "B": B, "nz": nz,
            "cos_mean": r["cos_mean"], "cos_std": r["cos_std"],
            "gauge": r["gauge"], "grade_energy": ge, "top_grade": top_grade,
        })

    return results


# =====================================================================
# TEST C: Multi-output functions
# =====================================================================

def test_c_multi_output():
    print()
    print("=" * 72)
    print("  TEST C: Multi-output 4-in 4-out — each output has its own bridge")
    print("=" * 72)

    fns = {
        "XOR_all": lambda x: x[0] ^ x[1] ^ x[2] ^ x[3],
        "AND_all": lambda x: x[0] & x[1] & x[2] & x[3],
        "OR_all":  lambda x: x[0] | x[1] | x[2] | x[3],
        "MAJ":     lambda x: int(sum(x) >= 2),
    }

    print(f"\n  {'output':>10s}  {'bridge mag pattern':>24s}  "
          f"{'cos(m0,B)':>16s}  {'gauge':>7s}")
    bridges = {}
    for name, fn in fns.items():
        B = walsh_bridge(truth_table(fn, 4))
        bridges[name] = B
        r = run_oscillator(B, depth=4, n_seeds=10)

        unique = {}
        for c in range(16):
            m = round(abs(B[c]), 4)
            unique[m] = unique.get(m, 0) + 1
        shape_str = ",".join(f"{c}x{m:.3f}"
                             for m, c in sorted(unique.items(), reverse=True)
                             if m > 1e-6)[:24]

        cos_str = f"{r['cos_mean']:>+7.4f}+/-{r['cos_std']:.3f}"
        print(f"  {name:>10s}  {shape_str:>24s}  {cos_str:>16s}  {r['gauge']:>7.4f}")

    print(f"\n  Cross-output cosine similarity (are outputs distinguishable?):")
    names = list(bridges.keys())
    print("  " + " " * 12 + "  ".join(f"{n:>8s}" for n in names))
    for n1 in names:
        row = "  " + f"{n1:>10s}  " + "  ".join(
            f"{float(np.dot(bridges[n1], bridges[n2]) / (np.linalg.norm(bridges[n1]) * np.linalg.norm(bridges[n2]) + 1e-12)):>+8.3f}"
            for n2 in names
        )
        print(row)


# =====================================================================
# TEST D: Sparsity / recoverability correlation
# =====================================================================

def test_d_sparsity(results_from_b):
    print()
    print("=" * 72)
    print("  TEST D: Recoverability vs bridge sparsity")
    print("=" * 72)
    print()
    print(f"  {'gate':>22s}  {'nz':>3s}  {'top grade':>10s}  "
          f"{'cos':>9s}  {'gauge':>7s}")

    data = []
    for r in results_from_b:
        print(f"  {r['name']:>22s}  {r['nz']:>3d}  {r['top_grade']:>10d}  "
              f"{r['cos_mean']:>+9.4f}  {r['gauge']:>7.4f}")
        data.append((r["name"], r["nz"], r["top_grade"],
                     r["cos_mean"], r["gauge"]))

    nzs = np.array([d[1] for d in data])
    coss = np.array([d[3] for d in data])
    gauges = np.array([d[4] for d in data])
    print(f"\n  Correlation(nz, cos)   : {np.corrcoef(nzs, coss)[0,1]:+.3f}")
    print(f"  Correlation(nz, gauge) : {np.corrcoef(nzs, gauges)[0,1]:+.3f}")
    print(f"  Correlation(gauge, cos): {np.corrcoef(gauges, coss)[0,1]:+.3f}")

    by_grade = defaultdict(list)
    for name, nz, tg, cs, g in data:
        by_grade[tg].append((name, cs, g))

    print(f"\n  Grouped by dominant grade:")
    for tg in sorted(by_grade.keys()):
        gates = by_grade[tg]
        mean_cos = np.mean([g[1] for g in gates])
        mean_gauge = np.mean([g[2] for g in gates])
        print(f"    grade {tg}: n={len(gates):>2d}  "
              f"mean cos={mean_cos:+.4f}  mean gauge={mean_gauge:.4f}")


# =====================================================================
# TEST E: Noise robustness
# =====================================================================

def test_e_noise():
    print()
    print("=" * 72)
    print("  TEST E: Composite self-organization under label noise")
    print("  Function: (x0 XOR x1) XOR (x2 AND x3)")
    print("=" * 72)

    fn = lambda x: (x[0] ^ x[1]) ^ (x[2] & x[3])
    n = 4
    N = 16
    B_true = walsh_bridge(truth_table(fn, n))

    def accumulate(n_examples, eta, seed=42):
        rng = np.random.default_rng(seed)
        accum = np.zeros(N)
        for k in range(n_examples):
            v = int(rng.integers(0, N))
            x_bits = [(v >> i) & 1 for i in range(n)]
            y = fn(x_bits)
            if rng.random() < eta:
                y = 1 - y
            s_y = 2 * y - 1
            for c in range(N):
                accum[c] += character(c, x_bits, n) * s_y
        return accum / n_examples

    print(f"\n  {'examples':>10s}  {'eta=0.00':>10s}  {'eta=0.05':>10s}  "
          f"{'eta=0.10':>10s}  {'eta=0.20':>10s}  {'eta=0.30':>10s}")
    print(f"  {'':>10s}  " + "  ".join(f"{'cos/rmse':>10s}" for _ in range(5)))

    for n_ex in [500, 1000, 3000, 10000]:
        row = [f"{n_ex:>10d}"]
        for eta in [0.00, 0.05, 0.10, 0.20, 0.30]:
            B_learned = accumulate(n_ex, eta)
            cos_sim = float(np.dot(B_learned, B_true) /
                            (np.linalg.norm(B_learned) * np.linalg.norm(B_true) + 1e-12))
            rmse = float(np.sqrt(((B_learned - B_true) ** 2).mean()))
            row.append(f"{cos_sim:+.2f}/{rmse:.2f}")
        print("  " + "  ".join(row))


# =====================================================================
# MAIN
# =====================================================================

def main():
    t_start = time.time()
    test_a_composition_rules()
    results_b = test_b_composites()
    test_c_multi_output()
    test_d_sparsity(results_b)
    test_e_noise()

    print()
    print("=" * 72)
    print(f"  Total time: {time.time() - t_start:.1f}s")
    print("=" * 72)


# =====================================================================
# Self-test
# =====================================================================

def _self_test():
    """Verify composition rules at small scale."""
    # XOR rule, direct vs algebraic
    f = lambda x: x[0] & x[1]
    g = lambda x: x[2] & x[3]
    B_f = walsh_bridge(truth_table(f, 4))
    B_g = walsh_bridge(truth_table(g, 4))

    # XOR
    B_xor_direct = walsh_bridge(truth_table(lambda x: f(x) ^ g(x), 4))
    assert np.allclose(B_xor_direct, bridge_xor(B_f, B_g)), "XOR rule fail"

    # AND
    B_and_direct = walsh_bridge(truth_table(lambda x: f(x) & g(x), 4))
    assert np.allclose(B_and_direct, bridge_and(B_f, B_g)), "AND rule fail"

    # OR
    B_or_direct = walsh_bridge(truth_table(lambda x: f(x) | g(x), 4))
    assert np.allclose(B_or_direct, bridge_or(B_f, B_g)), "OR rule fail"

    print("extended_composition_tests.py self-test: all rules verified.")


if __name__ == "__main__":
    _self_test()
    print()
    main()
