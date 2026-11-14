"""T07. Two routes to mu: the bond (quantum amplitudes) and detailed balance.
Detailed balance (supplementary_equilibrium_route.tex): resolution x^n (1 - eps) = relaxation eps,
so the odds are eps/(1 - eps) = x^n, with n = 1 forced by the deep-field limit.
Bond: the odds are (u + sqrt(1 + u^2))^2 with u = V3/V2, i.e. ln(odds) = 2 asinh(u).
Pass: an explicit map exists under which both give the same mu(x) and the same exchange."""
import sympy as sp
from exact_common import verdict, same
x, t = sp.symbols("x t", positive=True)
u = (t**2 - 1) / (2 * t)                       # every real u, t > 0
odds_bond = sp.simplify((u + sp.sqrt(1 + u**2)) ** 2)
print("bond odds:", odds_bond)
# map: driving intensity x  <->  V3/V2 = (x - 1)/(2 sqrt x)
u_of_x = (x - 1) / (2 * sp.sqrt(x))
ok1 = same(odds_bond.subs(t, sp.sqrt(x)), x) and same(u.subs(t, sp.sqrt(x)), u_of_x)
eps = sp.symbols("eps", positive=True)
eps_db = sp.solve(sp.Eq(x * (1 - eps), eps), eps)[0]
ok2 = same(eps_db, x / (1 + x))
# Boltzmann form: odds = exp(dE/kT); bond: dE/kT = 2 asinh(V3/V2)
ok3 = all(abs(sp.N(sp.log(x) - 2 * sp.asinh(u_of_x)).subs(x, val)) < 1e-30 for val in [sp.Rational(1, 7), 1, 3, 50])
# exchange: x -> 1/x  <->  resolution and relaxation swap  <->  u -> -u
ok4 = same(u_of_x.subs(x, 1 / x), -u_of_x) and same(eps_db.subs(x, 1 / x), 1 - eps_db)
print("map u = (x-1)/(2 sqrt x) gives bond odds = x:", ok1)
print("detailed balance gives eps = x/(1+x):", ok2)
print("Boltzmann gap: ln x = 2 asinh(V3/V2):", ok3)
print("exchange x -> 1/x is u -> -u in the bond and eps -> 1 - eps in detailed balance:", ok4)
verdict("T07", ok1 and ok2 and ok3 and ok4, "the driving intensity x of detailed balance is the bond's odds; "
        "same mu, same exchange")
