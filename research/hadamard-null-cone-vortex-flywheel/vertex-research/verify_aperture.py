"""Continuation of the registered constitutive vertex. Exact and numerical checks.
No new physical scale or drain-selection premise is inferred. Times dimensionless.
Run OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_aperture.py.
"""
from pathlib import Path
from itertools import permutations
import sympy as s
import numpy as np
from scipy.linalg import eig
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent
counts=dict(exact=0,numerical=0)
def ck(name,ok,kind='exact'):
    assert bool(ok),name
    counts[kind]+=1;print('PASS',kind,name,flush=True)
def eq(a,b):return s.simplify(a-b)==0
G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
M=s.Matrix([[-2,1,-2],[0,1,0],[-6,2,-s.Rational(99,10)]])
K=s.Matrix([[0,-s.Rational(1,2),0],[-s.Rational(1,2),0,-1],[1,-3,1]])
a=s.Matrix([s.Rational(1,3),1,0]);n=(a.T*G*a)[0];I=s.eye(3);proj=a*a.T*G/n;Q=I-proj;D=M-I;f=K*a;S=f*f.T*G/n
ck('local metric self-adjoint',M.T*G==G*M);ck('cross metric self-adjoint',K.T*G==G*K)
ck('empty partner row winding local eigenstate',M*a==a);ck('zero central component',a[2]==0)
ck('unit projector',proj*proj==proj);ck('D annihilates background',D*proj==s.zeros(3));ck('D commutes with complement',D*Q==Q*D)
ck('local characteristic',eq(M.charpoly().as_expr(),(M.charpoly().gen-1)*(10*M.charpoly().gen**2+119*M.charpoly().gen+78)/10))
ck('D negative on complement by trace and product',s.trace(D)<0 and (s.trace(D)**2-s.trace(D*D))/2>0)
ck('parallel cross coefficient',(a.T*G*f)[0]/n==-s.Rational(1,6));ck('transverse read',Q*f==s.Matrix([-s.Rational(4,9),0,-s.Rational(8,3)]))
ck('transverse exposure',(f.T*G*Q*f)[0]/n==s.Rational(26,9));ck('total exposure',(f.T*G*f)[0]/n==s.Rational(35,12))
ck('rank-one real anomalous term',S.rank()==1 and S.T*G==G*S)
susc=-(f.T*G*Q*(D+proj).inv()*Q*f)[0]/n
crit=1/susc;ck('exact seed susceptibility',susc==s.Rational(458,1863));ck('exact threshold',crit==s.Rational(1863,458))
h=s.symbols('h',real=True);cp=(D*(D+h*S)).charpoly();l=cp.gen
expected=l*(300*l*l+(10520*h-45543)*l+128547-31602*h)/300
ck('exact squared-frequency polynomial',eq(cp.as_expr(),expected));ck('threshold is polynomial root',eq((128547-31602*h).subs(h,crit),0))
c=s.Rational(59,308);t=s.symbols('t',positive=True);gamma=(1+t)/(t*c)
ck('all positive constitutive scale ratios supercritical at empty partner',1/c>crit)
ck('balanced stable interval nonempty',s.Rational(222607,119913)>1)
ck('t=1 gain derivative',gamma.subs(t,1)==s.Rational(616,59))
# Bracket from distribution of partial capacities, not an assumption that weights are actual occupations.
x=s.symbols('x',positive=True);v,m=s.symbols('v m',real=True)
phi=lambda v:x/(x+v)
ck('channel law convex in capacity',eq(s.diff(phi(v),v,2),2*x/(x+v)**3))
# pointwise tangent remainder and endpoint chord remainder, nonnegative on 0<=v<=1
ck('exact Jensen remainder',eq(phi(v)-phi(m)-s.diff(phi(m),m)*(v-m),x*(v-m)**2/((x+v)*(x+m)**2)))
ck('exact endpoint chord remainder',eq(1-v/(1+x)-phi(v),v*(1-v)/((1+x)*(x+v))))
ck('upper lower gap',eq(1-m/(1+x)-phi(m),m*(1-m)/((1+x)*(x+m))))
ck('open channel endpoint',eq(phi(1),x/(1+x)));ck('closed channel endpoint',eq(phi(0),1))
# first two moments at large x
z=s.symbols('z');ck('large acceleration first two moments',s.series(1/(1+v*z),z,0,3).removeO()==1-v*z+v*v*z*z)
# Native matrix C in all 16 coordinates; symmetry and exposure.
pairs=list(permutations(range(4),2));R=s.zeros(4,12);Qcol=s.zeros(4,12);T=s.zeros(12)
for k,(i,j) in enumerate(pairs):R[i,k]=1;Qcol[j,k]=1;T[pairs.index((j,i)),k]=1
C=(-T/2).row_join(-Qcol.T).col_join((-Qcol).row_join(-(s.ones(4)-s.eye(4))))
ck('C invertible',C.det()==-s.Rational(3,4096));ck('C symmetric',C.T==C)
Cjunction=(-T/2).row_join(-Qcol.T).col_join((-Qcol).row_join(-2*(s.ones(4)-s.eye(4))))
ck('shared-junction condition gives rank twelve',Cjunction.rank()==12)
ck('shared-junction nullspace dimension four',len(Cjunction.nullspace())==4)
for vv in Cjunction.nullspace():ck('junction null vector exact',Cjunction*vv==s.zeros(16,1))
U=s.Matrix.vstack(R,Qcol,T-s.eye(12)).nullspace();b=U[0].col_join(s.zeros(4,1));yc=s.zeros(12,1).col_join(s.ones(4,1))
ex=lambda b:(b.T*C*C*b)[0]/(b.T*b)[0]
ck('same inventory dark-to-base exposure',ex(b)==s.Rational(1,4));ck('same inventory uniform central exposure',ex(yc)==12)
ck('exposure not scalar inventory',ex(b)!=ex(yc))
for i in range(3):
    v=I[:,i];print('collective coefficient exposure',i,(v.T*G*K*K*v)[0]/(v.T*G*v)[0]);ck('positive collective exposure '+str(i),(v.T*G*K*K*v)[0]>0)
