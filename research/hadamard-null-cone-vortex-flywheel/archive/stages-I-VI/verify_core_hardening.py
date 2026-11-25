"""Exact finite algebra and conditional stability/registration tests. Reruns inherited suite."""
from contextlib import redirect_stdout
from io import StringIO
with redirect_stdout(StringIO()):
    import verify_extended_validation as v
p,c=v.p,v.c
import numpy as np
import sympy as s
from scipy.linalg import eigh
from scipy.optimize import minimize
from scipy.integrate import solve_ivp
from itertools import product, combinations
rng=np.random.default_rng(20261125)
checks=[]
def ck(msg,cond):
    assert bool(cond),msg
    checks.append(msg); print(f'PASS {len(checks):03d} {msg}',flush=True)
def near(a,b,tol=1e-9): return np.allclose(a,b,atol=tol,rtol=tol)
L,D,W=map(s.Matrix,(p.L,p.D,p.W)); I=s.eye(26); zero=s.zeros
old=len(p.checks)+len(c.checks)+len(v.checks);print('Inherited rerun:',old)
print('\n1. Hodge-Dirac')
Q=zero(26);Q[:6,6:18]=L;Q[6:18,:6]=L.T;Q[6:18,18:]=D;Q[18:,6:18]=D.T;A=Q*Q
ck('square is block Hodge Laplacian',A==s.diag(L*L.T,L.T*L+D*D.T,D.T*D))
for M,e in [(L*L.T,{0:1,4:3,6:2}),(L.T*L+D*D.T,{2:3,4:6,6:3}),(D.T*D,{0:1,2:3,4:3,6:1}),(A,{0:2,2:6,4:12,6:6})]:ck('exact Hodge spectrum '+str(e),M.eigenvals()==e)
cp=Q.charpoly();x=cp.gen
ck('Dirac characteristic polynomial',s.expand(cp.as_expr()-x**2*(x*x-2)**3*(x*x-4)**6*(x*x-6)**3)==0)
P={k:I for k in [0,2,4,6]}
for k in P:
    for j in P:
        if j!=k:P[k]=P[k]*(A-j*I)/(k-j)
    ck(f'exact spectral projector {k}',P[k]*P[k]==P[k] and P[k].T==P[k] and A*P[k]==k*P[k])
ck('orthogonal resolution of identity',sum(P.values(),zero(26))==I and all(P[a]*P[b]==zero(26) for a,b in combinations(P,2)))
ck('kernel constant vertex plus oriented fundamental face',P[0]==s.diag(s.ones(6)/6,zero(12),s.ones(8)/8))
G=s.diag(s.eye(6),-s.eye(12),s.eye(8));ck('degree grading anticommutes with Dirac',G*Q==-Q*G)
print('\n2. Torsion symmetry bridge')
cyc=[];tors=[];nz=[]; slots=[(a,b,d) for a in range(4) for b,d in combinations(range(4),2)];eps=s.Matrix([sum(s.LeviCivita(a,b,d,e) for e in range(4)) for a,b,d in slots])
for R in p.Td:
    U=s.Matrix(p.perm(p.V,R));V=s.Matrix(p.perm(p.S,R));det=int(round(np.linalg.det(R)));T=zero(12)
    for k,(a,b) in enumerate(p.E):
        i,j=int(np.argmax(np.array(U[:,a],int))),int(np.argmax(np.array(U[:,b],int)));T[p.E.index(tuple(sorted((i,j)))),k]=1 if i<j else -1
    X=s.diag(U,T,det*V);ck('Dirac equivariance with orientation twist',X*Q==Q*X)
    cyc.append(int(s.trace(c.Pcy*T)));nz.append(int(s.trace((I-P[0])*X)))
    pm=list(np.argmax(p.perm(p.S[:4],R),axis=0));TT=zero(24)
    for k,(a,b,d) in enumerate(slots):
        i,j=pm[b],pm[d];TT[slots.index((pm[a],min(i,j),max(i,j))),k]=1 if i<j else -1
    tors.append(int(s.trace(TT)));ck('torsion sign line transforms as orientation',TT*eps==det*eps)
