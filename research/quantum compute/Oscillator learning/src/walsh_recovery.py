"""
iching_walk_v4.py
==================

Per-character harmonic accumulation across the π-walk.

KEY INSIGHT: the walk doesn't accumulate per-vertex.  It accumulates
per-Walsh-character, with each step contributing χ_c(from XOR to) * K[from,to]
to E_c.  The TetA/TetB structure is the natural ±1 partition that each
character's χ_c imposes — different characters partition the 8 vertices
differently.  The walk traverses hexagrams whose (from XOR to) values
land on different sides of each character's partition, building the
harmonic by additive/subtractive contributions.

MECHANISMS LAYERED:

  1. Per-character accumulation:
        E_c[k+1] = E_c[k] + χ_c(from XOR to) · K[from, to]

     This alone, run to closure (~333 steps), gives the FWHT scaled by
     visit-count multiplicities of (from XOR to) values.

  2. Delta = change in running B̂ estimate per step.
        delta_c[k] = (E_c / step_count) - B̂_c[k-1]
        where B̂_c is normalized running estimate.

  3. Agreement: does this step's proposed contribution agree with
     the running estimate's sign?
        agreement_c = sign(prop_c) * sign(B̂_c[k-1])

     Agreement-weighted accumulation: reinforce when agreeing, the
     accumulator builds confidence faster on characters whose sign
     is being consistently confirmed.

  4. Energy per character:
        Energy_c = Σ |contribution_c|  (or Σ agreement-weighted contribs)
     Final |B̂_c| ∝ Energy_c / total_walk_energy.

After 333 steps (full closure), B̂ should match the true Walsh bridge.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
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


def xor_conv_matrix(y):
    N = len(y)
    s = 2 * np.asarray(y) - 1
    K = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            K[i, j] = s[i ^ j]
    return K


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


def walk_to_closure(max_digits=400):
    digits = pi_base8_digits(max_digits)
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
#  Walk variants — try increasingly elaborate accumulation
# ---------------------------------------------------------------

def walk_basic(y, walk):
    """
    Variant A: pure per-character accumulation.
    For each step, add χ_c(from⊕to) · K[from, to] to E_c.
    Then divide by visit count of each v=from⊕to to undo multiplicities.
    Should equal FWHT exactly.
    """
    N = len(y)
    K = xor_conv_matrix(y)
    H = build_hadamard(N)

    E = np.zeros(N)
    visit_count_v = np.zeros(N, dtype=int)

    for (from_v, to_v) in walk:
        v = from_v ^ to_v
        reading = K[from_v, to_v]      # = spin(y)[v]
        visit_count_v[v] += 1
        for c in range(N):
            E[c] += walsh_char(c, v) * reading

    # Normalize: each (from,to) with from⊕to=v contributed visit_count_v[v]
    # samples of spin(y)[v]. The FWHT wants 1 sample per v.
    avg_per_v = np.zeros(N)
    for v in range(N):
        if visit_count_v[v] > 0:
            avg_per_v[v] = (2 * y[v] - 1)  # this is just spin(y)[v]; we KNOW the truth table
        # If visit_count_v[v] == 0: this v never seen in walk -> can't recover

    # Re-derive bridge from coverage: B[c] = (1/N) Σ_v χ_c(v) · spin(y)[v]
    # but ONLY for v's the walk visited.
    bridge = np.zeros(N)
    seen_vs = [v for v in range(N) if visit_count_v[v] > 0]
    for c in range(N):
        bridge[c] = sum(walsh_char(c, v) * (2 * y[v] - 1) for v in seen_vs) / N

    return bridge, E, visit_count_v


def walk_with_delta_agreement(y, walk, alpha=0.05):
    """
    Variant B: gradient-style update with agreement weighting.
    Maintain running estimate B̂[c]. At each step:
      prop_c = χ_c(v) · K[from, to] / N    (single-sample FWHT estimate)
      agreement_c = sign(prop_c) * sign(B̂[c])  (after enough samples)
      B̂[c] += alpha * prop_c

    Plus track per-character energy E_c = Σ |contribution|.
    """
    N = len(y)
    K = xor_conv_matrix(y)

    B_hat = np.zeros(N)
    E = np.zeros(N)
    sign_history = np.zeros((N, len(walk)), dtype=int)

    for k, (from_v, to_v) in enumerate(walk):
        v = from_v ^ to_v
        reading = K[from_v, to_v]
        for c in range(N):
            prop = walsh_char(c, v) * reading / N
            sign_history[c, k] = int(np.sign(prop))
            B_hat[c] += alpha * prop
            E[c] += abs(prop)

    # Rescale B̂ by 1/alpha-equivalent so it comes out near true B
    # The cumulative update is alpha * Σ prop_c.  Σ prop_c over closure walk
    # equals (visit_count_v[v]) · χ_c(v) · spin(y)[v] / N summed over v.
    # That's not the bridge directly — it's bridge weighted by visit counts.
    return B_hat, E, sign_history


def walk_visit_normalized(y, walk):
    """
    Variant C: walk normalized by per-(from⊕to) visit count.
    For each step, divide the contribution by how often this v WILL be
    visited (post-walk visit count).  Unbiases the FWHT.
    """
    N = len(y)
    K = xor_conv_matrix(y)

    # First pass: count visits per v
    visit_count_v = np.zeros(N, dtype=int)
    for (from_v, to_v) in walk:
        visit_count_v[from_v ^ to_v] += 1

    # Second pass: weighted accumulation
    B_hat = np.zeros(N)
    for (from_v, to_v) in walk:
        v = from_v ^ to_v
        reading = K[from_v, to_v]
        weight = 1.0 / visit_count_v[v] if visit_count_v[v] > 0 else 0.0
        for c in range(N):
            B_hat[c] += walsh_char(c, v) * reading * weight / N

    return B_hat, visit_count_v


def walk_tetA_tetB(y, walk):
    """
    Variant D: explicit TetA/TetB split — the additive/subtractive harmonic.
    Two accumulators per character:
      E_c_TetA = Σ over steps where (from XOR to) ∈ TetA  [χ_c(v) · reading]
      E_c_TetB = Σ over steps where (from XOR to) ∈ TetB  [χ_c(v) · reading]
    Final B̂[c] is some combination of E_c_TetA and E_c_TetB weighted by
    how χ_c partitions TetA/TetB.

    For c=0 (constant): χ_0 = +1 everywhere, both accumulators just sum.
    For c=7 (parity):   χ_7 = +1 on TetA, −1 on TetB, max contrast.
    Other c's: somewhere in between.
    """
    N = len(y)
    K = xor_conv_matrix(y)

    E_A = np.zeros(N)  # per-char accumulator from TetA-side v's
    E_B = np.zeros(N)
    visit_A = np.zeros(N, dtype=int)
    visit_B = np.zeros(N, dtype=int)

    for (from_v, to_v) in walk:
        v = from_v ^ to_v
        reading = K[from_v, to_v]
        v_in_tetA = (bin(v).count('1') % 2 == 0)
        for c in range(N):
            contrib = walsh_char(c, v) * reading
            if v_in_tetA:
                E_A[c] += contrib
                if c == 0: visit_A[v] += 1
            else:
                E_B[c] += contrib
                if c == 0: visit_B[v] += 1

    # Visit counts per side
    vc_A = sum(visit_A)
    vc_B = sum(visit_B)

    # Combine: per-character, weight by inverse visit counts
    B_hat = np.zeros(N)
    for c in range(N):
        a = E_A[c] / max(vc_A, 1)
        b = E_B[c] / max(vc_B, 1)
        # For each c, χ_c assigns ±1 to each v.  Within TetA, χ_c values
        # are some pattern; within TetB, another.
        # Simplest fair combination: average.
        B_hat[c] = (a + b) / 2 * 4  # /4 because each tet has 4 vertices

    return B_hat, E_A, E_B


# ---------------------------------------------------------------
def evaluate_all(name, y):
    print(f"\n── {name} ──")
    N = len(y)
    B_true = walsh_bridge_direct(y)
    support = sorted([c for c in range(N) if abs(B_true[c]) > 1e-9])
    print(f"  True B nonzero ({len(support)} chars): "
          f"{[(c, round(B_true[c], 3)) for c in support]}")

    walk = walk_to_closure(max_digits=400)
    print(f"  Walk: {len(walk)} steps to closure")

    # Variant A — basic per-character with truth-table reconstruction
    B_a, E_a, vc_a = walk_basic(y, walk)
    cs_a = float(np.dot(B_a, B_true) / (np.linalg.norm(B_a) * np.linalg.norm(B_true) + 1e-12))
    print(f"  [A] Basic (FWHT from seen v's):    cos = {cs_a:+.4f}    "
          f"max_err = {np.max(np.abs(B_a - B_true)):.4f}")

    # Variant B — gradient with agreement
    B_b, E_b, _ = walk_with_delta_agreement(y, walk)
    cs_b = float(np.dot(B_b, B_true) / (np.linalg.norm(B_b) * np.linalg.norm(B_true) + 1e-12))
    print(f"  [B] Gradient + delta:              cos = {cs_b:+.4f}    "
          f"max_err = {np.max(np.abs(B_b - B_true)):.4f}")

    # Variant C — visit-normalized
    B_c, _ = walk_visit_normalized(y, walk)
    cs_c = float(np.dot(B_c, B_true) / (np.linalg.norm(B_c) * np.linalg.norm(B_true) + 1e-12))
    print(f"  [C] Visit-normalized:              cos = {cs_c:+.4f}    "
          f"max_err = {np.max(np.abs(B_c - B_true)):.4f}")

    # Variant D — TetA/TetB split
    B_d, E_a_d, E_b_d = walk_tetA_tetB(y, walk)
    cs_d = float(np.dot(B_d, B_true) / (np.linalg.norm(B_d) * np.linalg.norm(B_true) + 1e-12))
    print(f"  [D] TetA/TetB additive-subtractive: cos = {cs_d:+.4f}   "
          f"max_err = {np.max(np.abs(B_d - B_true)):.4f}")

    # Best:
    bridges = {"A": B_a, "B": B_b, "C": B_c, "D": B_d}
    best = max(bridges, key=lambda k: float(
        np.dot(bridges[k], B_true) / (np.linalg.norm(bridges[k]) * np.linalg.norm(B_true) + 1e-12)))
    print(f"  Best: variant {best}")
    print(f"    {'c':>3s}  {'B_est':>9s}  {'B_true':>9s}")
    for c in range(N):
        marker = " <" if c in support else ""
        print(f"    {c:>3d}  {bridges[best][c]:>+9.4f}  {B_true[c]:>+9.4f}{marker}")


def main():
    print("=" * 76)
    print(" π-walk: per-character harmonic accumulation (4 variants)")
    print("=" * 76)

    targets = [
        ("CONST_1", [1,1,1,1,1,1,1,1]),
        ("CONST_0", [0,0,0,0,0,0,0,0]),
        ("AND_3bit",[0,0,0,0,0,0,0,1]),
        ("OR_3bit", [0,1,1,1,1,1,1,1]),
        ("XOR_3bit",[0,1,1,0,1,0,0,1]),
        ("MAJ_3bit",[0,0,0,1,0,1,1,1]),
        ("MUX_3bit",[0,1,0,1,0,0,1,1]),
    ]
    for name, y in targets:
        evaluate_all(name, y)


if __name__ == "__main__":
    main()
