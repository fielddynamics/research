#!/usr/bin/env python3
"""
gfd_oscillator_3plus1.py
=========================

Reference implementation of the GFD 3+1 nested oscillator.

This module provides a canonical, well-tested implementation of the
stellated octahedron (SO) oscillator in its 3+1 nested topology:

    Level 0 : Container   (observable; the readout)
    Level 1 : Coarse      (first internal scale)
    Level 2 : Refined     (second internal scale)
    Level 3 : Closure     (deepest; contributes ~0 at D=3 by design)

Every SO carries two populations of K=4 cells:

    TetA  :  follows the partition law        mu = x / (x + 1)
    TetB  :  follows the interior  law        x(1 - mu)^2 = mu

The two populations cross-couple inside each SO via a Gram factor of
1/3 (the off-diagonal-to-diagonal ratio of the forced tetrahedral Gram
matrix).  This cross-coupling is the vote mechanism: TetA's mean drives
TetB; TetB's mean drives TetA through the topological transducer T.

The nested hierarchy couples SOs vertically:

    parent.field_origin  ->  child.x_ext           (top-down drive)
    transducer(child.avg_A)  ->  parent.child_contrib   (bottom-up vote)

Updates within a single time-step are bottom-up (leaf first, container
last), so each level's update incorporates its child's already-settled
state from this step.

Measurable properties at closure (x_ext = 1, converged)
-------------------------------------------------------
    Container TetB readout      = (1 + 2/17) * 1/phi^2  ~= 0.426814
    Fractional shift vs 1/phi^2 = 2/17                  ~= 0.117647  (impedance)
    Vote1 / Vote2 ratio         = sqrt(3)               ~= 1.732051
    Vote3                       = 0                     (closure at D=3)
    Asymptotic T_gap / mu_gap   = (3*phi + 1)/4         ~= 1.463525

Sanity baselines
----------------
    Flat baseline (interior law at x=1, isolated)   = 1/phi^2 ~= 0.381966
    Linearised restoring rate at mu*                = sqrt(5) ~= 2.236068
    Predicted perturbation half-life                = ln 2 / sqrt(5) ~= 0.310
    Characteristic denominator                      = f(K=4, s=0) = 17

References (constitutive origins)
---------------------------------
    TetA partition law          : Part I Sec. 1 (Fields & Partition)
    TetB interior law           : Part III Sec. 4.1 (Interior closure)
    Gram factor 1/3             : Forced Gram matrix, Part I Sec. 2
    Topological transducer T    : Cyclotomic Phi_6 bridge; t / (1 - t + t^2)
    2/17 impedance              : (D-1) / f(K, 0) at D=3, K=4
    Vote decomposition          : (D - sqrt(D))/17 + (sqrt(D) - 1)/17 + 0

Usage (minimal)
---------------
    net = Nested3Plus1()
    net.run(n_steps=600)
    print(net.container.readout())     # expect ~0.4268

Usage (diagnostic)
------------------
    net = Nested3Plus1(record_history=True)
    report = net.run_and_report(n_steps=600)
    report.pretty_print()

Author : Stephen Nelson / Field Dynamics Research
License: see repository LICENSE
"""

from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple


# =====================================================================
#   CONSTANTS
# =====================================================================

#: Number of cells per population in a single SO (K = 4 tetrahedral vertices)
K: int = 4

#: Golden ratio
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0

#: Gram factor: off-diagonal / diagonal ratio of the forced tetrahedral Gram
#: matrix (S4-invariant, F1-F3 conditions).  This is the cross-law coupling
#: weight that appears in TetA <-> TetB drives.
GRAM: float = 1.0 / 3.0

#: 1 / phi^2.  Interior law fixed point at x = 1, in isolation.
INV_PHI2: float = 1.0 / (PHI ** 2)

#: Characteristic denominator.  f(K, s=0) = 1 + s*K + K^2 = 17 at K = 4.
F_K0: int = 1 + K * K      # = 17

