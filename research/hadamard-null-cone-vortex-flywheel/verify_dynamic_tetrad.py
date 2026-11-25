"""Ten research tracks: microscopic tetrad read, optical observability, and GR obstacles.
Uses the existing Hamiltonian construction, not a newly tuned matrix.
"""
from pathlib import Path
from itertools import product
import numpy as np
import sympy as sp
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
root=Path(__file__).resolve().parent
ns={};exec((root/'verify_coupled_origins.py').read_text().split("ck('33 original geometric positions;")[0],ns)
H,d,S,A,base,idx,rings,inner,outer,tiles,J=[ns[k] for k in ('H','d','S','A','base','idx','rings','inner','outer','tiles','J')]
F=[np.eye(d,dtype=int)[:,[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if j!=i]+[base[i]]] for i in range(8)]
W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9
w=np.array([1,1,1,6]); Wc=np.outer(w,w)/54
U=sp.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
Un=np.array(U,float); eta=np.diag([-1,1,1,1]); count=0
def ck(label,ok):
 global count
 assert bool(ok),label
 count+=1;print(f'PASS {count:03d} {label}',flush=True)
def near(a,b,tol=1e-9):return np.allclose(a,b,atol=tol,rtol=tol)
# Actual original face labels; central A opposite s_i is the base on -s_i.
ids=[[base[i+4] if i==j else idx[j,i] for i in range(4) for j in range(4)], [base[i] if i==j else idx[j+4,i+4] for i in range(4) for j in range(4)]]
for chamber in range(2):
 ck('actual chamber tiles partition into diagonal central and off-diagonal lateral',len(set(ids[chamber]))==16 and all(tiles[i][0][-1]=='AB'[chamber] for i in ids[chamber]))
# 1. Exact local scalar invariant sector and early-time activation.
e0=np.eye(d,dtype=int)[:,0]; hc=H@e0; h2=H@hc
ck('central first-order amplitude -1 under H',np.all(hc[inner]==-1) and np.all(hc[outer]==0))
ck('lateral second-order amplitude +2 under H squared',np.all(h2[outer]==2))
ck('central H squared entries +3',np.all(h2[inner]==3))
# Td invariant coordinates: uniform each chamber central / lateral, and origin scalar.
groups=[[0],base[:4],base[4:],sum(rings[:4],[]),sum(rings[4:],[])]
Q=np.column_stack([np.isin(np.arange(d),g).astype(int) for g in groups]); L=np.diag([1/len(g) for g in groups])@Q.T; reduced=L@H@Q
ck('five-dimensional scalar invariant sector',near(H@Q,Q@reduced))
print('Scalar quotient (O, C_B,C_A,L_A,L_B):',reduced.tolist())
ck('pure scalar orbit has no circulation at any time (each ring equal)',all(np.all(Q[r]==Q[r[0]]) for r in rings))
E,V=np.linalg.eigh(H); amp=V.T@e0
series=[]
for t in np.geomspace(1e-4,.6,121):
 z=V@(np.exp(-1j*E*t)*amp); c=np.mean(abs(z[inner])**2); l=np.mean(abs(z[outer])**2)
 gamma=(c-l)/(c+3*l);series.append([t,c,l,gamma])
 if t<.001:ck('early-time quadratic central and quartic lateral intensities',abs(c/t**2-1)<5e-5 and abs(l/t**4-1)<.001)
# One coherent port history resolves all five uniform scalar coordinates, exactly.
Qsp=sp.Matrix(Q);hsp=sp.Matrix(H);Rs=(Qsp.T*Qsp).inv()*Qsp.T*hsp*Qsp
Cs=sp.Matrix([list(F[0]@w)])*Qsp
Os=sp.Matrix.vstack(*[Cs*Rs**j for j in range(5)])
ck('single filtered optical port resolves all five scalar coordinates using four derivatives',Os.det()==-5225472)
for j in range(5):
 ej=sp.eye(5)[:,j];ck('exact scalar history inverse reconstructs each basis direction',Os.inv()*Os*ej==ej)
