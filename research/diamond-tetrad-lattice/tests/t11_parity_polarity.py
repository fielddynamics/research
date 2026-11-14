"""T11. Parity as polarity reversal across the crystal.
H(k; V3) = [[-V3, -t f(k)], [-t f*(k), V3]], f(k) = sum_a exp(i k.v_a).
Checks: Sigma H(k;V3) Sigma = -H(k;-V3) with Sigma = diag(1,-1); the bond-midpoint
inversion (k -> -k, sublattices swapped) maps H(k;V3) to H(k;-V3); at V3 = 0 the
spectrum is symmetric E <-> -E at every k. Pass: exact."""
import sympy as sp
from exact_common import verdict
kx, ky, kz = sp.symbols("kx ky kz", real=True)
V3, t = sp.symbols("V3 t", real=True)
legs = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
f = sum(sp.exp(sp.I * (kx * a + ky * b + kz * c)) for a, b, c in legs)
H = lambda v3, F: sp.Matrix([[-v3, -t * F], [-t * sp.conjugate(F), v3]])
S = sp.diag(1, -1); X = sp.Matrix([[0, 1], [1, 0]])
ok1 = sp.simplify(S * H(V3, f) * S + H(-V3, f)) == sp.zeros(2)
fm = f.subs({kx: -kx, ky: -ky, kz: -kz}, simultaneous=True)
ok2 = sp.simplify(sp.expand(X * H(V3, fm) * X - H(-V3, f), complex=True)) == sp.zeros(2)
ev = H(0, f).eigenvals()
ok3 = sp.simplify(sum(ev.keys())) == 0
print("chiral: Sigma H(V3) Sigma = -H(-V3):", ok1)
print("inversion (k -> -k, swap): H(V3) -> H(-V3):", ok2)
print("V3 = 0: eigenvalues sum to zero (E <-> -E):", ok3, list(ev.keys())[:1])
verdict("T11", ok1 and ok2 and ok3, "swapping the ends reverses the polarity everywhere in the crystal, not only on one bond")