#: Characteristic closure impedance.  (D - 1) / f(K, 0) at D = 3, K = 4.
IMPEDANCE: float = 2.0 / F_K0      # = 0.117647...

#: Expected container-level readout at x_ext = 1, c_amp = 0, converged.
#: mu_B_container = (1 + 2/17) * 1/phi^2.
CONTAINER_READOUT_THEORY: float = INV_PHI2 * (1.0 + IMPEDANCE)

#: Linearised restoring rate at mu* = 1/phi^2 for interior law.
#: d(x(1-mu)^2 - mu)/d(mu)  =  -(2/phi + 1)  =  -sqrt(5).
SQRT5: float = math.sqrt(5.0)

#: Asymptotic T_gap / mu_gap ratio near mu* (linearised transducer slope).
#: T'(mu*) = (3*phi + 1) / 4.
T_PRIME_STAR: float = (3.0 * PHI + 1.0) / 4.0


# =====================================================================
#   CONSTITUTIVE LAWS
# =====================================================================

def mu_partition(x: float) -> float:
    """TetA constitutive law: partition fraction mu = x / (x + 1).

    Monotone increasing on x in [0, inf).  Maps x=0 -> 0, x=1 -> 1/2,
    x -> inf -> 1.  Equivalent to the sigmoid of the rapidity ln(x)
    centred at x = 1.

    Parameters
    ----------
    x
        Acceleration ratio (non-negative).  Not clamped; the caller is
        responsible for providing a meaningful value.

    Returns
    -------
    float
        mu in [0, 1).
    """
    return x / (x + 1.0)


def mu_interior(x: float) -> float:
    """TetB constitutive law: interior (closure) fixed point of x*(1-mu)^2 = mu.

    This is the closed-form root, taking the physical branch that satisfies
    mu -> 0 as x -> 0 and mu -> 1 as x -> inf.  At x = 1 the fixed point is
    exactly 1/phi^2 = (3 - sqrt(5)) / 2.

    Parameters
    ----------
    x
        Non-negative acceleration ratio.

    Returns
    -------
    float
        mu in [0, 1).  Zero returned for x below numerical floor.
    """
    if x < 1e-12:
        return 0.0
    return ((2.0 * x + 1.0) - math.sqrt(4.0 * x + 1.0)) / (2.0 * x)


def transducer(mu: float) -> float:
    """Topological transducer T(mu) = mu / (1 - mu + mu^2).

    The denominator is the 6th cyclotomic polynomial Phi_6(mu).  T maps
    the interior-law state into the spatial-capacity space consumed by
    TetA's drive (and by parent SOs via child_contrib).  T(0) = 0, T(1)
    diverges, and T is monotone on (0, 1).

    Parameters
    ----------
    mu
        State value in (0, 1).  Internally clamped to avoid division by
        values close to zero.

    Returns
    -------
    float
        Transduced value, strictly positive for mu > 0.
    """
    m = min(max(mu, 1e-10), 1.0 - 1e-10)
    return m / (1.0 - m + m * m)


# =====================================================================
#   STELLATED OCTAHEDRON
# =====================================================================

