"""Hadamard null-cone flywheel: exact finite identities and numerical model tests.
Run: python verify_hadamard_null_cone.py (numpy, scipy, sympy).
Geometry and Hamiltonians reconstructed from the GFD Hadamard/Walsh/vortex proofs.
Physical identification of the null cone, couplings, and flow selection are premises.
"""
from itertools import product, permutations, combinations
import numpy as np
import sympy as sp
from scipy.linalg import eigh, expm
from pathlib import Path

checks=[]
def ck(label, result):
    if not bool(result): raise AssertionError(label)
    checks.append(label); print(f'PASS {len(checks):03d} {label}')
def near(a,b,atol=2e-10): return np.allclose(a,b,atol=atol,rtol=1e-9)
A=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)],int)
S=np.vstack((A,-A)); parity=np.prod(S,axis=1); V=np.vstack((np.eye(3,dtype=int),-np.eye(3,dtype=int)))
E=[(i,j) for i,j in combinations(range(6),2) if V[i]@V[j]==0]
W=np.array([np.prod(S[:,list(k)],axis=1) if k else np.ones(8,int) for k in [(),(0,),(1,),(2,),(1,2),(0,2),(0,1),(0,1,2)]],int).T
D=np.zeros((12,8),int); B=np.array([[int(v@s==1) for s in S] for v in V]); L=np.zeros((6,12),int)
for e,(i,j) in enumerate(E):
    L[i,e]=-1; L[j,e]=1
    for f,s in enumerate(S):
        if B[i,f] and B[j,f]: D[e,f]=np.cross(V[i],V[j])@s
