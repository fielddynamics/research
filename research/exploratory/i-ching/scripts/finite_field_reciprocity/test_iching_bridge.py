"""Exact I Ching / finite-field bridge. Counterexamples are intentional tests.
No physical identification of the field algebra with gravity is asserted.
"""
from itertools import product, combinations
from collections import Counter
import numpy as np
import pytest
import mpmath as mp
from finite_geometry import field, mul, plane, registers

powers, logs = field()
def fp(x,n):
    return 0 if x == 0 else powers[(logs[x]*n)%4095]
def subfield(q): return {0}|{powers[i*(4095//(q-1))] for i in range(q-1)}
F8,F4,F16,F64 = map(subfield,(8,4,16,64))
def tr8(x):return x^fp(x,2)^fp(x,4)
beta=next(x for x in sorted(F8) if all(tr8(mul(fp(x,2**i),fp(x,2**j)))==int(i==j) for i,j in product(range(3),repeat=2)))
basis=[fp(beta,2**i) for i in range(3)]
omega=min(F4-{0,1})
def trig(a):
    return (basis[0] if a&1 else 0)^(basis[1] if a&2 else 0)^(basis[2] if a&4 else 0)
def hexa(a,b):return trig(a)^mul(trig(b),omega)
def rot(a):return ((a<<1)&7)|(a>>2)
def R(s):a,b=s;return b,a^b
def J(s):return s[::-1]
def S(s):return rot(s[0]),rot(s[1])
X=list(product(range(8),repeat=2)); idx={x:i for i,x in enumerate(X)}
orbits=sorted({tuple(sorted({s,R(s),R(R(s))})) for s in X}); oi={x:i for i,o in enumerate(orbits) for x in o}
reps=[o[0] for o in orbits[1:]]
def B(x,y):a,b=x;c,d=y;return ((a&d).bit_count()+(b&c).bit_count())%2
def trace64(z):
    return tr8(z^fp(z,8))
H=np.array([[(-1)**B(x,y) for y in X] for x in X],dtype=int)
N=np.array([[int(sum((-1)**B(x,y) for y in o)==3) for o in orbits[1:]] for x in reps],dtype=int)
U=np.array([[int(x in o)/np.sqrt(len(o)) for o in orbits] for x in X]); W=U.T@H@U/8
I=np.eye(21,dtype=int); ones=np.ones((21,21),dtype=int)
lines,baer=plane(); pencil=[l-{0} for l in lines if 0 in l]; d={x:i for i,l in enumerate(pencil) for x in l}; e={x:(d[x],d[-x%273]) for x in d};
rev=np.array([[-x%273==y for y in range(1,273)] for x in range(1,273)],dtype=int)
A,C,_=registers(); P=A.T@A/16; V=A.T/4; Z=C.T/np.sqrt(C.sum(1)); Q=Z@Z.T
# ordering of A's rows can differ from pencil ordering; the same formula holds.

def eq(a,b):np.testing.assert_allclose(a,b,atol=1e-11,rtol=1e-11)
def check(cases,name): assert cases[name]() is not False
def yes(v): assert bool(v)
def same(a,b):assert a==b
F={
 'self_dual_normal_basis':lambda:yes(all(tr8(mul(x,y))==int(i==j) for i,x in enumerate(basis) for j,y in enumerate(basis))),
 'normal_basis_trace_one':lambda:same(basis[0]^basis[1]^basis[2],1),
 'trigram_bijection':lambda:same({trig(a) for a in range(8)},F8),
 'heaven_earth_are_one_zero':lambda:same((trig(7),trig(0)),(1,0)),
 'trigram_xor_addition':lambda:yes(all(trig(a^b)==trig(a)^trig(b) for a,b in X)),
 'cyclic_lines_frobenius':lambda:yes(all(trig(rot(a))==fp(trig(a),2) for a in range(8))),
 'hexagram_bijection_gf64':lambda:same({hexa(*x) for x in X},F64),
 'xor_three_cycle_multiplication':lambda:yes(all(hexa(*R(x))==mul(omega,hexa(*x)) for x in X)),
 'swap_is_conjugation_mod_scalar':lambda:yes(all(hexa(*J(x))==mul(omega,fp(hexa(*x),8)) for x in X)),
 'axis_rotation_gf64_16th_power':lambda:yes(all(hexa(*S(x))==fp(hexa(*x),16) for x in X)),
 '21_projective_points':lambda:same(len({logs[hexa(*x)]//65%21 for x in X if x!=(0,0)}),21),
 'time_axis_projective_unit':lambda:same({hexa(*x) for x in [(7,0),(0,7),(7,7)]},F4-{0}),
 'unique_fixed_vector_line_over_gf16':lambda:same({x for x in powers if fp(x,16)==x},F16-{0}),
 'norm_to_trigram_7_fibers_3':lambda:same(sorted(Counter(fp(hexa(*x),9) for x in reps).values()),[3]*7),
 'rank_one_one_per_norm_fiber':lambda:same({fp(hexa(*x),9) for x in reps if 0 in x or x[0]==x[1]},F8-{0}),
 'swap_seven_fixed_projective_points':lambda:same(sum(oi[J(x)]==oi[x] for x in reps),7),
 'axis_rotation_three_fixed_projective_points':lambda:same(sum(oi[S(x)]==oi[x] for x in reps),3),
 'joint_invariance_only_ten_orbits':lambda:same(len({min(oi[x],oi[S(x)],oi[S(S(x))]) for x in X}),10),
}
@pytest.mark.parametrize('case',list(F),ids=list(F))
def test_field_bridge(case):check(F,case)

WALSH={
 'symplectic_trace_pairing':lambda:yes(all(B(x,y)==trace64(mul(hexa(*x),fp(hexa(*y),8))) for x,y in product(X,repeat=2))),
 'symplectic_rotation_invariant':lambda:yes(all(B(R(x),R(y))==B(x,y) for x,y in product(X,repeat=2))),
 'walsh_square_exact':lambda:eq(H@H,64*np.eye(64)),
 'polarity_incidence_symmetric':lambda:eq(N,N.T),
 'five_points_per_line':lambda:eq(N.sum(1),5*np.ones(21)),
 'incidence_design_exact':lambda:eq(N@N,4*I+ones),
 'nine_absolute_points':lambda:same(int(np.trace(N)),9),
 'incidence_spectrum':lambda:eq(np.linalg.eigvalsh(N),[-2]*9+[2]*11+[5]),
 'reduced_walsh_exact_blocks':lambda:eq(8*W,np.block([[np.ones((1,1)),np.sqrt(3)*np.ones((1,21))],[np.sqrt(3)*np.ones((21,1)),4*N-ones]])),
 'reduced_walsh_orthogonal':lambda:eq(W@W,np.eye(22)),
 'reduced_walsh_spectrum':lambda:eq(np.linalg.eigvalsh(W),[-1]*10+[1]*12),
 'lower_block_is_not_unitary':lambda:eq(np.linalg.svd(W[1:,1:],compute_uv=False),[1]*20+[1/8]),
}
# A projective line uses the GF64 -> GF4 trace, not the GF64 -> GF8 trace.
def tr64to4(z):return z^fp(z,4)^fp(z,16)
WALSH['polarity_hermitian_zero']=lambda:yes(all(N[i,j]==int(tr64to4(mul(hexa(*x),fp(hexa(*y),8)))==0) for i,x in enumerate(reps) for j,y in enumerate(reps)))
@pytest.mark.parametrize('case',list(WALSH),ids=list(WALSH))
def test_walsh_bridge(case):check(WALSH,case)

G={
 'complete_directed_graph':lambda:same(set(e.values()),set(permutations17())),
 'reciprocal_swap':lambda:yes(all(e[-x%273]==e[x][::-1] for x in d)),
 'no_pencil_loops':lambda:yes(all(i!=j for i,j in e.values())),
 '136_unordered_edges':lambda:same(len({tuple(sorted(pair)) for pair in e.values()}),136),
 '137_inverse_orbits_including_origin':lambda:same(len({min(x,-x%273) for x in range(273)}),137),
 'rational_baer_subplane_is_k5':lambda:same(set(e[x] for x in baer[0]-{0}),{(i,j) for i in rational() for j in rational() if i!=j}),
 'rational_pencil_count':lambda:same(len(rational()),5),
 'inverse_reverses_baer_color':lambda:yes(all((-x%273)%13==(-x)%13 for x in d)),
 'inverse_commutes_baer_projection':lambda:eq(rev@Q,Q@rev),
 'reciprocal_pencil_cross_gram':lambda:eq(V.T@rev@V,(np.ones((17,17))-np.eye(17))/16),
 'pencil_even_odd_ranks':lambda:same((np.linalg.matrix_rank((V+rev@V)/2),np.linalg.matrix_rank((V-rev@V)/2)),(17,16)),
 'baer_even_odd_ranks':lambda:same((np.linalg.matrix_rank((Z+rev@Z)/2),np.linalg.matrix_rank((Z-rev@Z)/2)),(7,6)),
 'even_pencil_spectrum':lambda:eq(np.linalg.eigvalsh(V.T@(np.eye(272)+rev)@V/2),[15/32]*16+[1]),
 'odd_pencil_spectrum':lambda:eq(np.linalg.eigvalsh(V.T@(np.eye(272)-rev)@V/2),[0]+[17/32]*16),
 'trigram_reversal_28_edges':lambda:same(len({tuple(sorted((a,b))) for a,b in X if a!=b}),28),
 'trigram_edges_7_matchings':lambda:same(sorted(Counter(a^b for a,b in combinations(range(8),2)).values()),[4]*7),
}
def permutations17():return ((i,j) for i,j in product(range(17),repeat=2) if i!=j)
def rational():return {i for i,l in enumerate(pencil) if len(l&baer[0])==4}
@pytest.mark.parametrize('case',list(G),ids=list(G))
def test_reciprocity(case):check(G,case)

with mp.workdps(400):
    z=mp.pi; digits=[]
    for _ in range(333):
        digit=int(z); digits.append(digit); z=(z-digit)*8
positions=[]; s=0
for digit in digits:
    s=(s+digit)%8;positions.append(s)
PI={
 'pi_visits_64_ordered_pairs':lambda:same(len(set(zip(positions,positions[1:]))),64),
 'pi_walk_not_xor_cycle':lambda:same(sum(c==a^b for a,b,c in zip(positions,positions[1:],positions[2:])),36),
 'first_pi_triple_counterexample':lambda:same((positions[:3],positions[0]^positions[1]),([3,4,5],7)),
 'fixed_digit_transition_not_bijection':lambda:yes(all(len({(b,(b+d)%8) for a,b in X})==8 for d in range(8))),
 'unique_linear_shift_order_three':lambda:same([(p,q) for p,q in product(range(2),repeat=2) if p==1 and all(iter_lin(a,b,p,q)==(a,b) for a,b in product(range(2),repeat=2))],[(1,1)]),
}
def iter_lin(a,b,p,q):
    for _ in range(3):a,b=b,(p*a)^(q*b)
    return a,b
@pytest.mark.parametrize('case',list(PI),ids=list(PI))
def test_pi_walk(case):check(PI,case)
