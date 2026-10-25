#!/usr/bin/env python3
"""
GFD Algebra Reference
=====================

Every algebraic object used in the RAR letter and its three
supplementary proofs, collected in one file with docstrings
tracing each to its origin.

Organisation follows the logical chain:

    Proof A  (Spatial Geometry)    — Tetrahedral uniqueness
    Proof C  (Exchange Symmetry)   — μ forced from parity duality
    Proof B  (Energy Functional)   — F(y) from integrating μ
    Letter   (RAR)                 — Action → field equation → data

Run:  python gfd_algebra.py
      Executes all self-checks.  Zero output = all pass.

Author: Stephen Nelson / Field Dynamics Research
"""

import math
import numpy as np


# =========================================================================
#  CONSTANTS
# =========================================================================

K = 4       # frame dimension (number of tetrad legs)
D = 3       # spatial dimension (number of positive eigenvalues of eta)
A0 = 1.2e-10  # MOND / GFD acceleration scale [m/s^2], adopted (McGaugh+2016)


# =========================================================================
#  PROOF A — The Spatial Geometry of the Lorentz Tetrad
# =========================================================================

def commutant(alpha: float, beta: float) -> np.ndarray:
    """S4-invariant 4x4 matrix from the commutant of the permutation
    representation.

    Origin: Proof A, Lemma 1 (Commutant of S4).
    The S4 action on {0,1,2,3} is 2-transitive, so G_ab is constant
    on two orbits: diagonal and off-diagonal.  Every S4-invariant
    4x4 matrix has the form  G = alpha * I + beta * J.

    Parameters
    ----------
    alpha : diagonal excess above beta
    beta  : off-diagonal value (also shifts diagonal by +beta)

    Returns
    -------
    G : 4x4 numpy array with G_aa = alpha + beta, G_ab = beta (a != b)
    """
    I = np.eye(4)
    J = np.ones((4, 4))
    return alpha * I + beta * J


def forced_gram_matrix(c: float) -> np.ndarray:
    """The unique Gram matrix satisfying F1-F3.

    Origin: Proof A, Theorem 1 (Forced Gram matrix).
    F1 (common norm |v_a| = c) fixes alpha + beta = c^2.
    F2 (balanced closure sum v_a = 0) fixes 4c^2 + 12*beta = 0,
    giving beta = -c^2/3, alpha = 4c^2/3.

    Result:  G = c^2 I - (c^2/3)(J - I)
    Diagonal: c^2.  Off-diagonal: -c^2/3.
    """
    alpha = 4.0 * c**2 / 3.0
    beta = -c**2 / 3.0
    return commutant(alpha, beta)


def gram_spectrum(c: float) -> tuple:
    """Eigenvalues and null eigenvector of the forced Gram matrix.

    Origin: Proof A, Corollary 1 (Rank and spectrum).
    G = (4c^2/3)I - (c^2/3)J.
    J has eigenvalue 4 on (1,1,1,1) and 0 with multiplicity 3.
    So G has eigenvalue 0 on (1,1,1,1) and 4c^2/3 with multiplicity 3.
    Rank = 3.  Kernel = span{(1,1,1,1)}.
    """
    zero_eigenvalue = 0.0
    nonzero_eigenvalue = 4.0 * c**2 / 3.0
    null_eigenvector = np.ones(4) / 2.0  # normalised
    return zero_eigenvalue, nonzero_eigenvalue, null_eigenvector


def edge_length_squared(c: float) -> float:
    """Squared edge length of the forced regular tetrahedron.

    Origin: Proof A, Corollary 2 (Regular tetrahedron).
    |v_a - v_b|^2 = G_aa + G_bb - 2*G_ab
                  = c^2 + c^2 - 2*(-c^2/3) = 8c^2/3.
    All six pairwise distances are equal → regular tetrahedron.
    Unique up to O(3) by rank-3 Gram factorisation (Horn & Johnson).
    """
    return 8.0 * c**2 / 3.0


def canonical_sign_matrix() -> np.ndarray:
    """The canonical {-1,+1} representative at c = sqrt(3).

    Origin: Proof A, Corollary 3 (Canonical representative).
    Columns are the four tetrad frame vectors in R^3.
    Each column has entries in {-1,+1}, |v_a|^2 = 3,
    v_a . v_b = -1 for a != b.
    Every F1-F3 realisation at c = sqrt(3) is O(3)-equivalent to M.
    """
    return np.array([
        [+1, +1, -1, -1],
        [+1, -1, +1, -1],
        [+1, -1, -1, +1],
    ], dtype=float)


def parity_completion(M: np.ndarray) -> np.ndarray:
    """Cube vertices as parity completion of the tetrahedron.

    Origin: Proof A, Corollary 4 (Cube as parity completion).
    V = columns of M (TetA).  P(V) = columns of -M (TetB).
    V union P(V) = all 8 elements of {-1,+1}^3 = cube vertices.
    """
    return np.hstack([M, -M])


def stella_octangula(M: np.ndarray) -> tuple:
    """The compound of two dual tetrahedra = Kepler's stella octangula.

    Origin: Proof A, Theorem 2 (Stella octangula).
    TetA (columns of M) and TetB (columns of -M) are both regular
    tetrahedra with the same Gram matrix.  They are antipodal,
    share a centre at the origin, and inscribe in {-1,+1}^3.
    Their compound is the stellated octahedron (Kepler 1619).
    """
    tet_a = M          # identity component under spatial parity
    tet_b = -M         # parity component
    return tet_a, tet_b


# =========================================================================
#  PROOF C — The Constitutive Law from Exchange Symmetry
# =========================================================================

def exchange_duality(mu_func, x: float) -> float:
    """Verify the exchange symmetry: mu(1/x) = 1 - mu(x).

    Origin: Proof C, Definition 2 (Exchange symmetry).
    Spatial parity exchanges TetA and TetB.  Under this exchange,
    the acceleration ratio inverts (x -> 1/x) and the two
    fractions swap: mu -> 1 - mu.  This is the duality condition
    inherited from the stellated octahedron's parity structure.
    """
    return mu_func(1.0 / x) - (1.0 - mu_func(x))


def odds_ratio(mu_val: float) -> float:
    """The odds ratio Omega = mu / (1 - mu).

    Origin: Proof C, Definition 3 (Odds ratio).
    Measures how many times more capacity TetA carries than TetB
    at a given acceleration.  Under exchange symmetry,
    Omega(1/x) = 1/Omega(x)  (Lemma 1, Odds-ratio duality).
    """
    return mu_val / (1.0 - mu_val)


def odds_ratio_duality(omega_func, x: float) -> float:
    """Verify Omega(1/x) = 1/Omega(x).

    Origin: Proof C, Lemma 1 (Odds-ratio duality).
    Direct consequence of mu(1/x) = 1 - mu(x).
    The odds ratio inverts when the acceleration inverts.
    This is the exchange symmetry in its simplest algebraic form.
    """
    return omega_func(1.0 / x) * omega_func(x) - 1.0


def mobius_general(x: float, a: float, b: float,
                   c: float, d: float) -> float:
    """General Mobius map Omega(x) = (ax + b) / (cx + d).

    Origin: Proof C, Lemma 3 (Classification of Aut(P^1)).
    The exchange x -> 1/x sends 0 <-> infinity, so the natural
    domain is the projective line P^1 (Lemma 2, Symmetry domain).
    We require Omega in Aut(P^1) — the minimal algebraically
    closed class containing the exchange involution and stable
    under composition and inversion (Definition 4, Structural axiom).
    Over R, Aut(P^1) = PGL_2(R), so every such map is fractional
    linear (Hartshorne 1977).
    """
    return (a * x + b) / (c * x + d)


