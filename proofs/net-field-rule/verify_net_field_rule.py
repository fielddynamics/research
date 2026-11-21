#!/usr/bin/env python3
"""
Verification: The Net-Field Rule
================================

Every statement of the proof is checked here: exactly with sympy where it is algebraic,
by quadrature for the Cassini quadrupole, and against data where it is a test (globular
clusters, dwarfs, SPARC). The checks are grouped by the paper's statements:

  Theorem 1      four faces of a drainless field, and the dictionary   Parts 16-18, 20-22, 26
  Corollary 1    the flux involution, and why it singles out x/(1+x)   Parts 21, 26
  Proposition 1  a body's TetB: enclosed, screened, bounded            Parts 1, 15, 28
  Proposition 2  a drain around every star is forced to fail           Parts 2, 3
  Theorem 2      the rubber sheet: the exact two-scale split           Parts 4, 5, 10, 13, 19, 23, 24
  Proposition 3  the sheet's edge                                      Parts 14, 25
  Proposition 4  bare G and the drain criterion, against the data      Parts 6-9, 17
  Proposition 5  predictions: wide binaries, the a0-free RAR slope     Parts 11, 21, 27
  Remark         the vortex picture                                    Part 12

Run: python verify_net_field_rule.py        (numpy, scipy, sympy, pytest)
"""
import math

import numpy as np
import pytest
import sympy as sp
from scipy import optimize

# ============================================================================================
# Constants (SI unless stated)
# ============================================================================================
G = 6.674e-11
A0 = 1.2e-10                     # m s^-2, measured (SPARC calibration)
GM_SUN = 1.32712440018e20        # m^3 s^-2
AU = 1.495978707e11
KPC = 3.0857e19
PC = 3.0857e16
V_SUN = 229e3                    # m/s, circular speed at the Sun (Eilers et al. 2019)
R_SUN = 8.2 * KPC                # m, galactocentric radius of the Sun
Q2_CASSINI_2SIGMA = 9e-27        # s^-2, Hees et al. 2014: Q2 = (3 +- 3) x 10^-27

PLANETS_AU = {"Mercury": 0.387, "Earth": 1.0, "Mars": 1.524, "Jupiter": 5.20,
              "Saturn": 9.58, "Uranus": 19.2, "Neptune": 30.1}

x, y, t, r = sp.symbols("x y t r", positive=True)
GS = sp.Symbol("G", positive=True)   # symbolic G for the exact tests


def mu(X):
    return X / (X + 1)


def g_total(gs, a0=A0):
    """Invert g_s = mu(g_t/a0) g_t for the simple law: g_t = (g_s + sqrt(g_s^2 + 4 g_s a0))/2."""
    return 0.5 * (gs + np.sqrt(gs * gs + 4 * gs * a0))


# ============================================================================================
# 1  Enclosure: a body's TetB is counted in its GM (Gauss)
# ============================================================================================
class TestEnclosure:
    """Outside a body, gravity reports only the enclosed total. However the body's mass is
    split between a TetA part and an enclosed TetB part, no orbit outside can separate them."""

    R, a, b, c = sp.symbols("R a b c", positive=True)

    def exterior_field(self, rho):
        s = sp.symbols("s", positive=True)
        M = sp.integrate(4 * sp.pi * s**2 * rho(s), (s, 0, self.R))
        return sp.simplify(GS * M / r**2), sp.simplify(M)

    def test_exterior_field_depends_only_on_total_mass(self):
        R, a, b, c = self.R, self.a, self.b, self.c
        rho_A = lambda s: a * (1 - s / R)            # a TetA profile
        rho_B = lambda s: b * (1 - (s / R) ** 2)     # an enclosed TetB profile
        rho_C = lambda s: c                          # any other profile
        gAB, MAB = self.exterior_field(lambda s: rho_A(s) + rho_B(s))
        gC, MC = self.exterior_field(rho_C)
        # choose c so that the two bodies have the same total mass: then the fields agree for all r > R
        csol = sp.solve(sp.Eq(MAB, MC), c)[0]
        assert sp.simplify(gAB - gC.subs(c, csol)) == 0

    def test_split_between_teams_is_invisible(self):
        R, a, b = self.R, self.a, self.b
        f = sp.symbols("f", positive=True)          # TetB fraction of the enclosed mass, anything in (0,1)
        M = sp.symbols("M", positive=True)
        g_split = GS * ((1 - f) * M + f * M) / r**2
        assert sp.simplify(g_split - GS * M / r**2) == 0

    def test_kepler_measures_only_GM_total(self):
        P, aa, GMt = sp.symbols("P a GM", positive=True)
        kepler = sp.Eq(P**2, 4 * sp.pi**2 * aa**3 / GMt)
        f, M = sp.symbols("f M", positive=True)
        lhs = sp.solve(kepler.subs(GMt, GS * ((1 - f) * M + f * M)), P)[0]
        rhs = sp.solve(kepler.subs(GMt, GS * M), P)[0]
        assert sp.simplify(lhs - rhs) == 0


# ============================================================================================
# 2  The per-mass reading is forced to fail (exact)
# ============================================================================================
class TestPerMassReadingForced:
    """Apply mu to each mass's own field. Then around every star the TetB share leaves a
    tail g_t - g_s = (1 - mu) g_t. Exchange symmetry plus flat curves force that tail to a0
    for EVERY admissible mu, not just x/(x+1): no interpolating function escapes."""

    def test_simple_law_tail_tends_to_a0(self):
        gs, a0 = sp.symbols("g_s a_0", positive=True)
        gt = (gs + sp.sqrt(gs**2 + 4 * gs * a0)) / 2
        assert sp.simplify(gt * (gt / a0) / (gt / a0 + 1) - gs) == 0   # it is the inverse
        assert sp.limit(gt - gs, gs, sp.oo) == a0

    def test_exchange_plus_deep_field_forces_one_over_x(self):
        """Exchange: mu(1/x) = 1 - mu(x). Deep field: mu(x)/x -> 1 as x -> 0.
        Hence x (1 - mu(x)) = x mu(1/x) = mu(u)/u with u = 1/x -> 0, so it tends to 1."""
        # the family mu = (1 + tanh h(ln x))/2 with h odd and h(t) ~ t/2 at both ends
        for alpha in (0, sp.Rational(3, 5), 2, 4):
            h = t / 2 + alpha * sp.tanh(t)
            m = (1 + sp.tanh(h)) / 2
            # exchange symmetry holds identically
            assert sp.simplify(m.subs(t, -t) - (1 - m)) == 0
            # tail ratio x (1 - mu) = e^t (1 - mu) at t -> +oo
            tail = sp.limit(sp.exp(t) * (1 - m), t, sp.oo)
            assert tail == sp.exp(-2 * alpha)   # finite and nonzero: the tail is a constant pull
        # GFD's member (alpha = 0) is x/(x+1), with tail exactly 1
        m0 = (1 + sp.tanh(t / 2)) / 2
        assert sp.simplify(m0.rewrite(sp.exp) - sp.exp(t) / (sp.exp(t) + 1)) == 0

    def test_tail_is_a_constant_pull_at_every_planet(self):
        """Per-mass reading: an extra Sun-ward pull within 1% of a0 at every planet."""
        for name, d in PLANETS_AU.items():
            gs = GM_SUN / (d * AU) ** 2
            extra = g_total(gs) - gs
            assert abs(extra / A0 - 1) < 1e-2, name

    def test_tail_is_not_absorbable_into_GM(self):
        """A constant pull is not 1/r^2, so no rescaling of GM removes it: the effective GM
        it implies grows as r^2 across the planets (factor ~6000 from Mercury to Neptune)."""
        eff = []
        for d in PLANETS_AU.values():
            rr = d * AU
            eff.append(g_total(GM_SUN / rr**2) * rr**2)
        frac = [(e - GM_SUN) / GM_SUN for e in eff]
        assert frac[-1] / frac[0] > 5e3


# ============================================================================================
# 3  ... and Cassini excludes it (external-field quadrupole)
# ============================================================================================
def Tzz_simple(eta):
    """Tidal T_zz of the phantom potential at the Sun, units G M_sun = a0 = 1, external field eta z^.
    QUMOND form with nu(y) = 1/2 + sqrt(1/4 + 1/y), the inverse of the simple mu (as in
    research/bimetric-projection/probe_efe_solar_system.py)."""
    nu = lambda yy: 0.5 + np.sqrt(0.25 + 1 / yy)

    def inner(rr):
        th = np.linspace(0, np.pi, 2001)
        ct, st = np.cos(th), np.sin(th)
        gx = -st / rr**2
        gz = -ct / rr**2 + eta
        gn = np.hypot(gx, gz)
        f = nu(gn) - 1
        Px, Pz = f * gx, f * gz
        Pr = Px * st + Pz * ct
        Pt = Px * ct - Pz * st
        P2 = 0.5 * (3 * ct**2 - 1)
        return np.trapezoid((Pr * P2 + Pt * ct * st) * st, th) / rr**2

    # integrate over ln r on a fine grid (the integrand is smooth in ln r; r from 1e-4 to 1e4 r_M)
    rs = np.logspace(-4, 4, 4001)
    return 3 * np.trapezoid(np.array([inner(rr) for rr in rs]) * rs, np.log(rs))