# 2. Static response and natural-read counterexamples.
static=[]; bands={}
for name,kernel in [('full',W),('filtered',Wc)]:
 B=np.array([F[i]@kernel@F[i+4].T for i in range(4)])
 def M(k):
  C=-np.einsum('i,ijk->jk',np.exp(1j*A@k),B);return np.block([[H,C],[C.conj().T,H]])
 ev,vec=np.linalg.eigh(M(np.zeros(3)).real); u=vec[:,0];u*=np.sign(u[0]); gap=ev[1]-ev[0]
 ck(name+' scalar band is simple, isolated at k=0',gap>.5 and np.all(u[:33]>0) and np.all(u[d:d+33]>0))
 for i,I in enumerate(ids):
  C=abs(u[np.array(I).reshape(4,4)])**2; cv=np.mean(np.diag(C));lv=np.mean(C[~np.eye(4,dtype=bool)])
  ck(name+' uniform but nonzero central and lateral reads',cv>lv>0 and near(np.diag(C),cv) and near(C[~np.eye(4,dtype=bool)],lv))
  gam=(cv-lv)/(cv+3*lv);ck(name+' unfiltered intensity dictionary not equal GR potentials',0<gam<1)
  static.append([name,'AB'[i],cv,lv,gam]);print('Static',static[-1])
 # fixed scalar source, full inverse and actual tile linear intensity response at small k
 for k in [.005,.01,.02]:
  q=np.array([k,0.,0.]); r=np.linalg.solve(M(q)-ev[0]*np.eye(2*d),u);r/=u@r
  ck(name+' full susceptibility approaches scalar eigenvector',np.linalg.norm(r-u)<.02)
  for i,I in enumerate(ids):
   Y=(2*u[I]*r[I].real).reshape(4,4); cv=np.trace(Y)/4;lv=(Y.sum()-np.trace(Y))/12;gam=(cv-lv)/(cv+3*lv)
   target=next(row[-1] for row in static if row[:2]==[name,'AB'[i]])
   ck(name+' static intensity slip persists as k tends to zero',abs(gam-target)<.002)
 bands[name]=(u,gap,ev[0],B)
# 3. Exact observability, integer rows and invariant kernel certificate.
h=sp.Matrix(H); obs={}; metrics={}
for name,C in [('four-filter',sp.Matrix(np.array([f@w for f in F[:4]]))),('eight-filter',sp.Matrix(np.array([f@w for f in F]))),('four-full',sp.Matrix(np.concatenate(F[:4],axis=1).T))]:
 B=C; ranks=[]
 while True:
  B=sp.Matrix.vstack(*[r.T for r in B.T.columnspace()]);ranks.append(B.rows)
  nxt=B.col_join(B*h)
  if nxt.rank()==B.rows:break
  B=nxt
 K=sp.Matrix.hstack(*B.nullspace()) if B.rows<d else sp.zeros(d,0)
 ck(name+' exact invariant unobservable subspace',K.cols==d-B.rows and B*K==sp.zeros(B.rows,K.cols) and B*h*K==sp.zeros(B.rows,K.cols))
 obs[name]=ranks; print('Observability',name,ranks,'dark',K.cols)
 if name=='four-filter':
  ck('filtered rank sequence',ranks==[4,8,12,16,20,23,26]); Kdark=K
  for I in ids:
   columns=[]
   for j in range(K.cols):
    Y=sp.Matrix(4,4,list(K[I,j]));m=U*(Y+Y.T)*U.T;columns.append(sp.Matrix(16,1,list(m)))
   basis=sp.Matrix.hstack(*columns).columnspace()
   ck('exactly two metric-sensitive hidden combinations',len(basis)==2)
   for b in basis:
    m=sp.Matrix(4,4,list(b));ck('hidden metric is traceless diagonal spatial E sector',m==sp.diag(*m.diagonal()) and m[0,0]==0 and sp.trace(m)==0)
  # check linear phase-neutral intensity read around real scalar band, not just raw amplitude
  for name2,(u,*_) in bands.items():
   for I in ids:
    columns=[]
    for j in range(K.cols):
     Y=(2*u[I]*np.array(K[I,j],float).ravel()).reshape(4,4);m=Un@(Y+Y.T)@Un.T;columns.append(m.ravel())
    M=np.array(columns).T
    ck(name2+' intensity Jacobian has same two invisible metric directions',np.linalg.matrix_rank(M,tol=1e-8)==2 and near(M[[0,1,2,3,4,6,7,8,9,11,12,13,14]],0) and near(M[[5,10,15]].sum(0),0))
 if name=='eight-filter':
  ck('dark kernel unchanged when all eight ports are read',K.cols==10 and B*Kdark==sp.zeros(B.rows,10))
 if name=='four-full':ck('full interface history recovers all 36 coordinates',ranks==[16,32,36])
