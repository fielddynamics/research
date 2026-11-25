"""Unified overlapping-origin model; dimensionless amplitude Hamiltonian.
Imports only the geometry/H definition prefix of the preserved Stage IX verifier.
The outer tile read is a specified symmetry-equivariant routing, not derived physical dynamics.
"""
from pathlib import Path
from itertools import product, permutations
import numpy as np
import sympy as sp
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import expm_multiply
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
# Reuse the exact historical construction without rerunning its ODE tests or rewriting its figures.
src=(root/'verify_coupled_origins.py').read_text()
marker="ck('33 original geometric positions;"
assert src.count(marker)==1
ns={'__file__':str(root/'verify_coupled_origins.py')}
exec(compile(src.split(marker)[0],ns['__file__'],'exec'),ns)
S,A,H,O,V,d,base,idx,rings,inner,outer,tiles,pos,J=(ns[k] for k in ('S','A','H','O','V','d','base','idx','rings','inner','outer','tiles','pos','J'))
checks=[]
def ck(msg,test):
    assert bool(test),msg
    checks.append(msg); print(f'PASS {len(checks):03d} {msg}',flush=True)
def eq(a,b):return np.array_equal(a,b)
def near(a,b,tol=1e-10):return np.allclose(a,b,atol=tol,rtol=tol)
W9=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]],dtype=int); W=W9/9
# For apex s, base vertex (s+t)/2 corresponds to lateral tile opposite it.
# Facing sections related by inversion use the same t labels on both sides.
ports=[]
for f,s in enumerate(S):
    ts=[j for j in range(4*(f//4),4*(f//4)+4) if j!=f]
    ids=[idx[f,j] for j in ts]+[base[f]]
    ports.append(ids)
    ck('three lateral tiles plus actual base at each apex',set(ids[:3])==set(rings[f]) and ids[3] in inner)
    for j,k in zip(ts,ids[:3]):
        v=tuple((s+S[j])//2)
        ck('outer read uses lateral face opposite its base vertex',v not in tiles[k][1] and v in tiles[base[f]][1])
    ck('base lies on active leg at s/3',near(pos[base[f]],s/3))
F=[np.eye(d,dtype=int)[:,p] for p in ports]
ck('eight ports partition 32 tiles exactly',sorted(sum(ports,[]))==list(range(1,33)))
ck('four active ports use 16 disjoint tile coordinates',len(set(sum(ports[:4],[])))==16)
ck('all inactive port coordinates distinct from active ones',not(set(sum(ports[:4],[]))&set(sum(ports[4:],[]))))
for i in range(8):
    ck('orthonormal port embedding',eq(F[i].T@F[i],np.eye(4,dtype=int)))
    ck('other seven ports orthogonal',all(not np.any(F[i].T@F[j]) for j in range(8) if j!=i))
# Check full tetrahedral equivariance of the routing, not just local C3.
for p in permutations(range(3)):
 for sig in product([-1,1],repeat=3):
    if np.prod(sig)!=1:continue
    R=np.diag(sig)@np.eye(3,dtype=int)[list(p)]
    mp=[next(j for j,s in enumerate(S) if eq(s,R@v)) for v in S]
    tilemap=[next(j for j,(q,vs) in enumerate(tiles) if q==k and vs==frozenset(tuple(R@np.array(v)) for v in verts)) for k,verts in tiles]
    for i in range(4):
        # Facing inversion mates transform with the same permutation of 3 outer labels.
        perm=[ports[mp[i]].index(tilemap[k]) for k in ports[i]]
        permb=[ports[mp[i+4]].index(tilemap[k]) for k in ports[i+4]]
        ck('Td covariance of facing port labels and area kernel',perm==permb and eq(W9[np.ix_(perm,perm)],W9))
# Exact local transfer spectra and central separation.
wm=sp.Matrix(W9)/9
ck('area kernel exact spectrum',wm.eigenvals()=={sp.Rational(7,9):1,sp.Rational(1,3):1,sp.Rational(-2,9):2})
for v in ([1,-1,0,0],[1,0,-1,0]):
    ck('zero-sum ring modes transmit at signed amplitude -2/9',wm*sp.Matrix(v)==-sp.Rational(2,9)*sp.Matrix(v))
ck('winding subspace has zero direct central read',eq(W9[3,:3],np.ones(3,dtype=int)))
for i in range(4):
    K9=F[i+4]@W9@F[i].T # receiver <- source
    ck('reciprocal interface rank four',np.linalg.matrix_rank(K9)==4)
    nA=np.r_[1,S[i]];nB=np.r_[1,S[i+4]]
    # exact scaled leading block: H_pair = M/9
    M=np.block([[9*H,-K9.T],[-K9,9*H]])
    M2=M@M; M3=M2@M; o2=np.array(O)+d
    ck('no direct or two-hop O-to-O connection',not np.any(M[np.ix_(o2,O)]) and not np.any(M2[np.ix_(o2,O)]))
    ck('leading cubic block is -(2/3) n_B n_A^T',eq(M3[np.ix_(o2,O)],-486*np.outer(nB,nA)))
ck('all four direct port records resolve O',eq(np.c_[np.ones(4,dtype=int),A].T@np.c_[np.ones(4,dtype=int),A],4*np.eye(4,dtype=int)))
# Diamond lattice and relation to original cube-centre/junction construction.
Bmat=(A[0]-A[1:]).T
ck('primitive FCC determinant 16',abs(round(np.linalg.det(Bmat)))==16)
ck('12 distinct directed two-step offsets',len({tuple(a-b) for a in A for b in A if not eq(a,b)})==12)
ck('four exact first-shell directions',eq(A@A.T,4*np.eye(4,dtype=int)-np.ones((4,4),int)))
# All even cube centres split into two cosets of L_A. Each has four odd junctions.
for p in product(range(-4,5,2),repeat=3):
    cls=sum(p)%4
    ck('old cube net separates by centre parity class',cls in (0,2) and all((sum(np.array(p)+s)-sum(A[0]))%4==cls for s in A))
# Periodic diamond network: 3^3 primitive cells x 2 complete fields.
L=3; coords=list(product(range(L),repeat=3)); sites=[(p,b) for p in coords for b in range(2)]; ids={p:i for i,p in enumerate(sites)}; N=len(sites)
shifts=np.vstack([np.zeros((1,3),int),-np.eye(3,dtype=int)])
links=[]; Hnet=lil_matrix((N*d,N*d),dtype=float)
sl=lambda i:slice(i*d,(i+1)*d)
for j in range(N): Hnet[sl(j),sl(j)]=H
for p in coords:
    a=ids[p,0]
    for i,shift in enumerate(shifts):
        b=ids[tuple((np.array(p)+shift)%L),1]; K=F[i+4]@W@F[i].T
        Hnet[sl(b),sl(a)]=-K; Hnet[sl(a),sl(b)]=-K.T; links.append((a,b,i))
Hnet=Hnet.tocsr(); adj=[set() for _ in sites]
for a,b,i in links:adj[a].add(b);adj[b].add(a)
ck('all 54 complete fields have four reciprocal active neighbours',all(len(v)==4 for v in adj) and len(links)==2*N)
visited={0}; todo=[0]
while todo:
    for j in adj[todo.pop()]-visited:visited.add(j);todo.append(j)
ck('periodic network connected',len(visited)==N)
ck('full network Hermitian',(Hnet-Hnet.T).nnz==0)
ck('no artificial exterior source/sink',near(Hnet.diagonal(),0))
# Bloch 72-coordinate symbol is the Fourier block of the same periodic model.
for k in [np.zeros(3),np.array([.3,.5,-.4]),np.array([1,2,3])*2*np.pi/L]:
    C=sum(np.exp(-1j*k@q)*F[i+4]@W@F[i].T for i,q in enumerate(shifts))
    hb=np.block([[H,-C.conj().T],[-C,H]])
    ck('Bloch Hermiticity and time reversal',near(hb,hb.conj().T) and near(np.linalg.eigvalsh(hb),np.linalg.eigvalsh(hb.conj())))
# Initial 8-ring state of Stage IX (raw basis q_i+3q_j), full network evolution.
z=np.array([1,1j,0])/np.sqrt(2); raw=np.zeros((d,3),int)
for (i,j),k in idx.items():raw[k]=S[i]+3*S[j]
x=raw@z; x=x/np.linalg.norm(x); psi=np.zeros(N*d,complex);psi[:d]=x
ring_sign=np.sign(S@(-1j*np.cross(z.conj(),z)).real)
ck('eight initial winding rings and all 24 currents nonzero',all(abs(sum(x[r]))<1e-12 for r in rings) and all(J(H,x)[a,b]*ring_sign[i]>0 for i,r in enumerate(rings) for a,b in zip(r,r[1:]+r[:1])))
ck('initial actual origins and central tiles empty',near(x[inner+O],0))
T=np.linspace(0,8,401); Y=expm_multiply(-1j*Hnet,psi,start=0,stop=8,num=len(T),traceA=0)
rows=[]; strict=0; errN=errE=errC=0.; E0=np.vdot(psi,Hnet@psi).real
nb=sorted(adj[0]); other=list(set(range(N))-set(nb)-{0}); lead=[]
for t,y in zip(T,Y):
    yy=y.reshape(N,d);dy=(-1j*Hnet@y).reshape(N,d);n=(abs(yy)**2).sum(1);nO=(abs(yy[:,V])**2).sum(1); dn=2*np.real((yy.conj()*dy).sum(1)); ledger=np.zeros(N)
    for a,b,i in links:
        f=2*np.imag(np.vdot(yy[b,ports[i+4]],-W@yy[a,ports[i]]));ledger[a]-=f;ledger[b]+=f
    E=np.vdot(y,Hnet@y).real; errN=max(errN,abs(n.sum()-1));errE=max(errE,abs(E-E0));errC=max(errC,np.max(abs(dn-ledger)))
    j0=J(H,yy[0]); signmin=min(j0[a,b]*ring_sign[i] for i,r in enumerate(rings) for a,b in zip(r,r[1:]+r[:1])); incoming=j0[np.ix_(inner,V)].sum();out=-ledger[0]
    if signmin>1e-9 and incoming>1e-9 and out>1e-9 and nO[nb].sum()>1e-10:strict+=1
    rows.append([t,n[0],n[nb].sum(),n[other].sum(),nO[0],nO[nb].sum(),out,signmin,incoming])
rows=np.array(rows)
ck('network norm conserved',errN<1e-10);ck('network energy conserved',errE<1e-10);ck('local ledger equals net occupation change at every sample',errC<1e-10)
ck('direct neighbours populated',rows[:,2].max()>1e-3);ck('beyond first shell populated',rows[:,3].max()>1e-3);ck('directional origin excited in source and neighbours',min(rows[:,4].max(),rows[:,5].max())>1e-5)
ck('simultaneous eight-ring circulation, inward origin current and outward transport sampled',strict>0)
print('MAX ERRORS norm energy continuity',errN,errE,errC)
print('PEAKS first-shell beyond first-shell source O first-shell O',rows[:,2:6].max(0)); print('SIMULTANEOUS SAMPLES',strict)
np.savetxt(root/'unified_flower_dynamics.csv',rows,delimiter=',',header='t,source,first_shell,beyond_first_shell,source_polar_origin,first_shell_polar_origins,source_outflux,min_directed_ring_current,source_inward_origin_current',comments='')
fig,ax=plt.subplots(2,1,figsize=(9,6.8),sharex=True)
for i,lab in [(1,'Source field'),(2,'Four direct neighbours'),(3,'Beyond first shell')]:ax[0].plot(rows[:,0],rows[:,i],label=lab)
ax[0].set(ylabel='Occupation',title='54 complete fields · 1,944 amplitudes · conservative periodic lattice');ax[0].legend(loc='best')
for i,lab in [(4,'Source directional O'),(5,'Four neighbouring directional O')]:ax[1].plot(rows[:,0],rows[:,i],label=lab)
ax[1].set(xlabel='Dimensionless time',ylabel='Origin occupation');ax[1].legend();fig.tight_layout();fig.savefig(root/'figures/28_unified_flower_dynamics.svg');plt.close(fig)
print(f'{len(checks)}/{len(checks)} unified checks passed.')