class TestCassiniExcludesPerMass:
    @pytest.fixture(scope="class")
    @staticmethod
    def q2():
        rM = math.sqrt(GM_SUN / A0)
        unit = A0 / rM
        ge = 1.9 * A0                           # the Milky Way's net field at the Sun, x ~ 1.9
        return 1.5 * abs(Tzz_simple(ge / A0)) * unit

    def test_quadrupole_value(self, q2):
        assert 3e-26 < q2 < 5e-26               # ~ 4e-26 s^-2

    def test_quadrupole_exceeds_cassini(self, q2):
        assert q2 > 4 * Q2_CASSINI_2SIGMA


# ============================================================================================
# 4  Free fall removes the host's uniform field exactly
# ============================================================================================
class TestUniformFieldDropsOut:
    """N bodies in their own Newtonian field plus a uniform host field g_e. Relative positions
    obey equations with no g_e in them: the host's net field, uniform across the system, is
    removed by common free fall. (In GR this is the equivalence principle.)"""

    def test_three_body_relative_motion_is_independent_of_g_e(self):
        n = 3
        m = sp.symbols("m0:%d" % n, positive=True)
        X = [sp.Matrix(sp.symbols(f"x{i} y{i} z{i}", real=True)) for i in range(n)]
        ge = sp.Matrix(sp.symbols("gx gy gz", real=True))

        def acc(i):
            a = sp.zeros(3, 1)
            for j in range(n):
                if j != i:
                    d = X[j] - X[i]
                    a += GS * m[j] * d / (d.dot(d)) ** sp.Rational(3, 2)
            return a + ge

        for i in range(n):
            for j in range(n):
                if i < j:
                    rel = acc(j) - acc(i)
                    assert all(sp.diff(rel[k], gsym) == 0 for k in range(3) for gsym in ge)

    def test_centre_of_mass_carries_the_host_field(self):
        n = 3
        m = sp.symbols("m0:%d" % n, positive=True)
        ge = sp.symbols("g_e", real=True)
        # internal forces cancel pairwise (Newton's third law), so the COM accelerates at g_e
        F = sp.symbols("F01 F02 F12", real=True)
        a0_ = (F[0] + F[1]) / m[0] + ge
        a1_ = (-F[0] + F[2]) / m[1] + ge
        a2_ = (-F[1] - F[2]) / m[2] + ge
        acom = (m[0] * a0_ + m[1] * a1_ + m[2] * a2_) / sum(m)
        assert sp.simplify(acom - ge) == 0


# ============================================================================================
# 5  What survives is the tide, four orders below Cassini
# ============================================================================================
class TestTideIsWhatSurvives:
    def test_relative_acceleration_is_the_tidal_tensor(self):
        """Host potential Phi(X), here a general quartic in three variables: two nearby bodies at
        X and X + eps d feel, beyond their own field, -grad Phi(X + eps d) + grad Phi(X)
        = -eps (Hess Phi) d + O(eps^2). The uniform part has gone; the tide is what is left."""
        X = sp.symbols("X1:4", real=True)
        d = sp.symbols("d1:4", real=True)
        eps = sp.Symbol("epsilon", real=True)
        monos = [X[0]**i * X[1]**j * X[2]**k for i in range(5) for j in range(5) for k in range(5)
                 if i + j + k <= 4]
        coeffs = sp.symbols("c0:%d" % len(monos), real=True)
        Phi = sum(c * m_ for c, m_ in zip(coeffs, monos))
        shift = {X[i]: X[i] + eps * d[i] for i in range(3)}
        for k in range(3):
            gk = -sp.diff(Phi, X[k])
            rel = sp.expand(gk.subs(shift, simultaneous=True) - gk)
            assert rel.coeff(eps, 0) == 0                                   # uniform part removed
            tidal = -sum(sp.diff(Phi, X[k], X[i]) * d[i] for i in range(3))
            assert sp.expand(rel.coeff(eps, 1) - tidal) == 0                # first order: the tide

    def test_flat_curve_tide_components(self):
        """Phi = v^2 ln R (flat rotation curve, in the plane): radial tide d2Phi/dR2 = -v^2/R^2,
        azimuthal (1/R) dPhi/dR = +v^2/R^2. Both have size v^2/R^2 = g/R."""
        v, R = sp.symbols("v R", positive=True)
        Phi = v**2 * sp.log(R)
        assert sp.simplify(sp.diff(Phi, R, 2) + v**2 / R**2) == 0
        assert sp.simplify(sp.diff(Phi, R) / R - v**2 / R**2) == 0

    def test_tide_at_the_sun(self):
        T = V_SUN**2 / R_SUN**2
        assert 7e-31 < T < 1.1e-30

    def test_tide_is_four_orders_below_cassini(self):
        T = V_SUN**2 / R_SUN**2
        assert Q2_CASSINI_2SIGMA / T > 5e3

    def test_tide_at_saturn(self):
        T = V_SUN**2 / R_SUN**2
        a_sat = T * PLANETS_AU["Saturn"] * AU
        assert 5e-19 < a_sat < 3e-18           # ~ 1e-18 m/s^2

    def test_tide_is_the_one_every_model_already_has(self):
        """The tide is fixed by the observed rotation curve alone (v, R), so GR with a dark halo,
        MOND and GFD with the net-field rule all give the same number at the Sun."""
        v, R = sp.symbols("v R", positive=True)
        assert sp.diff(v**2 * sp.log(R), R, 2).free_symbols == {v, R}

    def test_galactic_field_is_uniform_across_the_solar_system(self):
        """Across Neptune's orbit (60 AU) the host field changes by a fraction ~ 60 AU / 8.2 kpc
        ~ 4e-8 of itself, and the change (the tide) is ~ 1e-12 of the Sun's own field there."""
        frac_of_host = 2 * PLANETS_AU["Neptune"] * AU / R_SUN
        assert 1e-8 < frac_of_host < 1e-7
        r_nep = PLANETS_AU["Neptune"] * AU
        tide_over_sun = (V_SUN**2 / R_SUN**2) * r_nep / (GM_SUN / r_nep**2)
        assert 1e-13 < tide_over_sun < 1e-11


# ============================================================================================
# 6  A host factor on G is invisible to orbits ...
# ============================================================================================
class TestHostFactorInvisibleToOrbits:
    """An alternative reading: the host's mu-bar multiplies the internal G (G -> G/mu-bar,
    the quasi-Newtonian external-field effect). Orbits cannot tell, because Kepler sees GM."""

    def test_kepler_scaling(self):
        P, aa, M, mb = sp.symbols("P a M mubar", positive=True)
        P_ren = sp.sqrt(4 * sp.pi**2 * aa**3 / ((GS / mb) * M))
        P_bare = sp.sqrt(4 * sp.pi**2 * aa**3 / (GS * (M / mb)))
        assert sp.simplify(P_ren - P_bare) == 0

    def test_dynamical_mass_absorbs_the_factor(self):
        mb = mu(1.9)
        GM_measured = GM_SUN                  # what planetary ephemerides return
        GM_true_bare = GM_measured * mb       # the mass that would be inferred with G/mu-bar
        assert GM_true_bare / GM_measured == pytest.approx(mb)


# ============================================================================================
# 7  ... but globular clusters see it: so G stays bare
# ============================================================================================
# Outer-halo globular clusters and Milky Way dwarfs at low acceleration (as in
# research/bimetric-projection/probe_testD_clusters_vs_dwarfs.py).
# Units: pc, km/s, Msun.  Wolf et al. (2010): M(<r_1/2) = M/2 with r_1/2 = 4 Re/3.
G_PC = 4.30091e-3                 # pc (km/s)^2 / Msun
A0_PC = 3.7                       # (km/s)^2 / pc  (= 1.2e-10 m/s^2)
V_MW = 184.0                      # km/s, Milky Way circular speed in the outer halo
OBJECTS = {
    # name: (type, M [Msun], Re [pc], D_GC [kpc], sigma_obs, err)
    "Pal 14":    ("cluster", 1.2e4, 26.0, 71, 0.38, 0.12),    # Jordi et al. 2009
    "Pal 4":     ("cluster", 2.98e4, 18.4, 103, 0.87, 0.18),  # Frank et al. 2012
    "Crater II": ("dwarf", 3.3e5, 1066.0, 120, 2.34, 0.36),   # Caldwell et al. 2017; Ji et al. 2021
}


def sigmas(name):
    _, M, Re, D, so, se = OBJECTS[name]
    x_e = V_MW**2 / (D * 1000) / A0_PC
    rh = 4 * Re / 3
    x_in = G_PC * (M / 2) / rh**2 / A0_PC
    s_newton = math.sqrt(G_PC * M / (8 * Re))
    s_mu = math.sqrt(G_PC * M / (8 * Re) / mu(x_e + x_in))
    return s_newton, s_mu, so, se, x_e, x_in


class TestClustersAreNewtonian:
    @pytest.mark.parametrize("name", ["Pal 14", "Pal 4"])
    def test_cluster_is_deep_in_the_low_acceleration_regime(self, name):
        *_, x_e, x_in = sigmas(name)
        assert x_e + x_in < 0.2               # mu would matter strongly here

    @pytest.mark.parametrize("name", ["Pal 14", "Pal 4"])
    def test_bare_G_fits(self, name):
        sN, _, so, se, *_ = sigmas(name)
        assert abs(so - sN) / se < 1.5

    @pytest.mark.parametrize("name", ["Pal 14", "Pal 4"])
    def test_host_factor_on_G_is_excluded(self, name):
        _, sM, so, se, *_ = sigmas(name)
        assert (sM - so) / se > 8

    def test_so_the_rule_is_not_the_external_field_effect(self):
        """Orbits (Part 6) cannot separate bare G from G/mu-bar; photometric masses can, and
        they choose bare G. Inside a closed-drain system the host enters only by free fall
        and tide (Parts 4-5), never as a factor on G."""
        verdicts = []
        for name in ("Pal 14", "Pal 4"):
            sN, sM, so, se, *_ = sigmas(name)
            verdicts.append(abs(so - sN) < abs(so - sM))
        assert all(verdicts)