stationary=s.Matrix([s.Rational(1,3),1,-s.Rational(4,15)])
ck('balanced stationary matched eigenstate',(M+K)*stationary==s.Rational(11,10)*stationary)
ck('balanced stationary nonzero cross exposure',(stationary.T*G*K*K*stationary)[0]>0)
ck('balanced stationary nonzero overlap',(stationary.T*G*K*stationary)[0]>0)
# Full native 33 graph. Verify collective embedding at complex phase direction.
AA=np.zeros((16,16));AA[12:,12:]=-9.9*np.eye(4)
for i,(aidx,j) in enumerate(pairs):
    AA[i,12+aidx]=AA[12+aidx,i]=-2
    for k,(aa,jj) in enumerate(pairs):
        if aidx==aa and j!=jj:AA[i,k]=-1
Cn=np.array(C,float);H=np.zeros((33,33));H[:16,:16]=H[16:32,16:32]=AA;H[12:16,32]=H[32,12:16]=-1;H[28:32,32]=H[32,28:32]=-1
V=np.zeros_like(H);V[:16,16:32]=Cn;V[16:32,:16]=Cn
sign=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
z0=np.array([1,1j,0])/np.sqrt(2);q=sign@z0
E=np.array([[q[i],q[j],0] for i,j in pairs]+[[0,0,qi] for qi in q])/2
Gn=np.array(G,float);Mn=np.array(M,float);Kn=np.array(K,float);Dn=np.array(D,float);an=np.array(a,float).ravel()/np.sqrt(float(n));fn=Kn@an;Sn=np.outer(fn,fn@Gn)
ck('embedding metric',np.max(abs(E.conj().T@E-Gn))<1e-12,'numerical');ck('embedding local',np.max(abs(AA@E-E@Mn))<1e-12,'numerical');ck('embedding cross',np.max(abs(Cn@E-E@Kn))<1e-12,'numerical');ck('origin dark all collective modes',np.max(abs(E[12:].sum(0)))<1e-12,'numerical')
# Exact empty solution and seed Jacobian, in frame rotating at E=1.
c0=float(c);crit0=float(crit)
def gain(u,t):return (1+t)*u/(t*c0+abs(u))
def rhs(y,t):return -1j*((H+gain(np.vdot(y,V@y).real/2,t)*V)@y)
def energy(y,t):
    u=abs(np.vdot(y,V@y).real/2);return np.vdot(y,H@y).real+2*(1+t)*(u-t*c0*np.log1p(u/(t*c0)))
y0=np.r_[E@an,np.zeros(17,complex)]
for tt in [.2,1,1.8,4]:
    ck('exact empty trajectory vector field t='+str(tt),np.linalg.norm(rhs(y0,tt)+1j*y0)<1e-12,'numerical')
    hh=(1+tt)/(tt*c0);J=np.block([[np.zeros((3,3)),Dn],[-(Dn+hh*Sn),np.zeros((3,3))]])
    ev,evec=eig(J);i=np.argmax(ev.real);rate=ev[i].real;root=np.roots([300,10520*hh-45543,128547-31602*hh]);ck('growth eigenvalue agrees t='+str(tt),abs(rate-np.sqrt(-min(root)))<1e-10,'numerical')
    ck('one strictly growing mode t='+str(tt),sum(ev.real>1e-7)==1,'numerical')
