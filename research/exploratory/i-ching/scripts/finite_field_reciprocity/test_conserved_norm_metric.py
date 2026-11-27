"""Tests for WORK_METRIC_FROM_THE_CONSERVED_NORM.md.

Run from this folder:  python -m pytest -q test_conserved_norm_metric.py
Self-contained: builds the hexagram register, Walsh read, XOR read, exchange
and shared zone directly, without importing the other suites.
"""
import itertools as it
import numpy as np
import pytest
from scipy.linalg import expm

V = range(8)
dot = lambda a, b: bin(a & b).count("1") % 2
X = [(a, b) for a in V for b in V]
IX = {x: i for i, x in enumerate(X)}
I64 = np.eye(64)


def perm(f):
    P = np.zeros((64, 64))
    for x in X:
        P[IX[f(x)], IX[x]] = 1
    return P


W = np.array([[(-1) ** ((dot(x[0], y[1]) + dot(x[1], y[0])) % 2) for y in X] for x in X]) / 8.0
H2 = np.array([[1, 1], [1, -1]])
W_ord = H2
for _ in range(5):
    W_ord = np.kron(W_ord, H2)
W_ord = W_ord / 8.0
R = perm(lambda x: (x[1], x[0] ^ x[1]))
J = perm(lambda x: (x[1], x[0]))
ORBITS = {frozenset({x, (x[1], x[0] ^ x[1]), (x[0] ^ x[1], x[0])}) for x in X}
HB = np.array([[1.0 if x in o else 0.0 for x in X] for o in ORBITS]).T
HB /= np.linalg.norm(HB, axis=0)
PH = HB @ HB.T                                  # R-invariant register (22)
f = np.array([(x[0] == 0) + (x[1] == 0) + (x[0] == x[1]) for x in X], float)
F = np.outer(f, f) / (f @ f)                    # the common line
H0 = PH - F                                     # the 21 contrast directions
E_even, E_odd = (I64 + J) / 2, (I64 - J) / 2


def shared(u):
    L = {0, u}
    return PH @ np.diag([1.0 if (x[0] in L or x[1] in L or (x[0] ^ x[1]) in L) else 0.0
                         for x in X]) @ PH


def S(u):                                       # orientation operator on the 21
    Q = shared(u)
    return (Q + (PH - Q) @ J) @ H0


tr = lambda M: float(np.trace(M))
rng = np.random.default_rng(26)


# ------------------------------------------------------------------ 1. the flat-read theorem
def test_walsh_reads_are_orthogonal_and_flat():
    for M in (W, W_ord):
        assert np.allclose(M @ M.T, I64)
        assert np.allclose(M ** 2, 1 / 64)      # every coefficient sees every record at weight 1/64


@pytest.mark.parametrize("M", [W, W_ord])
def test_diagonal_of_read_conjugate_is_the_mean(M):
    for _ in range(5):
        h = rng.uniform(0.2, 3.0, 64)
        assert np.allclose(np.diag(M @ np.diag(h) @ M.T), h.mean())


@pytest.mark.parametrize("M", [W, W_ord])
def test_diagonal_read_invariant_metric_is_scalar(M):
    # W diag(h) W^T = diag(h) forces h constant; any non-constant diagonal h is moved
    for _ in range(5):
        h = rng.uniform(0.2, 3.0, 64)
        moved = M @ np.diag(h) @ M.T
        assert not np.allclose(moved, np.diag(h))
    assert np.allclose(M @ (2.5 * I64) @ M.T, 2.5 * I64)


def test_xor_read_alone_does_not_force_scalar():
    # R is a permutation: a diagonal metric constant on R-orbits but not globally is R-invariant
    h = np.zeros(64)
    for k, o in enumerate(sorted(ORBITS, key=lambda o: min(IX[x] for x in o))):
        for x in o:
            h[IX[x]] = 1.0 + k
    Hm = np.diag(h)
    assert np.allclose(R @ Hm @ R.T, Hm)
    assert not np.allclose(Hm, Hm[0, 0] * I64)


# ------------------------------------------------------------------ 2. the two-weight family is not record-diagonal
def test_unequal_two_weight_metric_has_cross_record_terms():
    for a, b in [(1.0, 2.0), (3.0, 1.0)]:
        Hm = a * E_even + b * E_odd
        assert np.allclose(W @ Hm @ W.T, Hm)    # read-invariant ...
        off = Hm - np.diag(np.diag(Hm))
        assert np.abs(off).max() > 0            # ... but couples (a,b) with (b,a)
    Hm = 1.7 * E_even + 1.7 * E_odd
    assert np.allclose(Hm, 1.7 * I64)


@pytest.mark.parametrize("a,b", [(1.0, 1.0), (1.0, 2.0), (2.0, 1.0)])
def test_weighted_counts(a, b):
    Hm = a * E_even + b * E_odd
    for u in range(1, 8):
        Su = S(u)
        P0 = (H0 + Su) / 2
        Q0 = shared(u) - F
        assert np.isclose(tr(Hm @ P0), 14 * a + 3 * b)
        assert np.isclose(tr(Hm @ Su), 14 * a - b)
        assert np.isclose(tr(Hm @ Q0), 10 * a + 3 * b)


# ------------------------------------------------------------------ 3. the conserved norm gives 17/13 on every axis
@pytest.mark.parametrize("u", range(1, 8))
def test_scalar_metric_gives_seventeen_over_thirteen(u):
    c = 1.9
    Su = S(u)
    P0 = (H0 + Su) / 2
    Q0 = shared(u) - F
    assert np.isclose(tr(c * H0), c * 21)
    assert np.isclose(tr(c * P0), c * 17)
    assert np.isclose(tr(c * Su), c * 13)
    assert np.isclose(tr(c * P0) / tr(c * Su), 17 / 13)
    assert np.isclose(tr(c * P0) / tr(c * Q0), 17 / 13)


# ------------------------------------------------------------------ 4. the native dynamics conserves exactly the Euclidean norm
def test_hermitian_nonlinear_flow_conserves_euclidean_norm():
    n = 12
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    Hb = (A + A.conj().T) / 2
    Cv = rng.normal(size=(n // 2, n // 2))
    Vm = np.block([[np.zeros((n // 2, n // 2)), Cv], [Cv.T, np.zeros((n // 2, n // 2))]])
    psi = rng.normal(size=n) + 1j * rng.normal(size=n)
    psi /= np.linalg.norm(psi)
    g = lambda u: u / (1 + abs(u))              # a real, state-dependent gain, as in the vertex law
    NA0 = np.linalg.norm(psi[: n // 2]) ** 2
    for _ in range(200):
        u = float(np.real(psi.conj() @ Vm @ psi)) / 2
        psi = expm(-1j * 0.01 * (Hb + g(u) * Vm)) @ psi
    assert np.isclose(np.linalg.norm(psi), 1.0)                       # total norm conserved
    NA, NB = np.linalg.norm(psi[: n // 2]) ** 2, np.linalg.norm(psi[n // 2:]) ** 2
    assert np.isclose(NA + NB, 1.0) and not np.isclose(NA, NA0)       # occupation is exchanged in it


def test_energy_metric_is_not_record_diagonal():
    # a quadratic energy with cross-record coupling is a non-diagonal metric: the theorem
    # does not apply to it, so the registered quantity must be the conserved occupation
    n = 8
    Cv = rng.normal(size=(n // 2, n // 2))
    E = np.eye(n) + 0.3 * np.block([[np.zeros((4, 4)), Cv], [Cv.T, np.zeros((4, 4))]])
    assert np.abs(E - np.diag(np.diag(E))).max() > 0
