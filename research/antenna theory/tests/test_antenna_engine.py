"""Tests for antenna_engine. They check stated identities and the behaviour of
the stated finite model; they are not evidence that the model is physical."""
import sys
from fractions import Fraction
from math import comb
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import antenna_engine as ae  # noqa: E402


# --- Part 1: Sierpinski bookkeeping -------------------------------------

@pytest.mark.parametrize("n", range(6))
def test_gasket_vs_ledger_counts(n):
    assert ae.gasket_triangles(n) == 3 ** n
    assert ae.ledger_addresses(n) == 4 ** n
    assert ae.ledger_addresses(n) - ae.gasket_triangles(n) == 4 ** n - 3 ** n


def test_constructions_differ_beyond_level_zero():
    assert all(ae.gasket_triangles(n) < ae.ledger_addresses(n) for n in range(1, 6))


@pytest.mark.parametrize("n", range(6))
def test_area_and_edge(n):
    assert ae.gasket_area(n) == Fraction(3, 4) ** n
    assert ae.edge_fraction(n) == Fraction(1, 2) ** n


def test_band_ratio_is_two():
    assert ae.band_ratio() == 2


def test_band_ladder_dyadic():
    assert np.allclose(ae.band_ladder(), [1, 2, 4, 8])
    assert ae.band_ladder()[-1] / ae.band_ladder()[0] == 2 ** ae.D


def test_gate_depth_counts():
    c = ae.gate_depth_counts()
    assert c == [27, 27, 9, 1]
    assert sum(c) == ae.K ** ae.D == 64


@pytest.mark.parametrize("depth", range(1, 7))
def test_gate_depth_binomial_sum(depth):
    assert sum(ae.gate_depth_counts(depth)) == 4 ** depth


@pytest.mark.parametrize("n", range(1, 7))
def test_gasket_site_count(n):
    # Pascal mod 2 over 2^n rows has 3^n odd entries
    assert len(ae.gasket_points(n)) == 3 ** n


@pytest.mark.parametrize("n", range(1, 7))
def test_self_similar_about_feed(n):
    assert ae.self_similar_about_feed(n)


def test_octahedron_has_twelve_edges():
    # audit of legacy "9 edges": regular octahedron V-E+F = 2 with V=6, F=8
    V, F = 6, 8
    E = V + F - 2
    assert E == 12 and E != 9


# --- Part 2: vertex model -----------------------------------------------

def test_no_direct_chamber_edge():
    A = ae.adjacency(ae.Vertex())
    assert A[0, 2] == 0 and A[2, 0] == 0
    assert A[0, 1] == A[1, 2] == 1


def test_only_path_runs_through_origin():
    # remove the origin: A and B become disconnected
    A = ae.adjacency(ae.Vertex())
    sub = A[np.ix_([0, 2], [0, 2])]
    assert not sub.any()


def test_without_vertex_no_exchange():
    v = ae.Vertex(g=0.0)
    y = ae.evolve_linear_exact(v, [1, 0, 0], np.linspace(0, 50, 101))
    assert np.max(np.abs(y[2])) == 0.0


@pytest.mark.parametrize("g", [0.3, 1.0, 2.5])
def test_symmetric_closed_form(g):
    ts = np.linspace(0, 10, 41)
    y = ae.evolve_linear_exact(ae.Vertex(g=g), [1, 0, 0], ts)
    a, o, b = ae.symmetric_transfer_exact(g, ts)
    assert np.allclose(y[0], a, atol=1e-12)
    assert np.allclose(y[1], o, atol=1e-12)
    assert np.allclose(y[2], b, atol=1e-12)


def test_symmetric_complete_transfer_time():
    g = 1.0
    t = np.pi / (np.sqrt(2) * g)
    _, o, b = ae.symmetric_transfer_exact(g, t)
    assert abs(abs(b) ** 2 - 1) < 1e-12 and abs(o) < 1e-12


