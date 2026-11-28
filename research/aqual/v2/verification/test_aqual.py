import numpy as np
import pytest
from scipy.integrate import quad
import sympy as sp
from aqual import *

X=[.001,.01,.1,.5,1,2,10,100,1000]
@pytest.mark.parametrize('x',X)
def test_exchange(x):
    assert np.isclose(mu(x)+mu(1/x),1)
    assert np.isclose(capacity(x)+capacity(1/x),34)
    assert np.isclose(x*(1-mu(x)),mu(x))
@pytest.mark.parametrize('x',X)
def test_integral(x):
    expected=quad(lambda t:2*t*t/(1+t),0,x,epsabs=1e-15)[0]
    assert np.isclose(energy(x*x),expected,rtol=2e-10,atol=1e-15)
@pytest.mark.parametrize('x',X)
def test_inverse(x):
    assert np.isclose(total(source(x)),x,rtol=1e-12)
    assert np.isclose(x-source(x),mu(x))
@pytest.mark.parametrize('x',X)
def test_dual(x):
    z=source(x)
    assert np.isclose(dual(z),dual_closed(z),rtol=2e-7,atol=1e-14)
    for t in [0,x/2,2*x,3*x]:
        assert 2*z*t-energy(t*t)<=dual(z)+1e-10
@pytest.mark.parametrize('x',X)
def test_bound(x):
    b=bound_mu(x)
    assert np.isclose(x*(1-b)**2,b)
    assert np.isclose(b,np.sqrt(x*b)/(1+np.sqrt(x*b)))
@pytest.mark.parametrize('x',X)
def test_response(x):
    p=x*np.array([1,2,3])/np.sqrt(14)
    a=jacobian(p);ev=np.linalg.eigvalsh(a)
    assert np.allclose(ev,[mu(x),mu(x),x*(x+2)/(x+1)**2])
    assert np.isclose(ev[-1]/ev[0],2-mu(x))
@pytest.mark.parametrize('r',[.01,.1,.5,1,2,10,100])
def test_mass(r):
    g=point_mass(r); v=np.sqrt(r*g)
    assert np.isclose(decode(r,v),1)
    h=r*1e-5
    assert np.isclose((potential(r+h)-potential(r-h))/(2*h),g,rtol=1e-8)
@pytest.mark.parametrize('x',X)
def test_settlement(x):
    p=np.array([x,0,0]);q=settle(p);b=np.linalg.norm(q)
    assert np.allclose(q/(1-b),p,rtol=1e-10)
    assert np.isclose(p@q-vacancy_cost(b),vacancy_dual(x))
    assert np.isclose(x*x-2*vacancy_dual(x),energy(x*x),atol=1e-14)
@pytest.mark.parametrize('seed',range(10))
def test_strict_monotonicity(seed):
    r=np.random.default_rng(seed);p,q=r.normal(size=(2,3));assert (flux(p)-flux(q))@(p-q)>0
@pytest.mark.parametrize('a',[1,1.4,2,3])
def test_shell(a):
    A=np.diag([a,1.,1.]);v=shell_potential([0,0,0],A,n=64)
    for x in [[.1,0,0],[0,.3,0],[.2,.1,.2]]:assert np.isclose(shell_potential(x,A,n=64),v,rtol=1e-10)
@pytest.mark.parametrize('b',[[0,0,0],[.2,.1,0],[.4,0,.1]])
def test_poisson_kernel(b):
    b=np.array(b);n,w=sphere_quadrature();s=poiss_kernel(n,b)
    assert np.isclose(w@s,1,rtol=1e-10)
    assert np.allclose((w*s)@n,b,atol=1e-10)
    assert np.isclose((w*s)@(1/np.linalg.norm(n-[0,0,2],axis=1)),1/np.linalg.norm(b-[0,0,2]),rtol=1e-10)

def test_tetrahedral_trace_and_alias():
    n=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)
    T=np.array([[1,2,3],[2,4,5],[3,5,6]]);b=np.array([.2,.3,.4]);c=2;R=.1
    def f(p):return c+R*p@b+R**2/2*np.einsum('ni,ij,nj->n',p,T,p)
    assert np.isclose(sum(f(n)),4*c+2*R**2/3*np.trace(T))
    assert np.allclose(3/(8*R)*(n.T@f(n)+(-n).T@f(-n)),b)

def test_qmond_curl():
    u,v=sp.symbols('u v',positive=True);p=sp.Matrix([2*u,4*v]);z=sp.sqrt(p.dot(p));nu=(1+sp.sqrt(1+4/z))/2
    c=sp.diff(nu*p[1],u)-sp.diff(nu*p[0],v)
    assert abs(float(c.subs({u:1,v:1})))>1e-4

def test_symbolic_energy():
    y=sp.symbols('y',positive=True);F=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
    assert sp.simplify(sp.diff(F,y)-sp.sqrt(y)/(1+sp.sqrt(y)))==0
    Fb=y+sp.sqrt(y)-(sp.Rational(2,3)*sp.sqrt(y)+sp.Rational(1,6))*sp.sqrt(1+4*sp.sqrt(y))+sp.Rational(1,6)
    assert sp.simplify(sp.diff(Fb,y)-(sp.sqrt(1+4*sp.sqrt(y))-1)/(sp.sqrt(1+4*sp.sqrt(y))+1))==0

def test_zero_and_phantom():
    assert energy(0)==0 and np.all(jacobian([0,0,0])==0)
    for r in [.1,1,10]:
        h=r*1e-5
        def q(r):return r*r*mu(point_mass(r))
        assert np.isclose((q(r+h)-q(r-h))/(2*h)/(4*np.pi*r*r),phantom_density(r),rtol=1e-8)
