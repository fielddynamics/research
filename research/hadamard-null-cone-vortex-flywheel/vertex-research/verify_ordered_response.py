"""Ordered response continuation: exact identities + numerical witnesses.
Run OPENBLAS_NUM_THREADS=1 python verify_ordered_response.py.
No physical drain parameter or acceleration identification is derived here.
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
counts={'exact':0,'numerical':0}
def ck(name,condition,kind='exact'):
    assert bool(condition),name
    counts[kind]+=1;print('PASS',kind,name,flush=True)
def eq(a,b):return s.simplify(a-b)==0
x,tau,gamma=s.symbols('x tau gamma',positive=True)
b=s.symbols('b',real=True)
a0=s.symbols('a_0',positive=True)
W=-b-s.log(1-b);L=x-s.log(1+x);mu=x/(1+x)
# Scheme and ordered state, not an identification of acceleration with det parity.
eta=s.diag(-1,1,1,1);par=s.diag(1,-1,-1,-1)
E=s.Matrix(4,4,s.symbols('e0:16'))
ck('constant parity preserves metric',par.T*eta*par==eta)
ck('parity leaves time coframe unchanged',(par*E)[0,:]==E[0,:])
ck('parity flips determinant',par.det()==-1)
na,nb=s.symbols('N_A N_B',positive=True);z=(na-nb)/(na+nb);odds=na/nb
ck('occupation contrast Cayley odds',eq(z,(odds-1)/(odds+1)))
ck('occupation share complementary',eq(mu.subs(x,odds),na/(na+nb)))
ck('root exchange changes contrast sign',eq(z.xreplace({na:nb,nb:na}),-z))
ck('response odds swap',eq(mu+mu.subs(x,1/x),1))
ck('log odds susceptibility',eq(x*s.diff(mu,x),mu*(1-mu)))
# Existing settlement dual: drive p=a0 x, response q=a0 mu. Difference is observable flux.
q=a0*mu;p=a0*x
ck('response odds exact',eq((p-q)/q,x))
ck('response fraction not capacity occupancy',eq(q/p,1-mu))
ck('AQUAL radial potential derivative',eq(s.diff(p*p-2*a0*a0*L,x),2*a0*a0*x*mu))
# Gated finite capacity: two distinct conditional constructions.
# series / reduced capacity (tau>0); q= a0*tau*b, cost=(a0*tau)^2 W(b)
cs=a0*tau;bs=x/(x+tau);qs=cs*bs
# parallel / active fraction gamma; cost=gamma*a0^2 W(q/(gamma*a0))
cp=gamma*a0;bp=mu;qp=cp*bp
for name,cap,weight,bopt,qopt in [('capacity',cs,cs**2,bs,qs),('parallel',cp,gamma*a0**2,bp,qp)]:
    cost=weight*W
    ck(name+' stationary work conjugacy',eq(s.diff(cost,b).subs(b,bopt),p*cap))
    ck(name+' strict convexity',eq(s.diff(cost,b,2),weight/(1-b)**2))
    dual=s.simplify(p*qopt-cost.subs(b,bopt))
    target=(cs**2*(x/tau-s.log(1+x/tau)) if name=='capacity' else gamma*a0**2*L)
    ck(name+' dual',eq(dual,target))
    ck(name+' response from dual derivative',eq(s.diff(target,x)/a0,qopt))
    ck(name+' full-open recovery',eq(qopt.subs(tau if name=='capacity' else gamma,1),q))
    ck(name+' closed drain limit',s.limit(qopt,tau if name=='capacity' else gamma,0,dir='+')==0)
    ck(name+' Newtonian flux at closed drain',s.limit(p-qopt,tau if name=='capacity' else gamma,0,dir='+')==p)
ms=1-qs/p;mp=1-qp/p
ck('capacity effective mu',eq(ms,x/(x+tau)))
ck('parallel effective mu',eq(mp,1-gamma/(1+x)))
ck('partial gates not equivalent',eq((mp-ms).subs(gamma,tau),tau*(1-tau)/((1+x)*(x+tau))))
ck('different deep limit capacity',s.limit(ms,x,0,dir='+')==0)
ck('different deep limit parallel',s.limit(mp,x,0,dir='+')==1-gamma)
ck('capacity radial differential response',eq(s.diff(x*ms,x),x*(x+2*tau)/(x+tau)**2))
ck('parallel radial differential response',eq(s.diff(x*mp,x),1-gamma/(1+x)**2))
# Ordered rates for response fraction, not wave amplitude or irreversible dynamics without a reservoir.
f,r=s.symbols('f r',positive=True);m=s.symbols('m',real=True);kap=s.symbols('kappa',positive=True)
rate=kap*(r*(1-m)-f*m);meq=r/(r+f)
ck('detailed balance equilibrium',eq(rate.subs(m,meq),0))
ck('unique relaxation exponent',eq(s.diff(rate,m),-kap*(r+f)))
ck('relabeling rate exchanges equilibrium',eq(meq+meq.xreplace({r:f,f:r}),1))
ck('open detailed balance recovers mu',eq(meq.subs({r:x,f:1}),mu))
ck('closed outward rate gives full retained response',s.limit(meq,f,0,dir='+')==1)
ck('positive balanced exchange despite zero net',eq((r*(1-m)+f*m).subs(m,meq),2*r*f/(r+f)))
# Real & imaginary coherence in a common eigenchannel, using canonical complex Hamilton convention.
A,B,c,k=s.symbols('A B c k',real=True);ar,ai,br,bi=s.symbols('ar ai br bi',real=True)
aa=ar+s.I*ai;bb=br+s.I*bi;chi=c*s.conjugate(aa)*bb
ad=-s.I*k*c*bb;bd=-s.I*k*c*aa
nd=2*s.re(s.conjugate(aa)*ad);chid=s.conjugate(ad)*c*bb+s.conjugate(aa)*c*bd
ck('canonical transfer sign',eq(nd,2*k*s.im(chi)))
ck('coherence derivative purely imaginary in eigenchannel',eq(s.re(chid),0))
ck('imaginary coherence derivative',eq(s.im(chid),k*c*c*(br*br+bi*bi-ar*ar-ai*ai)))
ck('zero flux need not remain zero',eq(s.im(chid).subs({ar:2,ai:0,br:1,bi:0}),-3*k*c*c))
# Reconstruct exact Stage VII blocks on the fixed-q triplet in each chamber.
G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
M=s.Matrix([[-2,1,-2],[0,1,0],[-6,2,-s.Rational(99,10)]])
K=s.Matrix([[0,-s.Rational(1,2),0],[-s.Rational(1,2),0,-1],[1,-3,1]])
ck('local G symmetry',M.T*G==G*M);ck('cross G symmetry',K.T*G==G*K)
ck('local and cross do not commute',M*K-K*M!=s.zeros(3))
# In parity basis imbalance is off diagonal. Heisenberg closure over rationals:
# i[H0,O] upper block i[M,L]; i[V,O] upper block i{K,L}.
# Work with 10M,2K to use integer operations. A modular independent set is a rigorous lower bound in Q;
# ambient real dimension 18 gives the upper bound. Keep real and imaginary parts separately.
Mi=np.array(10*M,dtype=np.int64);Ki=np.array(2*K,dtype=np.int64);prime=1009
basis={};queue=[];words=[]
def insert(R,I,word):
    R=R%prime;I=I%prime
    v=np.r_[R.ravel(),I.ravel()].astype(np.int64)
    for j,w in sorted(basis.items()):v=(v-v[j]*w)%prime
    nz=np.flatnonzero(v)
    if not len(nz):return
    j=int(nz[0]);basis[j]=v*pow(int(v[j]),-1,prime)%prime;queue.append((R,I,word));words.append(word)
insert(np.eye(3,dtype=np.int64),np.zeros((3,3),dtype=np.int64),'Z')
while queue:
    R,I,w=queue.pop(0)
    insert(-(Mi@I-I@Mi),Mi@R-R@Mi,'L'+w)
    insert(-(Ki@I+I@Ki),Ki@R+R@Ki,'V'+w)
print('IMBALANCE OBSERVABLE CLOSURE dimension',len(basis),'mod',prime,'words',words)
ck('imbalance requires full 18 real off-diagonal directions',len(basis)==18)
# Full 33 graph and exact counterexamples: common eigenchannel in ker R & Q.
pairs=list(permutations(range(4),2));AA=np.zeros((16,16));AA[12:,12:]=-9.9*np.eye(4);C=np.zeros((16,16));C[12:,12:]=-(np.ones((4,4))-np.eye(4))
for i,(a,j) in enumerate(pairs):
    AA[i,12+a]=AA[12+a,i]=-2;C[i,12+j]=C[12+j,i]=-1;C[i,pairs.index((j,a))]=-.5
    for k,(aa,jj) in enumerate(pairs):
        if a==aa and j!=jj:AA[i,k]=-1
R=s.zeros(4,12);Q=s.zeros(4,12);T=s.zeros(12)
for n,(i,j) in enumerate(pairs):R[i,n]=1;Q[j,n]=1;T[pairs.index((j,i)),n]=1
AE=s.Matrix(AA).applyfunc(lambda z:s.Rational(str(float(z))));CE=s.Matrix(C).applyfunc(lambda z:s.Rational(str(float(z))))
U=s.Matrix.vstack(R,Q,T-s.eye(12)).nullspace();ck('common dark symmetric channel dimension',len(U)==2)
for v in U:
    v=v.col_join(s.zeros(4,1));ck('native common eigenvector local',AE*v==v);ck('native common eigenvector cross',CE*v==-v/2)
H=np.zeros((33,33));H[:16,:16]=H[16:32,16:32]=AA;H[12:16,32]=H[32,12:16]=-1;H[28:32,32]=H[32,28:32]=-1
V=np.zeros_like(H);V[:16,16:32]=C;V[16:32,:16]=C.T
cf=59/308
def gain(u):return 2*u/(cf+abs(u))
def energy(y):
    u=np.vdot(y,V@y).real/2;return np.vdot(y,H@y).real+4*(abs(u)-cf*np.log1p(abs(u)/cf))
def rhs(y):return -1j*((H+gain(np.vdot(y,V@y).real/2)*V)@y)
# Constant real overlap, exact Rabi exchange through genuine nonlinear law restricted to a common channel.
v=np.array(U[0].col_join(s.zeros(4,1)),float).ravel();v/=np.linalg.norm(v)
times=np.linspace(0,20,401);rows=[]
for phase in [0,np.pi/6,np.pi/2,np.pi,5*np.pi/4]:
    a=np.sqrt(.8);b0=np.sqrt(.2)*np.exp(1j*phase);y0=np.r_[a*v,b0*v,0j];u=(-.5*np.conj(a)*b0).real;g=gain(u);om=-g/2
    sol=solve_ivp(lambda t,y:rhs(y),(0,20),y0,t_eval=times,rtol=1e-10,atol=1e-12,method='DOP853');ck('Rabi integration '+str(phase),sol.success,'numerical')
    aa=np.exp(-1j*times)*(a*np.cos(om*times)-1j*b0*np.sin(om*times));bb=np.exp(-1j*times)*(b0*np.cos(om*times)-1j*a*np.sin(om*times));pred=np.r_[v[:,None]*aa,v[:,None]*bb,np.zeros((1,len(times)))];Y=sol.y
    ck('native full Rabi formula '+str(phase),np.max(abs(Y-pred))<2e-8,'numerical')
    ck('energy conservation '+str(phase),max(abs(np.array([energy(y) for y in Y.T])-energy(y0)))<1e-8,'numerical')
    nk=np.sum(abs(Y[:16])**2,axis=0);fl=np.array([2*g*np.vdot(y[:16],C@y[16:32]).imag for y in Y.T]);ck('constant overlap '+str(phase),max(abs(np.array([np.vdot(y,V@y).real/2 for y in Y.T])-u))<1e-8,'numerical')
    rows.extend(zip([phase]*len(times),times,nk,fl))
# Distinguish standing instant from invariant no-transfer: phase 0 starts at zero flux but later moves.
rr=np.array(rows);r0=rr[rr[:,0]==0];ck('zero initial flux later moves',abs(r0[0,3])<1e-12 and np.ptp(r0[:,2])>.5,'numerical')
# Bound / no-go: normalized overlap can't determine acceleration/odds; orthogonal paired inputs have u=0 at any population.
# 24 arbitrary normalized amplitude pairs, actual derivative exact numerical identity and counterexamples.
rng=np.random.default_rng(84)
for j in range(24):
    y=rng.normal(size=33)+1j*rng.normal(size=33);y[32]=0;y/=np.linalg.norm(y);A=y[:16];B=y[16:32];chi=np.vdot(A,C@B);dy=rhs(y)
    ck(f'full transfer identity {j}',abs(2*np.vdot(A,dy[:16]).real-2*gain(chi.real)*chi.imag)<2e-12,'numerical')
    chidot=np.vdot(dy[:16],C@B)+np.vdot(A,C@dy[16:32]);formula=1j*np.vdot(A,(AA@C-C@AA)@B)+1j*gain(chi.real)*(np.vdot(B,C@C@B)-np.vdot(A,C@C@A))
    ck(f'full coherence identity {j}',abs(chidot-formula)<2e-12,'numerical')
    ck(f'bound overlap {j}',abs(chi)<=np.linalg.norm(C,2)*np.linalg.norm(A)*np.linalg.norm(B)+1e-12,'numerical')
# PSD channel activity: rank alone is not a universal weight. Projection weight = Tr(P rho)/Tr(rho).
for rank in [1,4,8,12,16]:
    Pr=np.diag([1]*rank+[0]*(16-rank));ck('uniform exposure fraction '+str(rank),np.trace(Pr)/16==rank/16,'numerical')
    y=np.eye(16)[0];ck('aligned exposure '+str(rank),y@Pr@y==1,'numerical')
    if rank<16:ck('dark exposure '+str(rank),np.eye(16)[-1]@Pr@np.eye(16)[-1]==0,'numerical')
# Plot actual Rabi tests + exact static comparison.
fig,ax=plt.subplots(1,2,figsize=(12,4.5));xx=np.logspace(-3,3,500)
for t in [0,.25,.5,1]:
    ax[0].semilogx(xx,xx/(xx+t),label=f'capacity τ={t:g}')
    if t not in [0,1]:ax[0].semilogx(xx,1-t/(1+xx),'--',label=f'parallel γ={t:g}')
ax[0].set(xlabel='x = |p|/a₀',ylabel='effective TetA response',title='Two conditional drain closures',ylim=(-.02,1.02));ax[0].legend(fontsize=8)
for ph in [0,np.pi/6,np.pi/2]:
    a=rr[np.isclose(rr[:,0],ph)];ax[1].plot(a[:,1],a[:,2],label=f'initial phase {ph/np.pi:.2g}π')
ax[1].set(xlabel='model time',ylabel='TetA occupation',title='Zero initial flux is not a closed drain',ylim=(-.02,1.02));ax[1].legend(fontsize=8);fig.tight_layout();fig.savefig(P/'figures/ordered_response.png',dpi=180);plt.close(fig)
np.savetxt(P/'ordered_response_trajectories.csv',rr,delimiter=',',header='phase,time,N_A,vertex_flux',comments='')
print('TOTAL',counts,'sum',sum(counts.values()))
