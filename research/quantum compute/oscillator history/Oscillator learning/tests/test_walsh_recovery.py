"""
iching_walk_battery.py
=======================

Exhaustive validation of the π-walk Walsh recovery on N=8.

Tests:
  T1. All 256 3-input Boolean functions (full enumeration).
  T2. Coverage check: which v values does the closure walk visit?
  T3. How does cosine vs walk-length curve look?  (early-stop behavior)
  T4. Exact-equality check: does B_recovered == B_true to machine precision?
  T5. Robustness: does it still work if the walk starts at a different
      digit offset of π?
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np


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


def walk_to_closure(start_offset=0, max_digits=500):
    """Sliding-window walk starting at digit offset; stop when 64 hexagrams seen."""
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


# ---------------------------------------------------------------
#  Variant A — coverage-based FWHT
# ---------------------------------------------------------------
def recover_variant_a(y, walk):
    """Mark which v's the walk visited, then FWHT on those."""
    N = len(y)
    visited = set()
    for (from_v, to_v) in walk:
        visited.add(from_v ^ to_v)
    bridge = np.zeros(N)
    for c in range(N):
        bridge[c] = sum(walsh_char(c, v) * (2 * y[v] - 1)
                        for v in visited) / N
    return bridge, visited


# ---------------------------------------------------------------
#  Variant C — visit-normalized accumulation
# ---------------------------------------------------------------
def recover_variant_c(y, walk):
    """Each step contributes; weight by 1/visit_count[v]."""
    N = len(y)
    K = np.zeros((N, N))
    s = 2 * np.asarray(y) - 1
    for i in range(N):
        for j in range(N):
            K[i, j] = s[i ^ j]

    visit_count = np.zeros(N, dtype=int)
    for (from_v, to_v) in walk:
        visit_count[from_v ^ to_v] += 1

    bridge = np.zeros(N)
    for (from_v, to_v) in walk:
        v = from_v ^ to_v
        if visit_count[v] == 0:
            continue
        reading = K[from_v, to_v]
        weight = 1.0 / visit_count[v]
        for c in range(N):
            bridge[c] += walsh_char(c, v) * reading * weight / N
    return bridge


# ---------------------------------------------------------------
#  T1 — All 256 functions
# ---------------------------------------------------------------
def test_all_256_functions():
    print("=" * 76)
    print("  T1: All 256 three-input Boolean functions")
    print("=" * 76)

    walk = walk_to_closure(start_offset=0)
    print(f"  Walk: {len(walk)} steps to closure")

    perfect_a = 0
    perfect_c = 0
    failures = []

    for f_idx in range(256):
        y = [(f_idx >> v) & 1 for v in range(8)]
        B_true = walsh_bridge_direct(y)
        B_a, visited = recover_variant_a(y, walk)
        B_c = recover_variant_c(y, walk)

        err_a = float(np.max(np.abs(B_a - B_true)))
        err_c = float(np.max(np.abs(B_c - B_true)))

        if err_a < 1e-10:
            perfect_a += 1
        if err_c < 1e-10:
            perfect_c += 1

        if err_a > 1e-6 or err_c > 1e-6:
            failures.append((f_idx, err_a, err_c, len(visited)))

    print(f"  Variant A (coverage FWHT):           {perfect_a}/256 perfect")
    print(f"  Variant C (visit-normalized walk):   {perfect_c}/256 perfect")
    if failures:
        print(f"  Failures (first 10):")
        for (f, ea, ec, nv) in failures[:10]:
            print(f"    f_idx={f:>3d}  err_a={ea:.4f}  err_c={ec:.4f}  visited={nv}/8")
    else:
        print(f"  No failures.  All 256 functions recovered to machine precision.")


# ---------------------------------------------------------------
#  T2 — Coverage check
# ---------------------------------------------------------------
def test_coverage():
    print("\n" + "=" * 76)
    print("  T2: Coverage of v-space by closure walk")
    print("=" * 76)

    for offset in [0, 50, 100, 200]:
        walk = walk_to_closure(start_offset=offset)
        visited = set()
        first_complete = None
        for k, (from_v, to_v) in enumerate(walk):
            v = from_v ^ to_v
            visited.add(v)
            if len(visited) == 8 and first_complete is None:
                first_complete = k + 1
        print(f"  offset={offset:>3d}: walk={len(walk):>3d} steps, "
              f"v-coverage complete at step {first_complete}, "
              f"unique v's = {sorted(visited)}")


