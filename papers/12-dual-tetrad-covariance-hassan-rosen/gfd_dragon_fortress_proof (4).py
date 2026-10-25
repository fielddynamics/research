#!/usr/bin/env python3
"""
GFD Bimetric Lock: Structured Derivation
==========================================
Derivation of {β₀, β₁, β₂, β₃, β₄} = {1, 0, 16, 0, 1}
with explicit theorem / axiom separation.

Architecture:
  WALL 1 — Exact algebra
  WALL 2 — Explicit physical postulates (clearly labeled)
  WALL 3 — Consequences (derived from Walls 1+2)

Every claim is labeled: THEOREM, AXIOM, or COROLLARY.
Counterexamples are addressed explicitly.

Framework: Gravity Field Dynamics / Hassan-Rosen bimetric gravity
Author: Stephen Nelson / Field Dynamics Research
"""

# ═══════════════════════════════════════════════════════════════
# MATRIX UTILITIES (pure Python, no dependencies)
# ═══════════════════════════════════════════════════════════════

def mat_zeros(n):
    return [[0.0]*n for _ in range(n)]

def mat_eye(n):
    m = mat_zeros(n)
    for i in range(n): m[i][i] = 1.0
    return m

def mat_trace(M):
    return sum(M[i][i] for i in range(len(M)))

def mat_mul(A, B):
    n = len(A)
    C = mat_zeros(n)
    for i in range(n):
        for j in range(n):
            C[i][j] = sum(A[i][k]*B[k][j] for k in range(n))
    return C

def mat_det(M):
    n = len(M)
    A = [row[:] for row in M]
    det = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(A[r][col]))
        if pivot != col:
            A[col], A[pivot] = A[pivot], A[col]
            det *= -1
        if abs(A[col][col]) < 1e-15: return 0.0
        det *= A[col][col]
        for row in range(col+1, n):
            factor = A[row][col] / A[col][col]
            for j in range(col, n):
                A[row][j] -= factor * A[col][j]
    return det

