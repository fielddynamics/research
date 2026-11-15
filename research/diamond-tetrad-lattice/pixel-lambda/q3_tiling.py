"""Q3. Joined pixels: the cubic tiling with shared corners.
Simple-cubic lattice (side 1): Field Origin at the cell centre, one corner site per cell.
Each centre couples to its 8 corners: tA along its TetA legs v/2, tB along its TetB legs -v/2.
H(k) = [[Delta, -F], [-F*, 0]], F(k) = tA sum_TetA e^{i k.v/2} + tB sum_TetB e^{-i k.v/2}.
Pass: exact TetA leg-energy share tA/(tA + tB) at k = 0; numerically k = 0 is the global minimum
over a 40^3 zone grid for several tA/tB and Delta."""
import numpy as np
import sympy as sp
from common import LEGS
tA, tB, D = sp.symbols("t_A t_B Delta", positive=True)
F0 = 4 * tA + 4 * tB
E0 = (D - sp.sqrt(D**2 + 4 * F0**2)) / 2
o, cA = -E0, F0                                  # eigenvector (o, c) of [[D, -F0], [-F0, 0]]
Hk0 = sp.Matrix([[D, -F0], [-F0, 0]])
ok1 = sp.simplify(Hk0 * sp.Matrix([o, cA]) - E0 * sp.Matrix([o, cA])) == sp.zeros(2, 1)
eA = 4 * (-tA) * 2 * o * cA; eB = 4 * (-tB) * 2 * o * cA
share = sp.simplify(eA / (eA + eB))
ok2 = sp.simplify(share - tA / (tA + tB)) == 0
print("k = 0 ground state; TetA leg-energy share =", share, ":", ok1 and ok2)
L = np.array(LEGS, float)
m = 40
s = 2 * np.pi * (np.arange(m) / m)
K = np.array(np.meshgrid(s, s, s, indexing="ij")).reshape(3, -1).T      # SC zone, side 1
ok3 = True
for ta, tb, dl in [(1.0, 0.3, 0.5), (0.2, 1.0, 2.0), (1.0, 1.0, 0.1), (5.0, 0.1, 10.0)]:
    Fk = ta * np.exp(1j * K @ L.T / 2).sum(1) + tb * np.exp(-1j * K @ L.T / 2).sum(1)
    Ek = (dl - np.sqrt(dl**2 + 4 * np.abs(Fk)**2)) / 2
    i = np.argmin(Ek)
    at_gamma = np.allclose(np.mod(K[i] + 1e-9, 2 * np.pi), 1e-9, atol=1e-6)
    gap = np.sort(Ek)[1] - Ek[i] if at_gamma else 0
    print(f"  tA={ta}, tB={tb}, Delta={dl}: minimum at k = {np.round(K[i], 3)}, Gamma: {at_gamma}")
    ok3 &= at_gamma
ok = ok1 and ok2 and ok3
print("\nQ3", "PASS" if ok else "FAIL", "- in the tiling the ground state is at k = 0 and its TetA share is tA/(tA + tB), "
      "linear in the couplings")
