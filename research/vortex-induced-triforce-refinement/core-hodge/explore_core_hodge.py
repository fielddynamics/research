"""Discrete Hodge decomposition on the actual core mesh. Exact algebra, then conditional dynamics."""
from pathlib import Path
from itertools import combinations, permutations
import numpy as np
import sympy as sp
from scipy.linalg import eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
P=Path(__file__).resolve().parent
src=P.parent/'core-flywheel/explore_core_flywheel.py'
ns={'__file__':str(src)}
exec(src.read_text().split('# Exact identity for cubic pseudoscalar')[0],ns)
A,tiles,inner,F,parent,E2,H,W,B7,Bs,O,inter,intra=[ns[k] for k in ('A','tiles','inner','F','parent','E2','H','W','B7','Bs','O','inter','intra')]
checks=0
def ck(s,b):
 global checks
 assert bool(b),s
 checks+=1;print(f'PASS H{checks:03d} {s}',flush=True)
coarse=[frozenset(tuple(2*np.array(v)) for v in tiles[i][1]) for i in inner]; fids=[i for i,p in enumerate(parent) if p in inner]; fine=[F[i] for i in fids]
def graph(faces):
 verts=sorted(set().union(*faces)); ix={v:i for i,v in enumerate(verts)}; edges=[]; pe=[]
 for a,b in combinations(range(len(faces)),2):
  s=faces[a]&faces[b]
  if len(s)!=2:continue
  x,y=map(np.array,sorted(s)); t=np.array(next(iter(faces[a]-s)))
  if np.cross(y-x,t-x)@(x+y+t)<0:x,y=y,x
  edges.append((a,b));pe.append((ix[tuple(x)],ix[tuple(y)]))
 B=sp.zeros(len(faces),len(edges));D=sp.zeros(len(edges),len(verts))
 for e,((a,b),(x,y)) in enumerate(zip(edges,pe)):B[a,e]=1;B[b,e]=-1;D[e,x]=-1;D[e,y]=1
 return verts,edges,pe,B,D
vc,ec,pc,Bc,Dc=graph(coarse);vf,ef,pf,Bf,Df=graph(fine)
for name,v,e,b,d,counts in [('coarse',vc,ec,Bc,Dc,(6,12,8)),('fine',vf,ef,Bf,Df,(18,48,32))]:
 ck(name+' octahedral mesh counts',(len(v),len(e),b.rows)==counts)
 ck(name+' Euler sphere',len(v)-len(e)+b.rows==2)
 ck(name+' boundary of boundary zero',b*d==sp.zeros(b.rows,d.cols))
 ck(name+' connected dual graph',b.rank()==b.rows-1)
 ck(name+' connected primal graph',d.rank()==d.cols-1)
 ck(name+' every divergence-free current is a stream difference',b.cols-b.rank()==d.rank())
R=sp.zeros(12,48);U=sp.zeros(8,32);V=sp.zeros(6,18);ci={p:i for i,p in enumerate(inner)};cp=[ci[parent[i]] for i in fids]
for i,p in enumerate(cp):U[p,i]=1
for i,v in enumerate(vc):V[i,vf.index(v)]=1
for i,(a,b) in enumerate(ef):
 pa,pb=cp[a],cp[b]
 if pa!=pb:R[ec.index(tuple(sorted((pa,pb)))),i]=1 if pa<pb else -1
ck('two child fluxes per coarse edge',R*R.T==2*sp.eye(12));ck('aggregation commutes with divergence',Bc*R==U*Bf);ck('stream restriction commutes with aggregation',R*Df==Dc*V)
ck('cycle ranks 5 and 17; kernel of aggregation on cycles dimension 12',Dc.rank()==5 and Df.rank()==17 and (R*Df).rank()==5)
K=Df.T*Df;old=[vf.index(v) for v in vc];new=[i for i in range(18) if i not in old];Kmm=K.extract(new,new);X=-Kmm.inv()*K.extract(new,old);J=sp.zeros(18,6);Z=sp.zeros(18,12)
for i,o in enumerate(old):J[o,i]=1
for i,m in enumerate(new):J[m,:]=X[i,:];Z[m,i]=1
ck('Dirichlet block positive definite',all(Kmm[:i,:i].det()>0 for i in range(1,13)))
ck('harmonic extension preserves restriction',V*J==sp.eye(6));ck('harmonic and hidden loops orthogonal',(Df*J).T*Df*Z==sp.zeros(6,12));ck('12 independent hidden loops aggregate to zero',R*Df*Z==sp.zeros(12,12) and (Df*Z).rank()==12);ck('visible cycles aggregate to coarse stream',R*Df*J==Dc);ck('constant gauge preserved',J*sp.ones(6,1)==sp.ones(18,1))
Keff=J.T*K*J; L0=Dc.T*Dc
print('Kron stiffness',Keff.tolist());print('Kron spectrum',Keff.eigenvals())
for name,M in [('dipole',sp.Matrix(vc)),('quadrupole',sp.Matrix([[int(abs(v[0])==2)-int(abs(v[2])==2),int(abs(v[1])==2)-int(abs(v[2])==2)] for v in vc]))]:
 i,j=next((i,j) for i in range(M.rows) for j in range(M.cols) if M[i,j]!=0);l=(L0*M)[i,j]/M[i,j];mu=(Keff*M)[i,j]/M[i,j];ck(name+' stiffness eigenspaces exact',L0*M==l*M and Keff*M==mu*M);print(name,'coarse',l,'refined',mu,'ratio',mu/l)
