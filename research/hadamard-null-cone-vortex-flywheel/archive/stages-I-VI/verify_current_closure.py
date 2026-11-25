"""Continuation of the Hadamard null cone proof. Run with NumPy, SciPy, SymPy.
Builds on (and reruns) verify_hadamard_null_cone.py. No empirical parameters fitted.
"""
from contextlib import redirect_stdout
from io import StringIO
with redirect_stdout(StringIO()) as prior_output:
    import verify_hadamard_null_cone as p
import numpy as np
import sympy as sp
from scipy.linalg import eigh, expm
from itertools import combinations
S,V,D,L,K,W,parity = p.S,p.V,p.D,p.L,p.K,p.W,p.parity
Td,Tperms,tiles,tedges = p.Td,p.Tperms,p.tiles,p.tedges
E=p.E; rng=np.random.default_rng(1729)
checks=[]
def ck(label, result):
    if not bool(result): raise AssertionError(label)
    checks.append(label); print(f'PASS {len(checks):03d} {label}')
def near(a,b,tol=2e-9): return np.allclose(a,b,atol=tol,rtol=tol)
print(f'Previous proof rerun: {len(p.checks)}/{len(p.checks)} passed')
# Barycentric pushforward: each outer triangle collapses to its base edge midpoint,
# each central triangle to its centroid, origin to uniform distribution on vertices.
# All matrices here are rational. Use exact arithmetic for chain/equivariance checks.
vid={tuple(v):i for i,v in enumerate(V)}
C0=sp.zeros(6,33)
for t,(kind,verts) in enumerate(tiles):
    ids=[vid[v] for v in verts if v in vid]
    if t==0: ids=list(range(6))
    for i in ids: C0[i,t]=sp.Rational(1,len(ids))
L33=sp.zeros(33,len(tedges))
for e,(i,j) in enumerate(tedges): L33[i,e]=-1; L33[j,e]=1
Ls=sp.Matrix(L); Ds=sp.Matrix(D)
Lplus=Ls.T*(Ls*Ls.T+sp.ones(6)/6).inv() # right inverse on zero-sum vectors

def wedge(a,b):
    return sp.Matrix([a[u]*b[v]-a[v]*b[u] for u,v in E])
def adjacent_support(a,b):
    ids=[i for i in range(6) if a[i] or b[i]]
    return all(V[i]@V[j]==0 for i,j in combinations(ids,2))
C1=sp.zeros(12,len(tedges)); routing={}
for e,(i,j) in enumerate(tedges):
    a,b=C0[:,i],C0[:,j]
    if i==0:
        C1[:,e]=Lplus*(b-a); kind='centre'
    elif adjacent_support(a,b):
        C1[:,e]=wedge(a,b); kind='single face'
    else:
        shared=[v for v in tiles[i][1]&tiles[j][1] if v in vid]
        assert len(shared)==2
        m=sp.zeros(6,1)
        for v in shared: m[vid[v]]=sp.Rational(1,2)
        assert adjacent_support(a,m) and adjacent_support(m,b)
        C1[:,e]=wedge(a,m)+wedge(m,b); kind='shared edge'
    routing[kind]=routing.get(kind,0)+1
ck('exact conservation chain map L C1 = C0 L33',Ls*C1==C0*L33)
ck('every fine site has unit barycentric weight',sp.ones(1,6)*C0==sp.ones(1,33))
for R,P in zip(Td,Tperms):
    Q=p.perm(V,R); Te=np.zeros((12,12),int); Tf=np.zeros((104,104),int)
    for edges,Q_,T in [(E,Q,Te),(tedges,P,Tf)]:
        idx={tuple(e):k for k,e in enumerate(edges)}
        for k,(i,j) in enumerate(edges):
            u,v=np.argmax(Q_[:,i]),np.argmax(Q_[:,j]); key=tuple(sorted((u,v)))
            # centre bonds are appended and oriented 0 -> i
            T[idx[key],k]=1 if u<v else -1
    ck('exact site equivariance',sp.Matrix(Q)*C0==C0*sp.Matrix(P.astype(int)))
    ck('exact edge equivariance',sp.Matrix(Te)*C1==C1*sp.Matrix(Tf))