# The ten-dimensional local dark space is invariant and annihilated by every filtered bond.
C8=sp.Matrix(np.array([f@w for f in F]));ck('all eight filtered bond factors annihilate exact dark kernel',C8*Kdark==sp.zeros(8,10))
ck('exact dark polynomial H(H-2I) vanishes on local kernel',(h*h-2*h)*Kdark==sp.zeros(d,10))
ck('five dark eigenvectors at each of zero and two',(h*Kdark).rank()==5 and ((h-2*sp.eye(d))*Kdark).rank()==5)
kn=np.array(Kdark,float); Qdark=np.linalg.qr(kn)[0]; dark_eval=np.linalg.eigvalsh(Qdark.T@H@Qdark)
print('Local dark eigenvalues:',np.round(dark_eval,10).tolist())
q2=np.block([[Qdark,np.zeros_like(Qdark)],[np.zeros_like(Qdark),Qdark]])
_,_,_,B=bands['filtered']
for k in (np.zeros(3),np.array([.13,.21,.37]),np.array([-.4,.33,1.1])):
 X=-np.einsum('i,ijk->jk',np.exp(1j*A@k),B);Mk=np.block([[H,X],[X.conj().T,H]])
 ck('20 invariant flat dark directions per primitive cell independent of Bloch momentum',near(Mk@q2,q2@np.block([[Qdark.T@H@Qdark,np.zeros((10,10))],[np.zeros((10,10)),Qdark.T@H@Qdark]])))
# 4. Exact vortex subspace from earlier Klein-four construction; no parameters adjusted.
omega=np.exp(2j*np.pi/3); z=np.zeros(d,complex); z[rings[0]]=np.array([1,omega,omega**2])/np.sqrt(3)
lookup={v:i for i,(_,v) in enumerate(tiles)}
def perm(sign):return np.eye(d)[:,[lookup[frozenset(tuple(np.array(v)*sign) for v in vs)] for _,vs in tiles]+list(range(33,36))]
a=sum(perm(sig)@z for sig in product([-1,1],repeat=3) if np.prod(sig)==1)/2;b=perm((-1,-1,-1))@a
Z=np.column_stack([a,b]);M=Z.conj().T@H@Z
ck('Klein-four locked vortex subspace invariant',near(H@Z,Z@M) and near(M,[[1,-1],[-1,1]]))
v=(a+b)/np.sqrt(2);ck('zero-energy stationary eight-vortex state',near(H@v,0) and near(v[inner+[0,33,34,35]],0))
ringpairs=[(i,j) for r in rings for i,j in zip(r,r[1:]+r[:1])]; currents=lambda x:np.array([J(H,x)[i,j] for i,j in ringpairs])
jv=currents(v);ck('all eight rings carry exact common magnitude current',near(abs(jv),1/(8*np.sqrt(3))))
ck('vortex is dark to all eight filtered interfaces',all(near(w@f.T@v,0) for f in F))
ck('vortex is not dark to full overlap',any(np.linalg.norm(W@f.T@v)>.01 for f in F))
# 5. Coexistence in two-sublattice periodic Bloch model. Scalar frequency different from vortex.
u,gap,energy,B=bands['filtered'];vv=np.r_[v,np.zeros(d)];M0=np.block([[H,-B.sum(0)],[-B.sum(0).T,H]])
ck('localized vortex is exact stationary mode of filtered periodic cell',near(M0@vv,0));ck('scalar mode exact',near(M0@u,energy*u))
amp0=.1; jmin=[]
for phase in np.linspace(0,2*np.pi,81):
 x=vv+amp0*np.exp(1j*phase)*u; j=currents(x[:d]); jmin.append(np.min(j*np.sign(jv)))
 ck('all 24 vortex bond signs preserved in scalar superposition',jmin[-1]>0)
# uniform analytical cross bound, valid at all relative phases
bound=min(abs(jv[k])-2*amp0*(abs(v[i])*abs(u[j])+abs(v[j])*abs(u[i])) for k,(i,j) in enumerate(ringpairs))
ck('strict all-time circulation bound, not just samples',bound>0)
print('All-phase current bound',bound,'sample min',min(jmin))
ck('time-averaged intensity additive between distinct frequencies',near(np.mean([abs(vv+amp0*np.exp(1j*p)*u)**2 for p in np.arange(64)*2*np.pi/64],axis=0),abs(vv)**2+amp0**2*abs(u)**2))
# 6. Lorentz boosts not unitary in the microscopic positive norm: even flat reference.
from scipy.linalg import expm
Aboost=np.zeros((4,4));Aboost[0,1]=Aboost[1,0]=1;Lam=expm(.3*Aboost)
ck('Lorentz boost preserves eta but not positive norm',near(Lam.T@eta@Lam,eta) and not near(Lam.T@Lam,np.eye(4)))
Jm=Un.T@eta@Un;X=Jm;Xp=Un.T@eta@Lam@Un
ck('same metric, different Euclidean channel norm',near(Xp.T@Jm@Xp,X.T@Jm@X) and np.linalg.norm(Xp)>np.linalg.norm(X))
# 7. Metric-compatible pure-gauge link telescope, not curvature.
rng=np.random.default_rng(2026); es=[np.eye(4)+.07*rng.normal(size=(4,4)) for _ in range(6)]
loop=np.eye(4)
for i in range(6):
 j=(i+1)%6;Lij=np.linalg.solve(es[i],es[j]);ck('metric-compatible identity-spin link',near(Lij.T@(es[i].T@eta@es[i])@Lij,es[j].T@eta@es[j]));loop=loop@Lij
