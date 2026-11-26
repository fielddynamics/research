"""Constitutive vertex: exact dual/action/curvature and full-space stability checks.
Run with OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_mu_vertex.py.
All amplitudes and times are dimensionless. No physical calibration is claimed.
"""
from pathlib import Path
from itertools import permutations
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent
count={'exact':0,'numerical':0}
def ck(name,test,kind='exact'):
    assert bool(test),name
    count[kind]+=1;print('PASS',kind,name,flush=True)
x,b,t=s.symbols('x b t',positive=True)
mu=x/(1+x); W=-b-s.log(1-b); L=x-s.log(1+x)
ck('vacancy cost derivative',s.simplify(s.diff(W,b)-b/(1-b))==0)
ck('vacancy cost strictly convex',s.simplify(s.diff(W,b,2)-1/(1-b)**2)==0)
ck('unique stationary response',s.simplify(s.diff(W,b).subs(b,mu)-x)==0)
ck('Legendre dual',s.simplify(x*mu-W.subs(b,mu)-L)==0)
ck('dual slope is mu',s.diff(L,x)==mu or s.simplify(s.diff(L,x)-mu)==0)
ck('dual curvature',s.simplify(s.diff(L,x,2)-1/(1+x)**2)==0)
ck('exchange complement',s.simplify(mu+mu.subs(x,1/x)-1)==0)
ck('logistic derivative',s.simplify(x*s.diff(mu,x)-mu*(1-mu))==0)
ck('AQUAL relation',s.simplify(s.diff(x*x-2*L,x)-2*x*mu)==0)
G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
MA=s.Matrix([[-2,1,-2],[0,1,0],[-6,2,-s.Rational(99,10)]])
MC=s.Matrix([[0,-s.Rational(1,2),0],[-s.Rational(1,2),0,-1],[1,-3,1]])
v=s.Matrix([s.Rational(1,3),1,-s.Rational(4,15)]); f=s.Rational(225,1232); E=s.Rational(11,10)
K=MA+MC-E*s.eye(3); c=(f*v.T*G*MC*v)[0]
ck('stationary eigenvector',K*v==s.zeros(3,1));ck('normalized metric',(2*f*v.T*G*v)[0]==1);ck('overlap',c==s.Rational(59,308))
for A in [MA,MC,K]:ck('metric self-adjoint',A.T*G==G*A)
proj=v*v.T*G/(v.T*G*v)[0]; d=(s.eye(3)-proj)*MC*v
hc=1/(f*(d.T*G*(-K+proj).inv()*d)[0]); ck('curvature threshold',hc==s.Rational(290521,42815))
u=s.symbols('u',positive=True); F=2*(1+t)*(u-t*c*s.log(1+u/(t*c)))
ck('slope matches Stage VII',s.simplify(s.diff(F,u).subs(u,c)-2)==0)
h=s.factor(s.diff(F,u,2).subs(u,c)); ck('curvature formula',s.simplify(h-2*t/(c*(1+t)))==0)
tcrit=s.factor(hc*c/(2-hc*c)); ck('threshold ratio',s.simplify(h.subs(t,tcrit)-hc)==0)
ck('unit ratio below threshold',h.subs(t,1)<hc);ck('ratio two above threshold',h.subs(t,2)>hc)
print('EXACT c,h_c,t_crit,h(1):',c,hc,tcrit,h.subs(t,1))
# Direct AQUAL energy differs from its Legendre-dual correction.
D=(u/(t*c))**2-2*u/(t*c)+2*s.log(1+u/(t*c)); Da=2*D/s.diff(D,u).subs(u,c)
ha=s.factor(s.diff(Da,u,2).subs(u,c)); ck('AQUAL normalized curvature',s.simplify(ha-2*(1+2*t)/(c*(1+t)))==0);ck('AQUAL bound exceeds threshold',2/c>hc)
Z=s.Matrix.hstack(*(v.T*G).nullspace()); ck('tangent rank',Z.rank()==2 and v.T*G*Z==s.zeros(1,2))
for ratio in [s.Rational(1,10),s.Rational(1,2),1,s.Rational(3,2),2,4]:
    H=h.subs(t,ratio); B=K+H*f*MC*v*v.T*G*MC; R=Z.T*G*B*Z
    ck(f'tangent symmetry {ratio}',R==R.T)
    ck(f'tangent inertia {ratio}',(R[0,0]<0 and R.det()>0) if ratio<tcrit else R.det()<0)
