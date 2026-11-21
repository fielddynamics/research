"""
The tug-of-war theorem for the GFD constitutive law, tested.

    mu(x) = x/(x+1),  x = g/a0,  is the TetA share of a tug of war between
    TetA (pulling with g) and TetB (pulling with a0), and every premise that
    makes it so is necessary.

Parts (each test name says which statement it checks):
  1  The cube forces a two-team share           (geometry; proved in WalshEigenmodes.lean)
  2  Exchange + screening force a power law     (algebra)
  3  Flat rotation curves force the power 1     (dynamics)
  4  Every premise is necessary                 (explicit counterexamples)
  5  The Field Origin is the one node           (Kron reduction)
  6  The cap: TetB never pulls past a0          (bookkeeping)
  7  Decoding mass: quiet, drive, brake         (the decoding-mass letter's quantities)
  8  Vortex facts the picture rests on          (exact Navier-Stokes solutions)
  9  Two corrections to the constitutive-law folder

Run:  python -m pytest -q test_tug_of_war.py
"""
import itertools
import math

import numpy as np
import pytest
import sympy as sp
from scipy.optimize import brentq

# ============================================================================================
# Shared definitions
# ============================================================================================
CORNERS = [np.array(s) for s in itertools.product([1, -1], repeat=3)]
IDX = {tuple(s): i for i, s in enumerate(CORNERS)}
IN_A = np.array([s.prod() == 1 for s in CORNERS])  # TetA: xyz = +1
SUBSETS = list(itertools.product([0, 1], repeat=3))  # Walsh index as an indicator of {x, y, z}


def walsh(S):
    return np.array([np.prod([s[d] for d in range(3) if S[d]]) for s in CORNERS], dtype=float)


def Td():
    """The 24 signed axis permutations that keep TetA."""
    group = []
    for p in itertools.permutations(range(3)):
        for signs in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3), dtype=int)
            for i in range(3):
                M[i, p[i]] = signs[i]
            if all((M @ s).prod() == 1 for s, a in zip(CORNERS, IN_A) if a):
                group.append(M)
    return group


def perm_matrix(M):
    P = np.zeros((8, 8))
    for i, s in enumerate(CORNERS):
        P[IDX[tuple(M @ s)], i] = 1
    return P


def SA(phi):
    return phi[IN_A].sum()


def SB(phi):
    return phi[~IN_A].sum()


def share(phi):
    return SA(phi) / (SA(phi) + SB(phi))


def law(x):
    return x / (x + 1)


def screening_root(x, n, m, p):
    """The root in (0, 1) of the screening relation x^n (1 - mu)^m = mu^p."""
    return brentq(lambda u: x**n * (1 - u) ** m - u**p, 1e-300, 1 - 1e-16, xtol=1e-15)


def total_pull(g_bar, a0, k):
    """Solve mu(g/a0) g = g_bar for the total pull g, with odds (g/a0)^k."""
    f = lambda g: (g / a0) ** k / (1 + (g / a0) ** k) * g - g_bar  # noqa: E731
    hi = g_bar + 10 * a0 + 10 * (g_bar * a0**k) ** (1 / (k + 1))
    return brentq(f, g_bar, hi, xtol=1e-30, rtol=1e-14)


# ============================================================================================
# 1. The cube forces a two-team share
# ============================================================================================
def test_1_1_Td_has_24_elements_and_keeps_each_chamber():
    G = Td()
    assert len(G) == 24
    assert all(IN_A[IDX[tuple(M @ s)]] == a for M in G for s, a in zip(CORNERS, IN_A))


def test_1_2_symmetric_states_have_exactly_two_values_one_per_team():
    P = sum(perm_matrix(M) for M in Td()) / 24
    assert np.linalg.matrix_rank(P, tol=1e-10) == 2
    for ind in (IN_A.astype(float), (~IN_A).astype(float)):
        assert np.allclose(P @ ind, ind)


@pytest.mark.parametrize("wA,wB", [(1.0, 1.0), (3.0, 1.0), (0.2, 5.0)])
def test_1_3_share_rope_position_and_capacity(wA, wB):
    """mu = wA/(wA+wB); the rope position s = c_xyz/c_1; the docs' capacity f = 17 + 4 s."""
    phi = np.where(IN_A, wA, wB)
    s = (walsh((1, 1, 1)) @ phi) / (walsh((0, 0, 0)) @ phi)
    x = wA / wB
    assert math.isclose(share(phi), wA / (wA + wB))
    assert math.isclose(s, (x - 1) / (x + 1))
    assert math.isclose(share(phi), (1 + s) / 2)
    assert math.isclose(17 + 4 * s, (21 * x + 13) / (x + 1))


