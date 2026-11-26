# From one time-face interaction to the 48 effective links

[Interactive HTML companion](interactive/kernel.html) — offline explorer of the existing results.

## 1. Recover the actual Stage VII operator

Read the definitions of [Stage VII](../SUSTAINED_TRIFORCE_FLYWHEEL.md) with their original weights r,d,b,a,k,o. In each chamber use X∈C¹² (ordered off-diagonal pairs), y∈C⁴ (central triangles). Put A=(X⁺,y⁺), B=(X⁻,y⁻). The scalar centre O is a separate **existing** vertex record; retain its local coupling to both chamber reads. There are 24 ring links and 24 base links (within chambers); 8 scalar-centre links; 48 direct chamber-to-chamber entries in the old graph. The latter are 12 transpose, 24 opposite-column (12 per direction), and 12 central links. No new physical bonds are introduced below.

Define T X by (TX)_ij=X_ji, R X by row sums, Q X by column sums, and K=J−I. Direct index summation gives T=Tᵀ=T⁻¹, QT=R, QQᵀ=RRᵀ=3I, QRᵀ=K. Thus QTQᵀ=K. The cross block (from B to A, in the same reference labels) is

$$C=\begin{pmatrix}dT&aQ^T\\aQ&kK\end{pmatrix}.$$

It is symmetric for the Stage VII chamber-exchange-invariant subclass. Its bilinear energy is A†CB+B†CA. In the disjoint-domain interpretation this is a bilinear **effective vertex read**, not a spatial path. The full original graph has 104 undirected edges; exactly 48 appear in C.

## 2. Exact rank theorem [new]

For d≠0, block elimination gives C=LDLᵀ with L lower-unit-triangular and D=diag(dT,(k−a²/d)K), L's bottom left block (a/d)QT. Since T invertible and K has eigenvalues 3,−1,−1,−1, rank C is 16 unless dk=a², when rank C=12. Its determinant is det(dT)det((k−a²/d)K)=−3d⁸(dk−a²)⁴ (six negative eigenvalues of T). If d=0, a≠0, kernel equations first give y=0 (Qᵀ injective), then QX=0, so rank=8. If d=a=0, rank=4 for k≠0, otherwise zero. Stage VII's d=−1/2, a=k=−1 gives k−a²/d=1, determinant −3/4096 and rank 16. Its inertia is 7 positive, 9 negative: T has six of each sign and the Schur block has one positive and three negative. This is not the energy stability of the full H; it is the inertia of the cross block alone.

The equality dk=a² appeared in the earlier common-junction research; here it has an exact interpretation as the loss of four cross-channel directions. That earlier premise was conditional, not selected by the vortex dynamics. It does not hold for the original Stage VII witness. The full cross map respects all tetrahedral label permutations. The 16-coordinate representation is (A₁⊕T₂)⊗(A₁⊕T₂)=2A₁⊕E⊕T₁⊕3T₂. That also shows why a single triplet or scalar cannot resolve the whole vertex.

## 3. Rank bounds for separate time-face reads [new]

Let A and B be read separately into m complex channels by linear maps L_A,L_B, and let vertex coupling be 2 Re[(L_A A)† K_O(L_B B)]. Its effective cross matrix is L_A† K_O L_B; rank≤m. The generic Stage VII model therefore requires at least 16 complex linear channels to reproduce **the full cross block** in an instantaneous separate-read factorization. This also bounds complex-linear mixed Hessians of a differentiable interaction through fixed separate linear reads; a general nonlinear real-linear Hessian uses real dimensions and needs its own rank accounting. This theorem does not prohibit a scalar-valued energy with a full-rank bilinear overlap inside it. Nor does it exclude lower-dimensional dynamics on a restricted state space, frequency-dependent histories, or other mechanisms. A Schur-mediated instantaneous linear block through m independent intermediate modes has the same rank bound at each fixed nonsingular frequency.

A physical time face need not have 16 independent propagating modes; its actual transfer map may have lower rank. But Proof 23 gives exactly 16 possible depth-two geometric addresses. Define a read W by storing X_ij at (i,j) and y_i at (i,i), then applying F=h⊗h. W is unitary. Set K_O=W C W†. Then C=W†K_O W exactly. For each label permutation p, the address permutation intertwines the chamber action, and K_O commutes with the corresponding Walsh-conjugated action. At fixed time-face index, this is precisely the stabilizer action on the two recursive child indices. This demonstrates **one vertex, multiple spectral records**, without adding independent coordinates. It is a representation of the known matrix; it does not derive K_O from geometric overlap or electrodynamics. The matrix figure in the README shows the two equivalent encodings.

## 4. The actual collective sector requires less but not just a scalar

Set q_i=s_i·z, Σq_i=0; X_ij=u q_i+v q_j, y_i=w q_i. The cross block acts on (u,v,w) via

$$M_C=\begin{pmatrix}0&d&0\\d&0&a\\-a&3a&-k\end{pmatrix}.$$

Derive this by summing QX=(3v−u)q and Kq=−q. The same-chamber operator acts via M_A=[[e+2r,−r,b],[0,e−r,0],[3b,−b,e_c]]. Their sum is exactly the Stage VII even-sector matrix. det M_C=d(dk−a²). For the full triplet sector the rank is 9 generically, 6 in the tuned d≠0 case; for fixed z the rank is 3 or 2. The 3-amplitude engine is a multiplicity space, not three extra modes grafted onto the field.

At the row-closed initial state u=v/3, w=0, R X=0, Q X=(8v/3)q. With only the same-chamber base bonds, the core remains dark. A vertex read must access the opposite-column or another nonzero winding read, not simply the row mean. A scalar O still cannot linearly receive a T₂ amplitude. For an isolated same-chamber block, the four base histories Y,YA,YA²,… have rank 8 and completely miss eight row-closed winding coordinates (each ring/base block has a symmetric two-dimensional subspace and a two-dimensional winding subspace). With the inherited witness's column read Q the rank is 11, and combining Y and Q remains rank 11; this is exact for the isolated block, not a universal dynamic bound for the interacting system. The earlier optical/history research offers a route to richer reads, but the vertex selection still needs derivation.