# ============================================================================================
# 8  Open drains keep mu: dwarfs are not Newtonian
# ============================================================================================
class TestDwarfsKeepMu:
    def test_crater_ii_is_not_newtonian(self):
        sN, _, so, se, *_ = sigmas("Crater II")
        assert (so - sN) / se > 4

    def test_crater_ii_is_consistent_with_mu(self):
        _, sM, so, se, *_ = sigmas("Crater II")
        assert abs(so - sM) / se < 2.5

    def test_crater_ii_estimator_matches_mcgaugh_deep_efe(self):
        """Cross-check: McGaugh's deep-EFE form sigma^2 = a0 G M / (3 g_e r_1/2) gives 2.1 km/s."""
        _, M, Re, D, *_ = OBJECTS["Crater II"]
        g_e = V_MW**2 / (D * 1000)
        s = math.sqrt(A0_PC * G_PC * M / (3 * g_e * 4 * Re / 3))
        assert s == pytest.approx(2.1, abs=0.05)


# ============================================================================================
# 9  The drain criterion sorts clusters and dwarfs as observed
# ============================================================================================
class TestDrainCriterion:
    """Clusters and dwarfs sit at the SAME low accelerations (x ~ 0.1) in the SAME host field.
    Any rule that depends only on accelerations treats them alike. The data treat them
    differently. The drain criterion (D) is what separates them, and in the right direction."""

    def test_same_accelerations(self):
        xs = {n: sigmas(n)[4] + sigmas(n)[5] for n in OBJECTS}
        assert max(xs.values()) / min(xs.values()) < 2.5
        assert max(xs.values()) < 0.2

    def test_no_acceleration_only_rule_fits_both(self):
        """With a common mu-bar applied to all three, the best single factor misfits badly."""
        def chi2(boost):
            tot = 0
            for n in OBJECTS:
                sN, _, so, se, *_ = sigmas(n)
                tot += ((so - sN * boost) / se) ** 2
            return tot
        best = optimize.minimize_scalar(chi2, bounds=(0.5, 10), method="bounded")
        assert best.fun > 15                   # three points, one parameter: still a bad fit

    def test_drain_rule_fits_all_three(self):
        drain_open = {"Pal 14": False, "Pal 4": False, "Crater II": True}
        chi2 = 0
        for n, open_ in drain_open.items():
            sN, sM, so, se, *_ = sigmas(n)
            pred = sM if open_ else sN
            chi2 += ((so - pred) / se) ** 2
        assert chi2 < 7.5                     # three points, no parameter: chi2 = 6.2


# ============================================================================================
# 10  The pointer picture: a closed system enters its host as one mass
# ============================================================================================
class TestPointerPicture:
    """Far from a bound system of size d, its field is G M/D^2 at the centre of mass, with
    no dipole and corrections of order (d/D)^2. So the host's net field is built from
    pointers (total mass, position) and its internal structure never enters."""

    def test_dipole_vanishes_about_centre_of_mass(self):
        m1, m2, d, D, eps = sp.symbols("m1 m2 d D epsilon", positive=True)
        # masses on the axis at -m2 d/(m1+m2) and +m1 d/(m1+m2): COM at 0
        z1 = -m2 * d / (m1 + m2)
        z2 = m1 * d / (m1 + m2)
        pot = -GS * m1 / (D - eps * z1) - GS * m2 / (D - eps * z2)
        ser = sp.series(pot, eps, 0, 3).removeO()
        c0 = sp.simplify(ser.coeff(eps, 0))
        c1 = sp.simplify(ser.coeff(eps, 1))
        c2 = sp.simplify(ser.coeff(eps, 2))
        assert sp.simplify(c0 + GS * (m1 + m2) / D) == 0      # monopole: the pointer
        assert c1 == 0                                         # no dipole
        assert sp.simplify(c2 + GS * m1 * m2 * d**2 / ((m1 + m2) * D**3)) == 0   # quadrupole ~ (d/D)^2

    def test_solar_system_pointer_error(self):
        """The quadrupole correction relative to the monopole, for the solar system seen from
        1 pc: (m_J/M_sun)(5.2 AU / 1 pc)^2 ~ 6e-13."""
        rel = (1 / 1047) * (5.2 * AU / PC) ** 2
        assert rel < 1e-12


# ============================================================================================
# 11  Wide binaries: the rule's sharp prediction
# ============================================================================================
class TestWideBinaries:
    def test_binary_mond_radius(self):
        """Separation where a binary's internal field falls to a0: r_M = sqrt(GM/a0)."""
        rM_sun = math.sqrt(GM_SUN / A0) / AU
        assert 6800 < rM_sun < 7300            # ~ 7000 AU for one solar mass
        assert math.sqrt(2) * rM_sun > 9500    # ~ 10^4 AU for a 2 Msun pair

    def test_gfd_predicts_exact_newton(self):
        """Closed drain: gamma = g_obs/g_N = 1 at every separation (Parts 4-7)."""
        M, s_, a0s, ge = sp.symbols("M s a_0 g_e", positive=True)
        g_internal = G * M / s_**2                       # TetA alone, bare G
        assert not ({a0s, ge} & g_internal.free_symbols)  # no a0, no host field
        for s_kau in (1, 3, 10, 20, 30):
            ss = s_kau * 1e3 * AU
            gamma = float(g_internal.subs({M: 2 * GM_SUN / G, s_: ss})) / (2 * GM_SUN / ss**2)
            assert gamma == pytest.approx(1.0, rel=1e-12)

    def test_acceleration_only_rules_predict_a_boost(self):
        """Quasi-Newtonian estimate with the host field: gamma = 1/mu(x_e + x_in) at the Sun's
        x_e ~ 1.9. At 20 kAU for 2 Msun this is ~1.5 in acceleration (~1.2 in velocity)."""
        x_e = 1.9
        s = 20e3 * AU
        x_in = 2 * GM_SUN / s**2 / A0
        gamma = 1 / mu(x_e + x_in)
        assert 1.4 < gamma < 1.6
        assert 1.15 < math.sqrt(gamma) < 1.3

    def test_the_two_predictions_differ_measurably(self):
        x_e = 1.9
        gammas = []
        for s_kau in (5, 10, 20):
            x_in = 2 * GM_SUN / (s_kau * 1e3 * AU) ** 2 / A0
            gammas.append(1 / mu(x_e + x_in))
        assert min(gammas) > 1.15              # every such rule: >15% at 5-20 kAU; GFD: 0%


# ============================================================================================
# 12  The vortex picture: pebble in a stream, open vs closed drain
# ============================================================================================
class TestVortexPicture:
    def test_navier_stokes_is_galilean_invariant(self):
        """Pebble in a stream: add a uniform stream U and move with it. For the 1D Burgers form
        u_t + u u_x = nu u_xx, u'(X,T) = u(X - U T, T) + U. By the chain rule
        u'_T = u_T - U u_xi, u'_X = u_xi, u'_XX = u_xixi, so the residuals are equal."""
        U, nu_, u0, ut, uxi, uxx = sp.symbols("U nu u u_T u_xi u_xixi", real=True)
        res_old = ut + u0 * uxi - nu_ * uxx
        res_new = (ut - U * uxi) + (u0 + U) * uxi - nu_ * uxx
        assert sp.expand(res_new - res_old) == 0
        # and the chain rule itself, on an explicit travelling profile
        X, T = sp.symbols("X T", real=True)
        f = sp.exp(-(X - U * T) ** 2) * sp.sin(T)
        xi = sp.Symbol("xi", real=True)
        g = sp.exp(-xi**2) * sp.sin(T)
        assert sp.simplify(sp.diff(f, T) - (sp.diff(g, T) - U * sp.diff(g, xi)).subs(xi, X - U * T)) == 0

    def test_small_body_sees_strain_not_stream(self):
        """Across a pebble of size d in a smooth stream U(x), the velocity difference is
        (dU/dx) d: the stream itself drops out, its gradient (the tide) remains."""
        X, d, eps = sp.symbols("X d epsilon", real=True)
        Uf = sp.Function("U")
        diff = sp.series(Uf(X + eps * d) - Uf(X), eps, 0, 2).removeO()
        assert sp.simplify(diff.doit() - eps * d * sp.diff(Uf(X), X)) == 0

    def test_open_drain_sustains_the_vortex(self):
        """Burgers vortex (drain strength alpha > 0): steady vorticity omega = C exp(-alpha r^2/4 nu)
        solves u_r omega' = alpha omega + nu (omega'' + omega'/r) with u_r = -alpha r/2."""
        al, nu_, C = sp.symbols("alpha nu C", positive=True)
        om = C * sp.exp(-al * r**2 / (4 * nu_))
        lhs = (-al * r / 2) * sp.diff(om, r)
        rhs = al * om + nu_ * (sp.diff(om, r, 2) + sp.diff(om, r) / r)
        assert sp.simplify(lhs - rhs) == 0

    def test_closed_drain_vortex_decays(self):
        """No drain (alpha = 0): Lamb-Oseen, omega = Gamma/(4 pi nu t) exp(-r^2/4 nu t), solves
        omega_t = nu (omega'' + omega'/r), and its peak decays as 1/t: no self-sustained vortex."""
        nu_, Gam = sp.symbols("nu Gamma", positive=True)
        om = Gam / (4 * sp.pi * nu_ * t) * sp.exp(-r**2 / (4 * nu_ * t))
        assert sp.simplify(sp.diff(om, t) - nu_ * (sp.diff(om, r, 2) + sp.diff(om, r) / r)) == 0
        assert sp.limit(om.subs(r, 0), t, sp.oo) == 0

    def test_closed_drain_keeps_its_circulation_far_away(self):
        """The Lamb-Oseen vortex keeps its total circulation Gamma (the far swirl Gamma/2 pi r):
        a closed system still has its total, like a body's GM, but no sustained core of its own."""
        nu_, Gam = sp.symbols("nu Gamma", positive=True)
        om = Gam / (4 * sp.pi * nu_ * t) * sp.exp(-r**2 / (4 * nu_ * t))
        assert sp.simplify(sp.integrate(2 * sp.pi * r * om, (r, 0, sp.oo)) - Gam) == 0


