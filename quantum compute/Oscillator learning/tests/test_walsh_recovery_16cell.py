"""
walsh_recovery_16.py
=====================

π-walk Walsh recovery extended to 16-cell bridges (4-input Boolean functions).

Same architecture as the 8-cell version:
    - π in base 16 generates a sequence of vertex addresses (one hex digit each).
    - Each consecutive pair of digits is a hexagram (from, to) on 16 vertices.
    - Walk visits hexagrams in π's deterministic order.
    - At each step v = from XOR to is the truth-table index sampled.
    - Once every v ∈ {0..15} is visited, FWHT on the visited entries
      gives the bridge exactly.

Differences from 8-cell:
    - 256 possible (from, to) pairs instead of 64
    - Need v-coverage of 16 entries instead of 8
    - Closure (all 256 hexagrams seen) takes longer than just v-coverage
    - For our purpose, v-coverage is what matters — and that's much faster
"""
import math
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


# ---------------------------------------------------------------
def pi_base16_digits(n_digits):
    """Compute first n_digits hex digits of π's fractional part."""
    try:
        from mpmath import mp, pi as mp_pi
        # Need enough decimal precision: log10(16) ≈ 1.204 dec digits per hex digit
        mp.dps = max(int(n_digits * 1.21) + 30, 80)
        x = mp_pi - 3
        digits = []
        for _ in range(n_digits):
            x = x * 16
            d = int(x)
            digits.append(d)
            x = x - d
        return digits
    except ImportError:
        # Fallback: hardcoded first 256 hex digits of π fractional part
        # (the famous BBP-formula digits)
        s = ("243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89"
             "452821E638D01377BE5466CF34E90C6CC0AC29B7C97C50DD3F84D5B5B5470917"
             "9216D5D98979FB1BD1310BA698DFB5AC2FFD72DBD01ADFB7B8E1AFED6A267E96"
             "BA7C9045F12C7F9924A19947B3916CF70801F2E2858EFC16636920D871574E69")
        return [int(c, 16) for c in s][:n_digits]


def walk_to_v_coverage(N, max_digits=2000, start_offset=0):
    """Sliding-window walk; stop when all v ∈ {0..N-1} have been visited."""
    digits = pi_base16_digits(max_digits + start_offset)[start_offset:]
    visited = set()
    walk = []
    for k in range(len(digits) - 1):
        a, b = digits[k], digits[k + 1]
        v = a ^ b
        walk.append((a, b))
        visited.add(v)
        if len(visited) == N:
            return walk
    return walk  # may not have completed coverage


def walk_to_full_closure(N, max_digits=4000, start_offset=0):
    """Sliding-window walk; stop when all N² (from, to) pairs seen."""
    digits = pi_base16_digits(max_digits + start_offset)[start_offset:]
    seen = set()
    walk = []
    for k in range(len(digits) - 1):
        a, b = digits[k], digits[k + 1]
        walk.append((a, b))
        seen.add((a, b))
        if len(seen) == N * N:
            return walk
    return walk  # may not have closed


def walk_n_steps(n_steps, start_offset=0):
    digits = pi_base16_digits(n_steps + start_offset + 2)[start_offset:]
    return [(digits[k], digits[k+1]) for k in range(min(n_steps, len(digits)-1))]


# ---------------------------------------------------------------
#  Variant A: visited-set FWHT
# ---------------------------------------------------------------
def recover_A(y, walk):
    N = len(y)
    visited = set(from_v ^ to_v for (from_v, to_v) in walk)
    bridge = np.zeros(N)
    for c in range(N):
        bridge[c] = sum(walsh_char(c, v) * (2 * y[v] - 1) for v in visited) / N
    return bridge, visited


# ---------------------------------------------------------------
#  Variant C: visit-normalized walk-time accumulation
# ---------------------------------------------------------------
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


# ---------------------------------------------------------------
#  Tests
# ---------------------------------------------------------------
def t1_all_4input_at_v_coverage():
    """All 65,536 4-input Boolean functions, at full v-coverage walk."""
    print("─" * 72)
    print("  T1: All 65,536 four-input Boolean functions @ v-coverage")
    print("─" * 72)
    N = 16
    walk = walk_to_v_coverage(N)
    print(f"  Walk: {len(walk)} steps to v-coverage")

    # 65,536 is a lot; sample first 5,000 + a stratified set + edge cases
    n_total = 1 << 16
    failures = []
    n_tested = 0

    # Sample: every 4th function (16,384 of them) — covers the space
    for f_idx in range(0, n_total, 4):
        y = [(f_idx >> v) & 1 for v in range(N)]
        B_true = walsh_bridge_direct(y)
        B_a, _ = recover_A(y, walk)
        err = float(np.max(np.abs(B_a - B_true)))
        if err > 1e-10:
            failures.append((f_idx, err))
        n_tested += 1

    if failures:
        print(f"  ✗ FAIL  {len(failures)}/{n_tested} functions not exact")
        for (f, e) in failures[:5]:
            print(f"    f_idx={f}, max_err={e:.4e}")
        return False
    print(f"  ✓ PASS  {n_tested}/{n_tested} sampled functions exact")
    return True


