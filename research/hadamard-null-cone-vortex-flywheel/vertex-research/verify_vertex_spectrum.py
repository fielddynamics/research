"""Exact registration, spectral and nonlinear time-face research. No new physical parameters.
Run from any directory with numpy scipy sympy matplotlib.  All new coefficients
in the dynamical scans are explicitly illustrative dimensionless probes.
"""
from itertools import permutations, combinations
from pathlib import Path
import sympy as s
import numpy as np
from scipy.linalg import eigvals, expm
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent
counts={'exact':0,'numeric':0}
def check(name,b,kind='exact'):
    assert bool(b),name
    counts[kind]+=1;print('PASS',kind,name)
def eq(A,B):return (A-B).applyfunc(s.simplify)==s.zeros(*A.shape)
I=range(4); pairs=list(permutations(I,2)); addr=pairs+[(i,i) for i in I]; ix={p:i for i,p in enumerate(addr)}
R=s.Matrix(4,12,lambda i,j:int(pairs[j][0]==i)); Q=s.Matrix(4,12,lambda i,j:int(pairs[j][1]==i)); T=s.Matrix(12,12,lambda i,j:int(pairs[i]==pairs[j][::-1])); K=s.ones(4)-s.eye(4)
d,a,k,t=s.symbols('d a k t',real=True); C=(d*T).row_join(a*Q.T).col_join((a*Q).row_join(k*K)); C0=C.subs({d:-s.Rational(1,2),a:-1,k:-1})
U=[]
for p in permutations(I):U.append(s.Matrix(16,16,lambda i,j:int(addr[i]==tuple(p[x] for x in addr[j]))))
# independent relabelling invariants, exactly two uniform orbit vectors per chamber
Pfix=sum(U,s.zeros(16))/24
check('fixed projector',Pfix**2==Pfix and Pfix.rank()==2)
check('independent relabel averaging',sum((u*C for u in U),s.zeros(16))/24==Pfix*C)
check('double average no spatial contrast',Pfix*C*Pfix==Pfix*C and (Pfix*C*Pfix).rank()==2)
for j,u in enumerate(U):
    check(f'common registration equivariance {j}',u*C*u.T==C)
    check(f'independent registered kernel covariance {j}',u.T*(u*C)==C)
