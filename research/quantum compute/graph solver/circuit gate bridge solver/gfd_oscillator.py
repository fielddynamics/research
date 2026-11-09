"""
GFD Oscillator — Core Engine
==============================

A universal graph computation engine based on the Gravity Field Dynamics
framework. One coupling law — K·sin(φⱼ − φᵢ) — solves multiple classes
of NP-hard problems through anti-ferromagnetic phase frustration.

Architecture
------------
Each graph node carries `depth` independent phase oscillators.
The anti-ferromagnetic Kuramoto coupling pushes connected nodes toward
opposite phases. The frustrated equilibrium encodes the solution.

Two channels operate simultaneously:

    Amplitude:  dμ/dt = x_eff·(1−μ)² − μ
                Constitutive law from GFD. Ferromagnetic coupling.
                Solves flow/pressure problems (shortest path, maze).

    Phase:      dφ/dt = ω + Σⱼ K_ij·sin(φⱼ − φᵢ)
                Kuramoto oscillator. Coupling sign encodes the problem.
                Solves partition (Max-Cut, coloring), ordering (TSP),
                and clustering (community detection) problems.

Self-Regulation
---------------
The SVD of the depth×N cos(φ) matrix produces singular values S₀ ≥ S₁ ≥ ... ≥ S_{d-1}.

    - The number of active modes (S_k/S₀ > threshold) is the problem class signature.
    - The last singular value S_{d-1} is the depth gauge.
    - S_{d-1} ≈ 0: answer is resolved at this depth.
    - S_{d-1} >> 0: depth is saturated; double and re-run.

This implements the {1,3,3,1} grade structure of the Clifford algebra Cl(3,0):
three modes carry the answer, one mode reports the confidence.

Universal grade decomposition
-----------------------------
Depth 4 is the minimal SO (stella octangula, dual-tetrahedral Cl(3,0))
and handles the {1, 3, 3, 1} = 8-dimensional grade structure. For wider
problems whose natural state space is 2^n with n ≠ 3, the analogous
structure is {1, C(n,1), C(n,2), ..., C(n,n)} = 2^n — the exterior
algebra Cl(n, 0). Higher-grade content is accessed by nesting deeper
SOs. The depth-4 tetrahedral unit is the ontological base cell; all
larger structures are nestings of it.

For Walsh-bridge-encoded problems specifically (see gate_signature_tests.py
and bridge.py), the grade decomposition appears directly as the
Hamming-weight partition of the 2^n bridge cells — this is the same
universal structure read through a different projection.

Reference
---------
Stephen Nelson, Field Dynamics Research
https://docs.fielddynamics.org

License: MIT
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, List


# =========================================================================
#  Data Structures
# =========================================================================

@dataclass
class GraphEncoding:
    """
    Sparse directed-edge encoding of a graph with per-edge coupling weights.

    Attributes
    ----------
    n : int
        Number of nodes.
    src : np.ndarray
        Source node indices for each directed edge.
    dst : np.ndarray
        Destination node indices for each directed edge.
    K_eff : np.ndarray
        Effective coupling weight for each directed edge.
        Negative = anti-ferromagnetic (repel). Positive = ferromagnetic (attract).
    """
    n: int
    src: np.ndarray
    dst: np.ndarray
    K_eff: np.ndarray


@dataclass
class OscillatorState:
    """
    Full state of the oscillator after convergence.

    Attributes
    ----------
    phi : np.ndarray
        Phase array, shape (depth, n). The raw oscillator output.
    mu : Optional[np.ndarray]
        Amplitude array, shape (depth, n). Only populated when amplitude channel is active.
    Sv : np.ndarray
        Singular values from SVD of cos(φ) matrix.
    Vt : np.ndarray
        Right singular vectors. Each row Vt[k] is the k-th mode over nodes.
    depth : int
        Number of phase channels used.
    gauge : float
        Depth gauge: last singular value normalized by S₀.
    n_active : int
        Number of active modes (S_k/S₀ > threshold).
    """
    phi: np.ndarray
    mu: Optional[np.ndarray]
    Sv: np.ndarray
    Vt: np.ndarray
    depth: int
    gauge: float
    n_active: int


# =========================================================================
#  Core Engine
# =========================================================================

class GFDOscillator:
    """
    Universal graph computation engine.

    Parameters
    ----------
    dt : float
        Integration timestep. Default 0.01.
    steps : int
        Number of integration steps per run. Default 3000.
    active_threshold : float
        Threshold for counting active SVD modes (fraction of S₀). Default 0.01.
    gauge_threshold : float
        Threshold for depth gauge. Below this, the answer is considered resolved. Default 0.3.
    max_depth : int
        Maximum depth for adaptive cascade. Default 64.
    """

    def __init__(self, dt=0.01, steps=3000, active_threshold=0.01,
                 gauge_threshold=0.3, max_depth=64):
        self.dt = dt
        self.steps = steps
        self.active_threshold = active_threshold
        self.gauge_threshold = gauge_threshold
        self.max_depth = max_depth

    # -----------------------------------------------------------------
    #  Phase channel (Kuramoto)
    # -----------------------------------------------------------------

    def run_phase(self, graph: GraphEncoding, depth: int = 4,
                  seed: int = 42) -> OscillatorState:
        """
        Run the phase channel to convergence.

        Each node carries `depth` independent phase oscillators.
        The coupling K_ij·sin(φⱼ − φᵢ) is applied per edge.
        After convergence, SVD decomposes the cos(φ) matrix into
        orthogonal modes.

        Parameters
        ----------
        graph : GraphEncoding
            Sparse graph with per-edge coupling weights.
        depth : int
            Number of phase channels per node.
        seed : int
            Random seed for initial phase assignment.

        Returns
        -------
        OscillatorState
            Full state including phases, SVD decomposition, and gauge.
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
    #  Amplitude channel (constitutive law)
    # -----------------------------------------------------------------

    def run_amplitude(self, graph: GraphEncoding, x_drive: np.ndarray,
                      c_amp: float = 0.3, depth: int = 1,
                      seed: int = 42) -> OscillatorState:
        """
        Run the amplitude channel to convergence.

        Each node carries `depth` independent amplitude oscillators.
        The constitutive law dμ/dt = x_eff·(1−μ)² − μ with ferromagnetic
        coupling through (1−μⱼ)/μⱼ creates a pressure field.

        Parameters
        ----------
        graph : GraphEncoding
            Sparse graph (K_eff is ignored; coupling is always ferromagnetic).
        x_drive : np.ndarray
            Per-node external drive. Shape (n,).
        c_amp : float
            Amplitude coupling strength.
        depth : int
            Number of amplitude channels per node.
        seed : int
            Random seed.

        Returns
        -------
        OscillatorState
            Full state with amplitude field in mu.
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

        This is the full `tetra_joint_rhs` architecture. Both channels
        operate on the same graph, carrying orthogonal information.

        Parameters
        ----------
        graph : GraphEncoding
            Sparse graph. K_eff is used for phase coupling.
        x_drive : np.ndarray
            Per-node external drive for amplitude channel.
        c_amp : float
            Amplitude coupling strength.
        K_pll : float
            Phase-lock-loop coupling strength. Positive = ferromagnetic.
        depth : int
            Number of channels per node.
        seed : int
            Random seed.

        Returns
        -------
        OscillatorState
            Full state with both mu and phi.
        """
        n = graph.n
        rng = np.random.RandomState(seed)
        mu = rng.uniform(0.2, 0.8, (depth, n))
        phi = rng.uniform(0, 2 * np.pi, (depth, n))

        for _ in range(self.steps):
            ms = np.clip(mu, 1e-8, 1 - 1e-8)
            for ch in range(depth):
                # Amplitude
                comp = (1 - ms[ch]) / ms[ch]
                coupling = np.zeros(n)
                np.add.at(coupling, graph.src, c_amp * comp[graph.dst])
                dmu = (x_drive + coupling) * (1 - ms[ch]) ** 2 - ms[ch]
                mu[ch] = np.clip(ms[ch] + self.dt * dmu, 1e-8, 1 - 1e-8)

                # Phase
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

        Starts at depth 4. After convergence, checks the depth gauge
        (last singular value). If saturated, doubles the depth and
        re-runs. Continues until the gauge reads resolved or max_depth
        is reached.

        Parameters
        ----------
        graph : GraphEncoding
            Sparse graph with per-edge coupling weights.
        seed : int
            Base random seed.

        Returns
        -------
        OscillatorState
            State from the depth that resolved the problem.
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
    #  SVD analysis
    # -----------------------------------------------------------------

    def _analyze(self, phi: np.ndarray, mu: Optional[np.ndarray],
                 depth: int, n: int) -> OscillatorState:
        """
        Compute SVD decomposition and extract gauge and mode count.
        """
        cos_mat = np.array([np.cos(phi[ch] % (2 * np.pi))
                            for ch in range(depth)])
        U, Sv, Vt = np.linalg.svd(cos_mat, full_matrices=False)

        gauge = Sv[-1] / Sv[0] if Sv[0] > 1e-10 else 0.0
        n_active = sum(1 for s in Sv if s / Sv[0] > self.active_threshold)

        return OscillatorState(
            phi=phi, mu=mu, Sv=Sv, Vt=Vt,
            depth=depth, gauge=gauge, n_active=n_active
        )

    # -----------------------------------------------------------------
    #  Utility: build graph encodings
    # -----------------------------------------------------------------

    @staticmethod
    def encode_edges(n: int, edges: list, K: float = -2.0) -> GraphEncoding:
        """
        Build a GraphEncoding from an edge list with uniform coupling.

        Parameters
        ----------
        n : int
            Number of nodes.
        edges : list of (int, int)
            Undirected edges.
        K : float
            Coupling weight. Negative = anti-ferromagnetic.

        Returns
        -------
        GraphEncoding
        """
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
        """
        Build a GraphEncoding from a full coupling matrix.

        Non-zero entries become directed edges with coupling K_matrix[i,j].

        Parameters
        ----------
        n : int
            Number of nodes.
        K_matrix : np.ndarray
            n×n coupling matrix. Diagonal is ignored.

        Returns
        -------
        GraphEncoding
        """
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
