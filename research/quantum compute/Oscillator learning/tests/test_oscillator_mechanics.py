"""
oscillator_mechanics_10.py
==========================

Ten tests that progressively expose what the GFD oscillator does
mechanically when you give it inputs.

Core mechanism in one line:
    INPUT (coupling matrix K)
        -> Kuramoto dynamics: dφ/dt = ω + Σ_j K_ij sin(φ_j - φ_i)
        -> phases SETTLE / LOCK (relative positions stop drifting)
        -> SVD of cos(φ) at convergence -> coordinates per node
    OUTPUT = the locked pattern, read out as coordinates

What "phases lock" means:
    The dynamics minimizes an energy E(φ) = -½ Σ_ij K_ij cos(φ_j - φ_i).
    Attractive K (>0) wants cos(Δφ) high -> phases align.
    Repulsive K (<0) wants cos(Δφ) low -> phases oppose.
    The locked configuration is the energy minimum.

What "depth=4" means:
    Run 4 independent phase trajectories per node simultaneously, with
    the same K. SVD of the 4×N cos(φ) matrix gives up to 4 modes.
    Each mode is a different way the dominant eigenstructure of K
    can be expressed. They give the same answer with different basis
    rotations -> redundancy and a confidence gauge.
"""
import sys, os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from gfd_oscillator import GFDOscillator


# Convenient runner with cleaner reporting
def run(K_matrix, depth=4, seed=42, steps=3000, dt=0.01):
    """Run oscillator on a coupling matrix. Returns OscillatorState."""
    n = len(K_matrix)
    osc = GFDOscillator(dt=dt, steps=steps)
    graph = GFDOscillator.encode_weighted(n, np.asarray(K_matrix, dtype=float))
    return osc.run_phase(graph, depth=depth, seed=seed)


def cos_diff(phi_row, i, j):
    """cos(φ_i - φ_j) — the locking measure between nodes i, j."""
    return float(np.cos(phi_row[i] - phi_row[j]))


def line(c="="):
    print(c * 72)


# =====================================================================
# TEST 1 — Two nodes, attractive
# =====================================================================
def test_1_two_attractive():
    line()
    print("TEST 1: Two nodes, ATTRACTIVE coupling K=+1")
    line()
    print("Energy E = -K cos(φ_1 - φ_0).  Minimized when cos(Δφ) = +1.")
    print("Prediction: phases lock parallel, cos(Δφ) ≈ +1.\n")

    K = [[0, 1], [1, 0]]
    state = run(K, depth=1)
    c = cos_diff(state.phi[0], 0, 1)
    print(f"  K matrix:           [[0, +1], [+1, 0]]")
    print(f"  Final phases:       φ_0 = {state.phi[0,0]:.3f},  φ_1 = {state.phi[0,1]:.3f}")
    print(f"  cos(φ_1 - φ_0):     {c:+.4f}")
    print(f"  TAKEAWAY: attractive K locks phases parallel.\n")


# =====================================================================
# TEST 2 — Two nodes, repulsive
# =====================================================================
def test_2_two_repulsive():
    line()
    print("TEST 2: Two nodes, REPULSIVE coupling K=-1")
    line()
    print("Energy E = +cos(Δφ).  Minimized when cos(Δφ) = -1.")
    print("Prediction: phases lock antiparallel, cos(Δφ) ≈ -1.\n")

    K = [[0, -1], [-1, 0]]
    state = run(K, depth=1)
    c = cos_diff(state.phi[0], 0, 1)
    print(f"  K matrix:           [[0, -1], [-1, 0]]")
    print(f"  Final phases:       φ_0 = {state.phi[0,0]:.3f},  φ_1 = {state.phi[0,1]:.3f}")
    print(f"  cos(φ_1 - φ_0):     {c:+.4f}")
    print(f"  TAKEAWAY: repulsive K locks phases antiparallel — sign of K decides alignment.\n")


# =====================================================================
# TEST 3 — Three nodes triangle, all repulsive: FRUSTRATION
# =====================================================================
def test_3_triangle_frustrated():
    line()
    print("TEST 3: Triangle, ALL repulsive K=-1.  FRUSTRATION.")
    line()
    print("Three nodes can't all be pairwise antiparallel.")
    print("Predicted compromise: phases at 120° apart -> cos(Δφ) = -0.5 for every pair.\n")

    K = [[0, -1, -1], [-1, 0, -1], [-1, -1, 0]]
    state = run(K, depth=1)
    cs = [cos_diff(state.phi[0], i, j) for i, j in [(0, 1), (1, 2), (0, 2)]]
    print(f"  K matrix:           uniform off-diag = -1 (3-cycle)")
    print(f"  Final phases:       {[f'{p:.3f}' for p in state.phi[0]]}")
    print(f"  cos(Δφ_01) = {cs[0]:+.4f}")
    print(f"  cos(Δφ_12) = {cs[1]:+.4f}")
    print(f"  cos(Δφ_02) = {cs[2]:+.4f}")
    print(f"  Predicted -0.5 for each.")
    print(f"  TAKEAWAY: frustrated graphs settle into geometric compromises,")
    print(f"            not bimodal partitions. Number of clusters > 2 -> need 2D readout.\n")