def proj(b):
 b=b[:-1,:];return sp.eye(b.cols)-b.T*(b*b.T).inv()*b
Pc=proj(Bc);Pf=proj(Bf)
for name,p,b,d in [('coarse',Pc,Bc,Dc),('fine',Pf,Bf,Df)]:ck(name+' exact Hodge projection',p==p.T and p*p==p and b*p==sp.zeros(b.rows,p.cols) and p*d==d)
comm=Pc*R-R*Pf
ck('fine cycles aggregate to coarse cycles',Pc*R*Pf==R*Pf)
ck('commutator equals coarse projection of aggregated fine gradient',comm==Pc*R*(sp.eye(48)-Pf))
ck('projection and aggregation do not commute',comm.rank()==5)
# All five coarse cycles can arise from pure fine gradient currents. The nonzero
# eigenvalues are exact squared singular values, not physical coupling constants.
cc=comm*comm.T; print('gradient contamination spectrum',cc.eigenvals())
ck('exact gradient contamination spectrum',cc.eigenvals()=={sp.Rational(2,3):3,sp.Rational(2,5):2,sp.Integer(0):7})
for name,M,lam in [('dipole',sp.Matrix(vc),sp.Rational(2,3)),('quadrupole',sp.Matrix([[int(abs(v[0])==2)-int(abs(v[2])==2),int(abs(v[1])==2)-int(abs(v[2])==2)] for v in vc]),sp.Rational(2,5))]:
 J0=Dc*M;ck(name+' pure-gradient contamination spans coarse sector',cc*J0==lam*J0)
 L=comm.T*J0/lam
 ck(name+' explicit false circulation witness from a fine gradient',Pf*L==sp.zeros(48,M.cols) and Pc*R*L==J0)
# Uniform cross-boundary lift is a right inverse of aggregation, but not of circulation.
Lift=R.T/2
ck('uniform lift preserves coarse edge read',R*Lift==sp.eye(12))
ck('uniform lift of coarse cycles not necessarily divergence free',Bf*Lift*Dc!=sp.zeros(32,6))
z=np.array([1,1j,0])/np.sqrt(2);odd=[]
for p in permutations(range(4)):
 r=(A[list(p)].T@A)//4
 if round(np.linalg.det(r))==-1 and abs(np.vdot(z,r@z))>1-1e-12:odd.append(p)
ck('axis-aligned phase ray has odd stabilizer',len(odd)>0);print('odd stabilizers',odd)
# Rational real/imaginary representation of z=(1,i,0)/sqrt(2).
g=odd[0];r=(A[list(g)].T@A)//4;zz=sp.Matrix([1,sp.I,0]); phase=(sp.Matrix(r)*zz)[0]
ck('exact odd ray stabilizer, not a numerical tolerance',sp.Matrix(r)*zz==phase*zz and sp.expand(phase*sp.conjugate(phase))==1 and sp.Matrix(r).det()==-1)
print('odd ray stabilizer matrix',r.tolist(),'phase',phase)
# Fine dynamics from previous model; no new fitting.
E=E2/2;W36=np.zeros((36,36));W36[:33,:33]=np.array(W,float);D=np.zeros((132,132))
for i,j in intra:D[i,j]-=1;D[j,i]-=1;D[i,i]+=1;D[j,j]+=1
def hfine(h,k):
 f=np.zeros((132,132))
 for i,j in inter:f[i,j]=f[j,i]=2*h[parent[i],parent[j]]
 for i,p in enumerate(parent):
  f[i,i]=h[p,p]
  for j,o in enumerate(O):f[i,128+j]=f[128+j,i]=h[p,o]/2
 f[128:,128:]=h[np.ix_(O,O)];return f+k*D
