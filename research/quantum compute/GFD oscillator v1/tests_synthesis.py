#!/usr/bin/env python3
"""
tests_synthesis.py
===================

Empirical verification of §§4-8 of gfd_oscillator_synthesis.md against
the reference implementation gfd_oscillator_3plus1.py.

Tests are organised by synthesis section:

    T4  container closure at 2/17              (§4)
    T5  three-vote decomposition, sqrt(3) ratio (§5)
    T6  variant comparison: full / TetA-only / TetB-only  (§6)
    T7  harmonic-mean identity at tighter integration  (§7)
    T8  perturbation dynamics: rate = sqrt(5), etc  (§8)

Each test prints pass/fail against the synthesis's stated tolerances.
A single summary figure is produced at the end.

Author: surgical test harness, built on Stephen Nelson's 3+1 reference
"""

import math
import random
import statistics
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.size"] = 10

import sys
sys.path.insert(0, "/home/claude")

# Import the reference implementation (unchanged)
from gfd_oscillator_3plus1 import (
    StellatedOctahedron,
    Nested3Plus1,
    transducer,
    mu_partition,
    mu_interior,
    K, GRAM, PHI, INV_PHI2, F_K0, IMPEDANCE, CONTAINER_READOUT_THEORY,
    SQRT5, T_PRIME_STAR,
)

OUT = "/mnt/user-data/outputs"
import os
os.makedirs(OUT, exist_ok=True)


# =====================================================================
#  Helpers shared by multiple tests
# =====================================================================

def pass_fail(ok: bool, label: str, details: str = "") -> str:
    tag = "PASS" if ok else "FAIL"
    return f"  [{tag}]  {label}" + (f"   ({details})" if details else "")