cubeadj=(S@S.T==1).astype(int)
H4=np.vstack((np.ones(4,int),A.T)); order=[0,4,5,6,7,1,2,3]
ck('Hadamard orthogonality',np.array_equal(H4@H4.T,4*np.eye(4)))
ck('parity-times-frame factorization',np.array_equal(W[:,order].T,np.kron([[1,1],[1,-1]],H4)))
ck('null Gram = minus 2/3 Hamming distance (time-negative convention)',np.array_equal(S@S.T-3*np.ones((8,8),int),-2*((3-S@S.T)//2)))
ck('each stellation base is exactly one core face',np.all(B.sum(0)==3) and np.all(B.sum(1)==4))
ck('all eight lateral pyramids have the same volume 1/3',all(abs(round(np.linalg.det(np.array([V[i]-s for i in np.flatnonzero(B[:,f])]))))==2 for f,s in enumerate(S)))
ck('three edges per oriented face, two faces per edge',np.all(np.sum(abs(D),axis=0)==3) and np.all(np.sum(abs(D),axis=1)==2))
ck('boundary of boundary vanishes exactly',np.array_equal(L@D,np.zeros((6,8),int)))
ck('closed surface: all oriented faces cancel',np.array_equal(D@np.ones(8,int),np.zeros(12,int)))
ck('oriented face Gram is the Hadamard cube Laplacian',np.array_equal(D.T@D,3*np.eye(8,dtype=int)-cubeadj))
ck('exact Walsh diagonalization of face Gram',np.array_equal(D.T@D@W,W@np.diag([0,2,2,2,4,4,4,6])))
ck('unsigned vertex incidence sees exactly scalar/vector Walsh grades',np.array_equal(B.T@B@W,W@np.diag([12,4,4,4,0,0,0,0])))
ck('face-to-edge rank seven',sp.Matrix(D).rank()==7)
ck('vertex-edge rank five',sp.Matrix(L).rank()==5)
ck('face map spans all divergence-free core currents',sp.Matrix(D).rank()==12-sp.Matrix(L).rank())
K=np.array([np.cross(V[i],V[j]) for i,j in E]);
ck('grade-one face circulation is exactly twice the square-ring basis',np.array_equal(D@S,2*K))
ck('three square rings, four edges each',np.array_equal(K.T@K,4*np.eye(3,dtype=int)))
for i in range(3):
    ck(f'hemisphere {i}: four face loops give one square ring',np.array_equal(D@(S[:,i]>0).astype(int),K[:,i]))
ck('all three Walsh circulation sectors are orthogonal',np.array_equal((D@W).T@(D@W),8*np.diag([0,2,2,2,4,4,4,6])))
# Full tetrahedral group: oriented face coefficients are pseudoscalars.
Td=[np.diag(sig)@np.eye(3,dtype=int)[list(p)] for p in permutations(range(3)) for sig in product([1,-1],repeat=3) if np.prod(sig)==1]
def perm(points,R):
    ids={tuple(v):i for i,v in enumerate(points)}
    P=np.zeros((len(points),len(points)),int)
    for i,v in enumerate(points): P[ids[tuple(R@v)],i]=1
    return P
for R in Td:
    P=perm(S,R); Q=perm(V,R); T=np.zeros((12,12),int)
    for k,(i,j) in enumerate(E):
        u=np.argmax(Q[:,i]); v=np.argmax(Q[:,j]); T[E.index(tuple(sorted((u,v)))),k]=1 if u<v else -1
    ck('oriented boundary equivariance (determinant twist)',np.array_equal(T@D,round(np.linalg.det(R))*D@P))
# Exact symbolic identity for circular core current.
x,y,z,u,v,w,k=sp.symbols('x y z u v w k',real=True)
zz=sp.Matrix([x+sp.I*u,y+sp.I*v,z+sp.I*w]); C=-sp.I*sp.conjugate(zz).cross(zz)
for i,j in E:
    a=sp.Matrix(V[i]); b=sp.Matrix(V[j]); actual=k*sp.im(sp.conjugate(b.dot(zz))*a.dot(zz))
    ck('symbolic core current equals chirality cross product',sp.simplify(actual+k*a.cross(b).dot(C)/2)==0)
# 15-site graph with centre, octahedron vertices, eight stellations. No direct corner bonds.
U=V/np.sqrt(2); UA=A/2; UB=-A/2
ck('chamber A projects to sqrt(2) core triplet',near(U.T@B[:,:4]@UA,np.sqrt(2)*np.eye(3)))
ck('chamber B projects to sqrt(2) core triplet',near(U.T@B[:,4:]@UB,np.sqrt(2)*np.eye(3)))
Q=np.zeros((15,9)); Q[1:7,:3]=U; Q[7:11,3:6]=UA; Q[11:15,6:]=UB
ck('collective embedding is isometric',near(Q.T@Q,np.eye(9)))
def build15(df,ea,eb,ca,cb,h):
    H=np.diag([.13]+[df]*6+[ea]*4+[eb]*4); H[0,1:7]=H[1:7,0]=-.9; H[0,7:11]=H[7:11,0]=-.8; H[0,11:]=H[11:,0]=-.5
    for i,j in E: H[i+1,j+1]=H[j+1,i+1]=-h
    for f in range(8):
        for i in np.flatnonzero(B[:,f]): H[i+1,f+7]=H[f+7,i+1]=-(ca if f<4 else cb)
    M=np.array([[df,-np.sqrt(2)*ca,-np.sqrt(2)*cb],[-np.sqrt(2)*ca,ea,0],[-np.sqrt(2)*cb,0,eb]])
    return H,M

def J(H,psi): return 2*np.imag(psi[:,None]*H.T*psi.conj()[None,:])
def chi(z): return np.real(-1j*np.cross(z.conj(),z))
rng=np.random.default_rng(20261124)
# Physically signed currents after eliminating a corner: J_(u->s)=sum_v J^s_(u->v).
worst=0.; samples=[]
for trial in range(12):
    df,ea,eb=rng.normal(size=3); ca,cb=rng.uniform(.3,1.4,size=2); h=rng.uniform(-.5,.5)
    H,M=build15(df,ea,eb,ca,cb,h)
    ck('invariant collective Hamiltonian equals M tensor I3',near(H@Q,Q@np.kron(M,np.eye(3))))
    es,vs=eigh(M)
    for branch,(energy,m) in enumerate(zip(es,vs.T)):
        z=rng.normal(size=3)+1j*rng.normal(size=3); z/=np.linalg.norm(z)
        psi=Q@np.kron(m,z); core=psi[1:7]; zz=m[0]*z; Cn=chi(zz); currents=J(H,psi)
        ck('collective triplet eigenstate and exact dark centre',near(H@psi,energy*psi) and abs(psi[0])<1e-14)
        ck('stationary physical current is divergence-free',near(currents.sum(axis=1),0))
        # Schur elimination of the apex amplitudes. Treat the T2 centre as identically zero.
        coeff=np.array([ca**2/(energy-ea)]*4+[cb**2/(energy-eb)]*4)
        med=np.array([2*np.imag(core[:,None]*core.conj()[None,:])*coeff[f]*np.outer(B[:,f],B[:,f]) for f in range(8)])
        ck('each eliminated apex preserves every incident bond current',near(med.sum(axis=2).T,currents[1:7,7:]))
        reduced=currents[1:7,1:7]+med.sum(axis=0)
        ck('reduced core currents obey local continuity',near(reduced.sum(axis=1),0))
        keff=-h+coeff[0]+coeff[4]
        values=np.array([reduced[i,j] for i,j in E]); expected=-keff/4*(D@(S@Cn))
        ck('actual reduced core current equals oriented eight-face circulation',near(values,expected))
        ck('core currents reverse under conjugation',near(J(H,psi.conj()),-currents))
        ck('apex-mediated and direct coefficients recover formal secular current',near(2*keff,energy-df-2*h))
        # canonical face coefficients via zero-mean inverse; no claim they equal individual physical ring currents.
        recovered=np.linalg.pinv(D)@values
        ck('unique mean-zero face ledger recovered',near(recovered,-keff/4*(S@Cn)))
        worst=max(worst,np.max(abs(values-expected)))
        if trial==0: samples.append((energy,keff,m.tolist()))
# Exact resonant transfer; dark and bright are collective outer coordinates.
H,M=build15(0,0,0,1,.7,.23); coupling=np.linalg.norm(M[0,1:]); bright=np.r_[0,M[0,1:]/coupling]; dark=np.r_[0,-M[0,2]/coupling,M[0,1]/coupling];
ck('bright flywheel reaches full core occupation at resonance',near(abs((expm(-1j*M*np.pi/(2*coupling))@bright)[0])**2,1))
ck('dark flywheel cannot excite core in symmetric resonant model',near((expm(-1j*M)@dark)[0],0))
ck('unitary evolution conserves total occupation',near(np.linalg.norm(expm(-1j*M*.73)@bright),1))
# A finite core can carry a dark circulation sector beyond square rings.
ck('grade-two loops are nonzero and invisible to square-ring projection',np.linalg.norm(D@W[:,4:7])>0 and np.array_equal(K.T@D@W[:,4:7],np.zeros((3,3),int)))
ck('parity loop also invisible to square-ring projection',np.linalg.norm(D@W[:,7])>0 and np.array_equal(K.T@D@W[:,7],np.zeros(3,int)))
# Nonlinear scalar chamber accounting (quadratic, not the linear mu read).
for _ in range(5):
    a,b=rng.normal(size=(2,3)); j=S@a+parity*(S@b); sq=j*j
    ck('quadratic current scalar reads total vector and bivector intensity',near(np.mean(sq),a@a+b@b))
    ck('quadratic chamber sign reads vector-bivector interference',near(np.mean(sq*parity),2*a@b))
# Triforce graph: verify the eight outer rings are the lateral faces of the eight stellations.
tiles=[('O',frozenset([(0,0,0)]))]
for tag,T in [('A',A),('B',-A)]:
    for f in combinations(range(4),3):
        tri=T[list(f)]; mid=lambda a,b: tuple((a+b)//2)
        tiles.append(('C'+tag,frozenset(mid(tri[i],tri[j]) for i,j in combinations(range(3),2))))
        for i in range(3): tiles.append(('E'+tag,frozenset([tuple(tri[i])]+[mid(tri[i],tri[j]) for j in range(3) if j!=i])))
Tpos=np.array([np.mean(list(v),axis=0) for _,v in tiles]); ix={v:i for i,v in enumerate(tiles)}
Tperms=[]
for R in Td:
    p=[ix[(k,frozenset(tuple(R@np.array(a)) for a in vs))] for k,vs in tiles]
    Tperms.append(np.eye(33)[:,p])
outer=[i for i,(k,_) in enumerate(tiles) if k[0]=='E']; inner=[i for i,(k,_) in enumerate(tiles) if k[0]=='C']
ringids=[]
for f,s in enumerate(S):
    ids=[i for i in outer if tuple(s) in tiles[i][1]]; ringids.append(ids)
    base=[tuple(V[i]) for i in np.flatnonzero(B[:,f])]
    desired={frozenset([tuple(s),u,v]) for u,v in combinations(base,2)}
    ck('Triforce ring tiles are exactly the three lateral faces of the stellation',len(ids)==3 and {tiles[i][1] for i in ids}==desired)
    ck('opposite-chamber central tile is exactly the triangular base',any(tiles[i][1]==frozenset(base) and tiles[i][0][1]!=('A' if f<4 else 'B') for i in inner))
# Model follows the formal proof: edge-sharing tiles and centre-to-central tile bonds.
tedges=[(i,j) for i,j in combinations(range(1,33),2) if len(tiles[i][1]&tiles[j][1])==2]+[(0,i) for i in inner]
ck('Triforce has 33 sites and 104 bonds',len(tiles)==33 and len(tedges)==104)
T2P=sum(np.trace(R)*P for R,P in zip(Td,Tperms))/8
ck('T2 character projector has rank 18',near(T2P@T2P,T2P) and near(np.trace(T2P),18))
_,PV=eigh(T2P); T2B=PV[:,-18:]
# Symmetrize arbitrary site energies and edge hoppings to get generic Td-invariant H.
raw=np.diag(rng.uniform(-1,1,33))
for i,j in tedges: raw[i,j]=raw[j,i]=-rng.uniform(.2,1.5)
TH=sum(P@raw@P.T for P in Tperms)/24
te,tv=eigh(T2B.T@TH@T2B)
ck('six distinct T2 eigenbranches, each triply degenerate',np.max(np.ptp(te.reshape(6,3),axis=1))<1e-10 and np.min(np.diff(te[::3]))>1e-6)
# Read polar vectors from the three distinct site-orbit types, separately by chamber.
reads=[]
for tag in ['CA','CB','EA','EB']:
    read=Tpos.T.copy(); read[:,[i for i,(k,_) in enumerate(tiles) if k!=tag]]=0; reads.append(read)
# On each real triplet the ring-current quadratic form is purely imaginary antisymmetric.
# Identify its coefficient with one reference circular polarization, then test general states.
def ringcurr(psi):
    flow=J(TH,psi); out=[]
    for s,ids in zip(S,ringids):
        out.append(sum(flow[i,j]*np.sign(np.cross(Tpos[i],Tpos[j])@s) for i,j in combinations(ids,2))/3)
    return np.array(out)
ks=[]; maxtri=0.
for k in range(6):
    branch=T2B@tv[:,3*k:3*k+3]
    read=max(reads,key=lambda R:np.linalg.norm(R@branch))
    l,sv,rh=np.linalg.svd(read@branch); ck('triplet admits nonzero isotropic polar read',sv[-1]>1e-8 and np.ptp(sv)<1e-9)
    branch=branch@rh.T@l.T
    ck('branch transforms as the polar spatial representation',all(near(P@branch,branch@R) for P,R in zip(Tperms,Td)))
    z=np.array([1,1j,0])/np.sqrt(2); sig=S@chi(z); j=ringcurr(branch@z)
    ca=np.dot(j[:4],sig[:4])/np.dot(sig[:4],sig[:4]); cb=np.dot(j[4:],sig[4:])/np.dot(sig[4:],sig[4:]); ks.append([float(ca),float(cb)])
    for _ in range(4):
        z=rng.normal(size=3)+1j*rng.normal(size=3); z/=np.linalg.norm(z); j=ringcurr(branch@z); sig=S@chi(z)
        target=sig*np.array([ca]*4+[cb]*4)
        ck('all eight physical Triforce ring currents share one chirality vector',near(j,target))
        ck('outward signed circulation sums separately to zero in each chamber',near([j[:4].sum(),j[4:].sum()],0))
        cplus=(ca+cb)/2; cminus=(ca-cb)/2
        ck('oriented face aggregation separates common and chamber-difference Walsh cycles',near(D@j,cplus*(D@sig)+cminus*(D@(parity*sig))))
        ck('square-ring projection discards chamber-difference cycles',near(K.T@D@j/4,2*cplus*chi(z)))
        maxtri=max(maxtri,np.max(abs(j-target)))
print(f'Largest Triforce ring-current identity residual: {maxtri:.3e}')
print('Triforce branch coefficients (arbitrary model units):',ks)
print(f'\nLargest core current identity residual: {worst:.3e}')
print('Example (energy, effective edge hopping, core/A/B mode weights):',samples)
print(f'{len(checks)}/{len(checks)} checks passed (exact integer/symbolic identities and finite numerical examples).')
