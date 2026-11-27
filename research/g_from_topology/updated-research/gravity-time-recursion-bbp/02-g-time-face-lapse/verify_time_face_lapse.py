import sympy as s
from itertools import product
checks=[]
def ck(name, condition):
    assert bool(condition),name
    checks.append(name);print('PASS',name)
I=s.eye(3); S=s.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
ck('four-port vector sum',S.T*s.ones(4,1)==s.zeros(3,1))
ck('tetrahedral metric',S.T*S==4*I)
T=s.ones(4,1).row_join(S)
ck('Hadamard completeness',T.T*T==4*s.eye(4))
h,J,c,G,rho,m,he,alpha=s.symbols('h J c G rho m hbar alpha',positive=True)
a=s.Matrix(s.symbols('a:3')); u=s.symbols('u'); d=h*S*a
ck('affine lapse gradient recovery',S.T*d/(4*h)==a)
ck('bond sum',s.expand((d.T*d)[0]-4*h*h*(a.T*a)[0])==0)
V=8*h**3
k=2*(J/2)*(d.T*d)[0]/(2*V*(a.T*a)[0]); k=s.simplify(k)
ck('continuum stiffness',k==J/(4*h))
GG=c**4/(4*s.pi*k)
ck('gravitational coefficient',s.simplify(GG-c**4*h/(s.pi*J))==0)
ck('discrete source normalization',s.simplify(V*rho*c**2/(2*h**2*J)-4*s.pi*GG*rho/c**2)==0)
lam=he/(m*c); j=s.symbols('j',positive=True)
ck('dimensionless coupling',s.simplify((GG*m*m/(he*c)).subs(J,j*he*c/h)-(h/lam)**2/(s.pi*j))==0)
gamma=s.Rational(17,13)*alpha**21
ck('target stiffness matching',s.simplify((GG*m*m/(he*c)).subs(J,he*c/h*(h/lam)**2/(s.pi*gamma))-gamma)==0)
# Normalized determinant cancels any common scalar attenuation.
t,z=s.symbols('t z',positive=True)
b=s.symbols('b:3',real=True); B=s.diag(*[1+z*x for x in b]); B0=B.subs(z,0)
ck('common transmission factor cancels',s.cancel((t*B).det()/(t*B0).det()-B.det()/B0.det())==0)
ck('log determinant derivative is trace',s.simplify(s.diff(s.log(B.det()),z).subs(z,0)-sum(b))==0)
ck('clock compliance enters squared',s.simplify((c**4*z*z/(4*s.pi*k))/(c**4/(4*s.pi*k))-z*z)==0)
# Linearized curvature, signature (-,+,+,+), static Cartesian perturbation.
x=s.symbols('x:3'); time=s.symbols('time'); coords=(time,*x)
U=s.Function('u')(*x); W=s.Function('v')(*x)
eta=s.diag(-1,1,1,1); p=s.diag(-2*U,-2*W,-2*W,-2*W)
tr=s.trace(eta*p)
def dd(expr,i,j):return s.diff(expr,coords[i],coords[j])
R=s.Matrix(4,4,lambda i,j:s.simplify(sum(eta[k,k]*(dd(p[k,j],k,i)+dd(p[k,i],k,j)-dd(p[i,j],k,k)) for k in range(4))/2-dd(tr,i,j)/2))
lap=lambda f:sum(s.diff(f,xx,2) for xx in x)
ck('linear static R00',s.simplify(R[0,0]-lap(U))==0)
ck('linear static R0i',all(R[0,i]==0 for i in range(1,4)))
ck('linear static Rij',all(s.simplify(R[i+1,j+1]-s.diff(W-U,x[i],x[j])-(lap(W) if i==j else 0))==0 for i,j in product(range(3),repeat=2)))
Ein=R-eta*s.trace(eta*R)/2
ck('linear static G00',s.simplify(Ein[0,0]-2*lap(W))==0)
ck('zero spatial stress with equal potentials',Ein[1:4,1:4].subs(W,U).doit().applyfunc(s.simplify)==s.zeros(3))
ck('flat spatial metric generally fails vacuum equations',s.simplify(R[1,2].subs(W,0).doit())==-s.diff(U,x[0],x[1]))
# Exact isotropic Schwarzschild relation.
q,N=s.symbols('q N',positive=True)
Nq=(1-q)/(1+q)
ck('Schwarzschild spatial factor in lapse',s.simplify((2/(1+Nq))**4-(1+q)**4)==0)
ck('weak spatial factor',s.diff((2/(1+N))**4,N).subs(N,1)==-2)
print(f'{len(checks)}/{len(checks)} checks passed')