# same t=1 as previous stable balanced witness; choose expanding seed, not arbitrary noise
hh=2/c0;J=np.block([[np.zeros((3,3)),Dn],[-(Dn+hh*Sn),np.zeros((3,3))]])
ev,evec=eig(J);i=np.argmax(ev.real);rate=ev[i].real;vec=evec[:,i].real;seed=vec[:3]+1j*vec[3:];seed/=np.sqrt(np.vdot(seed,Gn@seed).real);print('GROWTH amplitude exponent',rate)
rows=[];times=np.linspace(0,3,601)
for eps in [0,1e-8,1e-6,1e-4]:
    ini=np.r_[np.sqrt(1-eps*eps)*E@an,eps*E@seed,0j]
    sol=solve_ivp(lambda t,y:rhs(y,1),(0,3),ini,t_eval=times,method='DOP853',rtol=2e-11,atol=2e-13);Y=sol.y
    ck('integration seed '+str(eps),sol.success,'numerical');NB=np.sum(abs(Y[16:32])**2,axis=0);N=np.sum(abs(Y)**2,axis=0)
    ck('norm conservation seed '+str(eps),max(abs(N-1))<2e-8,'numerical');ck('energy conservation seed '+str(eps),max(abs(np.array([energy(y,1) for y in Y.T])-energy(ini,1)))<2e-8,'numerical');ck('O dark seed '+str(eps),max(abs(Y[32]))<1e-10,'numerical')
    if eps:
        # compare predicted exponential in the linear regime where amplification is substantial but small
        mask=(times>.03)&(eps*np.exp(rate*times)<.0007)
        err=max(abs(np.sqrt(NB[mask])/(eps*np.exp(rate*times[mask]))-1));ck('early linear seed amplification '+str(eps),err<.005,'numerical')
        ck('seed recruitment finite-time witness '+str(eps),NB.max()>0.001,'numerical')
    else:ck('empty B remains empty',NB.max()<1e-18,'numerical')
    print('SEED',eps,'peak NB',NB.max())
    rows.extend(zip(np.full(len(times),eps),times,NB,np.sum(abs(Y[28:32])**2,axis=0)))
rows=np.array(rows);np.savetxt(P/'seed_aperture_trajectories.csv',rows,delimiter=',',header='seed,time,NB,NBcentral',comments='')
# Random coherent exposure test and rigorous mixture inequalities with floating samples.
rng=np.random.default_rng(20261126);lam,U=np.linalg.eigh(Cn);norm2=max(lam**2);taus=lam**2/norm2
for j in range(32):
    B=rng.normal(size=16)+1j*rng.normal(size=16);B/=np.linalg.norm(B);w=abs(U.T@B)**2;m0=w@taus
    ck('spectral aperture identity '+str(j),abs(m0-np.vdot(B,Cn@Cn@B).real/norm2)<2e-14,'numerical')
    ck('spectral aperture bounds '+str(j),0<=m0<=1+1e-14,'numerical')
    for xx in [.001,.1,1,10,1000]:
        mixture=w@(xx/(xx+taus));lo=xx/(xx+m0);hi=1-m0/(1+xx)
        ck('mixture bracket '+str(j)+' '+str(xx),lo-2e-14<=mixture<=hi+2e-14,'numerical')
print('NATIVE C spectral squared / maximum',taus)
# Publication-style figure with two separate mathematical findings.
fig,ax=plt.subplots(1,2,figsize=(12,4.4),layout='constrained')
for eps in [1e-8,1e-6,1e-4]:
    r=rows[rows[:,0]==eps];ax[0].semilogy(r[:,1],np.maximum(r[:,2],1e-20),label=f'seed {eps:g}')
ax[0].set(xlabel='Dimensionless model time',ylabel='TetB occupation',title='Seed amplification (full 33-coordinate model)');ax[0].legend();ax[0].grid(alpha=.2)
xx=np.geomspace(.001,100,500);mean=.5;ax[1].semilogx(xx,xx/(xx+mean),label='Equal partial capacities');ax[1].semilogx(xx,1-mean/(1+xx),label='Binary open/closed channels');ax[1].semilogx(xx,.5*xx/(xx+.25)+.5*xx/(xx+.75),label='Distributed capacities');ax[1].set(xlabel='Acceleration ratio x',ylabel='Effective response',title='Two previous closures bound every mixture');ax[1].legend();ax[1].grid(alpha=.2)
fig.savefig(P/'figures/aperture_and_seed.png',dpi=180);plt.close(fig)
print('TOTAL',counts,'passed',sum(counts.values()))
