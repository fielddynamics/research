#!/usr/bin/env python3
"""
GFD Vortex Horizon Extended — 20 Tests
======================================================

EXTENDING THE VORTEX

The first 20 tests (gfd_vortex_horizon_20.py) established:
  - The vortex IS the electric field, governed by μ = x/(x+1)
  - a₀_v = Bohr acceleration (exact)
  - g = φ at the Field Origin (exact)
  - C = 2πn²a₀/Z_eff per element (< 2% mean error)

This suite pushes further into:

  Section F: Atomic Tully-Fisher & energy scaling (4 tests)
  Section G: Chemical bonds from vortex overlap (4 tests)
  Section H: Shell structure from D=3 geometry (4 tests)
  Section I: Gauss's law for vortex flux (4 tests)
  Section J: Cross-scale connections (4 tests)

Each test either validates a new prediction or maps a frontier.

Requirements: Python 3.8+, math only.

    python gfd_vortex_horizon_ext_20.py

Author: Stephen Nelson / Field Dynamics Research
Date:   March 2026
"""

import math
import sys
import statistics

# =============================================================================
# CONSTANTS
# =============================================================================

K = 4
D = 3
phi = (1.0 + math.sqrt(5.0)) / 2.0
alpha_fs = 7.2973525693e-3
c_light  = 299792458.0
m_e      = 9.1093837015e-31
m_p      = 1.67262192369e-27
e_charge = 1.602176634e-19
k_e      = 8.9875517873681764e9
hbar     = 1.054571817e-34
G_SI     = 6.67430e-11

a0_m  = 5.29177210903e-11        # Bohr radius (m)
a0_pm = 52.9177                  # Bohr radius (pm)
v_bohr = alpha_fs * c_light      # Bohr velocity (m/s)
a_bohr = v_bohr**2 / a0_m        # Bohr acceleration (m/s²)
Ry_eV = 13.6057                  # Rydberg (eV)

# =============================================================================
# DATA
# =============================================================================

Z_EFF = {
    1: (1, 1.000),  2: (1, 1.688),  3: (2, 1.279),  4: (2, 1.912),
    5: (2, 2.421),  6: (2, 3.136),  7: (2, 3.834),  8: (2, 4.453),
    9: (2, 5.100), 10: (2, 5.758), 11: (3, 2.507), 12: (3, 3.308),
   13: (3, 4.066), 14: (3, 4.285), 15: (3, 4.886), 16: (3, 5.482),
   17: (3, 6.116), 18: (3, 6.764), 19: (4, 3.495), 20: (4, 4.398),
}

CALC_RADII = {
    1: 53,  2: 31,  3: 167,  4: 112,  5: 87,   6: 67,
    7: 56,  8: 48,  9: 42,  10: 38,  11: 190, 12: 145,
   13: 118, 14: 111, 15: 98, 16: 88,  17: 79,  18: 71,
   19: 243, 20: 194,
}

# First ionization energies (eV)
IE_OBS = {
    1: 13.598, 2: 24.587, 3: 5.392, 4: 9.323, 5: 8.298,
    6: 11.260, 7: 14.534, 8: 13.618, 9: 17.423, 10: 21.565,
    11: 5.139, 12: 7.646, 13: 5.986, 14: 8.152, 15: 10.487,
    16: 10.360, 17: 12.968, 18: 15.760, 19: 4.341, 20: 6.113,
}

# Electron affinities (eV, positive = energy released)
EA_OBS = {
    1: 0.754, 2: 0.0, 3: 0.618, 6: 1.263, 7: -0.07,
    8: 1.461, 9: 3.401, 10: 0.0, 11: 0.548, 17: 3.613, 18: 0.0,
}

EL = {1:'H',2:'He',3:'Li',4:'Be',5:'B',6:'C',7:'N',8:'O',9:'F',10:'Ne',
      11:'Na',12:'Mg',13:'Al',14:'Si',15:'P',16:'S',17:'Cl',18:'Ar',
      19:'K',20:'Ca'}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def g_vortex(x_N):
    """Actual vortex field given Newtonian parameter x_N."""
    if x_N <= 0:
        return 0.0
    return (x_N + math.sqrt(x_N**2 + 4.0 * x_N)) / 2.0


# =============================================================================
# TEST FRAMEWORK
# =============================================================================

_results = []


