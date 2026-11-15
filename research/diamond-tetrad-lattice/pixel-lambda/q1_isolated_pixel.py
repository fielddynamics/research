"""Q1. The isolated pixel is a Lambda system. Pass: exact."""
import sympy as sp
from common import pixel_H, leg_energy_share
tA, tB, D, c, g, a0 = sp.symbols("t_A t_B Delta c g a0", positive=True)
H = pixel_H(tA, tB, D)
T2 = 4 * (tA**2 + tB**2)
Eb = (D - sp.sqrt(D**2 + 4 * T2)) / 2
vb = sp.Matrix([-Eb] + [tA] * 4 + [tB] * 4)
ok1 = sp.simplify(H * vb - Eb * vb) == sp.zeros(9, 1)
ok2 = H.rank() == 2                                  # so 7 eigenvalues are 0: the dark states
cp = sp.factor(H.charpoly().as_expr())
lam = sp.symbols("lambda")
ok3 = sp.simplify(cp.as_expr().subs(lam, 0)) == 0 if hasattr(cp, "as_expr") else False
num = {tA: sp.Rational(3, 2), tB: sp.Rational(2, 3), D: sp.Rational(5, 7)}
ev = sorted(float(sp.re(sp.N(e))) for e in H.subs(num).eigenvals(multiple=True))
ok4 = abs(ev[0] - float(Eb.subs(num))) < 1e-12 and sum(abs(e) < 1e-12 for e in ev) == 7
wA = sp.simplify(sum(vb[i]**2 for i in range(1, 5)) / sum(vb[i]**2 for i in range(1, 9)))
eA = leg_energy_share(vb, tA, tB)
ok5 = sp.simplify(wA - tA**2 / (tA**2 + tB**2)) == 0 and sp.simplify(eA - tA**2 / (tA**2 + tB**2)) == 0
sub = {tA: sp.sqrt(c * g), tB: sp.sqrt(c * a0)}
ok6 = sp.simplify(wA.subs(sub) - g / (g + a0)) == 0
print("bright state is an eigenvector with E = (Delta - sqrt(Delta^2 + 16(tA^2 + tB^2)))/2:", ok1)
print("rank H = 2, so 7 dark states at E = 0:", ok2, "| numerically: lowest = bright, seven zeros:", ok4)
print("TetA share of the bright state, by weight and by leg energy, = tA^2/(tA^2 + tB^2):", ok5)
print("with tA^2 : tB^2 = g : a0 the share is mu(g/a0) for every Delta:", ok6)
ok = ok1 and ok2 and ok4 and ok5 and ok6
print("\nQ1", "PASS" if ok else "FAIL", "- the pixel is a Lambda system: one bright state with TetA share tA^2/(tA^2+tB^2), "
      "seven dark states")