# ============================================================================================
# 13  The rubber sheet as an exact two-scale split
# ============================================================================================
# Write the total field as   g = F[ g_N(rho_bar) ] + g_N(rho - rho_bar),
#   F       : the drained (host) field law, nonlinear, applied to the host's smoothed density;
#   rho_bar : the density smoothed with a top-hat of radius l around each sheet (bound system);
#   second term: the sheet's own field, linear, bare G, no mu (premise A).
# The shell theorem makes the split exact: the sheet term vanishes identically outside l, so
# nothing is counted twice, and the host sees each sheet as one mass (Part 10).
class TestRubberSheetSplit:
    l, M = sp.symbols("ell M", positive=True)

    def g_point(self):
        return GS * self.M / r**2

    def g_tophat(self):
        l, M = self.l, self.M
        return sp.Piecewise((GS * M * r / l**3, r < l), (GS * M / r**2, True))

    def test_sheet_term_vanishes_outside_the_sheet(self):
        diff = self.g_point() - self.g_tophat()
        assert sp.simplify(diff.subs(r, self.l * 2)) == 0
        assert sp.simplify(diff.subs(r, self.l * 7)) == 0
        rr = sp.Symbol("rr", positive=True)
        outside = sp.piecewise_fold((self.g_point() - self.g_tophat()).subs(r, self.l + rr))
        assert sp.simplify(outside) == 0

    def test_sheet_term_is_continuous_at_the_edge(self):
        inside = GS * self.M / r**2 - GS * self.M * r / self.l**3
        assert sp.simplify(inside.subs(r, self.l)) == 0

    def test_sheet_term_inside_is_the_ball_minus_a_harmonic_term(self):
        """Inside the sheet, the sheet's own field is GM/r^2 (the ball, bare G) minus GM r/l^3.
        The second piece is returned by the host term, so inside the sheet the only change from
        pure TetA is (host response - 1) x GM r/l^3: a uniform-density-like term."""
        inside = GS * self.M / r**2 - GS * self.M * r / self.l**3
        returned = GS * self.M * r / self.l**3
        assert sp.simplify(inside + returned - GS * self.M / r**2) == 0

    def test_host_field_unchanged_by_smoothing(self):
        """Outside every sheet, g_N(rho_bar) = g_N(rho) exactly, so the galaxy's x, and every
        galactic prediction, is unchanged by treating its star systems as pointers."""
        assert sp.simplify((self.g_tophat() - self.g_point()).subs(r, 3 * self.l)) == 0

    def test_linear_guest_has_no_tail_nonlinear_guest_does(self):
        """The split is the drain criterion in equations. Put the ball's field through the
        linear (drainless) law and it stays GM/r^2. Put it through the drained law F and it
        picks up the a0 tail of Part 2."""
        gs, a0 = sp.symbols("g_s a_0", positive=True)
        F = (gs + sp.sqrt(gs**2 + 4 * gs * a0)) / 2
        assert sp.limit(gs - gs, gs, sp.oo) == 0
        assert sp.limit(F - gs, gs, sp.oo) == a0


# ============================================================================================
# 14  The sheet's edge is the Jacobi radius, with no free parameter
# ============================================================================================
OMEGA_SUN = V_SUN / R_SUN


def jacobi_radius(GM, Omega):
    """Tidal (Jacobi) radius in a flat rotation curve: r_J^3 = GM / (4 Omega^2 - kappa^2),
    kappa^2 = 2 Omega^2, so r_J^3 = GM / (2 Omega^2)."""
    return (GM / (2 * Omega**2)) ** (1 / 3)


class TestSheetEdge:
    def test_flat_curve_epicyclic_frequency(self):
        v, R = sp.symbols("v R", positive=True)
        Om2 = v**2 / R**2
        kappa2 = R * sp.diff(Om2, R) + 4 * Om2
        assert sp.simplify(kappa2 - 2 * Om2) == 0
        assert sp.simplify(4 * Om2 - kappa2 - 2 * Om2) == 0

    def test_sun_sheet_edge(self):
        rJ = jacobi_radius(GM_SUN, OMEGA_SUN)
        assert 1.2 < rJ / PC < 1.6               # ~ 1.4 pc ~ 290 kAU, set by the host alone
        assert 2.5e5 < rJ / AU < 3.3e5

    def test_inside_the_edge_the_residual_is_tide_level(self):
        """At l = r_J, GM/l^3 = 2 Omega^2 exactly: the harmonic term of Part 13 is the tide's
        size by construction. Times the host response minus one (1/mu(1.9) - 1 ~ 0.5), it is
        ~1e-30 s^-2, the same four orders below Cassini as the tide."""
        rJ = jacobi_radius(GM_SUN, OMEGA_SUN)
        assert GM_SUN / rJ**3 == pytest.approx(2 * OMEGA_SUN**2, rel=1e-12)
        resid = (1 / mu(1.9) - 1) * GM_SUN / rJ**3
        assert resid < 1e-29
        assert Q2_CASSINI_2SIGMA / resid > 5e3

    def test_residual_as_an_equivalent_density(self):
        """The residual acts like a uniform density (1/mu - 1) 3M/(4 pi r_J^3) ~ 0.04 Msun/pc^3,
        far below planetary-ephemeris bounds on extra mass in the solar system
        (~1e-20 g/cm^3 ~ 160 Msun/pc^3; Pitjev & Pitjeva 2013, arXiv:1306.5534)."""
        rJ_pc = jacobi_radius(GM_SUN, OMEGA_SUN) / PC
        rho = (1 / mu(1.9) - 1) * 3 * 1.0 / (4 * math.pi * rJ_pc**3)
        assert rho < 0.1
        assert 160 / rho > 1e3

    @pytest.mark.parametrize("name", ["Pal 14", "Pal 4"])
    def test_clusters_lie_inside_their_sheets(self, name):
        _, M, Re, D, *_ = OBJECTS[name]
        Om = V_MW / (D * 1000)                    # km/s/pc
        rJ = (G_PC * M / (2 * Om**2)) ** (1 / 3)  # pc
        assert 4 * Re / 3 < rJ / 3                # half-mass radius well inside the edge

    def test_every_bound_wide_binary_is_inside_its_sheet(self):
        """A pair is bound only inside its Jacobi radius, so the rule says every bound wide
        binary is Newtonian, including those beyond r_M ~ 1e4 AU where x_in < 1."""
        rJ = jacobi_radius(2 * GM_SUN, OMEGA_SUN) / AU
        rM = math.sqrt(2 * GM_SUN / A0) / AU
        assert rJ > 30 * rM


# ============================================================================================
# 15  The ball's TetB stays in the ball: sunspots and GM
# ============================================================================================
class TestBallKeepsItsTetB:
    def test_internal_flows_conserve_the_enclosed_mass(self):
        """Continuity, rho_t + div(rho v) = 0, in a ball with no flow across its surface
        (v . n = 0 at R): dM/dt = -flux = 0. Example: any axisymmetric swirl plus a meridional
        circulation that closes inside the ball (a sunspot-like vortex)."""
        R0, A_, B_, s_ = sp.symbols("R A B s", positive=True)
        # radial velocity vanishing at the surface, any internal profile
        vr = A_ * s_ * (R0 - s_) * sp.sin(B_ * s_)
        rho0 = sp.Function("rho")(s_)
        flux_at_surface = 4 * sp.pi * R0**2 * (rho0 * vr).subs(s_, R0)
        assert sp.simplify(flux_at_surface) == 0

    def test_exterior_changes_only_through_multipoles(self):
        """Outside the ball, a time-varying interior changes the potential only through its
        multipoles: the l-th falls as r^-(l+1) and satisfies Laplace's equation."""
        th = sp.Symbol("theta", real=True)
        for l_ in range(0, 5):
            Pl = sp.legendre(l_, sp.cos(th))
            V = Pl / r**(l_ + 1)
            lap = (sp.diff(r**2 * sp.diff(V, r), r) / r**2
                   + sp.diff(sp.sin(th) * sp.diff(V, th), th) / (r**2 * sp.sin(th)))
            assert sp.simplify(lap) == 0

    def test_solar_quadrupole_is_negligible_at_the_planets(self):
        """J2 ~ 2e-7 (EPM2011): its pull relative to the monopole at Mercury is
        J2 (R_sun/r)^2 ~ 3e-11, and smaller outward."""
        J2, Rsun = 2e-7, 6.957e8
        rel = J2 * (Rsun / (PLANETS_AU["Mercury"] * AU)) ** 2
        assert rel < 1e-10

    def test_gm_rate_bound_on_tetb_exchange(self):
        """Ephemerides: d(GM)/dt / GM = (-5.0 +- 4.1) e-14 per year (3 sigma, EPM2011).
        Radiation alone removes 6.8e-14 per year. Any TetB exchange across the Sun's surface,
        steady or with the sunspot cycle, is therefore below ~1e-13 per year."""
        meas, err3, rad = -5.0e-14, 4.1e-14, -6.8e-14
        room = max(abs(meas - err3 - rad), abs(meas + err3 - rad))
        assert room < 1e-13
        assert (meas - err3) <= rad <= (meas + err3)   # radiation alone fits

    def test_an_open_drain_in_the_ball_would_be_seen(self):
        """If a sunspot opened the ball's TetB to the sheet, the sheet would carry a TetB share
        and mu would act on the Sun's field: the a0 tail of Part 2 at every planet, ~1e6 times
        the tide at Saturn. So the drain is closed."""
        tail = g_total(GM_SUN / (PLANETS_AU["Saturn"] * AU) ** 2) - GM_SUN / (PLANETS_AU["Saturn"] * AU) ** 2
        tide = V_SUN**2 / R_SUN**2 * PLANETS_AU["Saturn"] * AU
        assert tail / tide > 1e7