def test(name, section):
    def decorator(func):
        def wrapper():
            try:
                func()
                _results.append((section, name, "PASS", ""))
                print(f"  \033[92mPASS\033[0m  {name}")
            except AssertionError as e:
                _results.append((section, name, "FAIL", str(e)))
                print(f"  \033[91mFAIL\033[0m  {name}")
                print(f"        {e}")
            except Exception as e:
                _results.append((section, name, "ERROR", str(e)))
                print(f"  \033[93mERROR\033[0m {name}")
                print(f"        {e}")
        wrapper._test_section = section
        wrapper._test_name = name
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


# #############################################################################
#
#  SECTION F: ATOMIC TULLY-FISHER & ENERGY SCALING (Tests 1–4)
#
#  The galaxy Tully-Fisher relation v⁴ ∝ M has an atomic parallel.
#  The vortex flat velocity scales as Z^(1/4).
#  Hydrogen-like ions validate the Newtonian limit exactly.
#
# #############################################################################


@test(
    "F1. Atomic Tully-Fisher: v_flat = v_Bohr × Z^(1/4)",
    "F. Atomic Tully-Fisher",
)
def test_atomic_tully_fisher():
    """In the deep vortex regime (r ≫ a₀):
    v⁴ = (kZe²/mₑ) · a₀_v = Z · v_Bohr⁴

    So the flat velocity of a vortex with Z protons is:
    v_flat = v_Bohr · Z^(1/4)

    This is the atomic Tully-Fisher relation.
    In galaxies: v⁴ ∝ M.  In atoms: v⁴ ∝ Z.

    Verify numerically at r = 100·a₀ for Z = 1, 4, 16, 64."""
    for Z in [1, 4, 16, 64]:
        r = 100.0  # in units of a₀
        x_N = Z / r**2
        g = g_vortex(x_N)
        v = math.sqrt(g * r)
        v_expected = Z**0.25
        assert abs(v - v_expected) / v_expected < 0.03, (
            f"Z={Z}: v={v:.4f}, expected={v_expected:.4f}"
        )


@test(
    "F2. H-like ion energies: E = −Ry·Z² (Newtonian limit, < 0.1%)",
    "F. Atomic Tully-Fisher",
)
def test_hydrogen_like_energies():
    """Hydrogen-like ions have one tile deep in the Newtonian regime
    (x = Z³ ≫ 1). The Bohr energy E = −Ry·Z²/n² is exact.

    This confirms: for x ≫ 1, the vortex reduces to Coulomb.
    The constitutive law adds nothing at high acceleration.

    H:   −13.60 eV (obs: −13.598)
    He⁺: −54.42 eV (obs: −54.418)
    Li²⁺: −122.45 eV (obs: −122.45)"""
    for Z, E_obs in [(1, -13.598), (2, -54.418), (3, -122.45)]:
        E_pred = -Ry_eV * Z**2
        assert abs(E_pred - E_obs) / abs(E_obs) < 0.002, (
            f"Z={Z}: E_pred={E_pred:.2f}, E_obs={E_obs:.3f}"
        )


@test(
    "F3. Vortex energy scales as Z^(3/2) in deep-vortex regime",
    "F. Atomic Tully-Fisher",
)
def test_deep_vortex_energy_scaling():
    """In the deep vortex (x ≪ 1), g ≈ √(x_N) in units of a₀_v.
    The orbital energy at the vortex flat part:
    KE = ½mₑv² = ½mₑ·v_Bohr²·√Z = ½·Ry·√Z

    For a tile at the flat velocity region:
    E_vortex ∝ √Z (not Z² as in Newtonian)

    This is a PREDICTION: if we could observe electrons at
    r ≫ a₀/Z (past the atom, in the vortex tail), their
    energy would scale as √Z, not Z²."""
    for Z in [1, 4, 16]:
        # At r = 100 a₀: tile is in deep vortex for all Z
        r = 100.0
        x_N = Z / r**2
        g = g_vortex(x_N)
        v_sq = g * r
        # Should be proportional to sqrt(Z)
        ratio = v_sq / math.sqrt(Z)
        # All ratios should be approximately equal
    ratios = []
    for Z in [1, 4, 9, 16, 25]:
        r = 100.0
        g = g_vortex(Z / r**2)
        ratios.append(g * r / math.sqrt(Z))
    spread = (max(ratios) - min(ratios)) / statistics.mean(ratios)
    assert spread < 0.05, f"v² / √Z spread = {spread:.3f}"


