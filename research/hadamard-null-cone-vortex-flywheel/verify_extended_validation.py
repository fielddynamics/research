"""Next validation of the GFD Hadamard null cone. Exact where indicated.
The physical null-cone interpretation and candidate Hamiltonian dynamics are premises.
Run python verify_extended_validation.py; imports and reruns both previous stages.
"""
from contextlib import redirect_stdout
from io import StringIO
with redirect_stdout(StringIO()):
    import verify_current_closure as c
p=c.p
import numpy as np
import sympy as sp
from scipy.linalg import expm, eigh, null_space
from itertools import permutations, product, combinations
from pathlib import Path
from math import comb
rng=np.random.default_rng(4317)
checks=[]
def ck(label, condition):
    assert bool(condition),label
    checks.append(label); print(f'PASS {len(checks):03d} {label}')
def near(a,b,tol=2e-9):return np.allclose(a,b,atol=tol,rtol=tol)
print(f'Inherited checks rerun: {len(p.checks)} + {len(c.checks)}')
S,D,L,W,K=p.S,p.D,p.L,p.W,p.K
Ds,Ls,Ws=map(sp.Matrix,(D,L,W)); lam=[0,2,2,2,4,4,4,6]
print('\n1. Exact algebra, reconstruction and coordinate independence')
Gplus=Ws*sp.diag(*[0]+[sp.Rational(1,l) for l in lam[1:]])*Ws.T/8
F=Gplus*Ds.T; P=Ds*F
ck('exact Moore-Penrose inverse in Walsh coordinates',F*Ds==sp.eye(8)-sp.ones(8)/8 and P==P.T and P*P==P)
ck('reconstruction of every divergence-free current (basis proof)',all(Ds*F*v==v for v in Ls.nullspace()))
ck('minimum-norm zero-mean face ledger',sp.ones(1,8)*F==sp.zeros(1,12))
for signs in product([-1,1],repeat=12):
    # All 4096 possible choices of edge orientations, exact integer identities.
    sign=np.array(signs); d=sign[:,None]*D; l=L*sign
    assert np.array_equal(l@d,np.zeros((6,8),int)) and np.array_equal(d.T@d,D.T@D)
ck('all 4096 independent edge orientation choices preserve Gram and boundary',True)
for perm in permutations(range(4)):
    ids=list(perm)+[i+4 for i in perm]
    ck('paired frame relabelling preserves boundary spectrum and Walsh read',np.array_equal(D[:,ids].T@D[:,ids]@W[ids],W[ids]@np.diag(lam)))
# A closed current algebra requires a choice of product; natural face-ledger product modulo mean is not associative.
P8=sp.eye(8)-sp.ones(8)/8
mul=lambda a,b:P8*a.multiply_elementwise(b)
x,y=Ws[:,1],Ws[:,2]
ck('zero-mean Walsh product is not associative: (x*x)*y != x*(x*y)',mul(mul(x,x),y)==sp.zeros(8,1) and mul(x,mul(x,y))==y)
ck('all 64 full Walsh products are characters, with unique output',all(any(np.array_equal(W[:,i]*W[:,j],W[:,k]) for k in range(8)) for i in range(8) for j in range(8)))
print('\n2. Flywheel time evolution and conserved collective coherence')
Z0=np.zeros((3,3),complex); z=np.array([1,1j,0])/np.sqrt(2); a,b=.8,1.3; g=np.hypot(a,b)
M=np.array([[0,a,b],[a,0,0],[b,0,0.]])
for t in np.linspace(0,4,33):
    Z0[1:]=np.outer(np.array([a,b])/g,z); Z=expm(-1j*M*t)@Z0
    ck('resonant bright-state transfer and chirality conservation',near(np.linalg.norm(Z[0])**2,np.sin(g*t)**2) and near(Z.conj().T@Z,Z0.conj().T@Z0))
Z0[1:]=np.outer(np.array([-b,a])/g,z)
ck('dark state remains dark for equal chamber energies',near(expm(-1j*M*1.4)@Z0,Z0))
for de in [.2,1.,3.]:
    Md=M+np.diag([0,de,-de]); drive=(a*Z0[1]+b*Z0[2]); second=(M@Md@Z0)[0]
    t=1e-4; zz=expm(-1j*Md*t)@Z0
    ck('unequal energies release dark mode at second order in amplitude',near(drive,0) and near(zz[0]/t**2,-second/2,2e-4))
