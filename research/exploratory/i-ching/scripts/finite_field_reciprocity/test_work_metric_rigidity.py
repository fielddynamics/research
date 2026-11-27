"""Exact shared-zone metric rigidity and conditional factorization tests."""
import sympy as s
import pytest
from test_orientation_character import I,W,J,G,O,pair,F,D,M,E,K,gate,odd_basis

U=E*(I-D)
A=s.Matrix.hstack(*U.columnspace())
B,ns=odd_basis()
B0=M*D

def compressed(X):
    return (X.T*G*X).inv()*X.T*G*W*X

def connected(X):
    seen={0}
    while True:
        nxt=seen|{j for i in seen for j in range(X.rows) if X[i,j]!=0}
        if nxt==seen: return len(seen)==X.rows
        seen=nxt

def test_even_span_and_complete_graph():
    assert A.cols==7 and (M*D*W*A).rank()==7
    assert s.Matrix.hstack(A,M*D*W*A).rank()==14
    assert all(abs(v)==s.Rational(1,4) for v in compressed(A))

def test_odd_connectivity():
    assert B.cols==7 and connected(compressed(B))

@pytest.mark.parametrize('i',range(7))
def test_character_signatures(i):
    u=ns[i]
    assert A[:,i] in [A[:,j] for j in range(7)]
    # Each outside even line has a unique three-axis incidence signature.
    signatures=[tuple((A[:,j].T*G*pair(v)[0]*A[:,j])[0]/(A[:,j].T*G*A[:,j])[0] for v in range(1,8)) for j in range(7)]
    assert len(set(signatures))==7 and sum(signatures[i])==3
    assert all(sum(sig)==3 for sig in signatures)
    assert sum((pair(v)[0] for v in range(1,8)),s.zeros(22))==3*I+4*D

@pytest.mark.parametrize('a,b',[(1,1),(1,2),(2,1),(3,4),(s.Rational(1,3),2)])
def test_weighted_formula(a,b):
    H=a*(E-F)+b*K
    assert H.T*G==G*H and H*W==W*H
    for u in range(1,8):
        Q=pair(u)[0]-F; P=M*(I+gate(u))/2; S=M*gate(u)
        assert H*Q==Q*H and H*S==S*H
        assert s.trace(H*P)==14*a+3*b
        assert s.trace(H*S)==14*a-b
        assert s.trace(H*Q)==10*a+3*b
        assert (s.trace(H*S)==s.trace(H*Q))==(a==b)

def test_reciprocal_phase_symmetry_closes_metric():
    # Opposite orientation of one independent pair is a distinct record.
    i=next(i for i in range(22) if J[i,i]==0)
    L=I.copy();L[i,i]=-1
    assert L*F==F and L.T*G*L==G
    assert L*E!=E*L
    a,b=s.symbols('a b'); H=a*(E-F)+b*K
    assert all(s.expand(x.subs(b,a))==0 for x in H*L-L*H)
    assert any(s.expand(x.subs({a:1,b:2}))!=0 for x in H*L-L*H)

def rmat(n):
    return s.Matrix(n*n,n*n,lambda i,j:int(i==(j%n)*n+((j//n)^(j%n))))

@pytest.mark.parametrize('n',[2,4,8])
def test_scalar_product_metric(n):
    R=rmat(n); H=s.eye(n)*3; K0=s.eye(n)*7
    T=s.kronecker_product(H,K0)
    assert R**3==s.eye(n*n) and R.T*T*R==T
    assert T==21*s.eye(n*n)

@pytest.mark.parametrize('n',[2,4,8])
def test_nonuniform_product_not_isometric(n):
    R=rmat(n); A0=s.diag(*range(1,n+1)); B0=s.eye(n)+s.ones(n)/2
    for h,k in [(A0,A0),(B0,B0),(A0,B0),(s.eye(n),A0)]:
        T=s.kronecker_product(h,k)
        assert R.T*T*R!=T

def test_symbolic_product_metric_two_state():
    a,b,c,d,e,f=s.symbols('a b c d e f',real=True)
    h=s.Matrix([[a,c],[c,b]]);k=s.Matrix([[d,f],[f,e]])
    T=s.kronecker_product(h,k);R=rmat(2)
    U=R.T*T*R-T
    # Diagonal equations force proportional factors, then constant diagonals.
    assert s.expand(U[2,2]-(a*e-b*d))==0
    # For proportional factors with constant diagonals, nonzero correlation forces singularity.
    V=U.subs({b:a,d:a,e:a,f:c})
    assert any(s.factor(x)==c*(a-c) or s.factor(x)==-c*(a-c) for x in V)