# ---------------------------------------------------------------
#  T3 — Cosine vs walk length
# ---------------------------------------------------------------
def test_walk_length_curve():
    print("\n" + "=" * 76)
    print("  T3: Cosine recovery vs walk length (early stopping)")
    print("=" * 76)

    walk = walk_to_closure()

    targets = [
        ("AND_3bit",  [0,0,0,0,0,0,0,1]),
        ("XOR_3bit",  [0,1,1,0,1,0,0,1]),
        ("MAJ_3bit",  [0,0,0,1,0,1,1,1]),
    ]

    print(f"  {'name':>10}   {'@8':>8}  {'@16':>8}  {'@32':>8}  {'@64':>8}  "
          f"{'@128':>8}  {'@full':>8}")
    for name, y in targets:
        B_true = walsh_bridge_direct(y)
        row = []
        for n_steps in [8, 16, 32, 64, 128, len(walk)]:
            partial_walk = walk[:n_steps]
            B_a, vis = recover_variant_a(y, partial_walk)
            cs = (np.dot(B_a, B_true) /
                  (np.linalg.norm(B_a) * np.linalg.norm(B_true) + 1e-12))
            row.append(f"{cs:+.4f}({len(vis)})")
        print(f"  {name:>10}   " + "  ".join(f"{v:>8}" for v in row))

    print(f"  Format: cosine(visited_count)  -- visited=8 means full coverage")


# ---------------------------------------------------------------
#  T4 — Exact equality check on standard gates
# ---------------------------------------------------------------
def test_exact_equality():
    print("\n" + "=" * 76)
    print("  T4: Exact equality vs FWHT (machine precision)")
    print("=" * 76)

    walk = walk_to_closure()

    targets = [
        ("CONST_0", [0,0,0,0,0,0,0,0]),
        ("CONST_1", [1,1,1,1,1,1,1,1]),
        ("AND_3",   [0,0,0,0,0,0,0,1]),
        ("OR_3",    [0,1,1,1,1,1,1,1]),
        ("XOR_3",   [0,1,1,0,1,0,0,1]),
        ("MAJ_3",   [0,0,0,1,0,1,1,1]),
        ("MUX_3",   [0,1,0,1,0,0,1,1]),
        ("NAND_3",  [1,1,1,1,1,1,1,0]),
        ("NOR_3",   [1,0,0,0,0,0,0,0]),
        ("XNOR_3",  [1,0,0,1,0,1,1,0]),
    ]
    print(f"  {'gate':>10}   {'max_err_A':>11}  {'max_err_C':>11}  {'status':>10}")
    for name, y in targets:
        B_true = walsh_bridge_direct(y)
        B_a, _ = recover_variant_a(y, walk)
        B_c = recover_variant_c(y, walk)
        err_a = float(np.max(np.abs(B_a - B_true)))
        err_c = float(np.max(np.abs(B_c - B_true)))
        status = "EXACT" if max(err_a, err_c) < 1e-10 else "DIFFERS"
        print(f"  {name:>10}   {err_a:>11.2e}  {err_c:>11.2e}  {status:>10}")


# ---------------------------------------------------------------
#  T5 — Robustness across π offsets
# ---------------------------------------------------------------
def test_robustness_across_offsets():
    print("\n" + "=" * 76)
    print("  T5: Same gate recovered identically across π offsets")
    print("=" * 76)

    targets = [
        ("XOR_3", [0,1,1,0,1,0,0,1]),
        ("MAJ_3", [0,0,0,1,0,1,1,1]),
    ]
    offsets = [0, 25, 50, 100, 200, 300]

    print(f"  {'gate':>8}  " +
          "  ".join(f"off={o:>3d}" for o in offsets))
    for name, y in targets:
        B_true = walsh_bridge_direct(y)
        row = []
        for offset in offsets:
            walk = walk_to_closure(start_offset=offset)
            B_a, _ = recover_variant_a(y, walk)
            err = float(np.max(np.abs(B_a - B_true)))
            row.append(f"{err:.0e}({len(walk)})")
        print(f"  {name:>8}  " + "  ".join(f"{v:>10}" for v in row))
    print(f"  Format: max_err(walk_steps)")


def main():
    print(" " * 18 + "π-WALK WALSH RECOVERY — TEST BATTERY\n")
    test_all_256_functions()
    test_coverage()
    test_walk_length_curve()
    test_exact_equality()
    test_robustness_across_offsets()

    print("\n" + "=" * 76)
    print("  Summary")
    print("=" * 76)
    print("""
  If all 256 functions recover at machine precision and coverage
  completes well before the closure point, the simple-case story
  is solid.  Then we extend to N=16.
""")


if __name__ == "__main__":
    main()
