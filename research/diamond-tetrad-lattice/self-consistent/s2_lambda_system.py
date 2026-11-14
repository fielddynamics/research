"""S2. One mechanism for both requirements: the Lambda system.
Basis (TetA end, TetB end, Field Origin). H = [[0, 0, -tA], [0, 0, -tB], [-tA, -tB, Delta]].
Pass (exact, any Delta): bright state's TetA:TetB odds = tA^2 : tB^2; dark state decoupled at E = 0
with the exchanged shares; with tA^2 = c g, tB^2 = c a0 the share is mu(g/a0); eliminating the
Field Origin at large Delta gives polar energy (g - a0)/2 and coupling sqrt(g a0) (times c/Delta)."""
import sympy as sp
tA, tB, D, c, g, a0 = sp.symbols("t_A t_B Delta c g a0", positive=True)
H = sp.Matrix([[0, 0, -tA], [0, 0, -tB], [-tA, -tB, D]])
T2 = tA**2 + tB**2
Eb = (D - sp.sqrt(D**2 + 4 * T2)) / 2
vb = sp.Matrix([tA, tB, -Eb])
ok1 = sp.simplify(H * vb - Eb * vb) == sp.zeros(3, 1)
evals = sorted(H.eigenvals().keys(), key=lambda e: sp.N(e.subs({tA: 1, tB: 1, D: 1})))
ok1b = sp.simplify(evals[0] - Eb) == 0          # it is the lowest
shareA = sp.simplify(vb[0]**2 / (vb[0]**2 + vb[1]**2))
ok1c = sp.simplify(shareA - tA**2 / T2) == 0
vd = sp.Matrix([tB, -tA, 0])
ok2 = H * vd == sp.zeros(3, 1)
dark_share = sp.simplify(vd[0]**2 / (vd[0]**2 + vd[1]**2))
ok2b = sp.simplify(dark_share - tB**2 / T2) == 0 and sp.simplify(dark_share + shareA - 1) == 0
sub = {tA: sp.sqrt(c * g), tB: sp.sqrt(c * a0)}
ok3 = sp.simplify(shareA.subs(sub) - g / (g + a0)) == 0
x = sp.symbols("x", positive=True)
ok3b = sp.simplify(dark_share.subs(sub).subs(g, x * a0) - (1 / x) / (1 + 1 / x)) == 0   # dark = exchange image
# second-order elimination: H_eff = -|t><t| / Delta
Heff = -sp.Matrix([tA, tB]) * sp.Matrix([[tA, tB]]) / D
Heff_s = sp.simplify(Heff.subs(sub))
shift = sp.simplify((Heff_s[0, 0] + Heff_s[1, 1]) / 2)
polar = sp.simplify((Heff_s[1, 1] - Heff_s[0, 0]) / 2)     # TetB minus TetA, halved: result 9's V3 convention
coupling = sp.simplify(-Heff_s[0, 1])
ok4 = sp.simplify(polar - c / D * (g - a0) / 2) == 0 and sp.simplify(coupling - c / D * sp.sqrt(g * a0)) == 0
print("bright state is the lowest eigenvector, odds tA^2 : tB^2:", ok1 and ok1b and ok1c)
print("dark state (tB, -tA, 0) at E = 0, decoupled, shares exchanged:", ok2 and ok2b)
print("tA^2 = c g, tB^2 = c a0: bright share = g/(g + a0) for every Delta:", ok3, "| dark share = mu(1/x):", ok3b)
print("eliminating the Field Origin: polar energy (c/Delta)(g - a0)/2, coupling (c/Delta) sqrt(g a0):", ok4)
print("bright energy", sp.simplify(Eb.subs(sub)), "-> -(c/Delta)(g + a0) at large Delta")
ok = ok1 and ok1b and ok1c and ok2 and ok2b and ok3 and ok3b and ok4
print("\nS2", "PASS" if ok else "FAIL", "- one assumption, tA^2 : tB^2 = g : a0, gives both of result 9's requirements; "
      "the share is exact for every Delta; exchange is bright <-> dark")
