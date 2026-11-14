"""T09 diagnostic: does the crystal keep the exchange symmetry share(1/x) = 1 - share(x),
and how does the deviation scale with V1? (Not a re-run of the criterion.)"""
import numpy as np
from bz import LEGS, kgrid
K = kgrid(16); ph = np.exp(1j * K @ LEGS.T)
def share(x, v1, V2=1.0):
    V3 = (x - 1) / (2 * np.sqrt(x)) * V2
    H = np.zeros((len(K), 8, 8), complex)
    for a in range(4):
        for b in range(4):
            if a != b: H[:, a, b] = -v1; H[:, 4+a, 4+b] = -v1
        H[:, a, a] = -V3; H[:, 4+a, 4+a] = V3
        H[:, a, 4+a] = -V2 * ph[:, a]; H[:, 4+a, a] = -V2 * np.conj(ph[:, a])
    U = np.linalg.eigh(H)[1][:, :, :4]
    return np.mean(np.sum(np.abs(U[:, :4, :])**2, axis=(1, 2))) / 4
for x in (0.1, 0.316, 3.16, 10):
    s, sinv = share(x, 0.25), share(1/x, 0.25)
    print(f"x={x:6.3g}: share(x) + share(1/x) - 1 = {s + sinv - 1:+.2e}")
x = 0.316; mu = x/(1+x)
d = [(v1, share(x, v1) - mu) for v1 in (0.025, 0.05, 0.1)]
print("absolute deviation at x=0.316 vs V1:", ", ".join(f"V1={v:.3f}: {e:.2e}" for v, e in d),
      f"| ratio for doubling V1: {d[1][1]/d[0][1]:.2f}, {d[2][1]/d[1][1]:.2f} (4 = quadratic)")