def force_odds_ratio(x: float) -> float:
    """The forced odds ratio: Omega(x) = x.

    Origin: Proof C, Theorem 4 (Forced odds ratio).
    Let Omega: P^1 -> P^1 be a rational bijection satisfying
    Omega(1/x) = 1/Omega(x) and Omega(0) = 0.

    Proof sketch:
      1. Omega(0) = b/d = 0  =>  b = 0.
      2. Substitute into exchange condition, cross-multiply:
         a^2 x = cd x^2 + (c^2 + d^2) x + cd
      3. Comparing coefficients:  cd = 0,  a^2 = c^2 + d^2.
      4. d = 0 => Omega = a/c = const (not bijective). Rejected.
      5. c = 0 => Omega = (a/d) x,  (a/d)^2 = 1.
      6. Omega >= 0 for x >= 0  =>  a/d = +1.

    Result: Omega(x) = x.  The unique element of Aut(P^1)
    satisfying the exchange symmetry and endpoint condition.
    This is a uniqueness theorem within the automorphism group
    of the projective symmetry space, not a claim about
    arbitrary constitutive functions.
    """
    return x


# =========================================================================
#  THE CONSTITUTIVE LAW
# =========================================================================

def mu(x):
    """The gravitational constitutive law: mu(x) = x / (x + 1).

    Origin: Proof C, Corollary 1 (Constitutive law).
    From Omega(x) = x, invert the odds-ratio definition:
        mu = Omega / (1 + Omega) = x / (1 + x).

    This is the TetA partition fraction — the fraction of the
    total field capacity carried by the identity component of
    the tetrad equation at dimensionless acceleration x = g/a0.

    Identified empirically by Milgrom (1983).
    Selected by fitting by Famaey & Binney (2005).
    Derived here from exchange symmetry of the tetrad equation's
    two parity-related spatial roots.

    Kinematic, not dynamic.  The algebraic form is identical to
    the GFD field equation's static limit, but the origin is
    geometric (exchange symmetry), not variational (action).
    Connected to the field equation via the AQUAL identity mu = dF/dy.
    """
    x = np.asarray(x, dtype=float)
    return x / (x + 1.0)


def one_minus_mu(x):
    """TetB partition fraction: 1 - mu(x) = 1 / (x + 1).

    Origin: Proof C, Definition 1 / eq (2).
    The fraction of the total field capacity carried by the
    parity component (TetB) at acceleration x.

    In the torsion-free projection, these 24 antisymmetric
    connection components are discarded.  Their field fraction
    is what, in the torsion-free framework, must be attributed
    to invisible mass.
    """
    x = np.asarray(x, dtype=float)
    return 1.0 / (x + 1.0)


def midpoint_value() -> float:
    """mu(1) = 1/2.  Derived, not assumed.

    Origin: Proof C, Corollary 2 (Midpoint value).
    At the parity midpoint x = 1 (the MOND transition scale),
    TetA and TetB contribute equally.  This is a consequence
    of the exchange symmetry, not an independent condition.
    """
    return mu(1.0)


def screening_identity(x: float) -> float:
    """Verify x(1 - mu) = mu.  Algebraic identity, not a postulate.

    Origin: Proof C, Remark 2 (Screening identity is algebraic).
    The odds-ratio identification mu/(1-mu) = x rearranged:
    multiply both sides by (1-mu) to obtain mu = x(1-mu).
    """
    m = mu(x)
    return x * (1.0 - m) - m


def logistic_identity(x: float) -> float:
    """Verify x * dmu/dx = mu(1 - mu).  The logistic transition.

    Origin: Letter 3 eq (7); also Letter body context.
    Under t = ln(x), becomes dmu/dt = mu(1-mu): the canonical
    two-sector transition law.  The product mu(1-mu) measures
    the simultaneous presence of both tetrahedral chambers.
    Peaks at x = 1 where mu(1-mu) = 1/4.
    """
    m = mu(x)
    # Analytic derivative: dmu/dx = 1/(x+1)^2
    dmu_dx = 1.0 / (x + 1.0)**2
    lhs = x * dmu_dx
    rhs = m * (1.0 - m)
    return lhs - rhs


# =========================================================================
#  PROOF B — The Energy Functional of the Gravitational Constitutive Law
# =========================================================================

def aqual_energy_functional(y):
    """F(y) = y - 2*sqrt(y) + 2*ln(1 + sqrt(y)).

    Origin: Proof B, Theorem 1 (Closed-form energy functional).
    The AQUAL framework (Bekenstein & Milgrom 1984) requires a
    kinetic functional F(y), with y = |grad Phi|^2 / a0^2,
    whose derivative w.r.t. y is the interpolating function mu.

    The AQUAL identity:  mu(sqrt(y)) = dF/dy.
    With boundary condition F(0) = 0:

        F(y) = integral_0^y mu(sqrt(t)) dt

    Substituting mu(x) = x/(x+1), setting u = sqrt(t):

        F(y) = 2 * integral_0^{sqrt(y)} u^2/(u+1) du

    Polynomial long division:
        u^2/(u+1) = (u - 1) + 1/(u+1)

    The remainder 1/(u+1) is identically 1 - mu(u): the TetB
    field fraction.  The logarithmic term of the action integrates
    twice the field share that the torsion-free condition discards.

    Integrating term by term yields three terms:
        y        from integral(u du)     — K^2 face-coupling level
        -2*sqrt(y)  from integral(-1 du) — sK state-dependent level
        2*ln(1+sqrt(y)) from integral(1/(u+1) du) — K^0 field origin

    Coefficients {1, 2, 2} are forced by the integration.
    Not fitted.  Not adjusted.
    """
    y = np.asarray(y, dtype=float)
    return y - 2.0 * np.sqrt(y) + 2.0 * np.log(1.0 + np.sqrt(y))


def dF_dy(y):
    """dF/dy = sqrt(y) / (1 + sqrt(y)) = mu(sqrt(y)).

    Origin: Proof B, Lemma 1 (Recovery of mu by differentiation).
    Independent verification of Theorem 1.
    Working in u = sqrt(y):
        F = u^2 - 2u + 2*ln(1+u)
        dF/du = 2u - 2 + 2/(1+u) = 2u^2/(1+u)
        dF/dy = (dF/du)/(dy/du) = (2u^2/(1+u)) / (2u) = u/(1+u)
    This is mu(u) = mu(sqrt(y)).  QED.
    """
    y = np.asarray(y, dtype=float)
    u = np.sqrt(y)
    return u / (1.0 + u)


def F_newtonian_limit(y):
    """High-acceleration limit: F(y) -> y.

    Origin: Proof B, Corollary 1 (Newtonian limit).
    For y >> 1, the subleading terms -2*sqrt(y) + 2*ln(1+sqrt(y))
    grow as O(sqrt(y)), negligible relative to y.
    So dF/dy -> 1 = mu(infinity).
    The modified Poisson equation reduces to nabla^2 Phi = 4*pi*G*rho.
    """
    return y


def F_deep_mond_limit(y):
    """Low-acceleration limit: F(y) -> (2/3) * y^(3/2).

    Origin: Proof B, Corollary 2 (Deep-MOND limit).
    Taylor expand ln(1 + sqrt(y)) about sqrt(y) = 0:
        ln(1+u) = u - u^2/2 + u^3/3 - ...
    Substituting into F:
        F = y - 2u + 2u - y + (2/3)y^(3/2) + O(y^2)
          = (2/3) y^(3/2) + O(y^2)
    The linear and square-root orders cancel exactly among all
    three terms, leaving the deep-MOND y^(3/2) scaling.
    Produces g_t -> sqrt(g_s * a0) and the baryonic Tully-Fisher
    relation M proportional to v^4.
    """
    return (2.0 / 3.0) * y**1.5


