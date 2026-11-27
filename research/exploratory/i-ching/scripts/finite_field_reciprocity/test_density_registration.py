"""Density-register rank, common-mode and attenuation discriminators."""
import numpy as np
import pytest
import sympy as s
from itertools import product

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
kron3=lambda a,b,c:np.kron(np.kron(a,b),c)
B=np.array([kron3(*p)/np.sqrt(8) for p in product([I,X,Y,Z],repeat=3)])
U=(I+1j*(X+Y+Z))/2
U3=kron3(U,U,U)
# Explicit unitary spectral basis of U3 (two phase-identical extremes and two triples).
vals,vecs=np.linalg.eigh(X+Y+Z)
V=kron3(vecs,vecs,vecs)[:,[0,7,1,2,4,3,5,6]]
blocks=[slice(0,2),slice(2,5),slice(5,8)]

def twirl(a):
    return sum(np.linalg.matrix_power(U3,j)@a@np.linalg.matrix_power(U3,j).conj().T for j in range(3))/3

def rand(seed,shape):
    rng=np.random.default_rng(seed)
    return rng.normal(size=shape)+1j*rng.normal(size=shape)

def project_blocks(a):
    b=np.zeros_like(a)
    for q in blocks: b[q,q]=a[q,q]
    return b

@pytest.mark.parametrize('seed',range(4))
def test_parseval(seed):
    z=rand(seed,(8,)); rho=np.outer(z,z.conj()); coeff=np.einsum('aij,ji->a',B,rho)
    assert np.max(np.abs(coeff.imag))<1e-12
    assert np.allclose(np.einsum('a,aij->ij',coeff,B),rho)
    assert np.isclose(np.vdot(coeff,coeff),np.vdot(z,z)**2)

def test_twirl_block_form():
    assert np.allclose(U3@U3@U3,-np.eye(8))
    a=rand(4,(8,8));a=a+a.conj().T
    assert np.allclose(twirl(a),V@project_blocks(V.conj().T@a@V)@V.conj().T)
    assert np.allclose(twirl(twirl(a)),twirl(a))

@pytest.mark.parametrize('r,d',[(1,12),(2,19),(3,21),(4,21)])
def test_rank_and_tangent(r,d):
    # Fixed-trace tangent to a block Gram map of r independent columns.
    A=rand(r,(8,r)); A/=np.linalg.norm(A)
    basis=[]
    for i,j in product(range(8),range(r)):
        for phase in [1,1j]:
            D=np.zeros_like(A);D[i,j]=phase
            D-=np.real(np.vdot(A,D))*A
            b=project_blocks(D@A.conj().T+A@D.conj().T)
            basis.append(np.r_[b.real.ravel(),b.imag.ravel()])
    assert np.linalg.matrix_rank(np.array(basis),tol=1e-9)==d
    for q in blocks: assert np.linalg.matrix_rank((A@A.conj().T)[q,q],tol=1e-9)==min(q.stop-q.start,r)

@pytest.mark.parametrize('seed',range(4))
def test_three_snapshot_surjectivity(seed):
    # Every positive definite invariant target is the twirl of <=3 snapshots.
    target=np.zeros((8,8),complex); A=np.zeros((8,3),complex)
    for i,q in enumerate(blocks):
        m=q.stop-q.start; L=rand(seed*3+i,(m,m)); target[q,q]=L@L.conj().T
        A[q,:m]=L
    target/=np.trace(target).real; A/=np.linalg.norm(A)
    states=V@A
    assert np.allclose(twirl(states@states.conj().T),V@target@V.conj().T)
    assert np.isclose(np.linalg.norm(states)**2,1)


def test_common_line_not_trace():
    # f in the signless Pauli orbit labeling; common vector is 3 at identity,
    # and one on pure X-, Y-, Z-strings (all other labels zero).
    F=sum(kron3(I+p,I+p,I+p) for p in [X,Y,Z])
    assert np.linalg.matrix_rank(F,tol=1e-9)==3
    assert np.isclose(np.trace(F),24)
    assert np.isclose(np.trace(F@F),240)
    assert np.allclose(twirl(F),F)
    assert not np.allclose(F,3*np.eye(8))


def test_trace_fixed_projection_metric():
    # e identity coordinate, f normalized common line; overlap^2=3/10.
    c2=s.Rational(3,10)
    assert 1/c2-1==s.Rational(7,3)
    assert (17+1/c2-1)/(13+1/c2-1)==s.Rational(29,23)
    # Test actual register projectors in the previous rational orbit basis.
    from test_common_mode_proof import I as E22,W,F,G,pair,M,f
    e=E22[:,0];v=M*e
    assert (v.T*G*v)[0]==s.Rational(7,10)
    Bv=v*v.T*G/s.Rational(7,10)
    H=M+s.Rational(7,3)*Bv
    for u in range(1,8):
        Q,_=pair(u);P,_=pair(u,1)
        assert (P-F)*v==v and (Q-F)*v==v
        assert s.trace(H*(P-F))/s.trace(H*(Q-F))==s.Rational(29,23)
    assert W*e!=e


def test_walsh_trace_compression():
    from test_common_mode_proof import I as E22,W,G
    e=E22[:,0]; T=E22-e*e.T*G
    K=T*W*T
    # Singular squares in weighted inner product: 0, 1/64, 1 (20).
    z=s.Symbol('z'); A=K.T*G*K*G.inv()
    assert s.expand(A.charpoly(z).as_expr()-z*(z-1)**20*(z-s.Rational(1,64)))==0

@pytest.mark.parametrize('p',[s.Rational(1,2),s.Rational(1,7),s.Rational(1,137)])
def test_density_attenuation(p):
    assert (p*s.eye(21)).det()==p**21
    assert ((p*s.eye(21)).T*(p*s.eye(21))).det()==p**42
    t=s.sqrt(p); assert ((t*s.eye(21)).T*(t*s.eye(21))).det()==p**21


def test_core_norm_not_total_norm():
    # Inherited origin-core coupling -T from Stage IX, choose one origin
    # scalar and all eight core entries with a relative imaginary phase.
    signs=np.array(list(product([-1,1],repeat=3)))
    T=np.c_[np.ones(8),signs]; z=1j*np.ones(8); c=np.array([1,0,0,0])
    zdot=1j*T@c; cdot=1j*T.T@z
    assert np.isclose(2*np.real(np.vdot(z,zdot)),16)
    assert np.isclose(2*np.real(np.vdot(c,cdot)),-16)
