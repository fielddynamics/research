"""Stage IX: exact matched Triforce interface and dynamical directional Field Origins.
Dimensionless candidate; no fitted gravitational constants.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)])
S=np.vstack((A,-A)); tiles=[('O',frozenset([(0,0,0)]))]
for tag,T in [('A',A),('B',-A)]:
    for f in combinations(range(4),3):
        tri=T[list(f)]; mid=lambda a,b:tuple((a+b)//2)
        tiles.append(('C'+tag,frozenset(mid(tri[i],tri[j]) for i,j in combinations(range(3),2))))
        for i in range(3): tiles.append(('E'+tag,frozenset([tuple(tri[i])]+[mid(tri[i],tri[j]) for j in range(3) if j!=i])))
pos=np.array([np.mean(list(v),axis=0) for _,v in tiles]); lookup={v:i for i,v in enumerate(tiles)}
outer=[i for i,(k,_) in enumerate(tiles) if k[0]=='E']; inner=[i for i,(k,_) in enumerate(tiles) if k[0]=='C']
edges=[(i,j) for i,j in combinations(range(1,33),2) if len(tiles[i][1]&tiles[j][1])==2]+[(0,i) for i in inner]
rings=[]; idx={}; base=[]
for f,s in enumerate(S):
    ids=[i for i in outer if tuple(s) in tiles[i][1]]
    if np.cross(pos[ids[0]],pos[ids[1]])@s<0: ids[1],ids[2]=ids[2],ids[1]
    rings.append(ids)
    base.append(next(i for i in inner if np.allclose(pos[i],s/3)))
    for i in ids:
        t=next(g for g in range(4*(f//4),4*(f//4)+4) if g!=f and tuple((s+S[g])//2) not in tiles[i][1]);idx[f,t]=i
import sympy as sp
from scipy.linalg import eigh
checks=[]
def ck(label,test):
    assert bool(test),label
    checks.append(label);print(f'PASS {len(checks):03d} {label}',flush=True)
def near(a,b,tol=2e-9):return np.allclose(a,b,atol=tol,rtol=tol)
def chi(b):return (-1j*np.cross(b.conj(),b)).real
def crossmat(p):
    x,y,z=p;return np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
def J(H,x):return 2*np.imag(x[:,None]*H.T*x.conj()[None,:])
O=[0,33,34,35]; V=O[1:]; d=36
# A1 + T2 polar read at the actual centre. Equal magnitude sign weights.
T=np.column_stack([np.ones(8,dtype=int),S]); H=np.zeros((d,d),int)
for i,j in edges:
    if i!=0:H[i,j]=H[j,i]=-1
H[np.ix_(base,O)]=-T;H[np.ix_(O,base)]=-T.T
ck('33 original geometric positions; 36 complex coordinates, four at O',len(tiles)==33 and len(O)==4 and len(edges)==104)
ck('orthogonal scalar and polar centre channels',np.array_equal(T.T@T,8*np.eye(4,dtype=int)))
ck('centre retains all eight original scalar bonds',np.all(H[0,base]==-1))
ck('24 directional couplings at O and 104 original bonds',np.count_nonzero(np.triu(H,1))==128)
ck('scalar and spatial orthogonality forces old scalar darkness',np.array_equal(T[:,0]@T[:,1:],np.zeros(3)))
# Exact single-cell intertwining under all Td transformations.
for R in [np.diag(sig)@np.eye(3,dtype=int)[list(p)] for p in permutations(range(3)) for sig in product([-1,1],repeat=3) if np.prod(sig)==1]:
    perm=[lookup[k,frozenset(tuple(R@np.array(a)) for a in vs)] for k,vs in tiles]; U=np.zeros((d,d),int);U[perm,np.arange(33)]=1;U[np.ix_(V,V)]=R
    ck('full directional centre equivariance under Td',np.array_equal(U@H@U.T,H))
# Inversion changes chambers and polar centre, not scalar. Two T2 copies: one bright, one dark.
perm=[lookup[(k[0]+('B' if k[-1]=='A' else 'A') if k!='O' else 'O'),frozenset(tuple(-np.array(a)) for a in vs)] for k,vs in tiles]
U=np.zeros((d,d),int);U[perm,np.arange(33)]=1;U[np.ix_(V,V)]=-np.eye(3,dtype=int)
ck('chamber inversion symmetry including polar O',np.array_equal(U@H@U.T,H))
ck('opposite polar reads cancel for even chamber amplitudes',np.array_equal(S.T@np.vstack([A,A]),np.zeros((3,3),int)))
ck('odd chamber pattern is bright at O',np.array_equal(S.T@S,8*np.eye(3,dtype=int)))
# Select one original tetrahedral face with outward normal s. Reflect neighbour in plane s.x=1.
s=S[0]; face=[i for i in range(1,33) if all(np.dot(s,v)==1 for v in tiles[i][1])]
ck('one actual original Triforce face has three outer tiles and one central tile',len(face)==4 and len(set(face)&set(inner))==1 and len(set(face)&set(outer))==3)
R=sp.eye(3)-sp.Rational(2,3)*sp.Matrix(s)*sp.Matrix(s).T; shift=sp.Rational(2,3)*sp.Matrix(s)
ck('face reflection is an exact improper isometry',R.T*R==sp.eye(3) and R.det()==-1)
for i in face:
    ck('all vertices of matched subtriangle coincide exactly',all(R*sp.Matrix(v)+shift==sp.Matrix(v) for v in tiles[i][1]))
ck('two distinct origins on opposite sides of shared plane',sp.Matrix(s).dot(shift)==2)
F=np.eye(d,dtype=int)[:,face]; K=F@F.T; H2=np.block([[H,-K],[-K,H]])
ck('matched interface is rank four and no edge/vertex-only exchange',np.linalg.matrix_rank(K)==4 and np.count_nonzero(K)==4)
ck('two identical cells with reciprocal Hermitian face matching',np.array_equal(H2,H2.T) and np.array_equal(H2[:d,:d],H2[d:,d:]))
# A1 + T2 port basis of the four congruent face tiles: average plus three differences.
W=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
ck('four-channel interface admits orthogonal common/difference read',near(W@W.T,np.eye(4)))
# Exact order of arrival: for initial directional centre, receiver at neighbour O is t^3.
O2=[d+i for i in O]; V2=[d+i for i in V]; P=H2.copy();
for order in [1,2]:
    ck('no shorter path from source O to neighbour O',np.array_equal(P[np.ix_(O2,O)],np.zeros((4,4),int)));P=P@H2
n=np.r_[1,s]; ck('exact third-order matched central tile transfer block',np.array_equal(P[np.ix_(O2,O)],-np.outer(n,n)))
print('third-order O→O block:',P[np.ix_(O2,O)].tolist())
# A face supplies just one normal-direction projection at order three, not all polar components.
ck('leading spatial transfer rank one',np.linalg.matrix_rank(P[np.ix_(V2,V)])==1)
# The four face-normal records of either chamber are complete at O.
for chamber in [A,-A]:
    N=np.column_stack([np.ones(4,dtype=int),chamber]);ck('four face normals span the full four-coordinate origin',np.array_equal(N.T@N,4*np.eye(4,dtype=int)))
# All-eight face-first initial winding, odd chamber amplitude to activate polar centre.
z=np.array([1,1j,0],complex)/np.sqrt(2); x=np.zeros(d,complex)
for (i,j),k in idx.items():x[k]=S[i]@z/3+S[j]@z
x/=np.linalg.norm(x); initial=np.r_[x,np.zeros(d,complex)]
signs=np.sign(S@chi(z)); jb=lambda Jm:np.array([[Jm[a,b] for a,b in zip(r,r[1:]+r[:1])] for r in rings])
ck('all eight initial rings row-closed and all 24 ring currents nonzero',all(abs(sum(x[r]))<1e-12 for r in rings) and np.min(jb(J(H,x))*signs[:,None])>0)
ck('initial inner triangles and all centre components empty',near(x[inner+O],0))
ck('no first-order centre excitation from outer tiles',near((H@x)[O],0))
ck('second-order directional O excitation nonzero',np.linalg.norm((H@H@x)[V])>1e-5)
print('H² x at O:',(H@H@x)[O]); print('directional leading occupation coefficient:',np.linalg.norm((H@H@x)[V])**2/4)
# Exact single-cell second-order formula for raw q: signs determine constructive sum.
raw=np.zeros((d,3),int)
for (i,j),k in idx.items():raw[k]=S[i]+3*S[j]
ck('exact second-order face-first directional centre forcing',np.array_equal((H@H@raw)[O],np.vstack([np.zeros((1,3),int),-64*np.eye(3,dtype=int)])))
ck('exact raw outer basis normalization',np.array_equal(raw.T@raw,192*np.eye(3,dtype=int)))
print('H² outer basis at O:',(H@H@raw)[O].tolist())
# Hermitian two-cell evolution, no forcing or sink.
eig,U=eigh(H2); coeff=U.conj().T@initial
Tgrid=np.linspace(0,12,1201); series=[]; strict=[]
for t in Tgrid:
    xx=U@(np.exp(-1j*eig*t)*coeff);jj=J(H2,xx); dx=-1j*H2@xx; dn=2*np.real(xx.conj()*dx)
    flux=jj[:d,d:].sum(); n1=np.linalg.norm(xx[:d])**2;n2=np.linalg.norm(xx[d:])**2
    throat1=np.linalg.norm(xx[V])**2;throat2=np.linalg.norm(xx[V2])**2
    oin=jj[np.ix_(inner,V)].sum();ringmin=np.min(jb(jj[:d,:d])*signs[:,None]);
    series.append([t,n1,n2,throat1,throat2,flux,oin,ringmin])
    if ringmin>1e-8 and oin>1e-8 and flux>1e-8 and throat2>1e-10:strict.append(t)
    if round(t*100)%100==0:
        ck('two-cell local continuity and reciprocal interface',near(dn,-jj.sum(1)) and near(dn[:d].sum(),-flux) and near(dn[d:].sum(),flux))
        ck('total norm and energy conserved',near(n1+n2,1) and near(np.vdot(xx,H2@xx),np.vdot(initial,H2@initial)))
series=np.array(series)
ck('directional O in both cells populated from eight face vortices',series[:,3].max()>1e-4 and series[:,4].max()>1e-4)
ck('nonzero interface transport into neighbouring cell',series[:,2].max()>1e-3)
ck('all 24 original ring signs, inward O flux and outward face flux coexist at sampled times',len(strict)>0)
ck('closed two-cell interface reverses flux, not permanent drain',series[:,5].min()<0 and series[:,5].max()>0)
ck('integral interface balance on dense time grid',near(np.trapezoid(series[:,5],series[:,0]),series[-1,2],tol=2e-4))
print('simultaneous ring/centre/interface samples:',len(strict),'range',min(strict),max(strict));print('peak O occupation',series[:,3:5].max(axis=0),'peak neighbour norm',series[:,2].max())
# Full backreaction, neutral axial canonical variables at each O.
# H_total = psi† H2 psi + sum((p²+Ω² a²)/2 - g p.C(b)).
g=.7;Omega=1.3
# Use real integration, no frozen chirality. p.C(b)=b† i[p]_cross b.
def unpack(X):return X[:72]+1j*X[72:144],X[144:].reshape(2,2,3)
def pack(x,r):return np.r_[x.real,x.imag,r.ravel()]
def rhs(t,X):
    x,r=unpack(X);dx=-1j*(H2@x);dr=np.empty_like(r)
    for c,v in enumerate([V,V2]):
        a,p=r[c]; b=x[v];dx[v]+= -g*crossmat(p)@b # -i*(-g*i[p]x)=-g[p]x
        dr[c,0]=p-g*chi(b);dr[c,1]=-Omega**2*a
    return pack(dx,dr)
def energy(X):
    x,r=unpack(X);return np.vdot(x,H2@x).real+sum((p@p+Omega**2*(a@a))/2-g*p@chi(x[v]) for (a,p),v in zip(r,[V,V2]))
for seed in range(4):
    rng=np.random.default_rng(990+seed)
    if seed==0: x0=initial;r0=np.zeros((2,2,3))
    else:
        x0=rng.normal(size=72)+1j*rng.normal(size=72);x0/=np.linalg.norm(x0);r0=rng.normal(size=(2,2,3))*.15
    X0=pack(x0,r0); sol=solve_ivp(rhs,[0,8],X0,t_eval=np.linspace(0,8,401),rtol=2e-10,atol=2e-12,method='DOP853')
    ck('nonlinear solver completed',sol.success)
    en=np.array([energy(X) for X in sol.y.T]);N=np.array([np.linalg.norm(unpack(X)[0])**2 for X in sol.y.T]);
    ck('full nonlinear backreaction conserves energy',np.max(abs(en-en[0]))<2e-8)
    ck('full nonlinear backreaction conserves occupation',np.max(abs(N-N[0]))<2e-8)
    # Local continuity includes internal mixing of directional components; cell sum unaffected.
    x,r=unpack(sol.y[:,-1]);dx,_=unpack(rhs(8,sol.y[:,-1]));jj=J(H2,x)
    ck('neutral interaction does not spoil interface balance',near(2*np.real(np.vdot(x[:d],dx[:d])),-jj[:d,d:].sum()))
    ck('U(1) equivariance of full nonlinear equations',near(rhs(0,pack(np.exp(.37j)*x,r)),pack(np.exp(.37j)*dx,unpack(rhs(0,sol.y[:,-1]))[1])))
    # Time reversal: conjugate wave, reverse canonical p, leave a fixed.
    def rev(X):
        x,r=unpack(X);r=r.copy();r[:,1]*=-1;return pack(x.conj(),r)
    ck('full equations time-reversal covariant',near(rhs(0,rev(sol.y[:,-1])),-rev(rhs(0,sol.y[:,-1]))))
    if seed==0:ck('neutral axial receivers excited at both actual origins',all(np.max(np.linalg.norm(sol.y[144+6*c:150+6*c],axis=0))>1e-6 for c in range(2)))
    else:ck('noncollinear nonlinear backreaction actually active',any(np.linalg.norm(np.cross(p,chi(x[v])))>1e-6 for (a,p),v in zip(r,[V,V2])))
    print('nonlinear case',seed,'max E,N errors',np.max(abs(en-en[0])),np.max(abs(N-N[0])))
# Analytic Stage VIII constant-C check with full wave evolution in an isotropic triplet.
C0=chi(z); y0=np.r_[z.real,z.imag,np.zeros(6)]
def iso(t,y):
    b=y[:3]+1j*y[3:6];a,p=y[6:9],y[9:12];db=-g*crossmat(p)@b;return np.r_[db.real,db.imag,p-g*chi(b),-Omega**2*a]
sol=solve_ivp(iso,[0,10],y0,t_eval=np.linspace(0,10,201),rtol=1e-11,atol=1e-13)
ck('Stage VIII analytic collinear response with actual backreaction',near(sol.y[6:9].T,-g/Omega*np.sin(Omega*sol.t)[:,None]*C0,tol=1e-8) and near(sol.y[9:12].T,g*(1-np.cos(Omega*sol.t))[:,None]*C0,tol=1e-8))
ck('Stage VIII chirality constant without freezing wave',all(near(chi(v[:3]+1j*v[3:6]),C0,tol=1e-8) for v in sol.y.T))
root=Path(__file__).parent;np.savetxt(root/'coupled_origins_dynamics.csv',series,delimiter=',',header='time,N1,N2,O1_polar,O2_polar,face_flux_1_to_2,O1_inward_flux,min_directed_ring_bond',comments='')
fig,ax=plt.subplots(2,1,figsize=(9,7),sharex=True);ax[0].plot(series[:,0],series[:,1],label='Cell 1');ax[0].plot(series[:,0],series[:,2],label='Cell 2');ax[0].plot(series[:,0],series[:,3],label='Origin 1 polar');ax[0].plot(series[:,0],series[:,4],label='Origin 2 polar');ax[0].set_ylabel('Occupation');ax[0].legend(ncol=2);ax[1].plot(series[:,0],series[:,5],label='Matched-face flux 1→2');ax[1].plot(series[:,0],series[:,6],label='Inner→O1 flux');ax[1].axhline(0,color='gray',lw=.6);ax[1].set(xlabel='Dimensionless time',ylabel='Signed current');ax[1].legend();fig.tight_layout();fig.savefig(root/'figures/12_coupled_origins.svg');plt.close(fig)
print(f'{len(checks)}/{len(checks)} Stage IX checks passed.')
