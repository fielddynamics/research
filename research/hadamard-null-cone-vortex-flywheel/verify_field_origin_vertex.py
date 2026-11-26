"""Exact checks for the candidate Field Origin vertex (FIELD_ORIGIN_VERTEX.md).

Each chamber's collective amplitude is a complex vector q_A, q_B (here in C^2,
enough to be general for these identities). With H = H_O(q_A, q_B) and the
standard complex Hamilton equations i dq/dt = dH/d(conj q), we compute
dN_A/dt and dN_B/dt exactly for each candidate coupling, where N = |q|^2.

Checks:
  1. lambda|chi|^2        : N_A and N_B each conserved (resonance only).
  2. kappa Re(e^{i th} chi^2): only N_A + N_B conserved; dN_A/dt is a fixed
                             multiple of kappa Im(e^{i th} chi^2) (4 in this
                             script's real-coordinate time convention).
  3. k Re(chi)            : the linear term is a bilinear bond between the
                             chambers' amplitudes (the Stage VII form) and
                             also transfers occupation.
  4. Locked phase         : the chi^2 transfer stops exactly when
                             Im(e^{i th} chi^2) = 0.
"""
import sympy as sp

n = 2
xa = sp.symbols(f"xa0:{n}", real=True); ya = sp.symbols(f"ya0:{n}", real=True)
xb = sp.symbols(f"xb0:{n}", real=True); yb = sp.symbols(f"yb0:{n}", real=True)
lam, kap, k, th = sp.symbols("lambda kappa k theta", real=True)
qA = [xa[i] + sp.I * ya[i] for i in range(n)]
qB = [xb[i] + sp.I * yb[i] for i in range(n)]
chi = sum(sp.conjugate(qA[i]) * qB[i] for i in range(n))
NA = sum(xa[i]**2 + ya[i]**2 for i in range(n))
NB = sum(xb[i]**2 + yb[i]**2 for i in range(n))

def rates(H):
    """dN/dt from Hamilton's equations in real coordinates q = (x + i y)/sqrt2
    convention-free form: dx/dt = dH/dy, dy/dt = -dH/dx (up to a common
    positive factor, irrelevant for the signs and zero tests here)."""
    H = sp.expand(sp.re(sp.expand(H, complex=True)))
    def dN(xs, ys):
        return sp.simplify(sum(2*xs[i]*sp.diff(H, ys[i]) - 2*ys[i]*sp.diff(H, xs[i]) for i in range(n)))
    return dN(xa, ya), dN(xb, yb)

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

# 1. resonance term
dA, dB = rates(lam * chi * sp.conjugate(chi))
check("lambda|chi|^2 conserves N_A", sp.simplify(dA) == 0)
check("lambda|chi|^2 conserves N_B", sp.simplify(dB) == 0)

# 2. nonlinear transfer term
Ht = kap * sp.re(sp.expand(sp.exp(sp.I*th) * chi**2, complex=True))
dA, dB = rates(Ht)
check("kappa Re(e^{i th} chi^2) conserves N_A + N_B", sp.simplify(dA + dB) == 0)
check("kappa Re(e^{i th} chi^2) transfers occupation (dN_A/dt not identically 0)", sp.simplify(dA) != 0)
im_part = sp.im(sp.expand(sp.exp(sp.I*th) * chi**2, complex=True))
ratio = sp.simplify(dA / (kap * im_part))
check("transfer rate is a constant multiple of kappa Im(e^{i th} chi^2)", ratio.is_constant())
print("   dN_A/dt = (", ratio, ") * kappa * Im(e^{i th} chi^2)")

# 3. linear term = bilinear cross-chamber bond, and it also transfers
Hl = k * sp.re(sp.expand(chi, complex=True))
bond = k * sum(xa[i]*xb[i] + ya[i]*yb[i] for i in range(n))
check("k Re(chi) is the bilinear bond k * sum Re(conj(qA_i) qB_i)", sp.simplify(sp.expand(Hl) - bond) == 0)
dA, dB = rates(Hl)
check("linear bond transfers occupation and conserves the total", sp.simplify(dA) != 0 and sp.simplify(dA + dB) == 0)

# 4. phase locking stops transfer: rate vanishes on Im(e^{i th} chi^2) = 0
check("chi^2 transfer stops exactly when Im(e^{i th} chi^2) = 0", ratio.is_constant() and ratio != 0)

passed = sum(ok for _, ok in results)
print(f"{passed}/{len(results)} exact checks passed.")
