# The coupling polynomial as recursive Sierpiński counting

Continuation of ATOMIC_INVERSE_RECONSTRUCTION.md; not Proof 26. Exact finite algebra and conditional physical generator. The prior archive is preserved. No native value of alpha or G is derived.

## 1. Counts and their physical interpretation

The four-child Triforce hierarchy retains the central triangle (unlike the classical three-child gasket). At levels n=0,1,2, the read sizes are K^n with K=4. The signed count f(K,s)=1+sK+K² evaluates to 21,17,13. Depth parity (-1)^n explains the abstract signs; its identification with physical root exchange is open. The center is the average of the signed endpoint counts, not a zero branching factor: substituting sK into a geometric series would give 1+sK+s²K², not f(K,s).

The grade-preserving pair capacity is 1+K²+K⁴=f(K,+1)f(K,-1)=1+K²f(K,0). Thus 273=21×13=1+272. This is a structural capacity, not a claim of 273 physical degrees of freedom or nonzero matrix entries.

## 2. The unipotent generator cannot supply attenuation

L(z)=[[1,0],[z,1]]. For n=0,1,2 let S_n=L(z)^(tensor 2n). For all z, det S_n=1, tr S_n=4^n, S_n^-1=S_n(-z). For nonzero z the support sizes are 1,9,81. The total support is 91, capacity 273, diagonal count 21. Merely changing z (null-rotation parameter) cannot generate the alpha exponent. A scalar weighting t S_n has determinant t^(4^n), and the block sum has determinant t^21. This is a new physical scaling premise, not a consequence of L(z).

Distinguish the latter from tensor-power replication of a weighted primitive. If B=t S_1 for the four-dimensional block S_1, det B=t^4, det(B tensor B)=t^32. The two levels alone yield t^36, rather than t^20. Thus recursive counting is not the same as repeated loss along every ancestral path. To obtain the desired determinant the gain must apply once to each grade's own newly resolved detail, not be compounded on every inherited common record.

## 3. A precise recursive gain model preserving the common record

On each four-way node P0=11^T/4 and Pc=I-P0. A linear map commuting with every S4 label permutation has equal diagonal and equal off-diagonal entries. If it preserves the common record it is A(t)=P0+t Pc, uniquely determined by its (still free) contrast gain t. It is contractive for |t|<=1; if it is also a nonnegative stochastic matrix then -1/3<=t<=1. A(t)A(u)=A(tu). Idempotence would force t=0 or 1, so a nontrivial gain is a transmission map, not an idempotent registration projection.

Let D_n be the orthogonal detail projectors of the 64-leaf four-way tree; ranks 3,12,48. For the simultaneous order-three rotation Q, ranks of QD_n are 1,4,16. The common scalar E=11^T/64 is preserved. On the invariant contrast sector the map J=product_n[I+(t_n-1)D_n] has determinant t0 t1^4 t2^16, whereas on the full contrast sector the exponents are 3,12,48. The factors commute because grades are orthogonal. Thus if all t_n=t and the complete-frame source is selected, |det J_inv|²=|t|^42. With |t|²=alpha this is alpha^21. The same map can be represented in inverse Walsh coordinates using the existing orthogonal factors. No extra clocks are needed. The grade-preserving operation is conditional; neither geometry nor algebra forces temporal order or a common gain at different physical scales.

## 4. Nonspatial paired time-face implementation and remaining freedom

The same four-way records in two chambers can realize a conservative common-reference read. Let c²+s²=1. The orthogonal eight-coordinate interaction is

U=[[P0+c Pc,-s Pc],[s Pc,P0+c Pc]].

It commutes with simultaneous S4 relabelling, preserves both scalar records, and rotates only the two registered copies of each contrast. Its retained A-to-A read is A(c); complementary squared transmission is (1-c²)Pc. This is an abstract nonspatial coupling of registered amplitudes, not a new oscillator or spatial bond. The implementation has one common parameter, not 21. All c in [-1,1] are compatible with the same geometry and conservation. Therefore geometry, symmetry and losslessness do not fix c²=alpha. A time-face interaction action or independent electromagnetic normalization must supply that value; if the cross-chamber output rather than the retained output is read, its gain is s rather than c. The physical port choice is also open.

## 5. Consequence for the research

The counting part of the coupling polynomial is settled in the specified representation. The precise remaining requirements are: (i) select the detail-only map, rather than repeated tensor attenuation, from the native nonlinear vertex; (ii) derive its common gain from the paired time faces and show its scale independence; (iii) derive the source's collective complete-frame read and relative winding response; (iv) preserve additive mass registration and the drainless limit. No numerical fit is introduced here, and the existing Stage VII witness is not claimed to realize this map.

Reproduce with OPENBLAS_NUM_THREADS=1 python verify_recursive_generator.py. 83 assertions passed (symbolic exact and numerical projected determinants); historical 4200 checks retained, not rerun. No Lean run or live repository edits. Proofs 24 and 25 unchanged.