# Geometry relative frame map.  Relative proper rotation L and P parity.
M=s.Matrix([[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])
G=4*s.eye(4)-s.ones(4); Pw=G/4
check('frame Gram',M.T*M==G and M*M.T==4*s.eye(3))
for j,p in enumerate(permutations(range(3))):
    L=s.eye(3)[:,list(p)]
    if L.det()<0:L[:,0]=-L[:,0]
    MB=-L*M; Jrel=M.T*MB/4
    check(f'root blind rotated partner {j}',MB.T*MB==G)
    check(f'relative Gram partial isometry {j}',Jrel.T*Jrel==Pw and Jrel*Jrel.T==Pw)
    check(f'relative map reconstructs orientation {j}',-M*Jrel*M.T/4==L)
check('parity-aligned cross Gram',M.T*(-M)/4==-Pw)
# 2 uniform, E (symmetric dark 2), T1 (antisym dark 3), T2 x3 (9).
Z=s.Matrix.hstack(*R.col_join(Q).nullspace()); check('common row column dark rank five',Z.cols==5)
check('dark split 2+3',( (s.eye(12)+T)*Z).rank()==2 and ((s.eye(12)-T)*Z).rank()==3)
Zfull=Z.col_join(s.zeros(4,5)); check('dark subspace sees only transpose',C*Zfull==(d*T*Z).col_join(s.zeros(4,5)))
S=s.Matrix.hstack(s.ones(12,1).col_join(s.zeros(4,1))/s.sqrt(12),s.zeros(12,1).col_join(s.ones(4,1))/2)
Sblock=s.Matrix([[d,s.sqrt(3)*a],[s.sqrt(3)*a,3*k]])
check('uniform block',eq(C*S,S*Sblock))
E=s.zeros(16,9)
for j,(i,l) in enumerate(pairs):E[j,0:3]=M[:,i].T;E[j,3:6]=M[:,l].T
E[12:16,6:9]=M.T
MC=s.Matrix([[0,d,0],[d,0,a],[-a,3*a,-k]])
check('triplet block',C*E==E*s.kronecker_product(MC,s.eye(3)))
check('complete orthogonal decomposition',S.T*E==s.zeros(2,9) and Zfull.T*E==s.zeros(5,9) and S.T*Zfull==s.zeros(2,5) and S.row_join(Zfull).row_join(E).rank()==16)
polyU=s.factor((t*s.eye(2)-Sblock).det());polyT=s.factor((t*s.eye(3)-MC).det());poly=(t-d)**2*(t+d)**3*polyU*polyT**3
print('uniform characteristic:',polyU,'triplet characteristic:',polyT)
check('full charpoly witness',s.expand(C0.charpoly(t).as_expr().subs({s.Symbol('t'):t})-poly.subs({d:-s.Rational(1,2),a:-1,k:-1}))==0 if C0.charpoly(t).gen==t else s.Poly(C0.charpoly().as_expr()).all_coeffs()==s.Poly(poly.subs({d:-s.Rational(1,2),a:-1,k:-1}),t).all_coeffs())
# Frequency grade projection in ordered digit read, test scale mixing.
P0=s.ones(4)/4; P1=s.eye(4)-P0
W=s.Matrix(16,16,lambda i,j:int(addr[j]==divmod(i,4)))
Pgrades=[W.T*s.kronecker_product(P0,P0)*W,W.T*(s.kronecker_product(P0,P1)+s.kronecker_product(P1,P0))*W,W.T*s.kronecker_product(P1,P1)*W]
check('grade ranks',[p.rank() for p in Pgrades]==[1,6,9]);check('grade sum',sum(Pgrades,s.zeros(16))==s.eye(16))
for i,j in combinations(range(3),2):
    z=Pgrades[i]*C*Pgrades[j]; print('grade mixing',i,j,'squared Frobenius',s.factor(s.trace(z.T*z)))
    check(f'grade cross block {i} {j} witness nonzero',z.subs({d:-s.Rational(1,2),a:-1,k:-1})!=s.zeros(16)) if (i,j)!=(0,1) else check('scalar first contrast prohibited',z==s.zeros(16))
# common junction law: exact factorization via twelve registered lateral records
L=s.eye(12).row_join(a/d*T*Q.T)
check('one 12 record junction plus Schur residual',eq(C,d*L.T*T*L+s.diag(s.zeros(12),(k-a*a/d)*K)))
check('shared junction rank twelve',C.subs(k,a*a/d).subs({a:2,d:1}).rank()==12)
# passive same read cannot realize indefinite kernel through positive Gram, phase signs required
check('witness cross inertia via LDL',C0.det()==-s.Rational(3,4096))
cn=np.array(C0,float); eig=np.linalg.eigvalsh(cn);check('spectral witness inertia',sum(eig>1e-9)==7 and sum(eig<-1e-9)==9,'numeric')
# Positive Gram and passive phase twist, polar factorization C=|C|^(1/2) S |C|^(1/2)
val,V=np.linalg.eigh(cn); amp=(V*np.sqrt(abs(val)))@V.T; phase=(V*np.sign(val))@V.T
check('phase twist unitary',np.max(abs(phase@phase-np.eye(16)))<1e-12,'numeric');check('phase matched factorization',np.max(abs(amp@phase@amp-cn))<1e-12,'numeric')
# General quartic relative phase: pair law alone cannot seed empty; norm-assisted single exchange can.
x,y,u,v=s.symbols('x y u v',real=True); A=x+s.I*y; B=u+s.I*v; chi=s.conjugate(A)*B; N=A*s.conjugate(A)+B*s.conjugate(B)
lam,kap,g,delta=s.symbols('lambda kappa gamma Delta',real=True)
HH=s.expand(lam*chi*s.conjugate(chi)+kap*s.re(chi**2)+g*N*s.re(chi)+delta*B*s.conjugate(B))
rate=lambda H,x,y:s.expand(x*s.diff(H,y)-y*s.diff(H,x))
check('one quartic law total conservation',s.simplify(rate(HH,x,y)+rate(HH,u,v))==0)
check('single and pair transfer rates',s.simplify(rate(HH,x,y)-2*kap*s.im(chi**2)-g*N*s.im(chi))==0)
check('seed empty partner',s.simplify(s.diff(HH,u).subs({u:0,v:0})-g*(x*x+y*y)*x)==0)
# Scalar exact phase portrait on norm 1: p=N_B, phi=arg B-arg A.
p=s.symbols('p',positive=True); ph=s.symbols('phi',real=True); Zp=s.sqrt(p*(1-p)); Hred=delta*p+p*(1-p)*(lam+kap*s.cos(2*ph))+g*Zp*s.cos(ph)
# phi dot = -H_p; p dot=H_phi (canonical convention)
check('reduced transfer matches Hamiltonian derivative',s.simplify(s.diff(Hred,ph)+2*kap*p*(1-p)*s.sin(2*ph)+g*Zp*s.sin(ph))==0)
# phase lock balanced with no detuning; exact Hessian at p=1/2, phi=0
Hpp=s.simplify(s.diff(Hred,p,2).subs({p:s.Rational(1,2),ph:0})); Hff=s.simplify(s.diff(Hred,ph,2).subs({p:s.Rational(1,2),ph:0})); check('balanced fixed point zero gradient if detuning zero',s.diff(Hred,p).subs({p:s.Rational(1,2),ph:0,delta:0})==0)
check('balanced Hessian population',s.simplify(Hpp+2*(lam+kap+g))==0);check('balanced Hessian phase',s.simplify(Hff+kap+g/2)==0)
print('linear lock frequency squared',s.factor(Hpp*Hff))
# Nonzero phase branch if cos(phi)=-g/(4 kap sqrt(p(1-p))) ; p=1/2 -> -g/(2kap)
# Full 33 graph stationary witness; vary lambda-kappa keeping beta=lambda+kappa.
AA=np.zeros((16,16)); AA[12:,12:]=-9.9*np.eye(4)
for i,(a1,b1) in enumerate(pairs):
    AA[i,12+a1]=AA[12+a1,i]=-2
    for j,(a2,b2) in enumerate(pairs):
        if a1==a2 and b1!=b2:AA[i,j]=-1
Hloc=np.zeros((33,33));Hloc[:16,:16]=Hloc[16:32,16:32]=AA;Hloc[12:16,32]=Hloc[32,12:16]=-1;Hloc[28:32,32]=Hloc[32,28:32]=-1
q=np.array(M.T,float)@np.array([1,1j,0])/np.sqrt(2)
p0=np.sqrt(3)/8*np.sqrt(75/77)*np.r_[np.array([q[i]/3+q[j] for i,j in pairs]),-4*q/15];psi=np.r_[p0,p0,0j]; E0=1.1
ch=np.vdot(p0,cn@p0).real;beta=1/ch
check('stationary norm',abs(np.vdot(psi,psi)-1)<1e-12,'numeric');print('stationary overlap',ch,'beta',beta)
# real tangent gradient, exact formula validated by finite differences
v0=cn@p0
def grad(y,lam,kap):
    A,B=y[:16],y[16:32];chi=np.vdot(A,cn@B);coef=lam*chi.conjugate()+kap*chi
    g=Hloc@y;g[:16]+=coef*(cn@B);g[16:32]+=coef.conjugate()*(cn@A);return g-E0*y
def jac_action(h,lam,kap):
    a,b=h[:16],h[16:32];dc=np.vdot(a,v0)+np.vdot(p0,cn@b);cf=lam*dc.conjugate()+kap*dc
    g=Hloc@h-E0*h;g[:16]+=cn@b+cf*v0;g[16:32]+=cn@a+cf.conjugate()*v0;return -1j*g

def pack(z):return np.r_[z.real,z.imag]
def unpack(z):return z[:33]+1j*z[33:]
def jac(lam,kap):return np.column_stack([pack(jac_action(unpack(e),lam,kap)) for e in np.eye(66)])
rng=np.random.default_rng(26)
for ratio in [-2,-1,0,0.5,1,2]:
    kap=ratio*beta;lam=beta-kap
    check(f'same stationary branch {ratio}',np.linalg.norm(grad(psi,lam,kap))<1e-12,'numeric')
    h=rng.normal(size=33)+1j*rng.normal(size=33);eps=1e-6
    fd=-1j*(grad(psi+eps*h,lam,kap)-grad(psi-eps*h,lam,kap))/(2*eps)
    check(f'analytic tangent {ratio}',np.linalg.norm(fd-jac_action(h,lam,kap))<1e-7,'numeric')
ratios=np.linspace(-3,3,241);growth=[]
for ratio in ratios:
    kap=ratio*beta;lam=beta-kap; j=jac(lam,kap); ev=eigvals(j);growth.append(max(ev.real));check(f'linear Hamiltonian trace {ratio:.3f}',abs(np.trace(j))<1e-9,'numeric')
print('scan min max growth',min(growth),max(growth),'argmin',ratios[np.argmin(growth)])
# same even subspace, varies only transverse stability. Separate even/odd spectrum.
# even perturbation includes scalar; odd scalar zero. use normalized embedding maps.
Ve=np.zeros((33,17)); Vo=np.zeros((33,16)); Ve[:16,:16]=Ve[16:32,:16]=np.eye(16)/np.sqrt(2);Ve[32,16]=1;Vo[:16]=np.eye(16)/np.sqrt(2);Vo[16:32]=-np.eye(16)/np.sqrt(2)
from scipy.linalg import block_diag
Ee=block_diag(Ve,Ve);Oo=block_diag(Vo,Vo)
for ratio in [-2,0,1,2]:
    kap=ratio*beta;lam=beta-kap; j=jac(lam,kap)
    check(f'parity tangent block {ratio}',np.linalg.norm(Ee.T@j@Oo)<1e-12 and np.linalg.norm(Oo.T@j@Ee)<1e-12,'numeric')
    print('parity growth',ratio,max(eigvals(Ee.T@j@Ee).real),max(eigvals(Oo.T@j@Oo).real))
np.savetxt(P/'vertex_stability_scan.csv',np.c_[ratios,growth],delimiter=',',header='kappa_over_beta,max_real_linear_eigenvalue',comments='')
fig,ax=plt.subplots(figsize=(8,4.4),layout='constrained');ax.plot(ratios,growth,lw=2);ax.set(xlabel='κ / (λ + κ), stationary coupling fixed',ylabel='Maximum real tangent eigenvalue',title='Stability diagnostic of the same stationary flywheel');ax.grid(alpha=.25);fig.savefig(P/'figures/vertex_stability_scan.png',dpi=180);plt.close(fig)
# Exact instability and sharp curvature threshold in the fixed-z balanced sector.
Gm=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
xstar=s.Matrix([s.Rational(1,3),1,-s.Rational(4,15)])
Ma=s.Matrix([[-2,1,-2],[0,1,0],[-6,2,-s.Rational(99,10)]])
Mc=MC.subs({d:-s.Rational(1,2),a:-1,k:-1}); f=s.Rational(225,1232)
chi=(f*xstar.T*Gm*Mc*xstar)[0]; L=Ma+Mc-s.Rational(11,10)*s.eye(3)
check('exact stationary overlap',chi==s.Rational(59,308) and 2*f*(xstar.T*Gm*xstar)[0]==1)
check('exact stationary kernel and metric symmetry',L*xstar==s.zeros(3,1) and Gm*L==L.T*Gm and Gm*Mc==Mc.T*Gm)
check('two negative nonzero L eigenvalues',s.factor(L.charpoly().as_expr())==s.factor(L.charpoly().gen*(L.charpoly().gen**2+s.Rational(66,5)*L.charpoly().gen+s.Rational(539,25))))
curv=s.symbols('h',real=True); Bm=L+curv*f*Mc*xstar*xstar.T*Gm*Mc; Fm=-L*Bm
la=Fm.charpoly().gen
pchar=s.factor(Fm.charpoly().as_expr()); expected=la*(la**2+(s.Rational(1802900,13750)-s.Rational(257375,13750)*curv)*la+(s.Rational(6391462,13750)-s.Rational(941930,13750)*curv))
check('exact squared tangent characteristic',s.expand(pchar-expected)==0)
hcrit=s.Rational(290521,42815); Pstar=xstar*xstar.T*Gm/(xstar.T*Gm*xstar)[0]; vec=(s.eye(3)-Pstar)*Mc*xstar
check('sharp rank-one curvature threshold',s.simplify(1/(f*(vec.T*Gm*(-L+Pstar).inv()*vec)[0])-hcrit)==0)
check('pair curvature exceeds threshold',2/chi>hcrit)
check('pair squared tangent has one positive and one negative nonzero root',s.Poly(s.cancel(pchar.subs(curv,2/chi)/la),la).TC()<0)
print('exact squared tangent pair polynomial',s.factor(pchar.subs(curv,2/chi)))
print('sharp curvature threshold',hcrit,float(hcrit))
# Existence of a flat-curvature nonlinear response, not a physical selection.
U0=s.symbols('u0',real=True); Fpot=2*U0**2/chi-s.Rational(2,3)*U0**3/chi**2
check('flat-curvature potential has no bilinear field term',s.diff(Fpot,U0).subs(U0,0)==0)
check('flat-curvature stationary slope',s.diff(Fpot,U0).subs(U0,chi)==2)
check('flat-curvature stationary Hessian',s.diff(Fpot,U0,2).subs(U0,chi)==0)

def flat_grad(y):
    A,B=y[:16],y[16:32]; u=np.vdot(A,cn@B).real; f1=2*u/float(chi)-u*u/float(chi)**2
    out=Hloc@y-E0*y;out[:16]+=f1*(cn@B);out[16:32]+=f1*(cn@A);return out
check('flat stationary vector',np.linalg.norm(flat_grad(psi))<1e-12,'numeric')
H7=Hloc.copy();H7[:16,16:32]=H7[16:32,:16]=cn
for j in range(20):
    h=rng.normal(size=33)+1j*rng.normal(size=33); eps=1e-6
    fd=(flat_grad(psi+eps*h)-flat_grad(psi-eps*h))/(2*eps)
    check(f'flat tangent equals Stage VII {j}',np.linalg.norm(fd-(H7-E0*np.eye(33))@h)<1e-7,'numeric')
# Rank-one curvature gives an exact design criterion on reduced tangent only.
cs=np.linspace(-2,13,301); ex=[]
for h in cs:
    ev=np.linalg.eigvals(np.array(Fm.subs(curv,h),float));ex.append(np.sqrt(max(0,np.max(ev.real))))
fig,ax=plt.subplots(figsize=(8,4.5),layout='constrained');ax.plot(cs,ex,lw=2,label='fixed-z balanced tangent');ax.axvline(float(hcrit),ls='--',label='exact curvature threshold');ax.axvline(float(2/chi),ls=':',label='quadratic overlap');ax.set(xlabel='Vertex curvature F″(χ*)',ylabel='Maximum growth exponent',title='The stationary vertex needs saturation, not stronger overlap');ax.grid(alpha=.25);ax.legend();fig.savefig(P/'figures/vertex_curvature_threshold.png',dpi=180);plt.close(fig)
np.savetxt(P/'vertex_curvature_scan.csv',np.c_[cs,ex],delimiter=',',header='curvature,max_growth_fixed_z_balanced',comments='')
# Grade separation obstruction: both cross-grade norms vanish iff zero parameters.
check('grade separation forces a=d=k=0',s.solve([a,d+k,2*a-d+3*k],[a,d,k])=={a:0,d:0,k:0})
print('TOTAL',counts)