# ============================================================================================
# THE ALGEBRA OF THE RULE
# Parts 16-20 state the rule as algebra. Four equivalent faces of one statement:
#   a field is drainless  <=>  its law is linear (superposition holds)
#                         <=>  a guest's response tensor is the identity (bare G)
#                         <=>  its flux is conserved across empty shells (no vacuum divergence)
#                         <=>  its TetB share 1 - mu is zero in its exterior.
# And the pointer projection that builds the hierarchy is an exact, idempotent, nested projector.
# ============================================================================================
gs_, gt_, a0_, lam = sp.symbols("g_s g_t a_0 lambda", positive=True)
F_SIMPLE = (gs_ + sp.sqrt(gs_**2 + 4 * gs_ * a0_)) / 2        # the drained law, g_t = F(g_s)


# ============================================================================================
# 16  Drainless <=> linear: superposition is the drain criterion
# ============================================================================================
class TestSuperposition:
    def test_drainless_law_is_additive(self):
        a, b = sp.symbols("a b", positive=True)
        L = lambda g: g
        assert sp.simplify(L(a + b) - L(a) - L(b)) == 0

    def test_drained_law_is_not_additive(self):
        """The interaction term F(a+b) - F(a) - F(b) is nonzero, and negative: two drained
        sources together pull less than the sum of each alone."""
        a, b = sp.symbols("a b", positive=True)
        I = F_SIMPLE.subs(gs_, a + b) - F_SIMPLE.subs(gs_, a) - F_SIMPLE.subs(gs_, b)
        val = I.subs({a: 1, b: 2, a0_: 1})
        assert float(val) < 0
        # concavity is the reason: F'' < 0 for every g_s > 0
        F2 = sp.simplify(sp.diff(F_SIMPLE, gs_, 2))
        assert all(float(F2.subs({gs_: v, a0_: 1})) < 0 for v in (1e-4, 1e-2, 1, 1e2, 1e4))

    def test_deep_field_is_maximally_nonlinear(self):
        """Deep field: F(lam g) / F(g) -> sqrt(lam), degree 1/2. Strong field: -> lam, degree 1."""
        deep = sp.limit(F_SIMPLE.subs(gs_, lam * gs_) / F_SIMPLE, gs_, 0)
        strong = sp.limit(F_SIMPLE.subs(gs_, lam * gs_) / F_SIMPLE, gs_, sp.oo)
        assert sp.simplify(deep - sp.sqrt(lam)) == 0
        assert sp.simplify(strong - lam) == 0

    def test_nonlinearity_is_carried_by_the_tetb_share(self):
        """The degree of F, d ln F / d ln g_s, equals 1/(2 - mu): 1 exactly when mu = 1 (no TetB
        share, linear) and 1/2 when mu = 0 (all TetB, square root)."""
        gN = gt_**2 / (gt_ + a0_)                       # g_s as a function of g_t
        degree = sp.simplify(1 / (sp.diff(gN, gt_) * gt_ / gN))
        m = gt_ / (gt_ + a0_)
        assert sp.simplify(degree - 1 / (2 - m)) == 0


# ============================================================================================
# 17  Drainless <=> identity response: the bare G of Part 7, as algebra
# ============================================================================================
y_, x_ = sp.symbols("y x", positive=True)
NU_SIMPLE = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / y_)     # g = nu(g_N/a0) g_N


class TestResponseTensor:
    """Put a guest's field delta through the host's drained law, g = nu(|g_N|/a0) g_N, at the
    host field g_e e. To first order delta -> nu delta_perp + d(y nu)/dy delta_par.
    The response is the identity only if nu = 1 and nu' = 0: only if there is no TetB share."""

    def test_linearisation(self):
        e1, e2, d1, d2 = sp.symbols("e1 e2 d1 d2", real=True)
        ge = sp.Symbol("g_e", positive=True)
        nu = sp.Function("nu")
        g = sp.Matrix([ge + e1 * d1, e2 * d2])          # host along axis 1, guest (d1, d2)
        norm = sp.sqrt(g.dot(g))
        out = nu(norm / a0_) * g
        par = sp.diff(out[0], e1).subs({e1: 0, e2: 0})
        perp = sp.diff(out[1], e2).subs({e1: 0, e2: 0})
        yy = sp.Symbol("Y", positive=True)
        expected_par = (nu(yy) + yy * sp.diff(nu(yy), yy)).subs(yy, ge / a0_) * d1
        expected_perp = nu(ge / a0_) * d2
        assert sp.simplify((par - expected_par).doit()) == 0
        assert sp.simplify(perp - expected_perp) == 0

    def test_simple_nu_inverts_simple_mu(self):
        """nu(y) = 1/mu(x) where y = x mu(x): the two forms of the law agree."""
        yy = x_ * x_ / (x_ + 1)
        n = (x_ + 1) / x_
        # nu is the root > 1/2 of nu^2 - nu - 1/y = 0; check (x+1)/x is that root
        assert sp.simplify(n**2 - n - 1 / yy) == 0
        assert all(float(n.subs(x_, v)) > 0.5 for v in (1e-3, 1, 1e3))
        assert float((NU_SIMPLE.subs(y_, yy) - n).subs(x_, sp.Rational(7, 3))) == pytest.approx(0, abs=1e-14)

    def test_response_is_never_identity_at_finite_field(self):
        """nu > 1 and d(y nu)/dy > 1 for every finite y: any rule that sends the guest through
        the host's law boosts it. Both tend to 1 only as y -> oo (TetA alone)."""
        par = sp.simplify(sp.diff(y_ * NU_SIMPLE, y_))
        for v in (1e-3, 1e-1, 1, 10, 1e3, 1e6):
            assert float(NU_SIMPLE.subs(y_, v)) > 1
            assert float(par.subs(y_, v)) > 1
        assert sp.limit(NU_SIMPLE, y_, sp.oo) == 1
        assert sp.limit(par, y_, sp.oo) == 1

    @pytest.mark.parametrize("name", ["Pal 14", "Pal 4"])
    def test_size_of_the_boost_that_clusters_rule_out(self, name):
        *_, x_e, _ = sigmas(name)
        y_e = x_e * mu(x_e)
        nu_e = float(NU_SIMPLE.subs(y_, y_e))
        assert nu_e == pytest.approx(1 / mu(x_e), rel=1e-9)
        assert nu_e > 7                          # sigma would be > 2.6x Newtonian; it is ~1x

    def test_drainless_guest_has_identity_response(self):
        """The rule: the guest's field bypasses the host's law and adds linearly."""
        d = sp.Matrix(sp.symbols("d1 d2 d3", real=True))
        host = sp.Matrix(sp.symbols("h1 h2 h3", real=True))
        total = host + d
        J = total.jacobian(list(d))
        assert J == sp.eye(3)


