"""Phase-neutral Field Origin read and conditional static potential bridge.
Reuses the existing geometry/H prefix only; not a physical calibration.
"""
from pathlib import Path
from itertools import product, permutations
import numpy as np
import sympy as sp
from scipy.linalg import expm
from scipy.sparse import coo_matrix
from scipy.optimize import root as solve
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
src=(root/'verify_coupled_origins.py').read_text(); marker="ck('33 original geometric positions;"
ns={'__file__':str(root/'verify_coupled_origins.py')};exec(compile(src.split(marker)[0],ns['__file__'],'exec'),ns)
A,S,T,H,O,d,base,idx,rings=[ns[k] for k in ('A','S','T','H','O','d','base','idx','rings')]
checks=[]
def ck(label,b):
 assert bool(b),label
 checks.append(label); print(f'PASS {len(checks):03d} {label}',flush=True)
def near(a,b,tol=1e-10):return np.allclose(a,b,atol=tol,rtol=tol)
def read(c):return 2*np.real(np.conj(c[0])*c[1:])
def axial(c):return (-1j*np.cross(c[1:].conj(),c[1:])).real
rng=np.random.default_rng(20261124)
# Exact all-eight-face moment identity, coefficients of c* c.
for j in range(3):
 E=np.zeros((4,4),int);E[0,j+1]=E[j+1,0]=8
 ck('exact polar intensity moment matrix',np.array_equal(T.T@np.diag(S[:,j])@T,E))
ck('exact mean occupation matrix',np.array_equal(T.T@T,8*np.eye(4)))
for _ in range(12):
 c=rng.normal(size=4)+1j*rng.normal(size=4); p=read(c)
 ck('neutral polar read of reconstructed records',near(S.T@abs(T@c)**2/8,p))
 ck('phase and conjugation invariance',near(read(c*np.exp(.71j)),p) and near(read(c.conj()),p))
 ck('polar/axial inversion and time reversal',near(read(c*np.array([1,-1,-1,-1])),-p) and near(axial(c*np.array([1,-1,-1,-1])),axial(c)) and near(axial(c.conj()),-axial(c)))
 ck('neutral read magnitude bound',np.linalg.norm(p)<=np.vdot(c,c).real+1e-12)
ck('circular pure triplet can circulate with zero polar intensity read',near(read(np.array([0,1,1j,0])/np.sqrt(2)),0) and near(axial(np.array([0,1,1j,0])/np.sqrt(2)),[0,0,1]))
# actual Stage IX cell with Flower interface, full and central branch
F=[]
for i in range(8):
 ids=[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if j!=i]+[base[i]]
 F.append(np.eye(d,dtype=int)[:,ids])
