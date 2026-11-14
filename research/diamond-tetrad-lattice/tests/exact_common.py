"""Small helpers shared by the exact tests."""
import sympy as sp


def verdict(name, ok, note=""):
    print(f"\n{name} {'PASS' if ok else 'FAIL'}" + (f" - {note}" if note else ""))
    return ok


def same(a, b):
    """Exact equality, falling back to numerical checks at random points when simplify is stuck."""
    d = sp.simplify(a - b)
    if d == 0:
        return True
    syms = sorted(d.free_symbols, key=str)
    import random
    random.seed(0)
    for _ in range(8):
        sub = {s: sp.Rational(random.randint(1, 97), random.randint(1, 13)) for s in syms}
        if abs(sp.N(d.subs(sub), 40)) > 1e-30:
            return False
    return True