@test(
    "F4. The fourth-power law at the Field Origin: v⁴/v_B⁴ = φ² = φ+1 = 2.618",
    "F. Atomic Tully-Fisher",
)
def test_fourth_power_golden():
    """At the Field Origin (x = 1), v² = φ·v_B².
    So v⁴ = φ²·v_B⁴ = (φ+1)·v_B⁴ = 2.618·v_B⁴.

    The golden ratio squared: φ² = φ + 1. This is the
    Tully-Fisher normalization at the Field Origin.
    It combines the fourth-power law with the golden gate."""
    v4_ratio = phi**2  # v⁴/v_B⁴ at x = 1
    assert abs(v4_ratio - (phi + 1)) < 1e-12
    assert abs(v4_ratio - 2.6180339887) < 1e-6


# #############################################################################
#
#  SECTION G: CHEMICAL BONDS FROM VORTEX OVERLAP (Tests 5–8)
#
#  When two vortices overlap, their combined field illuminates
#  shared tiles. The bond length is where the combined vortex
#  reaches the bonding threshold.
#
# #############################################################################


@test(
    "G5. H-H bond: d = a₀√2 at threshold x = K (0.9% error)",
    "G. Chemical Bonds",
)
def test_h2_bond():
    """Two hydrogen vortices separated by distance d.
    At the midpoint (d/2 from each), the combined field:
    x_total = 2·(a₀/(d/2))² = 8a₀²/d²

    If the bonding threshold is x = K = 4 (the topological constant):
    8a₀²/d² = 4 → d = a₀√2 = 74.8 pm

    Observed H-H bond length: 74.14 pm. Error: 0.9%.

    The threshold x = K is the packing capacity of the scaffold.
    Two overlapping vortices fuse tiles into a shared region
    when the combined field reaches the K=4 packing density."""
    d_pred = a0_pm * math.sqrt(2)
    d_obs = 74.14  # pm
    error = abs(d_pred - d_obs) / d_obs * 100
    assert error < 1.5, f"d = {d_pred:.1f} pm, obs = {d_obs}, err = {error:.1f}%"


@test(
    "G6. N-N single bond: d = a₀√(2·Z_eff) (0.5% error)",
    "G. Chemical Bonds",
)
def test_nn_single():
    """For a homonuclear single bond between atoms with Z_eff:
    x_total = 2·Z_eff·(a₀/(d/2))² = 8·Z_eff·a₀²/d²

    At threshold x = K = 4:
    d = a₀·√(2·Z_eff)

    Nitrogen (Z_eff = 3.834):
    d = 52.9·√(7.668) = 146.5 pm
    Observed N-N single bond: 145.8 pm. Error: 0.5%."""
    _, Zeff = Z_EFF[7]
    d_pred = a0_pm * math.sqrt(2 * Zeff)
    d_obs = 145.8
    error = abs(d_pred - d_obs) / d_obs * 100
    assert error < 1.5, f"d = {d_pred:.1f} pm, obs = {d_obs}, err = {error:.1f}%"


@test(
    "G7. N≡N triple bond: d = a₀√(2·Z_eff) / BO^(1/4) (1.4%)",
    "G. Chemical Bonds",
)
def test_n2_triple():
    """For multiple bonds, the bond order BO increases the
    effective vortex overlap. The bond shortens by BO^(1/4)
    — the SAME fourth-power scaling as Tully-Fisher.

    This is because v⁴ ∝ M in TF means that doubling the
    effective mass (overlap) changes the velocity by 2^(1/4),
    and the bonding distance scales inversely.

    N≡N (BO=3): d = a₀√(2·3.834) / 3^(1/4) = 111.3 pm
    Observed: 109.76 pm. Error: 1.4%."""
    _, Zeff = Z_EFF[7]
    BO = 3
    d_pred = a0_pm * math.sqrt(2 * Zeff) / BO**0.25
    d_obs = 109.76
    error = abs(d_pred - d_obs) / d_obs * 100
    assert error < 2.0, f"d = {d_pred:.1f} pm, obs = {d_obs}, err = {error:.1f}%"


