"""
pi_walk_oscillator_k4d3.py
============================

K=4, D=3 π-walk oscillator with 64-channel connection decomposition
per the t-bit framework (tbit_algebra.md §6.2).

Physics:
  - 8 vertices on the stellated octahedron (2^D, D=3, fixed)
  - Two tetrahedra: TetA (4 vertices) and TetB (4 vertices)
  - K=4 means K=4 vertices per tetrahedron, K²=16 connection components per face
  - 4 faces × 16 channels = 64 total connection components
  - Walk traverses 64 hexagrams (one per channel), bijection between hexagrams
    and connection components

Channel decomposition (per face):
  - 4 diagonal (root-blind classical channels)
  - 6 upper-triangle (TetA coherent — sign-symmetric)
  - 6 lower-triangle (TetB coherent — sign-antisymmetric)
  → 4 + 6 + 6 = 16 per face

Face decomposition (4 faces):
  - AA: from ∈ TetA, to ∈ TetA  (16 hexagrams)
  - AB: from ∈ TetA, to ∈ TetB  (16 hexagrams)
  - BA: from ∈ TetB, to ∈ TetA  (16 hexagrams)
  - BB: from ∈ TetB, to ∈ TetB  (16 hexagrams)
  → 4 × 16 = 64 hexagrams = 64 channels

Output:
  - 64 coefficients per oscillator
  - Organized as (face, channel) = (4, 16)
  - Sub-organized within each face as (diagonal: 4, upper: 6, lower: 6)
"""

import numpy as np
from typing import Optional


# =====================================================================
# π in base 8
# =====================================================================

def pi_base8_digits(n_digits=400):
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


# =====================================================================
# Tetrahedral structure of the 8 vertices
# =====================================================================

def vertex_to_tet(v):
    """
    The 8 vertices split into TetA and TetB by parity.
    TetA: v with even popcount → 0, 3, 5, 6
    TetB: v with odd popcount  → 1, 2, 4, 7
    Returns 'A' or 'B'.
    """
    return 'A' if bin(v).count('1') % 2 == 0 else 'B'


def vertex_index_in_tet(v):
    """Position 0..3 of v within its own tet."""
    if vertex_to_tet(v) == 'A':
        # TetA = [0, 3, 5, 6] — return index in this list
        return [0, 3, 5, 6].index(v)
    else:
        # TetB = [1, 2, 4, 7]
        return [1, 2, 4, 7].index(v)


def hexagram_face(from_v, to_v):
    """
    Which face does hexagram (from_v, to_v) live on?
    Returns 'AA', 'AB', 'BA', 'BB' based on (from-tet, to-tet).
    """
    return vertex_to_tet(from_v) + vertex_to_tet(to_v)


def hexagram_channel(from_v, to_v):
    """
    Within a face, which channel does the hexagram occupy?
    Channel index (a, b) where a = position of `from` in its tet,
    b = position of `to` in its tet. Both ∈ [0..3].

    Returns (a, b) tuple, and channel_kind:
      - 'diagonal' (a == b): root-blind classical
      - 'upper' (a < b): TetA-coherent
      - 'lower' (a > b): TetB-coherent
    """
    a = vertex_index_in_tet(from_v)
    b = vertex_index_in_tet(to_v)
    if a == b:
        kind = 'diagonal'
    elif a < b:
        kind = 'upper'
    else:
        kind = 'lower'
    return (a, b), kind


# =====================================================================
# The K=4, D=3 π-walk oscillator
# =====================================================================