def test_1_4_inversion_swaps_the_teams():
    rng = np.random.default_rng(0)
    for _ in range(20):
        phi = rng.uniform(0.1, 5, 8)
        swapped = np.array([phi[IDX[tuple(-s)]] for s in CORNERS])
        assert math.isclose(share(swapped), 1 - share(phi))


def test_1_5_vortex_modes_cannot_move_the_rope():
    """The vortices live in the T2 modes (grades 1 and 2); adding any of them leaves mu fixed."""
    rng = np.random.default_rng(1)
    base = np.where(IN_A, 2.0, 1.0)
    for _ in range(50):
        vortex = sum(rng.normal() * walsh(S) for S in SUBSETS if sum(S) in (1, 2))
        assert math.isclose(share(base + vortex), share(base))


# ============================================================================================
# 2. Exchange + screening force a power law
# ============================================================================================
@pytest.mark.parametrize("n,m,p", list(itertools.product([1, 2, 3], repeat=3)))
def test_2_1_exchange_holds_exactly_when_the_screening_powers_match(n, m, p):
    """x^n (1 - mu)^m = mu^p is exchange-symmetric, mu(1/x) = 1 - mu(x), iff m = p."""
    defect = max(abs(screening_root(x, n, m, p) + screening_root(1 / x, n, m, p) - 1)
                 for x in (0.05, 0.3, 2.0, 7.0))
    assert (defect < 1e-9) == (m == p)


def test_2_2_matching_powers_make_the_odds_a_pure_power():
    """m = p gives (mu/(1-mu))^p = x^n: the odds are Omega = x^k with k = n/p."""
    x, u = sp.symbols("x u", positive=True)
    for n, p in [(1, 1), (2, 1), (1, 2), (3, 2)]:
        k = sp.Rational(n, p)
        assert sp.simplify((x**n * (1 - u) ** p - u**p).subs(u, x**k / (1 + x**k))) == 0


def test_2_3_any_smooth_scale_covariant_odds_are_a_power():
    """Omega(xy) = Omega(x) Omega(y), differentiated at y = 1, gives x Omega' = k Omega."""
    x, k = sp.symbols("x k", positive=True)
    f = sp.Function("Omega")
    sol = sp.dsolve(sp.Eq(x * f(x).diff(x), k * f(x)), f(x)).rhs
    C1 = sp.Symbol("C1")
    sol = sol.subs(C1, sp.solve(sp.Eq(sol.subs(x, 1), 1), C1)[0])  # Omega(1) = 1
    assert sp.simplify(sol - x**k) == 0


# ============================================================================================
# 3. Flat rotation curves force the power 1
# ============================================================================================
@pytest.mark.parametrize("k", [0.5, 1.0, 2.0, 3.0])
def test_3_1_outer_rotation_curve_slope_is_k_minus_1_over_k_plus_1(k):
    GM, a0, r1, r2 = 1.0, 1.0, 1e5, 1e6
    v2 = lambda r: total_pull(GM / r**2, a0, k) * r  # noqa: E731
    slope = math.log(v2(r2) / v2(r1)) / math.log(r2 / r1)
    assert math.isclose(slope, (k - 1) / (k + 1), abs_tol=2e-3)


def test_3_2_power_1_gives_tully_fisher():
    GM, a0 = 3.0, 1.0
    for r in (1e5, 1e6, 1e7):
        v2 = total_pull(GM / r**2, a0, 1.0) * r
        assert math.isclose(v2**2, GM * a0, rel_tol=1e-3)


@pytest.mark.parametrize("k", [0.5, 1, 2, 3])
def test_3_3_power_1_iff_the_team_strengths_are_accelerations(k):
    """With odds x^k, TetA's strength is g^k: mu (g^k + a0^k) = g^k. The strengths are
    accelerations that add up to the measured pull, mu (g + a0) = g, only for k = 1."""
    a0 = 1.0
    ok = all(math.isclose((g / a0) ** k / (1 + (g / a0) ** k) * (g + a0), g, rel_tol=1e-12)
             for g in (0.1, 0.7, 3.0, 20.0))
    assert ok == (k == 1)


