# π-stepped invariant settlement: three interleaved orbit passes and the running determinant

Continuation of Proof 26 revision 4 and `gfd-pi-step-ledger`. Exact finite algebra and numerical cross-checks; not a revision of the proof or a microscopic derivation of gravity. Sources: [Proof 26](https://github.com/fielddynamics/research/blob/main/proofs/recursive-field-closure-response/PROOF_26.md), [π stepping synthesis](https://github.com/fielddynamics/research/tree/main/research/bbp%20and%20pi%20field%20closure%20stepping), [Three sub-reads](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/THREE_SUBREAD_CLOSURE.md). `source_step_ledger.csv` is the previous certified 333-digit trace. The included `certify_digits.py` regenerates the original ledger independently from rational BBP bounds (writes `pi_step_ledger.csv`; compare to source). `verify_innovations.py` calculates exact projectors from that ledger and independently checks determinant identities numerically.

## 1. Three interleaved member passes, not three contiguous time intervals

Map ordered pair (u,v) to the three bit pairs (2*u_bit+v_bit), high to low bit. Apply the internal simultaneous digit cycle C:0 fixed,1→2→3→1. There is one fixed address and 21 orbits of size three. This is the internal address action used by the preceding computational investigation; physical spatial rotation of corner pairs has a different invariant dimension (24, not 22), as Proof 26 explains. No physical equivariant identification is supplied.

For each orbit count distinct visited members, not repeated visits. All 21 nonfixed orbits have at least one member at step 156, at least two at step 192, and all three at step 332. Step 0 is the integer digit, so the last event is digit 333. The fixed address (0,0,0) is visited as well. The three passes are defined by within-orbit encounter order and interleave. They are not demonstrated to be the three physical resolution sweeps or three 13→21 resets. First and second members of different orbits can be interspersed. For a general register, order the three orbit values by the action C (not chronological encounter order) and define y_l=1/sqrt(3) sum_{k=0}^2 omega^(-lk)b_k, omega=e^(2 pi i/3). The Fourier matrix is unitary; all three observations recover the common orbit coefficient and two rotating coefficients. In the invariant case the rotating coefficients vanish. Thus the full walk can verify invariance and recover information a quotient discards, under a static/coherent state premise. The one common inventory record of the entire field is distinct from the single fixed address and from any individual orbit average.

## 2. Exact incremental settlement with independently known mean

Assume the register is orbit-constant and its weighted common mean is independently known (not necessarily physical mass). In orbit-value coordinates b in R^22, use inner product diag(w), w=(1,3,...,3), inherited from counting the 64 original addresses. Let U be the unread orbit labels, m_U their indicator and W_U=sum_{i in U} w_i. The unresolved orthogonal projector is

R_U=diag(m_U)-m_U (w*m_U)^T/W_U, for U nonempty, and zero for U empty.

It projects onto vectors supported on U with zero weighted sum. The resolved contrast projector is L_U=I-P0-R_U, where P0=1 w^T/64. A first observation removing i from U gives D_i=R_U-R_(U\{i}); nested residual spaces imply D_i is an orthogonal projector of rank one unless |U|=1, in which case D_i=0. Repeat observations do not change it. D_i D_j=0 for different innovation events. Thus sum D_i=I-P0 exactly. An explicit spanning vector of the new direction is e_i/w_i-m_U/W_U; its squared weighted norm is 1/w_i-1/W_U. This is the normalized least-squares innovation and requires no new oscillator. If the true invariant contrast is b_c=(I-P0)b, the unresolved squared-error cost E_U=1/2 ||R_U b_c||_w^2 decreases by 1/2 ||D_i b_c||_w^2 on a new read. This is an information error, not a derived mechanical energy or dissipated heat.

The actual sequence reaches 21 orthogonal innovations at step 104: the last unread orbit is inferred from the known common mean. At this point only 20 of the 21 nonfixed orbits and the fixed address have been visited. The last orbit is directly visited at 156. The three-member verification does not finish until 332. Without the known mean, all 22 orbit records are required. Without orbit constancy, 22 records do not suffice to recover the full 64-address signal. These rank distinctions are crucial.

## 3. Running version of Theorem 8

At each independently resolved direction assume an elementary retained amplitude t, with unchanged orthogonal complement. Define T_i=I+(t-1)D_i. Then the full running transfer, including the common record, is

T(n)=product_i T_i=I+(t-1)L_n,

det(T(n)^*T(n))=|t|^(2 r_n), r_n=rank L_n.

The adjoint is for the weighted inner product; all projectors are orthogonal therein. At completion r_n=21, so for a separately derived |t|²=alpha this yields alpha^21. The orthogonal increments give multiplicativity without assuming all 333 visits attenuate independently; repeated reads and the inferred last orbit do not add exponents. This is a concrete conditional implementation of the determinant law in Proof 26. It does not derive the gain, select volume response as mechanical coupling, or show the physical engine performs least-squares projections. Raw full non-invariant contrast accounting would yield 63 innovations, not 21.

## 4. Test the proposed running coupling state

For each step compute the prefix projections P_d on the internal orbit-constant space by averaging over all suffixes. Their exact ranks are 1,2,6,22, so Q_d=P_d-P_(d-1) has ranks 1,4,16. The running grade shares r_d(n)=tr(Q_d L_n) sum to r_n; they are not generally integers. All 21 rank-one innovations have positive overlap with more than one grade. The π ordering therefore does not simply execute the three orthogonal grades one after another in this model.

Use one explicit diagnostic (not an inherited physical rule): start with the signed depth operator I-2Q_2 on the contrast space, and reverse the sign on the resolved middle grade via D(n)=I-2Q_2+2Q_2 L_n Q_2. Then f_n=13+2 tr(Q_2 L_n) increases monotonically from 13 to 21, reaching 21 at step 104. It never equals 17 at an integer step: at 15 it is 947/56=16.910714..., at 16 it is 433/25=17.32. It does not reset three times. A different natural hypothesis, a middle grade unitary phase with period three, would give real trace values 21,15,15, not 13,17,21. The continuously variable middle phase can yield 13,17,21 (phase pi, pi/2, 0), but is lossless and does not generate alpha. These diagnostics rule out these direct identifications, not a physical cyclic read with further dynamics.

## 5. Physical next step

The completed register can separate energy (common direction) from the complete invariant frame; three member observations can also test phase/rotation differences. The actual physical Hamiltonian must explain how the 333-digit walk performs those operations, whether the local read is invariant, how the common energy is retained at reset, and why the physical work response selects the product of elementary gains rather than an ordinary sum of squared errors. The missing 17/13 stiffness and electromagnetic elementary gain remain independent. The native H36 is not changed or simulated in this calculation. No physical three-cycle timing, redshift, G or finite stopping rule derived. No changes to Proof 26 or GitHub.

Run `python certify_digits.py` (mpmath) and compare `pi_step_ledger.csv` with `source_step_ledger.csv`; run `OPENBLAS_NUM_THREADS=1 python verify_innovations.py` (SymPy, NumPy, matplotlib). The script checks the weighted projection identities at every step, the mutually orthogonal innovations, all grade overlaps, three pass endpoints, the exact C3 phase trace, and numerical determinants for every rank at two illustrative gains. See `verification.txt`, `running_settlement.csv`, `innovation_events.csv`, and `three_passes.png`.
