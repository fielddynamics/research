"""
Phase 0 field model (P0.1): closure uniformity and the capstone pump.

Study A — GFD closure current.
    J = mu grad Phi / (4 pi G) with mu ~ 1 (g / a0 ~ 1e11).  Inside the
    pyramid grad Phi is the terrestrial field (with its free-air gradient)
    plus the self-gravity of the pyramid (uniform-density square pyramid,
    discretised into cells).  The half-flux plane Phi_section(z) = Phi_base/2
    is located and compared with Theorem 1 of 01.6 and the King's Chamber
    floor (pre-registered test of 01.7 / PROGRAMME sec. 5).

Study B — atmospheric electric pump (axisymmetric finite differences).
    The pyramid is replaced by the cone of equal height and equal base area
    standing on a grounded plane, in a uniform fair-weather field E0.
    B1: dielectric body (eps_r = 8): flux of D through horizontal sections.
    B2: grounded conducting body (DC steady state, or a gilded / wetted skin):
        apex field enhancement, effective capture area, collected current and
        an upper bound on extractable power.

Run:  python -m python.phase0_field_model
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# Great Pyramid (Petrie 1883)
INCH = 0.0254
H_M = 5776.0 * INCH                    # 146.71 m
B_M = 9068.8 * INCH                    # 230.35 m (square base side)
KC_FLOOR_M = 1692.55 * INCH            # Petrie sec. 148, mean
ZSTAR_FRAC = 1.0 - 1.0 / math.sqrt(2.0)

# Physical constants and environment
G_N = 6.674e-11
G_EARTH = 9.7929                       # m/s^2 at Giza (approx.)
FREE_AIR = 3.086e-6                    # s^-2, vertical gradient of g
RHO_LIMESTONE = 2300.0                 # kg/m^3 (bulk, incl. voids; approx.)
EPS0 = 8.854e-12
E0_FAIR = 130.0                        # V/m, fair-weather potential gradient
J_AIR_EARTH = 2.0e-12                  # A/m^2, fair-weather air-earth current


# ===========================================================================
# Study A — GFD closure current through the pyramid
# ===========================================================================

def _pyramid_cells(n: int):
    """Centres and masses of n^3-ish cells filling the square pyramid."""
    zs = (np.arange(n) + 0.5) * H_M / n
    dz = H_M / n
    pts, mass = [], []
    for z in zs:
        half = 0.5 * B_M * (1 - z / H_M)
        m = max(1, int(round(n * half * 2 / B_M)))
        d = 2 * half / m
        c = -half + (np.arange(m) + 0.5) * d
        X, Y = np.meshgrid(c, c, indexing="ij")
        pts.append(np.column_stack([X.ravel(), Y.ravel(), np.full(X.size, z)]))
        mass.append(np.full(X.size, RHO_LIMESTONE * d * d * dz))
    return np.vstack(pts), np.concatenate(mass), dz


def self_gravity(points: np.ndarray, n_cells: int = 40, chunk: int = 4000) -> np.ndarray:
    """Gravitational acceleration (vector) of the pyramid's own mass at points."""
    cells, mass, dz = _pyramid_cells(n_cells)
    soft2 = (0.5 * dz) ** 2
    out = np.zeros_like(points)
    for i in range(0, len(points), chunk):
        p = points[i:i + chunk]
        d = cells[None, :, :] - p[:, None, :]
        r2 = np.sum(d * d, axis=2) + soft2
        out[i:i + chunk] = G_N * np.einsum("ij,ijk->ik", mass / r2 ** 1.5, d)
    return out


def closure_current_z(points: np.ndarray, include_self: bool = True,
                      include_free_air: bool = True) -> np.ndarray:
    """Vertical component of grad Phi (= -g_z), i.e. 4 pi G J_z / mu, at points.

    The terrestrial field points down (g_z = -g), so grad Phi points up."""
    z = points[:, 2]
    gz = -(G_EARTH - (FREE_AIR * z if include_free_air else 0.0))
    if include_self:
        gz = gz + self_gravity(points)[:, 2]
    return -gz