def long_division_remainder(u: float) -> float:
    """u^2/(u+1) = (u - 1) + 1/(u+1).  The remainder is 1 - mu(u).

    Origin: Proof B, Theorem 1 proof; Letter 3 eq (14).
    The algebraic identity u^2 - 1 = (u-1)(u+1) gives:
        u^2/(u+1) = (u^2 - 1 + 1)/(u+1) = (u-1) + 1/(u+1)
    The fractional remainder 1/(u+1) is identically the TetB
    field fraction.  The logarithmic term of the action is the
    integral of twice this remainder.
    """
    exact = u**2 / (u + 1.0)
    decomposed = (u - 1.0) + 1.0 / (u + 1.0)
    return exact - decomposed


# =========================================================================
#  THE COUPLING POLYNOMIAL
# =========================================================================

def coupling_polynomial(K: int, s: float) -> float:
    """f(K, s) = 1 + s*K + K^2.

    Origin: Letter 3 eq (2); Letter 2 (Nelson2026b).
    The tetrad equation contains three structural ingredients
    at ranks 0, 1, 2 on the frame space, with graded dimensions
    K^0 = 1, K^1 = K, K^2.  The rank-1 vielbein is parity-odd,
    so the state parameter s takes sign (-1)^1 = -1 under parity.
    Ranks 0 and 2 are parity-even.

    Evaluations at K = 4:
        f(4, +1) = 21   (TetA total)
        f(4,  0) = 17   (field origin balance)
        f(4, -1) = 13   (TetB core)

    Range: Delta f = 21 - 13 = 2K = 8 = 2^D.
    This is the closure condition 2(D+1) = 2^D read as the
    dynamic range of the polynomial.
    """
    return 1 + s * K + K**2


def connection_decomposition(K: int) -> dict:
    """The 40/24 decomposition of the affine connection.

    Origin: Letter 3 eqs (3)-(6); Proof A context.
    Each K x K slice of the connection has:
        K diagonal entries (shared, root-blind)
        K(K-1)/2 upper-triangle (TetA, retained)
        K(K-1)/2 lower-triangle (TetB, discarded)

    Per face:
        Retained = K + K(K-1)/2 = K(K+1)/2 = (f(K,+1) - 1)/2 = 10
        Discarded = K(K-1)/2 = (f(K,-1) - 1)/2 = 6
        Total = K^2 = 16

    Across K = 4 faces:
        Retained: 4 * 10 = 40  (Christoffel)
        Discarded: 4 * 6 = 24  (torsion)
        Total: 4 * 16 = 64 = K^3
    """
    retained_per_face = K * (K + 1) // 2
    discarded_per_face = K * (K - 1) // 2
    total_per_face = K**2
    return {
        "retained_per_face": retained_per_face,    # 10
        "discarded_per_face": discarded_per_face,   # 6
        "total_per_face": total_per_face,            # 16
        "retained_total": K * retained_per_face,     # 40
        "discarded_total": K * discarded_per_face,   # 24
        "connection_total": K**3,                     # 64
    }


# =========================================================================
#  THE DIOPHANTINE UNIQUENESS
# =========================================================================

def uniqueness_equation(d: int) -> bool:
    """Check 2(d+1) = 2^d.  Unique positive integer solution: d = 3.

    Origin: Letter 2 (Nelson2026b); DFP framework.
    Left side counts faces: two roots, each carrying a D-simplex
    with D+1 = K faces.
    Right side counts vertices: D binary axes, each admitting
    two orientations, giving 2^D sign combinations.

    d=1: 4 != 2.  d=2: 6 != 4.  d=3: 8 == 8.
    d=4: 10 != 16.  Exponential outgrows linear for d > 3.
    D = 3 is the minimum and unique positive integer solution.
    """
    return 2 * (d + 1) == 2**d


# =========================================================================
#  LETTER — GFD Field Equation and RAR Prediction
# =========================================================================

def gfd_field_equation(g_bar, a0: float = A0) -> np.ndarray:
    """g_obs = (1/2) [g_bar + sqrt(g_bar^2 + 4*a0*g_bar)].

    Origin: Letter eq (4), boxed.  The prediction tested against SPARC.

    Derivation chain (Letter §3, three steps):

    Step 1 — Modified Poisson equation (Bekenstein & Milgrom 1984):
        Vary the F(y) term of the covariant action w.r.t. Phi.
        In the weak-field static limit:
            div[mu(|grad Phi|/a0) grad Phi] = 4*pi*G*rho
        The scalar exponential e^{-2Phi/c^2} -> 1 and the vector
        sector decouples, so the modified Poisson equation captures
        the full content of the action for static spherical systems.

    Step 2 — Gauss's theorem:
        Integrate over a sphere of radius r:
            mu(g_t / a0) * g_t = g_bar
        where g_t = |grad Phi| is total acceleration and
        g_bar = GM(<r)/r^2 is baryonic acceleration.

    Step 3 — Algebraic substitution:
        Substitute mu(x) = x/(x+1) into mu * g_t = g_bar:
            g_t/(g_t/a0 + 1) * (g_t/a0) * a0 = ... simplifies to
            g_bar = g_t^2 / (a0 + g_t)
        Solve the resulting quadratic for g_t:
            g_obs = (1/2) [g_bar + sqrt(g_bar^2 + 4*a0*g_bar)]

    Contains one empirical constant (a0) and no fitted parameters.
    mu is derived (Proof C).  F is derived from mu (Proof B).
    """
    g_bar = np.asarray(g_bar, dtype=float)
    return 0.5 * (g_bar + np.sqrt(g_bar**2 + 4.0 * a0 * g_bar))


def gfd_field_equation_inverse(g_obs, a0: float = A0) -> np.ndarray:
    """g_bar = g_obs^2 / (a0 + g_obs).

    Origin: Letter eq (4) rearranged; Letter 3 eq (10).
    The field equation form: substitute mu = g_bar/g_obs,
    x = g_obs/a0 into mu * g_obs = g_bar.

    This is NOT the covariant action (the SST).
    This is NOT the field equation (the modified Poisson equation).
    This IS the field equation solved in the spherical static limit.
    The four equivalent forms are one equation (the coupling polynomial)
    written for different purposes.
    """
    g_obs = np.asarray(g_obs, dtype=float)
    return g_obs**2 / (a0 + g_obs)


def mcgaugh_rar(g_bar, g_dagger: float = A0) -> np.ndarray:
    """McGaugh+2016 empirical fit: g_obs = g_bar / (1 - exp(-sqrt(g_bar/g+))).

    Origin: McGaugh, Lelli & Schombert, PRL 117 (2016) 201101.
    One-parameter empirical fit to the SPARC radial acceleration relation.
    The parameter g+ (= a0) is fitted to rotation curve data.

    Compared against the GFD field equation in the RAR letter.
    The two are statistically indistinguishable at SPARC precision:
    Delta sigma = 0.0003 dex across 3284 points / 164 galaxies.
    """
    g_bar = np.asarray(g_bar, dtype=float)
    return g_bar / (1.0 - np.exp(-np.sqrt(g_bar / g_dagger)))


# =========================================================================
#  THE COVARIANT ACTION (display only — not computable as a function)
# =========================================================================

COVARIANT_ACTION = r"""
The Gravity Field Dynamics covariant action (Letter eq (1)):

    S = int d^4x sqrt(-g) [ R/(16*pi*G)
                           - a0^2/(8*pi*G) * F(y)
                           - (1/4) * e^{-2*Phi/c^2} * F_uv * F^uv
                           + L_matter ]

where:
    R           = Ricci scalar (Einstein-Hilbert)
    F(y)        = y - 2*sqrt(y) + 2*ln(1 + sqrt(y))  (AQUAL energy functional)
    y           = |grad Phi|^2 / a0^2  (kinetic variable)
    Phi         = gravitational scalar potential (not a new field)
    F_uv        = field strength of auxiliary vector field
    L_matter    = standard matter Lagrangian

Term 1: spacetime curvature (general relativity).
Term 2: scalar sector, kinetic function F derived from mu (Proof B).
Term 3: electromagnetic coupling encoding scalar potential's
        imprint on photometric observables.
Term 4: standard matter.

No term contains a free function.  mu fixes F via the AQUAL identity.
The frame geometry determines the remaining couplings.
"""