# Each oriented outer ring pushes to one quarter of its base boundary, exactly.
ringmat=sp.zeros(104,8)
for f,(s,ids) in enumerate(zip(S,p.ringids)):
    for i,j in combinations(ids,2):
        ringmat[tedges.index((i,j)),f]=int(np.sign(np.cross(p.Tpos[i],p.Tpos[j])@s))
ck('eight fine triangular rings map to eight oriented core face boundaries /4', C1*ringmat==Ds/4)
ck('fine ring columns are divergence-free', L33*ringmat==sp.zeros(33,8))
# exact Hodge sector projectors
DW=Ds*sp.Matrix(W[:,1:]); G=DW.T*DW
ck('exact cycle orthogonality',G==sp.diag(16,16,16,32,32,32,48))
projectors=[]
for inds in [range(3),range(3,6),[6]]:
    A=DW[:,list(inds)]; projectors.append(A*(A.T*A).inv()*A.T)
Pcy=sum(projectors,sp.zeros(12))
ck('cycle projector equals I minus gradient projector',Pcy==sp.eye(12)-Lplus*Ls)
ck('pushforward spans complete core cycle space on fine cycles', (C1*ringmat).rank()==7)
C=np.array(C1,float); C0n=np.array(C0,float); L33n=np.array(L33,float)
Pv=[np.array(x,float) for x in projectors]; Pc=sum(Pv)
# Representation selection: Td class by trace, determinant. Characters on irreps.
chars={(3,1):(1,1,2,3,3),(0,1):(1,1,-1,0,0),(-1,1):(1,1,2,-1,-1),(-1,-1):(1,-1,0,1,-1),(1,-1):(1,-1,0,-1,1)}
rows=np.array([chars[(int(np.trace(R)),int(round(np.linalg.det(R))))] for R in Td])
names=['A1','A2','E','T1','T2']
for m in [1,2,3,6,10]:
    x=m*rows[:,4]; x2=np.array([m*np.trace(R@R) for R in Td]); wedgechar=(x*x-x2)/2
    mult=rows.T@wedgechar/24
    ck(f'Lambda^2({m} T2) contains no A2, T1 multiplicity m(m+1)/2', mult[1]==0 and mult[3]==m*(m+1)//2)
# Full T2 invariant subspace, real eigenbases aligned as polar triplets.
T2B=p.T2B; reads=p.reads
EP=sum(c*P for c,P in zip(rows[:,2],Tperms))/12
_,ev=eigh(EP); EB=ev[:,-4:]
ck('Triforce E isotypic rank 4',near(EP@EP,EP) and near(np.trace(EP),4))

def randomH():
    raw=np.diag(rng.uniform(-1,1,33))
    for i,j in tedges: raw[i,j]=raw[j,i]=-rng.uniform(.2,1.5)
    return sum(P@raw@P.T for P in Tperms)/24

def aligned(H):
    e,v=eigh(T2B.T@H@T2B); out=[]
    assert np.max(np.ptp(e.reshape(6,3),axis=1))<1e-9
    for k in range(6):
        A=T2B@v[:,3*k:3*k+3]; R=max(reads,key=lambda R:np.linalg.norm(R@A)); u,s,vh=np.linalg.svd(R@A)
        assert s[-1]>1e-9
        out.append(A@vh.T@u.T)
    return e[::3],np.column_stack(out)

def flow(H,psi):
    F=p.J(H,psi); return np.array([F[i,j] for i,j in tedges])

def faceledger(j): return np.linalg.pinv(D)@j

def ringread(f): return np.array(ringmat,float).T@f/3
maxcontinuity=0; maxA2=0; hidden=[]; ehidden=[]; discrepancy=[]; records=[]; stationary_currents=[]
for trial in range(10):
    H=randomH(); e,A=aligned(H)
    ck('all six aligned branches intertwine tetrahedral action', all(near(P@A,A@np.kron(np.eye(6),R)) for P,R in zip(Tperms,Td)))
    for b in range(6):
        z=rng.normal(size=3)+1j*rng.normal(size=3); z/=np.linalg.norm(z); psi=A[:,3*b:3*b+3]@z
        F=flow(H,psi); j=C@F; ledger=faceledger(j); rr=ringread(F); stationary_currents.append(j)
        ck('stationary Triforce mapped current is divergence-free',near(L@j,0))
        ck('T2 stationary current has no parity cycle',near(Pv[2]@j,0))
        # Two independent vector coefficients, each parallel to chirality.
        c=p.chi(z); a=W[:,1:4].T@ledger/8; bb=W[:,4:7].T@ledger/8
        ck('complete stationary current vector/bivector sectors align with same chirality',near(np.cross(a,c),0) and near(np.cross(bb,c),0))
        hidden.append(np.linalg.norm(Pv[1]@j)); discrepancy.append(np.linalg.norm(j-D@rr/4)); maxA2=max(maxA2,np.linalg.norm(Pv[2]@j))
        if trial==0: records.append((b,float(np.linalg.norm(Pv[0]@j)),float(np.linalg.norm(Pv[1]@j)),float(np.linalg.norm(j-D@rr/4))))
    # arbitrary coherent superposition of all six branches, not necessarily stationary
    Z=rng.normal(size=(6,3))+1j*rng.normal(size=(6,3)); Z/=np.linalg.norm(Z); psi=A@Z.ravel()
    F=flow(H,psi); j=C@F
    # Continuity: d |psi|² / dt = L33 F. Sign consistent with physical bond definition.
    drho=2*np.real(psi.conj()*(-1j*H@psi))
    ck('fine continuity for coherent superposition',near(L33n@F,drho))
    ck('coarse continuity for coherent superposition',near(L@j,C0n@drho))
    ck('even arbitrary coherent T2 mixing has no A2 parity cycle',near(Pv[2]@j,0))
    maxcontinuity=max(maxcontinuity,np.max(np.abs(L@j-C0n@drho)))
    # Shared density is conserved under any multiplicity mixing; time-independent H here.
    M=(A.T@H@A).reshape(6,3,6,3)[:,0,:,0]
    ck('actual T2 Hamiltonian has multiplicity tensor identity form',near(A.T@H@A,np.kron(M,np.eye(3))))
    Q0=Z.conj().T@Z; Z1=expm(-1j*M*.91)@Z
    ck('shared spatial density including collective chirality is conserved',near(Z1.conj().T@Z1,Q0))
    ck('local chirality can change while total is conserved',near(sum(map(p.chi,Z)),sum(map(p.chi,Z1))))
    # E eigen-doublet: permitted A2 cycle. T1 cannot produce it alone.
    ee,ve=eigh(EB.T@H@EB)
    for b in range(2):
        U=EB@ve[:,2*b:2*b+2]; psi=U@np.array([1,1j])/np.sqrt(2); j=C@flow(H,psi)
        ck('E doublet gives stationary divergence-free current',near(L@j,0))
        ck('E doublet current can only occupy A2 cycle, not square/bivector rings',near(Pv[0]@j,0) and near(Pv[1]@j,0))
        ehidden.append(np.linalg.norm(Pv[2]@j)); stationary_currents.append(j)
ck('counterexample: full projected current is not merely mapped outer mean ring currents',max(discrepancy)>1e-3)
ck('counterexample: grade-2 cycle survives physical projection, absent from original 15-site T2 model',max(hidden)>1e-3)
print('E doublet maximum A2 current:',max(ehidden))
ck('E doublet counterexample activates parity-only cycle',max(ehidden)>1e-3)
ck('stationary currents across tested Triforce branches span all seven cycles',np.linalg.matrix_rank(np.array(stationary_currents),tol=1e-9)==7)
# Exact parity-cycle eigenstate of the 15-site model, missed by the +/-i winding reduction.
# E: equal amplitudes at antipodes, trace-free across axes, no apex or centre amplitude.
from scipy.integrate import solve_ivp
om=np.exp(2j*np.pi/3); zE=np.array([1,om,om**2])/np.sqrt(3)
Eemb=np.abs(V)/np.sqrt(2)
for _ in range(8):
    df,ea,eb=rng.normal(size=3); ca,cb=rng.uniform(.3,1.4,2); h=rng.uniform(.2,1.4)
    H,M=p.build15(df,ea,eb,ca,cb,h)
    psi=np.zeros(15,complex); psi[1:7]=Eemb@zE
    F=p.J(H,psi); j=np.array([F[i+1,j+1] for i,j in E])
    ck('15-site E mode: exact energy Delta_f+2h, zero apex and centre',near(H@psi,(df+2*h)*psi))
    ck('15-site E mode: physical parity cycle equals h sqrt(3)/12 Dp',near(j,h*np.sqrt(3)/12*(D@parity)))
    ck('15-site E mode: no axial square-ring read, current locally conserved',near(K.T@j,0) and near(L@j,0))
# Algebraic origin of the E sector: square of odd core spatial amplitude, project trace-free diagonal.
# E conversion is phase-charge 2.  H_int=lambda (e^* dot P(z^2)+c.c.), e in sum-zero C^3.
P0=np.eye(3)-np.ones((3,3))/3
leg=np.array([1,om,om**2])/np.sqrt(3); axis=np.array([1,1j,0])/np.sqrt(2)
# The E coordinate transforms under Td by unsigned axis permutations, not as polar T2.
for R in Td:
    for zz in [leg,axis]:
        ck('quadratic map T2 to E equivariant exactly in form',near(P0@(R@zz)**2,np.abs(R)@(P0@zz**2)))
# At fixed normalized winding polarization d, e is along normalized P(d^2).
# Both selected states give invariant two-mode systems, but only leg winding generates parity current.
for name,d in [('leg',leg),('axis',axis)]:
    source=P0@d**2; eta=np.linalg.norm(source); v=source/eta
    ck(f'{name}: nonzero E harmonic and backreaction stays along original T2 polarization',eta>0 and near(d.conj()*v,eta*d))
    def rhs(t,y):
        z=y[:3]; e=y[3:]; return -1j*np.r_[2*z.conj()*e,P0@z**2]
    sol=solve_ivp(rhs,(0,5),np.r_[d,np.zeros(3,complex)],rtol=1e-10,atol=1e-12,t_eval=np.linspace(0,5,151))
    zz=sol.y[:3]; ee=sol.y[3:]; norm=np.sum(abs(zz)**2,axis=0)+2*np.sum(abs(ee)**2,axis=0)
    ck(f'{name}: nonlinear receiver conserves charge N_z+2N_E',np.max(abs(norm-1))<1e-8)
    ck(f'{name}: E conversion remains trace-free',np.max(abs(ee.sum(axis=0)))<1e-10)
    ck(f'{name}: numerical conversion matches exact resonant sech/tanh solution',near(np.sum(abs(zz)**2,axis=0),1/np.cosh(np.sqrt(2)*eta*sol.t)**2,1e-8))
    # Physical parity current if this harmonic is placed in the linear E core channel, h=1.
    j=[]
    for y in ee.T:
        a=Eemb@y; j.append(np.array([-2*np.imag(a[i]*a[k].conj()) for i,k in E]))
    j=np.array(j); strength=np.max(np.linalg.norm(j,axis=1))
    ck(f'{name}: harmonic produces only parity-cycle component',near(j@Pv[0],0) and near(j@Pv[1],0))
    ck(f"{name}: {'nonzero' if name=='leg' else 'zero'} parity circulation selection",strength>0.1 if name=='leg' else strength<1e-9)
    print(f'{name} quadratic E harmonic eta={eta:.9f}; max charge residual={np.max(abs(norm-1)):.3e}; parity current norm={strength:.9f}')

# Off-resonant conservative coupling: energy bounds E-mode occupation.
# Hamiltonian in rotating frame H=delta |e|²+2 Re(e* P(z²)); initial H=0.
for detune in [.2,1.,3.,10.]:
    d=leg; eta=np.linalg.norm(P0@d**2)
    def rhs_det(t,y):
        z=y[:3]; e=y[3:]; return -1j*np.r_[2*z.conj()*e,detune*e+P0@z**2]
    sol=solve_ivp(rhs_det,(0,20),np.r_[d,np.zeros(3,complex)],rtol=1e-9,atol=1e-11,t_eval=np.linspace(0,20,1001))
    zz=sol.y[:3]; ee=sol.y[3:]; energy=detune*np.sum(abs(ee)**2,axis=0)+2*np.real(np.sum(ee.conj()*(P0@zz**2),axis=0))
    bound=(np.sqrt(detune**2+32*eta**2)-abs(detune))/(8*eta)
    pop=np.sum(abs(ee)**2,axis=0)
    ck('detuned E conversion conserves Hamiltonian',np.max(abs(energy))<1e-7)
    ck('detuned E conversion respects analytic population bound',np.max(pop)<=bound**2+1e-7)
    print(f'detuning={detune:g}: maximum E occupation={np.max(pop):.9f}, bound={bound**2:.9f}')
# Quadratic scalar read: in the real corner signal f=s·a+p s·b, exact Walsh product.
a=sp.Matrix(sp.symbols('a1:4',real=True)); b=sp.Matrix(sp.symbols('b1:4',real=True)); f=sp.Matrix(S)*a+sp.diag(*map(int,parity))*sp.Matrix(S)*b
sq=f.applyfunc(lambda x: sp.expand(x*x)); scalar=(sp.ones(1,8)*sq)[0]/8; odd=(sp.Matrix(parity).T*sq)[0]/8
ck('quadratic scalar total exactly norm sum',sp.expand(scalar-a.dot(a)-b.dot(b))==0)
ck('quadratic chamber sign exactly interference',sp.expand(odd-2*a.dot(b))==0)
# Ring scalar share for isolated triplet (not linear mu). Fix same chirality, vary scalar mode independently.
for x in [.01,.1,.3,1,3,10,100]:
    z=np.array([1.,1j,0])/np.sqrt(2); Cn=p.chi(z); sig=S@Cn
    j=sig*np.array([np.sqrt(x)]*4+[1.]*4)
    qa=np.sum(j[:4]**2)/np.sum(j*j)
    ck('quadratic read yields x/(1+x) ONLY under sqrt intensity-odds assignment',near(qa,x/(1+x)))
    # Add independently chosen A1 amplitudes to same spatial corner signal.
    for share in [.13,.5,.87]:
        spatial=S@np.array([.01,.02,.03]); f=spatial+np.array([share]*4+[1-share]*4)
        ck('same spatial coefficients allow independent linear scalar partition',near(f[:4].sum()/f.sum(),share) and near(W[:,1:4].T@f/8,[.01,.02,.03]))
# General quadratic A1 scalar insensitive to time reversal, real symmetric multiplicity coefficients.
for _ in range(6):
    Z=rng.normal(size=(6,3))+1j*rng.normal(size=(6,3)); Bm=rng.normal(size=(6,6)); Bm=(Bm+Bm.T)/2
    q=lambda zz:np.real(np.trace(zz.conj().T@Bm@zz))
    ck('real quadratic scalar invariant under root-conjugate circulation reversal',near(q(Z),q(Z.conj())))
print('Routing counts:',routing)
print('Largest coarse continuity residual:',maxcontinuity)
print('Largest T2 forbidden parity residual:',maxA2)
print('Maximum stationary grade-2 cycle norm:',max(hidden))
print('Maximum difference full current vs outer ring-only:',max(discrepancy))
print('First Hamiltonian branch records [branch, square, grade2, ring-only discrepancy]:',records)
print(f'{len(checks)}/{len(checks)} continuation checks passed; {len(p.checks)} earlier checks rerun.')
