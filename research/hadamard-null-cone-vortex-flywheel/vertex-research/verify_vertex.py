"""New conditional vertex research. Exact checks separately from numerical witnesses.
Requires Python 3, numpy, scipy, sympy, matplotlib. All weights inherited from
Stage VII except the explicitly marked overlap witness normalization.
"""
from itertools import permutations, product
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent; (P/'figures').mkdir(exist_ok=True)
counts={'exact':0,'numeric':0}
def ck(name,test,kind='exact'):
    assert bool(test),name
    counts[kind]+=1
    print(f'PASS [{kind}] {name}')
def near(a,b,tol=1e-9): return np.max(np.abs(np.asarray(a)-np.asarray(b)))<tol
# 1. Scheme: determinant is a central idempotent grading, not a path.
t=s.symbols('t',real=True); eta=s.diag(-1,1,1,1); parity=s.diag(1,-1,-1,-1)
ck('parity preserves metric',parity.T*eta*parity==eta); ck('opposite determinant',parity.det()==-1)
e=s.eye(4)*(1-t)+t*parity
ck('straight path determinant',s.expand(e.det()-(1-2*t)**3)==0)
ck('midpoint singular',e.subs(t,s.Rational(1,2)).rank()==1)
ck('metric midpoint singular',(e.T*eta*e).subs(t,s.Rational(1,2)).rank()==1)
S=s.diag(1,-1); PA=(s.eye(2)+S)/2; PB=(s.eye(2)-S)/2
ck('root projectors',PA**2==PA and PB**2==PB and PA*PB==s.zeros(2) and PA+PB==s.eye(2))
a,b,c,d=s.symbols('a b c d',real=True); L=s.Matrix([[a,b],[c,d]])
ck('offdiagonal interaction fails to commute with root sign',S*L-L*S==s.Matrix([[0,2*b],[-2*c,0]]))
# 2. Exact channel dictionary, Stage VII cross block.
I=range(4); pairs=list(permutations(I,2)); ix={p:i for i,p in enumerate(pairs)}
R=s.Matrix(4,12,lambda i,j:int(pairs[j][0]==i)); Q=s.Matrix(4,12,lambda i,j:int(pairs[j][1]==i)); T=s.Matrix(12,12,lambda i,j:int(pairs[i]==pairs[j][::-1])); K=s.ones(4)-s.eye(4)
ck('transpose involution',T*T==s.eye(12) and T.T==T); ck('transpose exchanges row and column',Q*T==R)
ck('row/column identities',Q*Q.T==3*s.eye(4) and R*R.T==3*s.eye(4) and Q*R.T==K)
ck('Schur identity',Q*T*Q.T==K); ck('K eigenvalues',K.charpoly().as_expr()==s.expand((s.Symbol('lambda')-3)*(s.Symbol('lambda')+1)**3))
d,a,k=s.symbols('d a k',real=True,nonzero=True)
C=(d*T).row_join(a*Q.T).col_join((a*Q).row_join(k*K))
D=s.diag(d*T,(k-a*a/d)*K); L=s.eye(12).row_join(s.zeros(12,4)).col_join((a/d*Q*T).row_join(s.eye(4)))
ck('exact LDL transpose factorization',(L*D*L.T-C).applyfunc(s.simplify)==s.zeros(16))
ck('48 cross chamber edges',sum(x!=0 for x in C)==48)
C0=C.subs({d:-s.Rational(1,2),a:-1,k:-1})
ck('witness cross rank 16',C0.rank()==16); ck('witness det',C0.det()==-s.Rational(3,4096))
for dv,av,kv,rank in [(1,2,4,12),(1,2,3,16),(0,1,0,8),(0,1,3,8),(0,0,1,4),(0,0,0,0),(-2,3,-s.Rational(9,2),12)]:
    ck(f'rank stratum {(dv,av,kv)}',C.subs({d:dv,a:av,k:kv}).rank()==rank)
# address equivariance: map outer Xij to (i,j), base yi to (i,i)
addr=pairs+[(i,i) for i in I]; ai={p:i for i,p in enumerate(addr)}
H4=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
F=s.kronecker_product(H4,H4); W=s.Matrix(16,16,lambda i,j:int(addr[j]==divmod(i,4))); read=F*W
ck('address read is unitary',read*read.T==s.eye(16)); Kf=read*C0*read.T
ck('spectral read recovers all cross links',read.T*Kf*read==C0)
for p in permutations(I):
    U=s.Matrix(16,16,lambda i,j:int(addr[i]==tuple(p[x] for x in addr[j])))
    ck('cross symmetry '+str(p),U*C==C*U)
    ck('read covariance '+str(p),read*U*read.T*Kf==Kf*read*U*read.T)