def test_3_4_the_law_is_the_tug_of_war_of_g_against_a0():
    g, a0 = sp.symbols("g a0", positive=True)
    assert sp.simplify(g / (g + a0) - law(g / a0)) == 0


# ============================================================================================
# 4. Every premise is necessary
# ============================================================================================
def omega_counter(x, c):
    """Exchange-symmetric odds with the right MOND limits that are NOT the law:
    log Omega(e^t) - t = c t exp(-t^2) is odd in t and vanishes at both ends."""
    t = np.log(x)
    return x * np.exp(c * t * np.exp(-t * t))


@pytest.mark.parametrize("c", [0.3, -0.3, 0.6])
def test_4_1_exchange_and_limits_alone_do_not_fix_mu(c):
    xs = np.logspace(-6, 6, 4001)
    mu = omega_counter(xs, c) / (1 + omega_counter(xs, c))
    mu_inv = omega_counter(1 / xs, c) / (1 + omega_counter(1 / xs, c))
    assert np.allclose(mu_inv, 1 - mu, atol=1e-12)  # exchange
    assert abs(mu[0] / xs[0] - 1) < 1e-4 and abs(mu[-1] - 1) < 1e-5  # both limits
    assert np.all(np.diff(mu) > 0)  # increasing
    assert np.max(np.abs(mu - law(xs))) > 1e-2  # and yet not the law
    lhs = omega_counter(np.array([2.7 * 0.4]), c)[0]  # it fails scale covariance
    assert abs(lhs - omega_counter(np.array([2.7]), c)[0] * omega_counter(np.array([0.4]), c)[0]) > 1e-3


def test_4_2_without_matching_powers_the_bimetric_law_breaks_exchange():
    """The folder's N = 2 law x (1 - mu)^2 = mu gives mu(1) = 1/phi^2, not 1/2."""
    phi = (1 + math.sqrt(5)) / 2
    assert math.isclose(screening_root(1.0, 1, 2, 1), 1 / phi**2, rel_tol=1e-12)
    assert abs(screening_root(3.0, 1, 2, 1) + screening_root(1 / 3, 1, 2, 1) - 1) > 1e-2


def test_4_3_without_power_1_the_curves_do_not_flatten():
    GM, a0 = 1.0, 1.0
    v2 = lambda r: total_pull(GM / r**2, a0, 2.0) * r  # noqa: E731
    assert v2(1e6) / v2(1e5) > 2.0  # k = 2: v^2 ~ r^(1/3), still rising


@pytest.mark.parametrize(
    "name,f",
    [("standard", lambda x: x / np.sqrt(1 + x**2)),
     ("exponential", lambda x: 1 - np.exp(-x)),
     ("n = 3 family", lambda x: x / (1 + x**3) ** (1 / 3))],
)
def test_4_4_other_interpolating_functions_break_exchange(name, f):
    xs = np.logspace(-2, 2, 41)
    assert np.max(np.abs(f(xs) + f(1 / xs) - 1)) > 1e-2
    assert np.allclose(law(xs) + law(1 / xs), 1, atol=1e-14)


def _identity_solutions(expr, var, unknowns):
    coeffs = sp.Poly(sp.expand(sp.numer(sp.together(expr))), var).coeffs()
    return sp.solve(coeffs, unknowns, dict=True)


def test_4_5_degree_one_route_and_the_share_condition():
    """The repo's other route: a relation of degree one, p + q x + r mu + t x mu = 0, with
    mu(0) = 0 and exchange leaves x/(x+1) and x/(x-1); only the first stays in [0, 1]."""
    x = sp.symbols("x", positive=True)
    p, q, r, t = sp.symbols("p q r t")
    mu = -(p + q * x) / (r + t * x)
    laws = set()
    for s in _identity_solutions(mu.subs(x, 1 / x) - (1 - mu), x, [p, q, r, t]):
        m = sp.simplify(mu.subs(s))
        if sp.simplify(m.diff(x)) == 0:
            continue
        free = sorted(m.free_symbols - {x}, key=str)
        for e in sp.solve(sp.Eq(m.subs(x, 0), 0), free[0]):
            laws.add(sp.simplify(m.subs(free[0], e)))
    assert laws == {x / (x + 1), x / (x - 1)}
    in_range = {m for m in laws if all(0 <= float(m.subs(x, v)) <= 1 for v in (0.1, 0.5, 2, 10))}
    assert in_range == {x / (x + 1)}