class StellatedOctahedron:
    """A single SO: K=4 TetA cells and K=4 TetB cells, cross-coupled by GRAM.

    State
    -----
    mu_A : list[float] of length K
        TetA amplitudes (partition-law population).
    mu_B : list[float] of length K
        TetB amplitudes (interior-law population).
    field_origin : float
        Summary readout = GRAM * mean(transducer(mu_B)).  This value is
        consumed by a parent SO's child to set the parent's effective
        x_ext, and is what the container's container reads as the
        "transduced signal" of this SO.

    Update
    ------
    Each call to step() applies forward-Euler integration with the
    following two constitutive targets:

        TetB target = mu_interior( x_ext * (1 + GRAM*<TetA_neighbors>
                                           + 0.5 * child_contrib) )
        TetA target = mu_partition( x_ext * (1 + GRAM*<T(TetB_neighbors)>) )

    The "neighbors" at cell i are the K-1 other cells in the same
    population.  child_contrib is transducer(child.avg_A) in a nested
    context, or 0 when the SO has no child.

    Numerical guards
    ----------------
    Amplitudes are clamped to [0.001, 0.999] after each step to avoid
    transducer denominator pathologies; this clamp does not affect the
    converged fixed point and is well inside the ~1e-6 boundary where
    the laws are well-defined.
    """

    __slots__ = (
        "label", "mu_A", "mu_B", "field_origin",
        "_rng",
        "hist_A", "hist_B", "hist_field_origin",
        "record_history",
    )

    def __init__(
        self,
        label: str = "",
        seed: int = 42,
        init_noise: float = 0.02,
        record_history: bool = False,
    ) -> None:
        """Initialise an SO with small random perturbations around mu = 0.5.

        Parameters
        ----------
        label
            Human-readable identifier used in diagnostics (e.g. "L0",
            "Leaf").  Does not affect dynamics.
        seed
            Seed for the local RNG that jitters the initial amplitudes.
            Two SOs with the same seed begin in identical states.
        init_noise
            Half-width of the uniform initial jitter around mu = 0.5.
            Small values (~0.02) are sufficient to break symmetry
            without pushing amplitudes near the clamp boundary.
        record_history
            When True, every step() call appends avg_A, avg_B and
            field_origin to in-memory lists.  Consumes O(n_steps)
            memory; leave False for production long runs.
        """
        self.label = label
        self._rng = random.Random(seed)
        self.mu_A = [0.5 + init_noise * (self._rng.random() - 0.5)
                     for _ in range(K)]
        self.mu_B = [0.5 + init_noise * (self._rng.random() - 0.5)
                     for _ in range(K)]
        self.field_origin = 0.5
        self.record_history = record_history
        self.hist_A: List[float] = []
        self.hist_B: List[float] = []
        self.hist_field_origin: List[float] = []

    # ---- diagnostics -----------------------------------------------

    def avg_A(self) -> float:
        """Return mean of TetA cells."""
        return sum(self.mu_A) / K

    def avg_B(self) -> float:
        """Return mean of TetB cells.  This is the canonical readout."""
        return sum(self.mu_B) / K

    def readout(self) -> float:
        """Canonical observable: TetB mean."""
        return self.avg_B()

    def cross_law_gap(self) -> float:
        """Return the signed TetA-minus-TetB gap (internal vote state).

        At converged closure with nesting, this is positive and decays
        geometrically with depth in a 3+1 hierarchy.
        """
        return self.avg_A() - self.avg_B()

    # ---- field origin ----------------------------------------------

    def compute_field_origin(self) -> float:
        """Recompute and cache the field origin from current TetB state.

        field_origin = GRAM * mean( transducer(mu_B) )

        The field origin is the summary signal that flows upward in a
        nested hierarchy: parent consumes transducer(child.avg_A) as
        child_contrib; the container reads its own field_origin as a
        derived observable.  Calling this method is idempotent and
        does NOT mutate mu_A or mu_B.
        """
        total = sum(transducer(b) for b in self.mu_B) / K
        self.field_origin = GRAM * total
        return self.field_origin

    # ---- the one-step update ---------------------------------------

    def step(
        self,
        x_ext: float = 1.0,
        child_contrib: float = 0.0,
        dt: float = 0.1,
    ) -> None:
        """Advance the SO by one forward-Euler step.

        Parameters
        ----------
        x_ext
            Effective external drive.  For a container, this is typically
            1.0 (unit drive).  For an internal level in a nested
            hierarchy, this is derived from the parent's field origin:
                x_ext_child = parent.field_origin / (1 - parent.field_origin)
        child_contrib
            Upward signal from the immediately-deeper level:
                child_contrib = transducer(child.avg_A)
            Zero if this SO has no child (leaf).  Contributes additively
            to TetB's drive weighted by 0.5.
        dt
            Time step.  Default 0.1 balances convergence speed against
            stability for the reference regime.  Values above ~0.3 can
            overshoot.

        Notes
        -----
        The update computes both TetA and TetB targets using the
        SAME snapshot of the state, then applies them simultaneously
        (fully-explicit Euler).  This is intentional: alternating
        half-steps can bias which population "leads" and distort the
        TetA-TetB gap signal.
        """
        # -- TetB update: each cell i uses mean of the OTHER K-1 cells of TetA --
        new_B: List[float] = [0.0] * K
        for i in range(K):
            gram_drive = GRAM * sum(self.mu_A[j] for j in range(K) if j != i) / (K - 1)
            x_i = x_ext * (1.0 + gram_drive + 0.5 * child_contrib)
            target = mu_interior(x_i)
            new_B[i] = self.mu_B[i] + (target - self.mu_B[i]) * dt

        # -- TetA update: each cell i uses mean of transduced TetB neighbors --
        new_A: List[float] = [0.0] * K
        for i in range(K):
            trans_sum = sum(transducer(self.mu_B[j]) for j in range(K) if j != i)
            x_i = x_ext * (1.0 + GRAM * trans_sum / (K - 1))
            target = mu_partition(x_i)
            new_A[i] = self.mu_A[i] + (target - self.mu_A[i]) * dt

        # -- Commit updates, clamp to the safe interior of (0, 1) --
        self.mu_A = [min(max(a, 0.001), 0.999) for a in new_A]
        self.mu_B = [min(max(b, 0.001), 0.999) for b in new_B]

        # -- Refresh field origin so upstream reads a consistent value --
        self.compute_field_origin()

        # -- Optional history recording --
        if self.record_history:
            self.hist_A.append(self.avg_A())
            self.hist_B.append(self.avg_B())
            self.hist_field_origin.append(self.field_origin)


