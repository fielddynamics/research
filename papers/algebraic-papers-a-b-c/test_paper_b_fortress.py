"""
Paper B Fortress Tests: 20 tests pushing on every claim in the letter.

Each test targets a specific sentence or claim in the paper.
If any test fails, the corresponding claim needs revision.

Master Nelson / Field Dynamics Research
"""

import unittest
import itertools
import numpy as np
from collections import Counter
import math


def sign_perm(sigma):
    n = len(sigma)
    visited = [False] * n
    s = 1
    for i in range(n):
        if not visited[i]:
            j, cycle_len = i, 0
            while not visited[j]:
                visited[j] = True
                j = sigma[j]
                cycle_len += 1
            if cycle_len % 2 == 0:
                s *= -1
    return s


def cycle_type(sigma):
    n = len(sigma)
    visited = [False] * n
    cycles = []
    for i in range(n):
        if not visited[i]:
            j, length = i, 0
            while not visited[j]:
                visited[j] = True
                j = sigma[j]
                length += 1
            cycles.append(length)
    return tuple(sorted(cycles, reverse=True))


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def chi_V(sigma):
    return sum(1 for i in range(len(sigma)) if sigma[i] == i)


def chi_V_sq(sigma):
    sq = tuple(sigma[sigma[i]] for i in range(len(sigma)))
    return chi_V(sq)


# S₄ character table
CLASS_SIZES = {(1,1,1,1): 1, (2,1,1): 6, (3,1): 8, (4,): 6, (2,2): 3}
CHAR_TABLE = {
    'trivial':  {(1,1,1,1): 1, (2,1,1): 1,  (3,1): 1,  (4,): 1,  (2,2): 1},
    'sign':     {(1,1,1,1): 1, (2,1,1): -1, (3,1): 1,  (4,): -1, (2,2): 1},
    'V2':       {(1,1,1,1): 2, (2,1,1): 0,  (3,1): -1, (4,): 0,  (2,2): 2},
    'V3':       {(1,1,1,1): 3, (2,1,1): 1,  (3,1): 0,  (4,): -1, (2,2): -1},
    'V3sign':   {(1,1,1,1): 3, (2,1,1): -1, (3,1): 0,  (4,): 1,  (2,2): -1},
}


def inner_product(chi1, chi2):
    total = 0
    for ct, size in CLASS_SIZES.items():
        total += size * chi1[ct] * chi2[ct]
    return total // 24


