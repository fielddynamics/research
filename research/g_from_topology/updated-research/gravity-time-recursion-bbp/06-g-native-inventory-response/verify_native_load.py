import sympy as s
Q=s.Rational; I=s.eye(3)
G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
x=s.Matrix([Q(1,3),1,-Q(4,15)]); lam=Q(11,10)
Mp=s.Matrix([[-2,Q(1,2),-2],[-Q(1,2),1,-1],[-5,-1,-Q(89,10)]])
C=s.Matrix([[0,-Q(1,2),0],[-Q(1,2),0,-1],[1,-3,1]])
Mm=Mp-2*C; norm=(x.T*G*x)[0]
P=I-x*x.T*G/norm; A=-(Mp-lam*I)+I-P; b=P*C*x; xg=A.inv()*b
R=(lam*I-Mm).inv(); xp=R*x
av=lambda v,w:(v.T*G*w)[0]/norm
lp=av(x,C*x); k=av(b,xg)/2 # f=1/(2 norm)
c=av(x,xp); cp=2*av(xg,xp)-av(xp,(lp*I+C)*xp)
print('norm',norm,'lambda prime',lp,'k',k,'R*x',xp.T,'c',c,float(c),'cprime',cp,float(cp),'overlap coefficient',cp/8,float(cp/8))
print('odd eigenvalues',Mm.eigenvals());print('det', (lam*I-Mm).det())
checks=[]
def ck(label,test):
 assert bool(test),label
 checks.append(label);print('PASS',len(checks),label)
ck('G self adjoints',all(M.T*G==G*M for M in [Mp,Mm,C]))
ck('stationary branch', Mp*x==lam*x)
ck('normalized overlap',lp/2==Q(59,308))
ck('orthogonal derivative',(x.T*G*xg)[0]==0)
ck('even tangent equation',(lam*I-Mp)*xg==b)
ck('odd block invertible',(lam*I-Mm).det()==-Q(167,25))
ck('odd response vector',xp==s.Matrix([-Q(479,501),-Q(1673,501),-Q(2144,2505)]))
ck('exact load curvature',c==-Q(40753,12859))
ck('exact mixed curvature',cp==Q(22223198598,8102340169))
ck('existing drive susceptibility',k==Q(42815,290521))
chi=Q(59,308);h=1/chi
coef=s.factor(cp/8/(1-h*k));print('overlap coefficient at t=1',coef,float(coef))
ck('below existing threshold',h*k<1)
# exact symmetry of 6x6 parity block under differential loading and common shift.
d,g=s.symbols('delta g',real=True); Mp_g=Mp+(g-1)*C; Mm_g=Mm-(g-1)*C
K=Mp_g.row_join(-d*I/2).col_join((-d*I/2).row_join(Mm_g)); Z=s.diag(I,-I); V=s.diag(C,-C)
ck('parity load reversal',Z*K*Z==K.subs(d,-d));ck('overlap parity even', Z*V*Z==V)
# Independent eigensolve of the full six-dimensional nonlinear stationary sector.
import numpy as np
from scipy.linalg import eigh,block_diag
from scipy.optimize import root_scalar
G6=block_diag(np.array(G,float),np.array(G,float)); V6=np.array(V,float); xx=np.r_[np.array(x,float).ravel()/np.sqrt(float(norm)),np.zeros(3)]; eye=np.eye(3)
Mpn=np.array(Mp,float); Mmn=np.array(Mm,float); Cn=np.array(C,float); ch=float(chi)
def solve(d,t):
 def at(g):
  H=np.block([[Mpn+(g-1)*Cn,-d/2*eye],[-d/2*eye,Mmn-(g-1)*Cn]])+d/2*np.eye(6)
  vals,vec=eigh(G6@H,G6); j=np.argmax(abs(xx@G6@vec)); v=vec[:,j]; u=v@G6@V6@v/2
  return vals[j],v,u
 def fun(g):
  _,_,u=at(g);return g-(1+t)*u/(t*ch+abs(u))
 gr=root_scalar(fun,x0=1,x1=1.00001,xtol=1e-13).root; e,v,u=at(gr)
 nb=(v[:3]-v[3:])@np.array(G,float)@(v[:3]-v[3:])/2
 F=2*(1+t)*(abs(u)-t*ch*np.log1p(abs(u)/(t*ch)))
 return e,u,nb,e-2*gr*u+F
for t in [.25,1.,1.5]:
 hh=2*t/(ch*(1+t)); target=float(cp/8)/(1-hh*float(k)); base=solve(0,t)
 for delta in [.0001,.0002]:
  ep,up,npb,wp=solve(delta,t);em,um,nmb,wm=solve(-delta,t)
  ck(f't={t} delta={delta}: even overlap',abs(up-um)<1e-12)
  ck(f't={t} delta={delta}: inventory linear slope',abs((npb-nmb)/(2*delta)-float(c)/2)<1e-4)
  ck(f't={t} delta={delta}: self-consistent overlap coefficient',abs((up+um-2*base[1])/(2*delta**2)-target)<1e-4)
  ck(f't={t} delta={delta}: stationary energy curvature',abs((wp+wm-2*base[3])/(2*delta**2)-float(c)/4)<1e-5)
 print('t',t,'predicted coefficient',target)
print(f'{len(checks)} checks passed')
# Total norm change n: H remains the original generator; normalized eigenvector v(g)
# but the overlap entering the existing nonlinear gain is n * (v^* G V v)/2.
def solve_norm(n,t):
 G3=np.array(G,float); x0=xx[:3]
 def at(g):
  vals,vec=eigh(G3@(Mpn+(g-1)*Cn),G3);j=np.argmax(abs(x0@G3@vec));v=vec[:,j]
  return vals[j], n*(v@G3@Cn@v)/2
 def fun(g):
  _,u=at(g);return g-(1+t)*u/(t*ch+abs(u))
 gr=root_scalar(fun,x0=1,x1=1.00001,xtol=1e-13).root
 return at(gr)
for t in [.25,1.,1.5]:
 hh=2*t/(ch*(1+t));du=ch/(1-hh*float(k));dl=hh*ch*du
 ep,up=solve_norm(1.000001,t);em,um=solve_norm(.999999,t)
 ck(f't={t}: total inventory overlap derivative',abs((up-um)/.000002-du)<1e-6)
 ck(f't={t}: total inventory frequency derivative',abs((ep-em)/.000002-dl)<1e-6)
 print('t',t,'du/dn',du,'dlambda/dn',dl)
print('exact t=1 total overlap slope',s.factor(chi/(1-h*k)))
print('exact t=1 total frequency slope',s.factor(h*chi**2/(1-h*k)))
print(f'{len(checks)} checks passed')