fn,cn,rn,bn,dn,jn,vn=[np.array(m,float) for m in (Pf,Pc,R,Bf,Df,J,V)]
vis=dn@jn@vn@np.linalg.pinv(dn)@fn;hid=fn-vis
ck('visible and hidden cycle projectors orthogonal',np.linalg.norm(vis.T@hid)<1e-12)
n=np.array([.05,.08,1.]);n/=np.linalg.norm(n);u=np.array([1.,0,0]);u-=n*(n@u);u/=np.linalg.norm(u);z=(u+1j*np.cross(n,u))/np.sqrt(2)
scenarios=[('VII empty',W36,np.r_[B7@np.kron([1/3,1,0],z),0,0,0]),('VII stationary',W36,np.r_[B7@np.kron([1/3,1,-4/15],z),0,0,0]),('IX odd empty',H,Bs[-1]@np.kron([1/3,1,0,0],z))]
rows=[];summ=[];ts=np.linspace(0,8,201);ia=np.array([fids[a] for a,b in ef]);ib=np.array([fids[b] for a,b in ef]);out=sorted(set(range(132))-set(fids));fids=np.array(fids)
for name,h,x0 in scenarios:
 x0=x0/np.linalg.norm(x0)
 for k in [0,1,4,16,64]:
  hf=hfine(h,k);ev,vec=eigh(hf);c=vec.T@(E@x0);states=(vec@(np.exp(-1j*ev[:,None]*ts)*c[:,None])).T
  results=[];err=continuity=spliterr=falsecycle=0
  for t,y in zip(ts,states):
   I=2*np.imag(y[ia]*hf[ib,ia]*y[ib].conj());cy=fn@I;grad=I-cy;vv=vis@I;hh=hid@I
   pdot=2*np.real(y.conj()*(-1j*hf@y));outflux=2*np.imag(y[fids,None]*hf[np.ix_(fids,out)]*y[out].conj()[None,:]).sum(1)
   continuity=max(continuity,np.linalg.norm(pdot[fids]+bn@I+outflux,np.inf));err=max(err,np.linalg.norm(rn@hh));spliterr=max(spliterr,abs(I@I-grad@grad-vv@vv-hh@hh));falsecycle=max(falsecycle,np.linalg.norm(cn@rn@I-rn@cy))
   results.append([t,float(grad@grad),float(vv@vv),float(hh@hh),float(np.sum(abs(y[fids])**2)),float(outflux.sum()),float(np.linalg.norm(cn@rn@I-rn@cy))])
  ck(name+f' k={k} local continuity',continuity<2e-12);ck(name+f' k={k} orthogonal current split and invisible loop cancellation',spliterr<2e-12 and err<2e-12)
  r=np.array(results);den=r[:,2]+r[:,3];fraction=np.divide(r[:,3],den,out=np.zeros_like(den),where=den>1e-18);summ.append([name,k,r[:,1].max(),r[:,2].max(),r[:,3].max(),fraction.max(),falsecycle]);rows.extend([[name,k,*q] for q in results]);print('DIAGNOSTIC',summ[-1])
for file,header,data in [('hodge_dynamics.csv',['scenario','kappa','t','gradient_current_squared','visible_cycle_squared','hidden_cycle_squared','core_occupation','net_outflow','projection_discrepancy'],rows),('hodge_summary.csv',['scenario','kappa','peak_gradient_squared','peak_visible_squared','peak_hidden_squared','max_hidden_cycle_fraction','peak_projection_discrepancy'],summ)]:
 with open(P/file,'w') as f:w=csv.writer(f);w.writerow(header);w.writerows(data)
fig=plt.figure(figsize=(10,5),layout='constrained')
for panel,verts,primal,title in [(1,vc,pc,'Coarse: 6 stream vertices, 5 cycle modes'),(2,vf,pf,'Refined: 18 stream vertices, 17 cycle modes')]:
 ax=fig.add_subplot(1,2,panel,projection='3d');v=np.array(verts)/2
 for a,b in primal:ax.plot(*v[[a,b]].T,color='#64748b',alpha=.8,lw=1.3)
 mask=np.array([tuple(a) in vc for a in verts]);ax.scatter(*v[mask].T,color='#2563eb',s=52,label='original vertices')
 if not np.all(mask):ax.scatter(*v[~mask].T,color='#d97706',s=37,label='midpoints')
 ax.set_box_aspect((1,1,1));ax.view_init(20,35);ax.set_axis_off();ax.set_title(title,fontsize=11);ax.legend(loc='lower center',frameon=False)
fig.suptitle('Same octahedral core: five visible and twelve hidden circulation modes')
for ext in ['svg','png']:fig.savefig(P/f'core_hodge_mesh.{ext}',dpi=170)
plt.close(fig)
fig,axs=plt.subplots(3,2,figsize=(10,9),layout='constrained')
for i,(name,_,_) in enumerate(scenarios):
 for k in [1,4,16,64]:
  data=np.array([r[2:] for r in rows if r[0]==name and r[1]==k]);axs[i,0].plot(data[:,0],data[:,3],label=f'κ={k}');axs[i,1].plot(data[:,0],data[:,1],label=f'κ={k}')
 axs[i,0].set_ylabel(name);axs[i,0].legend(fontsize=8,frameon=False)
for a in axs.flat:a.set_xlabel('Dimensionless time');a.grid(alpha=.2)
axs[0,0].set_title('Hidden circulation: squared edge current');axs[0,1].set_title('Divergence-associated: squared edge current')
for ext in ['svg','png']:fig.savefig(P/f'core_hodge_dynamics.{ext}',dpi=160)
plt.close(fig)
print(f'{checks}/{checks} new Hodge checks passed; {ns["checks"]} reconstruction checks rerun')