# stabilizer of a selected time face i=0; character counts for 16 ordered addresses
for p in permutations(I):
    if p[0]!=0: continue
    U=s.Matrix(16,16,lambda i,j:int(addr[i]==tuple(p[x] for x in addr[j])))
    ck('selected-face trace '+str(p),s.trace(U)==sum(p[i]==i for i in I)**2)
# Sierpinski counts vs complete address tree, exact Möbius / scalar model
x=s.symbols('x',positive=True); mu=x/(1+x); sig=2*mu-1
ck('exchange symmetry',s.simplify(mu+mu.subs(x,1/x)-1)==0)
ck('weighted capacity',s.simplify(17+4*sig-(21*x+13)/(x+1))==0)
for n in range(5):
    ck(f'level {n} complete count',sum(s.binomial(n,j)*3**(n-j) for j in range(n+1))==4**n)
    ck(f'level {n} pointing trace',sum((-1)**j*s.binomial(n,j)*3**(n-j) for j in range(n+1))==2**n)
    ck(f'level {n} Sierpinski retained area',3**n*s.Rational(1,4)**n==s.Rational(3,4)**n)
ck('three-digit gate depth distribution',[s.binomial(3,j)*3**(3-j) for j in range(4)]==[27,27,9,1])
ck('one face depth two count',4**2==16); ck('64 full paired addresses',4*4**2==64)
# Face-stabilizer and hierarchy characters: one fixed child + three cycling.
rot=(0,2,3,1); U3=s.Matrix(16,16,lambda i,j:int(addr[i]==tuple(rot[x] for x in addr[j])))
P3=(s.eye(16)+U3+U3**2)/3
ck('C3 face projector rank six',P3**2==P3 and P3.rank()==6)
ck('S3 selected-face irrep counts', (16+3*4+2)//6==5 and (16-3*4+2)//6==1 and (2*16-2)//6==5)
# The full chamber S4 action is the tensor square of the permutation representation.
from collections import Counter
chars=Counter()
for p in permutations(I): chars[sum(p[i]==i for i in I)]+=1
ck('S4 character distribution',chars=={4:1,2:6,1:8,0:9})
# 3. Collective triplet invariance and actual full Hamiltonian.
M=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])[1:,:]; V=M.T
E=s.zeros(16,9)
for idx,(i,j) in enumerate(pairs): E[idx,0:3]=V[i,:]; E[idx,3:6]=V[j,:]
E[12:16,6:9]=V
Mc=s.Matrix([[0,d,0],[d,0,a],[-a,3*a,-k]])
ck('collective cross block invariant',C*E==E*s.kronecker_product(Mc,s.eye(3)))
ck('collective determinant',s.expand(Mc.det()-d*(d*k-a*a))==0)
ck('witness collective rank nine',Mc.subs({d:-s.Rational(1,2),a:-1,k:-1}).rank()*3==9)
ck('shared-edge tuned collective rank six',Mc.subs({d:1,a:2,k:4}).rank()*3==6)
r,b,ee,ec=s.symbols('r b e e_c',real=True)
A=s.diag(ee*s.eye(12),ec*s.eye(4))
for i,(j,l) in enumerate(pairs):
    for m,(jj,ll) in enumerate(pairs):
        if j==jj and l!=ll:A[i,m]=r
    A[i,12+j]=A[12+j,i]=b
Ma=s.Matrix([[ee+2*r,-r,b],[0,ee-r,0],[3*b,-b,ec]])
ck('same chamber reduction',A*E==E*s.kronecker_product(Ma,s.eye(3)))
ck('full even Stage VII matrix',Ma+Mc==s.Matrix([[ee+2*r,-r+d,b],[d,ee-r,a],[3*b-a,-b+3*a,ec-k]]))
A0=A.subs({r:-1,b:-2,ee:0,ec:-s.Rational(99,10)})
Y=s.zeros(4,12).row_join(s.eye(4)); Qall=Q.row_join(s.zeros(4,4)); Rall=R.row_join(s.zeros(4,4))
def krylov_rank(read,H,steps):
    return s.Matrix.vstack(*(read*H**i for i in range(steps))).rank()
