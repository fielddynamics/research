"""Numerical demonstration: the SST with the law read at the mountain's scale.

Static weak-field Lagrangian (time-leg proof, Lemma 1), with the law's term read on the mountain's potential
Phi_bar = P Phi, P the projector onto spatial modes longer than the mountain scale ell:

    L = -|grad Phi|^2/(8 pi G) - rho Phi - (1/8 pi G) h(grad P Phi),    h = a0^2 [F(y) - y],  y = |grad Phi_bar|^2/a0^2

Euler-Lagrange (P is self-adjoint):  lap Phi + P div[(mu - 1) grad Phi_bar] = 4 pi G rho.
Because P is idempotent and commutes with derivatives, this splits exactly:
    the dimple   phi' = (1 - P) Phi:  lap phi' = 4 pi G (1 - P) rho              (linear: settled residual, bare G)
    the mountain Phi_bar = P Phi:     P div[mu grad Phi_bar] = 4 pi G P rho     (the law, at the mountain's scale)

The demo puts a 'galaxy' (wide blob) and a 'Sun' (compact mass) in a periodic box, solves both the mountain-scale
theory and the pointwise one (P = 1), and compares the extra pull around the Sun.
Units: 4 pi G = 1, a0 = 1. Run: python demo_mountain_scale.py"""
import numpy as np