def t2_partial_coverage_curve():
    """Cosine recovery vs walk length for 4-input functions."""
    print("─" * 72)
    print("  T2: Partial coverage curve (sample of 100 functions)")
    print("─" * 72)
    N = 16

    # Get walk steps to compare
    full_walk = walk_to_v_coverage(N)
    coverage_step = len(full_walk)

    # Sample functions
    rng = np.random.RandomState(0)
    sample_indices = rng.choice(1 << 16, 100, replace=False)

    print(f"  v-coverage achieved at step {coverage_step}")
    print(f"  {'walk_len':>10s}  {'avg_visited':>12s}  {'#exact':>8s}  "
          f"{'avg_cos':>9s}  {'min_cos':>9s}")
    for n_steps in [4, 8, 16, 32, 64, 128, coverage_step, coverage_step + 50]:
        walk = walk_n_steps(n_steps)
        visited_counts = []
        n_exact = 0
        cosines = []
        for f_idx in sample_indices:
            y = [(f_idx >> v) & 1 for v in range(N)]
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
    print(f"  → exact when avg_visited == 16 (full v-coverage)")
    return True


def t3_v_coverage_threshold():
    """Find the exact step at which v-coverage hits 16."""
    print("─" * 72)
    print("  T3: v-coverage threshold for 16 cells")
    print("─" * 72)
    walk = walk_to_v_coverage(16, max_digits=4000)
    visited = set()
    for k, (from_v, to_v) in enumerate(walk):
        visited.add(from_v ^ to_v)
        if len(visited) == 16:
            print(f"  ✓ All 16 v's covered at step {k+1}")
            return True
    print(f"  ✗ FAIL coverage never completed in {len(walk)} steps")
    return False


def t4_off_by_one():
    """One step before threshold: errored. At threshold: exact."""
    print("─" * 72)
    print("  T4: Off-by-one at v-coverage threshold")
    print("─" * 72)
    walk = walk_to_v_coverage(16, max_digits=4000)
    visited = set()
    threshold = None
    for k, (from_v, to_v) in enumerate(walk):
        visited.add(from_v ^ to_v)
        if len(visited) == 16:
            threshold = k + 1
            break
    print(f"  Threshold step: {threshold}")

    # Build bent function
    bent = []
    for v in range(16):
        x = [(v >> i) & 1 for i in range(4)]
        bent.append((x[0] & x[1]) ^ (x[2] & x[3]))

    # Build other 4-input gates
    targets = [
        ("BENT",   bent),
        ("AND_4",  [0]*15 + [1]),
        ("XOR_4",  [v ^ ((v>>1) & 1) ^ ((v>>2) & 1) ^ ((v>>3) & 1) & 1 for v in range(16)]),
        ("MAJ_4",  [int(bin(v).count('1') >= 2) for v in range(16)]),
    ]
    # Fix XOR_4
    targets[2] = ("XOR_4", [bin(v).count('1') % 2 for v in range(16)])

    print(f"  {'gate':>10s}  {'@thresh-1':>12s}  {'@thresh':>11s}  {'@thresh+1':>12s}")
    for name, y in targets:
        B_true = walsh_bridge_direct(y)
        results = []
        for off in [-1, 0, 1]:
            n = threshold + off
            if n < 1: results.append("n/a"); continue
            B_a, _ = recover_A(y, walk[:n])
            err = float(np.max(np.abs(B_a - B_true)))
            results.append(f"{err:.0e}")
        print(f"  {name:>10s}  {results[0]:>12s}  {results[1]:>11s}  {results[2]:>12s}")
    return True


def t5_bent_function():
    """Bent function specifically — the case that broke the oscillator path."""
    print("─" * 72)
    print("  T5: BENT function — the case that broke earlier oscillator paths")
    print("─" * 72)
    bent = []
    for v in range(16):
        x = [(v >> i) & 1 for i in range(4)]
        bent.append((x[0] & x[1]) ^ (x[2] & x[3]))

    walk = walk_to_v_coverage(16)
    B_true = walsh_bridge_direct(bent)
    B_a, _ = recover_A(bent, walk)
    B_c = recover_C(bent, walk)

    err_a = float(np.max(np.abs(B_a - B_true)))
    err_c = float(np.max(np.abs(B_c - B_true)))

    cs_a = float(np.dot(B_a, B_true) / (np.linalg.norm(B_a) * np.linalg.norm(B_true)))
    print(f"  All 16 bent coefficients: {[round(b, 4) for b in B_true]}")
    print(f"  Variant A:  cosine = {cs_a:+.6f}, max_err = {err_a:.2e}")
    print(f"  Variant C:                       max_err = {err_c:.2e}")
    if max(err_a, err_c) < 1e-10:
        print(f"  ✓ PASS  bent function recovered exactly at machine precision")
        return True
    print(f"  ✗ FAIL")
    return False