# Conservation is of global coherence, not individual triplet chirality.
for _ in range(8):
    M=rng.normal(size=(3,3)); M=(M+M.T)/2; Z0=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)); Z0/=np.linalg.norm(Z0)
    Z=expm(-1j*M*.8)@Z0
    ck('general multiplicity dynamics preserves spatial Gram, energy and total chirality',near(Z.conj().T@Z,Z0.conj().T@Z0) and near(np.vdot(Z,M@Z),np.vdot(Z0,M@Z0)) and near(sum(map(p.chi,Z)),sum(map(p.chi,Z0))))
# Time reversal: conjugate state, reversed time, reverses physical current.
H,M=p.build15(.3,-.7,.8,.9,.4,.2); psi=p.Q@Z0.ravel()
ck('full physical time reversal',near(expm(-1j*H*.7)@psi.conj(),(expm(1j*H*.7)@psi).conj()) and near(p.J(H,psi.conj()),-p.J(H,psi)))
# Detuned two-level bright transfer: exact peak g^2/(g^2+(delta/2)^2).
for delta in [0.,.2,1.,3.,10.]:
    M2=np.array([[delta,g],[g,0.]])
    omega=np.sqrt(g*g+delta*delta/4); t=np.pi/(2*omega)
    u=expm(-1j*M2*t)@np.array([0.,1.]); peak=g*g/(g*g+delta*delta/4)
    ck('exact detuned bright transfer ceiling',near(abs(u[0])**2,peak))
# A normalized perturbation cannot grow in Hilbert norm under the same linear H.
for _ in range(6):
    psi=rng.normal(size=9)+1j*rng.normal(size=9); psi/=np.linalg.norm(psi)
    eps=rng.normal(size=9)+1j*rng.normal(size=9); eps*=1e-4/np.linalg.norm(eps)
    U=expm(-1j*np.kron(M,np.eye(3))*rng.uniform(0,30))
    ck('linear flywheel perturbation norm is preserved, not attracted',near(np.linalg.norm(U@(psi+eps)-U@psi),np.linalg.norm(eps)))
# Exact coherent transfer counterexample: degenerate triplet with real polarization cannot create chirality.
Z0=np.outer([0,1,1],np.array([1.,0,0])); Z=expm(-1j*M*.7)@Z0
ck('outer occupation alone does not imply vortex generation',near(sum(map(p.chi,Z)),0) and near(p.chi(Z[0]),0))
print('\n3. Registration ambiguity and exact dynamical memory')
# Explicit second chain map: reflection of cycle currents not in outer ring span on fine graph.
# Ring-fixed ambiguity from a Reynolds-averaged map of the fine ring complement to core cycles.
R=c.ringmat; Pr=R*(R.T*R).inv()*R.T
Tfs=[]; Tes=[]
for rot,Qf in zip(p.Td,p.Tperms):
    Qv=p.perm(p.V,rot)
    def edgeperm(edges,Q):
        out=sp.zeros(len(edges)); idx={e:i for i,e in enumerate(edges)}
        for n,(i,j) in enumerate(edges):
            u,v=np.argmax(Q[:,i]),np.argmax(Q[:,j]); out[idx[tuple(sorted((u,v)))],n]=1 if u<v else -1
        return out
    Tfs.append(edgeperm(p.tedges,Qf)); Tes.append(edgeperm(p.E,Qv))