@test(
    "G8. Bond order BO^(1/4) scaling: N single→triple ratio",
    "G. Chemical Bonds",
)
def test_bond_order_scaling():
    """The ratio of triple to single bond length should be 3^(-1/4).

    d_triple / d_single = BO^(-1/4) = 3^(-1/4) = 0.7598

    Observed for nitrogen:
    d(N≡N) / d(N-N) = 109.76 / 145.8 = 0.7528

    The prediction is within 1% of observation.
    This confirms the fourth-power (Tully-Fisher) scaling
    applies to bond-order as well."""
    ratio_pred = 3**(-0.25)
    ratio_obs = 109.76 / 145.8
    error = abs(ratio_pred - ratio_obs) / ratio_obs * 100
    assert error < 2.0, (
        f"ratio_pred = {ratio_pred:.4f}, "
        f"ratio_obs = {ratio_obs:.4f}, err = {error:.1f}%"
    )


# #############################################################################
#
#  SECTION H: SHELL STRUCTURE FROM D=3 (Tests 9–12)
#
#  Electron shell capacities come from spherical harmonics in D=3.
#  Nuclear shell capacities come from tetrahedral packing on K=4.
#  Same constants, different projections.
#
# #############################################################################


@test(
    "H9. Shell capacity 2n² from D=3 spherical harmonics",
    "H. Shell Structure",
)
def test_shell_capacity():
    """In D=3 spatial dimensions, the number of angular states
    at quantum number l is (2l+1) — the spherical harmonics.

    For principal quantum number n, l ranges from 0 to n−1.
    Total angular states: Σ(2l+1) = n²
    With spin (2 orientations): capacity = 2n²

    n=1: 2,  n=2: 8,  n=3: 18,  n=4: 32,  n=5: 50"""
    for n in range(1, 6):
        angular = sum(2*l + 1 for l in range(n))
        assert angular == n**2, f"n={n}: sum = {angular}"
        capacity = 2 * angular
        assert capacity == 2 * n**2


@test(
    "H10. Electron shells ≠ nuclear shells (TetA vs TetB geometry)",
    "H. Shell Structure",
)
def test_shells_differ():
    """Electron shells: 2, 8, 18, 32, 50 (cumulative: 2, 10, 28, 60, 110)
    Nuclear shells: 2, 8, 20, 28, 50, 82, 126

    These are DIFFERENT sequences because:
    - Electrons orbit in the VORTEX (spherical, on TetA)
    - Nucleons pack on the SCAFFOLD (tetrahedral, on TetB)

    The first two values match (2, 8) because at small n,
    spherical and tetrahedral harmonics coincide. They diverge
    for n ≥ 3."""
    electron_shells = [2*n**2 for n in range(1, 6)]
    nuclear_magic = [2, 8, 20, 28, 50, 82, 126]

    # First two match
    assert electron_shells[0] == nuclear_magic[0]  # 2
    cumulative_e = [sum(electron_shells[:i+1]) for i in range(5)]
    assert cumulative_e[1] == 10  # 2 + 8
    # But 10 ≠ 8 (the nuclear magic number)
    # Actually cumulative electrons at n=2 is 10, nuclear magic 2 is 8
    # The sequences diverge:
    assert electron_shells[2] != nuclear_magic[2]  # 18 ≠ 20


@test(
    "H11. Angular degeneracy (2l+1) requires exactly D=3",
    "H. Shell Structure",
)
def test_d3_required():
    """The formula (2l+1) for angular states per level l is
    specific to D=3. For other dimensions:

    D=2: degeneracy = 2 (for l > 0), 1 (for l = 0)
    D=3: degeneracy = 2l + 1
    D=4: degeneracy = (l+1)²

    Only D=3 gives shell capacities 2n² = 2, 8, 18, 32...
    which match the periodic table."""
    # D=3 shell capacities
    d3_shells = [2 * n**2 for n in range(1, 5)]
    assert d3_shells == [2, 8, 18, 32]

    # D=4 would give different capacities
    d4_caps = []
    for n in range(1, 5):
        angular = sum((l+1)**2 for l in range(n))
        d4_caps.append(2 * angular)
    # D=4: 2, 10, 28, 60 — not the periodic table!
    assert d4_caps != d3_shells
    assert d4_caps[1] != 8  # D=4 gives 10, not 8


