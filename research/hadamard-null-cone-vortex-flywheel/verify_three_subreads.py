"""Three nested radix-four reads; exact algebra and native-engine obstruction.
No physical attenuation or new G assumed to be derived.
"""
from pathlib import Path
from itertools import product
import numpy as np
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
P=Path(__file__).resolve().parent
n=0
def ck(label,test):
 global n
 assert bool(test),label
 n+=1; print(f'PASS {n:03d} {label}')
def near(a,b,tol=2e-10): return np.allclose(a,b,rtol=tol,atol=tol)
I=np.eye(4); h=np.array([[(-1)**((i&j).bit_count()) for j in range(4)] for i in range(4)])/2
F=np.kron(np.kron(h,h),h); ix=lambda a,b,c:16*a+4*b+c
# Bottom-up tree: fine read all 16 groups; only their averages feed 4 mid groups;
# only mid averages feed final root. Keep all detail outputs.
B1=np.kron(np.eye(16),h); B2=np.eye(64); B3=np.eye(64)
for a in range(4):
 ids=[ix(a,b,0) for b in range(4)]; B2[np.ix_(ids,ids)]=h
ids=[ix(a,0,0) for a in range(4)]; B3[np.ix_(ids,ids)]=h
B=B3@B2@B1
D=np.eye(64)
for c in range(1,4):
 ids=[ix(a,b,c) for a,b in product(range(4),repeat=2)];D[np.ix_(ids,ids)]=np.kron(h,h)
for b in range(1,4):
 ids=[ix(a,b,0) for a in range(4)];D[np.ix_(ids,ids)]=h