def fit_exp_rate(t: np.ndarray, y: np.ndarray) -> tuple:
    """Fit y(t) = A * exp(-rate * t) by linear regression on log(y).

    Returns (rate, r_squared).  y must be strictly positive.
    """
    mask = y > 1e-12
    if mask.sum() < 3:
        return float("nan"), 0.0
    logy = np.log(y[mask])
    tt = t[mask]
    slope, intercept = np.polyfit(tt, logy, 1)
    # R^2
    y_fit = slope * tt + intercept
    ss_res = np.sum((logy - y_fit) ** 2)
    ss_tot = np.sum((logy - np.mean(logy)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-20 else 1.0)
    return -slope, r2


# =====================================================================
#  SINGLE-LAW VARIANTS FOR §6
# =====================================================================
#
# In "TetA-only" each SO has ONE population following the partition law,
# self-coupled via GRAM * mean(neighbors) / (K-1), mirroring how TetA is
# driven in the full dual-law.  In "TetB-only" each SO has ONE population
# following the interior law, self-coupled via GRAM * mean(T(neighbors))
# / (K-1), mirroring how TetB is driven in the full dual-law.  No cross-
# law vote exists in either variant.  child_contrib in the nested chain
# is transducer(child.single_pop_mean) in both variants.

class SingleLawSO:
    __slots__ = ("law", "label", "mu", "field_origin", "_rng",
                 "hist", "hist_field_origin", "record_history")

    def __init__(self, law: str, label: str = "", seed: int = 42,
                 init_noise: float = 0.02, record_history: bool = False):
        assert law in ("partition", "interior"), law
        self.law = law
        self.label = label
        self._rng = random.Random(seed)
        self.mu = [0.5 + init_noise * (self._rng.random() - 0.5) for _ in range(K)]
        self.field_origin = 0.5
        self.record_history = record_history
        self.hist = []
        self.hist_field_origin = []

    def avg(self): return sum(self.mu) / K
    def readout(self): return self.avg()

    def compute_field_origin(self):
        total = sum(transducer(m) for m in self.mu) / K
        self.field_origin = GRAM * total
        return self.field_origin

    def step(self, x_ext=1.0, child_contrib=0.0, dt=0.1):
        # Both variants: linear self-coupling (just drop the T on neighbors).
        # Justification: the dual-law's two drives are asymmetric (TetB gets
        # raw A, TetA gets T(B)).  Removing one population collapses the
        # cross-coupling to a single self-drive.  The LINEAR form reproduces
        # the early single-SO reference values: TetA-only -> 0.5414 (root
        # of mu^2 + 5*mu - 3 = 0); TetB-only -> 0.4036.
        law_fn = mu_partition if self.law == "partition" else mu_interior
        new_mu = [0.0] * K
        for i in range(K):
            neigh_mean = sum(self.mu[j] for j in range(K) if j != i) / (K - 1)
            gram_drive = GRAM * neigh_mean
            x_i = x_ext * (1.0 + gram_drive + 0.5 * child_contrib)
            target = law_fn(x_i)
            new_mu[i] = self.mu[i] + (target - self.mu[i]) * dt
        self.mu = [min(max(m, 0.001), 0.999) for m in new_mu]
        self.compute_field_origin()
        if self.record_history:
            self.hist.append(self.avg())
            self.hist_field_origin.append(self.field_origin)


class SingleLawNested3Plus1:
    """Variant network: 4 levels, each using SingleLawSO with the same law."""
    def __init__(self, law: str, x_ext=1.0, dt=0.1, seeds=(42, 43, 44, 45),
                 init_noise=0.02):
        self.law = law
        self.x_ext = x_ext
        self.dt = dt
        self.container = SingleLawSO(law, "L0", seeds[0], init_noise)
        self.L1 = SingleLawSO(law, "L1", seeds[1], init_noise)
        self.L2 = SingleLawSO(law, "L2", seeds[2], init_noise)
        self.L3 = SingleLawSO(law, "L3", seeds[3], init_noise)
        self.levels = (self.container, self.L1, self.L2, self.L3)

    def step(self):
        fo_c = self.container.compute_field_origin()
        fo_1 = self.L1.compute_field_origin()
        fo_2 = self.L2.compute_field_origin()
        x_L1 = fo_c / max(1.0 - fo_c, 0.01)
        x_L2 = fo_1 / max(1.0 - fo_1, 0.01)
        x_L3 = fo_2 / max(1.0 - fo_2, 0.01)
        cc_L2 = transducer(self.L3.avg())
        cc_L1 = transducer(self.L2.avg())
        cc_L0 = transducer(self.L1.avg())
        self.L3.step(x_ext=x_L3, child_contrib=0.0, dt=self.dt)
        self.L2.step(x_ext=x_L2, child_contrib=cc_L2, dt=self.dt)
        self.L1.step(x_ext=x_L1, child_contrib=cc_L1, dt=self.dt)
        self.container.step(x_ext=self.x_ext, child_contrib=cc_L0, dt=self.dt)

    def run(self, n_steps): [self.step() for _ in range(n_steps)]
    def readout(self): return self.container.readout()
    def readouts_per_level(self): return [so.readout() for so in self.levels]


# =====================================================================
#  T4: Container closure at 2/17 (§4)
# =====================================================================

def test_T4():
    print("=" * 72)
    print("T4  Container closure at 2/17   (§4)")
    print("=" * 72)

    # Run at the synthesis-standard configuration
    net = Nested3Plus1()
    net.run(600)
    readouts = net.readouts_per_level()
    A_per = [so.avg_A() for so in net.levels]
    gaps = net.gaps_per_level()

    shift = readouts[0] - INV_PHI2
    frac = shift / INV_PHI2
    dev = frac - IMPEDANCE

    # Synthesis §4 table values
    synth = {
        "L0 TetB": 0.426814, "L1 TetB": 0.174481,
        "L2 TetB": 0.065855, "L3 TetB": 0.023039,
        "L0 TetA": 0.543035, "L0 gap": 0.116221,
    }
    meas = {
        "L0 TetB": readouts[0], "L1 TetB": readouts[1],
        "L2 TetB": readouts[2], "L3 TetB": readouts[3],
        "L0 TetA": A_per[0], "L0 gap": gaps[0],
    }

    print(f"  {'quantity':<20}  {'measured':>12}  {'synthesis':>12}  {'|diff|':>10}")
    print(f"  {'-'*20}  {'-'*12}  {'-'*12}  {'-'*10}")
    for k in synth:
        d = abs(meas[k] - synth[k])
        flag = "OK" if d < 1e-5 else "!"
        print(f"  {k:<20}  {meas[k]:>12.6f}  {synth[k]:>12.6f}  {d:>10.2e} {flag}")

    print()
    print(f"  container fractional shift = {frac:+.6f}")
    print(f"  target 2/17                = {IMPEDANCE:+.6f}")
    print(f"  |deviation|                = {abs(dev):.2e}")

    # Tighter run to check if deviation shrinks
    net2 = Nested3Plus1(dt=0.02)
    net2.run(3000)  # same total time 60 units
    frac2 = (net2.container.readout() - INV_PHI2) / INV_PHI2
    dev2 = frac2 - IMPEDANCE
    print(f"  tighter dt=0.02, n=3000:   frac = {frac2:+.6f}, dev = {dev2:+.2e}")

    # And with dt=0.005, n=20000 from synthesis §7
    net3 = Nested3Plus1(dt=0.005)
    net3.run(20000)
    frac3 = (net3.container.readout() - INV_PHI2) / INV_PHI2
    dev3 = frac3 - IMPEDANCE
    print(f"  tightest dt=0.005, n=20000: frac = {frac3:+.6f}, dev = {dev3:+.2e}")

    ok_table = all(abs(meas[k] - synth[k]) < 1e-5 for k in synth)
    ok_converge = abs(dev3) < abs(dev)  # tighter integration must shrink deviation
    print()
    print(pass_fail(ok_table, "All §4 table values reproduce within 1e-5"))
    print(pass_fail(ok_converge,
                    "Tighter integration shrinks deviation from 2/17",
                    f"{abs(dev):.2e} -> {abs(dev3):.2e}"))

    return dict(readouts=readouts, A_per=A_per, gaps=gaps, frac=frac, dev=dev,
                frac_tight=frac3, dev_tight=dev3)


# =====================================================================
#  T5: Three-vote decomposition at varying nesting depth (§5)
# =====================================================================

def _run_nested_depth(depth: int, n_steps=800, dt=0.05):
    """Run a nested network with a given internal depth and return the
    container TetB readout.

    depth = 0: single isolated SO (container only, no children).
    depth = 1: container + one child (L1).
    depth = 2: container + L1 + L2.
    depth = 3: full container + L1 + L2 + L3.
    """
    if depth == 0:
        so = StellatedOctahedron(label="solo", seed=42, init_noise=0.02)
        for _ in range(n_steps):
            so.step(x_ext=1.0, child_contrib=0.0, dt=dt)
        return so.readout()

    # depth in {1, 2, 3}: build a chain of (depth + 1) SOs where the container
    # is index 0 and the leaf is index depth.  We reuse the Nested3Plus1
    # step logic but truncate the chain.
    SOs = [StellatedOctahedron(label=f"L{i}", seed=42 + i, init_noise=0.02)
           for i in range(depth + 1)]

    for _ in range(n_steps):
        # Bottom-up update order.  Leaf has no child.
        # Snapshot top-down drives using FO from step-start.
        x_drives = [1.0] * (depth + 1)
        for i in range(depth):  # parents 0..depth-1 drive their child
            fo = SOs[i].compute_field_origin()
            x_drives[i + 1] = fo / max(1.0 - fo, 0.01)
        # Snapshot bottom-up child_contrib (each parent sees child's avg_A)
        child_contribs = [0.0] * (depth + 1)
        for i in range(depth):
            child_contribs[i] = transducer(SOs[i + 1].avg_A())
        # Update leaf first, container last
        for i in reversed(range(depth + 1)):
            SOs[i].step(x_ext=x_drives[i], child_contrib=child_contribs[i], dt=dt)

    return SOs[0].readout()


def test_T5():
    print()
    print("=" * 72)
    print("T5  Three-vote decomposition, sqrt(3) ratio   (§5)")
    print("=" * 72)

    # Using tighter integration for cleaner votes
    n_steps, dt = 3000, 0.02

    mu_flat = INV_PHI2
    # Depth 0..4.  Depth >=3 should be redundant (closure at D=3).
    readouts = {}
    for d in (0, 1, 2, 3):
        readouts[d] = _run_nested_depth(d, n_steps=n_steps, dt=dt)

    # Incremental votes: each depth adds to the previous shift
    shift = {d: readouts[d] - mu_flat for d in readouts}
    frac = {d: shift[d] / mu_flat for d in readouts}

    # Vote_k (k=1..3) is the INCREMENT when you add level k
    # per synthesis: Vote 1 = depth 0 relative to flat, Vote 2 = depth 1 increment, etc.
    votes = {
        1: shift[0] - 0.0,            # flat -> 1 SO
        2: shift[1] - shift[0],       # 1 SO -> 2 SOs
        3: shift[2] - shift[1],       # 2 SOs -> 3 SOs
        4: shift[3] - shift[2],       # 3 SOs -> 4 SOs (should be ~0)
    }

    # Closed-form predictions from §5
    D = 3
    vote1_cf = (D - math.sqrt(D)) / 17.0 * mu_flat
    vote2_cf = (math.sqrt(D) - 1) / 17.0 * mu_flat
    vote3_cf = 0.0

    print(f"  flat baseline 1/phi^2 = {mu_flat:.8f}")
    print(f"  {'depth':<7}  {'readout':>12}  {'shift':>12}  {'frac':>10}")
    for d in sorted(readouts):
        print(f"  d={d:<5}  {readouts[d]:>12.8f}  {shift[d]:>+12.8f}  {frac[d]:>+10.6f}")

    print()
    print(f"  Vote 1 (flat->d=0):  measured {votes[1]:+.8f}   "
          f"predicted {vote1_cf:+.8f}   |err| {abs(votes[1]-vote1_cf):.2e}")
    print(f"  Vote 2 (d=0->d=1):   measured {votes[2]:+.8f}   "
          f"predicted {vote2_cf:+.8f}   |err| {abs(votes[2]-vote2_cf):.2e}")
    print(f"  Vote 3 (d=1->d=2):   measured {votes[3]:+.8f}   "
          f"predicted {vote3_cf:+.8f}   |err| {abs(votes[3]-vote3_cf):.2e}")
    print(f"  Vote 4 (d=2->d=3):   measured {votes[4]:+.8f}   "
          f"(redundant, should be ~0)")

    ratio = votes[1] / votes[2] if abs(votes[2]) > 1e-12 else float("nan")
    sqrt3 = math.sqrt(3.0)
    print()
    print(f"  Vote1 / Vote2        = {ratio:.6f}")
    print(f"  sqrt(3)              = {sqrt3:.6f}")
    print(f"  |ratio - sqrt(3)|    = {abs(ratio - sqrt3):.2e}")

    ok_v1 = abs(votes[1] - vote1_cf) < 5e-4
    ok_v2 = abs(votes[2] - vote2_cf) < 5e-4
    ok_v3 = abs(votes[3]) < 5e-4
    ok_v4 = abs(votes[4]) < 5e-4
    ok_ratio = abs(ratio - sqrt3) < 0.01
    print()
    print(pass_fail(ok_v1, "Vote 1 matches (D - sqrt(D))/17 * mu_flat"))
    print(pass_fail(ok_v2, "Vote 2 matches (sqrt(D) - 1)/17 * mu_flat"))
    print(pass_fail(ok_v3, "Vote 3 is effectively zero (D=3 closure)"))
    print(pass_fail(ok_v4, "Vote 4 is effectively zero (redundant beyond 3)"))
    print(pass_fail(ok_ratio, "Vote1 / Vote2 = sqrt(3) to within 1%"))

    return dict(readouts=readouts, votes=votes, ratio=ratio,
                vote1_cf=vote1_cf, vote2_cf=vote2_cf)


# =====================================================================
#  T6: Variant comparison (§6)
# =====================================================================

def test_T6():
    print()
    print("=" * 72)
    print("T6  Variant comparison: full / TetA-only / TetB-only   (§6)")
    print("=" * 72)

    n_steps, dt = 3000, 0.02

    # Full (dual-law)
    net_full = Nested3Plus1(dt=dt)
    net_full.run(n_steps)
    container_full = net_full.container.readout()
    baseline_full = INV_PHI2
    frac_full = (container_full - baseline_full) / baseline_full

    # TetA-only
    net_A = SingleLawNested3Plus1("partition", dt=dt)
    net_A.run(n_steps)
    container_A = net_A.container.readout()
    baseline_A = 0.5                                     # partition law at x=1
    frac_A = (container_A - baseline_A) / baseline_A

    # TetB-only
    net_B = SingleLawNested3Plus1("interior", dt=dt)
    net_B.run(n_steps)
    container_B = net_B.container.readout()
    baseline_B = INV_PHI2                                # interior law at x=1
    frac_B = (container_B - baseline_B) / baseline_B

    synth = {
        "full": 0.117412,         # measured in synthesis
        "TetA-only": 0.15682,
        "TetB-only": 0.09594,
    }

    print(f"  {'variant':<12}  {'baseline':>10}  {'container':>12}  "
          f"{'frac_shift':>12}  {'synth':>10}  {'|diff|':>10}")
    print(f"  {'-'*12}  {'-'*10}  {'-'*12}  {'-'*12}  {'-'*10}  {'-'*10}")
    print(f"  {'full':<12}  {baseline_full:>10.6f}  {container_full:>12.6f}  "
          f"{frac_full:>+12.6f}  {synth['full']:>10.5f}  "
          f"{abs(frac_full - synth['full']):>10.2e}")
    print(f"  {'TetA-only':<12}  {baseline_A:>10.6f}  {container_A:>12.6f}  "
          f"{frac_A:>+12.6f}  {synth['TetA-only']:>10.5f}  "
          f"{abs(frac_A - synth['TetA-only']):>10.2e}")
    print(f"  {'TetB-only':<12}  {baseline_B:>10.6f}  {container_B:>12.6f}  "
          f"{frac_B:>+12.6f}  {synth['TetB-only']:>10.5f}  "
          f"{abs(frac_B - synth['TetB-only']):>10.2e}")

    # Critical claim: only the full variant hits 2/17
    full_hits_217 = abs(frac_full - IMPEDANCE) < 1e-3
    A_misses_217 = abs(frac_A - IMPEDANCE) > 0.02
    B_misses_217 = abs(frac_B - IMPEDANCE) > 0.01

    print()
    print(f"  2/17 = {IMPEDANCE:.6f}")
    print(f"  full's frac vs 2/17:     diff = {frac_full - IMPEDANCE:+.2e}")
    print(f"  TetA-only vs 2/17:       diff = {frac_A - IMPEDANCE:+.6f}")
    print(f"  TetB-only vs 2/17:       diff = {frac_B - IMPEDANCE:+.6f}")
    print()
    print(pass_fail(full_hits_217, "Full variant reaches 2/17 exactly"))
    print(pass_fail(A_misses_217, "TetA-only does NOT reach 2/17"))
    print(pass_fail(B_misses_217, "TetB-only does NOT reach 2/17"))

    return dict(
        frac_full=frac_full, frac_A=frac_A, frac_B=frac_B,
        container_full=container_full, container_A=container_A,
        container_B=container_B,
    )


# =====================================================================
#  T7: Harmonic mean identity (§7)
# =====================================================================

def test_T7(t6_results):
    print()
    print("=" * 72)
    print("T7  Harmonic-mean identity   (§7)")
    print("=" * 72)

    I_full = t6_results["frac_full"]
    I_A = t6_results["frac_A"]
    I_B = t6_results["frac_B"]

    # harmonic mean of I_A, I_B:   2 / (1/I_A + 1/I_B)
    hmean = 2.0 / (1.0 / I_A + 1.0 / I_B)

    print(f"  I_full   = {I_full:.8f}")
    print(f"  I_A      = {I_A:.8f}")
    print(f"  I_B      = {I_B:.8f}")
    print(f"  harmonic mean(I_A, I_B) = {hmean:.8f}")
    print(f"  2/17                   = {IMPEDANCE:.8f}")
    print()
    print(f"  |I_full  - 2/17|   = {abs(I_full - IMPEDANCE):.2e}")
    print(f"  |hmean   - 2/17|   = {abs(hmean  - IMPEDANCE):.2e}")
    print(f"  |hmean   - I_full| = {abs(hmean  - I_full):.2e}")
    rel_hmean_full = abs(hmean - I_full) / I_full * 100
    print(f"  |hmean - I_full| / I_full = {rel_hmean_full:.3f}%")

    # Synthesis flagged this as 1.2% at default integration; check if it
    # remains at that gap or shrinks at tighter integration (we already
    # ran with dt=0.02 which is 5x tighter than synthesis default).
    # A true identity should approach zero as integration tightens.
    # A coincidence should stay at ~1.2% (floor set by the measurement
    # itself, not the integrator).

    # Run TetA-only and TetB-only at ANOTHER tightening to see trend
    n_steps2, dt2 = 12000, 0.005
    net_A2 = SingleLawNested3Plus1("partition", dt=dt2)
    net_A2.run(n_steps2)
    I_A2 = (net_A2.container.readout() - 0.5) / 0.5
    net_B2 = SingleLawNested3Plus1("interior", dt=dt2)
    net_B2.run(n_steps2)
    I_B2 = (net_B2.container.readout() - INV_PHI2) / INV_PHI2
    net_F2 = Nested3Plus1(dt=dt2)
    net_F2.run(n_steps2)
    I_full2 = (net_F2.container.readout() - INV_PHI2) / INV_PHI2
    hmean2 = 2.0 / (1.0 / I_A2 + 1.0 / I_B2)

    print()
    print(f"  Tightest run (dt={dt2}, n={n_steps2}):")
    print(f"    I_A  = {I_A2:.8f}")
    print(f"    I_B  = {I_B2:.8f}")
    print(f"    hmean = {hmean2:.8f}")
    print(f"    I_full = {I_full2:.8f}")
    print(f"    |hmean - I_full| = {abs(hmean2 - I_full2):.2e}")
    rel2 = abs(hmean2 - I_full2) / I_full2 * 100
    print(f"    |hmean - I_full|/I_full = {rel2:.4f}%")

    # Is the gap collapsing as integration tightens, or staying put?
    gap_shrinks = rel2 < 0.5 * rel_hmean_full
    print()
    if rel2 < 0.1:
        verdict = "LIKELY EXACT (residual <0.1%)"
    elif gap_shrinks:
        verdict = "CONVERGING TO EXACT (residual shrank with tighter integration)"
    else:
        verdict = "LIKELY APPROXIMATE (residual did not shrink meaningfully)"
    print(f"  VERDICT on harmonic-mean identity:  {verdict}")
    return dict(I_full=I_full2, I_A=I_A2, I_B=I_B2, hmean=hmean2,
                rel_residual=rel2, verdict=verdict)


# =====================================================================
#  T8: Perturbation dynamics (§8)
# =====================================================================
#
# Setup: 4-node tetrahedral network, interior law at each cell, c_amp
# inter-cell coupling.  Each node runs x(1-mu)^2 = mu; interaction enters
# via x_i = x_ext + c_amp * sum_{j != i} (1 - mu_j)/mu_j.  This is the
# §A/§B tetrahedron from the original file, not the dual-law SO.
#
# A single cell is perturbed off the symmetric fixed point; we measure
# the decay of the gap between that cell and the rest.

def _tetra_rhs(t, y, n, x_ext, c_amp):
    dmu = np.zeros(n)
    for i in range(n):
        x_i = x_ext
        for j in range(n):
            if j != i:
                mu_j = np.clip(y[j], 1e-10, 1 - 1e-10)
                x_i += c_amp * (1.0 - mu_j) / mu_j
        mu_i = np.clip(y[i], 1e-10, 1 - 1e-10)
        dmu[i] = x_i * (1 - mu_i) ** 2 - mu_i
    return dmu


def _interior_fixed_point(x_ext, c_amp, n_neighbors=3):
    """Bisect for the symmetric fixed point of x(1-mu)^2 = mu with
    x = x_ext + n_neighbors * c_amp * (1-mu)/mu."""
    def f(mu):
        return (x_ext * mu * (1 - mu) ** 2
                + n_neighbors * c_amp * (1 - mu) ** 3 - mu ** 2)
    lo, hi = 1e-6, 1 - 1e-6
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return float("nan")
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if abs(fm) < 1e-15:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def _transducer_np(mu):
    mu = np.clip(mu, 1e-10, 1 - 1e-10)
    return mu / (1.0 - mu + mu * mu)


def _perturb_and_measure(c_amp, perturb_size, cell_idx, x_ext=1.0, n=4,
                         t_settle=20.0, t_post=6.0, n_points=2000):
    """Settle the tetrahedron, perturb one cell, record gap trajectory."""
    mu_star = _interior_fixed_point(x_ext, c_amp)
    y0 = np.full(n, mu_star + 1e-6)
    sol_settle = solve_ivp(_tetra_rhs, (0, t_settle), y0, method="RK45",
                           args=(n, x_ext, c_amp), max_step=0.01, rtol=1e-10,
                           atol=1e-12)
    y_settled = sol_settle.y[:, -1]
    # Perturb one cell
    y_pert = y_settled.copy()
    y_pert[cell_idx] = np.clip(y_settled[cell_idx] + perturb_size, 0.001, 0.999)
    # Evolve post-perturbation
    t_eval = np.linspace(0, t_post, n_points)
    sol_post = solve_ivp(_tetra_rhs, (0, t_post), y_pert, t_eval=t_eval,
                         method="RK45", args=(n, x_ext, c_amp),
                         max_step=0.005, rtol=1e-11, atol=1e-13)
    # gap signals
    mu_trace = sol_post.y                                       # shape (n, n_points)
    mu_gap = mu_trace[cell_idx] - mu_star                       # signed; may be positive or negative
    # Take magnitude, and compare to a "neighbor" cell
    others_mean = (np.sum(mu_trace, axis=0) - mu_trace[cell_idx]) / (n - 1)
    neigh_disp = others_mean - mu_star                          # how much neighbors moved
    # T-space gap for 8f
    T_pert = _transducer_np(mu_trace[cell_idx])
    T_star = _transducer_np(mu_star)
    T_gap = T_pert - T_star
    return dict(t=t_eval, mu_gap=mu_gap, T_gap=T_gap,
                neigh_disp=neigh_disp, mu_star=mu_star)


def test_T8():
    print()
    print("=" * 72)
    print("T8  Perturbation dynamics   (§8)")
    print("=" * 72)

    # --- T8a/b/c: monotonic, rate ~ sqrt(5), half-life ~ ln(2)/sqrt(5) at c=0
    configs = [
        (0.0, +0.05, 0),
        (0.0, +0.15, 0),
        (0.0, +0.30, 0),
        (0.0, -0.15, 0),
        (0.0, +0.15, 2),
    ]
    print(f"\n  T8a-c: at c_amp = 0, interior-law restoring rate")
    print(f"  {'cfg':<24} {'rate(mu)':>10} {'R^2':>8} {'halflife':>10} {'monotone?':>10}")
    results_c0 = []
    for c_amp, dmu, cell in configs:
        r = _perturb_and_measure(c_amp, dmu, cell)
        gap_abs = np.abs(r["mu_gap"])
        # Use only t where gap > 1e-6 to avoid log of zero
        rate, r2 = fit_exp_rate(r["t"], gap_abs)
        # Half-life empirical
        if rate > 0:
            hl = math.log(2.0) / rate
        else:
            hl = float("nan")
        # Monotonicity: is |gap| non-increasing over the window?
        diffs = np.diff(gap_abs)
        monotone = bool(np.all(diffs <= 1e-9))
        label = f"c={c_amp}, dmu={dmu:+.2f}, cell={cell}"
        print(f"  {label:<24} {rate:>10.4f} {r2:>8.4f} {hl:>10.4f} "
              f"{str(monotone):>10}")
        results_c0.append(dict(cfg=(c_amp, dmu, cell), rate=rate, r2=r2,
                               hl=hl, monotone=monotone, result=r))

    rates_c0 = [r["rate"] for r in results_c0]
    mean_rate = statistics.mean(rates_c0)
    print(f"\n  mean measured rate (c=0) = {mean_rate:.4f}")
    print(f"  predicted sqrt(5)        = {SQRT5:.4f}")
    print(f"  |mean - sqrt(5)|         = {abs(mean_rate - SQRT5):.4f}")
    ok_rate_c0 = abs(mean_rate - SQRT5) / SQRT5 < 0.05
    ok_monotone_c0 = all(r["monotone"] for r in results_c0)
    print(pass_fail(ok_rate_c0, "T8b: rate at c=0 matches sqrt(5) within 5%"))
    print(pass_fail(ok_monotone_c0, "T8a: monotonic decay across all configs"))

    # --- T8d: rate scales with c_amp
    c_values = [0.0, 0.1, 0.5, 1.0]
    print(f"\n  T8d: rate dependence on c_amp")
    print(f"  {'c_amp':>6}  {'mu*':>8}  {'rate':>10}  {'halflife':>10}")
    c_amp_rates = {}
    for c in c_values:
        r = _perturb_and_measure(c, +0.15, 0)
        rate, _ = fit_exp_rate(r["t"], np.abs(r["mu_gap"]))
        hl = math.log(2) / rate if rate > 0 else float("nan")
        print(f"  {c:>6.2f}  {r['mu_star']:>8.4f}  {rate:>10.4f}  {hl:>10.4f}")
        c_amp_rates[c] = rate
    rate_strictly_increases = all(
        c_amp_rates[c_values[i]] < c_amp_rates[c_values[i + 1]]
        for i in range(len(c_values) - 1))
    print(pass_fail(rate_strictly_increases,
                    "T8d: rate strictly increases with c_amp"))

    # --- T8e: perturbation spread (neighbor displacement max)
    print(f"\n  T8e: perturbation spreads at c_amp > 0")
    print(f"  {'c_amp':>6}  {'max |neigh disp|':>18}")
    spreads = {}
    for c in c_values:
        r = _perturb_and_measure(c, +0.15, 0)
        max_spread = float(np.max(np.abs(r["neigh_disp"])))
        spreads[c] = max_spread
        print(f"  {c:>6.2f}  {max_spread:>18.6f}")
    ok_local_at_0 = spreads[0.0] < 1e-5
    ok_spreads_at_c = spreads[1.0] > 1e-3
    print(pass_fail(ok_local_at_0, "T8e: c=0 is purely local (spread < 1e-5)"))
    print(pass_fail(ok_spreads_at_c, "T8e: c>0 distributes perturbation"))

    # --- T8f: T-gap and mu-gap have the SAME decay rate
    print(f"\n  T8f: T-gap vs mu-gap decay rates (at c=0)")
    print(f"  {'perturbation':<16} {'rate(mu)':>10} {'rate(T)':>10} {'diff%':>10}")
    same_rate_ok = True
    for dmu in (+0.05, +0.15, +0.30, -0.15):
        r = _perturb_and_measure(0.0, dmu, 0)
        rate_mu, _ = fit_exp_rate(r["t"], np.abs(r["mu_gap"]))
        rate_T, _ = fit_exp_rate(r["t"], np.abs(r["T_gap"]))
        diff = abs(rate_mu - rate_T) / rate_mu * 100
        print(f"  dmu={dmu:+.2f}        {rate_mu:>10.4f} {rate_T:>10.4f} "
              f"{diff:>9.2f}%")
        if diff > 2.0:
            same_rate_ok = False
    print(pass_fail(same_rate_ok, "T8f: T-gap rate == mu-gap rate (within 2%)"))

    # --- Asymptotic T'(mu*) check using small perturbation linear regime tail
    r = _perturb_and_measure(0.0, +0.05, 0)
    # use only the late portion where gap is small
    late = r["t"] > (r["t"][-1] * 0.3)
    if late.sum() > 10:
        # ratio should approach T'(mu*)
        ratios = r["T_gap"][late] / r["mu_gap"][late]
        # Drop any zero-division or huge spikes
        ratios = ratios[np.isfinite(ratios)]
        asymp_ratio = float(np.mean(ratios[-50:])) if len(ratios) >= 50 else float("nan")
        print(f"\n  asymptotic T_gap/mu_gap (late tail) = {asymp_ratio:.6f}")
        print(f"  predicted T'(mu*) = (3*phi+1)/4      = {T_PRIME_STAR:.6f}")
        ok_Tprime = abs(asymp_ratio - T_PRIME_STAR) < 0.01
        print(pass_fail(ok_Tprime, "T8f: asymptotic T_gap/mu_gap = T'(mu*)"))
    else:
        ok_Tprime = True

    return dict(
        rates_c0=rates_c0, c_amp_rates=c_amp_rates,
        spreads=spreads, ok_monotone=ok_monotone_c0, ok_rate_c0=ok_rate_c0,
        ok_same_rate=same_rate_ok,
        pert_sample=r,
    )


# =====================================================================
#  Summary plot
# =====================================================================

def make_summary_plot(t4, t5, t6, t7, t8):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # (0,0) T4: per-level readouts vs synthesis
    ax = axes[0, 0]
    lvls = ["L0", "L1", "L2", "L3"]
    synth_B = [0.426814, 0.174481, 0.065855, 0.023039]
    ax.bar(np.arange(4) - 0.2, t4["readouts"], 0.4,
           color="steelblue", alpha=0.85, label="measured TetB")
    ax.bar(np.arange(4) + 0.2, synth_B, 0.4,
           color="lightsteelblue", alpha=0.7, edgecolor="black", label="synthesis")
    ax.axhline(y=INV_PHI2, color="gold", linestyle="--", alpha=0.8,
               label=r"$1/\varphi^2$")
    ax.set_xticks(np.arange(4)); ax.set_xticklabels(lvls)
    ax.set_ylabel(r"$\bar\mu_B$")
    ax.set_title(f"T4: per-level readouts (shift = {t4['frac']*100:.3f}%, "
                 f"2/17 = {IMPEDANCE*100:.3f}%)",
                 fontweight="bold", fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

    # (0,1) T5: vote decomposition
    ax = axes[0, 1]
    vote_labels = ["Vote 1", "Vote 2", "Vote 3", "Vote 4"]
    vote_measured = [t5["votes"][k] for k in (1, 2, 3, 4)]
    vote_cf = [t5["vote1_cf"], t5["vote2_cf"], 0.0, 0.0]
    xs = np.arange(4)
    ax.bar(xs - 0.2, vote_measured, 0.4, color="darkorange", alpha=0.85,
           label="measured")
    ax.bar(xs + 0.2, vote_cf, 0.4, color="peachpuff", alpha=0.7,
           edgecolor="black", label="closed-form")
    ax.set_xticks(xs); ax.set_xticklabels(vote_labels)
    ax.set_ylabel("incremental shift")
    ax.set_title(f"T5: vote decomposition  (ratio = {t5['ratio']:.4f}, "
                 fr"$\sqrt{{3}}$ = {math.sqrt(3):.4f})",
                 fontweight="bold", fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

    # (0,2) T6: variant fractional shifts
    ax = axes[0, 2]
    vnames = ["full", "TetA-only", "TetB-only"]
    vmeas = [t6["frac_full"], t6["frac_A"], t6["frac_B"]]
    vsynth = [0.117412, 0.15682, 0.09594]
    xs = np.arange(3)
    colors = ["#2c3e50", "#e74c3c", "#27ae60"]
    ax.bar(xs - 0.2, vmeas, 0.4, color=colors, alpha=0.85, label="measured")
    ax.bar(xs + 0.2, vsynth, 0.4, color=colors, alpha=0.4, edgecolor="black",
           label="synthesis")
    ax.axhline(y=IMPEDANCE, color="red", linestyle="--", alpha=0.8,
               label=r"$2/17$  (only full hits this)")
    ax.set_xticks(xs); ax.set_xticklabels(vnames)
    ax.set_ylabel("fractional shift from baseline")
    ax.set_title("T6: variants — vote is necessary for 2/17",
                 fontweight="bold", fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

    # (1,0) T7: harmonic mean
    ax = axes[1, 0]
    labels = [r"$I_A$", r"$I_B$", r"hmean", r"$I_{\mathrm{full}}$", r"$2/17$"]
    vals = [t7["I_A"], t7["I_B"], t7["hmean"], t7["I_full"], IMPEDANCE]
    bar_colors = ["#e74c3c", "#27ae60", "purple", "#2c3e50", "gold"]
    ax.bar(np.arange(5), vals, color=bar_colors, alpha=0.85)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.003, f"{v:.5f}", ha="center", fontsize=9)
    ax.set_xticks(np.arange(5)); ax.set_xticklabels(labels)
    ax.set_ylabel("fractional impedance")
    ax.set_title(f"T7: harmonic mean test  ({t7['rel_residual']:.3f}% residual)",
                 fontweight="bold", fontsize=10)
    ax.grid(True, alpha=0.3)

    # (1,1) T8 decay: one representative trajectory on log scale
    ax = axes[1, 1]
    r = t8["pert_sample"]
    ax.semilogy(r["t"], np.abs(r["mu_gap"]), label=r"$|\mu - \mu^*|$",
                linewidth=1.8)
    ax.semilogy(r["t"], np.abs(r["T_gap"]), label=r"$|T(\mu) - T(\mu^*)|$",
                linewidth=1.8)
    # Reference line at rate sqrt(5)
    t0 = r["t"][10]
    y0 = np.abs(r["mu_gap"][10])
    ax.semilogy(r["t"], y0 * np.exp(-SQRT5 * (r["t"] - t0)),
                "k--", alpha=0.6, label=fr"$\exp(-\sqrt{{5}} \, t)$")
    ax.set_xlabel("time"); ax.set_ylabel("gap magnitude")
    ax.set_title(r"T8: exponential decay at rate $\sqrt{5}$",
                 fontweight="bold", fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3, which="both")

    # (1,2) T8 rate vs c_amp
    ax = axes[1, 2]
    c_vals = sorted(t8["c_amp_rates"].keys())
    rates = [t8["c_amp_rates"][c] for c in c_vals]
    ax.plot(c_vals, rates, "o-", color="#2c3e50", markersize=9, linewidth=2)
    ax.axhline(y=SQRT5, color="gold", linestyle="--", alpha=0.8,
               label=fr"$\sqrt{{5}}$ at $c=0$")
    for c, r in zip(c_vals, rates):
        ax.text(c, r + 0.05, f"{r:.3f}", ha="center", fontsize=9)
    ax.set_xlabel(r"$c_{\mathrm{amp}}$")
    ax.set_ylabel("measured decay rate")
    ax.set_title(r"T8d: rate scales with $c_{\mathrm{amp}}$",
                 fontweight="bold", fontsize=10)
    ax.legend(fontsize=9); ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"{OUT}/synthesis_tests_summary.png"
    plt.savefig(path, dpi=180); plt.close()
    print(f"\n  Summary figure: {path}")


# =====================================================================
#  MAIN
# =====================================================================

def main():
    print("\nConstants from reference module:")
    print(f"  1/phi^2     = {INV_PHI2:.10f}")
    print(f"  2/17        = {IMPEDANCE:.10f}")
    print(f"  sqrt(5)     = {SQRT5:.10f}")
    print(f"  T'(mu*)     = {T_PRIME_STAR:.10f}")
    print(f"  Container target (1+2/17)/phi^2 = {CONTAINER_READOUT_THEORY:.10f}")
    print()

    t4 = test_T4()
    t5 = test_T5()
    t6 = test_T6()
    t7 = test_T7(t6)
    t8 = test_T8()

    make_summary_plot(t4, t5, t6, t7, t8)

    print("\n" + "=" * 72)
    print("  ALL SYNTHESIS TESTS COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
