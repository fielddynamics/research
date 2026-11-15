"""Q2. The dark states in the cube's Walsh basis. Pass: exact."""
import itertools
import sympy as sp
from common import pixel_H, VERTS
tA, tB, D = sp.symbols("t_A t_B Delta", positive=True)
H = pixel_H(tA, tB, D)
names = {(): "1", (0,): "x", (1,): "y", (2,): "z", (0, 1): "xy", (1, 2): "yz", (0, 2): "xz", (0, 1, 2): "xyz"}
walsh = {names[S]: sp.Matrix([0] + [sp.prod([v[i] for i in S]) for v in VERTS]) for S in names}
coupled = {k: sp.simplify((H * w)[0]) for k, w in walsh.items()}
print("Field Origin coupling of each Walsh function:", coupled)
six = ["x", "y", "z", "xy", "yz", "xz"]
ok1 = all(coupled[k] == 0 for k in six) and coupled["1"] != 0 and coupled["xyz"] != 0
ok2 = all(H * walsh[k] == sp.zeros(9, 1) for k in six)          # exact dark states for any tA, tB
# seventh dark state: tB*(TetA part) - tA*(TetB part) = combination of 1 and xyz
d7 = sp.Matrix([0] + [tB] * 4 + [-tA] * 4)
ok3 = H * d7 == sp.zeros(9, 1)
alpha, beta = sp.symbols("alpha beta")
sol = sp.solve(list(d7 - alpha * walsh["1"] - beta * walsh["xyz"]), [alpha, beta], dict=True)
ok4 = bool(sol) and sp.simplify(sol[0][alpha] - (tB - tA) / 2) == 0 and sp.simplify(sol[0][beta] - (tB + tA) / 2) == 0
# at the ring tA = tB: bright corner part ~ 1, dark ~ xyz
vb_ring = sp.Matrix([0] + [tA] * 4 + [tA] * 4)
ok5 = sp.simplify(vb_ring - tA * walsh["1"]) == sp.zeros(9, 1) and sp.simplify(d7.subs(tB, tA) - tA * walsh["xyz"]) == sp.zeros(9, 1)
print("six Walsh functions x, y, z, xy, yz, xz are dark for any tA, tB:", ok1 and ok2)
print("seventh dark state is ((tB - tA)/2) 1 + ((tB + tA)/2) xyz:", ok3 and ok4)
print("at the ring tA = tB the bright state is 1 and the seventh dark state is xyz, the parity character:", ok5)
ok = ok1 and ok2 and ok3 and ok4 and ok5
print("\nQ2", "PASS" if ok else "FAIL", "- the Field Origin couples only through the Walsh pair {1, xyz}; six dark states by "
      "symmetry, the seventh is the parity character at the ring")
