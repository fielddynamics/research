"""Q4. Which coupling law goes with which picture. Shares: isolated pixel tA^2/(tA^2+tB^2) (Q1),
tiling tA/(tA+tB) (Q3). Laws: amplitude ~ field (tA:tB = g:a0) or squared ~ field (tA^2:tB^2 = g:a0).
Deep-field exponent from mu ~ x^n: g ~ g_N^(1/(n+1)); Tully-Fisher needs n = 1 (S5).
Pass: exact; each law gives mu in exactly one picture."""
import sympy as sp
g, a0, x = sp.symbols("g a0 x", positive=True)
iso = lambda ta, tb: ta**2 / (ta**2 + tb**2)
til = lambda ta, tb: ta / (ta + tb)
laws = {"amplitude ~ field": (g, a0), "squared ~ field": (sp.sqrt(g), sp.sqrt(a0))}
mu = g / (g + a0)
rows = {}
for law, (ta, tb) in laws.items():
    for pic, f in (("isolated pixel", iso), ("tiling", til)):
        sh = sp.simplify(f(ta, tb).subs(g, x * a0))
        n = sp.limit(sp.log(sh) / sp.log(x), x, 0)
        is_mu = sp.simplify(sh - x / (1 + x)) == 0
        rows[(law, pic)] = (is_mu, n)
        print(f"{law:18s} | {pic:14s}: share = {sh}; deep-field mu ~ x^{n}; = mu: {is_mu}; "
              f"g ~ g_N^{sp.Rational(1, 1) / (n + 1)}; Tully-Fisher: {n == 1}")
ok = rows[("amplitude ~ field", "tiling")][0] and rows[("squared ~ field", "isolated pixel")][0] \
    and not rows[("amplitude ~ field", "isolated pixel")][0] and not rows[("squared ~ field", "tiling")][0] \
    and rows[("amplitude ~ field", "isolated pixel")][1] == 2 and rows[("squared ~ field", "tiling")][1] == sp.Rational(1, 2)
print("\nQ4", "PASS" if ok else "FAIL", "- each coupling law gives mu in exactly one picture: in the cubic tiling with "
      "shared corners, mu needs the coupling amplitude proportional to the field")