def section_flux(z: float, n: int = 20, **kw) -> float:
    half = 0.5 * B_M * (1 - z / H_M)
    t, w = np.polynomial.legendre.leggauss(n)
    X, Y = np.meshgrid(half * t, half * t, indexing="ij")
    W = np.outer(w, w) * half * half
    pts = np.column_stack([X.ravel(), Y.ravel(), np.full(X.size, z)])
    return float(np.sum(W.ravel() * closure_current_z(pts, **kw)))


@dataclass(frozen=True)
class StudyA:
    half_point_m: float
    zstar_m: float
    kc_floor_m: float
    shift_from_zstar_in: float
    offset_from_floor_in: float
    self_field_fraction: float
    free_air_fraction: float


def study_a(nz: int = 41, **kw) -> StudyA:
    zs = np.linspace(0.0, 0.9 * H_M, nz)
    phi = np.array([section_flux(z, **kw) for z in zs])
    ratio = phi / phi[0]
    # half point by linear interpolation in the bracketing interval
    k = int(np.where(ratio < 0.5)[0][0])
    z1, z2, r1, r2 = zs[k - 1], zs[k], ratio[k - 1], ratio[k]
    # refine with the exact areal form inside the bracket
    def mu(z):
        return section_flux(z, **kw) / phi[0]
    lo, hi = z1, z2
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if mu(mid) > 0.5:
            lo = mid
        else:
            hi = mid
    zh = 0.5 * (lo + hi)
    zstar = ZSTAR_FRAC * H_M
    base_pt = np.array([[0.0, 0.0, 1.0]])
    sg = abs(self_gravity(base_pt)[0, 2]) / G_EARTH
    return StudyA(
        half_point_m=zh,
        zstar_m=zstar,
        kc_floor_m=KC_FLOOR_M,
        shift_from_zstar_in=(zh - zstar) / INCH,
        offset_from_floor_in=(zh - KC_FLOOR_M) / INCH,
        self_field_fraction=sg,
        free_air_fraction=FREE_AIR * H_M / G_EARTH,
    )


# ===========================================================================
# Study B — atmospheric electric pump (axisymmetric finite differences)
# ===========================================================================

CONE_A_M = B_M / math.sqrt(math.pi)    # equal-area base radius (129.96 m)


def cone_radius(z):
    return CONE_A_M * (1.0 - np.asarray(z) / H_M)


@dataclass
class Grid:
    r: np.ndarray
    z: np.ndarray
    dr: float
    dz: float


def _grid(dr: float, R: float, Z: float) -> Grid:
    r = np.arange(0.0, R + 0.5 * dr, dr)
    z = np.arange(0.0, Z + 0.5 * dr, dr)
    return Grid(r, z, dr, dr)