# Full graph; same labels, couplings and stationary witness as inherited verifier.
pairs=list(permutations(range(4),2)); M=np.array([[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float); q=M.T@np.array([1,1j,0])/np.sqrt(2)
AA=np.zeros((16,16));AA[12:,12:]=-9.9*np.eye(4)
C=np.zeros((16,16));C[12:,12:]=-(np.ones((4,4))-np.eye(4))
for i,(a,j) in enumerate(pairs):
    AA[i,12+a]=AA[12+a,i]=-2;C[i,12+j]=C[12+j,i]=-1;C[i,pairs.index((j,a))]=-.5
    for k,(aa,jj) in enumerate(pairs):
        if a==aa and j!=jj:AA[i,k]=-1
H0=np.zeros((33,33));H0[:16,:16]=H0[16:32,16:32]=AA;H0[12:16,32]=H0[32,12:16]=-1;H0[28:32,32]=H0[32,28:32]=-1
V=np.zeros_like(H0);V[:16,16:32]=C;V[16:32,:16]=C.T
D=np.zeros((16,3),complex)
for k,(i,j) in enumerate(pairs):D[k,:2]=[q[i],q[j]]
D[12:,2]=q; B=np.vstack([D,D,np.zeros((1,3))]); Q=np.linalg.qr(B)[0]; Proj=Q@Q.conj().T
psi=B@np.array(v,float).ravel();psi/=np.linalg.norm(psi); cf=float(c); E0=float(E)
ck('full stationary state',np.linalg.norm((H0+V)@psi-E0*psi)<1e-12,'numerical')
ck('full overlap',abs(np.vdot(psi,V@psi).real/2-cf)<1e-12,'numerical')
for name,A,MA0 in [('local',H0,MA),('vertex',V,MC)]:
    ck(name+' exact embedding numeric check',np.linalg.norm(A@B-B@np.array(MA0,float))<1e-12,'numerical')
    ck(name+' invariant complement',np.linalg.norm(A@Proj-Proj@A)<1e-12,'numerical')
# exact embedding in unscaled Gaussian integers, real matrices rational.
qe=s.Matrix([1+s.I,1-s.I,-1+s.I,-1-s.I]);De=s.zeros(16,3)
for j,(i,k) in enumerate(pairs):De[j,0]=qe[i];De[j,1]=qe[k]
De[12:,2]=qe; Be=De.col_join(De).col_join(s.zeros(1,3));
for name,A,MA0 in [('local',H0,MA),('vertex',V,MC)]:
    Ae=s.Matrix(A).applyfunc(lambda a:s.Rational(str(float(a))))
    ck(name+' exact invariant embedding',(Ae*Be-Be*MA0).applyfunc(s.simplify)==s.zeros(33,3))

def overlap(z):return np.vdot(z,V@z).real/2
def pot(u,r):return 2*(1+r)*(abs(u)-r*cf*np.log1p(abs(u)/(r*cf)))
def gain(u,r):return (1+r)*u/(r*cf+abs(u))
def energy(z,r):return np.vdot(z,H0@z).real+pot(overlap(z),r)
def rhs(z,r):return -1j*((H0+gain(overlap(z),r)*V)@z-E0*z)
for r in [.1,.5,1,1.5,2,4]:
    ck(f'stationary nonlinear r={r}',np.linalg.norm(rhs(psi,r))<1e-12,'numerical')
    w=V@psi; hh=float(h.subs(t,s.Rational(str(r))))
    def action(z):return -1j*((H0+V-E0*np.eye(33))@z+hh/2*np.vdot(w,z).real*w)
    J=np.column_stack([np.r_[action(z).real,action(z).imag] for z in np.c_[np.eye(33),1j*np.eye(33)].T]); growth=max(np.linalg.eigvals(J).real)
    ck(f'full Jacobian stability r={r}',growth<1e-5 if r<float(tcrit) else growth>1e-3,'numerical');print('growth',r,growth)
# Integrate the entire complex state, not only collective coordinates.
rng=np.random.default_rng(27);times=np.linspace(0,25,251); rows=[]
for r in [1.,2.]:
    for eps in [1e-4,1e-3,1e-2]:
        for mode in ['balanced','general']:
            z=rng.normal(size=33)+1j*rng.normal(size=33)
            if mode=='balanced':z=Proj@z
            z-=psi*np.vdot(psi,z);z/=np.linalg.norm(z);ini=psi+eps*z;ini/=np.linalg.norm(ini)
            sol=solve_ivp(lambda T,Y:rhs(Y,r),(0,25),ini,t_eval=times,rtol=2e-10,atol=2e-12,method='DOP853');ck(f'integration {r} {eps} {mode}',sol.success,'numerical')
            Y=sol.y;dist=np.sqrt(np.maximum(0,np.sum(abs(Y)**2,axis=0)+1-2*abs(psi.conj()@Y))); comp=np.sum(abs((np.eye(33)-Proj)@Y)**2,axis=0); es=np.array([energy(y,r) for y in Y.T]); norms=np.sum(abs(Y)**2,axis=0)
            ck(f'norm {r} {eps} {mode}',np.max(abs(norms-1))<1e-7,'numerical');ck(f'energy {r} {eps} {mode}',np.max(abs(es-es[0]))<1e-7,'numerical');ck(f'complement conservation {r} {eps} {mode}',np.max(abs(comp-comp[0]))<1e-8,'numerical')
            if r==1:ck(f'bounded orbital deviation {eps} {mode}',max(dist)<12*eps,'numerical')
            print('ORBIT',r,eps,mode,max(dist));rows.extend(zip([r]*len(times),[eps]*len(times),[mode]*len(times),times,dist,comp,es))
import csv
with (P/'mu_vertex_trajectories.csv').open('w') as out:
    wr=csv.writer(out);wr.writerow(['scale_ratio','perturbation','mode','time','phase_minimized_distance','complement_norm_squared','energy']);wr.writerows(rows)
# Empty B with zero-sum directional A stays empty, but a seeded B can transfer.
A=psi[:16]*np.sqrt(2);empty=np.r_[A,np.zeros(17,complex)];ck('no empty partner seed',np.linalg.norm(rhs(empty,1)[16:])<1e-12,'numerical')
seed=np.r_[A,np.exp(1j*np.pi/4)*A*.1,0j];seed/=np.linalg.norm(seed);chi=np.vdot(seed[:16],C@seed[16:32]);rate=2*np.vdot(seed[:16],rhs(seed,1)[:16]).real
ck('nonzero transfer for seeded partner',abs(rate)>1e-5,'numerical');ck('exchange rate formula',abs(rate-2*gain(overlap(seed),1)*chi.imag)<1e-12,'numerical')
# Plot actual test results.
fig,ax=plt.subplots(1,2,figsize=(11,4.2));rr=np.linspace(.01,4,400);ax[0].plot(rr,2*rr/(cf*(1+rr)),label='dual μ potential');ax[0].plot(rr,2*(1+2*rr)/(cf*(1+rr)),ls='--',label='direct AQUAL');ax[0].axhline(float(hc),color='black',ls=':',label='threshold');ax[0].axvline(float(tcrit),color='gray',ls=':');ax[0].set(xlabel='scale ratio t',ylabel='matched curvature',title='Exact curvature comparison');ax[0].legend(fontsize=8)
for r in [1.,2.]:
    R=[v for v in rows if v[0]==r and v[1]==.001 and v[2]=='general'];ax[1].semilogy([v[3] for v in R],[max(v[4],1e-12) for v in R],label=f't = {r:g}')
ax[1].set(xlabel='dimensionless time',ylabel='phase-minimized distance',title='Full 33-amplitude perturbation');ax[1].legend();fig.tight_layout();fig.savefig(P/'figures/mu_vertex_stability.png',dpi=180);plt.close(fig)
print('TOTAL',count,'sum',sum(count.values()))
