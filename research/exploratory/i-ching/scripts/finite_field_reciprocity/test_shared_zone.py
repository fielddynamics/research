"""Exact finite shared-zone geometry. Physical read selection is not assumed."""
from itertools import product
from collections import Counter
import numpy as np
import sympy as sp
import pytest

X=list(product(range(8), repeat=2)); Xset=set(X)
def R(x): a,b=x; return b,a^b
def J(x): return x[::-1]
def orbit(x): return tuple(sorted({x,R(x),R(R(x))}))
O=sorted({orbit(x) for x in X}); O1=O[1:]; idx={x:i for i,x in enumerate(X)}
def B(x,y): a,b=x;c,d=y;return ((a&d).bit_count()+(b&c).bit_count())%2
H=np.array([[(-1)**B(x,y) for y in X] for x in X],dtype=np.int64)
N=np.array([[int(sum((-1)**B(x[0],y) for y in o)==3) for o in O1] for x in O1],dtype=np.int64)
J21=np.array([[int(orbit(J(y[0]))==x) for y in O1] for x in O1],dtype=np.int64)
I=np.eye(21,dtype=np.int64)
def zones(u):
    S={x for x in X if x[0]^x[1] in (0,u)}
    A={R(x) for x in S}; C={R(x) for x in A}; U=S|A|C
    Q=np.diag([int(set(o)<=U) for o in O1]); P2=2*Q+(I-Q)@(I+J21)
    return S,A,C,U,Q,P2

@pytest.mark.parametrize('u',range(1,8))
def test_threefold_shared(u):
    S,A,C,U,Q,P2=zones(u); T=set(product((0,u),repeat=2))
    assert len(S)==len(A)==len(C)==16
    assert S&A==S&C==A&C==T
    assert len(U)==40 and len(Xset-U)==24
    assert Counter(len(set(o)&S) for o in O1)=={0:8,1:12,3:1}
    assert np.trace(Q)==13 and np.trace(P2)==34
    assert np.array_equal(P2@P2,2*P2) and np.array_equal(P2@Q,2*Q)
    assert np.array_equal(Q@J21,J21@Q)
    assert np.trace(Q@J21)==7 and np.trace((I-Q)@J21)==0

@pytest.mark.parametrize('u',range(1,8))
def test_walsh_shared(u):
    S,*_=zones(u); p=np.diag([int(x in S) for x in X]); q64=H@p@H
    dual={y for y in X if all(B(x,y)==0 for x in S)}
    assert len(dual)==4 and dual<=S
    assert np.array_equal(p@q64,q64@p)
    assert np.trace(p@q64)==256
    assert np.array_equal((p@q64)@(p@q64),64*p@q64)

def test_hamming_partition():
    assert Counter((a^b).bit_count() for a,b in X)=={0:8,1:24,2:24,3:8}
    assert all((a^(b^7)).bit_count()==3-(a^b).bit_count() for a,b in X)

@pytest.mark.parametrize('i,j',product(range(2),repeat=2))
def test_each_chamber_block(i,j):
    S,*_=zones(7); block={(a,b) for a,b in X if a.bit_count()%2==i and b.bit_count()%2==j}
    assert len(block)==16 and len(block&S)==4

def test_walsh_leakage():
    *_,Q,P2=zones(7); Wnum=4*N-np.ones_like(N)
    assert np.array_equal(N@J21,J21@N)
    assert sp.Matrix((I-Q)@Wnum@Q).rank()==6
    assert sp.Matrix((2*I-P2)@Wnum@P2).rank()==2

def test_unique_cyclic_axis():
    assert [u for u in range(1,8) if ((u<<1)&7)|(u>>2)==u]==[7]

def test_reciprocal_edges():
    assert Counter((a^b).bit_count() for a,b in X if a<b)=={1:12,2:12,3:4}
