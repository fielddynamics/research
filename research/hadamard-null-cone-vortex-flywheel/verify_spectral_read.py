"""Exact neutral-read identities and numerical Bloch reduction of the existing SFM.
No physical source, frequency, length or acceleration calibration is inferred.
"""
from pathlib import Path
from itertools import product
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parent
src=(root/'verify_coupled_origins.py').read_text(); ns={'__file__':str(root/'verify_coupled_origins.py')};exec(src.split("ck('33 original geometric positions;")[0],ns)
A,S,H,O,d,base,idx=[ns[k] for k in ['A','S','H','O','d','base','idx']]
F=[np.eye(d)[:,[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if j!=i]+[base[i]]] for i in range(8)]
W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9;Wc=np.outer([1,1,1,6],[1,1,1,6])/54
checks=[]
def ck(name,x):
 assert bool(x),name
 checks.append(name);print(f'PASS {len(checks):03d} {name}')
def near(x,y,tol=1e-9):return np.allclose(x,y,atol=tol,rtol=tol)
rng=np.random.default_rng(342)
for i in range(32):
 a,b=(c:=rng.normal(size=4)+1j*rng.normal(size=4))[0],c[1:];N=np.vdot(c,c).real;P=2*np.real(a.conj()*b);C=(-1j*np.cross(b.conj(),b)).real
 Q=2*np.real(np.conj(b[[1,2,0]])*b[[2,0,1]])
 ck('polar and axial reads orthogonal and share finite capacity',abs(P@C)<1e-10 and P@P+C@C<=N*N+1e-10)
 ck('one chamber intensity aliases polar and quadrupole; both chambers remove alias',near(A.T@abs(a+A@b)**2/4,P+Q) and near((-A).T@abs(a-A@b)**2/4,P-Q))
 ck('opposite-intensity difference gives uncontaminated directional record',near((abs(a+A@b)**2-abs(a-A@b)**2)/2,A@P))
 # Exact coherence deficit identity, a made real by common phase.
 b=b*np.exp(-1j*np.angle(a));u,v=b.real,b.imag;aa=abs(a)**2
 ck('capacity deficit is sum of squares',near(N*N-P@P-C@C,(aa+v@v-u@u)**2+4*(u@v)**2))
