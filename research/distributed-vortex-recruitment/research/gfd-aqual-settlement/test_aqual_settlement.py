"""AQUAL from registered response: exact algebra, numerical tests and no-go diagnostics.
All fields dimensionless (a0=1); inherited native overlap is NOT identified with g/a0.
Run: python -m pytest -q
"""
import numpy as np
import sympy as sp
import pytest
from scipy.optimize import root

# Target and its complementary Legendre pair. Stable series at small radii.
def L(x):
    if x < 1e-3:
        return sum((-1)**n*x**n/n for n in range(2,12))
    return x-np.log1p(x)

def W(r):
    if r < 1e-3:
        return sum(r**n/n for n in range(2,12))
    return -r-np.log1p(-r)

def A(g):
    x=np.linalg.norm(g)
    if x < 1e-3:
        return sum((-1)**(n+1)*x**n/n for n in range(3,12))
    return .5*x*x-L(x)

def pstar(g):
    return g/(1+np.linalg.norm(g))

def energy(g,p):
    return .5*np.dot(g,g)-np.dot(g,p)+W(np.linalg.norm(p))

def gradW(p):
    return p/(1-np.linalg.norm(p))

def radial_matrix(v, transverse, longitudinal):
    r=np.linalg.norm(v)
    return transverse*np.eye(len(v)) + ((longitudinal-transverse)*np.outer(v,v)/r**2 if r else 0)

def response(g):
    x=np.linalg.norm(g)
    return radial_matrix(g,x/(1+x),x*(x+2)/(1+x)**2)

def hessW(p):
    r=np.linalg.norm(p)
    return radial_matrix(p,1/(1-r),1/(1-r)**2)

def jac_p(g):
    x=np.linalg.norm(g)
    return radial_matrix(g,1/(1+x),1/(1+x)**2)

# Inherited regular tetrahedron: T.T T=I, T T.T=I-J/4.
T=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]],float)/2
DIRECTIONS=np.array([[1,0,0],[1,1,0],[1,1,1],[2,-3,5]],float)
DIRECTIONS/=np.linalg.norm(DIRECTIONS,axis=1)[:,None]
RADII=[0,1e-6,.001,.1,1,10,100]

@pytest.mark.parametrize('x',RADII)
@pytest.mark.parametrize('n',DIRECTIONS)
def test_elimination_and_response(x,n):
    g=x*n; p=pstar(g)
    assert np.linalg.norm(p)<1
    np.testing.assert_allclose(gradW(p),g,rtol=2e-13,atol=1e-14)
    np.testing.assert_allclose(energy(g,p),A(g),atol=2e-14,rtol=1e-10)
    np.testing.assert_allclose(np.eye(3)-jac_p(g),response(g),atol=3e-15)
    np.testing.assert_allclose(np.linalg.inv(hessW(p)),jac_p(g),atol=2e-14)
    np.testing.assert_allclose(np.linalg.eigvalsh(response(g)),[x/(1+x)]*2+[x*(x+2)/(1+x)**2],atol=2e-15)
    # The four oriented face records carry exactly the same vector response.
    q=T@p; z=T@g
    assert abs(sum(q))<2e-15
    np.testing.assert_allclose(.5*z@z-z@q+W(np.linalg.norm(q)),A(g),atol=2e-13,rtol=2e-10)
    np.testing.assert_allclose(T.T@q,p,atol=2e-15)

@pytest.mark.parametrize('x',[.01,.1,1,10])
@pytest.mark.parametrize('n',DIRECTIONS)
def test_independent_numerical_settlement(x,n):
    g=x*n
    # Unconstrained auxiliary w parametrizes open unit ball by p=w/sqrt(1+w^2).
    def decode(w): return w/np.sqrt(1+w@w)
    sol=root(lambda w: gradW(decode(w))-g, np.zeros(3),tol=1e-11)
    assert np.linalg.norm(sol.fun)<2e-10
    np.testing.assert_allclose(decode(sol.x),pstar(g),atol=2e-11)
    p=decode(sol.x)
    # Verify strict minimum against independent random feasible perturbations.
    rng=np.random.default_rng(123)
    for _ in range(10):
        q=rng.normal(size=3); q*=rng.uniform(0,.999)/np.linalg.norm(q)
        assert energy(g,q)>energy(g,p)-1e-13
    d=1e-5*max(1,x)
    J=np.column_stack([( (g+d*e-pstar(g+d*e))-(g-d*e-pstar(g-d*e)) )/(2*d) for e in np.eye(3)])
    np.testing.assert_allclose(J,response(g),atol=2e-8,rtol=2e-6)