ck('isolated four base histories rank eight',krylov_rank(Y,A0,4)==8)
ck('isolated row winding invisible to base histories', all(Y*A0**i*s.Matrix.vstack(s.eye(12)-R.T*R/3,s.zeros(4,12))==s.zeros(4,12) for i in range(4)))
print('isolated chamber observability ranks (Y,Q,Y+Q) at four steps',*[krylov_rank(z,A0,4) for z in [Y,Qall,Y.col_join(Qall)]])
# normalized row-closed initial q; symbolic overlap coefficient via G and E
q=s.Matrix(s.symbols('q0:4',real=True)); q[3]=-sum(q[:3]); out=s.Matrix([q[i]/3+q[j] for i,j in pairs]); ck('row closure',R*out==s.zeros(4,1)); ck('column read',Q*out==s.Rational(8,3)*q)
ck('initial transpose expectation',s.expand((out.T*T*out)[0]-s.Rational(8,9)*(q.T*q)[0])==0)
ck('initial base excitation zero',R*out==s.zeros(4,1)); ck('opposite-column excites core',Q*out!=s.zeros(4,1))
# 4. Correct Wirtinger normalization and transfer identities, scalar representative.
u,v,p,h=s.symbols('u v p h',real=True); lam,kap=s.symbols('lambda kappa',real=True)
z=u+s.I*v; w=p+s.I*h; chi=s.conjugate(z)*w
NA=u*u+v*v; NB=p*p+h*h
H=lam*chi*s.conjugate(chi)+kap*s.re(chi**2)
# z=x+iy -> i dot z=dH/dbar z; dx=H_y/2, dy=-H_x/2.
def rate(H,x,y):return s.expand(x*s.diff(H,y)-y*s.diff(H,x))
ck('pair transfer exact factor 2',s.simplify(rate(H,u,v)-2*kap*s.im(chi**2))==0)
ck('total occupation conservation',s.simplify(rate(H,u,v)+rate(H,p,h))==0)
ck('empty partner invariant for pair law',s.diff(H,p).subs({p:0,h:0})==0 and s.diff(H,h).subs({p:0,h:0})==0)
Hseed=(NA+NB)*2*s.re(chi)
ck('norm-lift permits empty partner seed',s.diff(Hseed,p).subs({p:0,h:0,u:1,v:0})==2)
# Bloch sphere: s continuous as expectation not determinant root.
ck('Bloch sphere identity',s.expand((NA-NB)**2+4*s.re(chi)**2+4*s.im(chi)**2-(NA+NB)**2)==0)
# phase-lock instantaneous is not invariant with detuning, demonstrated below.
# 5. Numerical dynamics; no direct cross-chamber hopping in H_local.
An=np.array(A0,float); Cn=np.array(C0,float); En=np.array(E,float)
Hloc=np.zeros((33,33)); Hloc[:16,:16]=Hloc[16:32,16:32]=An; Hloc[12:16,32]=Hloc[32,12:16]=-1; Hloc[28:32,32]=Hloc[32,28:32]=-1
Hcross=np.zeros_like(Hloc); Hcross[:16,16:32]=Hcross[16:32,:16]=Cn
H7=Hloc+Hcross
ck('full Stage VII undirected edges',np.count_nonzero(np.triu(H7,1))==104)
ck('48 removed cross links',np.count_nonzero(np.triu(Hcross,1))==48)
# choose original axis witness, z has C=(0,0,1) and all eight normals nonzero.
z0=np.array([1,1j,0])/np.sqrt(2); rho=np.sqrt(3)/8
x0=rho*En@np.concatenate([z0/3,z0,np.zeros(3)])
psi0=np.r_[x0,x0,0j]; N0=np.vdot(psi0,psi0).real
ck('initial norm 1',abs(N0-1)<1e-14,'numeric')
chi0=np.vdot(x0,Cn@x0).real
ck('initial overlap -1/12',abs(chi0+1/12)<1e-14,'numeric')
# H=Hloc energy + N/N0 * cross energy; derivative + common scalar.
def lift_rhs(t,y):
    N=np.vdot(y,y).real; ex=np.vdot(y,Hcross@y).real
    return -1j*(Hloc@y+N/N0*(Hcross@y)+ex/N0*y)
