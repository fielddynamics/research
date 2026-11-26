"""Core-coupled eight-vortex exploration; Stage VII and Stage IX, no fitted constants.
Geometry prefix from pinned verify_coupled_origins.py, reconstruction matching prior refinement.
Run with numpy scipy sympy matplotlib. Exact checks and floating diagnostics labeled separately.
"""
from itertools import combinations, permutations, product
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
P=Path(__file__).resolve().parent
checks=0
def ck(name, cond):
    global checks
    assert bool(cond),name
    checks+=1; print(f'PASS {checks:03} {name}',flush=True)
def sign(p):return (-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
perms=list(permutations(range(4))); even=[p for p in perms if sign(p)==1]
A=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)],dtype=int)
# Faithful reconstruction of verify_coupled_origins.py, pre-check prefix.
S=np.vstack((A,-A)); tiles=[('O',frozenset([(0,0,0)]))]
for tag,T in [('A',A),('B',-A)]:
    for f in combinations(range(4),3):
        tri=T[list(f)]; mid=lambda a,b:tuple((a+b)//2)
        tiles.append(('C'+tag,frozenset(mid(tri[i],tri[j]) for i,j in combinations(range(3),2))))
        for i in range(3):tiles.append(('E'+tag,frozenset([tuple(tri[i])]+[mid(tri[i],tri[j]) for j in range(3) if j!=i])))
pos=np.array([np.mean(list(v),axis=0) for _,v in tiles]);lookup={v:i for i,(_,v) in enumerate(tiles)}
outer=[i for i,(k,_) in enumerate(tiles) if k[0]=='E'];inner=[i for i,(k,_) in enumerate(tiles) if k[0]=='C']
edges=[(i,j) for i,j in combinations(range(1,33),2) if len(tiles[i][1]&tiles[j][1])==2]+[(0,i) for i in inner]
rings=[];idx={};base=[]
for f,s in enumerate(S):
    ids=[i for i in outer if tuple(s) in tiles[i][1]]
    if np.cross(pos[ids[0]],pos[ids[1]])@s<0:ids[1],ids[2]=ids[2],ids[1]
    rings.append(ids);base.append(next(i for i in inner if np.allclose(pos[i],s/3)))
    for i in ids:
        t=next(g for g in range(4*(f//4),4*(f//4)+4) if g!=f and tuple((s+S[g])//2) not in tiles[i][1]);idx[f,t]=i
O=[0,33,34,35]; T=np.column_stack([np.ones(8,dtype=int),S]); H=np.zeros((36,36),int)
for i,j in edges:
    if i!=0:H[i,j]=H[j,i]=-1
H[np.ix_(base,O)]=-T;H[np.ix_(O,base)]=-T.T
ck('native geometry: 32 tile sites, 104 scalar graph bonds, four origin coordinates',len(tiles)==33 and len(edges)==104 and H.shape==(36,36))
ck('native H36 symmetric',np.array_equal(H,H.T))
# Fine graph constructed from the *actual* 32 primary tiles. All fine vertices doubled integers.
def children(t):
    a,b,c=sorted(t); a,b,c=map(np.array,(a,b,c));ab,ac,bc=a+b,a+c,b+c
    return [frozenset(map(tuple,vs)) for vs in [(ab,ac,bc),(2*a,ab,ac),(2*b,ab,bc),(2*c,ac,bc)]]
F=[f for _,t in tiles[1:] for f in children(t)];parent=np.repeat(np.arange(1,33),4);N=132
fine_edges=[(i,j) for i,j in combinations(range(128),2) if len(F[i]&F[j])==2]
inter=[(i,j) for i,j in fine_edges if parent[i]!=parent[j]]; intra=[(i,j) for i,j in fine_edges if parent[i]==parent[j]]
from collections import Counter
counts=Counter(tuple(sorted((parent[i],parent[j]))) for i,j in inter)
ck('fine graph 128 distinct secondary triangles (both chamber surfaces)',len(set(F))==128)
ck('intra-parent graph: three medial edges per tile',len(intra)==96)
ck('each of 96 original tile bonds splits into two actual matching edges',set(counts)==set(e for e in edges if e[0]!=0) and set(counts.values())=={2})
# E maps coarse amplitudes to uniform child amplitudes /2; origins unchanged.
E2=np.zeros((N,36),int)
for k,i in enumerate(parent):E2[k,i]=1
for k,i in enumerate(O):E2[128+k,i]=2
ck('prolongation E=E2/2 is isometric',np.array_equal(E2.T@E2,4*np.eye(36)))
# Minimal illustrative extension: cross edge weight -2 from compression, within-tile
# graph Laplacian weight 1 (unfixed scale), uniform origin coupling /2 from compression.
# use 2*Hf integer. Local Laplacian zero on constant child states.
G=np.zeros((N,N),int)
for i,j in inter:G[i,j]=G[j,i]=-4
for i,j in intra:G[i,j]=G[j,i]=-2;G[i,i]+=2;G[j,j]+=2
for k,i in enumerate(parent):
    for a,o in enumerate(O):G[k,128+a]=G[128+a,k]=H[i,o]
ck('constructed fine Hamiltonian exactly compresses to H36',np.array_equal(E2.T@G@E2,8*H))
D=np.zeros((N,N),int)
for i,j in intra:D[i,j]-=1;D[j,i]-=1;D[i,i]+=1;D[j,j]+=1
ck('any uniform within-parent Laplacian scaling leaves leakage unchanged',not np.any(D@E2))
# Native Stage VII witness, retaining all 104 actual edges.
W=sp.zeros(33); weights=[-1,-sp.Rational(1,2),-2,-1,-1,-1]; r,d,b,a,k,o=weights
for i in inner: W[i,i]=-sp.Rational(99,10)
def bond(i,j,v):
    assert W[i,j]==0 and tuple(sorted((i,j))) in edges
    W[i,j]=W[j,i]=v
for ids in rings:
    for i,j in combinations(ids,2):bond(i,j,r)
for (i,j),p in idx.items():
    if i<4:bond(p,idx[j^4,i^4],d)
    bond(p,base[i],b);bond(p,base[j^4],a)
for i,j in product(range(4),repeat=2):
    if i!=j:bond(base[i],base[j+4],k)
for i in base:bond(0,i,o)
ck('exact Stage VII witness all original 104 bonds',sum(W[i,j]!=0 for i,j in combinations(range(33),2))==104)
# T2 (even/odd chamber) subspaces from the actual tile labels.
def embed(eps,n):
    blocks=4 if n==36 and eps==-1 else 3
    B=np.zeros((n,3*blocks),int)
    for (i,j),p in idx.items():
        f=1 if i<4 else eps
        B[p,:3]=f*A[i%4];B[p,3:6]=f*A[j%4]
    for i,p in enumerate(base):B[p,6:9]=(1 if i<4 else eps)*A[i%4]
    if blocks==4:B[33:36,9:12]=np.eye(3,dtype=int)
    return B
B7=embed(1,33);M7=sp.Matrix([[-2,sp.Rational(1,2),-2],[-sp.Rational(1,2),1,-1],[-5,-1,-sp.Rational(89,10)]])
ck('exact Stage VII reduction HB=B(M tensor I3)',W*sp.Matrix(B7)==sp.Matrix(B7)*sp.kronecker_product(M7,sp.eye(3)))
ck('Stage VII stationary branch exact',M7*sp.Matrix([sp.Rational(1,3),1,-sp.Rational(4,15)])==sp.Rational(11,10)*sp.Matrix([sp.Rational(1,3),1,-sp.Rational(4,15)]))
Ms={1:np.array([[-2,0,-1],[-1,1,-1],[-2,-2,1]]),-1:np.array([[-2,2,-1,0],[1,1,1,0],[-4,4,-1,-1],[0,0,-8,0]])}
Bs={eps:embed(eps,36) for eps in [1,-1]}
for eps in [1,-1]:
    B=Bs[eps]; M=Ms[eps]
    ck(f'exact Stage IX parity {eps} reduction',np.array_equal(H@B,B@np.kron(M,np.eye(3,dtype=int))))
    gram=B.T@B;ck(f'parity {eps} metric self-adjointness',np.array_equal(gram@np.kron(M,np.eye(3,dtype=int)),np.kron(M.T,np.eye(3,dtype=int))@gram))
    print('Stage IX parity',eps,'charpoly',sp.Matrix(M).charpoly().as_expr())
ck('two parity reductions orthogonal',not np.any(Bs[1].T@Bs[-1]))
# Current and orientation reads. Ring mean about each OUTWARD stellation axis.
core_edges=[(base[i],base[j+4]) for i,j in product(range(4),repeat=2) if i!=j]
core_cross=np.array([np.cross(pos[i],pos[j]) for i,j in core_edges])
def currents(h,y):return 2*np.imag(y[:,None]*h.T*y.conj()[None,:])
def metrics(h,y):
    J=currents(h,y); rr=np.array([[J[i,j] for i,j in zip(ids,ids[1:]+ids[:1])] for ids in rings]);means=rr.mean(1)
    core=np.array([J[i,j] for i,j in core_edges]); moment=core@core_cross
    return rr,means,core,moment
# Exact identity for cubic pseudoscalar from eight real ring currents. No assumption of mean winding.
x,y,z=sp.symbols('x y z',real=True); c=sp.Matrix([x,y,z]);
ck('exact tetrahedral cubic moment',sp.expand(sum((sp.Matrix(s).dot(c))**3 for s in A)/4)==6*x*y*z)
ck('exact opposite chamber sign',sp.expand(sum((sp.Matrix(s).dot(c))**3 for s in -A)/4)==-6*x*y*z)
ck('linear winding mean vanishes for any collective axial vector',sum((sp.Matrix(s) for s in A),sp.zeros(3,1))==sp.zeros(3,1))
# All Td maps: axial vector transforms det(R)R, cubic product is a sign character.
for p in perms:
    R=(A[list(p)].T@A)//4;sgn=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4)); v=sgn*sp.Matrix(R)*c
    ck(f'cubic axial pseudoscalar covariance {p}',sp.expand(v[0]*v[1]*v[2])==sgn*x*y*z)
# A second candidate, quartic in complex collective phase, with U(1) invariance.
# q4 = Im(zx^2 conj(zy)^2 + zy^2 conj(zz)^2 + zz^2 conj(zx)^2).
# For a circular normalized state it equals -3 Cx Cy Cz/2 (with convention checked below).
def circ(n):
    n=np.array(n,float);n/=np.linalg.norm(n);u=np.eye(3)[np.argmin(abs(n))];u-=n*(n@u);u/=np.linalg.norm(u);return (u+1j*np.cross(n,u))/np.sqrt(2)
def chir(z):return (-1j*np.cross(z.conj(),z)).real
def q4(z):return np.imag(sum(z[i]**2*z[(i+1)%3].conjugate()**2 for i in range(3)))
def orient(j):return (np.mean(j[:4]**3)-np.mean(j[4:]**3))/2
rng=np.random.default_rng(241123);rho=np.sqrt(3)/8
for n in [[.05,.08,1.],[.1,-.07,1.],[0,0,1.],[1,1,1.],[1,2,3.]]:
    zz=circ(n);C=chir(zz)
    ck('quartic phase scalar equals 3/2 product on circular normalized states',np.isclose(q4(zz),1.5*np.prod(C),atol=1e-13))
    ck('quartic phase scalar U(1) invariant',np.isclose(q4(zz*np.exp(.71j)),q4(zz),atol=1e-13))
    for p in perms:
        R=(A[list(p)].T@A)//4;sgn=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        ck('quartic phase scalar reflection law',np.isclose(q4(R@zz),sgn*q4(zz),atol=1e-13))
# Exact operator moment for arbitrary coherent collective ansatz; tests across both parity and models.
models=[('VII',np.array(W,float),B7,1),('IX-even',H,Bs[1],1),('IX-odd',H,Bs[-1],-1)]
for name,h,B,eps in models:
    for test in range(6):
        zz=rng.normal(size=3)+1j*rng.normal(size=3);zz/=np.linalg.norm(zz);C=chir(zz)
        xx=rng.normal(size=B.shape[1]//3)+1j*rng.normal(size=B.shape[1]//3)
        yy=rho*B@np.kron(xx,zz);rr,j,I,ell=metrics(h,yy)
        # Both models r=k=-1. Actual ring mean alpha=|v|^2/16 and core moment -eps |w|^2 C/6.
        alpha=abs(xx[1])**2/16
        ck(name+' ring means from actual directed bond currents',np.allclose(j,alpha*(S@C),atol=2e-13))
        ck(name+' exact core angular current law (numerical witness)',np.allclose(ell,-eps*abs(xx[2])**2*C/6,atol=2e-13))
        ck(name+' core current independently divergence-free',np.allclose(I.reshape(4,3).sum(1),0,atol=2e-13))
        ck(name+' nonzero cubic read despite zero mean read',np.isclose(orient(j),6*alpha**3*np.prod(C),atol=2e-13) and abs(j[:4].mean())<1e-12)
        ck(name+' cubic core angular read same orientation up to parity',np.isclose(np.prod(ell),(-eps*abs(xx[2])**2/6)**3*np.prod(C),atol=2e-13))
# Stage VII exact witness: generic tilted axis meeting published all-bond threshold.
zz=circ([.05,.08,1]);C=chir(zz);xstar=np.array([1/3,1,-4/15]);psi7=rho*B7@np.kron(xstar,zz);psi7/=np.linalg.norm(psi7)
rr,j,I,ell=metrics(np.array(W,float),psi7)
ck('Stage VII witness all 24 bonds circulate and actual core moment nonzero',np.all(rr*rr[:,0,None]>0) and np.linalg.norm(ell)>0)
ck('Stage VII witness q cubic nonzero and earlier mean read zero',abs(orient(j))>1e-9 and abs(j[:4].mean())<1e-13)
print('Stage VII stationary norm, ring cubic, core moment:',np.linalg.norm(psi7),orient(j),ell.tolist())
# Discrete stream function on the six actual octahedron vertices: exact dual edge identity.
# Each shared primal edge is oriented along the cross of outward normals.
for i,j in product(range(4),repeat=2):
    if i==j:continue
    a0,b0=base[i],base[j+4];v0,v1=sorted(tiles[a0][1]&tiles[b0][1]);v0,v1=np.array(v0),np.array(v1)
    cross=np.cross(A[i],-A[j]);delta=v1-v0
    if cross@delta<0:delta=-delta
    ck('actual octahedral shared edge: outward cross equals twice directed primal edge',np.array_equal(cross,2*delta))
# Thus I_ab = sigma(v_end)-sigma(v_start), sigma(v)=2 k eps rho^2 |w|^2 v dot C.
# This is a discrete stream function on the primal octahedron, not an identification of two Hamiltonians.
ck('axis-aligned counterexample: all ring means nonzero but cubic read zero',np.all(S@np.array([0,0,1])!=0) and np.prod([0,0,1])==0)
# Exact representation selection: sign occurs neither in T2 tensor T2 nor in scalar x T2.
# Use actual traces of vector matrices; inner product of characters.
sg=[];ct=[]
for p in perms:
    R=(A[list(p)].T@A)//4;sg.append((-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4)));ct.append(int(np.trace(R)))
ck('no quadratic S4 pseudoscalar on any number of T2 copies',sum(s*t*t for s,t in zip(sg,ct))==0)
ck('one axial vector in T2 tensor T2',sum(s*t**3 for s,t in zip(sg,ct))==24)
ck('signed ring representation A2+T1, no scalar contribution from T2 bilinear',sum(s*t*t for s,t in zip(sg,ct))==0)
# Fine-mesh prolongation from earlier geometry, generalized to original coarse H (VII padded to 36 with inert polar slots).
E=E2/2;Pco=E@E.T;D=np.zeros((N,N),int)
for i,j in intra:D[i,j]-=1;D[j,i]-=1;D[i,i]+=1;D[j,j]+=1
W36=np.zeros((36,36));W36[:33,:33]=np.array(W,float)
# For each original edge two fine edges. weight 2 h; diagonal child equal parent diagonal.
# Origin coupling is uniform h/2. Intra parent Laplacian remains independent parameter.
def fine(h,kappa):
    f=np.zeros((N,N))
    for i,j in inter:f[i,j]=f[j,i]=2*h[parent[i],parent[j]]
    for i,p in enumerate(parent):
        f[i,i]=h[p,p]
        for j,o in enumerate(O):f[i,128+j]=f[128+j,i]=h[p,o]/2
    f[128:,128:]=h[np.ix_(O,O)]
    return f+kappa*D
# Actual coordinate permutation on all fine tiles, including physical polar O.
fl={f:i for i,f in enumerate(F)}
for p in perms:
    R=(A[list(p)].T@A)//4;Uf=np.zeros((N,N),int);Uf[128,128]=1;Uf[129:,129:]=R
    for i,f in enumerate(F):Uf[fl[frozenset(tuple(R@v) for v in f)],i]=1
    # 20 times VII and 2 times IX are integer; no floating rank or tolerance.
    for name,h,scale in [('VII',W36,20),('IX',H,2)]:
        hf=np.rint(scale*fine(h,1)).astype(int)
        ck(name+' actual fine geometry preserves all tetrahedral permutations',np.array_equal(Uf@hf,hf@Uf))
# Aggregate fine currents on each original edge; internal child edges excluded.
edgechildren={}
for i,j in inter:
    a,b=parent[i],parent[j];edgechildren.setdefault((a,b),[]).append((i,j));edgechildren.setdefault((b,a),[]).append((j,i))
def fine_metrics(h,y):
    J=currents(h,y)
    jc=lambda a,b:sum(J[i,j] for i,j in edgechildren[a,b])
    rr=np.array([[jc(i,j) for i,j in zip(ids,ids[1:]+ids[:1])] for ids in rings]);means=rr.mean(1)
    I=np.array([jc(i,j) for i,j in core_edges]);ell=I@core_cross
    # Actual child moment separately (fine centroid positions in original units).
    fpos=np.array([np.mean(list(f),axis=0)/2 for f in F]);lf=sum((J[i,j]*np.cross(fpos[i],fpos[j]) for a,b in core_edges for i,j in edgechildren[a,b]),np.zeros(3))
    return rr,means,I,ell,lf
# Preserve exact normalization and verify current aggregation at embedding time.
for name,h,xx in [('VII',W36,np.r_[psi7,0,0,0]),('IX-even',H,rho*Bs[1]@np.kron([1/3,1,-.2],zz)),('IX-odd',H,rho*Bs[-1]@np.kron([1/3,1,-.2,0],zz))]:
    xx=xx/np.linalg.norm(xx);hf=fine(h,1)
    ck(name+' fine compression matches actual coarse Hamiltonian',np.allclose(E.T@hf@E,h,atol=1e-13))
    rf,jf,If,lf,_=fine_metrics(hf,E@xx);rc,jc,Ic,lc=metrics(h,xx)
    ck(name+' aggregate fine ring and core currents reproduce coarse exactly at uniform prolongation',np.allclose(rf,rc) and np.allclose(If,Ic) and np.allclose(lf,lc))
    ck(name+' fine coarse leakage independent of intra scale',np.allclose((np.eye(N)-Pco)@fine(h,0)@E,(np.eye(N)-Pco)@fine(h,16)@E))
# Symmetry-reduced effective dynamics: report actual response for original witness and stage IX odd row-closed state.
# Stage VII initial empty core + stationary; Stage IX odd empty core. All eight rings initially active.
init7=np.r_[rho*B7@np.kron([1/3,1,0],zz),0,0,0]
init9=rho*Bs[-1]@np.kron([1/3,1,0,0],zz)
scenarios=[('VII-empty',W36,init7),('VII-stationary',W36,np.r_[psi7,0,0,0]),('IX-odd-empty',H,init9)]
times=np.linspace(0,8,321);series=[];summary=[]
for name,h,x0 in scenarios:
    x0=x0/np.linalg.norm(x0);e0,v0=eigh(h);c0=v0.T@x0
    Y=(v0@(np.exp(-1j*e0[:,None]*times)*c0[:,None])).T
    rr0=metrics(h,x0)[0]; signs=np.sign(rr0);ck(name+' initial all eight rings circulate',np.all(rr0*rr0[:,0,None]>0))
    for kap in [0,1,4,16,64]:
        hf=fine(h,kap);ev,v=eigh(hf);coef=v.T@(E@x0);Z=(v@(np.exp(-1j*ev[:,None]*times)*coef[:,None])).T
        ck(name+f' k={kap} norm conservation',np.max(abs(np.sum(abs(Z)**2,axis=1)-1))<2e-12)
        energy=np.einsum('ti,ij,tj->t',Z.conj(),hf,Z).real;ck(name+f' k={kap} energy conservation',np.max(abs(energy-energy[0]))<2e-10)
        minring=1; mincore=1; maxdetail=0; qkeep=0; allring=0; maxaxis=0; maxringaxis=0; maxdiv=0
        for t,xc,xf in zip(times,Y,Z):
            r0,j0,ic,lc=metrics(h,xc);rf,jf,If,lf,lfactual=fine_metrics(hf,xf)
            maxaxis=max(maxaxis,np.linalg.norm(lf-C*(lf@C)))
            normals=S@C
            for sl in [slice(0,4),slice(4,8)]:
                vj=normals[sl];maxringaxis=max(maxringaxis,np.linalg.norm(jf[sl]-vj*(jf[sl]@vj)/(vj@vj)))
            maxdiv=max(maxdiv,np.max(abs(If.reshape(4,3).sum(1))))
            detail=np.linalg.norm(xf-E@(E.T@xf))**2;core=float(np.linalg.norm(lf));qv=orient(jf);q0=orient(j0)
            minring=min(minring,np.min(rf*signs));maxdetail=max(maxdetail,detail);allring+=int(np.all(rf*signs>1e-12));qkeep+=int(qv*orient(metrics(h,x0)[1])>0)
            series.append((name,kap,t,detail,np.linalg.norm(E.T@xf-xc),np.min(rf*signs),core,np.linalg.norm(lfactual),np.linalg.norm(lc),qv,q0,np.linalg.norm(xf[128:])**2))
        summary.append((name,kap,maxdetail,minring,allring/len(times),qkeep/len(times)))
        ck(name+f' k={kap} core axis locked and ring means follow tetrahedral axial vector',max(maxaxis,maxringaxis)<2e-11)
        print('Fine diagnostic',summary[-1],'core row divergence max',maxdiv)
# General bound on Schur correction away from detail poles, using independently fixed model.
# D has eigenvalues 0,1,1,4 on each 4-child star. Gap grows with kappa; no physical kappa selected.
from scipy.linalg import null_space
Q=null_space(E.T);ck('detail dimension 96',Q.shape==(132,96));ck('intra-parent detail Laplacian gap one',np.isclose(np.linalg.eigvalsh(Q.T@D@Q).min(),1))
for name,h,_ in scenarios[:2]+scenarios[2:]:
    hf=fine(h,16);hd=Q.T@hf@Q;L=Q.T@hf@E;omega=1j*3
    correction=L.T@np.linalg.solve(omega*np.eye(96)-hd,L)
    ck(name+' exact Schur compression numerical identity',np.allclose(E.T@np.linalg.solve(omega*np.eye(N)-hf,E),np.linalg.inv(omega*np.eye(36)-h-correction),atol=1e-11))
    ck(name+' passive upper-half-plane self energy',np.linalg.eigvalsh((correction-correction.conj().T)/(2j)).max()<1e-10)
    ck(name+' resolvent norm bound',np.linalg.norm(correction,2)<=np.linalg.norm(L,2)**2/3+1e-12)
# Save data, original plots, no assertion that fine coupling is physically selected.
with open(P/'core_flywheel_dynamics.csv','w') as f:
    w=csv.writer(f);w.writerow(['scenario','kappa','t','detail_probability','coarse_error','minimum_signed_ring_current','aggregate_core_moment','fine_cross_boundary_core_moment','coarse_core_moment','fine_cubic_read','coarse_cubic_read','origin_occupation']);w.writerows(series)
with open(P/'core_flywheel_summary.csv','w') as f:
    w=csv.writer(f);w.writerow(['scenario','kappa','peak_detail_probability','min_signed_ring_current','fraction_all_ring_signs','fraction_cubic_sign']);w.writerows(summary)
fig,axs=plt.subplots(3,3,figsize=(12,10),layout='constrained')
for row,(name,_,_) in enumerate(scenarios):
    for kap in [0,1,4,16,64]:
        ss=np.array([s[2:] for s in series if s[0]==name and s[1]==kap]);axs[row,0].plot(ss[:,0],ss[:,1],label=f'κ={kap}');axs[row,1].plot(ss[:,0],ss[:,3]);axs[row,2].plot(ss[:,0],ss[:,4]);
    axs[row,2].plot(ss[:,0],ss[:,6],'k--',label='coarse core');axs[row,0].set_ylabel(name);axs[row,0].legend(fontsize=7,frameon=False);axs[row,1].axhline(0,color='k',lw=.7)
for ax,title in zip(axs[0],['Detail occupation','Minimum signed ring current','Core angular moment magnitude']):ax.set_title(title)
for ax in axs.flat:ax.set_xlabel('Dimensionless time');ax.grid(alpha=.2)
fig.savefig(P/'core_flywheel_dynamics.svg');fig.savefig(P/'core_flywheel_dynamics.png',dpi=150);plt.close(fig)
# Actual stationary Stage VII geometry and directed currents, not funnel artwork.
fig=plt.figure(figsize=(12,5),layout='constrained')
J7=currents(np.array(W,float),psi7)
for panel,showring in [(1,True),(2,False)]:
    ax=fig.add_subplot(1,2,panel,projection='3d');ax.set_box_aspect((1,1,1));ax.view_init(22,34)
    evs=np.vstack([np.eye(3),-np.eye(3)])
    for a0,b0 in combinations(evs,2):
        if a0@b0==0:ax.plot(*np.array([a0,b0]).T,color='#94a3b8',alpha=.6,lw=1)
    ax.scatter(*pos[inner].T,color='#0d9488',s=32);ax.scatter([0],[0],[0],color='#111827',s=22)
    links=core_edges if not showring else [(a0,b0) for ids in rings for a0,b0 in zip(ids,ids[1:]+ids[:1])]
    if showring:ax.scatter(*pos[outer].T,color='#2563eb',s=24)
    mx=max(abs(J7[a0,b0]) for a0,b0 in links)
    for a0,b0 in links:
        j0=J7[a0,b0]
        if j0<0:a0,b0=b0,a0
        st=pos[a0];delta=pos[b0]-st
        ax.quiver(*st,*delta,color='#2563eb' if showring else '#0d9488',linewidth=.7+2*abs(j0)/mx,arrow_length_ratio=.25)
    ax.quiver(0,0,0,*C,color='#d97706',linewidth=2,arrow_length_ratio=.15)
    ax.set_title('Eight outer rings (24 directed bonds)' if showring else 'Shared core (12 central bonds)');ax.set_axis_off()
fig.suptitle('One Stage VII stationary flywheel: actual graph currents; orange = collective axis')
fig.savefig(P/'eight_rings_core.svg');fig.savefig(P/'eight_rings_core.png',dpi=160);plt.close(fig)
print(f'{checks}/{checks} checks passed')
