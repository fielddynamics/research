"""T06. Bond energy against the AQUAL energy, under result 9's dictionary
V3 = (g - a0)/2, V2 = sqrt(g a0).
A field equation div[mu(|grad phi|/a0) grad phi] = 4 pi G rho comes from a Lagrangian
density L(g), g = |grad phi|, with L'(g) = mu(g/a0) g. Ask whether the bond energy E(g)
gives the same field equation: E'(g) = c * mu(g/a0) g for a constant c (terms that do not
change the field equation are constants and overall factors).
Pass: they agree. Expected outcome (stated in the plan): fail."""
import sympy as sp
from exact_common import verdict, same
g, a0, c = sp.symbols("g a0 c", positive=True)
E = -sp.sqrt(((g - a0) / 2) ** 2 + g * a0)
print("bond energy under the dictionary:", sp.simplify(E))
need = g**2 / (g + a0)                        # mu(g/a0) * g
dE = sp.simplify(sp.diff(E, g))
print("dE/dg =", dE, " ; needed (up to a constant factor): mu g =", need)
ratio = sp.simplify(dE / need)
print("ratio dE/dg / (mu g) =", ratio, " -> constant?", sp.simplify(sp.diff(ratio, g)) == 0)
# what the AQUAL energy is: integral of mu g dg = a0^2 F(y)/2 with y = (g/a0)^2
Laq = sp.integrate(need, g)
s = sp.symbols("s", positive=True)
F = s**2 - 2 * s + 2 * sp.log(1 + s)
print("integral of mu g dg =", sp.simplify(Laq), " ; equals a0^2 F(g/a0)/2 up to a constant:", same(sp.diff(Laq - a0**2 * F.subs(s, g / a0) / 2, g), 0))
ok = sp.simplify(sp.diff(ratio, g)) == 0
verdict("T06", ok, "as expected, the dictionary fixes the shares but not the energy: E is linear in g, "
        "the AQUAL energy is not" if not ok else "")
