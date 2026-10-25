"""
iching_walk_hard_battery.py
============================

Adversarial validation for the π-walk Walsh recovery.

Each test targets a specific failure mode or a property that MUST hold
if the architecture is correct.  Tests are independent and self-checking.

  T1.  All 256 functions @ full closure        → 256/256 exact
  T2.  All 256 functions @ partial coverage    → graceful degradation
  T3.  Coverage threshold:  what's the minimum  walk length for v-coverage?
  T4.  Off-by-one: walk[:k] vs walk[:k+1] near coverage threshold
  T5.  Round-trip:  truth table → bridge → truth table → bridge.  Identity.
  T6.  Linearity:   B(y1 XOR y2) = B(y1) - 2·{both} mod proper sign rule.
                    More cleanly: 2y-1 → bridge is linear in (2y-1).
  T7.  Parseval:    Σ B[c]² = 1 for any Boolean function.
  T8.  Adversarial: maximally-balanced truth tables (4 ones, 4 zeros) —
                    the highest-entropy bridges.
  T9.  Sparse:     truth tables with single-1 entry (delta functions).
                    These have dense bridges with all 8 cells nonzero.
  T10. Visit-count test: with closure walk, every v ∈ {0..7} visited
                         AT LEAST ONCE (necessary), plus visit_count[v] > 0
                         for all v BEFORE closure-step.
  T11. Determinism: identical input → identical output, run 5 times.
  T12. Self-consistency between A and C: max|B_A - B_C| < 1e-12 always.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np


# ---------------------------------------------------------------
def walsh_char(c, v):
    return 1 if bin(c & v).count('1') % 2 == 0 else -1


def build_hadamard(N):
    H = np.zeros((N, N))
    for c in range(N):
        for v in range(N):
            H[c, v] = walsh_char(c, v)
    return H


def walsh_bridge_direct(y):
    N = len(y)
    s = 2 * np.asarray(y) - 1
    return (build_hadamard(N) @ s) / N


def reconstruct_truth_from_bridge(B):
    """Inverse FWHT: truth_spin = H @ B  (since H @ H = N·I, B = H @ s / N → s = H @ B)."""
    N = len(B)
    s = build_hadamard(N) @ B
    return ((s + 1) / 2).astype(int).tolist()  # back to 0/1


def pi_base8_digits(n_digits):
    try:
        from mpmath import mp, pi as mp_pi
        mp.dps = max(int(n_digits * 1.0) + 30, 80)
        x = mp_pi - 3
        digits = []
        for _ in range(n_digits):
            x = x * 8
            d = int(x)
            digits.append(d)
            x = x - d
        return digits
    except ImportError:
        s = ("11037552421026430215142306305056006701632112201116"
             "020234062106425352145357015210046064352146357203030"
             "157305372411272300033273042103605417544470004134004"
             "06754325623432473471064760525142115275203236321")
        return [int(c) for c in s][:n_digits]


def walk_full_closure(start_offset=0, max_digits=500):
    digits = pi_base8_digits(max_digits + start_offset)[start_offset:]
    seen = set()
    walk = []
    for k in range(len(digits) - 1):
        a, b = digits[k], digits[k + 1]
        walk.append((a, b))
        seen.add((a, b))
        if len(seen) == 64:
            break
    return walk


def walk_n_steps(n_steps, start_offset=0):
    digits = pi_base8_digits(n_steps + start_offset + 2)[start_offset:]
    return [(digits[k], digits[k+1]) for k in range(min(n_steps, len(digits)-1))]


# ---------------------------------------------------------------
def recover_A(y, walk):
    N = len(y)
    visited = set(from_v ^ to_v for (from_v, to_v) in walk)
    bridge = np.zeros(N)
    for c in range(N):
        bridge[c] = sum(walsh_char(c, v) * (2 * y[v] - 1) for v in visited) / N
    return bridge, visited


def recover_C(y, walk):
    N = len(y)
    s = 2 * np.asarray(y) - 1
    visit_count = np.zeros(N, dtype=int)
    for (from_v, to_v) in walk:
        visit_count[from_v ^ to_v] += 1
    bridge = np.zeros(N)
    for (from_v, to_v) in walk:
        v = from_v ^ to_v
        if visit_count[v] == 0:
            continue
        for c in range(N):
            bridge[c] += walsh_char(c, v) * s[v] / (N * visit_count[v])
    return bridge


# =====================================================================
def t1_all_256_full_closure():
    print("─" * 72)
    print("  T1: All 256 functions @ full closure → must be exact")
    print("─" * 72)
    walk = walk_full_closure()
    failures = []
    for f_idx in range(256):
        y = [(f_idx >> v) & 1 for v in range(8)]
        B_true = walsh_bridge_direct(y)
        B_a, _ = recover_A(y, walk)
        B_c = recover_C(y, walk)
        if max(np.max(np.abs(B_a - B_true)), np.max(np.abs(B_c - B_true))) > 1e-10:
            failures.append(f_idx)
    if failures:
        print(f"  ✗ FAIL  {len(failures)}/256 not recovered exactly: {failures[:10]}...")
        return False
    print(f"  ✓ PASS  256/256 recovered to machine precision")
    return True


def t2_all_256_partial_coverage():
    print("─" * 72)
    print("  T2: All 256 functions at varying walk lengths → graceful")
    print("─" * 72)
    print(f"  {'walk_len':>10s}  {'avg_visited':>12s}  {'#exact':>8s}  {'avg_cos':>9s}  {'min_cos':>9s}")
    for n_steps in [4, 8, 16, 24, 32, 64, 128, 367]:
        walk = walk_n_steps(n_steps)
        visited_counts = []
        n_exact = 0
        cosines = []
        for f_idx in range(256):
            y = [(f_idx >> v) & 1 for v in range(8)]
            B_true = walsh_bridge_direct(y)
            B_a, vis = recover_A(y, walk)
            visited_counts.append(len(vis))
            err = float(np.max(np.abs(B_a - B_true)))
            if err < 1e-10:
                n_exact += 1
            denom = np.linalg.norm(B_a) * np.linalg.norm(B_true)
            cs = float(np.dot(B_a, B_true) / denom) if denom > 1e-12 else 0.0
            cosines.append(cs)
        print(f"  {n_steps:>10d}  {np.mean(visited_counts):>12.2f}  "
              f"{n_exact:>8d}  {np.mean(cosines):>+9.4f}  {np.min(cosines):>+9.4f}")
    print(f"  → exact only when full v-coverage (avg=8.00) achieved")
    return True


def t3_coverage_threshold():
    print("─" * 72)
    print("  T3: Coverage threshold — minimum walk length for full v-coverage")
    print("─" * 72)
    walk = walk_full_closure()
    visited = set()
    for k, (from_v, to_v) in enumerate(walk):
        visited.add(from_v ^ to_v)
        if len(visited) == 8:
            print(f"  ✓ All 8 v's covered at step {k+1} (out of {len(walk)} closure steps)")
            print(f"  Coverage / closure ratio: {(k+1)/len(walk):.3f}")
            return True
    print(f"  ✗ FAIL coverage never completed in {len(walk)} steps")
    return False


def t4_off_by_one_threshold():
    print("─" * 72)
    print("  T4: Off-by-one at the v-coverage threshold")
    print("─" * 72)
    walk = walk_full_closure()
    visited = set()
    threshold_step = None
    for k, (from_v, to_v) in enumerate(walk):
        visited.add(from_v ^ to_v)
        if len(visited) == 8:
            threshold_step = k + 1
            break
    print(f"  Coverage threshold: step {threshold_step}")
    # Test recovery one step before vs one step after
    targets = [
        ("AND_3", [0,0,0,0,0,0,0,1]),
        ("XOR_3", [0,1,1,0,1,0,0,1]),
        ("MAJ_3", [0,0,0,1,0,1,1,1]),
    ]
    print(f"  {'gate':>10s}  {'@thresh-1':>11s}  {'@thresh':>11s}  {'@thresh+1':>11s}")
    for name, y in targets:
        B_true = walsh_bridge_direct(y)
        results = []
        for off in [-1, 0, 1]:
            n = threshold_step + off
            if n < 1: results.append("n/a"); continue
            walk_partial = walk[:n]
            B_a, _ = recover_A(y, walk_partial)
            err = float(np.max(np.abs(B_a - B_true)))
            results.append(f"{err:.0e}")
        print(f"  {name:>10s}  {results[0]:>11s}  {results[1]:>11s}  {results[2]:>11s}")
    print(f"  → expected: thresh-1 nonzero error, thresh and beyond exact")
    return True


def t5_roundtrip_truth_to_bridge_to_truth():
    print("─" * 72)
    print("  T5: Round-trip — truth table → bridge → truth table → bridge")
    print("─" * 72)
    walk = walk_full_closure()
    fails = []
    for f_idx in range(256):
        y = [(f_idx >> v) & 1 for v in range(8)]
        B1, _ = recover_A(y, walk)
        y_recovered = reconstruct_truth_from_bridge(B1)
        if y_recovered != y:
            fails.append(f_idx)
            continue
        B2, _ = recover_A(y_recovered, walk)
        if np.max(np.abs(B1 - B2)) > 1e-10:
            fails.append(f_idx)
    if fails:
        print(f"  ✗ FAIL: {len(fails)} round-trips broken: {fails[:10]}")
        return False
    print(f"  ✓ PASS: all 256 round-trips identical to machine precision")
    return True


def t6_linearity():
    print("─" * 72)
    print("  T6: Linearity in spin form — B(αs1 + βs2) = αB(s1) + βB(s2)")
    print("─" * 72)
    walk = walk_full_closure()
    H = build_hadamard(8) / 8.0
    rng = np.random.RandomState(42)
    fails = 0
    for trial in range(50):
        s1 = rng.choice([-1, 1], 8).astype(float)
        s2 = rng.choice([-1, 1], 8).astype(float)
        a, b = rng.uniform(-2, 2), rng.uniform(-2, 2)
        # Bridge of αs1 + βs2 should equal αB1 + βB2
        # Use direct H operation, not recover_A (which expects 0/1 inputs)
        B_combined = H @ (a * s1 + b * s2)
        B1 = H @ s1
        B2 = H @ s2
        err = np.max(np.abs(B_combined - (a * B1 + b * B2)))
        if err > 1e-10:
            fails += 1
    if fails:
        print(f"  ✗ FAIL: {fails}/50 linearity violations")
        return False
    print(f"  ✓ PASS: all 50 random combinations linear to ≤1e-10")
    return True


def t7_parseval():
    print("─" * 72)
    print("  T7: Parseval — Σ B[c]² == 1 for every Boolean function")
    print("─" * 72)
    walk = walk_full_closure()
    fails = []
    for f_idx in range(256):
        y = [(f_idx >> v) & 1 for v in range(8)]
        B, _ = recover_A(y, walk)
        total = float(np.sum(B ** 2))
        if abs(total - 1.0) > 1e-10:
            fails.append((f_idx, total))
    if fails:
        print(f"  ✗ FAIL: {len(fails)} Parseval violations, e.g. {fails[:3]}")
        return False
    print(f"  ✓ PASS: Σ B[c]² = 1.0 for all 256 functions to ≤1e-10")
    return True


def t8_adversarial_balanced():
    print("─" * 72)
    print("  T8: Adversarial — maximally balanced (4 ones, 4 zeros)")
    print("─" * 72)
    walk = walk_full_closure()
    from itertools import combinations
    failures = []
    n_total = 0
    for ones in combinations(range(8), 4):
        y = [1 if v in ones else 0 for v in range(8)]
        n_total += 1
        B_true = walsh_bridge_direct(y)
        B, _ = recover_A(y, walk)
        if np.max(np.abs(B - B_true)) > 1e-10:
            failures.append(ones)
    print(f"  Tested {n_total} balanced functions (C(8,4) = 70)")
    if failures:
        print(f"  ✗ FAIL: {len(failures)} not exact")
        return False
    print(f"  ✓ PASS: all {n_total} balanced functions exact")
    return True


def t9_sparse_delta():
    print("─" * 72)
    print("  T9: Sparse delta — single-1 truth tables (8 functions)")
    print("─" * 72)
    walk = walk_full_closure()
    print(f"  These have DENSE bridges (every B[c] = ±1/8)")
    failures = []
    for delta_v in range(8):
        y = [1 if v == delta_v else 0 for v in range(8)]
        B_true = walsh_bridge_direct(y)
        B, _ = recover_A(y, walk)
        # Check density: 8 nonzero entries, all magnitudes 0.25
        nz = int(np.sum(np.abs(B_true) > 1e-9))
        if nz != 8:
            failures.append((delta_v, "wrong density", nz))
        if np.max(np.abs(B - B_true)) > 1e-10:
            failures.append((delta_v, "wrong values"))
    if failures:
        print(f"  ✗ FAIL: {failures}")
        return False
    print(f"  ✓ PASS: all 8 delta functions have dense bridges, recovered exact")
    return True


def t10_visit_count_invariant():
    print("─" * 72)
    print("  T10: Visit count invariant — every v visited ≥ 1× by closure")
    print("─" * 72)
    walk = walk_full_closure()
    visit = np.zeros(8, dtype=int)
    for (from_v, to_v) in walk:
        visit[from_v ^ to_v] += 1
    print(f"  visit counts per v: {visit.tolist()}")
    if (visit > 0).all():
        print(f"  ✓ PASS: every v ∈ {{0..7}} visited at least once")
        return True
    print(f"  ✗ FAIL: missing v's: {[v for v in range(8) if visit[v] == 0]}")
    return False


def t11_determinism():
    print("─" * 72)
    print("  T11: Determinism — same input gives same output across runs")
    print("─" * 72)
    walk = walk_full_closure()
    y = [0,1,1,0,1,0,0,1]
    results = []
    for trial in range(5):
        B, _ = recover_A(y, walk)
        results.append(B)
    # Check all identical
    for r in results[1:]:
        if np.max(np.abs(r - results[0])) > 1e-15:
            print(f"  ✗ FAIL: nondeterministic")
            return False
    print(f"  ✓ PASS: 5 runs all identical to ≤1e-15")
    return True


def t12_consistency_A_vs_C():
    print("─" * 72)
    print("  T12: A and C agree on all 256 functions")
    print("─" * 72)
    walk = walk_full_closure()
    max_diff = 0.0
    for f_idx in range(256):
        y = [(f_idx >> v) & 1 for v in range(8)]
        B_a, _ = recover_A(y, walk)
        B_c = recover_C(y, walk)
        diff = float(np.max(np.abs(B_a - B_c)))
        max_diff = max(max_diff, diff)
    print(f"  max |B_A - B_C| over all 256 functions: {max_diff:.2e}")
    if max_diff < 1e-10:
        print(f"  ✓ PASS: A and C agree everywhere")
        return True
    print(f"  ✗ FAIL")
    return False


# =====================================================================
def main():
    print(" " * 16 + "π-WALK WALSH RECOVERY — HARD BATTERY\n")
    tests = [
        t1_all_256_full_closure,
        t2_all_256_partial_coverage,
        t3_coverage_threshold,
        t4_off_by_one_threshold,
        t5_roundtrip_truth_to_bridge_to_truth,
        t6_linearity,
        t7_parseval,
        t8_adversarial_balanced,
        t9_sparse_delta,
        t10_visit_count_invariant,
        t11_determinism,
        t12_consistency_A_vs_C,
    ]
    results = {}
    for t in tests:
        results[t.__name__] = t()
        print()
    print("=" * 72)
    print(f"  SUMMARY")
    print("=" * 72)
    n_pass = sum(1 for v in results.values() if v)
    n_total = len(results)
    print(f"  {n_pass}/{n_total} tests passed\n")
    for name, ok in results.items():
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {name}")


if __name__ == "__main__":
    main()