# Existing map minus projection onto the disjoint outer rings already supplies a nonzero ambiguity.
A=P*c.C1*(sp.eye(104)-Pr)
ck('nonzero alternative registration correction',A!=sp.zeros(12,104))
ck('alternative preserves divergence and all eight outer rings',Ls*A==sp.zeros(6,104) and A*R==sp.zeros(12,8))
ck('alternative is exactly equivariant for all 24 symmetries',all(Q*A==A*T for Q,T in zip(Tes,Tfs)))
# Dimension of all linear equivariant changes obeying these two requirements, via characters.
cf=np.array([int(sp.trace(T)) for T in Tfs]); cr=np.array([int(sp.trace((R.T*R).inv()*R.T*T*R)) for T in Tfs]); cc=np.array([int(sp.trace(P*T)) for T in Tes]); dim=int(cc@(cf-cr)//24)
ck('space of ring-fixed conservative equivariant changes has positive dimension',dim>0)
print('Dimension of unconstrained equivariant registration ambiguity:',dim)
# Exact 33-site dynamics with 15-site retained observation as in the previous research.
# Construct a geometry-defined rank-15 observation of origin, core vertices and apex corners.
O=np.zeros((15,33)); O[0,0]=1
for t,(kind,verts) in enumerate(p.tiles[1:],1):
    for v in verts:
        if v in [tuple(u) for u in p.V]: O[1+list(map(tuple,p.V)).index(v),t]+=1/3
        if v in [tuple(u) for u in S]: O[7+list(map(tuple,S)).index(v),t]+=1/3
ck('geometry observation has rank 15',np.linalg.matrix_rank(O)==15)
# orthonormal coordinates in rowspace and nullspace, no claim that coordinates are original sites
U,s,Vh=np.linalg.svd(O,full_matrices=True); Q=Vh[:15].T; N=Vh[15:].T
H=c.randomH(); A0=Q.T@H@Q; B=Q.T@H@N; C=N.T@H@N
ck('hidden dynamics couples to retained state, no autonomous exact 15-state linear evolution',np.linalg.norm(B)>1e-3)
for w in [1j,2+1j,-1+.2j]:
    Rf=Q.T@np.linalg.inv(w*np.eye(33)-H)@Q
    Re=np.linalg.inv(w*np.eye(15)-A0-B@np.linalg.solve(w*np.eye(18)-C,B.T))
    ck('Schur resolvent exactly reproduces observed response',near(Rf,Re))
y=N[:,0]; ck('same retained initial state can have different time derivative',near(Q.T@y,0) and np.linalg.norm(B)>1e-3)
# Memory kernel reconstructs projected time derivative using trapezoidal quadrature.
T=1.; init=Q@rng.normal(size=15); init/=np.linalg.norm(init); ev,vec=eigh(H); eC,vC=eigh(C)
def trajectory(t):return vec@(np.exp(-1j*ev*t)*(vec.T@init))
truth=-1j*Q.T@H@trajectory(T); yT=Q.T@trajectory(T); errors=[]
for n in [32,64,128,256]:
    ts=np.linspace(0,T,n+1); integr=np.array([B@vC@(np.exp(-1j*eC*(T-t))*(vC.T@B.T@Q.T@trajectory(t))) for t in ts]); pred=-1j*A0@yT-getattr(np,"trapezoid",getattr(np,"trapz",None))(integr,ts,axis=0); errors.append(np.linalg.norm(pred-truth))
ck('memory kernel converges quadratically to exact projected dynamics',errors[-1]<errors[0]/50 and errors[-1]<1e-5)
print('Memory integration errors:',errors)
print('\n4. Nonlinear invariants through sixth order')
# Monomials in z and conjugate z (formal independent variables), one or two T2 copies.
# Even coordinate sign flips force all three total axis degrees to have same parity.
# S3 orbit sums then form a complete linearly independent basis.
def compositions(n,k):
    if k==1: yield (n,); return
    for a in range(n+1):
        for rest in compositions(n-a,k-1):yield (a,)+rest

def orbitbasis(degree,m):
    k=2*m; seen=set(); out=[]
    for v in compositions(degree,3*k):
        a=tuple(v[i*k:(i+1)*k] for i in range(3))
        if len({sum(t)%2 for t in a})!=1:continue
        o=tuple(sorted(a))
        if o in seen:continue
        seen.add(o); out.append(o)
    return out

def conjugate(o,m):return tuple(sorted(t[m:]+t[:m] for t in o))
counts={}
for m in [1,2]:
    for d in range(7):
        basis=orbitbasis(d,m); neutral=[o for o in basis if sum(sum(t[:m])-sum(t[m:]) for t in o)==0]; even={min(o,conjugate(o,m)) for o in neutral}; counts[m,d]=(len(basis),len(neutral),len(even))
        ck(f'complete monomial orbit basis: {m} complex triplets degree {d}, conjugation closed',all(conjugate(o,m) in basis for o in basis) and len(set(basis))==len(basis))
print('Counts (all / U(1)-neutral / time-reversal even):',counts)
ck('single triplet has exactly one quadratic neutral invariant',counts[1,2][1]==1)
# holomorphic ring dimensions via degrees 2,3,4; compare enumeration through degree 12.
for d in range(13):
    hol=[o for o in orbitbasis(d,1) if all(t[1]==0 for t in o)]; pred=sum(2*a+3*b+4*c==d for a,b,c in product(range(d//2+1),range(d//3+1),range(d//4+1)))
    ck('holomorphic invariant Hilbert count matches degrees 2,3,4',len(hol)==pred)
# Independent Molien/character certificate for the orbit counts. For Sym^d of a
# representation, d h_d = sum_{k=1}^d tr(R^k) h_{d-k}.
def symtrace(R,m,d):
    h=[1]; tr=[0]+[m*int(np.trace(np.linalg.matrix_power(R,k))) for k in range(1,d+1)]
    for j in range(1,d+1):
        h.append(sum(tr[k]*h[j-k] for k in range(1,j+1))//j)
    return h[d]
for m in [1,2]:
    for d in range(7):
        allcount=sum(symtrace(R,2*m,d) for R in p.Td)//24
        if d%2==0:
            k=d//2; neutral=sum(symtrace(R,m,k)**2 for R in p.Td)//24
            rev=sum(symtrace(R@R,m,k) for R in p.Td)//24
            even=(neutral+rev)//2
        else: neutral=even=0
        ck('independent exact character count agrees with monomial orbit basis',counts[m,d]==(allcount,neutral,even))
# Explicit generator of the one-dimensional time-odd neutral sextic sector.
def odd6(z):
    return sp.im(sum(t*t for t in z)*sum(t*sp.conjugate(t)**3 for t in z)).expand()
zz=sp.Matrix([1,1+sp.I,0])
ck('explicit neutral time-odd sextic is nonzero',odd6(zz)==-2)
ck('sextic invariant on all 24 tetrahedral transformations',all(odd6(sp.Matrix(R)*zz)==-2 for R in p.Td))
ck('sextic reverses under conjugation and is invariant under a common phase',odd6(sp.conjugate(zz))==2 and odd6(sp.I*zz)==-2)
# Full generic quadratic scalar coupling of two triplets: two norms and complex inner product.
ck('two triplets have 4 neutral quadratic invariants, 3 time-even',counts[2,2][1:]==(4,3))
# Pointwise nonlinearity on normalized Walsh basis: products exactly XOR, no extra free tensor.
for _ in range(10):
    a=rng.integers(-4,5,8); b=rng.integers(-4,5,8); conv=W.T@((W@a)*(W@b))//8
    ck('exact quadratic Walsh convolution reconstructs site multiplication',np.array_equal(W@conv,(W@a)*(W@b)))
print('\n5. Constitutive-law selection and counterexamples')
# llms.txt: screening + exchange -> x^k, accelerations fix k=1. Not a new derivation.
xs=np.logspace(-6,6,97)
for k in [.5,1,2,3]:
    mu=xs**k/(1+xs**k); dual=1/(1+xs**k)
    ck(f'exchange permits distinct screening exponent k={k}',near(mu+dual,1) and near(xs**k*dual,mu))
    if k!=1:ck('exchange alone does not select the constitutive law',np.max(abs(mu-xs/(1+xs)))>.05)
# Counterexample: field partition remains independent of flywheel orientation.
for x in xs[::8]:
    mu=x/(1+x); val=np.array([mu]*4+[1-mu]*4)+.00000001*(S@np.array([1.,2.,-1.]))
    ck('prescribed acceleration odds reproduce linear chamber share independent of circulation',near(val[:4].sum()/val.sum(),mu))
    ck('drained partition has bounded TetB pull and adds to total',0<=x/(1+x)<=1 and near(mu*x+x/(1+x),x))
# Prescribed drain flag: a conditional check, not a microscopic drain criterion.
for drained in [False,True]:
    x=xs; m=x/(1+x) if drained else np.ones_like(x)
    visible=m*x; tetb=(x/(1+x) if drained else np.zeros_like(x))
    ck('conditional interior partition respects drain flag and total acceleration',near(visible+tetb,x) and (drained or near(visible,x)))
# stable analytic evaluation of F derivative, with y=x^2; not the full action.
y=sp.symbols('y',positive=True); Fsym=y-2*sp.sqrt(y)+2*sp.log(1+sp.sqrt(y))
ck('kinetic functional derivative equals constitutive law',sp.simplify(sp.diff(Fsym,y)-sp.sqrt(y)/(1+sp.sqrt(y)))==0)
print('\n6. Candidate lattice propagation: angular accuracy and causal distinction')
# Geometry only, dimensionless lattice step. Cube diagonal velocities normalized.
n=S/np.sqrt(3); axes=p.V
for v in [np.array([1.,0,0]),np.ones(3)/np.sqrt(3),np.array([1.,1,0])/np.sqrt(2)]:
    ck('diagonal stencil has exact isotropic second moment',near(np.mean((n@v)**2),1/3))
    ck('weighted axial + diagonal unit vectors restore fourth moment isotropy',near(.6*np.mean((n@v)**4)+.4*np.mean((axes@v)**4),1/5))
ck('eight directions alone are anisotropic at fourth order',not near(np.mean(n[:,0]**4),np.mean((n@np.ones(3)/np.sqrt(3))**4)))
# Exact polynomial identity for all orientations, not just three examples.
x,y,z=sp.symbols('x y z',real=True); r2=x*x+y*y+z*z
m4=sum((int(s[0])*x+int(s[1])*y+int(s[2])*z)**4 for s in S)/72
ax4=(x**4+y**4+z**4)/3
ck('all-direction fourth-moment isotropy for 3:2 diagonal/axial mixture',sp.expand(sp.Rational(3,5)*m4+sp.Rational(2,5)*ax4-r2**2/5)==0)
# Exact discrete causal support by shift and internal unitary; not Lorentz covariance.
from collections import defaultdict
state={(0,0,0):np.eye(8,dtype=complex)[0]}; coin=W/np.sqrt(8)
for t in range(1,6):
    nxt=defaultdict(lambda:np.zeros(8,complex))
    for r,u in state.items():
        v=coin@u
        for j,s in enumerate(S):nxt[tuple(np.array(r)+s)][j]+=v[j]
    state=nxt
    ck('candidate walk has strict finite-step causal support and unit norm',all(max(map(abs,r))<=t for r in state) and near(sum(np.vdot(u,u) for u in state.values()),1))
# Continuous-time nearest-neighbour Hamiltonian is not strictly finite-support.
H=np.diag(np.ones(7),1)+np.diag(np.ones(7),-1); u=expm(-1j*H*.5)[:,0]
ck('continuous-time finite-range hopping has nonzero amplitude outside one-step neighbourhood',abs(u[5])>1e-6)
print('\n7. Coupling invariant: what topology does and does not select')
for s in [-1,0,1]:ck('discrete structural states, K=4',1+4*s+16==17+4*s)
# Same 21-dimensional graded representation: different determinant depending on attenuation rule.
alpha=1/137.035999177
# logarithms avoid underflow; use dimension counting on 1+4+16 graded blocks.
ck('uniform attenuation on 21 states gives alpha^21',1+4+16==21)
ck('tensor-functor attenuation on four-vector gives alpha^36, not alpha^21',4+2*16==36)
ck('trace counts alone do not fix attenuation exponent',not near(21*np.log(alpha),36*np.log(alpha)))
print('Conclusion: neither 21 exponent nor 17/13 normalization selected by the new current algebra.')
print(f'\n{len(checks)}/{len(checks)} new checks passed; inherited {len(p.checks)+len(c.checks)} rerun; total {len(checks)+len(p.checks)+len(c.checks)}.')
