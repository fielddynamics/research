"""R2. Where the asymmetry appears in the tiling's waves.
F(k) = (tA + tB)(4 - k^2/2 + O(k^4)) - (i/2)(tA - tB) kx ky kz + O(k^5);
arg F = -(sigma/8) kx ky kz + O(k^5), sigma = (tA - tB)/(tA + tB). Pass: exact series."""
import sys
sys.path.insert(0, "../pixel-lambda")
import sympy as sp
from common import LEGS
tA, tB, e, g, a0, x = sp.symbols("t_A t_B epsilon g a0 x", positive=True)
kx, ky, kz = sp.symbols("k_x k_y k_z", real=True)
F = tA * sum(sp.exp(sp.I * e * (kx*v[0] + ky*v[1] + kz*v[2]) / 2) for v in LEGS) + \
    tB * sum(sp.exp(-sp.I * e * (kx*v[0] + ky*v[1] + kz*v[2]) / 2) for v in LEGS)
ser = sp.expand(sp.series(F, e, 0, 5).removeO())
even = sp.expand(sum(ser.coeff(e, n) * e**n for n in (0, 2, 4)))
odd = sp.expand(sum(ser.coeff(e, n) * e**n for n in (1, 3)))
k2 = kx**2 + ky**2 + kz**2
ok1 = sp.simplify(ser.coeff(e, 0) - 4 * (tA + tB)) == 0 and sp.simplify(ser.coeff(e, 2) + (tA + tB) * k2 / 2) == 0
ok2 = ser.coeff(e, 1) == 0 and sp.simplify(ser.coeff(e, 3) + sp.I * (tA - tB) * kx * ky * kz / 2) == 0
c4 = sp.factor(ser.coeff(e, 4))
ok2b = sp.simplify(sp.im(sp.expand(c4, complex=True))) == 0          # the O(k^4) term is even (real)
print("even part: 4(tA + tB) - (tA + tB) k^2/2 + O(k^4):", ok1, "| O(k^4) coefficient", c4)
print("odd part: only -(i/2)(tA - tB) kx ky kz at third order (nothing at first):", ok2, "| O(k^4) real:", ok2b)
argF = sp.series(sp.atan(sp.im(sp.expand(ser, complex=True)) / sp.re(sp.expand(ser, complex=True))), e, 0, 5).removeO()
sigma = (tA - tB) / (tA + tB)
ok3 = sp.simplify(argF.coeff(e, 3) + sigma * kx * ky * kz / 8) == 0 and argF.coeff(e, 1) == 0 and \
      sp.simplify(argF.coeff(e, 2)) == 0 and sp.simplify(argF.coeff(e, 4)) == 0
print("arg F = -(sigma/8) kx ky kz + O(k^5):", ok3)
sig_x = sp.simplify(sigma.subs({tA: g, tB: a0}).subs(g, x * a0))
ok4 = sp.simplify(sig_x - (x - 1) / (x + 1)) == 0 and sp.simplify(sig_x.subs(x, 1)) == 0 and \
      sp.simplify(sig_x.subs(x, 1 / x) + sig_x) == 0
print("with the tiling law tA : tB = g : a0, sigma = 2 mu - 1 = (x - 1)/(x + 1):", ok4,
      "| zero at the ring, opposite signs inside and outside, odd under exchange x -> 1/x")
ok5 = sp.simplify((kx*ky*kz).subs({kx: -kx, ky: -ky, kz: -kz}, simultaneous=True) + kx*ky*kz) == 0
print("the phase's k-dependence kx ky kz is odd under parity k -> -k:", ok5)
ok = ok1 and ok2 and ok2b and ok3 and ok4 and ok5
print("\nR2", "PASS" if ok else "FAIL", "- the TetA/TetB asymmetry enters the tiling's waves only through the parity "
      "character kx ky kz, with strength 2 mu - 1, vanishing at the ring and reversing across it")