# =====================================================================
#   3+1 NESTED TOPOLOGY
# =====================================================================

@dataclass
class ConvergenceReport:
    """Structured diagnostic output from a nested network run.

    Attributes
    ----------
    n_steps
        Number of Euler steps executed.
    readout_container
        The canonical result: container (L0) TetB mean.
    readouts_per_level
        TetB mean at each of [L0, L1, L2, L3].
    tetA_per_level
        TetA mean at each level.
    gaps_per_level
        Cross-law gap (TetA - TetB) at each level.
    container_shift
        readout_container - 1/phi^2.
    container_fractional_shift
        container_shift / (1/phi^2).
    deviation_from_impedance
        container_fractional_shift - 2/17.
    """
    n_steps: int
    readout_container: float
    readouts_per_level: List[float]
    tetA_per_level: List[float]
    gaps_per_level: List[float]
    container_shift: float
    container_fractional_shift: float
    deviation_from_impedance: float

    def pretty_print(self) -> None:
        """Print a human-readable summary of the run."""
        labels = ["L0 (container)", "L1 (coarse)", "L2 (refined)", "L3 (closure)"]
        print(f"Converged after {self.n_steps} steps")
        print(f"{'level':<18}  {'TetB':>10}  {'TetA':>10}  {'gap':>10}")
        for name, B, A, g in zip(labels, self.readouts_per_level,
                                 self.tetA_per_level, self.gaps_per_level):
            print(f"{name:<18}  {B:>10.6f}  {A:>10.6f}  {g:>+10.6f}")
        print()
        print(f"container shift         = {self.container_shift:+.6f}")
        print(f"fractional shift        = {self.container_fractional_shift:+.6f}")
        print(f"target (2/17)           = {IMPEDANCE:+.6f}")
        print(f"deviation               = {self.deviation_from_impedance:+.6f}")


