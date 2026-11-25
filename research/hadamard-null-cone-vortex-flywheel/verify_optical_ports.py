"""Exact optical channel decomposition and dimensionless reciprocal network witness.
No change to historical H or full area kernel; central-only link is an explicit alternative.
"""
from pathlib import Path
from itertools import product, permutations
import numpy as np
import sympy as sp
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import expm_multiply
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
src=(root/'verify_coupled_origins.py').read_text(); marker="ck('33 original geometric positions;"
assert src.count(marker)==1
ns={'__file__':str(root/'verify_coupled_origins.py')};exec(compile(src.split(marker)[0],ns['__file__'],'exec'),ns)
A,S,H,O,d,idx,base,rings,tiles,V,J=[ns[k] for k in ('A','S','H','O','d','idx','base','rings','tiles','V','J')]
checks=[]
def ck(s,b):
 assert bool(b),s
 checks.append(s);print(f'PASS {len(checks):03d} {s}',flush=True)
def near(a,b,tol=2e-9):return np.allclose(a,b,atol=tol,rtol=tol)
I=sp.eye; h=sp.Matrix(H); pairs=[(i,j) for i in range(4) for j in range(4) if i!=j]; B=I(d)[:,[idx[i,j] for i,j in pairs]]; C=I(d)[O,:]
R=sp.Matrix(4,12,lambda i,k:int(i==pairs[k][0])); L=sp.Matrix(4,12,lambda j,k:int(j==pairs[k][1])); Q=R/sp.sqrt(3); P=Q.T*Q; Z=I(12)-P
ck('twelve ordered non-backtracking diamond routes',len({tuple(A[i]-A[j]) for i,j in pairs})==12)
ck('one triplet per exact active Hadamard port',R*R.T==3*I(4))
ck('column read is also four triplets',L*L.T==3*I(4));ck('row-column intersection',R*L.T==sp.ones(4)-I(4))
ck('symmetric read is an isometry on bright subspace',Q*Q.T==I(4));ck('orthogonal bright and dark projectors',P*P==P and Z*Z==Z and P*Z==sp.zeros(12));ck('rank 4 bright and rank 8 dark',P.rank()==4 and Z.rank()==8)
ck('each individual input participates equally, none is individually dark',all(P[k,k]==sp.Rational(1,3) for k in range(12)))
# Invariance of read and impossibility of a diagonal 4-of-12 selector respecting all Td permutations.
orbit=set()
for perm in permutations(range(4)):
 U=sp.zeros(12);V4=sp.zeros(4)
 for k,(i,j) in enumerate(pairs):U[pairs.index((perm[i],perm[j])),k]=1
 for i in range(4):V4[perm[i],i]=1
 ck('port read equivariant under tetrahedral permutation',R*U==V4*R and U*P*U.T==P)
 orbit.add(pairs.index((perm[0],perm[1])))
ck('all 12 routes are one orbit: no invariant diagonal four-of-twelve selector',len(orbit)==12)
# Exact unfiltered local dynamical observability.
T=sp.Matrix(np.c_[np.ones(4,int),A]); Tm=sp.Matrix(np.c_[np.ones(4,int),-A]); As=sp.Matrix(A)
M2=C*h**2*B; M3=C*h**3*B
ck('origin initially dark through zero and one hop',C*B==sp.zeros(4,12) and C*h*B==sp.zeros(4,12))
ck('two-hop read is full row and column Hadamard combination',M2==T.T*R+Tm.T*L)
ck('three-hop polar read separates the two triplet copies',M3==sp.Matrix.vstack(-12*sp.ones(1,12),As.T*(-5*R+L)))
ck('two plus three hop read has rank seven',sp.Matrix.vstack(M2,M3).rank()==7)
D=sp.Matrix.hstack(*R.nullspace()); K=sp.Matrix.hstack(*sp.Matrix.vstack(R,L).nullspace())
ck('eight row-dark and five row-and-column-dark',D.shape==(12,8) and K.shape==(12,5));ck('three initially row-dark modes activate directional O', (M2*D).rank()==3)
X=B*K
for k in range(d):
 ck(f'common dark subspace invisible at O, power {k}',C*X==sp.zeros(4,5));X=h*X