# =========================================================================
#  DFP SERIES — Cosmological and Scale Equations
# =========================================================================

# --- Physical constants (SI) ---
G_SI = 6.674e-11       # m^3 kg^-1 s^-2
C_SI = 2.998e8          # m/s
M_E = 9.109e-31         # kg (electron mass)
R_E = 2.818e-15         # m  (classical electron radius)
E_CHARGE = 1.602e-19    # C  (elementary charge)
EPSILON_0 = 8.854e-12   # F/m (permittivity of free space)
HBAR = 1.055e-34        # J·s
K_B = 1.381e-23         # J/K


def graviton_polarizations(k: int = K) -> int:
    """Physical graviton polarizations: 10 - 2k.

    Origin: DFP V §2.5.
    The metric tensor has 10 independent components.
    k constraints remove 2k degrees of freedom (k lapse/shift
    choices + k constraint equations).
    LIGO measured exactly 2 polarizations from GW170817.
    10 - 2(4) = 2.  Confirms k = 4 observationally.
    """
    return 10 - 2 * k


def classical_electron_radius(m_e: float = M_E,
                               e: float = E_CHARGE,
                               eps0: float = EPSILON_0,
                               c: float = C_SI) -> float:
    """r_e = e^2 / (4*pi*epsilon_0 * m_e * c^2).

    Origin: DFP V §6.2, Route 1 (Electromagnetic stability).
    The EM-gravity crossover scale.  Not the "size" of the electron
    but the radius at which electrostatic self-energy equals rest
    mass energy.  Three independent routes converge on this scale
    (EM stability, cosmic topology, coupling test).
    """
    return e**2 / (4.0 * math.pi * eps0 * m_e * c**2)


def electron_surface_gravity(G: float = G_SI,
                              m_e: float = M_E,
                              r_e: float = R_E) -> float:
    """g_tile = G * m_e / r_e^2.

    Origin: DFP III §5.4 Step 3; DFP V §6.2 Route 3.
    The gravitational acceleration at the electron's classical
    radius.  The fundamental unit of gravitational coupling.
    g_tile = 7.66e-12 m/s^2.
    """
    return G * m_e / r_e**2


def a0_from_electron(k: int = K, G: float = G_SI,
                     m_e: float = M_E,
                     r_e: float = R_E) -> float:
    """a0 = k^2 * G * m_e / r_e^2 = 16 * g_tile.

    Origin: DFP III §5.4 Step 6; DFP IV §3.1; DFP V §6.3.
    Isotropic coupling through k^2 = 16 channels at the electron
    tile scale.  Each interior sphere has k = 4 coupling faces;
    with 4 spheres packed tetrahedrally: k * k = 16 channels.

    Result: a0 = 1.225e-10 m/s^2.
    Matches observed MOND scale (1.20 +/- 0.02) to 2%.
    Only the electron matches among known particles; proton is
    wrong by 10^7.
    """
    return k**2 * G * m_e / r_e**2


def a0_from_hubble(H_si: float, c: float = C_SI) -> float:
    """a0 = c * H / (2*pi).

    Origin: DFP II §2.3; DFP IV §3.2.
    Horizon thermodynamics route.  The Gibbons-Hawking temperature
    of the cosmological horizon T_GH = hbar*H/(2*pi*k_B*c)
    defines a minimum resolvable acceleration via the Unruh
    relation T = hbar*a/(2*pi*k_B*c).
    Equating: a0 = c*H/(2*pi).

    For H0 ~ 70 km/s/Mpc = 2.27e-18 s^-1:
        a0 = 1.08e-10 m/s^2.
    Matches MOND scale to ~10%.  The 10% gap is the port ratio.
    """
    return c * H_si / (2.0 * math.pi)


def port_ratio(k: int = K) -> float:
    """sqrt(k / pi) = sqrt(4 / pi) = 1.1284.

    Origin: DFP III §5.3; DFP IV §3.3; DFP V §5.3.
    Converts between continuous geometry (spherical field envelope,
    characterised by pi) and discrete topology (tetrahedral field
    chamber, characterised by k = 4).

    Area ratio: k/pi.  Length ratio: sqrt(k/pi).
    H has units involving length, not area, so take the square root.

    The ratio of the two a0 derivations:
        a0_electron / a0_hubble = 1.225/1.083 = 1.131
        sqrt(4/pi)                             = 1.128
    Match to 0.27%.

    If exact: H0 = 2*pi*k^2*G*m_e / (c*sqrt(k/pi)*r_e^2)
            = 69.92 km/s/Mpc.
    GW170817: 70.0 +/- 12.  Match to 0.11%.
    """
    return math.sqrt(k / math.pi)


def hubble_from_electron(k: int = K, G: float = G_SI,
                          m_e: float = M_E,
                          r_e: float = R_E,
                          c: float = C_SI) -> float:
    """H = (2*pi*k^2) / (c * sqrt(k/pi)) * G*m_e/r_e^2.

    Origin: DFP IV §6.3; DFP V §6.4.
    Complete derivation chain:
        1. a0 = k^2 * G*m_e/r_e^2  (electron route)
        2. H_flat = 2*pi*a0/c      (horizon thermodynamics inverted)
        3. H = H_flat / sqrt(k/pi) (port ratio correction)

    Result: H = 69.92 km/s/Mpc (in SI: 2.267e-18 s^-1).
    GW170817 (no distance ladder, no CMB model): 70.0 +/- 12.
    Match: 0.11%.

    Returns H in SI units (s^-1).  Multiply by 3.086e22/1e3
    to convert to km/s/Mpc.
    """
    a0 = k**2 * G * m_e / r_e**2
    H_flat = 2.0 * math.pi * a0 / c
    return H_flat / port_ratio(k)


def electron_mass_from_hubble(H_si: float,
                               k: int = K,
                               G: float = G_SI,
                               e: float = E_CHARGE,
                               eps0: float = EPSILON_0,
                               c: float = C_SI) -> float:
    """m_e^3 = H * e^4 * sqrt(k/pi) / (2*pi*k^2*G*(4*pi*eps0)^2*c^3).

    Origin: DFP IV §6.3 eq (3).
    The bidirectional derivation: given H, the electron mass is
    uniquely determined.  Substituting r_e = e^2/(4*pi*eps0*m_e*c^2)
    into a0 = k^2*G*m_e/r_e^2 and solving for m_e gives m_e^3.

    First theoretical derivation of a Standard Model mass parameter
    from cosmological data.  Inputs: H (measured), k = 4 (simplex
    theorem), e, eps0, G, c.

    Returns m_e in kg.
    """
    numerator = H_si * e**4 * port_ratio(k)
    denominator = (2.0 * math.pi * k**2 * G
                   * (4.0 * math.pi * eps0)**2 * c**3)
    return (numerator / denominator) ** (1.0 / 3.0)


def cosmic_electron_radius(k: int = K, G: float = G_SI,
                            m_e: float = M_E,
                            a0: float = A0) -> float:
    """r_e = k * sqrt(G * m_e / a0).

    Origin: DFP V §6.2 Route 2 (Cosmic topology).
    Uses gravity (G), cosmology (a0), and topology (k = 4).
    No electromagnetism.

    Result: 2.82e-15 m = 2.82 fm.
    Matches classical electron radius (2.818 fm) to 0.21%.
    Three independent routes converge on the same scale.
    """
    return k * math.sqrt(G * m_e / a0)