for name,U in [('fine',B1),('intermediate',B2),('root',B3),('tree',B),('detail mixing',D),('FWHT',F)]: ck(name+' orthogonal exactly',np.array_equal(U.T@U,np.eye(64)))
ck('tree plus detail mixing equals full Walsh exactly',np.array_equal(D@B,F))
ck('tree alone is not full Walsh',not np.array_equal(B,F))
ck('final common scalar is sum / 8',np.array_equal(B[0],np.ones(64)/8))
lev=np.array([0 if k==0 else 3 if k%4 else 2 if (k//4)%4 else 1 for k in range(64)])
ck('detail levels 1,3,12,48',np.array_equal(np.bincount(lev),[1,3,12,48]))
ck('same level projectors under detail mixing',all(np.array_equal(D[lev==j][:,lev!=j],np.zeros(((lev==j).sum(),(lev!=j).sum()))) for j in range(4)))
ck('all 64 basis inputs reconstruct exactly',np.array_equal(B.T@B,np.eye(64)))
rng=np.random.default_rng(2026)
for j in range(6):
 x=rng.normal(size=64)+1j*rng.normal(size=64);ck(f'complex ledger {j} reversible and Parseval',near(B.T@B@x,x) and near(np.linalg.norm(B@x),np.linalg.norm(x)) and near(D@B@x,F@x))
# Paired bit order: digit u_i+2v_i. Common 3-cycle 1->2->3->1.
cyc=[0,2,3,1]; T=[ix(cyc[a],cyc[b],cyc[c]) for a,b,c in product(range(4),repeat=3)]; M=np.eye(64)[:,T]; Q=(np.eye(64)+M+M@M)/3
ck('order three',np.array_equal(M@M@M,np.eye(64)))
ck('Walsh intertwines inverse',np.array_equal(F@M,M.T@F))
ck('orbit projector commutes with Walsh',near(Q@F,F@Q))
ck('22-dimensional orbit space',near(np.trace(Q),22))
ck('invariant detail dimensions 1,4,16',near([np.trace(Q[np.ix_(lev==j,lev==j)]) for j in range(4)],[1,1,4,16]))
# Tree basis induced symmetry: one fixed mean and 21 triples, but not independent per physical reader.
Mt=B@M@B.T; Qt=B@Q@B.T
ck('tree symmetry is permutation',near(Mt,np.round(Mt)) and np.all(Mt>=-1e-12) and near(Mt.sum(0),1))
ck('same reduced tree dimensions',near([np.trace(Qt[np.ix_(lev==j,lev==j)]) for j in range(4)],[1,1,4,16]))
ck('tree induced permutation preserves detail strata',all(near(Mt[lev==j][:,lev!=j],0) for j in range(4)))
# Root detail triplet stays within one reader, but intermediate/fine groups may span readers.
ck('one intermediate orbit crosses reader groups',any((np.argmax(Mt[:,k])//16)!=(k//16) for k in np.flatnonzero(lev==2)))
ck('one fine orbit crosses reader groups',any((np.argmax(Mt[:,k])//4)!=(k//4) for k in np.flatnonzero(lev==3)))
# Positive optical attenuation: on mean-preserving input contrasts, 63 raw /21 invariant.
# Apply after tree analysis, not a new dynamical law. alpha chosen physical numerical reference.
alpha=1/137.035999177;t=np.sqrt(alpha); A=np.diag([1]+[t]*63); J=B.T@A@B
ck('mean-preserving isotropic contraction',near(J,t*np.eye(64)+(1-t)*np.ones((64,64))/64))
ck('attenuation commutes with closure symmetry',near(J@Q,Q@J))
qval,qvec=np.linalg.eigh(Q); E=qvec[:,qval>.5]; R=E.T@J@E
ck('invariant attenuation singular values',near(np.linalg.eigvalsh(R),[t]*21+[1]))
ck('full attenuation singular values',near(np.linalg.eigvalsh(J),[t]*63+[1]))
ck('collective invariant determinant intensity alpha^21',abs(2*np.linalg.slogdet(R)[1]-21*np.log(alpha))<1e-10)
ck('unreduced determinant intensity alpha^63',abs(2*np.linalg.slogdet(J)[1]-63*np.log(alpha))<1e-10)
# Lossless 2-channel dilation on all read outputs, unused channels supply complement.
L=np.diag(np.sqrt(1-np.diag(A)**2)); dilation=np.block([[A,-L],[L,A]])
ck('lossless orthogonal dilation',near(dilation.T@dilation,np.eye(128)))
ck('ordinary normalized contrast has intensity alpha, not alpha^21',near(np.linalg.norm(J@(np.eye(64)[0]-np.eye(64)[1])/np.sqrt(2))**2,alpha))
# Original sign grading represented in invariant detail levels; not a passive filter for s=-1.
for s,g in [(-1,13),(0,17),(1,21)]:
 weights=np.array([0,1,s,1])[lev]; G=np.diag(weights); ck(f'graded orbit trace {g}',near(np.trace(Q@G),g))
ck('negative intermediate exponent would amplify, not attenuate',alpha**(-.5)>1)
# Core Pauli algebra: 64 signed real observables, not same as 64 independent amplitudes.
I2=np.eye(2); X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]); pa=[I2,X,Z,Y]
U=(I2+1j*(X+Y+Z))/2; U3=np.kron(np.kron(U,U),U)
ck('single-axis U unitary and U cubed = -I',near(U.conj().T@U,I2) and near(np.linalg.matrix_power(U,3),-I2))
ck('U implements exact 3-cycle of Pauli axes',all(near(U@p@U.conj().T,pa[cyc[j]]) for j,p in enumerate(pa)))
ops=np.array([np.kron(np.kron(pa[a],pa[b]),pa[c]) for a,b,c in product(range(4),repeat=3)])
ck('64 Pauli operators orthogonal',near(np.einsum('aij,bij->ab',ops.conj(),ops),8*np.eye(64)))
ck('all 64 operator labels cycle with same T',near(U3@ops@U3.conj().T,ops[T]))
ck('core U3 conjugation has order three',near(np.linalg.matrix_power(U3,3),-np.eye(8)))
for j in range(5):
 z=rng.normal(size=8)+1j*rng.normal(size=8);z/=np.linalg.norm(z);rho=np.outer(z,z.conj());p=np.einsum('aij,ji->a',ops,rho).real
 ck(f'Pauli three-axis read reconstructs pure core {j}',near(np.einsum('a,aij->ij',p,ops)/8,rho) and near(p@p,8))
 rt=sum(np.linalg.matrix_power(U3,k)@rho@np.linalg.matrix_power(U3,k).conj().T for k in range(3))/3
 ck(f'projective twirl {j} positive trace one and rank <=3',np.linalg.eigvalsh(rt).min()>-1e-10 and near(np.trace(rt),1) and np.linalg.matrix_rank(rt,tol=1e-9)<=3)
 ck(f'projective twirl {j} equals Pauli orbit averages',near(np.einsum('aij,ji->a',ops,rt),Q@p))
vals=np.linalg.eigvals(U3); mult=[np.count_nonzero(np.abs(vals-a)<1e-9) for a in [-1,np.exp(1j*np.pi/3),np.exp(-1j*np.pi/3)]]
ck('U3 eigenspaces 2,3,3 give commutant 22',mult==[2,3,3] and sum(x*x for x in mult)==22)
# Physical spatial C3 rotates axes, NOT the same three-cycle of Pauli labels.
rot=[((i&1)<<2)|(i>>1) for i in range(8)]; Rsp=np.eye(8)[:,rot]
ck('spatial C3 has two fixed corners and two triples',np.trace(Rsp)==2 and near(np.linalg.matrix_power(Rsp,3),np.eye(8)))
ck('spatial C3 conjugation invariant dimension 24 not 22',(64+2*int(np.trace(Rsp))**2)//3==24)
# Native H from actual 36-component geometry (only load construction, not old verifier).
ns={};exec((P/'verify_coupled_origins.py').read_text().split("ck('33 original geometric positions;")[0],ns)
H,d,S,base,tiles=[ns[k] for k in ('H','d','S','base','tiles')]; lookup={v:i for i,(_,v) in enumerate(tiles)}
perm=[lookup[frozenset(tuple(-np.array(v)) for v in vs)] for _,vs in tiles]; Inv=np.zeros((d,d),int);Inv[perm,np.arange(33)]=1;Inv[33:,33:]=-np.eye(3,dtype=int)
order=[next(i for i,s in enumerate(S) if tuple(s)==tuple(1-2*((j>>np.arange(3))&1))) for j in range(8)]; Emb=np.eye(d)[:,np.array(base)[order]]; inv8=Emb.T@Inv@Emb
ck('native inversion symmetry',np.array_equal(H@Inv,Inv@H))
ck('core inversion is XXX',np.array_equal(inv8,np.kron(np.kron(X,X),X)))
ck('Pauli rotation does not commute with native inversion',not near(U3@inv8,inv8@U3))
ck('rotation converts native inversion into ZZZ',near(U3@inv8@U3.conj().T,np.kron(np.kron(Z,Z),Z)))
for time in [.1,.5,1,2,3]:
 K=Emb.T@expm(-1j*H*time)@Emb;ck(f'native core compression at t={time} commutes with inversion',near(K@inv8,inv8@K))
# A minimal controlled realization on actual cube edges: all three axis generators commute.
K3=np.zeros((8,8),complex); generators=[]
for j in range(3):
 factors=[I2]*3; factors[j]=X+Y+Z
 g=-np.kron(np.kron(*factors[:2]),factors[2]);generators.append(g);K3+=g
 off=g-np.diag(np.diag(g)); ck(f'axis {j} controlled rotation uses only existing cube bonds',np.all((Emb.T@H@Emb)[np.abs(off)>0]==-1))
ck('three controlled axis generators commute',all(near(a@b,b@a) for a in generators for b in generators))
ck('one controlled pulse implements U3',near(expm(-1j*np.pi/(3*np.sqrt(3))*K3),U3))
K36=Emb@K3@Emb.T; pulse=expm(-1j*np.pi/(3*np.sqrt(3))*K36)
ck('controlled core pulse has no external leakage',near((np.eye(d)-Emb@Emb.T)@pulse@Emb,0))
ck('controlled pulse is not bare autonomous Hamiltonian',not near(K36,H))
# The 4-level grading is flag-dependent, not selected by the symmetry alone.
coordrot=[ix(b,c,a) for a,b,c in product(range(4),repeat=3)]; Rflag=np.eye(64)[:,coordrot]; mid=np.diag(lev==2)
ck('coordinate cyclic rotation preserves projective symmetry',near(Rflag@Q,Q@Rflag))
ck('middle grading not invariant under coordinate cyclic rotation',not near(Rflag@mid@Q,mid@Q@Rflag))
# Local 4-output Pauli transform is a different read from the address FWHT.
Rpa= np.array([m.T.reshape(-1) for m in pa])/np.sqrt(2)
ck('one-axis dyadic-to-Pauli read unitary',near(Rpa.conj().T@Rpa,np.eye(4)))
RP=np.kron(np.kron(Rpa,Rpa),Rpa)
# Map row-major density matrix into interleaved three pairs of row/column bits.
inter=[8*u+v for a,b,c in product(range(4),repeat=3) for u,v in [(((a//2)<<2)|((b//2)<<1)|(c//2),((a%2)<<2)|((b%2)<<1)|(c%2))]]
ck('dyadic address interleave bijective',len(set(inter))==64)
ck('three local Pauli reads equivalent to complete Pauli basis',near(RP,np.array([m.T.reshape(-1)[inter] for m in ops])/np.sqrt(8)))
# Connect to native seven-sample history. Physical coherent read needs reference phase and known H.
C=np.array([np.eye(d)[:,[ns['idx'][i,j] for j in range(4) if j!=i]+[base[i]]]@np.array([1,1,1,6]) for i in range(4)])
scan=np.loadtxt(P/'native_walsh_sampling.csv',delimiter=',',skiprows=1); best=scan[np.argmin(scan[:,4])];dt=best[0]
Obs=np.vstack([C@expm(-1j*H*k*dt) for k in range(7)]); dec=Emb.T@np.linalg.pinv(Obs,rcond=1e-10)
ck('native history yields complete core in bit order',near(dec@Obs,Emb.T,tol=1e-8))
for j in range(6):
 psi=rng.normal(size=d)+1j*rng.normal(size=d);psi/=np.linalg.norm(psi); z=dec@Obs@psi; truth=Emb.T@psi;rho=np.outer(z,z.conj()); rtrue=np.outer(truth,truth.conj());
 out=np.sqrt(8)*RP@rho.reshape(-1)[inter]; expected=np.einsum('aij,ji->a',ops,rtrue)
 ck(f'native coherent history → three-axis phase-neutral Pauli ledger {j}',near(out,expected,tol=1e-8))
print('History sample spacing:',dt,'core decoder residual:',np.linalg.norm(dec@Obs-Emb.T,2))
print('RESULT:',n,'fresh assertions passed; prior 5417 recorded not rerun.')
# Figures: all included as both vector and raster. No synthetic data.
def save(fig,name):
 for ext in ('svg','png'): fig.savefig(P/'figures'/f'{name}.{ext}',dpi=160,bbox_inches='tight')
 plt.close(fig)
fig,ax=plt.subplots(figsize=(13,5.5),layout='constrained');ax.set_xlim(-17,64);ax.set_ylim(-.8,3.8);ax.axis('off')
colors=['#087e8b','#386cb0','#d88732','#556575']
for l,count in enumerate([1,4,16,64]):
 y=3-l;x=(np.arange(count)+.5)*64/count-.5
 if l:
  parent=(np.arange(count)//4+.5)*64/(count//4)-.5
  for xp,xc in zip(parent,x):ax.plot([xp,xc],[y+1,y],color=colors[l-1],alpha=.55,lw=.85,zorder=1)
 ax.scatter(x,[y]*count,s=[230,135,62,14][l],c=colors[min(l,3)],zorder=2)
 ax.text(-16.5,y,['Final register / 1 reader','Faces / 4 readers','Subfaces / 16 readers','Subchannels / 64 addresses'][l],fontsize=11,weight='bold')
ax.text(32,-.48,'Read upward: 16 × 3 fine details + 4 × 3 intermediate details + 1 × 3 coarse details + 1 common scalar = 64',ha='center',fontsize=12)
ax.set_title('Three nested sub-reads — one reversible closure',fontsize=17,weight='bold');save(fig,'44_three_subread_tree')
fig,ax=plt.subplots(1,3,figsize=(13,4.4),layout='constrained')
for a,z,title in zip(ax,[B,D,F],['Hierarchical read B','Within-detail mixing D','Complete Walsh F = DB']):
 a.imshow(z,cmap='RdBu_r',vmin=-.5,vmax=.5);a.set(title=title,xlabel='Input coordinate',ylabel='Output coordinate')
fig.suptitle('Exact factorization: tree read ≠ full FWHT until the detail mixing is applied',fontsize=14);save(fig,'45_three_subread_factorization')
fig,ax=plt.subplots(1,2,figsize=(11,4.3),layout='constrained');a=ax[0];a.set_aspect('equal');a.axis('off');a.set(xlim=(-1.4,1.4),ylim=(-1.2,1.4));pts=np.array([[0,1],[-.866,-.5],[.866,-.5]])
for i,(p,q) in enumerate(zip(pts,np.roll(pts,-1,axis=0))):a.annotate('',xy=q*.8+p*.2,xytext=p*.8+q*.2,arrowprops=dict(arrowstyle='->',lw=2,color='#087e8b'))
for p,label in zip(pts,['X','Z','Y']):a.scatter(*p,s=950,c='#386cb0');a.text(*p,label,ha='center',va='center',color='white',weight='bold',fontsize=15)
a.text(0,0,'I fixed',ha='center',va='center',fontsize=13);a.set_title('One-axis Pauli cycle');a=ax[1];a.bar(['Identity','U3 orbit','Spatial C3'],[64,22,24],color=['#556575','#087e8b','#d88732']);a.set(ylabel='Invariant operator-space dimension',ylim=(0,70),title='Distinct rotations, distinct reads');
for i,v in enumerate([64,22,24]):a.text(i,v+1,str(v),ha='center')
fig.suptitle('Coherent internal rotation is not a rigid spatial rotation');save(fig,'46_pauli_cycle_obstruction')
fig,ax=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');a=ax[0];a.bar(['Coarse','Intermediate','Fine'],[3,12,48],label='Raw details',color='#386cb0');a.bar(['Coarse','Intermediate','Fine'],[1,4,16],label='Invariant details',color='#087e8b');a.set(ylabel='Dimension',title='63 raw details → 21 invariant contrasts');a.legend();a=ax[1];exps=[1,3,21,63];a.bar(['Single contrast','Three serial\nreads*','21-mode\ndeterminant','63-mode\ndeterminant'],[-k*np.log10(alpha) for k in exps],color=['#556575','#556575','#087e8b','#d88732']);a.set(ylabel='−log10(intensity factor)',title='Attenuation depends on what is read');a.tick_params(axis='x',labelsize=9);a.text(.02,.96,'*If independently attenuated per stage',transform=a.transAxes,va='top',fontsize=9)
fig.suptitle('Conditional attenuation: no single-mode response equals a collective determinant');save(fig,'47_three_subread_attenuation')

fig,ax=plt.subplots(figsize=(11,6),layout='constrained');ax.axis('off');ax.set(xlim=(0,10),ylim=(0,10));
for y,title,detail,fc in [(8.8,'Native 36-coordinate vortex state','Four coherent histories → eight core amplitudes','#e3edf7'),(6.8,'Phase-neutral core record','ρ = zz†  ·  64 real Hermitian coordinates','#e3edf7'),(4.8,'Three local Pauli reads','4 × 4 × 4  ·  exact basis conversion','#d8f0ec'),(2.8,'Threefold conjugation / orbit average','22 invariant coordinates  ·  identity + 21 contrasts','#d8f0ec'),(.8,'Conditional collective optical read','α²¹ if all 21 contrast modes enter a determinant','#fae8d3')]:
 ax.add_patch(FancyBboxPatch((1,y-.65),8,1.3,boxstyle='round,pad=.08',facecolor=fc,edgecolor='#536777',linewidth=1.1));ax.text(5,y+.2,title,ha='center',weight='bold',fontsize=12);ax.text(5,y-.25,detail,ha='center',fontsize=10.5)
 if y>.9:ax.annotate('',xy=(5,y-1.28),xytext=(5,y-.7),arrowprops=dict(arrowstyle='->',color='#536777',lw=1.7))
ax.set_title('One candidate engine: native read, recursive resolution, collective closure',fontsize=14,weight='bold');save(fig,'48_native_recursive_read')