@pytest.mark.parametrize('x',[.001,.1,1,10,100])
def test_tetrahedral_rotation_and_four_face_obstruction(x):
    # All 24 face permutations induce orthogonal transformations on the zero-sum frame.
    from itertools import permutations
    g=x*DIRECTIONS[3]
    for perm in permutations(range(4)):
        R=T.T@T[list(perm)]
        np.testing.assert_allclose(R.T@R,np.eye(3),atol=1e-15)
        np.testing.assert_allclose(pstar(R@g),R@pstar(g),atol=2e-15)
    # Independent face saturation is not an isotropic radial closure.
    # Compare leading cubic invariant on two unit directions.
    axis=np.sum(abs(T@DIRECTIONS[0])**3)
    diag=np.sum(abs(T@DIRECTIONS[2])**3)
    assert abs(axis-diag)>.05
    assert not np.isclose(sum(map(W,abs(T@pstar(x*DIRECTIONS[0])))),sum(map(W,abs(T@pstar(x*DIRECTIONS[2])))),rtol=1e-9,atol=1e-15)

def test_exact_legendre_and_schur():
    x,r=sp.symbols('x r',positive=True)
    w=-r-sp.log(1-r); l=x-sp.log(1+x); p=x/(1+x)
    assert sp.simplify(sp.diff(w,r).subs(r,p)-x)==0
    assert sp.simplify(sp.expand_log(x*p-w.subs(r,p)-l,force=True))==0
    assert sp.simplify(sp.diff(x*x/2-l,x)-x*x/(1+x))==0
    assert sp.simplify(sp.diff(x*x/2-l,x,2)-x*(x+2)/(1+x)**2)==0
    assert sp.simplify((x*(x+2)/(1+x)**2)/(x/(1+x))-(2-x/(1+x)))==0
    assert sp.simplify(1/sp.diff(w,r,2).subs(r,p)-1/(1+x)**2)==0
    assert sp.series(x*x/2-l,x,0,5).removeO()==x**3/3-x**4/4
    assert sp.series(w,r,0,5).removeO()==r**2/2+r**3/3+r**4/4
    U=sp.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/2
    assert U.T*U==sp.eye(3)
    assert U*U.T==sp.eye(4)-sp.ones(4)/4

@pytest.mark.parametrize('x',[0,.1,1,10])
def test_single_or_two_auxiliary_modes_cannot_screen_three_directions(x):
    # An affine drive and Newtonian bare Hessian require rank-three cancellation.
    delta=np.eye(3)-response(x*DIRECTIONS[3]); vals=np.linalg.eigvalsh(delta)
    assert np.linalg.matrix_rank(delta)==3
    # Eckart-Young lower bound on spectral norm error for ranks 1 and 2.
    np.testing.assert_allclose(vals,[1/(1+x)**2,1/(1+x),1/(1+x)],atol=1e-15)
    for rank in [1,2]:
        rng=np.random.default_rng(321+rank); B=rng.normal(size=(3,rank)); K=B@B.T
        assert np.linalg.norm(delta-K,2)>=vals[2-rank]-1e-12

@pytest.mark.parametrize('h',[.1,.01,.001,.0001])
def test_nonanalytic_deep_field(h):
    # AQUAL is C2 but not C3 at the origin; opposite one-sided cubic coefficients.
    # Along a line E(t)=|t|^3/3+O(t^4), impossible for a real-analytic even E.
    assert abs(A(np.array([h,0,0]))/h**3-1/3)<h/4+1e-9
    assert abs(A(np.array([-h,0,0]))/(-h)**3+1/3)<h/4+1e-9

# Native fixed-z stationary sector, copied exactly from inherited verifier.
G=sp.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
v=sp.Matrix([sp.Rational(1,3),1,-sp.Rational(4,15)])
M=sp.Matrix([[-2,sp.Rational(1,2),-2],[-sp.Rational(1,2),1,-1],[-5,-1,-sp.Rational(89,10)]])
C=sp.Matrix([[0,-sp.Rational(1,2),0],[-sp.Rational(1,2),0,-1],[1,-3,1]])
f=sp.Rational(225,1232); lam=sp.Rational(11,10); chi=sp.Rational(59,308)
P=sp.eye(3)-v*v.T*G/(v.T*G*v)[0]; B=P*C*v
k=(f*B.T*G*(-(M-lam*sp.eye(3))+sp.eye(3)-P).inv()*B)[0]