N, Lbox = 96, 96.0
dx = Lbox / N
x1 = (np.arange(N) - N // 2) * dx
X, Y, Z = np.meshgrid(x1, x1, x1, indexing="ij")
k1 = 2 * np.pi * np.fft.fftfreq(N, d=dx)
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
K2 = KX ** 2 + KY ** 2 + KZ ** 2
K2[0, 0, 0] = 1.0
mu = lambda x: x / (1 + x)

def blob(m, s, c):
    r2 = (X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2
    b = np.exp(-r2 / (2 * s ** 2)); return m * b / (b.sum() * dx ** 3)

def grad(f):
    F = np.fft.fftn(f)
    return [np.real(np.fft.ifftn(1j * K * F)) for K in (KX, KY, KZ)]

def div(v):
    return np.real(np.fft.ifftn(sum(1j * K * np.fft.fftn(c) for K, c in zip((KX, KY, KZ), v))))

def inv_lap(s):
    S = np.fft.fftn(s - s.mean()); S = -S / K2; S[0, 0, 0] = 0
    return np.real(np.fft.ifftn(S))

def projector(ell):
    if ell is None:
        return lambda f: f
    mask = (np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2) <= np.pi / ell)
    return lambda f: np.real(np.fft.ifftn(np.fft.fftn(f) * mask))

def solve(rho, ell, iters=250, damp=0.6):
    """Solve lap Phi + P div[(mu-1) grad P Phi] = rho (4 pi G = 1) by damped Picard iteration."""
    P = projector(ell)
    Phi = inv_lap(rho)
    for _ in range(iters):
        g = grad(P(Phi)); gm = np.sqrt(sum(c ** 2 for c in g)) + 1e-30
        src = rho - P(div([(mu(gm) - 1) * c for c in g]))
        Phi = (1 - damp) * Phi + damp * inv_lap(src)
    g = grad(P(Phi)); gm = np.sqrt(sum(c ** 2 for c in g)) + 1e-30
    res = div(grad(Phi)) + P(div([(mu(gm) - 1) * c for c in g])) - (rho - rho.mean())
    return Phi, np.abs(res).max() / np.abs(rho - rho.mean()).max()

def action(Phi, rho, ell):
    """Discrete action, 4 pi G = 1: S = sum[-|grad Phi|^2/2 - rho Phi - h(grad P Phi)/2] dx^3."""
    P = projector(ell)
    g = grad(Phi); gb = grad(P(Phi)); yb = sum(c ** 2 for c in gb)
    h = (yb - 2 * np.sqrt(yb) + 2 * np.log1p(np.sqrt(yb))) - yb
    return (-0.5 * sum(c ** 2 for c in g) - rho * Phi - 0.5 * h).sum() * dx ** 3

if __name__ == "__main__":
    sun_at = (24.0, 0.0, 0.0)
    rho_gal = blob(5000.0, 6.0, (0, 0, 0))
    rho_sun = blob(300.0, 1.0, sun_at)
    ell = 12.0
    out = {}
    for name, l in (("mountain", ell), ("pointwise", None)):
        Phi_both, r1 = solve(rho_gal + rho_sun, l)
        Phi_gal, r2 = solve(rho_gal, l)
        out[name] = (Phi_both, Phi_gal, max(r1, r2))
    Phi_sunN = inv_lap(rho_sun)            # the Sun's own locally settled Newtonian potential
    # 1. the exact split for the mountain-scale solution
    P = projector(ell)
    Phi_both = out["mountain"][0]
    dimple = Phi_both - P(Phi_both)
    exact = inv_lap(rho_gal + rho_sun - P(rho_gal + rho_sun))
    print(f"field-equation residual (mountain / pointwise): {out['mountain'][2]:.1e} / {out['pointwise'][2]:.1e}")
    print(f"dimple (1-P)Phi vs Newtonian potential of (1-P)rho: max diff / max = "
          f"{np.abs(dimple - exact).max() / np.abs(exact).max():.1e}")
    # 2. the extra pull around the Sun: g(gal+sun) - g(gal only) - g_N(sun), radial component toward the Sun
    rx, ry, rz = X - sun_at[0], Y - sun_at[1], Z - sun_at[2]
    rr = np.sqrt(rx ** 2 + ry ** 2 + rz ** 2) + 1e-12
    gN = grad(Phi_sunN)
    for name in ("mountain", "pointwise"):
        Pb, Pg, _ = out[name]
        gb, gg = grad(Pb), grad(Pg)
        extra_in = sum((gb[i] - gg[i] - gN[i]) * (c / rr) for i, c in enumerate((rx, ry, rz)))   # outward radial; >0 = pull toward Sun
        for R in (2.0, 3.0, 4.0, 6.0):
            shell = (rr > R - 0.5) & (rr < R + 0.5)
            own = np.mean(sum(gN[i] * c / rr for i, c in enumerate((rx, ry, rz)))[shell])
            print(f"  {name:9s} r = {R:.0f}: extra pull toward the Sun = {np.mean(extra_in[shell]):+.3f} a0 "
                  f"(Sun's own Newtonian pull {own:.2f} a0)")
    # 3. the galaxy is unchanged: the galaxy-only field at the Sun's position, mountain vs pointwise
    i0 = (N // 2 + int(sun_at[0] / dx), N // 2, N // 2)
    gm_m = np.sqrt(sum(c[i0] ** 2 for c in grad(out["mountain"][1])))
    gm_p = np.sqrt(sum(c[i0] ** 2 for c in grad(out["pointwise"][1])))
    print(f"galaxy's field at the Sun's position: mountain {gm_m:.4f} a0, pointwise {gm_p:.4f} a0 "
          f"(difference {abs(gm_m - gm_p) / gm_p:.1e})")
    # 4. the action's gradient equals the field equation (finite difference along a random direction)
    rng = np.random.default_rng(1)
    d = rng.standard_normal(X.shape); d = inv_lap(d - d.mean()); d /= np.abs(d).max()
    rho = rho_gal + rho_sun
    eps = 1e-4
    fd = (action(Phi_both + eps * d, rho, ell) - action(Phi_both - eps * d, rho, ell)) / (2 * eps)
    g = grad(P(Phi_both)); gm = np.sqrt(sum(c ** 2 for c in g)) + 1e-30
    EL = div(grad(Phi_both)) + P(div([(mu(gm) - 1) * c for c in g])) - (rho - rho.mean())
    print(f"dS along a random direction: finite difference {fd:.4e}, from the field equation {(EL * d).sum() * dx ** 3:.4e}")