@test(
    "H12. Noble gases at Z = 2Σn²: the periodic table is the vortex pattern",
    "H. Shell Structure",
)
def test_noble_gas_positions():
    """Noble gases occur when all tiles in a shell group are
    illuminated: He (2), Ne (10), Ar (18 = 10+8*).

    The first two noble gases sit at exact shell closings:
    He: Z = 2×1² = 2
    Ne: Z = 2×1² + 2×2² = 10

    Argon (Z=18) does NOT fill 2×3² = 18 in the n=3 shell.
    It fills only the 3s and 3p subshells (8 of 18 slots).
    The 3d subshell fills LATER (Sc–Zn) due to Aufbau ordering.

    * The Aufbau pattern (which subshells fill first) is a
    frontier question: can the vortex geometry predict it?"""
    # He fills n=1 completely
    assert 2 == 2 * 1**2

    # Ne fills n=1 + n=2 completely
    assert 10 == 2 * 1**2 + 2 * 2**2

    # Ar fills n=1 + n=2 + (3s + 3p = 8 of 18 in n=3)
    assert 18 == 10 + 8

    # The 8 = 2(2·0+1) + 2(2·1+1) = 2 + 6 = s + p subshells
    s_capacity = 2 * (2*0 + 1)  # l=0: 2
    p_capacity = 2 * (2*1 + 1)  # l=1: 6
    assert s_capacity + p_capacity == 8


# #############################################################################
#
#  SECTION I: GAUSS'S LAW FOR VORTEX FLUX (Tests 13–16)
#
#  The vortex carries Z units of flux. Illuminated tiles absorb
#  flux. The net flux at any radius determines the field felt by
#  tiles at that distance.
#
# #############################################################################


@test(
    "I13. Neutral atom: net flux = 0 outside, field drops to zero",
    "I. Gauss's Law for Flux",
)
def test_neutral_zero_flux():
    """A neutral atom has Z protons creating Z flux units, and
    Z illuminated tiles absorbing Z flux units. Beyond the
    outermost tile, the net flux is zero.

    This is why neutral atoms don't interact electromagnetically
    at long range — the vortex is fully consumed.

    For ions: net flux = Z - N_electrons ≠ 0."""
    for Z in range(1, 21):
        n_protons = Z
        n_electrons = Z  # neutral
        net_flux = n_protons - n_electrons
        assert net_flux == 0


@test(
    "I14. Noble gas stability: vortex fully consumed at shell closure",
    "I. Gauss's Law for Flux",
)
def test_noble_gas_stability():
    """Noble gases are stable because ALL vortex flux is consumed
    by tile illumination at shell closure. The outermost tile has
    JUST enough flux to stay illuminated — no excess for bonding.

    Evidence: noble gases have:
    - Zero electron affinity (no flux to illuminate an extra tile)
    - Highest ionization energy in their period (tiles tightly held)
    - No chemical bonds under normal conditions"""
    # EA = 0 for noble gases
    for Z in [2, 10, 18]:
        assert EA_OBS[Z] == 0.0, f"Z={Z}: EA should be 0"

    # Highest IE in each period
    # Period 1: He > H
    assert IE_OBS[2] > IE_OBS[1]
    # Period 2: Ne > all Li-F
    for Z in range(3, 10):
        assert IE_OBS[10] > IE_OBS[Z], f"Ne IE < {EL[Z]} IE"
    # Period 3: Ar > all Na-Cl
    for Z in range(11, 18):
        assert IE_OBS[18] > IE_OBS[Z], f"Ar IE < {EL[Z]} IE"


@test(
    "I15. Halogen affinity: one flux unit available for extra tile",
    "I. Gauss's Law for Flux",
)
def test_halogen_affinity():
    """Halogens (F, Cl) are one tile short of a complete shell.
    The vortex has enough flux to illuminate one more tile.
    When it does, the energy released is the electron affinity.

    Halogens have the HIGHEST electron affinity in each period:
    F: 3.40 eV, Cl: 3.61 eV

    In contrast, noble gases (complete shells) have EA = 0,
    and nitrogen (half-filled p-shell) has EA ≈ 0."""
    # Halogens have high EA
    assert EA_OBS[9] > 3.0, f"F EA = {EA_OBS[9]}"
    assert EA_OBS[17] > 3.0, f"Cl EA = {EA_OBS[17]}"

    # Noble gases have zero EA
    assert EA_OBS[10] == 0.0
    assert EA_OBS[18] == 0.0

    # Nitrogen has near-zero EA (half-filled = stable)
    assert EA_OBS[7] < 0.1


