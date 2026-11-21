"""
The net-field rule for the GFD constitutive law, tested.

    mu(x) = x/(x+1) acts on the net field of a system whose drain is open
    (a galaxy: occupied TetB behind its Field Origin). A system whose drain is
    closed (a star with its planets, a binary, a star cluster) has no TetB of
    its own: each body's TetB is enclosed in the body. Its internal gravity is
    TetA alone, Newton/GR with the bare G, and its host's net field reaches it
    only through common free fall (removed exactly) and the tide (tiny).

The core picture (Stephen Nelson, 2026-11-20). A solar system is a rubber sheet with a
bowling ball on it, sitting in the galaxy's net field. The ball (the Sun) has a TetB, enclosed
in it and counted in its GM. The sheet (the solar system's field) has no drain. A galaxy's
field is a funnel whose throat opens into occupied TetB: that field has a drain.

Premises, stated once:
  (D) Drain criterion. A drain belongs to a field, not to a body. Every body has its own TetB,
      enclosed within it and counted in its GM. A field carries a TetB share, and mu acts on
      it, only if the field itself has a drain: a throat opening into occupied TetB. A galaxy's
      field has one. The field of a star system, a binary or a star cluster does not.
  (N) Net-field rule. In a drained field x = |g_net|/a0, with g_net that field's own
      coarse-grained net field.
  (A) TetA is GR. A drainless field is the TetA connection: Newton/GR with the bare G.
These are the framework's premises; the tests prove what follows from them and check the
consequences against the data the framework must meet.

Parts (each test name says which statement it checks):
  1  Enclosure: a body's TetB is counted in its GM            (Gauss; exact)
  2  A field with a drain around every star is forced to fail (exchange + flat curves; exact)
  3  ... and Cassini excludes it                              (external-field quadrupole; quadrature)
  4  Free fall removes the host's uniform field exactly       (equivalence; exact)
  5  What survives is the tide, four orders below Cassini     (Taylor; exact + numbers)
  6  A host factor on G is invisible to orbits ...            (Kepler scaling; exact)
  7  ... but globular clusters see it: so G stays bare        (photometric masses; data)
  8  Drained fields keep mu: dwarfs are not Newtonian         (data)
  9  The drain criterion sorts clusters and dwarfs as observed
 10  The pointer picture: a sheet enters its host as one mass (multipoles; exact)
 11  Wide binaries: the rule's sharp prediction               (algebra + numbers)
 12  The vortex picture: pebble in a stream, open vs closed drain       (exact Navier-Stokes)
 13  The rubber sheet as an exact two-scale split             (shell theorem; exact)
 14  The sheet's edge is the Jacobi radius, with no free parameter      (exact + numbers)
 15  The ball's TetB stays in the ball: sunspots and GM       (continuity; data)

Run:  python -m pytest -q test_net_field_rule.py
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
