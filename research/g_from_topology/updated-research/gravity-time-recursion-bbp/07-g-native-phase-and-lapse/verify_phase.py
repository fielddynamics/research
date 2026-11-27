import sympy as s
import numpy as np
from scipy.linalg import expm
Q=s.Rational; I=s.eye(3)
G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
x=s.Matrix([Q(1,3),1,-Q(4,15)]); lam=Q(11,10)
Mp=s.Matrix([[-2,Q(1,2),-2],[-Q(1,2),1,-1],[-5,-1,-Q(89,10)]])
C=s.Matrix([[0,-Q(1,2),0],[-Q(1,2),0,-1],[1,-3,1]])
D=Mp-2*C-lam*I; L=Mp-lam*I; n=(x.T*G*x)[0]; chi=Q(59,308); h=1/chi
av=lambda M:s.factor((x.T*G*M*x)[0]/n)
checks=[]
def ck(name,b):
 assert bool(b),name
 checks.append(name); print('PASS',len(checks),name)
ck('native stationary vector',L*x==s.zeros(3,1))
ck('metric self adjoint blocks', all(M.T*G==G*M for M in [L,D,C]))
ck('native overlap',av(C)/2==chi)
ck('odd determinant',D.det()==Q(167,25))
z=s.symbols('z',real=True); w=s.symbols('w',real=True)
ck('odd characteristic polynomial',s.expand(D.charpoly().as_expr().subs(D.charpoly().gen,z)-(25*z**3+380*z**2+474*z-167)/25)==0)
P=625*z**3-120700*z**2+351596*z-27889
F=av((D**2-z*I).inv()); A=-av(D*(D**2-z*I).inv())/2
ck('phase rational kernel',s.cancel(F+(48125*z**2-8627025*z+23957017)/(77*P))==0)
ck('occupation rational kernel',s.cancel(A+(36875*z**2+1994575*z-6805751)/(154*P))==0)
ck('no static phase pole',P.subs(z,0)!=0 and F.subs(z,0)==Q(3422431,306779))
ck('static population response',A.subs(z,0)==-Q(40753,25718))
ck('phase transfer vanishes at zero frequency',(s.I*w*F.subs(z,w*w)).subs(w,0)==0)
ck('all three modes participate in phase read',s.gcd(s.numer(F),s.denom(F))==1 and s.degree(s.denom(F),z)==3)
# Fixed chemical potential, full real tangent of six-complex-coordinate sector.
K=L+h/2*C*x*x.T*G*C/n
ck('real even curvature self adjoint',K.T*G==G*K)
ck('real even curvature determinant',K.det()==Q(413,50))
ck('imaginary even curvature rank two',L.rank()==2)
Hess=s.diag(G*K,G*D,G*L,G*D)
ck('real Hessian symmetric',Hess==Hess.T)
ck('rank eleven',Hess.rank()==11)
phase=s.zeros(12,1);phase[6:9,0]=x
ck('only common phase is null',Hess*phase==s.zeros(12,1))
source=s.zeros(12,1);source[0:3,0]=G*x
ck('common occupation source orthogonal to phase',(phase.T*source)[0]==0)
sourceB=s.zeros(12,1);sourceB[0:3,0]=G*x/2;sourceB[3:6,0]=-G*x/2
ck('chamber load source orthogonal to phase',(phase.T*sourceB)[0]==0)
ck('static common norm susceptibility',av(K.inv())==Q(102694,170569))
ck('inverse compressibility',2*av(K.inv())==1/Q(170569,205388))
# A constant load switched on at t=0, exact linearized solution; check against matrix exponential.
Dn=np.array(D,float); xn=np.array(x,float).ravel(); Gn=np.array(G,float); nn=float(n)
J=np.block([[np.zeros((3,3)),Dn],[-Dn,np.zeros((3,3))]])
f=np.r_[np.zeros(3),xn/2]; Jaug=np.zeros((7,7));Jaug[:6,:6]=J;Jaug[:6,6]=f
vals,vec=np.linalg.eig(Dn); vi=np.linalg.inv(vec); xp=np.linalg.solve(Dn,xn)/2
for t in [.1,1,4,13,30]:
 exact=expm(Jaug*t)[:6,6]
 cosD=vec@np.diag(np.cos(vals*t))@vi;sinD=vec@np.diag(np.sin(vals*t))@vi
 sol=np.r_[(np.eye(3)-cosD)@xp,sinD@xp]
 ck(f'step response at {t}',np.max(np.abs(exact-sol))<1e-10)
# General gauge invariant source Ward identity: differential of a phase-invariant quadratic is orthogonal to i psi.
# Symbolic two-coordinate arbitrary Hermitian witness.
a,b,c,d,r,t,p,q=s.symbols('a b c d r t p q',real=True); v=s.Matrix([a+s.I*b,c+s.I*d]); V=s.Matrix([[r,p+s.I*q],[p-s.I*q,t]])
E=s.expand((v.conjugate().T*V*v)[0]); ward=s.Matrix([-b,a,-d,c]); grad=s.Matrix([s.diff(E,x) for x in [a,b,c,d]])
ck('phase Ward identity for arbitrary Hermitian energy',s.simplify((ward.T*grad)[0])==0)
# General uniform lapse rescaling: stationary condition N(grad E - lambda grad norm)=0; envelope W(N)=NW(1).
N=s.symbols('N',positive=True); E0=s.symbols('E0',real=True); u=s.symbols('u',real=True)
ck('lapse energy derivative',s.diff(N*E0,N)==E0)
ck('log lapse derivative',s.diff(s.exp(u)*E0,u)==s.exp(u)*E0)
print('odd eigenfrequencies:',sorted(abs(float(v)) for v in vals))
print('relative phase low-frequency coefficient:',float(F.subs(z,0)))
print(f'{len(checks)} checks passed')