def test_rk4_matches_exact_linear():
    v = ae.Vertex(g=0.8, wA=0.1, wB=-0.2, wO=0.3)
    t, y = ae.evolve(v, [1, 0, 0], 5.0, 1e-3)
    ye = ae.evolve_linear_exact(v, [1, 0, 0], t[::500])
    assert np.allclose(y[:, ::500], ye, atol=1e-8)


def _dispersive(delta_B=0.0, g=0.1, dO=2.0):
    v = ae.Vertex(g=g, wO=dO, wB=delta_B)
    ts = np.linspace(0, 800, 20001)
    return ae.evolve_linear_exact(v, [1, 0, 0], ts), ts


def test_dispersive_full_exchange_with_empty_origin():
    y, _ = _dispersive()
    assert np.max(np.abs(y[2]) ** 2) > 0.999
    assert np.max(np.abs(y[1]) ** 2) < 0.011


def test_dispersive_period_matches_effective_coupling():
    y, ts = _dispersive()
    J = ae.effective_exchange(0.1, 2.0)
    t_peak = ts[np.argmax(np.abs(y[2]))]
    assert abs(t_peak - np.pi / (2 * abs(J))) / (np.pi / (2 * abs(J))) < 0.02


@pytest.mark.parametrize("delta", [0.0, 0.005, 0.01, 0.02, 0.04])
def test_detuning_selection_matches_rabi(delta):
    y, _ = _dispersive(delta_B=delta)
    J = ae.effective_exchange(0.1, 2.0)
    assert abs(np.max(np.abs(y[2]) ** 2) - ae.rabi_max_transfer(J, delta)) < 0.01


def test_matched_ladders_exchange_every_band():
    assert np.all(ae.multiband_transfer(1.0) > 0.999)


@pytest.mark.parametrize("s", [1.1, 0.9, 1.5])
def test_mismatched_ladder_suppresses_exchange(s):
    assert np.all(ae.multiband_transfer(s) < 0.05)


@pytest.mark.parametrize("chi", [0.0, 1.0, 4.0])
def test_norm_conserved(chi):
    t, y = ae.evolve(ae.Vertex(g=1, chi=chi), [2.0, 0, 0], 20.0, 2e-3)
    assert abs(np.sum(np.abs(y[:, -1]) ** 2) - 4.0) < 1e-8


def test_time_reversible():
    v = ae.Vertex(g=1, chi=2.0, wA=0.1, wB=-0.1)
    _, y = ae.evolve(v, [1.5, 0, 0], 10.0, 1e-3)
    # conjugate-and-evolve reverses the Hamiltonian flow
    _, back = ae.evolve(v, np.conj(y[:, -1]), 10.0, 1e-3)
    assert np.allclose(np.conj(back[:, -1]), [1.5, 0, 0], atol=1e-6)


def test_nonlinear_reduces_to_linear_at_small_amplitude():
    v = ae.Vertex(g=1, chi=1.0)
    t, y = ae.evolve(v, [1e-3, 0, 0], 5.0, 1e-3)
    _, _, b = ae.symmetric_transfer_exact(1.0, t)
    assert np.allclose(y[2] / 1e-3, b, atol=1e-5)


def _peaks(N, chi=1.0, t_end=60.0):
    t, y = ae.evolve(ae.Vertex(g=1, chi=chi), [np.sqrt(N), 0, 0], t_end, 2e-3)
    return np.max(np.abs(y[2]) ** 2) / N, np.max(np.abs(y[1]) ** 2) / N


@pytest.mark.parametrize("N", [4, 16, 64])
def test_nonlinear_vertex_still_completes_exchange(N):
    # quasi-periodic: allow a long enough window for the exchange to complete
    fb, _ = _peaks(N, t_end=120.0)
    assert fb > 0.99


def test_nonlinear_vertex_share_falls_with_inventory():
    shares = [_peaks(N)[1] for N in (4, 16, 64)]
    assert shares[0] > shares[1] > shares[2]
    assert shares[2] < 0.5 * _peaks(0.01)[1]