def solve_axisymmetric(dr: float = 2.0, R: float = 900.0, Z: float = 900.0,
                       eps_body: float = 8.0, grounded_body: bool = False,
                       E0: float = E0_FAIR):
    """Solve div(eps grad V) = 0 in (r, z) for the cone in a uniform field.

    Boundary conditions: V = 0 on the ground (z = 0); V = -E0 z on the top and
    outer boundaries (uniform field E_z = +E0 means field pointing up; the
    fair-weather field points down, which only flips signs); symmetry at r = 0.
    If grounded_body, V = 0 inside the cone (conducting, earthed body).
    Returns (grid, V, eps, inside_mask)."""
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla

    g = _grid(dr, R, Z)
    nr, nz = len(g.r), len(g.z)
    Rr, Zz = np.meshgrid(g.r, g.z, indexing="ij")
    inside = Rr < cone_radius(np.clip(Zz, 0, H_M)) * (Zz < H_M)
    eps = np.where(inside, eps_body, 1.0)

    idx = np.arange(nr * nz).reshape(nr, nz)
    fixed = np.zeros((nr, nz), bool)
    val = np.zeros((nr, nz))
    fixed[:, 0] = True                      # ground
    fixed[:, -1] = True; val[:, -1] = -E0 * g.z[-1]
    fixed[-1, :] = True; val[-1, :] = -E0 * g.z
    if grounded_body:
        fixed |= inside
        val[inside] = 0.0

    rows, cols, data = [], [], []
    b = np.zeros(nr * nz)

    def eps_face(i1, j1, i2, j2):
        return 2.0 * eps[i1, j1] * eps[i2, j2] / (eps[i1, j1] + eps[i2, j2])

    for i in range(nr):
        for j in range(nz):
            k = idx[i, j]
            if fixed[i, j]:
                rows.append(k); cols.append(k); data.append(1.0); b[k] = val[i, j]
                continue
            diag = 0.0
            if i == 0:
                # r = 0 axis: (1/r) d/dr (r eps dV/dr) -> 2 d/dr(eps dV/dr), symmetric
                c = 4.0 * eps_face(0, j, 1, j) / dr ** 2
                rows.append(k); cols.append(idx[1, j]); data.append(c); diag -= c
            else:
                rp = g.r[i] + 0.5 * dr
                rm = g.r[i] - 0.5 * dr
                cp = eps_face(i, j, i + 1, j) * rp / (g.r[i] * dr ** 2)
                cm = eps_face(i, j, i - 1, j) * rm / (g.r[i] * dr ** 2)
                rows += [k, k]; cols += [idx[i + 1, j], idx[i - 1, j]]; data += [cp, cm]
                diag -= cp + cm
            czp = eps_face(i, j, i, j + 1) / dr ** 2
            czm = eps_face(i, j, i, j - 1) / dr ** 2
            rows += [k, k]; cols += [idx[i, j + 1], idx[i, j - 1]]; data += [czp, czm]
            diag -= czp + czm
            rows.append(k); cols.append(k); data.append(diag)

    A = sp.csr_matrix((data, (rows, cols)), shape=(nr * nz, nr * nz))
    V = spla.spsolve(A, b).reshape(nr, nz)
    return g, V, eps, inside