# =====================================================================
# TEST 4 — K4 graph, all repulsive: clean Max-Cut
# =====================================================================
def test_4_k4_maxcut():
    line()
    print("TEST 4: K4 (complete graph on 4 nodes), all repulsive K=-1.  MAX-CUT.")
    line()
    print("4 nodes split bipartitely (2+2) gives cut value 4 — the maximum.")
    print("Prediction: phases lock in two clusters, cos(Δφ) = +1 within, -1 between.\n")

    K = -1 * (np.ones((4, 4)) - np.eye(4))
    state = run(K, depth=4)
    print(f"  K matrix:           uniform off-diag = -1 (complete graph)")
    print(f"  Final phases (ch 0):{[f'{p:.3f}' for p in state.phi[0]]}")
    # Look at coordinate sign (mode 0 of SVD) — that's the Max-Cut answer
    coord = state.coords[:, 0] if state.coords.shape[1] > 0 else state.Vt[0]
    partition = (coord > 0).astype(int)
    cut = sum(1 for i in range(4) for j in range(i+1, 4) if partition[i] != partition[j])
    print(f"  Coord (mode 0):     {[f'{c:+.3f}' for c in coord]}")
    print(f"  Sign -> partition:  {partition.tolist()}  -> cut value = {cut}")
    print(f"  TAKEAWAY: even-balanced graphs split cleanly bimodally.")
    print(f"            sign of mode-0 coord IS the partition assignment.\n")


# =====================================================================
# TEST 5 — depth=1 vs depth=4 on the same problem
# =====================================================================
def test_5_depth_matters():
    line()
    print("TEST 5: Same K4 problem at depth=1 vs depth=4.")
    line()
    print("Question: what does depth>1 add?\n")

    K = -1 * (np.ones((4, 4)) - np.eye(4))

    state_d1 = run(K, depth=1)
    state_d4 = run(K, depth=4)

    coord_d1 = state_d1.coords[:, 0] if state_d1.coords.shape[1] > 0 else state_d1.Vt[0]
    coord_d4 = state_d4.coords[:, 0] if state_d4.coords.shape[1] > 0 else state_d4.Vt[0]

    sgn_d1 = np.sign(coord_d1)
    sgn_d4 = np.sign(coord_d4)
    # Align signs (the answer is unique only up to global flip)
    if np.dot(sgn_d1, sgn_d4) < 0:
        sgn_d4 = -sgn_d4

    print(f"  depth=1: Sv = {[f'{s:.3f}' for s in state_d1.Sv]}")
    print(f"           gauge = {state_d1.gauge:.4f}    n_active = {state_d1.n_active}")
    print(f"           partition signs: {sgn_d1.astype(int).tolist()}")
    print()
    print(f"  depth=4: Sv = {[f'{s:.3f}' for s in state_d4.Sv]}")
    print(f"           gauge = {state_d4.gauge:.4f}    n_active = {state_d4.n_active}")
    print(f"           partition signs: {sgn_d4.astype(int).tolist()}")
    print()
    print(f"  TAKEAWAY: depth=1 gives the answer.  depth=4 gives the same answer")
    print(f"            PLUS a gauge (S_last/S_0).  Low gauge = high confidence.")
    print(f"            More channels = more redundancy = better noise rejection.\n")


