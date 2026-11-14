"""S3. The field's energy in bond terms.
Pass (exact): L = (g - a0)^2/2 + a0^2 ln(1 + g/a0) has L' = mu g; equals 2 V3^2 + a0^2 ln(gap/a0)
+ const with V3 = (g - a0)/2, gap = 2 sqrt(V2^2 + V3^2) = g + a0; equals 2 V3^2 + (a0^2/2) ln|det H_bond|
+ const; equals the AQUAL a0^2 F(y)/2 up to a constant; ln(1 + x) is ln Z with mu = d ln Z / d ln x."""
import sympy as sp
g, a0, x = sp.symbols("g a0 x", positive=True)
L = (g - a0)**2 / 2 + a0**2 * sp.log(1 + g / a0)
ok1 = sp.simplify(sp.diff(L, g) - g**2 / (g + a0)) == 0
V3 = (g - a0) / 2; V2 = sp.sqrt(g * a0)
gap = 2 * sp.sqrt(V2**2 + V3**2)
ok2 = sp.expand(gap**2 - (g + a0)**2) == 0      # both positive, so the squares decide
ok3 = sp.simplify(sp.diff(L - (2 * V3**2 + a0**2 * sp.log(gap / a0)), g)) == 0
Hb = sp.Matrix([[-V3, -V2], [-V2, V3]])
ok4 = sp.simplify(sp.diff(L - (2 * V3**2 + a0**2 / 2 * sp.log(-Hb.det())), g)) == 0
s = g / a0
F = s**2 - 2 * s + 2 * sp.log(1 + s)
ok5 = sp.simplify(sp.diff(L - a0**2 * F / 2, g)) == 0
Z = 1 + x
ok6 = sp.simplify(x * sp.diff(sp.log(Z), x) - x / (1 + x)) == 0
print("L' = mu g:", ok1, "| gap = g + a0:", ok2, "| L = 2 V3^2 + a0^2 ln(gap/a0) + const:", ok3)
print("L = 2 V3^2 + (a0^2/2) ln|det H_bond| + const:", ok4, "| L = a0^2 F(y)/2 + const (AQUAL):", ok5)
print("ln(1 + x) = ln Z, mu = d ln Z / d ln x:", ok6)
ok = all([ok1, ok2, ok3, ok4, ok5, ok6])
print("\nS3", "PASS" if ok else "FAIL", "- the field's energy is a polarity term plus the log of the bond gap "
      "(the bond's log-determinant), not the bond energy that T06 tried")