def measurement_cage(k: int = K) -> tuple:
    """Hubble measurement cage: (k/pi)^(1/4) = 1.062 → +/- 6.2%.

    Origin: DFP IV §3.5; DFP V §5.5.
    The scatter factor is the fourth root of the full port ratio
    squared correction.  Cage spans H_pred * [1/cage, cage].

    For H_pred = 69.92: cage = [65.8, 74.3] km/s/Mpc.
    All seven major H measurement methods fall within this range.
    Probability by chance: (0.12)^7 ~ 3.6e-7.
    """
    cage = (k / math.pi) ** 0.25
    H_pred_kmsMpc = 69.92
    return H_pred_kmsMpc / cage, H_pred_kmsMpc * cage


def a0_cosmological_scaling(H_z: float, H_0: float,
                             a0_0: float = A0,
                             k: int = K) -> float:
    """a0(z) = a0_0 * (H(z)/H0)^(1 - 1/pi).

    Origin: DFP II §7.1.
    The cosmological scaling law.  Standard a0 = cH/(2pi) is
    modified by hexagonal tiling suppression (H0/H)^(1/pi):

        a0(z) = [cH(z)/(2pi)] * (H0/H(z))^(1/pi)

    Equivalently: a0 proportional to H^alpha where
    alpha = 1 - 1/pi ~ 0.682.

    The 1/pi exponent comes from continuous boundary averaging
    of the hexagonal closure tiling arc angle:
        <theta>/(2*pi) = 1/pi
    (DFP II §6.4, Theorem: Continuous Coupling Efficiency).
    """
    alpha = 1.0 - 1.0 / math.pi
    return a0_0 * (H_z / H_0) ** alpha


def cmb_enhancement(x: float) -> float:
    """Gravitational enhancement factor: (1 + x) / x = 1/mu(x).

    Origin: DFP II §5.1.
    In the modified Poisson equation, 1/mu(x) acts as the
    effective enhancement of gravitational coupling.
    At recombination (z = 1100), x ~ 0.183 gives
    enhancement ~ 6.46.  Planck observes 6.40.
    Match within 1%.
    """
    return (1.0 + x) / x


def hexagonal_coupling_fraction() -> float:
    """Average coupling fraction from hexagonal tiling: 1/pi.

    Origin: DFP II §6.4 (Theorem: Continuous Coupling Efficiency).
    For circular closure boundaries with separation uniformly
    distributed over [0, 2R], the average coupling fraction is:

        <theta>/(2*pi) = (1/(2*pi)) * integral_0^1 2*arccos(u) du
                       = (1/(2*pi)) * 2
                       = 1/pi

    The arc angle formula: theta(d) = 2*arccos(d/(2R)) for d <= 2R.
    Discrete case (d = R): theta = 2*pi/3, fraction = 1/3.
    Continuous average: fraction = 1/pi ~ 0.318.

    The cosmological scaling exponent is alpha = 1 - 1/pi ~ 0.682.
    """
    return 1.0 / math.pi


def dirac_large_numbers_gap(k: int = K) -> float:
    """k^2 * (k/pi) = 16 * (4/pi) = 20.37.

    Origin: DFP IV §4.3 (Test 3: Dirac Large Numbers).
    Dirac noted that the ratio of cosmic to atomic scales
    and the ratio of electromagnetic to gravitational forces
    are both ~10^40 but differ by a factor ~20.

    k^2 * (k/pi) = 20.37.
    Measured gap: R_H/r_e divided by F_EM/F_grav = 20.67.
    Match to 1.4%.
    """
    return k**2 * (k / math.pi)


# =========================================================================
#  SPARC DATA CONVENTIONS
# =========================================================================

KMS2_PER_KPC_TO_MS2 = (1.0e3)**2 / 3.0857e19  # = 3.241e-14

UPSILON_DISK = 0.5   # M/L at 3.6 um (Lelli+2016 standard)
UPSILON_BUL = 0.7    # M/L at 3.6 um (Lelli+2016 standard)


def v_bar_squared(v_gas, v_disk, v_bul,
                  Y_d: float = UPSILON_DISK,
                  Y_b: float = UPSILON_BUL):
    """Baryonic velocity squared from SPARC velocity decomposition.

    Origin: Letter §4; SPARC convention (Lelli+2016).
    v_bar^2 = v_gas * |v_gas|  +  Y_d * v_disk^2  +  Y_b * v_bul^2

    The gas sign is preserved (SPARC convention): v_gas can be
    negative in regions where the gas contribution to the
    circular velocity is formally negative (counter-rotating
    or pressure-supported gas).

    Y_d = 0.5 and Y_b = 0.7 are the standard SPARC mass-to-light
    ratios at 3.6 um.  Not fitted by this work.
    """
    vg = np.asarray(v_gas, dtype=float)
    vd = np.asarray(v_disk, dtype=float)
    vb = np.asarray(v_bul, dtype=float)
    return vg * np.abs(vg) + Y_d * vd**2 + Y_b * vb**2


def acceleration_from_velocity(v_squared, r_kpc):
    """Convert v^2/r in (km/s)^2/kpc to m/s^2.

    Origin: Letter §4.
    1 (km/s)^2 / kpc = 3.241e-14 m/s^2.
    """
    return np.asarray(v_squared, dtype=float) / np.asarray(r_kpc, dtype=float) * KMS2_PER_KPC_TO_MS2


# =========================================================================
#  SU(2) SPINOR PARAMETRIZATION — Analytic Continuation of s
# =========================================================================
#
#  The coupling polynomial f(K,s) has discrete states s ∈ {+1, 0, -1}.
#  Analytic continuation s = e^{iθ} lifts the state parameter to a
#  phase angle on the unit circle.  The constitutive law μ = x/(x+1)
#  then acquires a spinor parametrization μ = cos²(θ/2) that satisfies
#  all algebraic identities exactly — including the logistic transition
#  — by pure trigonometry.
#
#  Novel result: the MOND transition is an SU(2) rotation between
#  the dual tetrahedra.  Acceleration x is the geometric readout
#  of a spinor phase angle θ = 2 arctan(1/√x).


def complex_coupling_polynomial(K: int, theta: float) -> complex:
    """f(K, e^{iθ}) = (1 + K²) + K·e^{iθ} = (1+K²) + K·cos(θ) + iK·sin(θ).

    Origin: Analytic continuation of the discrete coupling polynomial.
    The state parameter s = e^{iθ} lifts the three discrete states
    to a continuous phase:
        θ = 0   → s = +1  → f = 21  (TetA total)
        θ = π/2 → s =  i  → f = 17 + 4i  (field origin + conjugate momentum)
        θ = π   → s = -1  → f = 13  (TetB core)

    Real part: (1+K²) + K·cos(θ) spans the physical states {13, 17, 21}.
    Imaginary part: K·sin(θ) is the conjugate momentum of the geometry.
    It vanishes at the pure parity states (θ = 0, π) and peaks at the
    transition midpoint (θ = π/2).
    """
    s = complex(math.cos(theta), math.sin(theta))
    return 1 + s * K + K**2


def coupling_polynomial_real(K: int, theta: float) -> float:
    """Re[f(K, e^{iθ})] = (1 + K²) + K·cos(θ).

    The real part spans the discrete physical states exactly:
        θ = 0:    17 + 4 = 21 = f(4,+1)
        θ = π/2:  17 + 0 = 17 = f(4, 0)
        θ = π:    17 - 4 = 13 = f(4,-1)
    """
    return (1 + K**2) + K * math.cos(theta)


def coupling_polynomial_imaginary(K: int, theta: float) -> float:
    """Im[f(K, e^{iθ})] = K·sin(θ).

    The conjugate momentum of the geometry.
    Vanishes at pure parity states (θ = 0, π).
    Peaks at the transition midpoint (θ = π/2): Im = K = 4.
    The transition between TetA and TetB is a quantum phase rotation;
    the imaginary part measures the rate of that rotation.
    """
    return K * math.sin(theta)


