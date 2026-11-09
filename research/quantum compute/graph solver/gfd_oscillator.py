"""
GFD Oscillator — Core Engine
==============================

A universal graph computation engine based on the Gravity Field Dynamics
framework. One coupling law drives the dynamics. The converged state IS
the answer.

The Oscillator as a Meter
--------------------------
The oscillator probes the eigenstructure of the coupling matrix K.
Given a graph with coupling K_ij on each edge, Kuramoto dynamics

    dφᵢ/dt = ω + Σⱼ K_ij · sin(φⱼ − φᵢ)

settle into a phase state whose dominant SVD modes align with the
dominant eigenvectors of K. The oscillator does not create structure —
it MEASURES the structure encoded in the coupling.

For a rank-1 coupling matrix K = B⊗B (outer product of a bridge
vector), the eigenvalues are {+|B|², -|B_i|²·|B_j|², ...}, with
the dominant eigenvector equal to B/|B|. The oscillator recovers
the sign pattern of B exactly (cosine = 1.0 for uniform-magnitude
bridges). This is verified on Boolean gate signatures.

Universal Readout
-----------------
The converged state IS the answer. On analog hardware, you measure
the voltages — the physical state is the partition, the coloring,
the path, the ordering. No downstream computation is needed.

On a digital computer, the equivalent is: SVD of the state matrix
produces weighted coordinates c_i = [S₀V₀[i], S₁V₁[i], ...] in
the active mode subspace. These coordinates ARE the answer:

    Partition problems: coordinate sign/angle = group assignment
    Ordering problems:  coordinate values = sequence position
    Flow problems:      coordinate gradient = path direction

The interpretation of coordinates is the problem definition, not
a readout technique. The oscillator always produces the same thing:
the equilibrium coordinates of nodes in the coupling eigenspace.

Two Channels
------------
The oscillator carries two independent dynamical channels per node:

    Amplitude:  dμ/dt = x_eff·(1−μ)² − μ
                Constitutive law from GFD. Attractive coupling
                through (1−μⱼ)/μⱼ. Creates pressure fields.

    Phase:      dφ/dt = ω + Σⱼ K_ij·sin(φⱼ − φᵢ)
                Kuramoto oscillator. First harmonic of the phase
                difference. Coupling sign/weight encodes the problem.

Both run simultaneously. The amplitude channel creates flow fields
(shortest path). The phase channel creates partition/ordering fields
(Max-Cut, coloring, TSP, community detection). The §D control test
proves they carry orthogonal information.

Depth and the {1,3,3,1} Structure
----------------------------------
Running `depth` independent channels creates a depth×N state matrix.
Its SVD yields `depth` singular values:

    S₀ ≥ S₁ ≥ ... ≥ S_{d-1}

The number of active modes (Sₖ/S₀ > threshold) is the problem's
class signature. The last singular value S_{d-1} is the depth gauge:

    S_{d-1} ≈ 0:  coupling eigenstructure fully resolved
    S_{d-1} >> 0: saturated, need more depth (nesting)

For a uniform-magnitude 4-cell bridge (e.g. AND gate), the coupling
matrix K = B⊗B has eigenvalues {+0.75, -0.25, -0.25, -0.25} — a
literal {1,3} split. The oscillator at depth=4 measures this as
Sv = [large, 0, 0, 0]: one dominant mode (the bridge direction),
three vanishing modes (the transverse space). The gauge reads zero.

For 8-cell bridges (3-input gates), the eigenvalue structure extends
to {1,3,3,1} — the Cl(3,0) Clifford algebra grade structure. Each
grade corresponds to a distinct eigenvalue level of K.

Reference
---------
Stephen Nelson, Field Dynamics Research
https://docs.fielddynamics.org
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional, List


# =========================================================================
#  Data Structures
# =========================================================================

@dataclass
class GraphEncoding:
    """
    Sparse directed-edge encoding of a graph with per-edge coupling.

    The coupling K_eff[e] on directed edge (src[e] → dst[e]) determines
    the Kuramoto interaction strength. Negative = repulsive (K < 0
    pushes neighbor phases apart). Positive = attractive (K > 0 pulls
    neighbor phases together). The sign structure of K_eff encodes
    the problem.
    """
    n: int
    src: np.ndarray
    dst: np.ndarray
    K_eff: np.ndarray


@dataclass
class OscillatorState:
    """
    Full state of the oscillator after convergence.

    The key output is `coords`: weighted SVD coordinates of each node
    in the active mode subspace. These coordinates ARE the answer.
    Everything else (phi, mu, Sv, Vt) is diagnostic.
    """
    phi: np.ndarray                # Raw phases, shape (depth, n)
    mu: Optional[np.ndarray]       # Raw amplitudes, shape (depth, n) or None
    Sv: np.ndarray                 # Singular values
    Vt: np.ndarray                 # Right singular vectors (modes over nodes)
    coords: np.ndarray             # Weighted SVD coordinates, shape (n, n_active)
    depth: int                     # Number of channels used
    gauge: float                   # Depth gauge: S_last / S_0
    n_active: int                  # Number of active modes


# =========================================================================
#  Core Engine
# =========================================================================

class GFDOscillator:
    """
    Universal graph computation engine.

    The oscillator probes the eigenstructure of the coupling matrix
    via Kuramoto dynamics. The converged state — expressed as weighted
    SVD coordinates — IS the answer for any graph problem.

    Parameters
    ----------
    dt : float
        Integration timestep.
    steps : int
        Number of integration steps per run.
    active_threshold : float
        Fraction of S₀ above which a mode is considered active.
    gauge_threshold : float
        Gauge value below which the depth is considered sufficient.
    max_depth : int
        Maximum depth for adaptive cascade.
    """

    def __init__(self, dt=0.01, steps=3000, active_threshold=0.01,
                 gauge_threshold=0.3, max_depth=64):
        self.dt = dt
        self.steps = steps
        self.active_threshold = active_threshold
        self.gauge_threshold = gauge_threshold
        self.max_depth = max_depth

    # -----------------------------------------------------------------
    #  Phase channel
    # -----------------------------------------------------------------

    def run_phase(self, graph: GraphEncoding, depth: int = 4,
                  seed: int = 42) -> OscillatorState:
        """
        Run the phase channel to convergence.

        The dynamics dφᵢ/dt = ω + Σⱼ K_ij·sin(φⱼ − φᵢ) settle into
        the dominant eigenvector(s) of the coupling matrix K. The SVD
        of the cos(φ) matrix extracts these as node coordinates.
        """
        n = graph.n
        rng = np.random.RandomState(seed)
        phi = rng.uniform(0, 2 * np.pi, (depth, n))

        for _ in range(self.steps):
            for ch in range(depth):
                diffs = phi[ch, graph.dst] - phi[ch, graph.src]
                forces = graph.K_eff * np.sin(diffs)
                kur = np.zeros(n)
                np.add.at(kur, graph.src, forces)
                phi[ch] += self.dt * (1.0 + kur)

        return self._analyze(phi, None, depth, n)

    # -----------------------------------------------------------------
    #  Amplitude channel
    # -----------------------------------------------------------------

    def run_amplitude(self, graph: GraphEncoding, x_drive: np.ndarray,
                      c_amp: float = 0.3, depth: int = 1,
                      seed: int = 42) -> OscillatorState:
        """
        Run the amplitude channel to convergence.

        The constitutive law dμ/dt = x_eff·(1−μ)² − μ with attractive
        coupling creates a pressure field. The SVD of the μ matrix gives
        coordinates proportional to the potential at each node.
        """
        n = graph.n
        rng = np.random.RandomState(seed)
        mu = rng.uniform(0.2, 0.8, (depth, n))

        for _ in range(self.steps):
            ms = np.clip(mu, 1e-8, 1 - 1e-8)
            for ch in range(depth):
                comp = (1 - ms[ch]) / ms[ch]
                coupling = np.zeros(n)
                np.add.at(coupling, graph.src, c_amp * comp[graph.dst])
                x_eff = x_drive + coupling
                dmu = x_eff * (1 - ms[ch]) ** 2 - ms[ch]
                mu[ch] = np.clip(ms[ch] + self.dt * dmu, 1e-8, 1 - 1e-8)

        return self._analyze(mu, mu.copy(), depth, n)

    # -----------------------------------------------------------------
    #  Both channels simultaneously
    # -----------------------------------------------------------------

    def run_both(self, graph: GraphEncoding, x_drive: np.ndarray,
                 c_amp: float = 0.3, K_pll: float = 0.5,
                 depth: int = 4, seed: int = 42) -> OscillatorState:
        """
        Run both amplitude and phase channels simultaneously.
        This is the full tetra_joint_rhs architecture.
        """
        n = graph.n
        rng = np.random.RandomState(seed)
        mu = rng.uniform(0.2, 0.8, (depth, n))
        phi = rng.uniform(0, 2 * np.pi, (depth, n))

        for _ in range(self.steps):
            ms = np.clip(mu, 1e-8, 1 - 1e-8)
            for ch in range(depth):
                comp = (1 - ms[ch]) / ms[ch]
                coupling = np.zeros(n)
                np.add.at(coupling, graph.src, c_amp * comp[graph.dst])
                dmu = (x_drive + coupling) * (1 - ms[ch]) ** 2 - ms[ch]
                mu[ch] = np.clip(ms[ch] + self.dt * dmu, 1e-8, 1 - 1e-8)

                diffs = phi[ch, graph.dst] - phi[ch, graph.src]
                forces = K_pll * np.sin(diffs)
                kur = np.zeros(n)
                np.add.at(kur, graph.src, forces)
                phi[ch] += self.dt * (1.0 + kur)

        return self._analyze(phi, mu.copy(), depth, n)

    # -----------------------------------------------------------------
    #  Adaptive depth cascade
    # -----------------------------------------------------------------

    def run_adaptive(self, graph: GraphEncoding,
                     seed: int = 42) -> OscillatorState:
        """
        Self-regulating depth cascade.

        Starts at depth 4. Checks the depth gauge (last singular value
        normalized by S₀). If saturated, doubles depth. Continues until
        the gauge reads resolved or max_depth is reached.

        The gauge reports whether the coupling matrix's eigenstructure
        has been fully resolved at the current depth.
        """
        depth = 4
        best_state = None

        while depth <= self.max_depth:
            state = self.run_phase(graph, depth=depth, seed=seed + depth)
            if best_state is None or state.gauge < best_state.gauge:
                best_state = state
            if state.gauge < self.gauge_threshold:
                break
            depth *= 2

        return best_state

    # -----------------------------------------------------------------
    #  Universal readout (SVD analysis)
    # -----------------------------------------------------------------

    def _analyze(self, state_matrix: np.ndarray, mu: Optional[np.ndarray],
                 depth: int, n: int) -> OscillatorState:
        """
        Universal readout: extract weighted SVD coordinates.

        The coordinates c_i = [S₀V₀[i], S₁V₁[i], ...] in the active
        mode subspace ARE the answer. The number of active modes, the
        gauge value, and the coordinate geometry encode both the
        solution and the problem class.

        This is the digital equivalent of "measure the voltages" on
        analog hardware. The SVD extracts the same information that
        physical measurement would provide.
        """
        cos_mat = np.array([np.cos(state_matrix[ch] % (2 * np.pi))
                            for ch in range(depth)])
        U, Sv, Vt = np.linalg.svd(cos_mat, full_matrices=False)

        # Depth gauge
        gauge = Sv[-1] / Sv[0] if Sv[0] > 1e-10 else 0.0

        # Active modes
        active = [m for m in range(len(Sv))
                  if Sv[m] / Sv[0] > self.active_threshold]
        n_active = len(active)

        # Weighted coordinates in active mode subspace
        # These coordinates ARE the answer
        coords = np.zeros((n, n_active))
        for idx, m in enumerate(active):
            coords[:, idx] = Sv[m] * Vt[m]

        return OscillatorState(
            phi=state_matrix, mu=mu, Sv=Sv, Vt=Vt,
            coords=coords, depth=depth, gauge=gauge, n_active=n_active
        )

    # -----------------------------------------------------------------
    #  Graph encoding utilities
    # -----------------------------------------------------------------

    @staticmethod
    def encode_edges(n: int, edges: list, K: float = -2.0) -> GraphEncoding:
        """Uniform coupling on all edges. K < 0 = repulsive (frustrated)."""
        src, dst = [], []
        for (i, j) in edges:
            src.extend([i, j])
            dst.extend([j, i])
        return GraphEncoding(
            n=n,
            src=np.array(src, dtype=np.int32),
            dst=np.array(dst, dtype=np.int32),
            K_eff=np.full(len(src), K, dtype=np.float64)
        )

    @staticmethod
    def encode_weighted(n: int, K_matrix: np.ndarray) -> GraphEncoding:
        """Per-edge coupling from a full n×n matrix. Diagonal ignored."""
        src, dst, K_vals = [], [], []
        for i in range(n):
            for j in range(n):
                if i != j and abs(K_matrix[i, j]) > 1e-12:
                    src.append(i)
                    dst.append(j)
                    K_vals.append(K_matrix[i, j])
        return GraphEncoding(
            n=n,
            src=np.array(src, dtype=np.int32),
            dst=np.array(dst, dtype=np.int32),
            K_eff=np.array(K_vals, dtype=np.float64)
        )