def mult(x):return tuple((c.rows.T@np.array(x)//24).tolist())
ck('cycle representation 2T1 + A2',mult(cyc)==(0,1,0,2,0));ck('torsion regular representation',mult(tors)==(1,1,2,3,3));ck('24 nonzero Dirac modes not torsion representation',mult(nz)==(0,2,2,4,2));ck('cycle-to-torsion equivariant map space dimension seven',np.dot(mult(cyc),mult(tors))==7)
print('Irrep order A1,A2,E,T1,T2:',mult(cyc),mult(tors),mult(nz))
print('\n3. Spin holonomy of uniform transport')
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
PS=[(s.eye(2)+sum((int(a)*M/s.sqrt(3) for a,M in zip(r,pauli)),zero(2)))/2 for r in p.S]
ck('eight spin projectors Hermitian rank one',all(s.simplify(P*P-P)==zero(2) and P.H==P and s.trace(P)==1 for P in PS))
idx={tuple(r):i for i,r in enumerate(p.S)};faces=[]
for axis in range(3):
    j,k=[i for i in range(3) if i!=axis]
    for sign in [-1,1]:
        ids=[]
        for a,b in [(1,1),(-1,1),(-1,-1),(1,-1)]:
            r=[0]*3;r[axis]=sign;r[j]=a;r[k]=b;ids.append(idx[tuple(r)])
        if np.dot(np.cross(p.S[ids[1]]-p.S[ids[0]],p.S[ids[2]]-p.S[ids[1]]),p.S[ids[0]])<0:ids=ids[::-1]
        faces.append(ids)
def barg(ids):
    M=s.eye(2)
    for i in ids:M=M*PS[i]
    return s.simplify(s.expand(s.trace(M)))
for f in faces:ck('oriented cube face has spin phase pi/3',s.simplify(barg(f)-(s.Rational(2,9)+2*s.sqrt(3)*s.I/9))==0)
adj=p.cubeadj;cycles=[]
def dfs(path):
    if len(path)==8:
        if adj[path[-1],path[0]]:cycles.append(path)
        return
    for j in np.flatnonzero(adj[path[-1]]):
        if j not in path:dfs(path+[int(j)])
dfs([0]);ck('twelve directed Hamiltonian cycles',len(cycles)==12)
for path in cycles:ck('uniform spin holonomy reproduces minus sign',s.simplify(barg(path)+s.Rational(16,81))==0)
spin=[eigh(np.array(P,complex))[1][:,-1] for P in PS];U=np.zeros((8,8),complex)
for i,j in zip(*np.nonzero(adj)):
    a=np.vdot(spin[i],spin[j]);U[i,j]=a/abs(a)
ev=eigh(3*np.eye(8)-U,eigvals_only=True);ck('nonflat spin Laplacian has positive ground eigenvalue',ev[0]>1e-5)
for _ in range(8):
    T=np.diag(np.exp(1j*rng.uniform(0,2*np.pi,8)));U1=T.conj().T@U@T
    ck('spin spectrum and Wilson loops gauge invariant',near(eigh(3*np.eye(8)-U1,eigvals_only=True),ev) and all(near(np.prod([U1[i,j] for i,j in zip(f,f[1:]+f[:1])]),np.exp(1j*np.pi/3)) for f in faces))
# Exact spectrum without relying on numeric eigensolver: each chamber is a tight spinor frame.
ck('each chamber spin frame has frame operator 2 I',sum(PS[:4],zero(2))==2*s.eye(2) and sum(PS[4:],zero(2))==2*s.eye(2))
ck('antipodal spin lines orthogonal, all other cross-root overlaps squared 2/3',all(s.simplify(s.trace(PS[i]*PS[j]))==(0 if j==i+4 else s.Rational(2,3)) for i in range(4) for j in range(4,8)))
ck('connection Laplacian matches exact tight-frame spectrum',near(ev,[3-np.sqrt(6)]*2+[3]*4+[3+np.sqrt(6)]*2))
print('Connection Laplacian:',ev)
print('\n4. Multiplication and nonlinear stability')
ww=p.W;lookup={tuple(ww[:,j]):j for j in range(8)};pr=np.array([[lookup[tuple(ww[:,i]*ww[:,j])] for j in range(8)] for i in range(8)]);wt=list(map(s.Integer,[1,2,2,2,3,3,3,1]));m=lambda i,j:wt[i]*wt[j]/wt[pr[i,j]]
ck('nonlocal transported product unital commutative associative',all(m(0,i)==1 and m(i,j)==m(j,i) and m(i,j)*m(pr[i,j],k)==m(j,k)*m(i,pr[j,k]) for i,j,k in product(range(8),repeat=3)))
ck('symmetry and associativity alone do not force pointwise product',m(1,1)==4)
a=s.symbols('a:6',real=True);n=sum(x*x for x in a);re=[a[i]*a[j]+a[i+3]*a[j+3] for i,j in combinations(range(3),2)]
V4=sum((sum(int(r[i])*a[i] for i in range(3))**2+sum(int(r[i])*a[i+3] for i in range(3))**2)**2 for r in p.S)/8
ck('exact quartic Hadamard identity',s.expand(V4-n*n-4*sum(x*x for x in re))==0)
for _ in range(24):
    u,_,vv=np.linalg.svd(rng.normal(size=(3,3)));O=u@vv;zz=(O[:,0]+1j*O[:,1])/np.sqrt(2);axis=np.cross(O[:,0],O[:,1]);ck('orientation quartic identity',near(np.mean(abs(p.S@zz)**4),1+sum(axis[i]**2*axis[j]**2 for i,j in combinations(range(3),2))))
beta=s.symbols('beta',positive=True);qr=sum(a[i]**2-a[i+3]**2 for i in range(3));qi=2*sum(a[i]*a[i+3] for i in range(3));energy=4*sum(x*x for x in re)+beta*(qr*qr+qi*qi)
r=s.sqrt(2)/2;u0=s.Matrix([r,0,0,0,r,0]);phase=s.Matrix([0,-r,0,r,0,0]);tang=s.Matrix.hstack(s.Matrix([r,0,0,0,-r,0]),s.Matrix([0,r,0,r,0,0]),s.Matrix([0,0,1,0,0,0]),s.Matrix([0,0,0,0,0,1]));Hs=s.hessian(energy,a).subs(dict(zip(a,u0)))
ck('minimum gradient vanishes',s.Matrix([s.diff(energy,x) for x in a]).subs(dict(zip(a,u0)))==zero(6,1))
ck('constrained Hessian exact and positive',s.simplify(tang.T*Hs*tang)==s.diag(8*beta,8*beta+8,4,4))
ck('phase and radial Hessian modes zero',Hs*phase==zero(6,1) and Hs*u0==zero(6,1))
print('Hessian eigenvalues: 8 beta, 8 beta+8, 4, 4')
z0=np.array([1,1j,0])/np.sqrt(2);basis=np.column_stack([z0.conj(),[0,0,1.]])
for b in [.1,1.,3.]:
    def loc(t):
        z=z0+basis@(t[:2]+1j*t[2:]);return z/np.linalg.norm(z)
    def en(z):return 4*sum(np.real(z[i].conjugate()*z[j])**2 for i,j in combinations(range(3),2))+b*abs(z@z)**2
    for eps in [.0001,.001,.01]:
        H=rng.normal(size=(3,3));H=(H+H.T)/2;H*=eps/np.linalg.norm(H)
        def f(t):
            z=loc(t);return en(z)+np.vdot(z,H@z).real
        opt=minimize(f,np.zeros(4),method='BFGS',options={'gtol':1e-9});t=opt.x;h=1e-4;eye=np.eye(4);HH=np.array([[(f(t+h*(i+j))-f(t+h*(i-j))-f(t+h*(-i+j))+f(t-h*(i+j)))/(4*h*h) for j in eye] for i in eye]);ck('symmetry-breaking perturbed minimum retains chirality and positive Hessian',np.linalg.norm(opt.jac)<1e-6 and np.linalg.eigvalsh(HH).min()>0 and np.linalg.norm(p.chi(loc(t)))>.99)
    init=z0+.01*(rng.normal(size=3)+1j*rng.normal(size=3));init/=np.linalg.norm(init)
    def rhs(t,z):return -1j*(4*np.array([sum(np.real(z[i].conjugate()*z[j])*z[j] for j in range(3) if i!=j) for i in range(3)])+2*b*(z@z)*z.conj())
    sol=solve_ivp(rhs,(0,100),init,rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,100,401));ck('nonlinear evolution conserves occupation and energy',sol.success and max(abs(np.linalg.norm(sol.y,axis=0)**2-1))<1e-7 and max(abs(en(z)-en(init)) for z in sol.y.T)<1e-7);ck('near-minimum trajectory remains near circular orbit',max(np.sqrt(max(0,1-abs(np.vdot(z0,z))**2)) for z in sol.y.T)<.12)
# Embed stable axial solution into a coupled three-triplet flywheel with an isolated lowest branch.
for _ in range(8):
    _,M=p.build15(*rng.normal(size=3),*rng.uniform(.3,1.4,size=2),.2)
    e,m=eigh(M);m0=m[:,0];P0=np.outer(m0,m0);gap=e[1]-e[0];Z=np.outer(m0,z0)
    def Efull(Z):
        return np.vdot(Z,(M-e[0]*np.eye(3))@Z).real + en(m0@Z)
    ck('stable three-triplet lift has all core and chamber components and energy minimum',gap>0 and np.min(abs(m0))>1e-8 and abs(Efull(Z))<1e-9)
    d=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));d=(np.eye(3)-P0)@d;d*=.01/np.linalg.norm(d);Z1=Z+d;Z1/=np.linalg.norm(Z1)
    ck('hidden branch perturbation has energy cost bounded by spectral gap',Efull(Z1)>=gap*np.linalg.norm((np.eye(3)-P0)@Z1)**2-1e-10)
