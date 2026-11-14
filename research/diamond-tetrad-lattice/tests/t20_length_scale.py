"""T20. Which energies would give x = g/a0? Exploratory.
Result 9 fixes only the ratio V3/V2 = (x - 1)/(2 sqrt x). With the bond-orbital scaling
V2 = eta hbar^2/(m d^2) (Harrison's 1999 universal parameters, Elementary Electronic Structure, give eta = 3.22 for the sp3 bond) and V2 = kappa sqrt(g a0),
the bond length is d = sqrt(eta hbar^2/(m kappa sqrt(g a0))), so d ~ (g a0)^(-1/4) exactly.
A number needs kappa (energy per unit acceleration), which the framework does not supply.
The plan names the classical electron radius r_e as the reference; take kappa = m_e r_e
(energy = m_e x acceleration x r_e) and m = m_e, and report d at the ring g = a0.
Pass (reported, not judged)."""
import sympy as sp
g, a0, eta, hbar, m, kappa = sp.symbols("g a0 eta hbar m kappa", positive=True)
d = sp.sqrt(eta * hbar**2 / (m * kappa * sp.sqrt(g * a0)))
print("d(g) =", d, "; d log d / d log g =", sp.simplify(sp.diff(sp.log(d), g) * g))
hb, me, c, alpha, re, A0 = 1.054571817e-34, 9.1093837015e-31, 2.99792458e8, 7.2973525693e-3, 2.8179403262e-15, 1.2e-10
etaH = 3.22
dval = (etaH * hb**2 / (me * me * re * A0)) ** 0.5
aB = hb / (me * c * alpha)
print(f"with kappa = m_e r_e, m = m_e, a0 = 1.2e-10 m/s^2: d(g = a0) = {dval:.3e} m")
print(f"identity: d(a0) = sqrt(eta * a_Bohr * c^2/a0) = sqrt({etaH} * {aB:.3e} m * {c**2/A0:.3e} m) = "
      f"{(etaH * aB * c**2 / A0) ** 0.5:.3e} m  (the geometric mean of the Bohr radius and the length c^2/a0)")
print("\nT20 PASS (reported) - d ~ (g a0)^(-1/4) is exact; the number depends entirely on the choice of kappa, "
      "which the framework does not yet fix. No match is claimed.")