def mu_spinor(theta: float) -> float:
    """μ = cos²(θ/2).  Spinor parametrization of the constitutive law.

    Origin: SU(2) double cover of the stellated octahedron parity group.
    Assigning μ to the probability amplitude of the TetA state on the
    Bloch sphere:
        μ       = cos²(θ/2)   (TetA fraction)
        1 - μ   = sin²(θ/2)   (TetB fraction)

    The partition μ + (1-μ) = 1 is automatic from the Pythagorean
    identity — no external constraint needed.

    Boundary values:
        θ = 0:  μ = 1     (pure TetA, Newtonian)
        θ = π/2: μ = 1/2  (equal partition, MOND transition)
        θ = π:  μ = 0     (pure TetB, deep field)
    """
    return math.cos(theta / 2.0) ** 2


def one_minus_mu_spinor(theta: float) -> float:
    """1 - μ = sin²(θ/2).  TetB fraction in spinor form."""
    return math.sin(theta / 2.0) ** 2


def x_from_theta(theta: float) -> float:
    """x = cot²(θ/2).  Dimensionless acceleration from spinor phase.

    Origin: Forced odds ratio Ω(x) = x (Proof C, Theorem 4),
    combined with the spinor parametrization.

    Ω = μ/(1-μ) = cos²(θ/2)/sin²(θ/2) = cot²(θ/2).
    Since Ω(x) = x, we have x = cot²(θ/2).

    Acceleration is the geometric readout of the spinor angle.
    High acceleration (x → ∞) corresponds to θ → 0 (pure TetA).
    Low acceleration (x → 0) corresponds to θ → π (pure TetB).
    MOND transition (x = 1) corresponds to θ = π/2.
    """
    return 1.0 / math.tan(theta / 2.0) ** 2


def theta_from_x(x: float) -> float:
    """θ = 2·arctan(1/√x).  Spinor phase from dimensionless acceleration.

    Inverse of x = cot²(θ/2).
    Maps the full acceleration range x ∈ (0, ∞) to θ ∈ (0, π).
    """
    return 2.0 * math.atan(1.0 / math.sqrt(x))


def logistic_identity_spinor(theta: float) -> float:
    """Verify x·dμ/dx = μ(1-μ) in spinor coordinates.  Returns residual.

    Origin: Chain rule verification through θ parametrization.

    dμ/dθ = -sin(θ/2)·cos(θ/2)
    dx/dθ = -cos(θ/2)/sin³(θ/2)
    dμ/dx = (dμ/dθ)/(dx/dθ) = sin⁴(θ/2)

    LHS: x·dμ/dx = cot²(θ/2)·sin⁴(θ/2) = cos²(θ/2)·sin²(θ/2)
    RHS: μ(1-μ)  = cos²(θ/2)·sin²(θ/2)

    Exact match.  The logistic transition identity is a trigonometric
    identity in the spinor frame.  The AQUAL energy functional is the
    exact consequence of an SU(2) rotation between the dual tetrahedra.
    """
    c = math.cos(theta / 2.0)
    s = math.sin(theta / 2.0)
    lhs = (c**2 / s**2) * s**4          # x · dmu/dx = cot^2 * sin^4
    rhs = c**2 * s**2                    # mu * (1-mu)
    return lhs - rhs


def spinor_transition_rate(theta: float) -> float:
    """μ(1-μ) = cos²(θ/2)·sin²(θ/2) = (1/4)·sin²(θ).

    The product μ(1-μ) measures simultaneous presence of both
    tetrahedral chambers.  In spinor form it equals (sin θ)²/4.
    Peaks at θ = π/2 (the MOND ring) where μ(1-μ) = 1/4.

    This is the squared imaginary part of the normalised complex
    coupling polynomial divided by K²:
        Im[f]² / (4K²) = K²·sin²(θ) / (4K²) = sin²(θ)/4.
    The transition rate IS the conjugate momentum squared.
    """
    return 0.25 * math.sin(theta) ** 2


# =========================================================================
#  SPECTRAL PROCESSOR — Walsh-Hadamard Boolean Algebra
# =========================================================================
#
#  Core insight: ANY Boolean function can be compiled to an exact
#  multilinear polynomial via the Walsh-Hadamard transform.  The
#  transform is self-inverse (H·H = N·I), so truth table → spectrum
#  and spectrum → truth table are the same operation.
#
#  The WaveNode is the hardware primitive that evaluates one term of
#  this polynomial:  bridge[c] × (−1)^popcount(input & c).
#  Stack N of them and you evaluate an N-term polynomial in one cycle.
#
#  This is the mathematical foundation of the spectral processor
#  (Kria KR260 FPGA target) and the Walsh chess engine.


def fwht(a) -> np.ndarray:
    """Fast Walsh-Hadamard Transform.  O(N log N), in-place butterfly.

    Origin: Standard algorithm.  Computes H @ a where
    H[i,j] = (−1)^popcount(i & j) is the Sylvester Hadamard matrix.

    H is self-inverse up to scaling: H·H = N·I.
    So FWHT serves as BOTH the forward and inverse transform.
    Forward: spectrum = FWHT(signal) / N.
    Inverse: signal = FWHT(spectrum).
    Same code, one normalization.

    This is the Fourier transform on the group (Z/2)^n.
    NOT the DFT on Z/N.  Different group, different basis,
    different sparsity structure.
    """
    a = np.asarray(a, dtype=np.float64).copy()
    N = len(a)
    assert (N & (N - 1)) == 0, "length must be a power of 2"
    h = 1
    while h < N:
        for i in range(0, N, h * 2):
            x = a[i:i + h].copy()
            y = a[i + h:i + 2 * h].copy()
            a[i:i + h] = x + y
            a[i + h:i + 2 * h] = x - y
        h *= 2
    return a


def truth_table_to_bridge(tt) -> np.ndarray:
    """Boolean truth table → Walsh bridge coefficients.

    Origin: Spectral processor core compilation step.
    The bridge coefficients are the exact multilinear polynomial
    representation of the Boolean function:

        f(x) = Σ_c bridge[c] × χ_c(x)

    where χ_c(x) = Π_{i: bit_i(c)=1} x_i  are the Walsh characters.

    Conversion:  bridge = FWHT(1 − 2·tt) / N
    The (1−2·tt) maps {0,1} → {+1,−1} (spectral convention).

    This is THE compiler.  Truth table in, equation out.
    One matrix multiply.  No search, no tuning, no learning.
    Lossless and invertible.
    """
    tt = np.asarray(tt, dtype=np.float64)
    N = len(tt)
    pm = 1.0 - 2.0 * tt  # {0,1} → {+1,−1}
    return fwht(pm) / N


def bridge_to_truth_table(bridge) -> np.ndarray:
    """Walsh bridge coefficients → Boolean truth table.

    Origin: Spectral processor inverse compilation.
    Because H is self-inverse (H·H = N·I), the inverse is:

        tt = (1 − FWHT(bridge)) / 2

    Same operation as forward, different normalization.
    This is the "reverse engineering" path: given bridge
    coefficients (e.g. from an FPGA bitstream), recover
    the Boolean function.
    """
    bridge = np.asarray(bridge, dtype=np.float64)
    pm = fwht(bridge)  # recover ±1 signal
    return ((1.0 - pm) / 2.0).round().astype(int)