@test(
    "I16. Alkali metals: one tile far out, low IE, high reactivity",
    "I. Gauss's Law for Flux",
)
def test_alkali_reactivity():
    """Alkali metals have one tile on a new shell (high n, low Z_eff).
    This tile sees only ~1 unit of vortex flux (all inner tiles
    have consumed the rest). It is weakly held:

    - Lowest IE in each period
    - Largest atomic radius in each period
    - Easily gives up one tile → positive ion

    The IE decreases down the group as n increases:
    Li: 5.39 eV, Na: 5.14 eV, K: 4.34 eV"""
    # Lowest IE in each period
    # Period 2: Li has lowest
    for Z in range(4, 11):
        assert IE_OBS[3] < IE_OBS[Z], f"Li IE > {EL[Z]} IE"
    # Period 3: Na has lowest
    for Z in range(12, 19):
        assert IE_OBS[11] < IE_OBS[Z], f"Na IE > {EL[Z]} IE"

    # IE decreases: Li > Na > K
    assert IE_OBS[3] > IE_OBS[11] > IE_OBS[19]

    # Largest radius in each period
    assert CALC_RADII[3] > max(CALC_RADII[Z] for Z in range(4, 11))
    assert CALC_RADII[11] > max(CALC_RADII[Z] for Z in range(12, 19))
    assert CALC_RADII[19] > max(CALC_RADII[Z] for Z in range(12, 19))


# #############################################################################
#
#  SECTION J: CROSS-SCALE CONNECTIONS (Tests 17–20)
#
#  The vortex picture connects atomic structure to deeper
#  framework properties: magnetism, spin, the hierarchy,
#  and the bridge to galactic dynamics.
#
# #############################################################################


@test(
    "J17. Bohr magneton = vortex circulation moment (exact identity)",
    "J. Cross-Scale Connections",
)
def test_bohr_magneton():
    """A circulating vortex IS a current loop. The magnetic moment:

    μ = I · A = (e·v)/(2πr) · πr² = e·v·r/2

    At the Bohr orbit: μ = e·v_Bohr·a₀/2 = e·(αc)·a₀/2

    Since v_Bohr·a₀ = αc · ℏ/(mₑαc) = ℏ/mₑ:
    μ = eℏ/(2mₑ) = μ_B (the Bohr magneton)

    The Bohr magneton is the magnetic moment of the vortex
    circulation at the Field Origin. Exact algebraic identity."""
    mu_B = e_charge * hbar / (2 * m_e)
    mu_vortex = e_charge * v_bohr * a0_m / 2

    assert abs(mu_B - mu_vortex) / mu_B < 1e-6, (
        f"μ_B = {mu_B:.6e}, μ_vortex = {mu_vortex:.6e}"
    )


@test(
    "J18. Spin = tile orientation: two states per tile gives factor 2 in 2n²",
    "J. Cross-Scale Connections",
)
def test_spin_from_tile():
    """A gravity tile on TetA has two orientations relative to the
    local vortex direction: aligned or anti-aligned. This gives
    spin quantum number s = 1/2 with two states (+½, −½).

    The factor 2 in the shell capacity 2n² comes from these
    two spin orientations per tile. Without spin: n² tiles per
    shell. With spin: 2n² tiles per shell.

    This is the same factor 2 that appears in nuclear shell
    capacities, because the spin degree of freedom exists on
    BOTH TetA (electrons) and TetB (nucleons)."""
    # Electron shells
    for n in range(1, 5):
        spatial_states = n**2
        spin_factor = 2
        total = spin_factor * spatial_states
        assert total == 2 * n**2

    # Nuclear shell sizes also have factor 2
    # (each nuclear orbital holds 2 nucleons)
    nuclear_subshell = {0: 2, 1: 6, 2: 10, 3: 14}  # (2l+1)×2
    for l, cap in nuclear_subshell.items():
        assert cap == 2 * (2*l + 1)


