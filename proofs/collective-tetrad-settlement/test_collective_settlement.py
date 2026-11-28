"""Algebraic and numerical checks of the conditional four-face theorem."""
import itertools
import numpy as np
import pytest
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/2
P=np.eye(4)-np.ones((4,4))/4
U=np.repeat(np.eye(4),16,axis=0)/4
I=np.eye(3)
H4=np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]],float)/2
B=np.kron(np.kron(H4,H4),H4)
RNG=np.random.default_rng(20261127)
DIRECTIONS=np.array([[1,0,0],[1,1,1],[2,-3,4],[-1,2,0]],float)
DIRECTIONS/=np.linalg.norm(DIRECTIONS,axis=1)[:,None]
FIELDS=[0.01,0.2,1.,2.,10.]

def q(z): return z/(1+np.linalg.norm(z))
def derivative(z):
    r=np.linalg.norm(z)
    return P/(1+r)-np.outer(z,z)/(r*(1+r)**2) if r else P.copy()
def cost(p):
    b=np.linalg.norm(p)
    return -b-np.log1p(-b)
def joint(x,p): return x@x/2-x@p+cost(p)
def eff(x):
    r=np.linalg.norm(x)
    return r*r/2-r+np.log1p(r)
def fd(fun,x,h=1e-6):
    return np.column_stack([(fun(x+h*d)-fun(x-h*d))/(2*h) for d in np.eye(len(x))])

def test_exact_frame():
    t=s.Matrix(T*2)/2
    t=t.applyfunc(s.nsimplify)
    assert t.T*t==s.eye(3)
    assert t*t.T==s.eye(4)-s.ones(4)/4

def test_exact_energy():
    r=s.symbols('r',nonnegative=True)
    b=r/(1+r)
    assert s.simplify(r**2/2-r*b-b-s.log(1-b)-(r**2/2-r+s.log(1+r)))==0
    assert s.simplify(s.diff(r**2/2-r+s.log(1+r),r)-r**2/(1+r))==0

def test_exact_tangent_ratio():
    r=s.symbols('r',positive=True)
    mu=r/(1+r)
    assert s.simplify(s.diff(r*mu,r)/mu-(2-mu))==0

def test_exact_locality_counterexample():
    z=s.Matrix([1,1,-1,-1]); zz=s.Matrix([s.sqrt(3)]+[-1/s.sqrt(3)]*3)
    h=lambda v:v/(1+s.Abs(v))
    p=s.eye(4)-s.ones(4)/4
    assert (z.T*z)[0]==(zz.T*zz)[0]==4
    assert p*z.applyfunc(h)==z/2
    assert (p*zz.applyfunc(h)-s.sqrt(3)*zz/4).applyfunc(s.simplify)==s.zeros(4,1)
    # Raw independent saturation does not preserve closure in general.
    assert s.simplify(sum(zz.applyfunc(h)))!=0

def test_quadratic_invariant():
    a=np.array([[1,2,3,4],[2,5,6,7],[3,6,8,9],[4,7,9,10]],float)
    perms=[np.eye(4)[list(p)] for p in itertools.permutations(range(4))]
    avg=sum(m@a@m.T for m in perms)/24
    np.testing.assert_allclose(P@avg@P,(avg[0,0]-avg[0,1])*P,atol=1e-13)

def test_zero():
    np.testing.assert_array_equal(q(np.zeros(4)),np.zeros(4))
    np.testing.assert_array_equal(derivative(np.zeros(4)),P)

@pytest.mark.parametrize('perm',list(itertools.permutations(range(4))))
def test_face_permutation(perm):
    m=np.eye(4)[list(perm)]; z=T@np.array([.7,-2.,1.1])
    np.testing.assert_allclose(q(m@z),m@q(z),atol=1e-14)
    np.testing.assert_allclose(derivative(m@z),m@derivative(z)@m.T,atol=1e-14)