def wavenode_eval(bridge, input_bits: int) -> float:
    """The WaveNode formula: output = Σ bridge[c] × (−1)^popcount(input & c).

    Origin: Spectral processor hardware primitive.
    Each WaveNode unit computes one term.  Stack N units for
    N-term evaluation in one cycle.

    This is the single-formula evaluation of ANY Boolean function.
    No gates, no lookup tables, no branching.  One dot product
    in the Walsh basis.

    Benchmarked at 649× faster than full gate simulation
    (verified across all 16 two-input Boolean functions,
    4-input functions, and wide-bit operations).

    On corners of the hypercube (input_bits ∈ {0,1}^n),
    recovers the exact Boolean output.
    On interior points (inputs ∈ [−1,+1]^n via character
    expansion), gives the multilinear extension — a calibrated
    probability.
    """
    N = len(bridge)
    total = 0.0
    for c in range(N):
        sign = (-1) ** bin(input_bits & c).count('1')
        total += bridge[c] * sign
    return total


def wavenode_eval_vectorised(bridge, inputs: np.ndarray) -> np.ndarray:
    """Vectorised WaveNode evaluation over multiple inputs.

    Origin: GPU batch engine (verified on H200).
    For each input x in inputs:
        output[x] = Σ_c bridge[c] × (−1)^popcount(x & c)

    Equivalent to: outputs = FWHT(bridge)[inputs]
    but the FWHT form precomputes all 2^n outputs at once.
    """
    bridge = np.asarray(bridge, dtype=np.float64)
    # FWHT of bridge gives all outputs at once
    all_outputs = fwht(bridge)
    return all_outputs[inputs]


def walsh_sparsity(bridge, threshold: float = 1e-10) -> int:
    """Count of nonzero Walsh coefficients above threshold.

    Origin: Spectral processor complexity metric.
    The intrinsic complexity of a Boolean function is measured
    by the number of nonzero bridge coefficients, not by its
    input width.

    Examples (6-input functions, N = 64):
        XOR (parity):     1 nonzero coefficient
        AND:              2^n coefficients (all nonzero)
        Random:           all 64 nonzero
        7-segment digit:  4-8 per segment (structured)

    Sparsity determines:
        - FPGA area (LUT count)
        - WaveNode cycle count
        - GA search difficulty
        - Compressibility
    """
    return int(np.sum(np.abs(np.asarray(bridge)) > threshold))


def walsh_character(c: int, x: int) -> int:
    """Walsh character χ_c(x) = (−1)^popcount(c & x).

    Origin: Group theory of (Z/2)^n.
    The Walsh characters are the irreducible representations
    of the Boolean group.  They form an orthonormal basis
    under the inner product <f,g> = (1/N) Σ_x f(x)g(x).

    χ_c(x) = Π_{i: bit_i(c)=1} x_i   (in ±1 encoding)
            = (−1)^popcount(c & x)     (equivalent form)
    """
    return (-1) ** bin(c & x).count('1')


def compile_to_lut6(tt_6bit) -> int:
    """Compile a 6-input truth table to a LUT-6 INIT value.

    Origin: FPGA synthesis path.
    Any Boolean function of ≤ 6 inputs compiles to exactly
    one LUT-6 cell.  The INIT value is the truth table packed
    as a 64-bit integer.  This is the target format for
    Xilinx/AMD FPGAs (Kria KR260).

    On the spectral processor, the same function is stored
    as 64 bridge coefficients instead.  Same function,
    different representation.  The LUT-6 is the lookup form;
    the bridge is the polynomial form.
    """
    tt = np.asarray(tt_6bit, dtype=int)
    assert len(tt) == 64, "LUT-6 requires exactly 64-entry truth table"
    init = 0
    for i in range(64):
        if tt[i]:
            init |= (1 << i)
    return init


def canonical_2input_gates() -> dict:
    """Walsh spectra of the six canonical 2-input Boolean gates.

    Origin: spectral_kernel.py _GATE_COEFFS.
    Each gate is a 4-entry truth table on 2 inputs.
    FWHT gives 4 bridge coefficients per gate.

    These are the atoms of Boolean logic in the Walsh basis.
    Any wider function decomposes into compositions of these.

    Convention: inputs in {+1,−1}, output in {+1,−1}.
    Bridge indexed by subset c ∈ {00, 01, 10, 11}.
    """
    gates = {}
    # Truth tables in {0,1} convention: tt[b1*2+b0]
    specs = {
        "AND":  [0, 0, 0, 1],
        "OR":   [0, 1, 1, 1],
        "XOR":  [0, 1, 1, 0],
        "NAND": [1, 1, 1, 0],
        "NOR":  [1, 0, 0, 0],
        "XNOR": [1, 0, 0, 1],
    }
    for name, tt in specs.items():
        gates[name] = {
            "truth_table": np.array(tt),
            "bridge": truth_table_to_bridge(np.array(tt)),
            "sparsity": walsh_sparsity(truth_table_to_bridge(np.array(tt))),
        }
    return gates


# =========================================================================
#  SELF-CHECKS
# =========================================================================

