"""Exact orientation character and common seed reconstruction."""
import itertools
import pytest
import sympy as s
from test_common_mode_proof import I,W,J,G,O,pair,cp,z,F,D,M
E=(I+J)/2
K=(I-J)/2

def gate(u):
    Q,_=pair(u) if u else (I,I)
    return Q+(I-Q)*J

def normal(a,b):
    return next(n for n in range(1,8) if (n&a).bit_count()%2==0 and (n&b).bit_count()%2==0)

def odd_basis():
    B=s.Matrix.hstack(*K.columnspace())
    ns=[normal(*O[next(i for i in range(22) if B[i,j])][0]) for j in range(7)]
    return B,ns

def test_seed_dual_completion():
    L=s.Matrix.hstack(D,W*D)
    assert L.rank()==15 and E*L==L
    assert s.factor(cp(D*W*D))==z**14*(z-1)*(4*z+1)*(2*z**2-1)**3/32
    assert (D-F).rank()==7 and (W*D*W-F).rank()==7

@pytest.mark.parametrize('u',range(1,8))
def test_marked_seed_completion(u):
    Q,_=pair(u);P,_=pair(u,1)
    L=s.Matrix.hstack(Q,W*D)
    assert L.rank()==18 and P*L==L
    assert P-F==M*(I+gate(u))/2
    assert s.trace(gate(u)*M)==13 and s.trace((I+gate(u))*M/2)==17
    assert gate(u)**2==I and gate(u).T*G*gate(u)==G

@pytest.mark.parametrize('u',range(8))
def test_binary_representation(u):
    B,ns=odd_basis(); A=gate(u)
    assert A*E==E
    assert A*B==B*s.diag(*[(-1)**((u&n).bit_count()) for n in ns])
    for v in range(8): assert A*gate(v)==gate(u^v)

def test_character_sum():
    assert sum((gate(u) for u in range(8)),s.zeros(22))/8==E
    assert s.trace(E*M)==14 and s.trace(K*M)==7
    assert [s.trace(gate(u)*M) for u in range(8)]==[21]+[13]*7
    assert sum((M*(I-gate(u))/2 for u in range(1,8)),s.zeros(22))==4*K

def test_axis_average():
    assert sum((pair(u)[0] for u in range(1,8)),s.zeros(22))==3*I+4*D

def test_skew_channel_incidence():
    labels={(u,n) for u in range(1,8) for n in range(1,8) if (u&n).bit_count()%2}
    assert len(labels)==28
    for n in range(1,8): assert sum(b==n for a,b in labels)==4
    for u in range(1,8): assert sum(a==u for a,b in labels)==4
    assert len({tuple((-1)**((u&n).bit_count()) for n in range(1,8)) for u in range(1,8)})==7

def test_walsh_does_not_commute_with_gate():
    A=gate(7)
    assert (W*A-A*W).rank()==4

def test_signed_trace_does_not_fix_work():
    P=M*(I+gate(7))/2;N=M-P
    assert s.trace(P)==17 and s.trace(N)==4
    assert s.trace(P*gate(7))==17 and s.trace(N*gate(7))==-4
    # Weight 2 on the negative sector is equally invariant under the gate, but changes ratio.
    H=P+2*N
    assert s.trace(H*P)/s.trace(H*gate(7))==s.Rational(17,9)