@pytest.mark.parametrize("k", [2, 3])
def test_4_6_the_two_routes_agree_only_at_power_1(k):
    """x^k is a degree-one (Moebius) map only for k = 1, so both routes single out the law."""
    x = sp.symbols("x", positive=True)
    a, b, c, d = sp.symbols("a b c d")
    sols = _identity_solutions(x**k * (c * x + d) - (a * x + b), x, [a, b, c, d])
    assert sols == [{a: 0, b: 0, c: 0, d: 0}]


# ============================================================================================
# 5. The Field Origin is the one node
# ============================================================================================
def test_5_1_one_node_between_two_teams_is_a_weighted_average():
    """Kirchhoff at the Field Origin: its state is the strength-weighted average of the teams,
    and eliminating it leaves the series (parallel-sum) link cA cB/(cA + cB)."""
    cA, cB, VA, VB, VO = sp.symbols("c_A c_B V_A V_B V_O", positive=True)
    VO_sol = sp.solve(sp.Eq(cA * (VA - VO) + cB * (VB - VO), 0), VO)[0]
    assert sp.simplify(VO_sol - (cA * VA + cB * VB) / (cA + cB)) == 0
    L = sp.Matrix([[cA, 0, -cA], [0, cB, -cB], [-cA, -cB, cA + cB]])
    Lred = L[:2, :2] - L[:2, 2:] * L[2:, 2:].inv() * L[2:, :2]
    assert sp.simplify(Lred[0, 0] - cA * cB / (cA + cB)) == 0


def cube_with_centre(tA, tB, he=0.0):
    """Eight corners and the Field Origin; corners link to the centre (tA on TetA, tB on
    TetB) and, if he != 0, directly along the cube's edges."""
    H = np.zeros((9, 9))
    for i, s in enumerate(CORNERS):
        H[i, 8] = H[8, i] = tA if IN_A[i] else tB
        for j, t in enumerate(CORNERS):
            if np.sum(s != t) == 1:
                H[i, j] = he
    return H


@pytest.mark.parametrize("tA,tB", [(1.0, 1.0), (2.0, 1.0), (0.3, 1.7)])
def test_5_2_eliminating_the_field_origin_leaves_one_rope(tA, tB):
    H = cube_with_centre(tA, tB)
    E = 5.0
    K = H[:8, :8] + H[:8, 8:] @ np.linalg.inv(E * np.eye(1) - H[8:, 8:]) @ H[8:, :8]
    assert np.linalg.matrix_rank(K, tol=1e-10) == 1
    w, V = np.linalg.eigh(K)
    assert math.isclose(share(V[:, np.argmax(np.abs(w))]), tA / (tA + tB), rel_tol=1e-12)


def test_5_3_direct_edges_between_the_teams_break_the_rule():
    tA, tB = 2.0, 1.0
    w, V = np.linalg.eigh(cube_with_centre(tA, tB, he=0.7))
    shares = [share(V[:8, k]) for k in range(9) if abs(SA(V[:8, k]) + SB(V[:8, k])) > 1e-6]
    assert shares and all(abs(m - tA / (tA + tB)) > 1e-3 for m in shares)


# ============================================================================================
# 6. The cap: TetB never pulls past a0
# ============================================================================================
def test_6_1_each_team_carries_mu_times_its_own_strength():
    """g = mu g + mu a0: TetA carries mu g, TetB carries mu a0 = (1 - mu) g."""
    g, a0 = sp.symbols("g a0", positive=True)
    mu = g / (g + a0)
    assert sp.simplify(mu * g + mu * a0 - g) == 0
    assert sp.simplify((1 - mu) * g - mu * a0) == 0


def test_6_2_tetB_rises_towards_a0_and_never_passes_it():
    a0 = 1.2e-10
    gs = np.logspace(-14, 2, 200)
    tetB = gs / (gs / a0 + 1)  # (1 - mu) g, computed without cancellation
    assert np.all(tetB < a0) and np.all(np.diff(tetB) > 0)
    assert math.isclose(tetB[-1] / a0, 1, rel_tol=1e-9)


