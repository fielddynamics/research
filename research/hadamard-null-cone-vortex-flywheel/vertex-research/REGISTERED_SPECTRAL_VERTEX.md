# Registered resonance: what the two time faces must actually exchange

[Interactive HTML companion](interactive/kernel.html) — offline explorer of the existing results.

**Status:** [T] exact finite algebra under the stated labelled-frame/graph premises. [D] candidate resonance realization. The preceding `SCHEME_AND_TIME_FACE.md`, `ANTENNA_AND_SPECTRAL_READ.md` and `VERTEX_FACTORIZATION.md` are the inputs. This continuation does not equate the discrete sign of a tetrad with a continuous amplitude, or infer physical subspace from parity alone. No new degrees of freedom are introduced.

## 1. The missing information is relative registration, not a spatial link

The scheme proof fixes a metric, observer and future time orientation. The two orientation sectors are related by spatial parity P; the frame equation is unchanged. The spatial realization can be represented by a 3×4 matrix M with MᵀM=4I−J, MMᵀ=4I, M1=0. However, an equally admissible opposite-root partner is M_B=−LM_A for any proper rotation L. Each self-Gram is identical and cannot determine L.

The cross-Gram carries precisely the missing orientation:

$$J_{AB}=M_A^TM_B/4,\quad J_{AB}^TJ_{AB}=J_{AB}J_{AB}^T=P_W,\quad L=-M_AJ_{AB}M_A^T/4,$$

where P_W=I−J/4 and the last equation uses M_B=−LM_A. In the parity-aligned case J_AB=−P_W. These equations follow by multiplication, and are checked for proper signed/permuted axes. More generally they hold for all proper L. Thus the cross-Gram is a partial isometry between the three-dimensional contrast spaces. It is an interaction datum, not a measured distance from A to B. Choosing the same time leg does not alone fix the relative rotation; the scheme's canonical parity comparison is a natural choice **if** the two time-face read frames are aligned. The actual phase registration and its dynamics remain physical questions.

Let U(p) permute both indices of the 16 addresses simultaneously, for p∈S₄. For common registration U(p) C U(p)ᵀ=C. If the two chambers may relabel independently, C must instead transform as a two-ended kernel C→U(p_A) C U(p_B)ᵀ, which makes A†CB invariant when the records are transformed too. No spatial identification is required. If C were a *fixed* numerical kernel invariant under each action separately, then C=P_fix C P_fix, where P_fix is the group-average projector. Its rank is at most two: the uniform lateral array and the uniform base array. With only the single spatial triplet the corresponding independent invariant read is zero. The same conclusion for a selected-face stabilizer uses its own invariant subspaces, not this full S₄ bound. Therefore a directional full-rank interaction must carry relative registration (or transform with it). This is a precise obstacle to a symmetry-blind scalar gate, and does not mean one scalar-valued nonlinear Hamiltonian cannot depend on a registered directional overlap.

## 2. Exact spectral channels of the inherited vertex

Use the Stage VII cross-block C and row, column, transpose maps R,Q,T of the previous note, and K=J−I. The common S₄ decomposition is

$$\mathbb R^{16}=2A_1\oplus E\oplus T_1\oplus3T_2.$$

A direct construction avoids reliance on matching dimensions alone. The two orthonormal uniform vectors are constant on lateral sites (normalization √12) and on central sites (normalization 2). Their block is

$$C_U=\begin{pmatrix}d&\sqrt3a\\\sqrt3a&3k\end{pmatrix}.$$

The five row- and column-dark lateral directions ker R ∩ ker Q split into symmetric arrays (dimension two) and antisymmetric arrays (dimension three), with exact eigenvalues d and −d respectively. They do not couple to base amplitudes through C. For a zero-sum four-vector q the other nine directions are X_ij=u q_i+v q_j, y_i=w q_i, with the three-dimensional multiplicity operator M_C of the preceding note. Their Gram metric is proportional to G_m=[[3,−1,0],[−1,3,0],[0,0,1]]. All these subspaces are orthogonal and span the complete space. Their characteristic polynomials therefore give the exact identity