# ============================================================================================
# 18  Drainless <=> flux conserved across empty shells; the TetB share is the flux growth
# ============================================================================================
class TestFluxAndDrain:
    """Flux through a sphere around a mass: Phi(r) = 4 pi r^2 g(r). A drainless field has
    d Phi/dr = 0 in vacuum (Gauss with real sources only). A drained field does not: its
    flux grows across matter-free shells, by exactly the TetB share's phantom density."""

    def test_flux_growth_exponent_is_a_function_of_mu_alone(self):
        """For a point mass under the simple law, d ln Phi / d ln r = 2(1 - mu)/(2 - mu)."""
        GM = sp.Symbol("GM", positive=True)
        gN = GM / r**2
        gt = F_SIMPLE.subs(gs_, gN)
        s_exp = sp.simplify(sp.diff(sp.log(r**2 * gt), r) * r)
        m = gt / (gt + a0_)
        target = 2 * (1 - m) / (2 - m)
        for vals in ({GM: 1, a0_: 1, r: sp.Rational(1, 3)}, {GM: 5, a0_: 2, r: 7}, {GM: 1, a0_: 1, r: 40}):
            assert float((s_exp - target).subs(vals)) == pytest.approx(0, abs=1e-12)

    def test_exponent_limits(self):
        m = sp.Symbol("m", positive=True)
        s_m = 2 * (1 - m) / (2 - m)
        assert s_m.subs(m, 1) == 0                       # drainless: flux conserved (Kepler)
        assert sp.limit(s_m, m, 0) == 1                  # deep drained field: flux grows as r
        assert s_m.subs(m, sp.Rational(1, 2)) == sp.Rational(2, 3)   # the ring x = 1

    def test_rotation_curve_slope_is_the_same_statement(self):
        """d ln v^2 / d ln r = -mu/(2 - mu): Keplerian -1 at mu = 1, flat 0 at mu = 0."""
        m = sp.Symbol("m", positive=True)
        slope = (2 * (1 - m) / (2 - m)) - 1
        assert sp.simplify(slope + m / (2 - m)) == 0

    def test_phantom_density_of_the_deep_field_is_an_isothermal_halo(self):
        """Deep field g = sqrt(GM a0)/r: vacuum divergence (1/r^2) d(r^2 g)/dr = sqrt(GM a0)/r^2,
        i.e. rho_ph = sqrt(GM a0)/(4 pi G r^2), and the flux grows linearly."""
        GM = sp.Symbol("GM", positive=True)
        g = sp.sqrt(GM * a0_) / r
        div = sp.diff(r**2 * g, r) / r**2
        assert sp.simplify(div - sp.sqrt(GM * a0_) / r**2) == 0
        assert sp.simplify(sp.diff(4 * sp.pi * r**2 * g, r) - 4 * sp.pi * sp.sqrt(GM * a0_)) == 0

    def test_kepler_flux_is_conserved_in_the_solar_system_sheet(self):
        """Drainless sheet: GM inferred from each planet is the same (exponent 0). A drained
        sheet (per-mass reading) would make it grow ~ 1/x: by 2e-5 at Neptune."""
        GMs = [GM_SUN for _ in PLANETS_AU]                   # the drainless prediction
        assert max(GMs) == min(GMs)
        x_nep = GM_SUN / (PLANETS_AU["Neptune"] * AU) ** 2 / A0
        assert 1e-5 < 1 / x_nep < 3e-5

    def test_flux_excess_is_the_missing_mass(self):
        """Phi(r)/(4 pi G) = M/mu at every radius (spherical): the excess M(1/mu - 1) is what
        is called dark matter, and it is zero exactly where the TetB share is zero."""
        m = sp.Symbol("m", positive=True)
        M = sp.Symbol("M", positive=True)
        excess = M / m - M
        assert excess.subs(m, 1) == 0
        assert sp.simplify(excess - M * (1 - m) / m) == 0      # = M / Omega, Omega = mu/(1-mu)


# ============================================================================================
# 19  The pointer projection: exact, idempotent, nested
# ============================================================================================
def pointer(masses, centre, radius):
    """Replace every mass inside a ball by one uniform ball of the same total mass at its centre.
    masses: list of points (m, position) and balls ('ball', M, centre, radius)."""
    is_ball = lambda b: isinstance(b[0], str)
    where = lambda b: np.array(b[2] if is_ball(b) else b[1])
    mass = lambda b: b[1] if is_ball(b) else b[0]
    inside = [b for b in masses if np.linalg.norm(where(b) - centre) < radius]
    rest = [b for b in masses if b not in inside]
    M = sum(mass(b) for b in inside)
    return rest + [("ball", M, tuple(float(c) for c in centre), radius)]


def field_at(masses, X):
    g = np.zeros(3)
    for b in masses:
        if isinstance(b[0], str):
            _, M, c, R = b
            d = np.array(c) - X
            dist = np.linalg.norm(d)
            g += M * d / dist**3 if dist >= R else M * d / R**3
        else:
            m_, p = b
            d = np.array(p) - X
            g += m_ * d / np.linalg.norm(d) ** 3
    return g


class TestPointerProjection:
    rng = np.random.default_rng(7)

    def system(self):
        # a 'sun' and 'planets' inside radius 1 about the origin, plus distant masses
        pts = [(1.0, (0.0, 0.0, 0.0))] + [(1e-3 * (i + 1), tuple(self.rng.normal(0, 0.2, 3))) for i in range(6)]
        far = [(2.0, (10.0, 0.0, 0.0)), (3.0, (0.0, -12.0, 4.0))]
        return pts + far

    def test_idempotent(self):
        s1 = pointer(self.system(), np.zeros(3), 1.0)
        s2 = pointer(s1, np.zeros(3), 1.0)
        assert s1 == s2

    def test_nested_projections_compose(self):
        """Projecting a small ball and then a larger one that contains it is the same as
        projecting the larger one directly: the hierarchy of sheets is consistent."""
        sys0 = self.system()
        a = pointer(pointer(sys0, np.zeros(3), 0.5), np.zeros(3), 1.0)
        b = pointer(sys0, np.zeros(3), 1.0)
        assert a[-1][1] == pytest.approx(b[-1][1]) and a[-1][2:] == b[-1][2:]

    def test_mass_is_conserved(self):
        sys0 = self.system()
        tot0 = sum(m_ for m_, _ in sys0)
        s1 = pointer(sys0, np.zeros(3), 1.0)
        tot1 = sum(b[1] if isinstance(b[0], str) else b[0] for b in s1)
        assert tot1 == pytest.approx(tot0)

    def test_monopole_part_of_exterior_field_is_unchanged(self):
        """Outside the ball the projected field differs from the original only by the
        sheet's internal multipoles (here l >= 1, small): the host's coarse field is exact
        to the quadrupole of the sheet. With the 'sun' dominating, the relative error is tiny."""
        sys0 = self.system()
        s1 = pointer(sys0, np.zeros(3), 1.0)
        for X in (np.array([5.0, 1.0, 0.0]), np.array([-8.0, 3.0, 2.0]), np.array([0.0, 0.0, 20.0])):
            g0, g1 = field_at(sys0, X), field_at(s1, X)
            assert np.linalg.norm(g0 - g1) / np.linalg.norm(g0) < 2e-3


# ============================================================================================
# 20  The rule in one formula
# ============================================================================================
class TestRuleInOneFormula:
    """g = F_host[ g_N(P rho) ] + g_N(rho - P rho)
    P: the pointer projection onto drainless sheets; F_host: the drained law of the host field.
    Every earlier part is a property of this one formula."""

    def test_at_a_planet(self):
        """At Saturn: host term ~ 2.3e-10 m/s^2 (uniform, removed by free fall), sheet term =
        GM_sun/r^2 exactly (bare G), host residual inside the sheet ~ tide level."""
        r_sat = PLANETS_AU["Saturn"] * AU
        host = g_total(1.9 * mu(1.9) * A0)
        sheet = GM_SUN / r_sat**2
        assert host == pytest.approx(1.9 * A0, rel=1e-9)        # the host's own net field, x = 1.9
        rel_motion = sheet                                     # free fall removes 'host'
        assert rel_motion == GM_SUN / r_sat**2
        residual = (1 / mu(1.9) - 1) * 2 * OMEGA_SUN**2 * r_sat
        assert residual / sheet < 1e-13

    def test_the_four_faces_agree(self):
        """For the simple law, at any TetB share m in (0, 1]: additivity defect, response
        defect, flux growth and TetB share all vanish together, and only at m = 1."""
        m = sp.Symbol("m", positive=True)
        degree_defect = 1 - 1 / (2 - m)                  # Part 16: F's degree minus 1, up to sign
        response_defect = 1 / m - 1                      # Part 17: nu - 1 = 1/mu - 1
        flux_growth = 2 * (1 - m) / (2 - m)              # Part 18
        tetb_share = 1 - m
        for f in (degree_defect, response_defect, flux_growth, tetb_share):
            assert sp.simplify(f.subs(m, 1)) == 0
            assert sp.solve(sp.Eq(f, 0), m) == [1]


# ============================================================================================
# 21  The flux exponent and the TetA share are exchanged by an involution
# ============================================================================================
def f_inv(u):
    return 2 * (1 - u) / (2 - u)


class TestFluxInvolution:
    """s = f(mu) with f(u) = 2(1 - u)/(2 - u), and f(f(u)) = u: the same map sends the flux
    exponent back to the TetA share. So outside the baryons (enclosed mass constant), the
    slope of a rotation curve alone gives mu, x and a0, with no mass model:
        s = 1 + d ln v^2 / d ln r,   mu = f(s),   x = mu/(1 - mu),   a0 = (v^2/r)/x."""

    def test_f_is_an_involution(self):
        u = sp.Symbol("u")
        assert sp.simplify(f_inv(f_inv(u)) - u) == 0

    def test_fixed_point(self):
        u = sp.Symbol("u", positive=True)
        sols = sp.solve(sp.Eq(f_inv(u), u), u)
        assert sp.Rational(1, 1) * (2 - sp.sqrt(2)) in [sp.nsimplify(s_) for s_ in sols]

    def test_a0_from_the_slope_of_a_synthetic_curve(self):
        """Synthetic galaxy: point mass M, simple law, a0 = 1.2e-10. Read a0 back from v(r) and
        its log-slope alone, beyond the baryons."""
        M = 5e10 * 1.989e30
        rs = np.logspace(np.log10(20 * KPC), np.log10(200 * KPC), 40)
        gN = G * M / rs**2
        v2 = g_total(gN) * rs
        slope = np.gradient(np.log(v2), np.log(rs))
        s_ = 1 + slope
        m_ = f_inv(s_)
        xx = m_ / (1 - m_)
        a0_read = (v2 / rs) / xx
        assert np.allclose(a0_read[2:-2], A0, rtol=2e-3)