def test_6_3_tetB_is_the_series_combination_of_g_and_a0():
    for g in (0.01, 1.0, 100.0):
        par = g / (1 + g)  # a0 = 1
        assert math.isclose((1 - law(g)) * g, par) and par <= min(g, 1.0)


def test_6_4_missing_over_visible_is_a0_over_g():
    for g in (0.1, 1.0, 1.75, 10.0):
        assert math.isclose((1 - law(g)) / law(g), 1 / g)


def test_6_5_a0_is_the_one_pull_the_exchange_leaves_fixed():
    """Swapping strong and weak pulls covariantly is g -> c/g; its fixed point is a0 = sqrt(c)."""
    g, c, lam = sp.symbols("g c lam", positive=True)
    E = c / g
    assert sp.simplify(E.subs(g, E) - g) == 0
    assert sp.simplify(E.subs(g, lam * g) - E / lam) == 0
    assert sp.solve(sp.Eq(E, g), g) == [sp.sqrt(c)]


# ============================================================================================
# 7. Decoding mass: quiet, drive, brake
# ============================================================================================
# g     total pull (observed: v^2/r)            g_bar  visible pull (photometric: G M_phot / r^2)
# M_dec = mu(g/a0) g r^2 / G  (the letter's decode)   M_phot = g_bar r^2 / G
# Measured share mu_obs = g_bar/g. TetB's measured strength w = g (g - g_bar)/g_bar, i.e. the
# a0 that would make the measured rope position the quiet one.
def decoded_ratio(g, g_bar, a0):
    return law(g / a0) * g / g_bar


def tetB_strength(g, g_bar):
    return g * (g - g_bar) / g_bar


def test_7_1_the_decode_is_the_letters_formula():
    G, a0 = 4.3e-6, 3.7e3  # kpc (km/s)^2 / Msun, and a0 in (km/s)^2/kpc
    for v, r in [(150.0, 5.0), (220.0, 15.0)]:
        g = v**2 / r
        assert math.isclose(law(g / a0) * g * r**2 / G, r * v**4 / (G * (a0 * r + v**2)))


@pytest.mark.parametrize("g,g_bar", [(2.0, 1.0), (2.0, 1.3), (0.5, 0.1), (0.5, 0.25), (30.0, 29.0)])
def test_7_2_decoded_over_photometric_is_tetB_strength_against_a0(g, g_bar):
    """M_dec/M_phot = (g + w)/(g + a0): the decode compares TetB's measured strength w with a0."""
    a0 = 1.0
    w = tetB_strength(g, g_bar)
    assert math.isclose(decoded_ratio(g, g_bar, a0), (g + w) / (g + a0), rel_tol=1e-12)
    assert math.isclose(decoded_ratio(g, g_bar, a0) - 1, (w - a0) / (g + a0), rel_tol=1e-9, abs_tol=1e-15)


def test_7_3_quiet_drive_brake_are_tetB_pulling_at_harder_or_softer_than_a0():
    a0 = 1.0
    rng = np.random.default_rng(3)
    for _ in range(500):
        g = 10 ** rng.uniform(-2, 2)
        g_bar = g * rng.uniform(0.01, 0.999)
        ratio, w = decoded_ratio(g, g_bar, a0), tetB_strength(g, g_bar)
        tetB_pull, quiet_pull = g - g_bar, law(g / a0) * a0
        drive, brake = ratio > 1 + 1e-12, ratio < 1 - 1e-12
        assert drive == (w > a0) == (tetB_pull > quiet_pull)  # drive: TetB pulls harder
        assert brake == (w < a0) == (tetB_pull < quiet_pull)  # brake: TetB pulls softer


def test_7_4_quiet_is_exactly_the_law():
    a0 = 1.0
    for g in (0.01, 0.5, 1.0, 4.0, 100.0):
        g_bar = law(g / a0) * g  # the law's visible pull
        assert math.isclose(decoded_ratio(g, g_bar, a0), 1.0, rel_tol=1e-12)
        assert math.isclose(tetB_strength(g, g_bar), a0, rel_tol=1e-9)


