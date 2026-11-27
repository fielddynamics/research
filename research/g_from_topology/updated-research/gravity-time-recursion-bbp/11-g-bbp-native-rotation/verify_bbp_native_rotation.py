import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
from itertools import permutations
Q=s.Rational; I=s.I; checks=[]
def ck(name,v):
 assert bool(v),name
 checks.append(name); print('PASS',name)
def eq(name,a,b):ck(name,s.simplify(s.trigsimp(a-b))==0)
e,th,z=s.symbols('e theta z',real=True)
R=(1-2*e-e**2)/(1+e**2); r=s.cos(th)-s.sin(th)
eq('half-angle reduction',r.subs(th,2*s.atan(e)),R)
eq('complementary quadrature norm',r**2+(s.cos(th)+s.sin(th))**2,2)
S=s.pi+2*th+2*s.log(r)
eq('BBP angular closure',S.subs(th,0),s.pi)
eq('BBP angular stationarity',s.diff(S,th).subs(th,0),0)
eq('BBP angular curvature',s.diff(S,th,2).subs(th,0),-4)
eq('BBP curvature in x',s.diff(S.subs(th,2*s.atan(e)),e,2).subs(e,0),-16)
eq('start of BBP path',S.subs(th,-s.pi/2),0)
eq('time-reversed read difference',r-r.subs(th,-th),-2*s.sin(th))
eq('even arithmetic read', (r+r.subs(th,-th))/2,s.cos(th))
eq('even geometric read squared',r*r.subs(th,-th),s.cos(2*th))
eq('even log slope',s.diff(s.log(s.cos(th)),th).subs(th,0),0)
eq('even log product curvature',s.diff(s.log(s.cos(2*th))/2,th,2).subs(th,0),-2)
# Stage VII matrices, using factorization's row/column conventions and inherited weights.
pairs=list(permutations(range(4),2)); Rm=s.Matrix(4,12,lambda i,j:int(pairs[j][0]==i)); Qm=s.Matrix(4,12,lambda i,j:int(pairs[j][1]==i)); T=s.Matrix(12,12,lambda i,j:int(pairs[i]==pairs[j][::-1])); K=s.ones(4)-s.eye(4)
Hl=(s.eye(12)-Rm.T*Rm).row_join(-2*Rm.T).col_join((-2*Rm).row_join(-Q(99,10)*s.eye(4)))
C=(-T/2).row_join(-Qm.T).col_join((-Qm).row_join(-K))
V=(Rm.col_join(Qm)).col_join(T-s.eye(12)).nullspace();ck('native symmetric row-column dark dimension',len(V)==2)
for j,w in enumerate(V):
 v=w.col_join(s.zeros(4,1)); ck(f'local eigenvector {j}',Hl*v==v);ck(f'cross eigenvector {j}',C*v==-v/2);ck(f'origin and filtered reads dark {j}',Rm*w==s.zeros(4,1) and Qm*w==s.zeros(4,1))
# Exact Bloch commutator identities.
X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-I],[I,0]]); Z=s.diag(1,-1); Om=s.symbols('Omega',real=True); H=s.eye(2)+Om*X
ck('population derivative',I*(H*Z-Z*H)==2*Om*Y)
ck('coherent quadrature derivative',I*(H*Y-Y*H)==-2*Om*Z)
ck('real overlap conserved',H*X-X*H==s.zeros(2))
# Energy along native orbit: fixed total norm n, fixed X, u=-X/4.
A,B=s.symbols('A B', real=True); a=A*s.cos(th/2)-I*B*s.sin(th/2); b=B*s.cos(th/2)-I*A*s.sin(th/2)
eq('native norm invariant',a*s.conjugate(a)+b*s.conjugate(b),A*A+B*B)
eq('native overlap invariant',s.re(s.conjugate(a)*b),A*B)
eq('native Z',a*s.conjugate(a)-b*s.conjugate(b),(A*A-B*B)*s.cos(th))
eq('native Y',2*s.im(s.conjugate(a)*b),-(A*A-B*B)*s.sin(th))
# Numerically integrate existing nonlinear constitutive law, not the closed-form rotation.
chi=59/308
for sat in (.25,1.,1.5):
 for aa,bb in ((.8,.6),(.6,.8)):
  init=np.array([aa,bb],complex); u0=sat*chi
  def gain(u):return (1+sat)*u/(u0+abs(u))
  def fun(t,v):
   u=-.5*np.real(np.conj(v[0])*v[1]); return -1j*(v-.5*gain(u)*v[::-1])
  def energy(v):
   u=-.5*np.real(np.conj(v[0])*v[1]); return np.sum(abs(v)**2)+2*(1+sat)*(abs(u)-u0*np.log1p(abs(u)/u0))
  ts=np.linspace(0,1,201); v=solve_ivp(fun,(0,1),init,t_eval=ts,rtol=1e-11,atol=1e-13).y
  omega=-.5*gain(-.5*aa*bb); angle=2*omega*ts; zz=abs(v[0])**2-abs(v[1])**2; yy=2*np.imag(np.conj(v[0])*v[1]); rr=(zz+yy)/(aa*aa-bb*bb)
  ck(f'nonlinear orbit projection {sat} {aa}',np.max(abs(rr-(np.cos(angle)-np.sin(angle))))<1e-9)
  ck(f'nonlinear orbit energy constant {sat} {aa}',np.max(abs(energy(v[:,0])-np.array([energy(w) for w in v.T])))<1e-9)