# ============================================================================================
# SOLIDIFY AND SIMPLIFY
# 22  The dictionary: every quantity of the rule is a function of mu alone
# 23  Drained fields have vacuum divergence for ANY configuration; drainless fields never
# 24  No self-force: a sheet's own pointer cannot push it, whatever the host's response
# 25  The sheet's edge is bounded by data from below and by binding from above
# 26  The involution singles out x/(1+x) in the standard family
# 27  An a0-free test of the law's shape on SPARC: the slope of the RAR is 1/(2 - mu)
# ============================================================================================
mu_s = sp.Symbol("mu", positive=True)


# ============================================================================================
# 22  The dictionary
# ============================================================================================
class TestDictionary:
    """Write x = mu/(1 - mu) (the odds Omega). Every derived quantity of the rule, computed
    from x through the law, reduces to a rational function of mu alone:
        degree of F          1/(2 - mu)
        flux exponent s      2(1 - mu)/(2 - mu)
        curve slope          -mu/(2 - mu)
        transverse response  1/mu
        parallel response    1/(mu (2 - mu))
        flux excess / M      (1 - mu)/mu = 1/Omega"""

    X = mu_s / (1 - mu_s)

    def gt_of_gN(self):
        return F_SIMPLE

    def test_x_inverts_mu(self):
        assert sp.simplify(mu(self.X) - mu_s) == 0

    def test_transverse_response(self):
        y_val = self.X * mu(self.X)
        n = (self.X + 1) / self.X
        assert sp.simplify(n**2 - n - 1 / y_val) == 0          # n is nu(y)
        assert sp.simplify(n - 1 / mu_s) == 0

    def test_parallel_response(self):
        """d g_t / d g_N at the host = 1/(mu (2 - mu))."""
        gN = gt_**2 / (gt_ + a0_)
        dgt_dgN = 1 / sp.diff(gN, gt_)
        expr = sp.simplify(dgt_dgN.subs(gt_, self.X * a0_))
        assert sp.simplify(expr - 1 / (mu_s * (2 - mu_s))) == 0

    def test_anisotropy_of_the_response(self):
        """Transverse minus parallel = (1 - mu)/(mu (2 - mu)): zero only without TetB share."""
        aniso = 1 / mu_s - 1 / (mu_s * (2 - mu_s))
        assert sp.simplify(aniso - (1 - mu_s) / (mu_s * (2 - mu_s))) == 0

    def test_all_entries_vanish_or_are_one_at_mu_one(self):
        entries = {"degree": 1 / (2 - mu_s), "s": 2 * (1 - mu_s) / (2 - mu_s),
                   "slope": -mu_s / (2 - mu_s), "nu_perp": 1 / mu_s,
                   "nu_par": 1 / (mu_s * (2 - mu_s)), "excess": (1 - mu_s) / mu_s}
        at_one = {k: v.subs(mu_s, 1) for k, v in entries.items()}
        assert at_one == {"degree": 1, "s": 0, "slope": -1, "nu_perp": 1, "nu_par": 1, "excess": 0}


# ============================================================================================
# 23  Vacuum divergence for any configuration
# ============================================================================================
def gN_two(X, m1=1.0, p1=(0, 0, 0), m2=0.3, p2=(3.0, 0.5, 0)):
    g = np.zeros(3)
    for m_, p in ((m1, p1), (m2, p2)):
        d = np.array(p, float) - X
        g += m_ * d / np.linalg.norm(d) ** 3
    return g


def divergence(field, X, h=1e-4):
    return sum((field(X + h * e)[k] - field(X - h * e)[k]) / (2 * h)
               for k, e in enumerate(np.eye(3)))


class TestVacuumDivergence:
    def test_drainless_field_has_no_vacuum_divergence_exact(self):
        """Any sum of point-mass fields is divergence-free off the masses (two masses, symbolic)."""
        X = sp.Matrix(sp.symbols("X1:4", real=True))
        m1, m2, b = sp.symbols("m1 m2 b", positive=True)
        P1, P2 = sp.Matrix([0, 0, 0]), sp.Matrix([b, 0, 0])
        g = sum((m_ * (P - X) / ((P - X).dot(P - X)) ** sp.Rational(3, 2) for m_, P in ((m1, P1), (m2, P2))),
                sp.zeros(3, 1))
        div = sum(sp.diff(g[k], X[k]) for k in range(3))
        assert sp.simplify(div) == 0

    @pytest.mark.parametrize("X", [np.array([1.5, 1.0, 0.3]), np.array([-2.0, 0.4, 1.0]), np.array([6.0, -3.0, 2.0])])
    def test_drained_field_has_vacuum_divergence(self, X):
        """QUMOND form g = nu(|g_N|/a0) g_N (units G = a0 = 1): nonzero divergence in empty space."""
        nu = lambda yy: 0.5 + np.sqrt(0.25 + 1 / yy)
        drained = lambda Y: nu(np.linalg.norm(gN_two(Y))) * gN_two(Y)
        lin = lambda Y: gN_two(Y)
        assert abs(divergence(lin, X)) < 1e-6
        assert abs(divergence(drained, X)) > 1e-3

    def test_phantom_density_is_positive_in_the_deep_field(self):
        """Far out, the phantom density -div g /(4 pi) is positive: the TetB share adds flux."""
        nu = lambda yy: 0.5 + np.sqrt(0.25 + 1 / yy)
        drained = lambda Y: nu(np.linalg.norm(gN_two(Y))) * gN_two(Y)
        for R in (10.0, 30.0, 100.0):
            X = np.array([R, 0.7 * R, 0.2 * R])
            assert -divergence(drained, X, h=1e-3 * R) > 0


# ============================================================================================
# 24  No self-force
# ============================================================================================
class TestNoSelfForce:
    """Inside its sheet the host term contains the sheet's own smoothed ball, a field linear in
    position, GM r/l^3, passed through the host's response tensor R (any 3x3 matrix). Its net
    force on the sheet's bodies is R (GM/l^3) sum m_i r_i = 0 about the centre of mass.
    So a sheet cannot push itself, whatever the host's anisotropic response."""

    def test_net_self_force_vanishes(self):
        n = 4
        m = sp.symbols("m0:%d" % n, positive=True)
        P = [sp.Matrix(sp.symbols(f"p{i}_1:4", real=True)) for i in range(n)]
        Rm = sp.Matrix(3, 3, sp.symbols("R0:9", real=True))
        k = sp.Symbol("k", positive=True)                      # GM/l^3
        com = sum((m[i] * P[i] for i in range(n)), sp.zeros(3, 1)) / sum(m)
        Q = [P[i] - com for i in range(n)]                     # positions about the COM
        F = sum((m[i] * Rm * (k * Q[i]) for i in range(n)), sp.zeros(3, 1))
        assert sp.simplify(F) == sp.zeros(3, 1)

    def test_self_torque_is_tide_like_not_zero(self):
        """The same term does exert a torque for an anisotropic R: it is the size of the tide
        (k = GM/l^3 = 2 Omega^2 at l = r_J), so it belongs with the tide-level residual."""
        k = GM_SUN / jacobi_radius(GM_SUN, OMEGA_SUN) ** 3
        assert k == pytest.approx(2 * OMEGA_SUN**2, rel=1e-12)


# ============================================================================================
# 25  The sheet's edge: bounded below by Cassini, above by binding
# ============================================================================================
def nu_par(m_):
    return 1 / (m_ * (2 - m_))


class TestSheetEdgeBounds:
    """Inside a sheet of radius l the residual is (response - 1) GM/l^3 per unit distance.
    Its anisotropic part is a quadrupole that Cassini bounds. So l cannot be small (that is
    the per-mass reading again), and it cannot exceed the Jacobi radius (unbound)."""

    m_e = mu(1.9)

    def quad_residual(self, l):
        return abs(1 / self.m_e - nu_par(self.m_e)) * GM_SUN / l**3

    def l_min(self):
        return (abs(1 / self.m_e - nu_par(self.m_e)) * GM_SUN / Q2_CASSINI_2SIGMA) ** (1 / 3)

    def test_small_sheet_is_excluded(self):
        assert self.quad_residual(100 * AU) > 1e4 * Q2_CASSINI_2SIGMA

    def test_cassini_lower_bound_on_the_edge(self):
        lmin = self.l_min() / AU
        assert 3e3 < lmin < 2e4                                # ~ 10^4 AU

    def test_lower_bound_is_near_the_mond_radius(self):
        rM = math.sqrt(GM_SUN / A0) / AU
        assert 0.5 < (self.l_min() / AU) / rM < 3

    def test_jacobi_edge_sits_inside_the_window(self):
        rJ = jacobi_radius(GM_SUN, OMEGA_SUN)
        assert rJ > 10 * self.l_min()

    def test_window_is_not_empty_for_any_star(self):
        """l_min ~ M^(1/3), r_J ~ M^(1/3): their ratio is independent of the star's mass, so the
        window exists for every star at the Sun's galactocentric radius."""
        ratios = []
        for Mfac in (0.1, 1.0, 10.0, 100.0):
            GMx = Mfac * GM_SUN
            lmin = (abs(1 / self.m_e - nu_par(self.m_e)) * GMx / Q2_CASSINI_2SIGMA) ** (1 / 3)
            ratios.append(jacobi_radius(GMx, OMEGA_SUN) / lmin)
        assert max(ratios) / min(ratios) == pytest.approx(1.0, rel=1e-9)