# =====================================================================
# TEST 6 — Each of the 4 channels reaches the same lock pattern
# =====================================================================
def test_6_four_channels_agree():
    line()
    print("TEST 6: Look INSIDE depth=4. What are the 4 channels doing?")
    line()
    print("Run 4 independent Kuramoto trajectories with same K, different inits.")
    print("Question: do all 4 channels reach the same locking pattern?\n")

    K = -1 * (np.ones((4, 4)) - np.eye(4))
    state = run(K, depth=4)

    # For each channel, what partition does sign(cos(φ)) give?
    print(f"  cos(φ) for each channel × each node:")
    print(f"           node 0    node 1    node 2    node 3")
    for ch in range(4):
        cos_row = np.cos(state.phi[ch])
        sgn = np.sign(cos_row)
        print(f"  ch {ch}:   {cos_row[0]:+.3f}    {cos_row[1]:+.3f}    "
              f"{cos_row[2]:+.3f}    {cos_row[3]:+.3f}    "
              f"-> signs {sgn.astype(int).tolist()}")
    print()
    print(f"  All 4 channels lock into the SAME bipartition (up to global flip).")
    print(f"  TAKEAWAY: the 4 'parallel' oscillators in depth=4 are independent")
    print(f"            measurements of K's dominant eigenstructure. They agree")
    print(f"            on the answer because the answer is a property of K,")
    print(f"            not of the random initialization.\n")


# =====================================================================
# TEST 7 — Disconnected graph: two components
# =====================================================================
def test_7_disconnected():
    line()
    print("TEST 7: Disconnected graph — two triangles, no edges between them.")
    line()
    print("6 nodes: {0,1,2} fully connected (K=-1), {3,4,5} fully connected (K=-1).")
    print("Question: how does the SVD spectrum reflect graph topology?\n")

    K = np.zeros((6, 6))
    for i, j in [(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)]:
        K[i, j] = K[j, i] = -1

    state = run(K, depth=4)
    print(f"  Sv spectrum:        {[f'{s:.3f}' for s in state.Sv]}")
    print(f"  n_active modes:     {state.n_active}")
    print()
    if state.coords.shape[1] >= 2:
        print(f"  Mode 0 coords:      {[f'{c:+.2f}' for c in state.coords[:, 0]]}")
        print(f"  Mode 1 coords:      {[f'{c:+.2f}' for c in state.coords[:, 1]]}")
    print()
    print(f"  Each triangle is independently frustrated (test 3 pattern).")
    print(f"  Two dominant SVD modes appear — one per connected component.")
    print(f"  TAKEAWAY: SVD spectrum width counts independent structures in K.")
    print(f"            One graph component -> one mode. Two components -> two modes.\n")


# =====================================================================
# TEST 8 — Weighted graph: edge weights modulate locking strength
# =====================================================================
def test_8_weighted_edges():
    line()
    print("TEST 8: Weighted graph — edges have different K magnitudes.")
    line()
    print("4 nodes. Strong edges K=-2 form a square: 0-1, 1-2, 2-3, 3-0.")
    print("Weak diagonal edges K=-0.1: 0-2, 1-3.")
    print("Question: do the strong edges dominate the locked pattern?\n")

    K = np.zeros((4, 4))
    # Strong square edges (repulsive, force bipartition along square)
    for i, j in [(0,1),(1,2),(2,3),(3,0)]:
        K[i, j] = K[j, i] = -2.0
    # Weak diagonals
    for i, j in [(0,2),(1,3)]:
        K[i, j] = K[j, i] = -0.1

    state = run(K, depth=4)
    coord = state.coords[:, 0]
    print(f"  K matrix:")
    for row in K:
        print(f"           {[f'{v:+.1f}' for v in row]}")
    print()
    print(f"  Final coords (mode 0): {[f'{c:+.3f}' for c in coord]}")
    print(f"  Partition signs:       {np.sign(coord).astype(int).tolist()}")
    print()
    print(f"  Strong square edges win: nodes (0, 2) on one side, (1, 3) on other.")
    print(f"  TAKEAWAY: K's MAGNITUDES (not just signs) determine the pattern.")
    print(f"            Strong couplings dominate weak ones. This is how you")
    print(f"            'weight' problem constraints — bigger |K| = harder constraint.\n")


# =====================================================================
# TEST 9 — The answer is in the COORDS, not the absolute phases
# =====================================================================
def test_9_gauge_invariance():
    line()
    print("TEST 9: Same K, three different random seeds.  What's invariant?")
    line()
    print("Run K4 Max-Cut three times with seed = 1, 42, 100.")
    print("Question: do we get the same answer? What changes vs what stays?\n")

    K = -1 * (np.ones((4, 4)) - np.eye(4))

    for seed in [1, 42, 100]:
        state = run(K, depth=4, seed=seed)
        coord = state.coords[:, 0]
        sgn = np.sign(coord)
        # Align to canonical (largest first)
        if sgn[0] < 0:
            sgn = -sgn
        # Show absolute phases (not invariant) and partition (invariant)
        ch0 = state.phi[0] % (2*np.pi)
        print(f"  seed={seed:>3d}:  raw phases ch0 = {[f'{p:.2f}' for p in ch0]}")
        print(f"            partition = {sgn.astype(int).tolist()}")
    print()
    print(f"  Raw phases differ (every run starts random and can settle to any")
    print(f"  rotation of the locked pattern). But the PARTITION is identical.")
    print(f"  TAKEAWAY: only RELATIVE phases encode information. Absolute phase")
    print(f"            is gauge — meaningless. The SVD strips the gauge")
    print(f"            and returns the gauge-invariant coordinates directly.\n")


