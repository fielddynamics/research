"""S4 diagnostic (not a re-run of the criterion): is the lattice field with mu computed from the
Lambda spectrum the same as the field with mu = x/(1+x) inserted by formula (T03's model)?
If so, S4's residual is T03's lattice graininess, not the mechanism."""
import numpy as np
import s4_lattice_lambda as S
def run_formula(a0):
    phi = S.solve(np.ones(len(S.I)), 1.0); wb = np.ones(len(S.I)); ws = np.ones(S.N)
    mu = lambda gg: (np.minimum(gg, 1e8 * a0) / a0) / (1 + np.minimum(gg, 1e8 * a0) / a0)
    for it in range(300):
        gm = S.grad_mag(phi); gm[S.src] = 1e8 * a0
        wb = 0.5 * wb + 0.5 * mu(0.5 * (gm[S.I] + gm[S.J])); ws = 0.5 * ws + 0.5 * mu(gm)
        new = S.solve(wb, ws, phi); ch = np.max(np.abs(new - phi)) / np.max(np.abs(new)); phi = new
        if ch < 1e-9: break
    return S.grad_mag(phi)
for a0 in (1e-4, 1e-2):
    gl, _ = S.run(a0, a0); gf = run_formula(a0)
    print(f"a0 = {a0:.0e}: max |g_Lambda/g_formula - 1| over the window = {np.max(np.abs(gl[S.win]/gf[S.win] - 1)):.1e}; "
          f"worst shell error of the formula model = {max(abs(v) for _, v in S.compare(gf, a0)):.4f}")
