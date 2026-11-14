"""S1. What the deep-field limit forces on any field-driven bond.
V3 = kappa (g - gs)/2, V2 = V2(g) > 0. TetA share mu = (1 + V3/sqrt(V2^2 + V3^2))/2.
Pass: (a) a constant V2 gives mu -> a nonzero constant as g -> 0; (b) mu -> g/a0 as g -> 0 needs
V2^2 ~ kappa^2 gs^2 g / a0; (c) mu = g/(g+a0) for all g iff gs = a0 and V2 = kappa sqrt(g a0)."""
import sympy as sp
g, a0, k, gs, V = sp.symbols("g a0 kappa g_s V", positive=True)
mu = lambda V3, V2: (1 + V3 / sp.sqrt(V2**2 + V3**2)) / 2
lim_const = sp.limit(mu(k * (g - gs) / 2, V), g, 0)
ok_a = sp.simplify(lim_const - (1 - k*gs/sp.sqrt(4*V**2 + k**2*gs**2)) / 2) == 0 and lim_const != 0
print("(a) constant V2: mu(g -> 0) =", sp.simplify(lim_const), "(nonzero: no deep field)")
# (b) small-g expansion with V2^2 = C g: mu ~ C g / (kappa^2 gs^2)
C = sp.symbols("C", positive=True)
lead = sp.limit(mu(k * (g - gs) / 2, sp.sqrt(C * g)) / g, g, 0)
ok_b = sp.simplify(lead - C / (k**2 * gs**2)) == 0
print("(b) V2^2 = C g: mu/g -> C/(kappa^2 gs^2); = 1/a0 iff C = kappa^2 gs^2/a0:", ok_b)
# (c) exactness: mu(V3, V2) = g/(g+a0) for all g  <=>  V3/V2 = (g - a0)/(2 sqrt(g a0))
expr = sp.simplify(mu(k * (g - a0) / 2, k * sp.sqrt(g * a0)) - g / (g + a0))
ok_c1 = expr == 0 or all(abs(sp.N(expr.subs({g: v, a0: 1, k: 2}))) < 1e-30 for v in (sp.Rational(1, 9), 1, 7, 300))
# uniqueness: mu fixes u = V3/V2 uniquely (mu is monotone in u), so V2 = V3 * 2 sqrt(g a0)/(g - a0);
# with V3 = kappa (g - gs)/2 this is kappa (g - gs) sqrt(g a0)/(g - a0), positive and finite at g = a0 only if gs = a0
V2_needed = k * (g - gs) / 2 * 2 * sp.sqrt(g * a0) / (g - a0)
ok_c2 = sp.limit(V2_needed.subs(gs, a0), g, a0) == k * a0 and sp.simplify(V2_needed.subs(gs, a0) - k * sp.sqrt(g * a0)) == 0
sign_flip = sp.simplify(V2_needed.subs({gs: 2 * a0, g: sp.Rational(3, 2) * a0, k: 1}))
ok_c3 = sign_flip < 0          # with gs != a0, the needed V2 turns negative between a0 and gs
print("(c) gs = a0 and V2 = kappa sqrt(g a0) give mu exactly:", ok_c1, "| forced:", ok_c2,
      "| gs != a0 would need V2 < 0 somewhere:", ok_c3, f"(e.g. {sign_flip})")
ok = ok_a and ok_b and ok_c1 and ok_c2 and ok_c3
print("\nS1", "PASS" if ok else "FAIL", "- a fixed coupling cannot give the deep field; the coupling must vanish as sqrt(g); "
      "exactness forces threshold a0 and coupling kappa sqrt(g a0)")
