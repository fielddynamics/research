"""Walsh skew channels, exact signed-Pauli averaging and symmetry obstructions."""
from itertools import product, combinations
import numpy as np
import pytest
from test_iching_bridge import X, H as H64, R, J, idx, orbits

n=8
I=np.eye(n,dtype=int)
H=np.array([[(-1)**((a&b).bit_count()%2) for b in range(n)] for a in range(n)])
def parity(x):return x.bit_count()%2
def pauli(d,k):return np.array([[(-1)**parity(k&j) if i==j^d else 0 for j in range(n)] for i in range(n)])
labels=list(product(range(n),repeat=2))
odd=[(d,k) for d,k in labels if parity(d&k)]
even=[(d,k) for d,k in labels if not parity(d&k)]
P={v:pauli(*v) for v in labels}
def perm(f):return np.array([[int(i==idx[f(x)]) for x in X] for i in range(64)])
RR=perm(R); SS=perm(J); W=H64/8
Aminus=(np.eye(64)-W)/2
U=sum(np.outer(P[v].ravel(),P[v].ravel()) for v in odd)/8

def linear(cols,x):
    y=0
    for i in range(3):
        if x>>i&1:y^=cols[i]
    return y
GL=[c for c in product(range(1,8),repeat=3) if len({linear(c,x) for x in range(8)})==8]
def act(c,d,k):
    return linear(c,d),next(l for l in range(8) if all(parity(l&linear(c,x))==parity(k&x) for x in range(8)))
def avg_channel(x):return sum(P[v]@x@P[v].T for v in odd)/28

def eq(a,b):np.testing.assert_allclose(a,b,atol=1e-12,rtol=1e-12)
@pytest.mark.parametrize('d',range(1,8))
def test_four_skew_labels_per_shift(d):
    assert sum(dd==d for dd,k in odd)==4
@pytest.mark.parametrize('k',range(1,8))
def test_four_skew_labels_per_character(k):
    assert sum(kk==k for d,kk in odd)==4
@pytest.mark.parametrize('v',odd)
def test_skew_orthogonal_and_square(v):
    a=P[v];eq(a.T,-a);eq(a@a,-I);eq(a.T@a,I)

def test_walsh_as_twisted_transpose():
    for a,b in X:
        M=np.zeros((8,8),dtype=int);M[a,b]=1
        eq((H64@M.ravel()).reshape(8,8),H@M.T@H)

def test_walsh_change_coordinates():
    for v in labels:
        M=P[v]@H
        eq((H64@M.ravel()).reshape(8,8),8*P[v].T@H)

def test_pauli_basis_orthogonal():
    z=np.stack([p.ravel() for p in P.values()]);eq(z@z.T,8*np.eye(64))

def test_skew_projector_is_transpose_odd():
    T=np.array([[int((a,b)==(d,c)) for c,d in X] for a,b in X]);eq(U,(np.eye(64)-T)/2)

def test_walsh_ranks():
    assert np.trace(W)==8;assert np.linalg.matrix_rank(Aminus)==28;assert len(even)==36

def test_pauli_characters_distinct():
    C=np.array([[(-1)**(parity(d&l)^parity(k&e)) for d,k in labels] for e,l in labels]);eq(C.T@C,64*np.eye(64))

def test_pauli_adjoint_sign():
    for e,l in labels:
        for d,k in labels:
            a=P[e,l];b=P[d,k];eq(a@b@a.T,(-1)**(parity(d&l)^parity(k&e))*b)

def test_gl_size_and_transitivity():
    assert len(GL)==168;assert {act(c,*odd[0]) for c in GL}==set(odd)

def test_gl_conjugation():
    for c in GL:
        M=np.array([[int(i==linear(c,j)) for j in range(8)] for i in range(8)])
        for v in odd: eq(M@P[v]@M.T,P[act(c,*v)])

def test_pauli_twirl_of_covariance():
    x=np.arange(1,29,dtype=float);x/=np.linalg.norm(x);C=np.outer(x,x)
    signs=np.array([[(-1)**(parity(d&l)^parity(k&e)) for d,k in odd] for e,l in labels]);
    D=sum(C*np.outer(s,s) for s in signs)/64;eq(D,np.diag(x*x))
    maps=[np.array([odd.index(act(c,*v)) for v in odd]) for c in GL]
    eq(sum(D[np.ix_(m,m)] for m in maps)/168,np.eye(28)/28)

def test_marked_time_axis_breaks_transitivity():
    G=[c for c in GL if linear(c,7)==7];assert len(G)==24
    selected={(d,k) for d,k in odd if d==7};assert len(selected)==4
    assert all({act(c,*v) for v in selected}==selected for c in G)

def test_marked_covariance_not_uniform():
    cov=np.diag([1/4 if d==7 else 0 for d,k in odd]);assert np.trace(cov)==1
    assert not np.allclose(cov,np.eye(28)/28)
    for c in GL:
        if linear(c,7)==7:
            m=[odd.index(act(c,*v)) for v in odd];eq(cov[np.ix_(m,m)],cov)

@pytest.mark.parametrize('d,k',[(0,0),(1,0),(0,1),(1,1),(7,7),(3,4),(2,6)])
def test_channel_eigenvalues(d,k):
    a=P[d,k]; expected=1 if (d,k)==(0,0) else (1 if parity(d&k) else -1)/7
    eq(avg_channel(a),expected*a)

def test_channel_formula_all_matrix_units():
    for a,b in X:
        m=np.zeros((8,8));m[a,b]=1;eq(avg_channel(m),(np.trace(m)*I-m.T)/7)

def test_channel_trace_preserving_unital():
    eq(avg_channel(I),I);m=np.arange(64).reshape(8,8);eq(np.trace(avg_channel(m)),np.trace(m))

def test_channel_convergence():
    m=np.arange(64).reshape(8,8);eq(avg_channel(avg_channel(m)),np.trace(m)*I/8+(m-np.trace(m)*I/8)/49)

def test_walsh_s3_characters_and_multiplicities():
    eq(W@RR,RR@W);eq(W@SS,SS@W)
    for sign,expected in [(-1,(7,3,9)),(1,(8,4,12))]:
        E=(np.eye(64)+sign*W)/2
        a,b,c=(round(np.trace(E@M)) for M in (np.eye(64),SS,RR))
        assert ((a+3*b+2*c)//6,(a-3*b+2*c)//6,(a-c)//3)==expected

def test_symmetry_does_not_fix_continuous_gain():
    for p in (0,.001,1/137,1/28,.5,1):
        a=np.sqrt(1-p)*np.eye(28);b=np.sqrt(p)*np.eye(28);eq(a.T@a+b.T@b,np.eye(28))

def test_137_28_combination_not_exact_measured():
    from fractions import Fraction
    pred=Fraction(137)+Fraction(1,28);assert pred==Fraction(3837,28)
    assert 0.00028 < 137.035999177-float(pred) < 0.00029