# Inherited recursive native boundary functions. Equal static read is NOT BBP's modulus slope.
d0=z**3+6*z*z-11*z-24; d1=z**4+2*z*z*z-19*z*z-4*z+32
p0=(13*z*z+15*z-8)/(13*d0); p1=(39*z**3-13*z*z-84*z+32)/(39*d1)
eq('scalar zero read',p0.subs(z,0),Q(1,39));eq('polar zero read',p1.subs(z,0),Q(1,39));eq('scalar first derivative',s.diff(p0,z).subs(z,0),-Q(7,117));eq('polar first derivative',s.diff(p1,z).subs(z,0),-Q(5,78))
l=s.log(p0/p1);eq('log scalar polar ratio slope',s.diff(l,z).subs(z,0),Q(1,6));eq('log ratio curvature',s.diff(l,z,2).subs(z,0),Q(4,9))
# Reality of coefficients implies conjugate symmetry under imaginary-axis evaluation.
for j,p in enumerate([p0,p1,p0/p1]):
 q=p.subs(z,I*z);eq(f'conjugate symmetry {j}',q.subs(z,-z),s.conjugate(q));eq(f'modulus-square slope {j}',s.diff(q*s.conjugate(q),z).subs(z,0),0)
# The time-reversal even closure deficit equals a Bernoulli relative entropy.
pminus=(1-s.sin(2*th))/2; pplus=(1+s.sin(2*th))/2
b=s.symbols('b',real=True); W=lambda v:-v-s.log(1-v)
eq('normalized squared quadrature probability minus',r**2/2,pminus)
eq('normalized squared quadrature probability plus',(s.cos(th)+s.sin(th))**2/2,pplus)
eq('probabilities sum',pminus+pplus,1)
eq('probability product',4*pminus*pplus,s.cos(2*th)**2)
eq('paired vacancy cost derivative',s.diff((W(b)+W(-b))/2,b),b/(1-b*b))
eq('paired vacancy curvature',s.diff((W(b)+W(-b))/2,b,2).subs(b,0),1)
# Log branches justified on |theta|<pi/4; differentiate to verify equality.
D=-s.log(s.cos(2*th)); avg=s.pi-(S+S.subs(th,-th))/2
KL=-s.log(2*pminus)/2-s.log(2*pplus)/2
for name,f in [('even BBP deficit',avg),('Bernoulli relative entropy',KL),('paired vacancy cost',((W(b)+W(-b))/2).subs(b,s.sin(2*th)))]:
 
 t=s.symbols('t',real=True); derivative=s.expand_trig(s.diff(f-D,th)); derivative=derivative.subs({s.sin(th):t/s.sqrt(1+t*t),s.cos(th):1/s.sqrt(1+t*t)}); eq(name+' derivative',s.cancel(derivative),0);eq(name+' reference',f.subs(th,0),0)
eq('even BBP information curvature',s.diff(D,th,2).subs(th,0),4)
print(f'{len(checks)} checks passed')