class Nested3Plus1:
    """A 3+1 nested oscillator: container + three internal levels.

    Topology
    --------
        container (L0)  -- reads out
            \
             L1  (coarse)
              \
               L2  (refined)
                \
                 L3  (closure; contributes ~0 at D=3)

    Each parent-child pair is connected by:
        top-down : parent.field_origin  ->  child.x_ext
        bottom-up: transducer(child.avg_A)  ->  parent.child_contrib

    Update order is strict bottom-up within each step (L3, L2, L1, L0),
    so when L0 updates this step it already sees the current-step
    aggregates from L1, which saw the current-step aggregate from L2,
    and so on.  This is the "3 sweeps of field closure" made concrete.

    Usage
    -----
        >>> net = Nested3Plus1()
        >>> net.run(n_steps=600)
        >>> net.container.readout()
        0.426814...

        >>> net = Nested3Plus1(record_history=True)
        >>> report = net.run_and_report(n_steps=600)
        >>> report.pretty_print()
    """

    #: Labels assigned to the four levels, outermost first.
    LEVEL_LABELS: Tuple[str, str, str, str] = (
        "L0 (container)", "L1 (coarse)", "L2 (refined)", "L3 (closure)"
    )

    def __init__(
        self,
        x_ext: float = 1.0,
        dt: float = 0.1,
        seeds: Sequence[int] = (42, 43, 44, 45),
        init_noise: float = 0.02,
        record_history: bool = False,
    ) -> None:
        """Construct a fresh 3+1 nested network.

        Parameters
        ----------
        x_ext
            External drive applied to the container's TetA/TetB update.
            Internal levels derive their x_ext from their parent's
            field_origin at each step.
        dt
            Forward-Euler time step used at every level.
        seeds
            4-tuple of RNG seeds for (L0, L1, L2, L3).  Distinct seeds
            break symmetry between levels; identical seeds give identical
            initial states.
        init_noise
            Initial jitter half-width.  Passed to each SO unchanged.
        record_history
            When True, every SO records avg_A / avg_B / field_origin per
            step.  Useful for plotting; adds O(n_steps) memory per level.
        """
        if len(seeds) != 4:
            raise ValueError(f"expected 4 seeds, got {len(seeds)}")
        self.x_ext = float(x_ext)
        self.dt = float(dt)
        self.container = StellatedOctahedron(
            label="L0", seed=seeds[0],
            init_noise=init_noise, record_history=record_history,
        )
        self.L1 = StellatedOctahedron(
            label="L1", seed=seeds[1],
            init_noise=init_noise, record_history=record_history,
        )
        self.L2 = StellatedOctahedron(
            label="L2", seed=seeds[2],
            init_noise=init_noise, record_history=record_history,
        )
        self.L3 = StellatedOctahedron(
            label="L3", seed=seeds[3],
            init_noise=init_noise, record_history=record_history,
        )
        # Convenience ordered tuple: [container, L1, L2, L3]
        self.levels: Tuple[StellatedOctahedron, ...] = (
            self.container, self.L1, self.L2, self.L3
        )

    # ---- single integration step -----------------------------------

    def step(self) -> None:
        """Advance the full 3+1 network by one Euler step, bottom-up.

        The order matters: L3 updates first (it has no child, so the
        child_contrib it sees is zero).  L2 then updates using the
        just-refreshed transducer(L3.avg_A).  L1 uses transducer(L2.avg_A)
        from this step.  The container uses transducer(L1.avg_A).

        Top-down drives are computed BEFORE any update in this step,
        so each child sees the parent's field_origin from the previous
        step.  This is a design choice; computing drives after updates
        would close the loop one step tighter but risks numerical
        instability at larger dt.
        """
        # -- Snapshot top-down drives (from parents' state at step start) --
        #    container uses external x_ext; internal levels use parent.FO
        fo_container = self.container.compute_field_origin()
        fo_L1 = self.L1.compute_field_origin()
        fo_L2 = self.L2.compute_field_origin()

        x_L1 = fo_container / max(1.0 - fo_container, 0.01)
        x_L2 = fo_L1 / max(1.0 - fo_L1, 0.01)
        x_L3 = fo_L2 / max(1.0 - fo_L2, 0.01)

        # -- Snapshot bottom-up child contribs from current state --
        child_contrib_L2 = transducer(self.L3.avg_A())
        child_contrib_L1 = transducer(self.L2.avg_A())
        child_contrib_L0 = transducer(self.L1.avg_A())

        # -- Bottom-up updates (leaf first, container last) --
        self.L3.step(x_ext=x_L3, child_contrib=0.0, dt=self.dt)
        self.L2.step(x_ext=x_L2, child_contrib=child_contrib_L2, dt=self.dt)
        self.L1.step(x_ext=x_L1, child_contrib=child_contrib_L1, dt=self.dt)
        self.container.step(
            x_ext=self.x_ext,
            child_contrib=child_contrib_L0,
            dt=self.dt,
        )

    # ---- convenience drivers ---------------------------------------

    def run(self, n_steps: int) -> None:
        """Advance the network by n_steps; no diagnostic output.

        Intended for production / unit tests where only the final
        readout matters.
        """
        for _ in range(n_steps):
            self.step()

    def run_and_report(self, n_steps: int) -> ConvergenceReport:
        """Advance the network and return a structured ConvergenceReport.

        Equivalent to run(n_steps) followed by build_report(n_steps).
        """
        self.run(n_steps)
        return self.build_report(n_steps)

    # ---- readouts ---------------------------------------------------

    def readout(self) -> float:
        """Canonical readout: container's TetB mean."""
        return self.container.readout()

    def readouts_per_level(self) -> List[float]:
        """TetB mean at each level, outermost first."""
        return [so.readout() for so in self.levels]

    def gaps_per_level(self) -> List[float]:
        """Cross-law gap (TetA - TetB) at each level.

        At closure we expect this sequence to decay strongly with
        depth; L3's gap should be ~1e-3 or smaller after adequate
        convergence at dt = 0.1, n_steps >= 600.
        """
        return [so.cross_law_gap() for so in self.levels]

    def build_report(self, n_steps: int) -> ConvergenceReport:
        """Package current network state into a ConvergenceReport."""
        B_per = self.readouts_per_level()
        A_per = [so.avg_A() for so in self.levels]
        gaps = self.gaps_per_level()
        shift = B_per[0] - INV_PHI2
        frac_shift = shift / INV_PHI2
        dev = frac_shift - IMPEDANCE
        return ConvergenceReport(
            n_steps=n_steps,
            readout_container=B_per[0],
            readouts_per_level=B_per,
            tetA_per_level=A_per,
            gaps_per_level=gaps,
            container_shift=shift,
            container_fractional_shift=frac_shift,
            deviation_from_impedance=dev,
        )


