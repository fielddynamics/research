import sympy as s
import numpy as np
from itertools import permutations
from native_geometry import H,idx,base,F
Q=s.Rational; I=s.eye; checks=[]
def ck(name,b):
 assert bool(b),name
 checks.append(name); print('PASS',name,flush=True)
def eq(name,a,b):ck(name,s.simplify(a-b)==0)
# 1. Native invariant sector and nested boundary invisibility.
pairs=list(permutations(range(4),2)); R=s.Matrix(4,12,lambda i,j:int(pairs[j][0]==i)); C=s.Matrix(4,12,lambda i,j:int(pairs[j][1]==i)); T=s.Matrix(12,12,lambda i,j:int(pairs[i]==pairs[j][::-1])); V=s.Matrix.hstack(*((R.col_join(C)).col_join(T-I(12))).nullspace()); ck('two symmetric row-column dark directions',V.cols==2)
J=s.Matrix.hstack(*[I(36)[:,[idx[i+g,j+g] for i,j in pairs]]*V for g in (0,4)]); HH=s.Matrix(H); E=I(36)[:,base]; P=s.Matrix(np.column_stack([f@np.array([1,1,1,6]) for f in F])); M=I(2).row_join(-I(2)).col_join((-I(2)).row_join(I(2)))
ck('native Stage IX invariant two-chamber sector',HH*J==J*M);ck('rank four sector',J.rank()==4);ck('central interface dark',E.T*J==s.zeros(8,4));ck('filtered outward interface dark',P.T*J==s.zeros(8,4)); ck('two zero and two positive energy eigenmodes',M.eigenvals()=={0:2,2:2})
for n in (2,3,4):
 L=s.diag(*[3**i*HH for i in range(n)]); B=E*P.T
 for i in range(n-1):
  L[i*36:(i+1)*36,(i+1)*36:(i+2)*36]=-B
  L[(i+1)*36:(i+2)*36,i*36:(i+1)*36]=-B.T
 for i in range(n):
  X=s.zeros(n*36,4);X[i*36:(i+1)*36,:]=J
  ck(f'isolated dark block depth {n} level {i}',L*X==3**i*X*M)
# 2. Exact recursion sensitivity.
z,g,m,e,p,a,b=s.symbols('z gamma m e p a b'); Fm=lambda x:p+g*g*m*m*x/(1-g*g*e*x)
eq('exact difference of recursive Mobius maps',Fm(a)-Fm(b),g*g*m*m*(a-b)/((1-g*g*e*a)*(1-g*g*e*b)))
D0=z**3+6*z*z-11*z-24; D1=z**4+2*z**3-19*z*z-4*z+32
ps=[(13*z*z+15*z-8)/(13*D0),(39*z**3-13*z*z-84*z+32)/(39*D1)]; ms=[6*z*(z+2)/(s.sqrt(39)*D0),2*z*(3*z*z+z-8)/(s.sqrt(39)*D1)]; es=[z*(z+3)/D0,z*(z*z+z-4)/D1]
for j in (0,1):
 eq(f'grade {j} p0',ps[j].subs(z,0),Q(1,39));eq(f'grade {j} m0',ms[j].subs(z,0),0);eq(f'grade {j} m slope',s.diff(ms[j],z).subs(z,0),-1/(2*s.sqrt(39)));eq(f'grade {j} e0',es[j].subs(z,0),0)
 base_series=[s.series(q,z,0,9).removeO() for q in (ps[j],ms[j],es[j])]
 # Explicit leading coefficient of adding depth d, series arithmetic on polynomials.
 for depth in (1,2,3,4):
  order=2*depth+1
  def trunc(poly):return s.Poly(s.expand(poly),z).rem(s.Poly(z**order,z)).as_expr()
  def inv(poly):
   cc=poly.subs(z,0); h=trunc(1-poly/cc); term=1; result=1
   for k in range(1,order):term=trunc(term*h);result+=term
   return trunc(result/cc)
  # Local Taylor series independent of coupling; epsilon_i=3^i, gamma_i=1.
  loc=[]
  for i in range(depth+1):
   # derive Taylor at base once per grade, then rescale
   loc.append([trunc(q.subs(z,z/3**i)/3**i) for q in base_series])
  def response(last,scaled=False):
   B=loc[last][0]
   for i in reversed(range(last)):
    pp,mm,ee=loc[i];factor=3**(2*i) if scaled else 1;B=trunc(pp+trunc(factor*B*mm*mm)*inv(trunc(1-factor*B*ee)))
   return B
  diff=trunc(response(depth)-response(depth-1)); target=Q(1,39*3**depth)*s.prod(Q(1,156*3**(4*i)) for i in range(depth))*z**(2*depth)
  eq(f'grade {j} depth {depth} leading change',diff,target)
  diff=trunc(response(depth,True)-response(depth-1,True));target=Q(1,39*156**depth*3**(depth**2))*z**(2*depth)
  eq(f'grade {j} depth {depth} selfsimilar leading change',diff,target)
# 3. BBP entropy in odds coordinate and comparison with inherited cost.
v=s.symbols('v',real=True); pplus=(1+s.tanh(v))/2;pminus=1-pplus
ck('probability normalization',s.simplify(pplus+pminus)==1);eq('odds are exp(2v)',(pplus/pminus).rewrite(s.exp),s.exp(2*v))
eq('paired deficit derivative equals tanh',s.diff(s.log(s.cosh(v)),v),s.tanh(v));eq('paired deficit curvature at balance',s.diff(s.log(s.cosh(v)),v,2).subs(v,0),1)
b=s.symbols('b',real=True); d=-s.log(1-b*b)/2; w=-b-s.log(1-b)
eq('BBP paired vacancy slope',s.diff(d,b),b/(1-b*b));eq('one-sided vacancy slope',s.diff(w,b),b/(1-b));eq('different odds constitutive slopes',s.diff(w-d,b),b*b/(1-b*b))
# 4. 21 independent paired reads: additive curvature rather than product.
bs=s.symbols('b0:21',real=True); DD=sum(-s.log(1-t*t)/2 for t in bs); zero=dict.fromkeys(bs,0); ck('21-register Hessian is identity',s.hessian(DD,bs).subs(zero)==I(21));eq('uniform collective curvature is 21',s.diff(DD.subs(dict.fromkeys(bs,b)),b,2).subs(b,0),21)
# 5. Universal metric source versus rescaling of uncalibrated gradient stiffness.
k,c,aa,rho,kk,lam=s.symbols('k c a rho kappa lambda',nonzero=True); q=s.symbols('q'); energy=kk*k*k*q*q/2+rho*c*c*aa*q
qstar=s.solve(s.diff(energy,q),q)[0];eq('static physical lapse response',aa*qstar,-rho*c*c*aa**2/(kk*k*k));eq('coordinate rescaling leaves susceptibility', (aa/lam)**2/(kk/lam**2),aa**2/kk);eq('physical stiffness scaling changes coupling',aa**2/(lam*kk),(aa**2/kk)/lam)
print('TOTAL',len(checks),flush=True)
