"""T05. Hellmann-Feynman responses: dE/dV3 = -alpha_p, dE/dV2 = -alpha_c, so mu = (1 - dE/dV3)/2.
Pass: exact identities."""
import sympy as sp
from exact_common import verdict, same
V2, V3 = sp.symbols("V2 V3", positive=True)
E = -sp.sqrt(V2**2 + V3**2)
ap, ac = V3 / sp.sqrt(V2**2 + V3**2), V2 / sp.sqrt(V2**2 + V3**2)
ok1 = same(sp.diff(E, V3), -ap); ok2 = same(sp.diff(E, V2), -ac)
# the share on the lower (TetA, at -V3) end
H = sp.Matrix([[-V3, -V2], [-V2, V3]])
vals, vecs = zip(*[(ev, vs[0]) for ev, m, vs in H.eigenvects()])
v = vecs[[same(e, E) for e in vals].index(True)]
mu = sp.simplify(v[0]**2 / (v.T * v)[0])
ok3 = same(mu, (1 - sp.diff(E, V3)) / 2)
print("dE/dV3 = -alpha_p:", ok1, "| dE/dV2 = -alpha_c:", ok2, "| mu = (1 - dE/dV3)/2:", ok3)
verdict("T05", ok1 and ok2 and ok3, "polarity and covalency are the bond energy's responses; mu is a derivative of E")