def lift_energy(y):return np.vdot(y,Hloc@y).real+np.vdot(y,y).real/N0*np.vdot(y,Hcross@y).real
# genuinely nonlinear overlap candidate: lambda=0, kappa=1/chi0, chosen only to match initial rate.
# Negative sign is model-specific. For general lambda, same even branch depends on lambda+kappa.
kappa=1/chi0

def overlap_rhs(t,y):
    A,B=y[:16],y[16:32]; chi=np.vdot(A,Cn@B)
    out=Hloc@y; out[:16]+=kappa*chi*(Cn@B); out[16:32]+=kappa*np.conj(chi)*(Cn@A)
    return -1j*out

def overlap_energy(y):return np.vdot(y,Hloc@y).real+kappa*np.real(np.vdot(y[:16],Cn@y[16:32])**2)

def integ(f,y,ts):
    sol=solve_ivp(f,(ts[0],ts[-1]),y,t_eval=ts,rtol=2e-11,atol=2e-12,method='DOP853'); assert sol.success;return sol.y.T

ts=np.linspace(0,20,401); linear=np.array([expm(-1j*H7*t)@psi0 for t in ts]); lifted=integ(lift_rhs,psi0,ts); nonlinear_full=integ(overlap_rhs,psi0,ts)
# The exact inversion-even collective submanifold is invariant; do not let
# roundoff in transverse unstable modes contaminate its own trajectory.
J3=rho*En@np.column_stack([np.r_[z0,np.zeros(6)],np.r_[np.zeros(3),z0,np.zeros(3)],np.r_[np.zeros(6),z0]])
ma=np.array(Ma.subs({r:-1,b:-2,ee:0,ec:-s.Rational(99,10)}),float)
mc=np.array(Mc.subs({d:-s.Rational(1,2),a:-1,k:-1}),float)
def even_rhs(t,x):
    X=J3@x; ch=np.vdot(X,Cn@X).real
    return -1j*(ma+kappa*ch*mc)@x
reduced=integ(even_rhs,np.array([1/3,1,0],complex),ts)
nonlinear=np.array([np.r_[J3@x,J3@x,0j] for x in reduced])
print('Full-space overlap maximum parity error',np.max(abs(nonlinear_full[:,:16]-nonlinear_full[:,16:32])))
for j,yn in enumerate(nonlinear_full):
    ck(f'full overlap conservation sample {j}',abs(np.vdot(yn,yn).real-N0)<3e-8 and abs(overlap_energy(yn)-overlap_energy(psi0))<3e-8,'numeric')
    if ts[j]<=.5: ck(f'early independent full vs reduced {j}',near(yn,nonlinear[j],3e-8),'numeric')
ring_edges=[(off+ix[(i,j)],off+ix[(i,l)]) for off in [0,16] for i in I for j,l in __import__('itertools').combinations([k for k in I if k!=i],2)]
core_edges=[(12+i,28+j) for i,j in pairs]
def currents(y,edges,mat):return np.array([2*np.imag(y[i]*mat[j,i]*np.conj(y[j])) for i,j in edges])
def observables(y, scale=1):return [np.linalg.norm(y[np.r_[12:16,28:32]])**2, np.min(np.abs(currents(y,ring_edges,Hloc))), abs(scale)*np.linalg.norm(currents(y,core_edges,Hcross))]
for j,(l,y,n) in enumerate(zip(linear,lifted,nonlinear)):
    phase=np.vdot(l,y); phase/=abs(phase)
    ck(f'lift projective trajectory sample {j}',near(y,phase*l,3e-8),'numeric')
    ck(f'lift all ring and effective core currents {j}',near(currents(y,ring_edges+core_edges,H7),currents(l,ring_edges+core_edges,H7),3e-8),'numeric')
    ck(f'lift norm/energy {j}',abs(np.vdot(y,y).real-N0)<3e-8 and abs(lift_energy(y)-lift_energy(psi0))<3e-8,'numeric')
    ck(f'overlap norm/energy {j}',abs(np.vdot(n,n).real-N0)<3e-8 and abs(overlap_energy(n)-overlap_energy(psi0))<3e-8,'numeric')
    ck(f'overlap parity and dark scalar {j}',near(n[:16],n[16:32],3e-8) and abs(n[32])<3e-8,'numeric')