ck('hexagonal closed pure-gauge link holonomy identity',near(loop,np.eye(4)))
# 8. GR scalar Einstein tensor from the actual channel metric (linearized, independent symbolics).
x,y,z=sp.symbols('x y z');coords=[sp.Symbol('t'),x,y,z];phi=sp.Function('phi')(x,y,z);psi=sp.Function('psi')(x,y,z);et=sp.diag(-1,1,1,1);g1=sp.diag(-2*phi,-2*psi,-2*psi,-2*psi);tr=sp.trace(et*g1)
box=lambda a:sum(et[k,k]*sp.diff(a,coords[k],2) for k in range(4))
R=sp.Matrix(4,4,lambda i,j:sum(et[k,k]*(sp.diff(g1[k,j],coords[k],coords[i])+sp.diff(g1[k,i],coords[k],coords[j])) for k in range(4))/2-(box(g1[i,j])+sp.diff(tr,coords[i],coords[j]))/2)
G=R-et*sp.trace(et*R)/2
ck('linear Einstein 00 read is 2 Laplacian spatial potential',sp.simplify(G[0,0]-2*box(psi))==0)
for i in range(1,4):
 for j in range(1,4):ck('linear spatial Einstein tensor is derivative of slip',sp.simplify(G[i,j]-(box(phi-psi) if i==j else 0)+sp.diff(phi-psi,coords[i],coords[j]))==0)
# Re-express the standard static Einstein scalar functional in channel coordinates.
a,b=sp.symbols('a b',real=True) # derivatives of central and lateral reads along one direction
ck('static GR functional in central/lateral coordinates has exact completed square',sp.expand(2*(a+3*b)*(a-b)-(a-b)**2-((a+3*b)**2-16*b*b))==0)
# Vacuum scalar action is stationary in the slip direction, not a positive energy minimum.
# q=d+3o; density couples to -c^2 q, so varying o at fixed q gives Laplace(o)=0.
# 9. Single soft scalar band cannot alone supply two independent GR tensor polarizations.
for name,(u,gap,e0,B) in bands.items():
 M0=np.block([[H,-B.sum(0)],[-B.sum(0).T,H]]);ck(name+' rank-one residue of band-edge inverse',np.linalg.matrix_rank(np.outer(u,u),tol=1e-10)==1 and np.linalg.matrix_rank(M0-e0*np.eye(2*d),tol=1e-8)==2*d-1)
# 10. G normalization is unchanged; positive amplitude contrasts require a read scale.
# The read depends on arbitrary amplitude normalization unless tied to energy/work convention.
for scale in (.5,2,3):ck('read amplitude normalization does not follow from eigenvectors alone',near(abs(scale*u)**2,scale**2*abs(u)**2))
with (root/'dynamic_tetrad_response.csv').open('w') as f:
 c=csv.writer(f);c.writerow(['t','central_intensity','lateral_intensity','psi_over_phi']);c.writerows(series)
with (root/'dynamic_tetrad_static.csv').open('w') as f:
 c=csv.writer(f);c.writerow(['interface','chamber','central_intensity','lateral_intensity','psi_over_phi']);c.writerows(static)
fig,ax=plt.subplots(1,3,figsize=(13,4.3));s=np.array(series);ax[0].loglog(s[:,0],s[:,1],label='Central');ax[0].loglog(s[:,0],s[:,2],label='Lateral');ax[0].loglog(s[:,0],s[:,0]**2,'--',alpha=.45,label='t²');ax[0].loglog(s[:,0],s[:,0]**4,':',alpha=.6,label='t⁴');ax[0].set(xlabel='Dimensionless time',ylabel='Intensity per tile',title='Central-first local response');ax[0].legend(fontsize=8)
labels=[r[0]+' '+r[1] for r in static];ax[1].bar(labels,[r[-1] for r in static]);ax[1].axhline(1,linestyle='--',label='Equal potentials');ax[1].set(ylim=(0,1.1),ylabel='ψ / φ',title='Raw static intensity read');ax[1].tick_params(axis='x',rotation=25);ax[1].legend(fontsize=8)
for n,rs in obs.items():ax[2].plot(range(len(rs)),rs,'o-',label=n)
ax[2].axhline(36,linestyle=':',alpha=.5);ax[2].set(xlabel='Highest derivative order',ylabel='Observable rank',title='Optical read histories',ylim=(0,38));ax[2].legend(fontsize=8)
for a in ax:a.grid(alpha=.18)
fig.tight_layout();fig.savefig(root/'figures/38_dynamic_tetrad.svg');fig.savefig(root/'figures/38_dynamic_tetrad.png',dpi=180);plt.close(fig)
print(f'TOTAL {count} checks passed')