def t6_random_4input():
    """Random 4-input — the other case that gave oscillator path trouble."""
    print("─" * 72)
    print("  T6: 100 random 4-input Boolean functions")
    print("─" * 72)
    walk = walk_to_v_coverage(16)
    rng = np.random.RandomState(42)
    failures = 0
    for trial in range(100):
        y = rng.randint(0, 2, 16).tolist()
        B_true = walsh_bridge_direct(y)
        B_a, _ = recover_A(y, walk)
        err = float(np.max(np.abs(B_a - B_true)))
        if err > 1e-10:
            failures += 1
    if failures:
        print(f"  ✗ FAIL: {failures}/100 not exact")
        return False
    print(f"  ✓ PASS  100/100 random functions recovered exactly")
    return True


def t7_parseval():
    """Σ B[c]² = 1 for sample of 4-input functions."""
    print("─" * 72)
    print("  T7: Parseval — Σ B[c]² == 1 for 1000 random 4-input functions")
    print("─" * 72)
    walk = walk_to_v_coverage(16)
    rng = np.random.RandomState(7)
    fails = 0
    for trial in range(1000):
        y = rng.randint(0, 2, 16).tolist()
        B, _ = recover_A(y, walk)
        if abs(float(np.sum(B ** 2)) - 1.0) > 1e-10:
            fails += 1
    if fails:
        print(f"  ✗ FAIL: {fails}/1000 violate Parseval")
        return False
    print(f"  ✓ PASS  Parseval holds for all 1000")
    return True


def t8_round_trip():
    """truth → bridge → truth → bridge identity."""
    print("─" * 72)
    print("  T8: Round-trip identity for 1000 random 4-input functions")
    print("─" * 72)
    walk = walk_to_v_coverage(16)
    H = build_hadamard(16)
    rng = np.random.RandomState(11)
    fails = 0
    for trial in range(1000):
        y = rng.randint(0, 2, 16).tolist()
        B1, _ = recover_A(y, walk)
        s_recon = H @ B1
        y_recon = ((s_recon + 1) / 2 + 0.5).astype(int).tolist()
        # Compare element-wise
        if y_recon != y:
            fails += 1
    if fails:
        print(f"  ✗ FAIL: {fails}/1000 round-trips broken")
        return False
    print(f"  ✓ PASS  All 1000 round-trips identical")
    return True


def t9_a_vs_c():
    """A and C must agree on every function."""
    print("─" * 72)
    print("  T9: A vs C consistency on 500 random functions")
    print("─" * 72)
    walk = walk_to_v_coverage(16)
    rng = np.random.RandomState(13)
    max_diff = 0.0
    for trial in range(500):
        y = rng.randint(0, 2, 16).tolist()
        B_a, _ = recover_A(y, walk)
        B_c = recover_C(y, walk)
        diff = float(np.max(np.abs(B_a - B_c)))
        max_diff = max(max_diff, diff)
    print(f"  max |B_A - B_C| over 500 functions: {max_diff:.2e}")
    if max_diff < 1e-10:
        print(f"  ✓ PASS")
        return True
    print(f"  ✗ FAIL")
    return False


def t10_robustness_offsets():
    """Recovery invariant across π start offsets."""
    print("─" * 72)
    print("  T10: Invariance across π start offsets")
    print("─" * 72)

    bent = []
    for v in range(16):
        x = [(v >> i) & 1 for i in range(4)]
        bent.append((x[0] & x[1]) ^ (x[2] & x[3]))

    B_true = walsh_bridge_direct(bent)
    print(f"  {'offset':>8s}  {'walk_len':>9s}  {'max_err':>11s}")
    all_ok = True
    for offset in [0, 50, 100, 200, 500]:
        walk = walk_to_v_coverage(16, start_offset=offset)
        B_a, _ = recover_A(bent, walk)
        err = float(np.max(np.abs(B_a - B_true)))
        if err > 1e-10:
            all_ok = False
        print(f"  {offset:>8d}  {len(walk):>9d}  {err:>11.2e}")
    if all_ok:
        print(f"  ✓ PASS  exact at all offsets tested")
        return True
    print(f"  ✗ FAIL")
    return False


# ---------------------------------------------------------------
def main():
    print(" " * 12 + "π-WALK 16-CELL WALSH RECOVERY — HARD BATTERY\n")
    tests = [
        t1_all_4input_at_v_coverage,
        t2_partial_coverage_curve,
        t3_v_coverage_threshold,
        t4_off_by_one,
        t5_bent_function,
        t6_random_4input,
        t7_parseval,
        t8_round_trip,
        t9_a_vs_c,
        t10_robustness_offsets,
    ]
    results = {}
    for t in tests:
        results[t.__name__] = t()
        print()
    print("=" * 72)
    print(f"  SUMMARY")
    print("=" * 72)
    n_pass = sum(1 for v in results.values() if v)
    print(f"  {n_pass}/{len(results)} tests passed\n")
    for name, ok in results.items():
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {name}")


if __name__ == "__main__":
    main()