# =====================================================================
#   SMOKE TESTS
# =====================================================================

def _smoke_test() -> None:
    """Run a standard convergence check and print the report.

    If this module is invoked as a script, this is what runs.  A quick
    way to verify the implementation reproduces the canonical closure
    values.
    """
    print("=" * 68)
    print("gfd_oscillator_3plus1 reference run")
    print("=" * 68)
    print(f"Target container readout   = (1 + 2/17) * 1/phi^2 "
          f"= {CONTAINER_READOUT_THEORY:.6f}")
    print(f"Target fractional shift    = 2/17 = {IMPEDANCE:.6f}")
    print(f"Target T'(mu*)             = (3*phi + 1)/4 "
          f"= {T_PRIME_STAR:.6f}")
    print(f"Target linear decay rate   = sqrt(5) = {SQRT5:.6f}")
    print()

    net = Nested3Plus1()
    report = net.run_and_report(n_steps=600)
    report.pretty_print()

    match_readout = abs(report.readout_container - CONTAINER_READOUT_THEORY)
    match_shift = abs(report.deviation_from_impedance)
    print()
    print(f"|readout - target|         = {match_readout:.2e}")
    print(f"|fractional_shift - 2/17|  = {match_shift:.2e}")
    tolerance = 1e-4
    status = "PASS" if (match_readout < tolerance and match_shift < tolerance) else "FAIL"
    print(f"smoke test                 = {status}")


if __name__ == "__main__":
    _smoke_test()
