"""T08. The TetB field as covalency: (1 - mu) g = (1/2) alpha_c sqrt(g a0),
with (1 - mu) g ~ g for g << a0 and -> a0 for g >> a0. Pass: exact."""
import sympy as sp
from exact_common import verdict, same
g, a0 = sp.symbols("g a0", positive=True)
mu = g / (g + a0); ac = 2 * sp.sqrt(g * a0) / (g + a0)
ok1 = same((1 - mu) * g, ac / 2 * sp.sqrt(g * a0))
ok2 = sp.limit((1 - mu) * g / g, g, 0) == 1 and sp.limit((1 - mu) * g, g, sp.oo) == a0
print("identity:", ok1, "| limits (ratio to g -> 1 as g -> 0; -> a0 as g -> oo):", ok2)
verdict("T08", ok1 and ok2, "the TetB part of the field is half the covalency times the covalent scale sqrt(g a0)")