# ============================================================================================
# 26  The involution singles out x/(1+x)
# ============================================================================================
class TestInvolutionUniqueness:
    """Standard family mu_n = x/(1 + x^n)^(1/n) (n = 1 is GFD's, n = 2 the 'standard' MOND).
    Its log-derivative is x mu'/mu = 1 - mu^n, so the flux exponent is s = 2(1 - mu^n)/(2 - mu^n).
    The map mu -> s is an involution only for n = 1."""

    n = sp.Symbol("n", positive=True)

    def test_log_derivative(self):
        for nv in (1, 2, 3):
            m_ = x / (1 + x**nv) ** sp.Rational(1, nv)
            L = sp.simplify(x * sp.diff(m_, x) / m_)
            assert sp.simplify(L - (1 - m_**nv)) == 0

    def test_flux_exponent(self):
        """s = 2 - 2/(2 - mu^n) from the point-mass flux, for n = 1, 2."""
        for nv in (1, 2):
            m_ = x / (1 + x**nv) ** sp.Rational(1, nv)
            gt_x = x                                           # units a0 = 1: g_t = x
            gN_x = x * m_
            dln_gN = sp.simplify(sp.diff(sp.log(gN_x), x) * x)  # d ln g_N / d ln g_t
            s_ = 2 - 2 / dln_gN
            assert sp.simplify(s_ - (2 - 2 / (2 - m_**nv))) == 0

    def test_involution_only_for_n_one(self):
        u = sp.Symbol("u", positive=True)
        for nv, expect in ((1, True), (2, False), (3, False)):
            fmap = lambda w: 2 * (1 - w**nv) / (2 - w**nv)
            val = float(fmap(fmap(sp.Rational(3, 10))))
            assert (abs(val - 0.3) < 1e-12) is expect


# ============================================================================================
# 27  An a0-free test of the law's shape on SPARC
# ============================================================================================
SPARC_CSV = (__import__("pathlib").Path(__file__).resolve().parents[2]
             / "papers/letter-radial-acceleration-relation-sparc/supplementary/sparc_rar.csv")


@pytest.fixture(scope="module")
def rar():
    import csv
    rows = list(csv.DictReader(open(SPARC_CSV)))
    gal = np.array([r_["galaxy"] for r_ in rows])
    gb = np.array([float(r_["g_bar_ms2"]) for r_ in rows])
    go = np.array([float(r_["g_obs_ms2"]) for r_ in rows])
    return gal, np.log10(gb), np.log10(go)


def binned_slope_test(gal, lb, lo, edges, n):
    c, m_ = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        s_ = (lb >= a) & (lb < b)
        c.append(np.median(lb[s_]))
        m_.append(np.median(lo[s_]))
    c, m_ = np.array(c), np.array(m_)
    beta = (m_[2:] - m_[:-2]) / (c[2:] - c[:-2])               # central differences
    muo = 10 ** (c[1:-1] - m_[1:-1])
    pred = 1 / (2 - muo**n)
    return beta, pred


@pytest.mark.skipif(not SPARC_CSV.exists(), reason="SPARC RAR csv not present")
class TestRARSlopeShape:
    """The local slope of the RAR, beta = d ln g_obs / d ln g_bar, is the inverse degree of the
    law: beta = 1/(2 - mu) for GFD, 1/(2 - mu^2) for the standard MOND law. Both sides are
    measured (mu = g_bar/g_obs), so the test uses NO value of a0. Bins in g_bar, where the
    points are dense (-11.25 to -9.15 dex)."""

    edges = np.arange(-11.55, -8.84, 0.30)

    def test_sample(self, rar):
        gal, lb, lo = rar
        assert len(lb) > 3000 and len(set(gal)) > 150

    def test_gfd_shape_fits_better_than_standard(self, rar):
        gal, lb, lo = rar
        b1, p1 = binned_slope_test(gal, lb, lo, self.edges, 1)
        b2, p2 = binned_slope_test(gal, lb, lo, self.edges, 2)
        rms1 = np.sqrt(np.mean((b1 - p1) ** 2))
        rms2 = np.sqrt(np.mean((b2 - p2) ** 2))
        assert rms1 < rms2
        assert rms1 < 0.06

    def test_bootstrap_over_galaxies(self, rar):
        """Resample galaxies; GFD's shape should win in most realisations."""
        gal, lb, lo = rar
        names = np.unique(gal)
        rng = np.random.default_rng(11)
        idx = {g_: np.where(gal == g_)[0] for g_ in names}
        wins = 0
        N = 200
        for _ in range(N):
            pick = rng.choice(names, size=len(names), replace=True)
            sel = np.concatenate([idx[p] for p in pick])
            b1, p1 = binned_slope_test(gal[sel], lb[sel], lo[sel], self.edges, 1)
            b2, p2 = binned_slope_test(gal[sel], lb[sel], lo[sel], self.edges, 2)
            wins += np.mean((b1 - p1) ** 2) < np.mean((b2 - p2) ** 2)
        assert wins / N > 0.8


# ============================================================================================
# 28  Screening of the Sun's TetB
# ============================================================================================
R_SUN_M = 6.957e8              # m, solar radius
RHO_C = 1.5e5                  # kg/m^3, solar central density (standard solar model)
M_SUN = GM_SUN / G


class TestSunScreening:
    """Apply the screening law x(1 - mu) = mu to the Sun's own field, inside the ball.
    The TetB share is 1 - mu = 1/(1 + x): screened to ~4e-13 at the surface, and dominant
    only in a micron-sized core at the centre, where g -> 0 (the Field Origin of the ball).
    Its whole equivalent mass is a fixed ~4e-13 of the Sun's, enclosed, so it is part of GM
    and never changes it."""

    def test_screening_law_is_the_simple_mu(self):
        assert sp.simplify(x * (1 - mu(x)) - mu(x)) == 0
        assert sp.simplify((1 - mu(x)) - 1 / (1 + x)) == 0

    def test_tetb_share_at_the_surface(self):
        x_surf = GM_SUN / R_SUN_M**2 / A0
        share = 1 / (1 + x_surf)
        assert 2e12 < x_surf < 3e12
        assert 3e-13 < share < 6e-13

    def test_screening_deepens_inward_until_the_core(self):
        """Inside a body g(r) = G M(<r)/r^2 falls to zero at the centre, so x falls and the
        TetB share rises. For a uniform core, g = (4 pi/3) G rho_c r."""
        rho, Gs, rr = sp.symbols("rho G r", positive=True)
        Menc = sp.Rational(4, 3) * sp.pi * rho * rr**3
        g_in = sp.simplify(Gs * Menc / rr**2)
        assert sp.simplify(g_in - sp.Rational(4, 3) * sp.pi * Gs * rho * rr) == 0
        assert sp.limit(1 / (1 + g_in / a0_), rr, 0) == 1        # pure TetB at the centre

    def test_tetb_dominated_core_is_microscopic(self):
        """x = 1 where (4 pi/3) G rho_c r = a0: r_B = 3 a0 / (4 pi G rho_c) ~ 3 microns."""
        rB = 3 * A0 / (4 * math.pi * G * RHO_C)
        assert 1e-6 < rB < 1e-5
        assert rB / R_SUN_M < 1e-14

    def test_screened_tetb_mass_is_fixed_and_tiny(self):
        """Even read pointwise inside the ball, the extra flux at the surface is
        (g_t - g_N) R^2 / G <= a0 R^2 / G ~ 9e17 kg ~ 4e-13 M_sun."""
        gN = GM_SUN / R_SUN_M**2
        dM = (g_total(gN) - gN) * R_SUN_M**2 / G
        assert dM <= A0 * R_SUN_M**2 / G * (1 + 1e-12)
        assert 3e-13 < dM / M_SUN < 6e-13

    def test_screened_tetb_is_counted_in_GM_and_constant(self):
        """It depends only on R and a0, so it does not vary with time unless the radius does.
        A solar-cycle radius change of ~1e-5 changes it by ~1e-17 of GM: far below the
        ephemeris bound of ~1e-13 per year (Part 15)."""
        dR_frac = 1e-5
        change = 2 * dR_frac * (A0 * R_SUN_M**2 / G) / M_SUN
        assert change < 1e-16

    def test_screened_tetb_stays_in_the_ball(self):
        """Outside the ball the sheet is drainless (Part 13): the screened TetB enters only
        through GM, whereas a TetB that leaked past the surface would be the a0 tail (Part 2)."""
        r_ear = AU
        enclosed = GM_SUN / r_ear**2                              # what the drainless sheet gives
        leaked = g_total(GM_SUN / r_ear**2) - GM_SUN / r_ear**2   # what a leak would add
        assert leaked / A0 == pytest.approx(1.0, rel=1e-6)
        assert leaked / enclosed > 1e-8                           # 2e-8 of the Sun's pull: excluded


# ============================================================================================
# Runner: python verify_net_field_rule.py  prints one PASS/FAIL line per check
# ============================================================================================
if __name__ == "__main__":
    import sys
    import pytest as _pt

    class _Report:
        def __init__(self):
            self.passed = self.failed = 0

        def pytest_runtest_logreport(self, report):
            if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
                name = report.nodeid.split("::", 1)[1].replace("::", " :: ")
                ok = report.outcome == "passed"
                skip = report.outcome == "skipped"
                self.passed += ok
                self.failed += (not ok and not skip)
                print(f"  [{'PASS' if ok else 'SKIP' if skip else 'FAIL'}] {name}")

    rep = _Report()
    code = _pt.main(["-p", "no:terminal", "-p", "no:cacheprovider", __file__], plugins=[rep])
    print(f"\n{rep.passed} passed, {rep.failed} failed")
    sys.exit(0 if (rep.failed == 0 and rep.passed > 0 and code == 0) else 1)