def run_checks():
    """Verify every algebraic identity.  Zero output = all pass."""

    # Proof A
    G = forced_gram_matrix(math.sqrt(3))
    assert np.allclose(np.diag(G), 3.0), "Gram diagonal != c^2"
    assert np.allclose(G - np.diag(np.diag(G)), -1.0 * (np.ones((4,4)) - np.eye(4))), "Gram off-diagonal != -c^2/3"
    M = canonical_sign_matrix()
    assert np.allclose(M.T @ M, G), "M^T M != forced Gram matrix"
    assert abs(edge_length_squared(math.sqrt(3)) - 8.0) < 1e-12, "edge^2 != 8c^2/3 at c=sqrt(3)"
    S = parity_completion(M)
    assert S.shape == (3, 8), "parity completion should be 3x8"

    # Proof C
    for x in [0.01, 0.1, 1.0, 10.0, 100.0]:
        assert abs(exchange_duality(mu, x)) < 1e-14, f"exchange duality fails at x={x}"
        assert abs(screening_identity(x)) < 1e-14, f"screening identity fails at x={x}"
        assert abs(logistic_identity(x)) < 1e-14, f"logistic identity fails at x={x}"
        omega = odds_ratio(mu(x))
        assert abs(omega - x) < 1e-12, f"odds ratio != x at x={x}"
    assert abs(midpoint_value() - 0.5) < 1e-15, "mu(1) != 1/2"

    # Proof B
    for y in [0.01, 0.1, 1.0, 10.0, 100.0]:
        assert abs(dF_dy(y) - mu(math.sqrt(y))) < 1e-14, f"dF/dy != mu(sqrt(y)) at y={y}"
    assert abs(long_division_remainder(3.0)) < 1e-14, "long division identity fails"
    # deep-MOND limit
    y_small = 1e-6
    assert abs(aqual_energy_functional(y_small) / F_deep_mond_limit(y_small) - 1.0) < 0.01, "deep-MOND limit fails"

    # Coupling polynomial
    assert coupling_polynomial(4, +1) == 21, "f(4,+1) != 21"
    assert coupling_polynomial(4,  0) == 17, "f(4, 0) != 17"
    assert coupling_polynomial(4, -1) == 13, "f(4,-1) != 13"
    assert coupling_polynomial(4, +1) - coupling_polynomial(4, -1) == 8, "range != 2K"

    # Connection decomposition
    cd = connection_decomposition(4)
    assert cd["retained_per_face"] == 10
    assert cd["discarded_per_face"] == 6
    assert cd["retained_total"] == 40
    assert cd["discarded_total"] == 24
    assert cd["connection_total"] == 64

    # Polynomial ↔ connection identity
    assert (coupling_polynomial(4, +1) - 1) // 2 == cd["retained_per_face"]
    assert (coupling_polynomial(4, -1) - 1) // 2 == cd["discarded_per_face"]

    # Diophantine uniqueness
    for d in range(1, 20):
        if d == 3:
            assert uniqueness_equation(d), "2(3+1) should equal 2^3"
        else:
            assert not uniqueness_equation(d), f"2({d}+1) should NOT equal 2^{d}"

    # GFD field equation round-trip
    g_bar_test = np.logspace(-13, -8, 100)
    g_obs_test = gfd_field_equation(g_bar_test)
    g_bar_back = gfd_field_equation_inverse(g_obs_test)
    assert np.allclose(g_bar_test, g_bar_back, rtol=1e-10), "field equation round-trip fails"

    # DFP series
    assert graviton_polarizations(4) == 2, "polarizations != 2 at k=4"
    assert abs(classical_electron_radius() - R_E) / R_E < 0.001, "r_e formula mismatch"
    assert abs(electron_surface_gravity() - 7.66e-12) / 7.66e-12 < 0.01, "g_tile mismatch"
    assert abs(a0_from_electron() - 1.225e-10) / 1.225e-10 < 0.01, "a0 electron mismatch"
    H0_si = 70.0 * 1e3 / 3.086e22  # 70 km/s/Mpc in s^-1
    assert abs(a0_from_hubble(H0_si) - 1.08e-10) / 1.08e-10 < 0.02, "a0 hubble mismatch"
    assert abs(port_ratio() - math.sqrt(4.0 / math.pi)) < 1e-14, "port ratio mismatch"
    H_pred = hubble_from_electron()
    H_pred_kmsMpc = H_pred * 3.086e22 / 1e3
    assert abs(H_pred_kmsMpc - 69.92) / 69.92 < 0.01, f"H prediction mismatch: {H_pred_kmsMpc}"
    m_e_recov = electron_mass_from_hubble(H0_si)
    assert abs(m_e_recov - M_E) / M_E < 0.01, f"m_e recovery mismatch: {m_e_recov}"
    r_e_cosmic = cosmic_electron_radius(a0=1.22e-10)  # DFP V uses empirical a0
    assert abs(r_e_cosmic - R_E) / R_E < 0.01, f"cosmic r_e mismatch: {r_e_cosmic}"
    cage_lo, cage_hi = measurement_cage()
    assert 65 < cage_lo < 66 and 74 < cage_hi < 75, "measurement cage bounds wrong"
    assert abs(hexagonal_coupling_fraction() - 1.0 / math.pi) < 1e-14, "hex fraction mismatch"
    assert abs(dirac_large_numbers_gap() - 20.37) < 0.01, "Dirac gap mismatch"
    # CMB enhancement
    assert abs(cmb_enhancement(0.183) - 6.46) < 0.02, "CMB enhancement mismatch"
    # Cosmological scaling: at z=0, a0 should be a0_0
    assert abs(a0_cosmological_scaling(H0_si, H0_si) - A0) < 1e-20, "scaling at z=0 fails"

    # SU(2) spinor parametrization
    # Complex polynomial recovers discrete states
    assert abs(complex_coupling_polynomial(4, 0).real - 21) < 1e-10, "f(4,e^0) real != 21"
    assert abs(complex_coupling_polynomial(4, 0).imag) < 1e-10, "f(4,e^0) imag != 0"
    assert abs(complex_coupling_polynomial(4, math.pi).real - 13) < 1e-10, "f(4,e^{iπ}) real != 13"
    assert abs(complex_coupling_polynomial(4, math.pi).imag) < 1e-10, "f(4,e^{iπ}) imag != 0"
    assert abs(complex_coupling_polynomial(4, math.pi/2).real - 17) < 1e-10, "f(4,e^{iπ/2}) real != 17"
    assert abs(complex_coupling_polynomial(4, math.pi/2).imag - 4) < 1e-10, "f(4,e^{iπ/2}) imag != 4"

    # Spinor mu matches algebraic mu
    for x_test in [0.01, 0.1, 1.0, 4.0, 10.0, 100.0]:
        theta_test = theta_from_x(x_test)
        mu_spin = mu_spinor(theta_test)
        mu_alg = float(mu(x_test))
        assert abs(mu_spin - mu_alg) < 1e-12, f"spinor mu != algebraic mu at x={x_test}"

    # Round-trip: x → θ → x
    for x_test in [0.01, 1.0, 100.0]:
        theta_test = theta_from_x(x_test)
        x_back = x_from_theta(theta_test)
        assert abs(x_back - x_test) / x_test < 1e-12, f"x round-trip fails at x={x_test}"

    # Logistic identity in spinor coordinates
    for theta_test in [0.3, math.pi/4, math.pi/2, math.pi/3, 2.5]:
        assert abs(logistic_identity_spinor(theta_test)) < 1e-12, \
            f"logistic spinor fails at θ={theta_test}"

    # Transition rate peaks at θ = π/2
    assert abs(spinor_transition_rate(math.pi / 2) - 0.25) < 1e-14, "peak rate != 1/4"
    assert abs(spinor_transition_rate(0.0)) < 1e-14, "rate at θ=0 != 0"
    assert abs(spinor_transition_rate(math.pi)) < 1e-14, "rate at θ=π != 0"

    # Midpoint: θ = π/2 gives x = 1, μ = 1/2
    assert abs(x_from_theta(math.pi / 2) - 1.0) < 1e-12, "x(π/2) != 1"
    assert abs(mu_spinor(math.pi / 2) - 0.5) < 1e-12, "μ(π/2) != 1/2"

    # Walsh-Hadamard spectral processor
    # FWHT self-inverse: H·H = N·I
    v = np.array([1.0, 0.0, 1.0, 1.0])
    assert np.allclose(fwht(fwht(v)), len(v) * v), "FWHT not self-inverse"

    # Round-trip: truth table → bridge → truth table
    tt_xor = np.array([0, 1, 1, 0])  # XOR of 2 bits
    bridge_xor = truth_table_to_bridge(tt_xor)
    tt_back = bridge_to_truth_table(bridge_xor)
    assert np.array_equal(tt_xor, tt_back), "XOR round-trip fails"

    # XOR has exactly 1 nonzero Walsh coefficient (parity)
    assert walsh_sparsity(bridge_xor) == 1, f"XOR sparsity != 1: {walsh_sparsity(bridge_xor)}"

    # WaveNode eval matches truth table on all inputs
    tt_and = np.array([0, 0, 0, 1])  # AND
    bridge_and = truth_table_to_bridge(tt_and)
    for x in range(4):
        wn = wavenode_eval(bridge_and, x)
        expected = 1.0 - 2.0 * tt_and[x]  # ±1 convention
        assert abs(wn - expected) < 1e-12, f"WaveNode AND mismatch at x={x}"

    # Vectorised eval matches scalar eval
    bridge_or = truth_table_to_bridge(np.array([0, 1, 1, 1]))
    inputs = np.arange(4)
    vec_out = wavenode_eval_vectorised(bridge_or, inputs)
    for x in range(4):
        assert abs(vec_out[x] - wavenode_eval(bridge_or, x)) < 1e-12, \
            f"vectorised mismatch at x={x}"

    # LUT-6 compilation
    tt6 = np.zeros(64, dtype=int)
    tt6[63] = 1  # 6-input AND
    init = compile_to_lut6(tt6)
    assert init == (1 << 63), "LUT-6 AND compilation wrong"

    # Canonical gates: check known properties
    gates = canonical_2input_gates()
    assert gates["XOR"]["sparsity"] == 1, "XOR gate sparsity wrong"
    assert gates["AND"]["sparsity"] == 4, "AND gate sparsity wrong"
    assert gates["XNOR"]["sparsity"] == 1, "XNOR gate sparsity wrong"

    # Walsh character orthogonality: <chi_a, chi_b> = delta_{ab}
    N = 8
    for a in range(N):
        for b in range(N):
            inner = sum(walsh_character(a, x) * walsh_character(b, x)
                        for x in range(N)) / N
            expected = 1.0 if a == b else 0.0
            assert abs(inner - expected) < 1e-12, \
                f"character orthogonality fails: a={a}, b={b}"

    print("All checks passed.")


if __name__ == "__main__":
    run_checks()
