"""T09. The single bond against the full sp3 crystal.
Harrison's 8-band sp3 model on diamond, in the hybrid basis: -V2 exp(i k.v_a) between A_a
and B_a, -V1 between hybrids on one atom, -V3 on A and +V3 on B. Occupied: the 4 lowest
bands (8 electrons per cell). TetA weight per electron = BZ average of the A-hybrid weight
of the occupied bands / 4. Compare with the single-bond mu(x), x = (u + sqrt(1+u^2))^2, u = V3/V2.
Pass: within 2% (relative) of mu(x) for V1/V2 <= 0.25, across 1e-2 <= x <= 1e2."""
import numpy as np
from bz import LEGS, kgrid

V2 = 1.0
K = kgrid(16)
ph = np.exp(1j * K @ LEGS.T)                 # (nk, 4)
xs = np.logspace(-2, 2, 9)
v1s = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
print("rows V1/V2, columns x; entries (share - mu)/mu")
print("V1/V2  " + " ".join(f"{x:8.3g}" for x in xs))
worst_cov = 0.0
for v1 in v1s:
    row = []
    for x in xs:
        u = (x - 1) / (2 * np.sqrt(x)); V3 = u * V2
        H = np.zeros((len(K), 8, 8), complex)
        for a in range(4):
            for b in range(4):
                if a != b:
                    H[:, a, b] = -v1; H[:, 4 + a, 4 + b] = -v1
            H[:, a, a] = -V3; H[:, 4 + a, 4 + a] = V3
            H[:, a, 4 + a] = -V2 * ph[:, a]; H[:, 4 + a, a] = -V2 * np.conj(ph[:, a])
        w, U = np.linalg.eigh(H)
        occ = U[:, :, :4]
        shareA = np.mean(np.sum(np.abs(occ[:, :4, :]) ** 2, axis=(1, 2))) / 4
        mu = x / (1 + x)
        e = shareA / mu - 1
        row.append(e)
        if v1 <= 0.25 + 1e-12:
            worst_cov = max(worst_cov, abs(e))
    print(f"{v1:5.2f}  " + " ".join(f"{e:+8.4f}" for e in row))
ok = worst_cov < 0.02
print(f"\nworst |relative deviation| for V1/V2 <= 0.25: {worst_cov:.4f}")
print("T09", "PASS" if ok else "FAIL", f"- the crystal's TetA share stays within {worst_cov*100:.2f}% of the single-bond mu(x) "
      "in the covalent regime (criterion 2%)")