def dielectric_section_flux(g: Grid, V: np.ndarray, eps: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Flux of D_z = -eps dV/dz through the cone's horizontal sections."""
    zs, flux = [], []
    for j in range(1, len(g.z) - 1):
        z = g.z[j]
        if z >= H_M:
            break
        a = cone_radius(z)
        Ez = -(V[:, j + 1] - V[:, j - 1]) / (2 * g.dz)
        Dz = eps[:, j] * Ez
        m = g.r <= a
        rr = g.r[m]
        if len(rr) < 3:
            break
        flux.append(np.trapezoid(2 * np.pi * rr * Dz[m], rr))
        zs.append(z)
    return np.array(zs), np.array(flux)


@dataclass(frozen=True)
class StudyB:
    b1_half_point_m: float
    b1_shift_from_zstar_m: float
    b2_apex_enhancement: float
    b2_capture_area_m2: float
    b2_current_fair_A: float
    b2_power_bound_fair_W: float
    b2_power_bound_storm_W: float


def study_b(dr: float = 2.0) -> StudyB:
    # B1: dielectric body
    g, V, eps, inside = solve_axisymmetric(dr=dr, eps_body=8.0)
    zs, fl = dielectric_section_flux(g, V, eps)
    ratio = fl / fl[0]
    k = int(np.where(ratio < 0.5)[0][0])
    zh = zs[k - 1] + (0.5 - ratio[k - 1]) * (zs[k] - zs[k - 1]) / (ratio[k] - ratio[k - 1])

    # B2: grounded conducting body
    g2, V2, eps2, inside2 = solve_axisymmetric(dr=dr, grounded_body=True)
    # field just above the apex (first exterior node on the axis)
    j_apex = int(np.searchsorted(g2.z, H_M))
    Ez_apex = abs(V2[0, j_apex + 1] - V2[0, j_apex]) / g2.dz
    enhancement = Ez_apex / E0_FAIR
    # capture area: flux of E into the earthed body plus ground, relative to E0,
    # evaluated on a horizontal plane just above the ground within radius Rc,
    # minus the undisturbed value pi Rc^2 (the body's extra collection).
    jz = 2
    Ez_low = -(V2[:, jz + 1] - V2[:, jz - 1]) / (2 * g2.dz)
    # total flux through a high plane equals flux into body + ground
    jt = int(np.searchsorted(g2.z, 1.6 * H_M))
    Ez_top = -(V2[:, jt + 1] - V2[:, jt - 1]) / (2 * g2.dz)
    Rc = 0.6 * g2.r[-1]
    m = g2.r <= Rc
    flux_top = np.trapezoid(2 * np.pi * g2.r[m] * Ez_top[m], g2.r[m])
    # flux reaching the ground outside the body within Rc
    outside = g2.r > cone_radius(0.0)
    mo = m & outside
    flux_ground = np.trapezoid(2 * np.pi * g2.r[mo] * Ez_low[mo], g2.r[mo])
    capture = abs(flux_top - flux_ground) / E0_FAIR
    I_fair = J_AIR_EARTH * capture
    # Upper bound on extractable power: current times the potential the apex
    # would float to if insulated (~E0 h), with a matched load (factor 1/4).
    P_fair = 0.25 * I_fair * E0_FAIR * H_M
    # Dust storm: E ~ 10 kV/m; current density scales roughly with E (ohmic air).
    E_storm = 1.0e4
    P_storm = P_fair * (E_storm / E0_FAIR) ** 2
    return StudyB(zh, zh - ZSTAR_FRAC * H_M, enhancement, capture, I_fair, P_fair, P_storm)


def showcase() -> None:
    print("Phase 0 field model (P0.1)")
    print("=" * 64)
    a = study_a()
    print("Study A — GFD closure current (terrestrial field + self-gravity)")
    print(f"  self-gravity / g at base centre : {a.self_field_fraction:.2e}")
    print(f"  free-air change over height / g : {a.free_air_fraction:.2e}")
    print(f"  half-flux plane                 : {a.half_point_m:.4f} m")
    print(f"  Theorem 1 z*                    : {a.zstar_m:.4f} m")
    print(f"  shift from z*                   : {a.shift_from_zstar_in:+.3f} in")
    print(f"  offset from King's Chamber floor: {a.offset_from_floor_in:+.2f} in")
    verdict = "CONFIRMS" if abs(a.offset_from_floor_in) <= 3 else (
        "FALSIFIES" if abs(a.offset_from_floor_in) > 10 else "INCONCLUSIVE")
    print(f"  pre-registered test (±3 in confirm / >10 in falsify): {verdict}")
    print()
    b = study_b()
    print("Study B — atmospheric electric pump (cone of equal area, FD)")
    print(f"  B1 dielectric (eps_r=8): D-flux half plane {b.b1_half_point_m:.1f} m "
          f"({b.b1_shift_from_zstar_m:+.1f} m from z*)")
    print(f"  B2 grounded body: apex field enhancement ~{b.b2_apex_enhancement:.1f} "
          f"(grid-limited)")
    print(f"     capture area {b.b2_capture_area_m2:.3e} m^2; "
          f"fair-weather current {b.b2_current_fair_A:.2e} A")
    print(f"     extractable power bound: fair weather {b.b2_power_bound_fair_W:.2e} W, "
          f"dust storm (10 kV/m) {b.b2_power_bound_storm_W:.2e} W")


if __name__ == "__main__":
    showcase()