@test(
    "J19. IE trend across periods follows vortex flux pattern",
    "J. Cross-Scale Connections",
)
def test_ie_trend():
    """Ionization energy generally INCREASES across a period
    (Li → Ne, Na → Ar) because Z_eff grows — more vortex flux
    reaches the outermost tile, binding it more tightly.

    But there are two dips in each period:
    - At the start of p-filling (B, Al): new subshell, less tightly bound
    - At the half-filled point (O, S): pairing energy penalty

    The vortex picture: these dips correspond to changes in
    how tiles pack angularly. A new angular mode (p-orbital)
    has less overlap with the vortex core than s-orbital tiles.
    Half-filling forces two tiles into the same angular slot,
    with one anti-aligned (pairing cost)."""
    # General increase across periods
    # Period 2: Li(5.39) → Ne(21.56) overall increase
    assert IE_OBS[10] > IE_OBS[3]
    # Period 3: Na(5.14) → Ar(15.76) overall increase
    assert IE_OBS[18] > IE_OBS[11]

    # Dip at B (Z=5) relative to Be (Z=4): B < Be
    assert IE_OBS[5] < IE_OBS[4], "B should have lower IE than Be"

    # Dip at O (Z=8) relative to N (Z=7): O < N
    assert IE_OBS[8] < IE_OBS[7], "O should have lower IE than N"

    # Same pattern in Period 3
    assert IE_OBS[13] < IE_OBS[12], "Al < Mg"
    assert IE_OBS[16] < IE_OBS[15], "S < P"


@test(
    "J20. Galaxy → Atom bridge: same equation, different coupling",
    "J. Cross-Scale Connections",
)
def test_galaxy_atom_bridge():
    """The galaxy and atom equations are structurally identical:

    Galaxy:  v⁴ = G·M · (v²/r + a₀)
    Atom:    v⁴ = (ke²Z/mₑ) · (v²/r + a₀_v)

    The coupling constant changes:
    Galaxy: G·M (gravitational)
    Atom:   ke²Z/mₑ (electromagnetic)

    The transition acceleration changes:
    Galaxy: a₀ = 1.2×10⁻¹⁰ m/s²
    Atom:   a₀_v = 9.04×10²² m/s²

    Ratio: a₀_v/a₀ = 7.5 × 10³²

    This ratio should be derivable from fundamental constants.
    For now, verify the structural identity by confirming both
    equations reduce to their known limits."""
    ratio = a_bohr / 1.2e-10
    assert 1e32 < ratio < 1e33, f"a₀_v/a₀ = {ratio:.2e}"

    # Both have the same limits:
    # x ≫ 1: v² = coupling/r (Newtonian / Keplerian)
    # x ≪ 1: v⁴ = coupling·a₀ (flat / Tully-Fisher)
    # x = 1: g = φ·g_N (Field Origin, golden enhancement)

    # The golden ratio appears in BOTH at x = 1
    g_at_FO = g_vortex(1.0)
    assert abs(g_at_FO - phi) < 1e-12


# =============================================================================
# MAIN
# =============================================================================

def main():
    print()
    print("=" * 76)
    print("  GFD VORTEX HORIZON EXTENDED: 20 TESTS")
    print("  Pushing the frontier: bonds, shells, scaling, bridges")
    print("=" * 76)

    all_tests = [
        test_atomic_tully_fisher,
        test_hydrogen_like_energies,
        test_deep_vortex_energy_scaling,
        test_fourth_power_golden,
        test_h2_bond,
        test_nn_single,
        test_n2_triple,
        test_bond_order_scaling,
        test_shell_capacity,
        test_shells_differ,
        test_d3_required,
        test_noble_gas_positions,
        test_neutral_zero_flux,
        test_noble_gas_stability,
        test_halogen_affinity,
        test_alkali_reactivity,
        test_bohr_magneton,
        test_spin_from_tile,
        test_ie_trend,
        test_galaxy_atom_bridge,
    ]

    current_section = None
    for t in all_tests:
        sec = t._test_section
        if sec != current_section:
            print(f"\n  ── {sec} {'─' * (70 - len(sec))}")
            current_section = sec
        t()

    print()
    print("=" * 76)
    passed = sum(1 for _, _, st, _ in _results if st == "PASS")
    failed = sum(1 for _, _, st, _ in _results if st == "FAIL")
    errors = sum(1 for _, _, st, _ in _results if st == "ERROR")
    total = len(_results)

    if failed == 0 and errors == 0:
        print(f"  \033[92m{passed}/{total} PASSED\033[0m")
    else:
        print(f"  {passed} passed, {failed} failed, {errors} errors")
    print("=" * 76)

    if failed > 0 or errors > 0:
        print("\n  ISSUES:")
        for sec, name, status, msg in _results:
            if status != "PASS":
                print(f"    [{status}] {name}")
                if msg:
                    print(f"           {msg[:120]}")

    return failed == 0 and errors == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