@pytest.mark.parametrize('r',FIELDS)
@pytest.mark.parametrize('direction',DIRECTIONS)
def test_settlement_and_hessian(r,direction):
    x=r*direction; z=T@x; p=T.T@q(z)
    b=np.linalg.norm(p); mu=r/(1+r)
    np.testing.assert_allclose(p,(1-b)*x,rtol=1e-12,atol=1e-12)
    assert b==pytest.approx(mu)
    assert abs(np.sum(q(z)))<1e-13
    np.testing.assert_allclose(joint(x,p),eff(x),rtol=1e-8,atol=1e-13)
    S=T.T@derivative(z)@T
    np.testing.assert_allclose(S,fd(lambda v:T.T@q(T@v),x),rtol=1e-7,atol=2e-9)
    np.testing.assert_allclose(np.linalg.eigvalsh(S),[1/(1+r)**2,1/(1+r),1/(1+r)],atol=1e-13)
    np.testing.assert_allclose(np.linalg.eigvalsh(I-S),[mu,mu,r*(r+2)/(1+r)**2],atol=1e-13)
    np.testing.assert_allclose(derivative(z)@np.ones(4),0,atol=1e-14)
    np.testing.assert_allclose(fd(lambda v:np.array([eff(v)]),x).ravel(),mu*x,rtol=5e-6,atol=2e-8)

@pytest.mark.parametrize('r',[0.1,0.5,1.,3.,8.])
def test_independent_minimization(r):
    # optimize over a radial unconstrained parametrization of the open ball
    x=r*DIRECTIONS[2]
    pmap=lambda w:w/(1+np.linalg.norm(w))
    res=minimize(lambda w:joint(x,pmap(w)),np.zeros(3),method='BFGS',tol=1e-10)
    np.testing.assert_allclose(pmap(res.x),x/(1+r),atol=2e-6)
    assert res.fun==pytest.approx(eff(x),abs=1e-9)

@pytest.mark.parametrize('seed',range(10))
def test_full_read_factorization(seed):
    rng=np.random.default_rng(seed); r=rng.normal(size=64)
    Q=U@P@U.T
    z=P@U.T@r
    np.testing.assert_allclose(U.T@U,np.eye(4),atol=1e-14)
    np.testing.assert_allclose(B.T@B,np.eye(64),atol=1e-14)
    assert np.linalg.norm(z)**2==pytest.approx((B@r)@(B@Q@B.T)@(B@r),abs=1e-12)
    detail=(np.eye(64)-Q)@rng.normal(size=64)
    np.testing.assert_allclose(P@U.T@(r+detail),z,atol=1e-14)
    np.testing.assert_allclose(q(P@U.T@(r+detail)),q(z),atol=1e-14)

def test_full_norm_not_coarse_norm():
    z=T@np.array([1.,0,0]); r=U@z
    r2=r+np.ones(64)/8
    assert np.linalg.norm(r2)==pytest.approx(np.sqrt(2))
    np.testing.assert_allclose(P@U.T@r2,z,atol=1e-14)

def test_incomplete_snapshot():
    z1=np.array([1.,-1,0,0]); z2=np.array([1.,-1,2,-2])
    np.testing.assert_array_equal(z1[:2],z2[:2]); assert q(z1)[0]!=pytest.approx(q(z2)[0])

@pytest.mark.parametrize('seed',range(10))
def test_read_order(seed):
    rng=np.random.default_rng(seed); r=rng.normal(size=64); recovered=np.empty(64)
    for i in rng.permutation(64): recovered[i]=r[i]
    np.testing.assert_allclose(q(P@U.T@recovered),q(P@U.T@r),atol=1e-15)

@pytest.mark.parametrize('r',[0.,0.1,1.,10.])
@pytest.mark.parametrize('seed',[0,1,2])
def test_rate_convergence(r,seed):
    x=r*DIRECTIONS[1]; rng=np.random.default_rng(seed); p0=rng.normal(size=3); p0*=.8/np.linalg.norm(p0)
    out=solve_ivp(lambda t,p:(1-np.linalg.norm(p))*x-p,[0,32],p0,rtol=1e-10,atol=1e-12,dense_output=True)
    t=np.linspace(0,32,200); ps=out.sol(t).T; b=np.linalg.norm(ps,axis=1)
    assert np.max(b)<=max(.8,r/(1+r))+1e-9
    np.testing.assert_allclose(ps[-1],x/(1+r),atol=1e-8)
    energies=np.array([cost(p)-x@p for p in ps]); assert np.max(np.diff(energies))<1e-9

def test_isotropy_exchange_not_uniqueness():
    omega=lambda r:r*np.exp(.2*r*(r-1)/(1+r)**3)
    assert omega(2)!=pytest.approx(2)
    for r in [.01,.1,1,10,100]: assert omega(r)*omega(1/r)==pytest.approx(1)
    assert omega(1e-8)/1e-8==pytest.approx(1)
    assert omega(1e8)/1e8==pytest.approx(1)