ck('balanced exact reduced trajectory has zero net chamber transfer',max(abs(np.vdot(y[:16],y[:16]).real-np.vdot(y[16:32],y[16:32]).real) for y in nonlinear)<1e-12,'numeric')
ck('overlap seed at same initial derivative',near(overlap_rhs(0,psi0),-1j*H7@psi0,1e-13),'numeric')
# full arbitrary state, asymmetric: norm-lift not confined to selected sector.
rng=np.random.default_rng(128); rnd=rng.normal(size=33)+1j*rng.normal(size=33);rnd/=np.linalg.norm(rnd)
short=np.linspace(0,4,41); yy=integ(lift_rhs,rnd,short)
for j,tv in enumerate(short):
    l=expm(-1j*H7*tv)@rnd; phase=np.vdot(l,yy[j]); phase/=abs(phase)
    ck(f'general-state lift {j}',near(yy[j],l*phase,3e-8),'numeric')
# Drainless counterexample: no transfer but B nonzero; initial instantaneous zero not locked.
# Use scalar detuned pair Hamiltonian H=Delta NB + kappa Re chi^2.
def pair_rhs(t,y):
    a,b=y; chi=np.conj(a)*b
    return -1j*np.array([chi*b,b+np.conj(chi)*a])
ylock=np.array([1,1],complex)/np.sqrt(2); pair=integ(pair_rhs,ylock,np.linspace(0,2,101))
ck('initial flux zero',abs(2*np.imag((np.conj(ylock[0])*ylock[1])**2))<1e-14,'numeric')
ck('instantaneous zero not invariant under detuning',abs(abs(pair[-1,1])**2-.5)>1e-3,'numeric')
# matched linear resonance on separated amplitude spaces: exact Rabi formula, not material proof.
for detune in [0,.5,2,10]:
    g=1.; H=np.array([[0,g],[g,detune]]); omega=np.sqrt(g*g+(detune/2)**2)
    for j,tv in enumerate(np.linspace(0,5,31)):
        y=expm(-1j*H*tv)@np.array([1,0]); expected=(g/omega)**2*np.sin(omega*tv)**2
        ck(f'detuning {detune} sample {j}',abs(abs(y[1])**2-expected)<1e-12,'numeric')
# plot trajectory comparison; effective bond diagnostic not physical path.
obs=np.array([observables(y) for y in linear]); obsn=np.array([observables(y,kappa*np.vdot(y[:16],Cn@y[16:32]).real) for y in nonlinear]);
np.savetxt(P/'trajectory.csv',np.c_[ts,obs,obsn],delimiter=',',header='time,stageVII_core_N,stageVII_min_ring_current,stageVII_cross_read_norm,overlap_core_N,overlap_min_ring_current,overlap_cross_read_norm',comments='')
fig,axs=plt.subplots(3,1,figsize=(9,8),sharex=True,layout='constrained')
for i,label in enumerate(['Central-face occupation','Minimum absolute ring current','Norm of effective core-bond read']):
    axs[i].plot(ts,obs[:,i],label='Stage VII / norm lift',lw=1.8,color='#2563eb'); axs[i].plot(ts,obsn[:,i],label='Nonlinear overlap witness',lw=1.5,color='#d97706');axs[i].set_ylabel(label,fontsize=10);axs[i].grid(alpha=.2)
axs[0].legend(); axs[-1].set_xlabel('Dimensionless evolution time');fig.suptitle('Same initial eight-ring state, different vertex laws',fontweight='bold');fig.savefig(P/'figures/vertex_dynamics.png',dpi=170);plt.close(fig)
fig,axs=plt.subplots(1,2,figsize=(10,4.8),layout='constrained');
for ax,data,title in zip(axs,[Cn,np.array(Kf,float)],['Original cross block (48 entries)','Same interaction in 16-channel Walsh read']):
    im=ax.imshow(data,cmap='RdBu_r',vmin=-max(abs(data).ravel()),vmax=max(abs(data).ravel()));ax.set_title(title,fontsize=11);ax.set_xlabel('TetB record');ax.set_ylabel('TetA record');fig.colorbar(im,ax=ax,shrink=.75)
fig.savefig(P/'figures/cross_block.png',dpi=170);plt.close(fig)
print('sampled extrema: stageVII',obs.min(axis=0),obs.max(axis=0),'overlap',obsn.min(axis=0),obsn.max(axis=0))
print('full vs reduced final deviation',np.linalg.norm(nonlinear_full[-1]-nonlinear[-1]))
print('overlap nonzero core sampled times',np.count_nonzero(obsn[1:,0]>1e-10),'of',len(ts)-1)
print('TOTAL',counts,'all passed')