$$\det(tI-C)=(t-d)^2(t+d)^3p_U(t)p_T(t)^3,$$
$$p_U=t^2-(d+3k)t+3(dk-a^2),$$
$$p_T=t^3+kt^2-(3a^2+d^2)t+a^2d-d^2k.$$

This makes the frequency-response decomposition of the *given* kernel explicit: two uniform branches, two symmetry-protected dark eigenvalues and three triply-degenerate branches. There are sixteen independent records but at most seven distinct eigenvalues in this generic family (two + two + three). The eigenvalues here are cross-coupling strengths in dimensionless model units, not measured resonant frequencies of the full H. The on-shell frequency response would require the complete intra-chamber dynamics and boundary conditions. The three constants d,a,k are not selected by symmetry. For instance the real symmetric commutant of the full registered S₄ action has dimension 3+1+1+6=11 (two copies of A1 and three of T2); the Stage VII family is a particular three-parameter subspace.

## 3. A nontrivial limitation of a simple Sierpiński antenna reading

The two-digit time-face encoding permits an orthogonal Walsh hierarchy. Let P₀=J/4, P₁=I−P₀. The three orthogonal projectors on the address space are E₀=P₀⊗P₀, E₁=P₀⊗P₁+P₁⊗P₀, E₂=P₁⊗P₁, with ranks 1,6,9. Identify diagonal addresses with base records and off-diagonal ones with lateral records, as in the first vertex study. This is an exact coordinate map, not a claim that the Walsh grades are independently propagating Maxwell modes. Applying the projectors to the inherited C gives

$$\|E_0 C E_1\|_F^2=0,$$
$$\|E_0 C E_2\|_F^2=\frac{3}{16}(2a-d+3k)^2,$$
$$\|E_1 C E_2\|_F^2=\frac34[4a^2+(d+k)^2].$$

These identities follow by direct contraction of the 4×4 address projectors, and are verified symbolically. In particular, requiring **all three grades to remain separate** forces a=0, d=−k and d=3k, hence a=d=k=0. No nonzero Stage VII cross kernel has this separability. Frequency matching cannot simply mean independent scalar resonances at each hierarchical depth. If this is the effective kernel, the vertex must mix the grades (or the physical frequency bands must be a different basis). This is a new constraint on the original antenna proposal. It does not contradict the experimentally familiar multiband response of fractal antennas; it concerns the specific GFD finite read. Neither the older antenna counts nor a free-space Maxwell antenna alone supplies the missing kernel.

## 4. The junction factorization and signed phase response

For d≠0 define L=[I₁₂, (a/d)TQᵀ]. Then

$$C=dL^TTL+\operatorname{diag}(0_{12},(k-a^2/d)K).$$

The exact shared-junction relation dk=a² eliminates the residual: the sixteen records couple through twelve registered read combinations. With the original Stage VII d=−1/2,a=k=−1 the residual is nonzero and four more independent read directions are required. This does not imply that the twelve read combinations are twelve new oscillators.

The full original cross-block has seven positive and nine negative eigenvalues. Hence a same-read positive Gram C=LᵀL (or its negative) cannot give this C. It is not a positive autocorrelation kernel. A relative phase response can resolve the algebraic issue: using the spectral absolute value |C| and sign involution S=sgn(C), C=|C|^(1/2) S |C|^(1/2), S²=I for this invertible case. The seven positive and nine negative channels are phase signs in this representation, not independently established propagation states. A reciprocal resonator with an explicit frequency-dependent phase or a registered read could in principle produce an indefinite cross response. The factorization does not derive either the frequencies or the phase signs from the Sierpiński geometry. Nor does indefinite cross coupling imply negative total physical energy; the full Hamiltonian must be considered.

## 5. The next independent test

We now know what a candidate vertex action has to supply: the registration map, the effective mixing between address grades, and signed transfer response. Derive these from the time-face read or a boundary variational principle *before* using the inherited C. Matching counts, inserting C, or choosing a spectral basis after seeing C cannot establish physical selection. The alternative nonlinear curvature calculation in `VERTEX_CURVATURE.md` adds a separate dynamical constraint on the interaction. These are two necessary parts of one engine, not two mechanisms.