print('\n5. Conditional canonical registration')
t=s.symbols('t',real=True);u,vv,r,w=s.symbols('u v r w',real=True);aa=s.Matrix([u,vv,1-u-vv]);bb=s.Matrix([r,w,1-r-w]);ll=aa+t*(bb-aa);wed=lambda a,b:s.Matrix([a[i]*b[j]-a[j]*b[i] for i,j in combinations(range(3),2)])
ck('Whitney straight-segment integral equals wedge of endpoints',all(s.simplify(s.integrate(ll[i]*s.diff(ll[j],t)-ll[j]*s.diff(ll[i],t),(t,0,1))-(aa[i]*bb[j]-aa[j]*bb[i]))==0 for i,j in combinations(range(3),2)))
counts={}
for k,(i,j) in enumerate(p.tedges):
    a,b=c.C0[:,i],c.C0[:,j]
    if i==0:
        f=c.Lplus*(b-a);typ='central gradient minimum';ck('central flow feasible and orthogonal to cycles',L*f==b-a and D.T*f==zero(8,1))
    elif c.adjacent_support(a,b):f=c.wedge(a,b);typ='single simplex Whitney'
    else:
        shared=[r for r in p.tiles[i][1]&p.tiles[j][1] if r in c.vid];m=zero(6,1)
        for r in shared:m[c.vid[r]]=s.Rational(1,2)
        f=c.wedge(a,m)+c.wedge(m,b);typ='two simplices via midpoint'
    assert f==c.C1[:,k];counts[typ]=counts.get(typ,0)+1
ck('all 104 registration columns reproduced under route and norm premises',sum(counts.values())==104)
a0=s.Matrix([1,0,0]);b0=s.Matrix([0,1,0]);m0=s.Matrix([0,0,1]);ck('changing path adds triangular circulation at fixed endpoints',wed(a0,m0)+wed(m0,b0)-wed(a0,b0)==s.Matrix([-1,1,-1]))
u0=s.symbols('u0');mid=(1-u0)*aa+u0*bb;ck('same-path subdivision additive',all(s.simplify(wed(aa,mid)[i]+wed(mid,bb)[i]-wed(aa,bb)[i])==0 for i in range(3)))
print('Registration columns:',counts)
print(f'\n{len(checks)}/{len(checks)} new checks passed; inherited {old} rerun; total {len(checks)+old}.')