# independent normalized phase example saturates bound with nonzero P and C
c=np.array([.5,1/np.sqrt(2),.5j,0]);a,b=c[0],c[1:];P=2*np.real(a.conj()*b);C=(-1j*np.cross(b.conj(),b)).real
ck('capacity equality attainable with both reads nonzero',near(P@P+C@C,1) and np.linalg.norm(P)>0 and np.linalg.norm(C)>0)
# spectral reduction
results=[];summary=[];Oa=np.array(O);Ob=Oa+d
for name,w in [('full',W),('central',Wc)]:
 B=np.array([F[i]@w@F[i+4].T for i in range(4)])
 def M(k):
  X=-np.einsum('i,ijk->jk',np.exp(1j*A@k),B);return np.block([[H,X],[X.conj().T,H]])
 M0=M(np.zeros(3)).real;e,v=np.linalg.eigh(M0);u=v[:,0];u*=np.sign(u[0]);e0=e[0];gap=e[1]-e0;R=(v[:,1:]/(e[1:]-e0))@v[:,1:].T
 ck(name+' simple lowest k=0 eigenvalue and scalar origin',gap>.5 and near(u[Oa],u[Ob]) and near(u[Oa[1:]],0))
 ck(name+' reduced resolvent identity',near((M0-e0*np.eye(2*d))@R,np.eye(2*d)-np.outer(u,u)))
 derivatives=[];curv=[];Qlist=[]
 for j in range(3):
  X=-np.einsum('i,ijk->jk',A[:,j],B);Q=np.block([[np.zeros_like(H),X],[-X.T,np.zeros_like(H)]]);Qlist.append(Q);w1=-R@Q@u;derivatives.append(w1)
  X2=np.einsum('i,ijk->jk',A[:,j]**2,B);M2=np.block([[np.zeros_like(H),X2],[X2.T,np.zeros_like(H)]]);curv.append(u@M2@u/2-u@Q@w1)
  ck(name+' first-order eigenvector equation',near((M0-e0*np.eye(2*d))@w1,-Q@u))
 J=np.array(derivatives).T;beta=np.trace(J[Oa[1:]])/3;D=np.mean(curv);alpha=u[0]
 ck(name+' polar response isotropic on both sublattices',near(J[Oa[1:]],beta*np.eye(3)) and near(J[Ob[1:]],beta*np.eye(3)) and near(J[[0,d]],0) and beta>0)
 ck(name+' positive isotropic diagonal stiffness',D>0 and near(curv,D))
 # independent mixed Hessian calculation
 for j,k in [(0,1),(0,2),(1,2)]:
  X2=np.einsum('i,ijk->jk',A[:,j]*A[:,k],B);M2=np.block([[np.zeros_like(H),X2],[X2.T,np.zeros_like(H)]]);mixed=u@M2@u-u@Qlist[j]@J[:,k]-u@Qlist[k]@J[:,j]
  ck(name+' mixed Hessian vanishes',abs(mixed)<1e-10)
 # full inverse, projected scalar susceptibility, and actual polar component
 for direction in [np.eye(3)[0],np.array([1,1,0])/np.sqrt(2),np.ones(3)/np.sqrt(3)]:
  for k in np.geomspace(.003,.55,35):
   kv=k*direction;Mk=M(kv);ev=np.linalg.eigvalsh(Mk);delta=ev[0]-e0
   x=np.linalg.solve(Mk-e0*np.eye(2*d),u);chi=(u@x).real;z=x/chi;pred=1j*beta*kv;err=np.linalg.norm(z[Oa[1:]]-pred)/np.linalg.norm(pred)
   results.append([name,*direction,k,delta/k**2,D*k*k*chi,err])
  ck(name+' exact full-matrix inverse has scalar 1/k² pole and polar gradient limit',abs(results[-35][-2]-1)<1e-4 and results[-35][-1]<.01 and abs(results[-35][-3]/D-1)<1e-4)
 # finite standing-wave construction: scalar background plus real ±k forced response.
 k=.015;direction=np.ones(3)/np.sqrt(3);kv=k*direction
 x=np.linalg.solve(M(kv)-e0*np.eye(2*d),u);z=x/(u@x);eps=.05
 for t in np.linspace(0,2*np.pi,13):
  state=u+eps*np.real(z*np.exp(1j*t));a=state[0];b=state[Oa[1:]];p=2*a*b
  pred=-alpha*beta*2*eps*k*np.sin(t)*(1+eps*np.cos(t))*direction
  ck(name+' static real standing-wave polar read equals gradient of envelope intensity to leading order',np.linalg.norm(p-pred)<.025*(2*alpha*beta*eps*k))
 summary.append([name,e0,gap,alpha,beta,D,alpha*beta,2*alpha*beta/D])
 print('PARAMETERS',summary[-1])
 # sampled stability, not a theorem of global band minimum
 minimum=min(np.linalg.eigvalsh(M(np.array(k)))[0]-e0 for k in product(np.linspace(-np.pi/2,np.pi/2,7),repeat=3))
 ck(name+' sampled band minimum not below k=0',minimum>-1e-9);print('sampled min shift',minimum)
# Conditional neutral work-coupling continuum example: uniform sphere of radius 1.
# Units K=f0=1, eta*rho=q^2. No empirical constants inferred.
for q in (.001,.03,.2,.7,1.2):
 R0=1.;f0=1.;B0=np.tan(q)/q-1;A0=1/(q*np.cos(q))
 ck('uniform sphere interior/exterior value and derivative match',near(A0*np.sin(q),1+B0) and near(A0*(q*np.cos(q)-np.sin(q)),-B0))
 ck('weak source positive charge and inward exterior read',B0>0 and -2*B0*(1+B0/2)/4<0)
ck('uniform sphere weak-source charge coefficient',near((np.tan(.001)/.001-1)/(.001**2),1/3,1e-6))
import csv
with (root/'spectral_read_response.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['kernel','ux','uy','uz','k','delta_over_k2','Dk2chi','polar_relative_error']);w.writerows(results)
with (root/'spectral_read_parameters.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['kernel','E0','gap','alpha','beta','D','alpha_beta','linear_response_ratio_2alpha_beta_over_D']);w.writerows(summary)
fig,ax=plt.subplots(1,3,figsize=(13,4))
for name,*rest in summary:
 r=np.array([row[1:] for row in results if row[0]==name and row[1]==1]);k=r[:,3];ax[0].semilogx(k,r[:,4],label=name);ax[1].semilogx(k,r[:,5],label=name);ax[2].loglog(k,r[:,6],label=name)
ax[0].set(xlabel='Wave number k (lattice units)',ylabel='(E(k)−E₀)/k²',title='Microscopic scalar stiffness');ax[1].set(xlabel='Wave number k',ylabel='D k² χ(k)',title='Static inverse-Laplacian pole');ax[2].set(xlabel='Wave number k',ylabel='Relative error',title='Directional origin gradient read')
for a in ax:a.legend();a.grid(alpha=.2)
fig.tight_layout();fig.savefig(root/'figures/33_spectral_read.svg');fig.savefig(root/'figures/33_spectral_read.png',dpi=170);plt.close(fig)
print(f'{len(checks)}/{len(checks)} spectral-read checks passed.')