class PiWalkK4D3Oscillator:
    """
    K=4, D=3 oscillator with 64-channel connection decomposition.

    Atomic unit: 8-vertex input (truth-table or continuous, length 8).
    Output: 64 coefficients organized as:
        - 4 faces (AA, AB, BA, BB)
        - 16 channels per face
        - Per-face decomposition: 4 diagonal + 6 upper + 6 lower

    The walk is the same 64-hexagram closure walk as the standard π-walk;
    what's different is the readout — instead of projecting through 8
    Walsh characters, we decompose into the 64 connection components.
    """

    N = 8                    # vertices
    K = 4                    # vertices per tet
    N_FACES = 4              # AA, AB, BA, BB
    N_CHANNELS_PER_FACE = 16 # K^2
    N_TOTAL_CHANNELS = 64    # 4 faces × 16 channels

    FACE_NAMES = ('AA', 'AB', 'BA', 'BB')

    # The two tets
    TET_A = (0, 3, 5, 6)     # even popcount
    TET_B = (1, 2, 4, 7)     # odd popcount

    def __init__(self, max_walk_steps=400):
        self.max_walk_steps = max_walk_steps
        self._walk = self._build_walk()

    def _build_walk(self):
        """
        Build the deterministic π hexagram walk.
        Stops at full closure (all 64 ordered pairs visited).
        """
        digits = pi_base8_digits(self.max_walk_steps)
        seen = set()
        walk = []
        for k in range(len(digits) - 1):
            a, b = digits[k], digits[k + 1]
            walk.append((a, b))
            seen.add((a, b))
            if len(seen) == 64:
                break
        return walk

    def settle(self, y):
        """
        Settle on an 8-element input. Returns a coefficient bank with
        face-channel structure.

        Args:
            y: array-like, length 8

        Returns:
            dict {
              'coeffs':         shape (64,) — flat coefficient vector
              'by_face':        dict {face: shape (16,) coeffs}
              'by_channel_kind':dict {face: dict {kind: array}}
              'walk_length':    int
            }
        """
        y = np.asarray(y, dtype=np.float64)
        if y.shape[-1] != self.N:
            raise ValueError(f"Input must have last dim = {self.N}, got {y.shape}")

        # Convert binary to spin if needed
        unique_vals = set(np.unique(y).tolist())
        if unique_vals <= {0.0, 1.0}:
            s = 2.0 * y - 1.0
        else:
            s = y

        # Build the K-matrix: K[from, to] = s[from XOR to]
        # This is the XOR-convolution matrix used by the framework.
        K_matrix = np.zeros((self.N, self.N), dtype=np.float64)
        for i in range(self.N):
            for j in range(self.N):
                K_matrix[i, j] = s[i ^ j]

        # Initialize coefficient bank: organized by face
        # Each face has 16 channels indexed by (a_idx, b_idx) where
        # a_idx, b_idx ∈ [0..3].
        by_face = {face: np.zeros((self.K, self.K)) for face in self.FACE_NAMES}
        visit_count = {face: np.zeros((self.K, self.K), dtype=np.int64)
                       for face in self.FACE_NAMES}

        # Walk through hexagrams, accumulating per-channel coefficients
        for (from_v, to_v) in self._walk:
            face = hexagram_face(from_v, to_v)
            (a, b), kind = hexagram_channel(from_v, to_v)
            reading = K_matrix[from_v, to_v]
            by_face[face][a, b] += reading
            visit_count[face][a, b] += 1

        # Normalize: divide by visit count to get average per-channel reading
        for face in self.FACE_NAMES:
            mask = visit_count[face] > 0
            by_face[face] = np.where(mask,
                                      by_face[face] / np.maximum(visit_count[face], 1),
                                      0.0)

        # Decompose each face's 16 channels into kinds: diagonal/upper/lower
        by_channel_kind = {}
        for face in self.FACE_NAMES:
            mat = by_face[face]
            diag = np.array([mat[i, i] for i in range(self.K)])  # 4
            upper = np.array([mat[i, j] for i in range(self.K)
                              for j in range(i + 1, self.K)])     # 6
            lower = np.array([mat[i, j] for i in range(self.K)
                              for j in range(i)])                 # 6
            by_channel_kind[face] = {
                'diagonal': diag,
                'upper': upper,
                'lower': lower,
            }

        # Flat 64-coefficient vector
        flat = np.concatenate([by_face[face].flatten() for face in self.FACE_NAMES])

        return {
            'coeffs': flat,
            'by_face': by_face,
            'by_channel_kind': by_channel_kind,
            'walk_length': len(self._walk),
            'visit_count': visit_count,
        }

    def settle_batched(self, Y):
        """
        Settle on a batch.
        Args:
            Y: shape (n_instances, 8)
        Returns:
            list of result dicts
        """
        Y = np.asarray(Y, dtype=np.float64)
        if Y.ndim == 1:
            return [self.settle(Y)]
        return [self.settle(Y[i]) for i in range(Y.shape[0])]

    # Diagnostics

    def channel_kind_counts(self):
        """Verify the framework's prediction: 4 diag + 6 upper + 6 lower per face."""
        counts = {face: {'diagonal': 0, 'upper': 0, 'lower': 0}
                  for face in self.FACE_NAMES}
        for (from_v, to_v) in [(i, j) for i in range(8) for j in range(8)]:
            face = hexagram_face(from_v, to_v)
            _, kind = hexagram_channel(from_v, to_v)
            counts[face][kind] += 1
        return counts

    def signal_strength(self, result):
        """Sum of squared coefficients."""
        return float(np.sum(result['coeffs'] ** 2))

    def face_energy(self, result):
        """Energy per face."""
        return {face: float(np.sum(result['by_face'][face] ** 2))
                for face in self.FACE_NAMES}

    def channel_kind_energy(self, result):
        """Energy per channel kind, summed across faces."""
        kinds = ('diagonal', 'upper', 'lower')
        energies = {kind: 0.0 for kind in kinds}
        for face in self.FACE_NAMES:
            for kind in kinds:
                energies[kind] += float(np.sum(
                    result['by_channel_kind'][face][kind] ** 2))
        return energies


# =====================================================================
if __name__ == "__main__":
    osc = PiWalkK4D3Oscillator()
    print("PiWalkK4D3Oscillator initialized")
    print(f"  Walk length: {len(osc._walk)} hexagrams")
    print(f"  Vertices: {osc.N}")
    print(f"  K (vertices per tet): {osc.K}")
    print(f"  Faces: {osc.N_FACES} ({osc.FACE_NAMES})")
    print(f"  Channels per face: {osc.N_CHANNELS_PER_FACE}")
    print(f"  Total channels: {osc.N_TOTAL_CHANNELS}")
    print()

    # Verify framework prediction: 4 diag + 6 upper + 6 lower per face
    counts = osc.channel_kind_counts()
    print("Hexagram counts per face per channel-kind (framework prediction: 4/6/6):")
    for face in osc.FACE_NAMES:
        c = counts[face]
        print(f"  {face}: diagonal={c['diagonal']}, upper={c['upper']}, lower={c['lower']}")
    print()

    # Run on XOR_3bit
    y = [0, 1, 1, 0, 1, 0, 0, 1]
    result = osc.settle(y)
    print(f"XOR_3bit input: {y}")
    print(f"  Walk length:   {result['walk_length']}")
    print(f"  Total energy:  {osc.signal_strength(result):.4f}")
    print()
    print(f"  Face energies:")
    for face, e in osc.face_energy(result).items():
        print(f"    {face}: {e:.4f}")
    print()
    print(f"  Channel-kind energies (summed across faces):")
    for kind, e in osc.channel_kind_energy(result).items():
        print(f"    {kind}: {e:.4f}")
    print()
    print(f"  Coefficients shape: {result['coeffs'].shape}")
    print(f"  By-face shape:      {result['by_face']['AA'].shape}")
