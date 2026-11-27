"""Exact finite tests of separator reads, reduced source energy and normalization.
No microscopic gravitational law is assumed to have been derived."""
import sympy as s
n=0
def check(label, cond):
    global n
    assert cond, label
    n+=1; print('PASS',label)
def eq(a,b):
    d=a-b
    return all(s.simplify(x)==0 for x in d) if isinstance(d,s.MatrixBase) else s.simplify(d)==0
# A six-node path with grounded ends (nodes 0 and 7).
N=6; L=2*s.eye(N)
for i in range(N-1): L[i,i+1]=L[i+1,i]=-1
G=L.inv(); I=[0,1,2]; B=[3]; O=[4,5]
A=L.extract(I,I); C=L.extract(I,B); D=L.extract(B,B); F=L.extract(O,O); Q=L.extract(B,O)
check('grounded path positive definite',L.is_positive_definite)
check('no direct inner/exterior coupling',L.extract(I,O)==s.zeros(3,2))
check('strictly positive inverse',all(v>0 for v in G))
for i in range(N):
    for j in range(N):
        check(f'path Green exact {i+1},{j+1}',G[i,j]==s.Rational((min(i,j)+1)*(N-max(i,j)),N+1))
check('external source sensitivity is rank one',G.extract(I,O).rank()==1)
check('separator read rank one',C.rank()==1)
check('exact separator factorization',eq(G.extract(I,O),-A.inv()*C*G.extract(B,O)))
check('boundary transfer is nonzero',G.extract(B,O).rank()==1)
# arbitrary sources and boundary trace
f=s.Matrix(s.symbols('f1:4')); g=s.Matrix([s.Symbol('g')]); h=s.Matrix(s.symbols('h1:3'))
x=A.inv()*(f-C*g)
check('interior solve',eq(A*x+C*g,f))
S=D-C.T*A.inv()*C-Q*F.inv()*Q.T
j=C.T*A.inv()*f+Q*F.inv()*h
fb=s.Symbol('fb'); gb=S.inv()*(s.Matrix([fb])-j)
full=s.Matrix(list(f)+[fb]+list(h)); u=G*full
check('registered interface equals global solution',eq(gb,u.extract(B,[0])))
check('registered child reconstructs global interior',eq(A.inv()*(f-C*gb),u.extract(I,[0])))
check('registered exterior reconstructs global state',eq(F.inv()*(h-Q.T*gb),u.extract(O,[0])))
check('interface stiffness positive',S.is_positive_definite)
check('boundary source read rank equals interface coupling rank',(C.T*A.inv()).rank()==C.rank())
v=s.Matrix([2,-1,0]); check('invisible source difference example',C.T*A.inv()*v==s.zeros(1,1))
check('invisible source changes interior',A.inv()*v!=s.zeros(3,1))
check('invisible source changes constant energy', (v.T*A.inv()*v)[0]>0)
# Same static states, different force scales; mass-coupled source energy.
k,q,m1,m2,r,l,t=s.symbols('k q m1 m2 r l t',positive=True)
E=-(q*q/(2*k))*(full.T*G*full)[0]
check('source Hessian is negative Green',eq(s.hessian(E,list(full)),-q*q/k*G))
for i,jj in [(0,5),(1,4),(2,3)]:
    check(f'attractive cross energy coefficient {i},{jj}',s.diff(E,full[i],full[jj])==-q*q/k*G[i,jj])
Ep=-q*q*m1*m2/(4*s.pi*k*r)
check('inverse square force from continuum Green',eq(-s.diff(Ep,r),-q*q*m1*m2/(4*s.pi*k*r*r)))
check('energy scaling changes force',eq(-s.diff(l*Ep,r),-l*s.diff(Ep,r)))
check('energy scaling leaves stationary solutions',eq((l*A).inv()*(l*f-l*C*g),x))
# Scalar source through an arbitrary diagonal filter: lower rank still couples.
T=s.diag(t,0,0); source=s.Matrix([1,0,0]);
check('rank-deficient bridge has zero determinant',T.det()==0)
check('rank-deficient bridge has nonzero ordinary susceptibility',eq((source.T*T.T*T*source)[0],t*t))
check('uniform bridge source response is quadratic not 21st power',eq((s.ones(21,1).T*(t*s.eye(21)).T*(t*s.eye(21))*s.ones(21,1))[0],21*t*t))
# Local wave/step-source Taylor series: first remote coefficient at distance d.
for i in range(N):
    for j in range(N):
        d=abs(i-j)
        check(f'local walk onset {i},{j}',all((L**k0)[i,j]==0 for k0 in range(d)) and (L**d)[i,j]==(-1)**d)
# Explicit tetrahedral acoustic symbol quadratic expansion.
px,py,pz,h0,e=s.symbols('px py pz h e',real=True)
vs=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
dots=[h0*(a*px+b*py+c*pz) for a,b,c in vs]
check('tetrahedral linear term zero',eq(sum(dots),0))
check('tetrahedral quadratic symbol isotropic',eq(sum(z*z for z in dots)/2,2*h0*h0*(px*px+py*py+pz*pz)))
print(f'\n{n} exact assertions passed')
