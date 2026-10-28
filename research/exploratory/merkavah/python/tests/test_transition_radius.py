import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import transition_radius as tr  # noqa: E402


def test_field_origin_state_at_transition_radius():
    for m in (tr.M_E, 70.0, tr.M_SUN):
        r = tr.transition_radius(m)
        x = tr.G * m / r ** 2 / tr.A0
        assert math.isclose(x, 1.0, rel_tol=1e-12)
        assert math.isclose(tr.mu(x), 0.5, rel_tol=1e-12)


def test_square_root_mass_scaling():
    r1, r2 = tr.transition_radius(1.0), tr.transition_radius(100.0)
    assert math.isclose(r2 / r1, 10.0, rel_tol=1e-12)


def test_human_chariot_radius():
    assert 6.2 < tr.transition_radius(70.0) < 6.3


def test_electron_transition_radius_is_re_over_K_with_derived_a0():
    a0_e = tr.K ** 2 * tr.G * tr.M_E / tr.R_E ** 2
    r = tr.transition_radius(tr.M_E, a0=a0_e)
    assert math.isclose(r, tr.R_E / tr.K, rel_tol=1e-12)


def test_electron_and_galaxy_span_their_own_field_origin():
    spans = {name for name, m, r in tr.BODIES if tr.transition_radius(m) < r}
    assert spans == {"electron", "Milky Way baryons"}