def test_7_5_drive_and_brake_hide_in_strong_fields():
    """The same change in TetB's strength moves the decode by (w - a0)/(g + a0): a few per cent
    in a galaxy's outskirts, invisible where g >> a0 (the solar system)."""
    a0, dw = 1.0, 0.5
    effect = lambda g: dw / (g + a0)  # noqa: E731
    assert effect(0.1) > 0.4 and effect(1e7) < 1e-7


# ============================================================================================
# 8. Vortex facts the picture rests on
# ============================================================================================
r, t, nu, alpha, Gam = sp.symbols("r t nu alpha Gamma", positive=True)


def azimuthal_residual(u_r, u_th, unsteady=False):
    """Axisymmetric azimuthal Navier-Stokes: d_t u + u_r (u' + u/r) = nu (u'' + u'/r - u/r^2)."""
    lhs = (sp.diff(u_th, t) if unsteady else 0) + u_r * (sp.diff(u_th, r) + u_th / r)
    rhs = nu * (sp.diff(u_th, r, 2) + sp.diff(u_th, r) / r - u_th / r**2)
    return sp.simplify(lhs - rhs)


def test_8_1_the_drained_vortex_is_steady_when_the_drain_balances_diffusion():
    """Burgers vortex: inflow u_r = -alpha r / 2 (axial outflow alpha z) holds the swirl
    u = Gamma/(2 pi r) (1 - exp(-alpha r^2 / 4 nu)) steady: the quiet state."""
    u = Gam / (2 * sp.pi * r) * (1 - sp.exp(-alpha * r**2 / (4 * nu)))
    assert azimuthal_residual(-alpha * r / 2, u) == 0


def test_8_2_without_a_drain_the_vortex_spreads_and_decays():
    """Lamb-Oseen: with no inflow the same circulation diffuses outwards."""
    u = Gam / (2 * sp.pi * r) * (1 - sp.exp(-r**2 / (4 * nu * t)))
    assert azimuthal_residual(0, u, unsteady=True) == 0


def _burgers_peak(a, n=1.0, G=1.0):
    u = lambda rr: G / (2 * math.pi * rr) * (1 - math.exp(-a * rr**2 / (4 * n)))  # noqa: E731
    rs = np.linspace(1e-4, 20 * math.sqrt(n / a), 200001)
    us = np.array([u(x) for x in rs])
    i = int(np.argmax(us))
    return rs[i], us[i]


def test_8_3_a_stronger_drain_tightens_and_spins_up_the_core():
    """Core radius ~ sqrt(nu/alpha), peak swirl ~ Gamma sqrt(alpha/nu): drive spins the core up,
    brake lets it spread."""
    (r1, u1), (r4, u4) = _burgers_peak(1.0), _burgers_peak(4.0)
    assert math.isclose(r1 / r4, 2.0, rel_tol=1e-3)
    assert math.isclose(u4 / u1, 2.0, rel_tol=1e-3)


def test_8_4_far_from_the_core_the_swirl_forgets_the_drain_strength():
    """Outside the core the swirl tends to Gamma/(2 pi r) whatever alpha is: the drain's strength
    is read from the core and the inflow, not from the far swirl."""
    u = Gam / (2 * sp.pi * r) * (1 - sp.exp(-alpha * r**2 / (4 * nu)))
    assert sp.limit(u * 2 * sp.pi * r / Gam, r, sp.oo) == 1


# ============================================================================================
# 9. Two corrections to research/constitutive-law-u(x)
# ============================================================================================
@pytest.mark.parametrize("N", [1, 2, 4, 16])
def test_9_1_independent_sites_stay_x_over_1_plus_x(N):
    """The folder says N sites give x^N/(1+x^N). Independent sites give x/(1+x) for any N; the
    Hill form needs the sites to fill together."""
    for x in (0.2, 1.0, 5.0):
        q = x / (1 + x)
        mean = sum(math.comb(N, j) * q**j * (1 - q) ** (N - j) * j / N for j in range(N + 1))
        assert math.isclose(mean, x / (1 + x), rel_tol=1e-12)


def test_9_2_the_standard_functions_inverse_is_algebraic_but_not_rational():
    u = sp.symbols("u", positive=True)
    inv = u / sp.sqrt(1 - u**2)
    assert sp.simplify(inv**2 * (1 - u**2) - u**2) == 0  # algebraic
    assert not inv.is_rational_function(u)  # not rational
    assert (u / (1 - u)).is_rational_function(u)  # the law's inverse is rational