ck('Cayley-Hamilton: exactly five permanently origin-dark initial outer modes',sp.Matrix.vstack(M2,M3).nullspace()==sp.Matrix.vstack(R,L).nullspace())
# Exact Schur splitting of the measured area matrix (not a derived physical decomposition).
W=sp.Matrix([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9;e=I(4)[:,3];v=sp.Matrix([1,1,1,6]);Wc=W*e*(e.T*W*e).inv()*e.T*W; Wp=W-Wc
ck('central-mediated rank-one candidate exact',Wc==v*v.T/54 and Wc.rank()==1)
ck('central row and column unchanged',Wp*e==sp.zeros(4,1) and e.T*Wp==sp.zeros(1,4))
ck('peripheral remainder rank three',Wp.rank()==3 and W==Wc+Wp)
ck('central rank-one amplitude eigenvalue 13/18',Wc*v==sp.Rational(13,18)*v)
ck('full area kernel has no dark channels',W.rank()==4)
for u in [sp.Matrix([1,-1,0,0]),sp.Matrix([1,0,-1,0])]:
 ck('rank-one filter kills winding; unfiltered overlap transmits it',Wc*u==sp.zeros(4,1) and W*u==-sp.Rational(2,9)*u)
for p in permutations(range(3)):
 ix=list(p)+[3];ck('all local tile permutations preserve splitting',Wc[ix,ix]==Wc and Wp[ix,ix]==Wp)
# Four resonator bright coordinates p=(1,1,1,6)/sqrt(39), in actual 36-coordinate tile graph.
F=[np.eye(d)[:,[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if i!=j]+[base[i]]] for i in range(8)]
p=np.array([1,1,1,6])/np.sqrt(39); U=np.column_stack([f@p for f in F[:4]]); q=np.array(Q,float); z=np.array(Z,float); G=U@q; Bn=np.array(B,float)
ck('four normalized central-mediated resonator directions',near(U.T@U,np.eye(4)));ck('12 external inputs with exactly four independent resonator couplings',np.linalg.matrix_rank(G)==4 and near(G@z,0))
# Lossless scattering in the standard dimensionless wide-band input-output model.
# C^T C not a probability; S-I measures resonator-mediated response, not propagation in a separate waveguide.
I12=np.eye(12);I36=np.eye(d); freqs=np.linspace(-16,16,641)+.000173
rows=[];unit=rec=dark=0.; minbright=1e9; maxfull=0.;err=0.
for w in freqs:
 def scatter(g):return I12-2j*g.T@np.linalg.solve(w*I36-H+1j*g@g.T,g)
 ss=scatter(G); su=scatter(Bn); sv=np.linalg.svd(ss-I12,compute_uv=False); uv=np.linalg.svd(su-I12,compute_uv=False)
 unit=max(unit,np.max(abs(ss.conj().T@ss-I12)),np.max(abs(su.conj().T@su-I12)));rec=max(rec,np.max(abs(ss-ss.T)));dark=max(dark,np.max(abs((ss-I12)@z)));minbright=min(minbright,sv[3]);maxfull=max(maxfull,uv[-1]);err=max(err,sv[4]);rows.append([w,*sv,*uv])
ck('lossless scattering unitary across 641 sampled frequencies',unit<1e-8);ck('reciprocal scattering',rec<1e-8);ck('eight coherent dark modes have no resonator-mediated response',dark<1e-8 and err<1e-8)
ck('four bright response modes at every sampled nonsingular frequency',minbright>1e-9);ck('unfiltered 12-channel scattering can have rank twelve',maxfull>1e-3)
rows=np.array(rows);np.savetxt(root/'optical_scattering.csv',rows,delimiter=',',header='frequency,'+','.join([f'filtered_s{i+1}' for i in range(12)]+[f'unfiltered_s{i+1}' for i in range(12)]),comments='')
# Conservative network using actual eight-ring initial state of previous stage; compare full and isolated central branch.
# 2^3 primitive cells x2 complete fields; four distinct reciprocal neighbors per node.
Lcell=2;coords=list(product(range(Lcell),repeat=3));sites=[(a,b) for a in coords for b in range(2)]; lookup={s:i for i,s in enumerate(sites)};N=len(sites);sl=lambda i:slice(i*d,(i+1)*d);shifts=np.vstack([np.zeros((1,3),int),-np.eye(3,dtype=int)])
links=[]
for a in coords:
 for i,shift in enumerate(shifts):links.append((lookup[a,0],lookup[tuple((np.array(a)+shift)%Lcell),1],i))
adj=[set() for _ in sites]
for a,b,i in links:adj[a].add(b);adj[b].add(a)
ck('all sixteen fields have four actual neighbours',all(len(x)==4 for x in adj))
# circular polar pattern on outer rings from earlier Stage IX B; construct raw values directly.
init=np.zeros(N*d,complex); zz=np.array([1,1j,0])/np.sqrt(2)
# use exact historical initial state construction (the odd row-closed basis) by explicit row formula
for i,s in enumerate(S):
 for j in range(4*(i//4),4*(i//4)+4):
  if i!=j:init[idx[i,j]]=(s+3*S[j])@zz
init/=np.linalg.norm(init);ck('initial state occupies all eight outer rings',all(np.linalg.norm(init[r])>0 for r in rings));ck('initial row sums vanish',all(abs(sum(init[r]))<1e-12 for r in rings))
nb=sorted(adj[0]);far=sorted(set(range(N))-{0}-set(nb));ts=np.linspace(0,8,321);out=[]
for label,kernel in [('full',np.array(W,float)),('central',np.array(Wc,float))]:
 Hn=lil_matrix((N*d,N*d),dtype=float)
 for i in range(N):Hn[sl(i),sl(i)]=H
 for a,b,i in links:
  M=F[i+4]@kernel@F[i].T;Hn[sl(b),sl(a)]=-M;Hn[sl(a),sl(b)]=-M.T
 Hn=Hn.tocsr();ck(label+' network Hermitian', (Hn-Hn.T).nnz==0)
 Y=expm_multiply(-1j*Hn,init,start=0,stop=8,num=len(ts));res=[];en0=np.vdot(init,Hn@init).real; ne=ee=ce=0.
 for y in Y:
  yy=y.reshape(N,d);n=np.sum(abs(yy)**2,axis=1);o=np.sum(abs(yy[:,V])**2,axis=1);dy=(-1j*(Hn@y)).reshape(N,d);dn=2*np.real(np.sum(yy.conj()*dy,axis=1));ledger=np.zeros(N)
  for a,b,i in links:
   vj=2*np.imag(np.vdot(yy[b],-F[i+4]@kernel@F[i].T@yy[a]));ledger[b]+=vj;ledger[a]-=vj
  ne=max(ne,abs(n.sum()-1));ee=max(ee,abs(np.vdot(y,Hn@y).real-en0));ce=max(ce,np.max(abs(dn-ledger)));res.append([n[0],n[nb].sum(),n[far].sum(),o[0],o[nb].sum()])
 res=np.array(res);out.append(res);ck(label+' norm and energy conserved',max(ne,ee)<1e-8);ck(label+' exact local flux ledger sampled',ce<1e-9);ck(label+' transport beyond immediate shell',res[:,2].max()>1e-4);print(label,'peaks',res[:,1:].max(0),'errors',ne,ee,ce)
 if label=='central':ck('central-mediated network initial derivative does not transmit winding directly',np.linalg.norm((Hn@init)[d:])<1e-12)
np.savetxt(root/'optical_network_dynamics.csv',np.column_stack([ts,*out]),delimiter=',',header='t,'+','.join(f'{a}_{b}' for a in ('full','central') for b in ('source','first','far','source_O','first_O')),comments='')
print('SCATTER max unitarity, reciprocity, dark, fifth singular',unit,rec,dark,err,'min fourth',minbright,'max unfiltered twelfth',maxfull)
# Reproducible static figures embedded in Markdown.
fig,ax=plt.subplots(1,2,figsize=(10,4.2),layout='constrained')
for a,mat,title in [(ax[0],np.array(P,float),'Four bright coherent modes'),(ax[1],np.array(Z,float),'Eight complementary winding modes')]:
 im=a.imshow(mat,vmin=-.67,vmax=.67,cmap='RdBu_r');a.set(title=title,xlabel='Incoming channel',ylabel='Outgoing channel',xticks=[1,4,7,10],xticklabels=['P1','P2','P3','P4'],yticks=[1,4,7,10],yticklabels=['P1','P2','P3','P4']);
 for k in [2.5,5.5,8.5]:a.axhline(k,color='black',lw=.5);a.axvline(k,color='black',lw=.5)
fig.colorbar(im,ax=ax,shrink=.8,label='Projection amplitude');fig.savefig(root/'figures/29_optical_projectors.svg');plt.close(fig)
fig,ax=plt.subplots(2,1,figsize=(9,7),sharex=True,layout='constrained')
for a,rr,title in [(ax[0],rows[:,1:13],'Central-mediated optical read: rank four'),(ax[1],rows[:,13:25],'Unfiltered outer read: up to rank twelve')]:
 for k in range(12):a.semilogy(freqs,np.maximum(rr[:,k],1e-16),lw=1 if k<4 else .7,alpha=.85 if k<4 else .55)
 a.set(ylabel='Singular value of S − I',title=title,ylim=(1e-16,3));a.grid(alpha=.15)
ax[1].set_xlabel('Dimensionless frequency');fig.savefig(root/'figures/30_optical_scattering.svg');plt.close(fig)
fig,ax=plt.subplots(2,1,figsize=(9,6.4),sharex=True,layout='constrained')
for a,r,t in zip(ax,out,['Full overlap W','Isolated central-mediated branch Wc']):
 for k,lab in enumerate(['Source','Four nearest','Beyond first shell']):a.plot(ts,r[:,k],label=lab)
 a.set(title=t,ylabel='Occupation');a.legend(loc='best');a.grid(alpha=.15)
ax[-1].set_xlabel('Dimensionless time');fig.savefig(root/'figures/31_optical_network.svg');plt.close(fig)
print(f'{len(checks)}/{len(checks)} new optical-port assertions passed.')