class TestPaperBFortress(unittest.TestCase):

    def setUp(self):
        self.S4 = list(itertools.permutations(range(4)))
        self.K = 4

    # ============================================================
    # CLAIM: "K³ = 64 independent components"
    # ============================================================
    def test_01_connection_has_K_cubed_components(self):
        """Paper claims Γᵃ_bc has K³ = 64 components.
        This is three frame indices, each running over K=4 values.
        Verify: 4³ = 64."""
        K = self.K
        self.assertEqual(K**3, 64)
        # Also verify: this equals 2^6
        self.assertEqual(K**3, 2**6)
        # Which means K=4 is special: K³ is a power of 2
        # only when K is a power of 2
        self.assertTrue(math.log2(K).is_integer())

    # ============================================================
    # CLAIM: "40 in the lower-index symmetric sector...
    #         24 in the lower-index antisymmetric sector"
    # ============================================================
    def test_02_symmetric_antisymmetric_split(self):
        """Paper claims 40 symmetric + 24 antisymmetric = 64.
        Sym: K × K(K+1)/2 = 4 × 10 = 40.
        Anti: K × K(K-1)/2 = 4 × 6 = 24."""
        K = self.K
        sym = K * K * (K + 1) // 2
        anti = K * K * (K - 1) // 2
        self.assertEqual(sym, 40)
        self.assertEqual(anti, 24)
        self.assertEqual(sym + anti, K**3)

    # ============================================================
    # CLAIM: "Any tensor whose indices run over a set of size K
    #         inherits a canonical S_K action"
    # ============================================================
    def test_03_S4_acts_on_connection_space(self):
        """Verify S₄ acts on the full K³ = 64 component space.
        σ sends Γᵃ_bc → Γ^{σ(a)}_{σ(b)σ(c)}.
        This is a well-defined action: (στ)·Γ = σ·(τ·Γ)."""
        # Build all 64 component triples
        triples = [(a, b, c) for a in range(4) for b in range(4) for c in range(4)]
        self.assertEqual(len(triples), 64)
        
        # Verify group action property: (s1∘s2)·Γ = s1·(s2·Γ)
        s1 = (1, 0, 2, 3)  # (01)
        s2 = (0, 2, 1, 3)  # (12)
        s12 = compose(s1, s2)  # s1 ∘ s2: apply s2 first, then s1
        
        for a, b, c in triples[:10]:
            # Apply s2 first
            step1 = (s2[a], s2[b], s2[c])
            # Then s1
            step2 = (s1[step1[0]], s1[step1[1]], s1[step1[2]])
            # s12 directly
            direct = (s12[a], s12[b], s12[c])
            self.assertEqual(step2, direct)

    # ============================================================
    # CLAIM: "χ_V(σ) counts fixed frame labels; it does not
    #         evaluate any inner product"
    # ============================================================
    def test_04_chi_V_is_purely_combinatorial(self):
        """χ_V only counts |{a : σ(a) = a}|. No inner product,
        no metric, no η anywhere."""
        for sigma in self.S4:
            chi = chi_V(sigma)
            fixed = sum(1 for i in range(4) if sigma[i] == i)
            self.assertEqual(chi, fixed)
            # This is an integer count, bounded by K
            self.assertGreaterEqual(chi, 0)
            self.assertLessEqual(chi, 4)

    # ============================================================
    # CLAIM: "χ_{Λ²V}(σ) = (χ_V(σ)² - χ_V(σ²))/2"
    # ============================================================
    def test_05_exterior_square_character_formula(self):
        """Verify the standard formula by direct computation
        on the 6 basis elements e_i ∧ e_j (i<j)."""
        pairs = [(i, j) for i in range(4) for j in range(i+1, 4)]
        self.assertEqual(len(pairs), 6)
        
        for sigma in self.S4:
            # Direct trace computation on Λ²V
            trace = 0
            for i, j in pairs:
                si, sj = sigma[i], sigma[j]
                if si < sj and (si, sj) == (i, j):
                    trace += 1
                elif si > sj and (sj, si) == (i, j):
                    trace -= 1
            # Compare with formula
            formula = (chi_V(sigma)**2 - chi_V_sq(sigma)) // 2
            self.assertEqual(trace, formula)

    # ============================================================
    # CLAIM: The character table in Section 3
    # ============================================================
    def test_06_torsion_character_is_24_0_0_0_0(self):
        """χ_{V⊗Λ²V}(σ) = χ_V(σ) · χ_{Λ²V}(σ).
        Must be (24, 0, 0, 0, 0)."""
        chi_torsion = {}
        for sigma in self.S4:
            ct = cycle_type(sigma)
            chi_lam2 = (chi_V(sigma)**2 - chi_V_sq(sigma)) // 2
            val = chi_V(sigma) * chi_lam2
            if ct not in chi_torsion:
                chi_torsion[ct] = val
            else:
                self.assertEqual(chi_torsion[ct], val)
        self.assertEqual(chi_torsion[(1,1,1,1)], 24)
        self.assertEqual(chi_torsion[(2,1,1)], 0)
        self.assertEqual(chi_torsion[(3,1)], 0)
        self.assertEqual(chi_torsion[(4,)], 0)
        self.assertEqual(chi_torsion[(2,2)], 0)

    # ============================================================
    # CLAIM: "A representation whose character equals |G| on the
    #         identity and vanishes on every other group element
    #         is the regular representation"
    # ============================================================
    def test_07_regular_rep_definition_check(self):
        """Verify this is a standard theorem: the regular rep
        is the UNIQUE rep with this character. Check by computing
        the inner product with each irrep."""
        chi_torsion = {(1,1,1,1): 24, (2,1,1): 0,
                       (3,1): 0, (4,): 0, (2,2): 0}
        for name, chi_irrep in CHAR_TABLE.items():
            mult = inner_product(chi_torsion, chi_irrep)
            dim = chi_irrep[(1,1,1,1)]
            # Regular rep: multiplicity = dimension
            self.assertEqual(mult, dim)

    # ============================================================
    # CLAIM: "1² + 1² + 2² + 3² + 3² = 24"
    # ============================================================
    def test_08_irrep_dimension_sum(self):
        """The regular rep decomposes as Σ dim(ρ) · ρ.
        Total dimension: Σ dim(ρ)² = 24."""
        dims = [1, 1, 2, 3, 3]
        self.assertEqual(sum(d**2 for d in dims), 24)
        self.assertEqual(len(dims), 5)  # five irreps = five conjugacy classes

    # ============================================================
    # CLAIM: Self-duality "V* ≅ V as S₄-modules"
    # ============================================================
    def test_09_self_duality_of_permutation_rep(self):
        """For the permutation representation, V ≅ V* because
        permutation matrices are orthogonal: P = P^{-T}.
        So the contragredient has the same character."""
        for sigma in self.S4:
            # Character of V: number of fixed points
            chi = chi_V(sigma)
            # Character of V* (contragredient): χ_{V*}(σ) = χ_V(σ⁻¹)
            # For permutation matrices, χ(σ) = χ(σ⁻¹) because
            # number of fixed points of σ = number of fixed points of σ⁻¹
            inv = [0]*4
            for i in range(4):
                inv[sigma[i]] = i
            chi_dual = chi_V(tuple(inv))
            self.assertEqual(chi, chi_dual)

    # ============================================================
    # CLAIM: "4 × 6 = 24 vertex-edge incidences...
    #         the incidence structure of a combinatorial tetrahedron"
    # ============================================================
    def test_10_tetrahedron_incidence(self):
        """A tetrahedron has 4 vertices and C(4,2) = 6 edges.
        Torsion T^a_{[bc]}: a = vertex (4), [bc] = edge (6).
        4 × 6 = 24. Verify enumeration."""
        K = 4
        vertices = K
        edges = K * (K - 1) // 2
        incidences = vertices * edges
        self.assertEqual(vertices, 4)
        self.assertEqual(edges, 6)
        self.assertEqual(incidences, 24)
        # Enumerate explicitly
        components = [(a, b, c) for a in range(K)
                      for b in range(K) for c in range(b+1, K)]
        self.assertEqual(len(components), 24)

    # ============================================================
    # CLAIM: Christoffel character is (40, 8, 1, 0, 0)
    # ============================================================
    def test_11_christoffel_character(self):
        """V ⊗ Sym²V has character χ_V · χ_{Sym²V}.
        χ_{Sym²V}(σ) = (χ_V(σ)² + χ_V(σ²))/2."""
        chi_chris = {}
        for sigma in self.S4:
            ct = cycle_type(sigma)
            chi_sym2 = (chi_V(sigma)**2 + chi_V_sq(sigma)) // 2
            val = chi_V(sigma) * chi_sym2
            if ct not in chi_chris:
                chi_chris[ct] = val
        self.assertEqual(chi_chris[(1,1,1,1)], 40)
        self.assertEqual(chi_chris[(2,1,1)], 8)
        self.assertEqual(chi_chris[(3,1)], 1)
        self.assertEqual(chi_chris[(4,)], 0)
        self.assertEqual(chi_chris[(2,2)], 0)

    # ============================================================
    # CLAIM: "⟨χ_Chris, χ_sign⟩ = (40-48+8)/24 = 0"
    # ============================================================
    def test_12_sign_rep_zero_in_christoffel(self):
        """Explicit inner product computation matching the paper."""
        chi_chris = {(1,1,1,1): 40, (2,1,1): 8,
                     (3,1): 1, (4,): 0, (2,2): 0}
        # By hand: 1·40·1 + 6·8·(-1) + 8·1·1 + 6·0·(-1) + 3·0·1
        numerator = 1*40*1 + 6*8*(-1) + 8*1*1 + 6*0*(-1) + 3*0*1
        self.assertEqual(numerator, 40 - 48 + 8)
        self.assertEqual(numerator, 0)
        self.assertEqual(inner_product(chi_chris, CHAR_TABLE['sign']), 0)

    # ============================================================
    # CLAIM: Sign rep multiplicity 1 in torsion
    # ============================================================
    def test_13_sign_rep_one_in_torsion(self):
        """Inner product of torsion character with sign character."""
        chi_torsion = {(1,1,1,1): 24, (2,1,1): 0,
                       (3,1): 0, (4,): 0, (2,2): 0}
        mult = inner_product(chi_torsion, CHAR_TABLE['sign'])
        self.assertEqual(mult, 1)

    # ============================================================
    # CLAIM: Christoffel decomposes as 4·1 ⊕ 3·V₂ ⊕ 7·V₃ ⊕ 3·V₃⊗sgn
    # ============================================================
    def test_14_christoffel_full_decomposition(self):
        """Verify every multiplicity in the stated decomposition."""
        chi_chris = {(1,1,1,1): 40, (2,1,1): 8,
                     (3,1): 1, (4,): 0, (2,2): 0}
        mults = {name: inner_product(chi_chris, chi)
                 for name, chi in CHAR_TABLE.items()}
        self.assertEqual(mults['trivial'], 4)
        self.assertEqual(mults['sign'], 0)
        self.assertEqual(mults['V2'], 3)
        self.assertEqual(mults['V3'], 7)
        self.assertEqual(mults['V3sign'], 3)
        # Dimension check
        total = 4*1 + 0*1 + 3*2 + 7*3 + 3*3
        self.assertEqual(total, 40)

    # ============================================================
    # CLAIM: "K²(K-1)/2 = K! holds only at K ∈ {2,4}"
    # ============================================================
    def test_15_uniqueness_equation(self):
        """Check K=1 through K=20."""
        solutions = []
        for K in range(1, 21):
            lhs = K**2 * (K-1) // 2
            rhs = math.factorial(K)
            if lhs == rhs:
                solutions.append(K)
        self.assertEqual(solutions, [2, 4])

    # ============================================================
    # CLAIM: "essentially S₁ × S₃, permuting the three spacelike
    #         legs while fixing the timelike leg"
    # ============================================================
    def test_16_eta_breaks_S4_to_S1xS3(self):
        """η = diag(-1,+1,+1,+1). The subgroup of S₄ preserving
        the signature pattern fixes leg 0 and permutes {1,2,3}.
        That's S₁ × S₃ ≅ S₃, order 6."""
        eta_preserving = []
        for sigma in self.S4:
            # Must fix 0 (the timelike leg)
            if sigma[0] == 0:
                # Must permute {1,2,3} among themselves (already guaranteed)
                eta_preserving.append(sigma)
        self.assertEqual(len(eta_preserving), 6)  # |S₃| = 6
        # Verify it's a subgroup (closed under composition)
        ep_set = set(eta_preserving)
        for a in eta_preserving:
            for b in eta_preserving:
                self.assertIn(compose(a, b), ep_set)

    # ============================================================
    # CLAIM: Christoffel + torsion = full connection
    # ============================================================
    def test_17_characters_add_to_full_connection(self):
        """χ_Chris + χ_torsion = χ_{V⊗V⊗V} at every conjugacy class."""
        chi_full = {}
        for sigma in self.S4:
            ct = cycle_type(sigma)
            chi_full[ct] = chi_V(sigma)**3
        
        chi_chris = {(1,1,1,1): 40, (2,1,1): 8,
                     (3,1): 1, (4,): 0, (2,2): 0}
        chi_torsion = {(1,1,1,1): 24, (2,1,1): 0,
                       (3,1): 0, (4,): 0, (2,2): 0}
        
        for ct in chi_full:
            self.assertEqual(chi_chris[ct] + chi_torsion[ct], chi_full[ct])

    # ============================================================
    # CLAIM: The sign rep is the UNIQUE 1D parity detector
    # ============================================================
    def test_18_sign_is_unique_parity_detector(self):
        """Only two 1D irreps of S₄: trivial and sign.
        Trivial gives +1 on everything (no detection).
        Sign gives +1 on even, -1 on odd (detects parity).
        No other 1D representation exists."""
        one_dim_irreps = [name for name, chi in CHAR_TABLE.items()
                          if chi[(1,1,1,1)] == 1]
        self.assertEqual(sorted(one_dim_irreps), ['sign', 'trivial'])
        # Trivial can't detect parity
        self.assertEqual(CHAR_TABLE['trivial'][(2,1,1)], 1)  # transposition: +1
        # Sign does detect parity
        self.assertEqual(CHAR_TABLE['sign'][(2,1,1)], -1)    # transposition: -1

    # ============================================================
    # CLAIM: "the torsion-free connection, built from the
    #         40-dimensional Christoffel sector alone, has no
    #         scalar mechanism for distinguishing even from odd"
    # ============================================================
    def test_19_christoffel_cannot_distinguish_even_odd(self):
        """Without the sign rep, even and odd permutations produce
        identical scalar outputs from the Christoffel sector.
        
        Verify: the projection of the Christoffel character
        onto the sign irrep is zero. This means there is no
        1D subspace of the Christoffel sector that transforms
        as sgn(σ). Any scalar observable built from Christoffel
        components is sign-blind."""
        chi_chris = {(1,1,1,1): 40, (2,1,1): 8,
                     (3,1): 1, (4,): 0, (2,2): 0}
        
        # Sign projection is zero
        sign_mult = inner_product(chi_chris, CHAR_TABLE['sign'])
        self.assertEqual(sign_mult, 0)
        
        # But trivial projection is nonzero: Christoffel HAS scalars
        triv_mult = inner_product(chi_chris, CHAR_TABLE['trivial'])
        self.assertEqual(triv_mult, 4)
        # 4 scalar invariants exist. None of them detect parity.

    # ============================================================
    # CLAIM: The full connection has exactly 1 copy of sign rep
    # ============================================================
    def test_20_full_connection_sign_content(self):
        """The 64-component full connection V⊗V⊗V has character
        (64, 8, 1, 0, 0). The sign rep appears exactly once.
        That one copy lives in the torsion. Zero in Christoffel.
        
        This is the TOTAL sign budget of the connection:
        1 = 1 (torsion) + 0 (Christoffel).
        
        GR's torsion-free condition removes all of it."""
        chi_full = {(1,1,1,1): 64, (2,1,1): 8,
                    (3,1): 1, (4,): 0, (2,2): 0}
        sign_full = inner_product(chi_full, CHAR_TABLE['sign'])
        self.assertEqual(sign_full, 1)
        
        # Budget: torsion contributes 1, Christoffel contributes 0
        chi_torsion = {(1,1,1,1): 24, (2,1,1): 0,
                       (3,1): 0, (4,): 0, (2,2): 0}
        chi_chris = {(1,1,1,1): 40, (2,1,1): 8,
                     (3,1): 1, (4,): 0, (2,2): 0}
        sign_torsion = inner_product(chi_torsion, CHAR_TABLE['sign'])
        sign_chris = inner_product(chi_chris, CHAR_TABLE['sign'])
        self.assertEqual(sign_torsion, 1)
        self.assertEqual(sign_chris, 0)
        self.assertEqual(sign_torsion + sign_chris, sign_full)


if __name__ == '__main__':
    unittest.main(verbosity=2)