W9=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]],int);Wc54=np.outer([1,1,1,6],[1,1,1,6]);O2=np.array(O)+d
rows=[]
for name,K,den in [('full',6*W9,54),('central',Wc54,54)]:
 for i,s in enumerate(A):
  B=F[i+4]@K@F[i].T; M=np.block([[den*H,-B.T],[-B,den*H]])
  n1=np.r_[1,s];n2=np.r_[1,-s]; M3=M@M@M
  ck(name+' exact third-order origin read',np.array_equal(M3[np.ix_(O2,O)],-(den**3*2//3)*np.outer(n2,n1)))
  c0=np.array([1,.1j,.15,-.2j]);x=np.zeros(2*d,complex);x[O]=c0; x/=np.linalg.norm(x);a=n1@x[O]
  target=-2*abs(a)**2*s/81
  for t in [.002,.004,.008,.016,.032,.064]:
   y=expm(-1j*t*M/den)@x; p=read(y[O2]);err=np.linalg.norm(p/t**6-target)/np.linalg.norm(target)
   rows.append([name,i,t,*p/t**6,err])
  ck(name+' receiving read points toward source at early time',err<.25 and np.dot(p,s)<0)
  ck(name+' predicted t^6 coefficient',rows[-6][-1]<.005)
# exact four-port gradient/mean decomposition
ell=np.sqrt(3); n=A/ell
ck('tetrahedron tight frame',np.array_equal(A.T@A,4*np.eye(3)) and near(n.sum(0),0))
for _ in range(16):
 p=rng.normal(size=3);m=rng.normal();delta=m+ell*n@p
 ck('four-port affine reconstruction',near(3/(4*ell)*n.T@delta,p) and near(delta.mean(),m))
 ck('exact quadratic read decomposition',near(delta@delta,4*m*m+4*ell**2/3*(p@p)))
# periodic diamond adjacency and variational gradient operators (dimensionless coordinates)
def lattice(L,h=1.):
 coords=list(product(range(L),repeat=3));ids={p:i for i,p in enumerate(coords)};N=2*len(coords);NB=np.empty((N,4),int); directions=np.tile(A,(N,1,1));directions[1::2]*=-1
 shifts=np.vstack([np.zeros((1,3),int),-np.eye(3,dtype=int)]);Bmat=(A[0]-A[1:]).T
 xyz=np.array([h*(Bmat@p+b*A[0]) for p in coords for b in range(2)])
 for p in coords:
  i=2*ids[p]
  for k,q in enumerate(shifts):
   j=2*ids[tuple((np.array(p)+q)%L)]+1;NB[i,k]=j;NB[j,k]=i
 return xyz,NB,directions,Bmat
xyz,NB,dirs,Bmat=lattice(4);N=len(NB);Adj=np.zeros((N,N),int)
for i in range(N):Adj[i,NB[i]]=1
Lmat=4*np.eye(N)-Adj;C=Adj[::2,1::2];FCC=C@C.T-4*np.eye(N//2,dtype=int)
ck('four reciprocal direct neighbours',np.array_equal(Adj,Adj.T) and near(Adj.sum(1),4))
ck('exact twelve second neighbours after scalar elimination',near(FCC.sum(1),12) and set(np.unique(FCC))=={0,1})
ck('Schur complement is quarter FCC Laplacian',near(Lmat[::2,::2]-C@C.T/4,(12*np.eye(N//2)-FCC)/4))
ck('one static constant gauge mode',np.count_nonzero(abs(np.linalg.eigvalsh(Lmat))<1e-10)==1)
# physical wavevector acoustic symbol, dimensionless ell=sqrt(3)
ks=np.geomspace(.002,.7,60);disp=[]
for k in ks:
 vals=[]
 for u in ([1,0,0],np.array([1,1,0])/np.sqrt(2),np.ones(3)/np.sqrt(3)):
  f=np.exp(1j*A@(k*np.array(u))).sum(); vals.append((4-abs(f))/(2*k*k))
 disp.append(vals)
ck('isotropic acoustic small-k limit',near(disp[0],np.ones(3),2e-6))
# p gradient and mean m from the four differences, all cells retained; a0=1 in numerical units.
def readgrid(phi,NB,dirs,h):
 delta=phi[NB]-phi[:,None]; return np.einsum('nki,nk->ni',dirs,delta)/(4*h),delta.mean(1)
def energygrad(phi,NB,dirs,h,drained=True):
 p,m=readgrid(phi,NB,dirs,h);r=np.linalg.norm(p,axis=1); mu=r/(1+r) if drained else np.ones_like(r)
 # E = 1/2 sum [F(r^2)+m^2/h^2], per-volume factor suppressed.
 E=np.sum((r*r-2*r+2*np.log1p(r) if drained else r*r)+m*m/h**2)/2
 t=np.einsum('nki,ni->nk',dirs,mu[:,None]*p)/(4*h)+m[:,None]/(4*h*h)
 grad=np.zeros(len(phi));np.add.at(grad,NB.ravel(),t.ravel());grad-=t.sum(1)
 return E,grad,t
for drained in (False,True):
 phi=rng.normal(size=N);direction=rng.normal(size=N);E,g,t=energygrad(phi,NB,dirs,1,drained)
 ck('constant shift gauge and global ledger',near(energygrad(phi+3,NB,dirs,1,drained)[1],g) and abs(g.sum())<1e-10)
 e=1e-5;fd=(energygrad(phi+e*direction,NB,dirs,1,drained)[0]-energygrad(phi-e*direction,NB,dirs,1,drained)[0])/(2*e)
 ck('variational gradient finite difference',near(fd,g@direction,1e-7))
 cut=np.arange(N)%3==0;flux=sum(t[i,k]*(int(cut[j])-int(cut[i])) for i in range(N) for k,j in enumerate(NB[i]))
 ck('regional static interface ledger',near(g[cut].sum(),flux))
 if not drained:ck('linear static stiffness is half diamond Laplacian',near(g,Lmat@phi/2))
# Nonlinear solve with known manufactured field and periodic zero-mean source.
k=2*np.pi*np.linalg.solve(Bmat.T,np.array([1.,1.,0.]))/4
truth=.8*np.sin(xyz@k)+.2*np.cos(2*xyz@k);truth-=truth.mean()
source=-energygrad(truth,NB,dirs,1)[1]
def residual(v):
 f=energygrad(v,NB,dirs,1)[1]+source;return f+v.mean()
sol=solve(residual,np.zeros(N),method='hybr',tol=1e-10)
# degeneracy at zero may hinder direct Newton; use linear Poisson starting point if needed
if not sol.success or np.linalg.norm(residual(sol.x))>1e-8:
 init=np.linalg.solve(Lmat/2+np.ones((N,N))/N,-source);sol=solve(residual,init,method='hybr',tol=1e-10)
ck('nonlinear periodic static solve residual',np.max(abs(residual(sol.x)))<1e-8)
ck('nonlinear manufactured potential recovered',np.max(abs(sol.x-truth))<1e-7)
# settlement functional exact gradient and stable radial Hessian, symbolic primitive
r=sp.symbols('r',positive=True);a=sp.symbols('a',positive=True);Fexpr=r*r-2*a*r+2*a*a*sp.log(1+r/a)
ck('constitutive energy derivative',sp.simplify(sp.diff(Fexpr,r)/2-r*r/(a+r))==0)
for p in (.01,.1,1.,10.,100.):
 q=p/(1+p);ck('conditional vector settlement equilibrium',near(q/(1-q),p) and near(p-q,p*p/(1+p)))
print('MAX nonlinear potential error',np.max(abs(sol.x-truth)),'residual',np.max(abs(residual(sol.x))))
np.savetxt(root/'field_read_dispersion.csv',np.c_[ks,disp],delimiter=',',header='k,axis,edge,body_diagonal',comments='')
import csv
with (root/'field_read_transfer.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['kernel','port','t','Px_over_t6','Py_over_t6','Pz_over_t6','relative_error']);w.writerows(rows)
fig,ax=plt.subplots(1,3,figsize=(12,3.8))
for name in ('full','central'):
 rr=np.array([row[2:] for row in rows if row[0]==name and row[1]==0]);ax[0].loglog(rr[:,0],rr[:,-1],marker='o',label=name)
ax[0].set(title='Origin read: leading t⁶ limit',xlabel='Dimensionless time',ylabel='Relative coefficient error');ax[0].legend()
for j,lab in enumerate(['axis','edge','body diagonal']):ax[1].semilogx(ks,np.array(disp)[:,j],label=lab)
ax[1].set(title='Static acoustic isotropy',xlabel='Wave number',ylabel='λ / (2k²)');ax[1].legend()
ax[2].scatter(truth,sol.x,s=9);v=np.linspace(truth.min(),truth.max());ax[2].plot(v,v,ls='--');ax[2].set(title='Nonlinear manufactured solution',xlabel='Prescribed potential',ylabel='Recovered potential')
fig.tight_layout();fig.savefig(root/'figures/32_field_read_bridge.svg');fig.savefig(root/'figures/32_field_read_bridge.png',dpi=170);plt.close(fig)
print(f'{len(checks)}/{len(checks)} field-read checks passed.')