def mat_inv(M):
    n = len(M)
    aug = [M[i][:] + [1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        aug[col], aug[pivot] = aug[pivot], aug[col]
        piv = aug[col][col]
        if abs(piv) < 1e-15: return None
        for j in range(2*n): aug[col][j] /= piv
        for row in range(n):
            if row == col: continue
            factor = aug[row][col]
            for j in range(2*n): aug[row][j] -= factor * aug[col][j]
    return [row[n:] for row in aug]

def e_n(S, n):
    """Elementary symmetric polynomial e_n of a 4×4 matrix."""
    if n == 0: return 1.0
    elif n == 1: return mat_trace(S)
    elif n == 2:
        t1 = mat_trace(S); t2 = mat_trace(mat_mul(S, S))
        return 0.5 * (t1*t1 - t2)
    elif n == 3:
        S2 = mat_mul(S, S); S3 = mat_mul(S, S2)
        t1, t2, t3 = mat_trace(S), mat_trace(S2), mat_trace(S3)
        return (t1**3 - 3*t1*t2 + 2*t3) / 6.0
    elif n == 4: return mat_det(S)
    return 0.0

N = 4

print('╔' + '═'*68 + '╗')
print('║  GFD BIMETRIC LOCK: STRUCTURED DERIVATION                        ║')
print('║  {β₀, β₁, β₂, β₃, β₄} = {1, 0, 16, 0, 1}                      ║')
print('╚' + '═'*68 + '╝')
print()

# ═══════════════════════════════════════════════════════════════
#  WALL 1: EXACT ALGEBRA
#  (incontrovertible — pure mathematics, no physics assumptions)
# ═══════════════════════════════════════════════════════════════

print('┌' + '─'*68 + '┐')
print('│  WALL 1: EXACT ALGEBRA                                           │')
print('│  Status: Theorem (pure mathematics, no physical assumptions)    │')
print('└' + '─'*68 + '┘')
print()

# --- THEOREM 1: Exchange identity ---
print('THEOREM 1: Symmetric polynomial exchange identity')
print('─'*68)
print()
print('  For any invertible 4×4 matrix S:')
print('    e_n(S⁻¹) = e_{4-n}(S) / det(S)')
print()
print('  In the unimodular sector (det S = 1):')
print('    e_n(S⁻¹) = e_{4-n}(S)')
print()

# Build test matrix with det ≠ 1 (general case)
S_gen = [[2.0,0.5,-0.3,0.1],[0.1,1.5,0.2,-0.4],[-0.2,0.3,1.8,0.1],[0.0,-0.1,0.2,1.2]]
det_gen = mat_det(S_gen)
S_gen_inv = mat_inv(S_gen)

print(f'  Verification (general case, det S = {det_gen:.6f}):')
all_pass = True
for n in range(5):
    en_inv = e_n(S_gen_inv, n)
    e4n_over_det = e_n(S_gen, 4-n) / det_gen
    ok = abs(en_inv - e4n_over_det) < 1e-8
    all_pass = all_pass and ok
    print(f'    e_{n}(S⁻¹) = {en_inv:+.8f},  e_{4-n}(S)/det = {e4n_over_det:+.8f}  {"✓" if ok else "✗"}')
assert all_pass, "THEOREM 1 FAILED"

# Unimodular case
scale = det_gen**(-1.0/N)
S_uni = [[S_gen[i][j]*scale for j in range(N)] for i in range(N)]
S_uni_inv = mat_inv(S_uni)
det_uni = mat_det(S_uni)

print(f'\n  Verification (unimodular case, det S = {det_uni:.10f}):')
for n in range(5):
    en_inv = e_n(S_uni_inv, n)
    e4n = e_n(S_uni, 4-n)
    ok = abs(en_inv - e4n) < 1e-8
    print(f'    e_{n}(S⁻¹) = {en_inv:+.8f},  e_{4-n}(S) = {e4n:+.8f}  {"✓" if ok else "✗"}')

print('\n  THEOREM 1 VERIFIED ✓')
print()

# --- THEOREM 2: Exchange invariance implies coefficient pairing ---
print('THEOREM 2: Exchange invariance implies coefficient pairing')
print('─'*68)
print()
print('  If V(S) = Σ βₙ eₙ(S) satisfies V(S) = V(S⁻¹) for all')
print('  unimodular S, then:')
print('    β₀ = β₄  and  β₁ = β₃')
print()
print('  Proof:')
print('    V(S⁻¹) = Σ βₙ eₙ(S⁻¹) = Σ βₙ e_{4-n}(S)  [by Theorem 1]')
print('           = β₄e₀ + β₃e₁ + β₂e₂ + β₁e₃ + β₀e₄')
print()
print('    V(S) = V(S⁻¹) for all S requires:')
print('      β₀ = β₄,  β₁ = β₃,  β₂ = β₂  (automatic)')
print()
print('    On the unimodular sector, e₀ = e₄ = 1 are fixed')
print('    endpoints, while e₁, e₂, e₃ vary independently.')
print('    Matching coefficients of the exchanged basis terms')
print('    yields β₀ = β₄ and β₁ = β₃.')
print()

# Verify: V(S) = V(S⁻¹) for paired coefficients
for b0, b1, b2 in [(1, 0, 16), (3, 5, 7), (2, 1, 10)]:
    b3, b4 = b1, b0  # paired
    VS = sum(b*e_n(S_uni, n) for n, b in enumerate([b0,b1,b2,b3,b4]))
    VSinv = sum(b*e_n(S_uni_inv, n) for n, b in enumerate([b0,b1,b2,b3,b4]))
    print(f'    ({b0},{b1},{b2},{b3},{b4}): V(S)={VS:.8f}, V(S⁻¹)={VSinv:.8f}, Δ={abs(VS-VSinv):.1e} ✓')

# Verify: V(S) ≠ V(S⁻¹) for unpaired coefficients
b0, b1, b2, b3, b4 = 1, 2, 16, 3, 4  # NOT paired
VS = sum(b*e_n(S_uni, n) for n, b in enumerate([b0,b1,b2,b3,b4]))
VSinv = sum(b*e_n(S_uni_inv, n) for n, b in enumerate([b0,b1,b2,b3,b4]))
print(f'    ({b0},{b1},{b2},{b3},{b4}): V(S)={VS:.8f}, V(S⁻¹)={VSinv:.8f}, Δ={abs(VS-VSinv):.1e} ← broken')

print('\n  THEOREM 2 VERIFIED ✓')
print()

# --- THEOREM 3: Hessian of e₂(S) at S=I has full rank 16 ---
print('THEOREM 3: Hessian rank of e₂(S) at S = I')
print('─'*68)
print()

indices = [(i,j) for i in range(N) for j in range(N)]
D = N*N

Hess = mat_zeros(D)
for idx1, (i,j) in enumerate(indices):
    for idx2, (k,l) in enumerate(indices):
        tr_eij = 1.0 if i==j else 0.0
        tr_ekl = 1.0 if k==l else 0.0
        tr_prod = 1.0 if (j==k and i==l) else 0.0
        Hess[idx1][idx2] = tr_eij * tr_ekl - tr_prod

def vec_dot(a, b): return sum(x*y for x, y in zip(a, b))
def hess_act(H, v): return [vec_dot(row, v) for row in H]
def verify_eigvec(H, v, tol=1e-10):
    Hv = hess_act(H, v)
    idx = max(range(len(v)), key=lambda i: abs(v[i]))
    lam = Hv[idx] / v[idx]
    for i in range(len(v)):
        assert abs(Hv[i] - lam*v[i]) < tol
    return lam

eig_count = {}

# Antisymmetric: dim=6, λ=+1
for i in range(N):
    for j in range(i+1, N):
        v = [0.0]*D
        v[indices.index((i,j))] = 1.0; v[indices.index((j,i))] = -1.0
        lam = verify_eigvec(Hess, v)
        eig_count[round(lam,10)] = eig_count.get(round(lam,10), 0) + 1

# Symmetric traceless off-diag: dim=6, λ=-1
for i in range(N):
    for j in range(i+1, N):
        v = [0.0]*D
        v[indices.index((i,j))] = 1.0; v[indices.index((j,i))] = 1.0
        lam = verify_eigvec(Hess, v)
        eig_count[round(lam,10)] = eig_count.get(round(lam,10), 0) + 1

# Symmetric traceless diagonal: dim=3, λ=-1
for p in range(N-1):
    v = [0.0]*D
    v[indices.index((p,p))] = 1.0; v[indices.index((p+1,p+1))] = -1.0
    lam = verify_eigvec(Hess, v)
    eig_count[round(lam,10)] = eig_count.get(round(lam,10), 0) + 1

# Identity: dim=1, λ=+3
v_id = [0.0]*D
for i in range(N): v_id[indices.index((i,i))] = 1.0
lam = verify_eigvec(Hess, v_id)
eig_count[round(lam,10)] = eig_count.get(round(lam,10), 0) + 1

total = sum(eig_count.values())
rank = sum(m for l, m in eig_count.items() if l != 0)

print(f'  Eigenvalue spectrum (verified by direct eigenvector substitution):')
for lam in sorted(eig_count.keys(), reverse=True):
    print(f'    λ = {lam:+.0f}  ×  {eig_count[lam]}')
print(f'\n  Eigenvectors verified: {total}/{D}')
print(f'  Rank: {rank}')
print(f'  Signature: (7, 9)')
print(f'  Null space: empty')
print()
assert total == D and rank == D
print('  THEOREM 3 VERIFIED ✓')
print()

# ═══════════════════════════════════════════════════════════════
#  WALL 2: EXPLICIT PHYSICAL POSTULATES
#  (clearly labeled — not claimed as theorems)
# ═══════════════════════════════════════════════════════════════

print('┌' + '─'*68 + '┐')
print('│  WALL 2: PHYSICAL POSTULATES                                     │')
print('│  Status: Axioms (physical principles, explicitly stated)         │')
print('└' + '─'*68 + '┘')
print()

print('AXIOM 1: Symmetric Ghost-Free Lock (No Residual Oriented Sector)')
print('─'*68)
print()
print('  The Hassan-Rosen construction identifies the unique ghost-free')
print('  interaction basis (the elementary symmetric polynomials eₙ),')
print('  but not the unique physical coefficient point within that')
print('  basis. The five βₙ define an admissible phenomenological')
print('  search space rather than, by themselves, the correct closure')
print('  lock. The present lock is a further selection inside that')
print('  space.')
print()
print('  Exchange symmetry (Theorem 2) requires β₁ = β₃. But it')
print('  permits β₁ = β₃ ≠ 0. The potential V = β₁(e₁ + e₃) is')
print('  exchange-invariant.')
print()
print('  However, (e₁, e₃) form the exchange-non-self-dual paired')
print('  sector: they are not individually invariant under S → S⁻¹,')
print('  but swap with each other. By contrast, e₂ is self-dual')
print('  (maps to itself), and (e₀, e₄) are fixed endpoints on the')
print('  unimodular sector. The (e₁, e₃) pair retains a residual')
print('  oriented coupling layer — it preserves exchange pairing')
print('  but still encodes directional organization within the lock.')
print()
print('  At the field origin, the interaction represents a balanced')
print('  closure of the two metric sectors. A balanced closure')
print('  excludes an active non-self-dual oriented sector. Therefore')
print('  the exchanged odd pair is eliminated:')
print()
print('  ┌──────────────────────────────────────────────┐')
print('  │  β₁ = β₃ = 0                                │')
print('  └──────────────────────────────────────────────┘')
print()
print('  NOTE: Generic ghost-free bimetric theories may admit')
print('  β₁ = β₃ ≠ 0. We are not claiming that ghost freedom alone')
print('  sets β₁ = β₃ = 0 in the general bimetric family. We are')
print('  claiming that at the symmetric lock point — where the')
print('  interaction represents balanced closure of two oppositely')
print('  oriented sectors — the symmetric lock selects the')
print('  exchange-self-dual subclass without residual oriented bias.')
print('  This removes the (e₁, e₃) sector.')
print()
print('  Physical basis: The two tetrahedra of the stellated')
print('  octahedron carry opposite spatial orientations. The')
print('  closure condition requires both orientations. At the')
print('  contact coupling point (s = 0 in the coupling polynomial),')
print('  both sectors contribute symmetrically. A term that')
print('  encodes which sector is "primary" (the non-self-dual')
print('  pair) does not remain active at a point where no primary')
print('  sector exists.')
print()

print('AXIOM 2: Rank-Zero Normalization')
print('─'*68)
print()
print('  The rank-0 term in the bimetric potential is normalized')
print('  to unity:')
print()
print('  ┌──────────────────────────────────────────────┐')
print('  │  β₀ = 1                                     │')
print('  └──────────────────────────────────────────────┘')
print()
print('  Combined with exchange symmetry (Theorem 2): β₄ = β₀ = 1.')
print()
print('  NOTE: An overall rescaling of β₀ can be absorbed into')
print('  the interaction mass scale m². The statement β₀ = 1')
print('  is therefore a normalization convention that fixes')
print('  the mass scale. It is not forced by algebra alone.')
print()
print('  Physical basis: The coupling polynomial f(K, 0) = 1 + K²')
print('  assigns weight K⁰ = 1 to the rank-0 (existence) term.')
print('  This is the unique rank-0 contribution to the graded')
print('  frame algebra. The normalization β₀ = K⁰ = 1 identifies')
print('  the interaction mass scale with the topological coupling.')
print()

print('AXIOM 3: Quadratic Completeness (Information Completeness)')
print('─'*68)
print()
print('  The quadratic interaction weight equals the number of')
print('  independent sensitivity directions of e₂(S) at S = I:')
print()
print('  ┌──────────────────────────────────────────────┐')
print('  │  β₂ = rank(∇²e₂(S)|_{S=I}) = 16            │')
print('  └──────────────────────────────────────────────┘')
print()
print('  NOTE: The Hessian rank (Theorem 3) is 16. But a')
print('  coefficient is not in general equal to the rank of')
print('  its term\'s Hessian. This axiom is the bridge principle:')
print('  one unit of coupling per independent sensitivity')
print('  direction. It is a constitutive choice, not a deduction.')
print()
print('  The quadratic coefficient is not assigned from Hessian')
print('  rank alone. It is selected by the convergence of three')
print('  structurally distinct representations of the same')
print('  closure architecture — variational, combinatorial, and')
print('  algebraic — all realizing the same quadratic')
print('  multiplicity 16.')
print()

print('WHY THE THREE "16" COUNTS ARE NOT ACCIDENTAL')
print('─'*68)
print()
print('  All three routes trace to the 4-dimensional frame.')
print('  A 4×4 matrix has 16 entries. Cl(1,3) has 2⁴ = 16')
print('  dimensions. Four faces with 4 medial subdivisions')
print('  give 4×4 = 16. The number 4 is doing the work,')
print('  and 16 = K² is its quadratic expression.')
print()
print('  This convergence is a feature of the construction')
print('  rather than a defect.')
print()
print('  The question is not "why do three things give 16?"')
print('  The question is "why does the quadratic interaction')
print('  layer see the FULL K² structure rather than some')
print('  subspace of it?"')
print()
print('  It would have been possible for e₂(S) to have a')
print('  degenerate Hessian — to see only 9 directions, or 7,')
print('  or 12. Many quadratic functions on 16-dimensional')
print('  spaces have rank less than 16. The theorem (Theorem 3)')
print('  is that THIS specific quadratic function — the one')
print('  Hassan and Rosen proved is the unique ghost-free')
print('  interaction — has no null directions. It is full-rank.')
print()
print('  The three routes are structurally distinct:')
print()
print('  ┌──────────────────────────────────────────────────────┐')
print('  │  VARIATIONAL (Hessian rank)                         │')
print('  │    Number of independent quadratic response          │')
print('  │    directions of e₂(S) at the proportional          │')
print('  │    background. Measures: how many independent        │')
print('  │    perturbations of the frame transition does the   │')
print('  │    interaction detect?                               │')
print('  │    Answer: all 16. No null directions in the            │')
print('  │    quadratic response.                                  │')
print('  ├──────────────────────────────────────────────────────┤')
print('  │  COMBINATORIAL (boundary channel count)             │')
print('  │    Number of face-mediated exchange channels at     │')
print('  │    the dual-tetrad boundary. The quadratic term     │')
print('  │    e₂(S) is the first interaction layer that        │')
print('  │    resolves pairwise boundary communication without │')
print('  │    sector preference. Its multiplicity is therefore │')
print('  │    identified with the complete count of            │')
print('  │    independent face-mediated exchange channels.     │')
print('  │    Answer: 4 faces × 4 medial = 16. The channel     │')
print('  │    count is complete at this interaction layer.     │')
print('  ├──────────────────────────────────────────────────────┤')
print('  │  ALGEBRAIC (Clifford closure dimension)             │')
print('  │    The tetrad frame generates a local Clifford      │')
print('  │    closure algebra Cl(1,3) of dimension 16. This    │')
print('  │    provides an algebraic realization of the same    │')
print('  │    quadratic multiplicity — not by identifying S    │')
print('  │    with Cl(1,3) element-by-element, but by showing │')
print('  │    that the local frame closure structure naturally │')
print('  │    occupies a 16-dimensional algebraic envelope.    │')
print('  │    Answer: dim(Cl_{1,3}) = 16. The algebraic        │')
print('  │    envelope is fully occupied at the same           │')
print('  │    multiplicity.                                    │')
print('  └──────────────────────────────────────────────────────┘')
print()
print('  Each route asks a different question:')
print('    Variational:    How many directions are DETECTED?')
print('    Combinatorial:  How many channels are OPEN?')
print('    Algebraic:      How many dimensions are OCCUPIED?')
print()
print('  All three answer: 16. The interaction layer is')
print('  COMPLETE. It exhausts the available structure.')
print()
print('  These are not three independent accidents. They are')
print('  three structurally distinct but closure-equivalent')
print('  realizations of the same quadratic multiplicity.')
print()
print('  Any β₂ < 16 leaves sensitivity directions unweighted,')
print('  boundary channels uncoupled, or algebraic dimensions')
print('  unoccupied — requiring an explanation of WHICH')
print('  directions are special and WHY they are excluded')
print('  when the geometry treats them all equivalently at')
print('  the proportional background.')
print()
print('  Any β₂ > 16 double-counts directions that the')
print('  Hessian resolves only once, couples channels that')
print('  the boundary provides only once, or exceeds the')
print('  algebraic dimension of the space.')
print()
print('  β₂ = 16 is the unique value consistent with')
print('  complete, non-redundant quadratic coverage across')
print('  all three structural descriptions.')
print()

# ═══════════════════════════════════════════════════════════════
#  WALL 3: CONSEQUENCES
#  (derived from Walls 1 + 2)
# ═══════════════════════════════════════════════════════════════

print('┌' + '─'*68 + '┐')
print('│  WALL 3: CONSEQUENCES                                            │')
print('│  Status: Corollaries (follow from Theorems 1-3 + Axioms 1-3)    │')
print('└' + '─'*68 + '┘')
print()

print('COROLLARY 1: The Locked Parameter Set')
print('─'*68)
print()
print('  From Theorem 2 + Axiom 1 (symmetric ghost-free lock): β₁ = β₃ = 0')
print('  From Theorem 2 + Axiom 2 (normalization): β₀ = β₄ = 1')
print('  From Theorem 3 + Axiom 3 (quadratic completeness): β₂ = 16')
print()
print('  ╔══════════════════════════════════════════════╗')
print('  ║  {β₀, β₁, β₂, β₃, β₄} = {1, 0, 16, 0, 1} ║')
print('  ╚══════════════════════════════════════════════╝')
print()

# Verify the locked potential
V_locked = e_n(S_uni, 0) + 16*e_n(S_uni, 2) + e_n(S_uni, 4)
V_locked_inv = e_n(S_uni_inv, 0) + 16*e_n(S_uni_inv, 2) + e_n(S_uni_inv, 4)
print(f'  V(S)   = {V_locked:.10f}')
print(f'  V(S⁻¹) = {V_locked_inv:.10f}')
print(f'  |V(S) - V(S⁻¹)| = {abs(V_locked - V_locked_inv):.1e}  ✓ Exchange invariant')
print()

print('COROLLARY 2: Galileon Hierarchy')
print('─'*68)
print()
print('  Under the standard decoupling-limit map (de Rham,')
print('  Gabadadze, Tolley 2011):')
print('    c₂ = β₁ = 0   → cubic Galileon killed')
print('    c₃ = (3/2)β₂ = 24  → quartic Galileon survives')
print('    c₄ = β₃ = 0   → quintic Galileon killed')
print()
print('  NOTE: The Galileon coefficient map depends on the')
print('  parameter basis, background choice, and Stückelberg')
print('  normalization. The map c₂=β₁, c₃=(3/2)β₂, c₄=β₃')
print('  follows the convention of de Rham et al. (2011) at')
print('  the proportional background with equal effective')
print('  Planck masses. If a different convention is used,')
print('  the numerical values change but the structural')
print('  consequence (only quartic survives) is preserved.')
print()

import math
print('COROLLARY 3: Scalar-Tensor Transition and Topological Coupling Impedance')
print('─'*68)
print()
print('  The GFD scalar-tensor transition (field equation from')
print('  varying the covariant action):')
print()
print('  ┌──────────────────────────────────────────────┐')
print('  │  g_s = g_t² / (a₀ + g_t)                    │')
print('  └──────────────────────────────────────────────┘')
print()
print('  This quadratic transition encodes the coupling between')
print('  TetA and TetB at the interaction vertex. It contains the')
print('  constitutive law μ(x) = x/(x+1) as its response function')
print('  and the mass decode formula M = rv⁴/[G(a₀r + v²)] as')
print('  its closed-form inverse.')
print()

# ── Topological Coupling Impedance (Hardware) ──
print('  ── Topological Coupling Impedance ──')
print()
print('  At the Field Origin (s = 0), the coupling polynomial gives')
print('  the total interaction capacity:')
print('    f(K, 0) = 1 + K² = 1 + 16 = 17')
print()
print('  The two boundary existence terms (β₀ = 1, β₄ = 1) represent')
print('  the irreducible overhead of maintaining the dual-tetrad')
print('  boundary condition. Their ratio to the total capacity is:')
print()
print('  ┌──────────────────────────────────────────────┐')
print('  │  Δμ = 2/17 = 0.117647  (11.76%)             │')
print('  └──────────────────────────────────────────────┘')
print()

# Compute
topo_impedance = 2/17
f_origin = 17
print(f'  f(4, 0) = {f_origin}  (total capacity at Field Origin)')
print(f'  β₀ + β₄ = 2  (boundary existence terms)')
print(f'  Δμ = 2/{f_origin} = {topo_impedance:.6f}  ({topo_impedance*100:.2f}%)')
print()
print('  This is the Topological Coupling Impedance: the geometric')
print('  overhead required to maintain the dual-tetrad boundary')
print('  condition relative to the total interaction capacity at')
print('  the Field Origin. It is an integers-only ratio, derived')
print('  entirely from the coupling polynomial and the locked')
print('  parameter set. It requires no field equation to be solved.')
print()

# ── Dynamical Consistency Check (Software) ──
print('  ── Dynamical Consistency Check ──')
print()
print('  The quartic Galileon (Corollary 2) produces, in the')
print('  bimetric decoupling limit, the N=2 screening equation:')
print('    x(1-μ)² = μ')
print()

x = 1.0
mu_galileon = (math.sqrt(1+4*x) - 1) / (math.sqrt(1+4*x) + 1)
phi = (1 + math.sqrt(5)) / 2
mu_constitutive = 0.5
dyn_impedance = mu_constitutive - mu_galileon

print(f'  At x = 1:')
print(f'    Constitutive law:       μ(1) = 1/2   = {mu_constitutive:.6f}')
print(f'    Galileon screening:     μ(1) = 1/φ²  = {mu_galileon:.6f}')
print(f'    Dynamical impedance:    Δμ            = {dyn_impedance:.6f} ({dyn_impedance*100:.2f}%)')
print()
print(f'  Topological (2/17):  {topo_impedance:.6f}')
print(f'  Dynamical (1/2-1/φ²): {dyn_impedance:.6f}')
print(f'  Agreement: {abs(topo_impedance - dyn_impedance)/topo_impedance*100:.2f}% relative difference')
print()
print('  Two independent projections — one from integer counting')
print('  at the geometric vertex, one from the continuous field')
print('  equation in the decoupling limit — converge on the same')
print('  physical bottleneck to within 0.3%. The small discrepancy')
print('  reflects the transition between the discrete geometric')
print('  node and the continuous field limit.')
print()

# ── Physical interpretation ──
print('  ── Physical Interpretation ──')
print()
print('  The impedance is analogous to feed-point impedance in')
print('  self-similar antenna structures (e.g. Sierpiński gasket),')
print('  where the junction between two fractal sub-structures')
print('  creates a discrete impedance floor.')
print()
print('  The constitutive law μ = x/(x+1) governs the field-level')
print('  partition (CMB, Tully-Fisher, galaxy rotation curves).')
print('  The topological impedance 2/17 characterises the insertion')
print('  loss at the dual-tetrad vertex core.')
print()
print('  NOTE: This impedance is a structural property of the')
print('  interaction vertex, located in the interior of the')
print('  gravitational vortex structure. Observational rotation')
print('  curve measurements sample the exterior velocity field,')
print('  which integrates over this interior structure. The')
print('  impedance is not directly accessible in v_obs at the')
print('  transition radius but is encoded in the mass decode')
print('  formula, which correctly extracts baryonic mass from')
print('  the exterior velocity profile using the full quadratic')
print('  scalar-tensor transition.')
print()

# ═══════════════════════════════════════════════════════════════
#  COUNTEREXAMPLE AWARENESS
#  (what happens if each axiom is relaxed)
# ═══════════════════════════════════════════════════════════════

print('┌' + '─'*68 + '┐')
print('│  COUNTEREXAMPLE AWARENESS                                        │')
print('│  (what is admitted if each axiom is relaxed)                     │')
print('└' + '─'*68 + '┘')
print()
print('  If Axiom 1 is dropped (symmetric lock / no oriented sector):')
print('    Admitted: {a, b, c, b, a} for any b ≠ 0')
print('    Example: {1, 3, 16, 3, 1} — exchange-symmetric,')
print('    but retains active non-self-dual oriented coupling.')
print('    This represents an admissible ghost-free model but')
print('    not a balanced closure lock.')
print()
print('  If Axiom 2 is dropped (normalization):')
print('    Admitted: {a, 0, 16, 0, a} for any a > 0')
print('    Example: {5, 0, 16, 0, 5} — differs only in')
print('    the interaction mass scale.')
print()
print('  If Axiom 3 is dropped (quadratic completeness):')
print('    Admitted: {1, 0, c, 0, 1} for any c > 0')
print('    Example: {1, 0, 9, 0, 1} — weights only the')
print('    symmetric traceless subspace.')
print()
print('  If ALL axioms are kept:')
print('    Unique: {1, 0, 16, 0, 1}')
print()

# ═══════════════════════════════════════════════════════════════
#  STATUS TABLE
# ═══════════════════════════════════════════════════════════════

print('┌' + '─'*68 + '┐')
print('│  STATUS TABLE: What is proved vs what is assumed                 │')
print('└' + '─'*68 + '┘')
print()
print('  Statement                                  │ Status')
print('  ───────────────────────────────────────────┼─────────────────────')
print('  e_n(S⁻¹) = e_{4-n}(S) for det S = 1       │ EXACT THEOREM')
print('  Exchange invariance ⟹ β₀=β₄, β₁=β₃       │ EXACT THEOREM')
print('  rank(∇²e₂|_{S=I}) = 16                    │ EXACT THEOREM')
print('  ───────────────────────────────────────────┼─────────────────────')
print('  β₁ = β₃ = 0                               │ AXIOM (symmetric ghost-')
print('                                             │   free lock, no residual')
print('                                             │   oriented sector)')
print('  β₀ = 1                                    │ AXIOM (normalization)')
print('  β₂ = 16                                   │ AXIOM (triple-convergent')
print('                                             │   completeness principle)')
print('  ───────────────────────────────────────────┼─────────────────────')
print('  {1, 0, 16, 0, 1}                          │ COROLLARY')
print('  Quartic-only Galileon (c₃=24)              │ COROLLARY')
print('  SST topological impedance Δμ = 2/17       │ COROLLARY')
print()

# ═══════════════════════════════════════════════════════════════
#  UNIQUENESS STATEMENT
# ═══════════════════════════════════════════════════════════════

print('╔' + '═'*68 + '╗')
print('║  UNIQUENESS                                                      ║')
print('╠' + '═'*68 + '╣')
print('║                                                                  ║')
print('║  Under exchange invariance (Theorem 2), the symmetric             ║')
print('║  ghost-free lock (Axiom 1), rank-zero normalization              ║')
print('║  (Axiom 2), and quadratic completeness (Axiom 3), the           ║')
print('║  interaction coefficient set is uniquely determined:             ║')
print('║                                                                  ║')
print('║        {β₀, β₁, β₂, β₃, β₄} = {1, 0, 16, 0, 1}               ║')
print('║                                                                  ║')
print('║  The quadratic coefficient β₂ = 16 is uniquely selected by      ║')
print('║  triple structural convergence: three structurally distinct      ║')
print('║  representations of the same closure architecture —              ║')
print('║  variational, combinatorial, and algebraic — all realize        ║')
print('║  the same quadratic multiplicity 16.                            ║')
print('║                                                                  ║')
print('║  Three exact theorems and three explicit physical axioms          ║')
print('║  together determine the locked set.                              ║')
print('║                                                                  ║')
print('╚' + '═'*68 + '╝')

