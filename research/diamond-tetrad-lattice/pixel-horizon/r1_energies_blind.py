"""R1. Energies are blind to the root; phases are not. Pass: exact."""
import sys
sys.path.insert(0, "../pixel-lambda")
import sympy as sp
from common import pixel_H, LEGS
tA, tB, D, lam = sp.symbols("t_A t_B Delta lambda", positive=True)
kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
# isolated pixel: characteristic polynomial depends on tA, tB only through tA^2 + tB^2
cp = sp.expand(pixel_H(tA, tB, D).charpoly(lam).as_expr())
S = sp.symbols("S", positive=True)
cp_S = sp.expand(cp.subs(tA**2, S - tB**2))
ok1 = sp.simplify(sp.diff(cp_S, tB)) == 0
ok1b = sp.simplify(cp - pixel_H(tB, tA, D).charpoly(lam).as_expr()) == 0
print("isolated pixel: characteristic polynomial depends only on tA^2 + tB^2:", ok1, "| symmetric under exchange:", ok1b)
# tiling: F(k) and its exchange image
F = lambda a, b: a * sum(sp.exp(sp.I * (kx*v[0] + ky*v[1] + kz*v[2]) / 2) for v in LEGS) + \
                 b * sum(sp.exp(-sp.I * (kx*v[0] + ky*v[1] + kz*v[2]) / 2) for v in LEGS)
ok2 = sp.simplify(sp.expand(F(tB, tA) - sp.conjugate(F(tA, tB)), complex=True)) == 0
absF2 = lambda a, b: sp.expand(F(a, b) * sp.conjugate(F(a, b)), complex=True)
ok3 = sp.simplify(absF2(tA, tB) - absF2(tB, tA)) == 0
print("tiling: exchange sends F(k) to F(k)* (conjugates the Bloch phase):", ok2)
print("tiling: |F(k)|^2, hence both bands E(k) = (Delta -+ sqrt(Delta^2 + 4|F|^2))/2, unchanged by exchange:", ok3)
# the phase does change: at a generic k, arg F differs in sign
num = {kx: 0.7, ky: -0.4, kz: 1.1, tA: 1.3, tB: 0.6}
a1 = complex(F(tA, tB).subs(num)); a2 = complex(F(tB, tA).subs(num))
import cmath
ok4 = abs(cmath.phase(a1) + cmath.phase(a2)) < 1e-12 and abs(cmath.phase(a1)) > 1e-3
print(f"tiling: at a generic k the phase changes sign under exchange: arg F = {cmath.phase(a1):+.6f}, "
      f"after exchange {cmath.phase(a2):+.6f}:", ok4)
ok = ok1 and ok1b and ok2 and ok3 and ok4
print("\nR1", "PASS" if ok else "FAIL", "- no energy tells TetA from TetB; exchange conjugates the tiling's Bloch phase. "
      "Energies are root-blind, phases root-resolving, as metric and frame in the Gram-matrix proof")