def test_native_exact_obstructions():
    assert G*M==M.T*G and G*C==C.T*G
    assert M*v==lam*v and P.rank()==2
    assert k==sp.Rational(42815,290521)
    assert (f*v.T*G*C*v)[0]==chi
    assert (f*v.T*G*v)[0]==sp.Rational(1,2)
    assert (P*C*v).rank()==1
    assert 2/chi>1/k
    assert 1/chi<1/k

@pytest.mark.parametrize('t',[.1,.5,1,1.5,1.8])
def test_native_stationary_susceptibility(t):
    gg,mm,cc,vv=[np.array(q,dtype=float) for q in [G,M,C,v]]; vv=vv.ravel()
    ff=float(f); ch=float(chi); u0=t*ch; h=2*t/(ch*(1+t)); kk=float(k)
    assert h<1/kk
    def solve(j):
        def eq(q):
            z=q[:3]; freq=q[3]; u=ff*z@gg@cc@z
            gain=(1+t)*u/(u0+abs(u))
            return np.r_[(mm+(gain-1+j)*cc)@z-freq*z,ff*z@gg@z-.5]
        s=root(eq,np.r_[vv,float(lam)],tol=1e-12)
        assert np.linalg.norm(s.fun)<1e-11
        z=s.x[:3]; return ff*z@gg@cc@z
    eps=1e-8
    observed=(solve(eps)-solve(-eps))/(2*eps)
    expected=2*kk/(1-h*kk)
    np.testing.assert_allclose(observed,expected,rtol=2e-6)
    # Envelope curvature of original Hamiltonian H_j=H+2ju on maximum branch.
    assert 2*observed>0
    # Its affine-drive contribution has wrong sign for subtracting AQUAL correction.

@pytest.mark.parametrize('x',[.01,.1,1,10])
def test_naive_knot_is_not_aqual(x):
    # Knot: min_b [x(1-b)^2+b^2]/2. Correct stationary share, wrong on-shell energy.
    b=x/(1+x)
    assert abs(-x*(1-b)+b)<1e-14
    knot=.5*(x*(1-b)**2+b*b)
    assert abs(knot-.5*x/(1+x))<1e-14
    # Neither the knot energy nor its slope equals the needed correction L.
    assert not np.isclose(knot,L(x))
    assert not np.isclose(.5/(1+x)**2,x/(1+x))

@pytest.mark.parametrize('x',[.0001,.001,.01,.1,1,10])
def test_independent_face_minimization_anisotropy(x):
    # Actually settle four independent face costs subject to closure, not just evaluate
    # the radial candidate at a different cost. Use unconstrained vector coordinates
    # in a box-mapped four-face dual, with Lagrange multiplier enforcing sum(q)=0.
    from scipy.optimize import brentq
    def solve(g):
        z=T@g
        def q(lam):
            d=z-lam
            return d/(1+abs(d))
        lam=brentq(lambda l: sum(q(l)),min(z)-1,max(z)+1,xtol=1e-15)
        qq=q(lam)
        assert abs(sum(qq))<1e-13
        assert np.max(abs(qq))<1
        return .5*(g@g)-z@qq+sum(map(W,abs(qq)))
    a=solve(x*DIRECTIONS[0]); b=solve(x*DIRECTIONS[2])
    assert b>a
    if x<=.001:
        np.testing.assert_allclose(a/x**3,1/6,rtol=.003)
        np.testing.assert_allclose(b/x**3,5/(12*np.sqrt(3)),rtol=.003)
    assert a<A(x*DIRECTIONS[0]) and b<A(x*DIRECTIONS[2])

def test_exact_face_cubic_coefficients():
    U=sp.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/2
    a=U*sp.Matrix([1,0,0]); b=U*sp.ones(3,1)/sp.sqrt(3)
    assert sum(abs(c)**3 for c in a)==sp.Rational(1,2)
    assert sp.simplify(sum(abs(c)**3 for c in b)-5/(4*sp.sqrt(3)))==0