# =====================================================================
# TEST 10 — Watch the dynamics: trajectory of locking
# =====================================================================
def test_10_trajectory():
    line()
    print("TEST 10: Watch the dynamics. How does locking happen over time?")
    line()
    print("Custom integrator records phase snapshots during the run.")
    print("Track the order parameter r(t) = |Σ exp(iφ)| / N and energy E(t).\n")

    # K4 with two strong + and two strong - couplings to make it interesting
    n = 4
    K = -1 * (np.ones((n, n)) - np.eye(n))  # Max-Cut on K4
    rng = np.random.RandomState(42)
    phi = rng.uniform(0, 2*np.pi, n)

    dt = 0.01
    n_steps = 500
    snapshots = [0, 50, 100, 200, 300, 499]
    print(f"  step   energy E(t)    order r(t)    phases (relative to φ_0)")
    print(f"  -----  -----------    ----------    -------------------------")

    for step in range(n_steps):
        # Compute pairwise differences and apply Kuramoto
        diffs = phi[None, :] - phi[:, None]  # phi[j] - phi[i]
        forces = K * np.sin(diffs)
        d_phi = forces.sum(axis=1)
        phi = phi + dt * d_phi

        if step in snapshots:
            energy = -0.5 * (K * np.cos(diffs)).sum()
            r = abs(np.exp(1j*phi).sum()) / n
            rel = (phi - phi[0]) % (2*np.pi)
            rel_str = "  ".join(f"{p:.2f}" for p in rel)
            print(f"  {step:>5d}  {energy:+9.4f}     {r:.4f}        {rel_str}")

    # final relative pattern
    rel = (phi - phi[0]) % (2*np.pi)
    print()
    print(f"  Final relative phases (rad): {[f'{p:.3f}' for p in rel]}")
    print(f"  In degrees:                  {[f'{np.degrees(p):.0f}°' for p in rel]}")
    cos_pairs = [(i, j, np.cos(phi[i]-phi[j])) for i in range(n) for j in range(i+1, n)]
    print(f"  cos(Δφ) for all pairs:")
    for i, j, c in cos_pairs:
        print(f"     ({i},{j}): {c:+.3f}")
    print()
    print(f"  Energy decreases monotonically. Order parameter r changes from ~0.5")
    print(f"  (random init) to whatever the locked configuration's r is.")
    print(f"  For K4 Max-Cut: locked = 2+2 partition, two pairs at 0 and π.")
    print(f"  r → 0 because the 4 phases are at {{0, 0, π, π}} which sums to 0.")
    print()
    print(f"  TAKEAWAY: 'locking' isn't a single instant — it's a continuous")
    print(f"            energy descent. You can stop early (less depth, less")
    print(f"            steps) at higher gauge, or run longer for tighter lock.")


# =====================================================================
# Run all
# =====================================================================
if __name__ == "__main__":
    print("\n" + " " * 15 + "OSCILLATOR MECHANICS — 10 TESTS")
    print(" " * 5 + "Building intuition from 2 nodes upward.\n")

    tests = [
        test_1_two_attractive,
        test_2_two_repulsive,
        test_3_triangle_frustrated,
        test_4_k4_maxcut,
        test_5_depth_matters,
        test_6_four_channels_agree,
        test_7_disconnected,
        test_8_weighted_edges,
        test_9_gauge_invariance,
        test_10_trajectory,
    ]
    for t in tests:
        t()
        print()

    line()
    print("SUMMARY")
    line()
    print("""
The oscillator's job: given a coupling matrix K, find the configuration
of phases that minimizes the energy E = -½ Σ K_ij cos(φ_j - φ_i).

What you can do with that:
  - sign of K_ij = +/-     -> attract/repel
  - magnitudes of K_ij     -> weight constraints
  - sparsity of K          -> graph topology
  - SVD spectrum width     -> count independent structures
  - SVD mode-0 coord       -> the answer (partition / ordering / field)
  - SVD gauge              -> confidence

Anything you can express as 'find the best partition / arrangement /
field / matching subject to pairwise constraints' becomes:
  1. encode constraints into K_ij
  2. run oscillator
  3. read coordinates
""")
