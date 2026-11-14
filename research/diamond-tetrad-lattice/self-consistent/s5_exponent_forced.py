"""S5. Is the remaining assumption free? tA^2 ~ g^n, tB^2 fixed: mu = x^n/(1 + x^n).
Deep field mu g = g_N with mu ~ x^n gives g^(n+1) ~ g_N a0^n, so g ~ g_N^(1/(n+1)).
Flat rotation with v^4 ~ G M a0 needs g ~ g_N^(1/2): only n = 1.
Pass (exact): exponents 2/3, 1/2, 1/3 for n = 1/2, 1, 2, and v^4 = G M a0 only for n = 1."""
import sympy as sp
gN, a0, G, M, r = sp.symbols("g_N a0 G M r", positive=True)
res = {}
for n in (sp.Rational(1, 2), 1, 2):
    gsym = sp.symbols("g", positive=True)
    sol = sp.solve(sp.Eq((gsym / a0)**n * gsym, gN), gsym)[0]       # deep field: mu ~ x^n
    expo = sp.simplify(sp.diff(sp.log(sol), gN) * gN)
    v2 = sp.simplify(sol.subs(gN, G * M / r**2) * r)                 # v^2 = g r
    flat = sp.simplify(sp.diff(v2, r)) == 0
    res[n] = (expo, flat, sp.simplify(v2**2) if flat else None)
    print(f"n = {n}: g ~ g_N^{expo}; flat rotation: {flat}" + (f"; v^4 = {sp.simplify(v2**2)}" if flat else ""))
ok = res[sp.Rational(1, 2)][0] == sp.Rational(2, 3) and res[1][0] == sp.Rational(1, 2) and res[2][0] == sp.Rational(1, 3) \
    and res[1][1] and not res[2][1] and not res[sp.Rational(1, 2)][1] and sp.simplify(res[1][2] - G * M * a0) == 0
print("\nS5", "PASS" if ok else "FAIL", "- only tA^2 ~ g (n = 1) gives flat rotation curves with v^4 = G M a0; "
      "the remaining exponent is fixed by baryonic Tully-Fisher, as in the detailed-balance route")
