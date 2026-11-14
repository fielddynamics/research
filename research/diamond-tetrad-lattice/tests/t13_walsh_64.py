"""T13. The 8x8 sp3 Hamiltonian of a primitive cell and the 8x8 Walsh-Hadamard matrix.
Hybrid basis: A_a at cube vertex v_a (TetA), B_a at vertex -v_a (TetB). Harrison's minimal
model: -V2 exp(i k.v_a) between A_a and B_a (the bond), -V1 between hybrids on one atom,
-V3 on A and +V3 on B. Transform by the Walsh functions chi_S(v) = prod_{i in S} v_i.
Pass: block-diagonal at Gamma, with blocks matching the irreps."""
import itertools
import sympy as sp
from exact_common import verdict
V1, V2, V3 = sp.symbols("V1 V2 V3", real=True)
legs = [sp.Matrix(v) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
verts = legs + [-v for v in legs]


def H(k):
    M = sp.zeros(8)
    for a in range(4):
        for b in range(4):
            if a != b:
                M[a, b] = -V1; M[4 + a, 4 + b] = -V1
        M[a, a] = -V3; M[4 + a, 4 + a] = V3
        ph = sp.exp(sp.I * (k.T * legs[a])[0])
        M[a, 4 + a] = -V2 * ph; M[4 + a, a] = -V2 * sp.conjugate(ph)
    return M


subsets = [(), (0, 1, 2), (0,), (1, 2), (1,), (0, 2), (2,), (0, 1)]   # paired {1,xyz},{x,yz},{y,xz},{z,xy}
W = sp.Matrix([[sp.prod([v[i] for i in S]) for v in verts] for S in subsets])
print("W W^T = 8 I:", W * W.T == 8 * sp.eye(8))
ok = True
for name, k in [("Gamma", sp.Matrix([0, 0, 0])), ("X", sp.Matrix([sp.pi / 2, 0, 0])), ("L", sp.Matrix([sp.pi / 4] * 3))]:
    Hw = sp.simplify(W * H(k) * W.T / 8)
    off = [(i, j) for i in range(8) for j in range(8) if i // 2 != j // 2 and sp.simplify(Hw[i, j]) != 0]
    print(f"{name}: entries outside the four 2x2 blocks: {len(off)}")
    if name == "Gamma":
        ok &= not off
        blocks = [sp.simplify(Hw[2*b:2*b+2, 2*b:2*b+2]) for b in range(4)]
        print("  block {1, xyz} (A1, s-like):", blocks[0].tolist())
        print("  block {x, yz} (T2, p-like):", blocks[1].tolist())
        ok &= blocks[1] == blocks[2] == blocks[3]
        ok &= blocks[0] != blocks[1]
verdict("T13", ok, "at Gamma the cube's Walsh basis block-diagonalises the 64-entry cell Hamiltonian into A1 + 3 T2, "
        "each 2x2 block a TetA-TetB bond")
