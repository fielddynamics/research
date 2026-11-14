"""T10. Share by Bloch mode, in the two-sublattice s-band model
H(k) = [[-V3, -t f(k)], [-t f*(k), V3]], f(k) = sum_a exp(i k.v_a).
Lower band share on TetA: mu_k = (1 + V3/sqrt(V3^2 + t^2 |f|^2))/2, i.e. x_k = (u_k + sqrt(1+u_k^2))^2
with u_k = V3/(t |f(k)|). Report the BZ-mean share and its spread; check exactly f(0) = K = 4
and the band edge +-sqrt(V3^2 + 16 t^2). Pass: reported (the exact checks must hold)."""
import numpy as np
import sympy as sp
from bz import LEGS, kgrid
kx, ky, kz = sp.symbols("kx ky kz", real=True); V3s, ts = sp.symbols("V3 t", positive=True)
f = sum(sp.exp(sp.I * (kx*a + ky*b + kz*c)) for a, b, c in LEGS.astype(int))
f0 = f.subs({kx: 0, ky: 0, kz: 0})
H0 = sp.Matrix([[-V3s, -ts*f0], [-ts*f0, V3s]])
ok = f0 == 4 and set(H0.eigenvals()) == {sp.sqrt(V3s**2 + 16*ts**2), -sp.sqrt(V3s**2 + 16*ts**2)}
print("f(0) = 4 = K:", f0 == 4, "| band edge at Gamma = +-sqrt(V3^2 + 16 t^2):", ok)
K = kgrid(24); F = np.abs(np.exp(1j * K @ LEGS.T).sum(1))
print("|f| over the zone: min", F.min().round(4), "max", F.max().round(4), "(zero on the X-W nodal lines)")
print("\n x(Gamma)   mu(x_Gamma)   BZ-mean share   spread (10%-90%)   geometric-mean x_k")
for xg in [0.01, 0.1, 0.5, 1, 2, 10, 100]:
    u_g = (xg - 1) / (2 * np.sqrt(xg)); V3 = u_g * 4.0           # t = 1, u at Gamma = V3/(4t)
    muk = 0.5 * (1 + V3 / np.sqrt(V3**2 + F**2))
    q10, q90 = np.quantile(muk, [0.1, 0.9])
    uk = V3 / np.maximum(F, 1e-12); xk = (uk + np.sqrt(1 + uk**2))**2
    print(f" {xg:7.3g}   {xg/(1+xg):.4f}        {muk.mean():.4f}          {q10:.3f}-{q90:.3f}         {np.exp(np.mean(np.log(xk))):.4g}")
print("\nT10", "PASS" if ok else "FAIL", "- exact checks hold; shares reported. A lattice spreads one bond's x into a range, "
      "pulled toward the ends where |f| is small")
