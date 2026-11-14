"""T14. The pixel's symmetry as cosets: Sym(stellated octahedron) = Sym(TetA) x {+-I}.
Pass: exact enumeration."""
import itertools
import numpy as np
from exact_common import verdict
R48 = []
for p in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3):
        Rm = np.zeros((3, 3), int)
        for i in range(3):
            Rm[i, p[i]] = s[i]
        R48.append(Rm)
TA = {(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)}; TB = {tuple(-c for c in v) for v in TA}
img = lambda Rm, S: {tuple(int(c) for c in Rm @ np.array(v)) for v in S}
stell = [Rm for Rm in R48 if img(Rm, TA | TB) == TA | TB]
td = [Rm for Rm in R48 if img(Rm, TA) == TA]
other = [Rm for Rm in stell if img(Rm, TA) != TA]
ok = len(stell) == 48 and len(td) == 24 and all(img(Rm, TA) == TB for Rm in other)
ok &= all(any((Rm == -T).all() for T in td) for Rm in other)
ok &= not any((T == -np.eye(3, dtype=int)).all() for T in td)
print(f"stellated octahedron: {len(stell)} symmetries; one tetrahedron: {len(td)}; index {len(stell)//len(td)}")
print("every other symmetry swaps TetA and TetB, and is -I times a tetrahedral one; -I is not tetrahedral")
verdict("T14", ok, "Sym(S) = Sym(TetA) x {+-I}: the tiling's TetA/TetB swap is the proofs' parity")
