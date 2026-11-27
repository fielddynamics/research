from native_geometry import *
from functools import lru_cache
z=sp.symbols('z'); H=sp.Matrix(H); P=sp.Matrix(np.column_stack([f@np.array([1,1,1,6]) for f in F])); E=sp.eye(36)[:,base]; I=sp.eye
checks=0
def ck(label,b):
 global checks
 assert bool(b),label
 checks+=1; print('PASS',checks,label,flush=True)
def eq(a,b):return sp.cancel(a-b)==0
ck('eight disjoint normalized port records',P.T*P==39*I(8)); ck('eight face records', E.T*E==I(8)); ck('central component of each port',E.T*P==6*I(8)); ck('face to child corner geometry',np.allclose(pos[base],S/3))
# Character sectors: exact joint Krylov subspace and reduced resolvent, normalization P/sqrt39.
@lru_cache(None)
def response(bits):
 a=sp.Matrix([int(np.prod([s[j] for j in bits])) for s in S]); v=P*a; w=E*a; basis=[]
 for init in (v,w):
  x=init
  while sp.Matrix.hstack(*basis,x).rank()>len(basis):
   basis.append(x); x=H*x
 Q=sp.Matrix.hstack(*basis); A=Q.gauss_jordan_solve(H*Q)[0]; M=sp.Matrix.hstack(v,w); X=Q.gauss_jordan_solve(M)[0]; g=(M.T*Q*(z*I(len(basis))-A).inv()*X/8).applyfunc(sp.factor)
 ck('exact invariant reduced Krylov basis '+str(bits),Q*A==H*Q and Q*X==M)
 return len(basis),g
ref=[]
for j in range(4):
 d,g=response(tuple(range(j))); ref.append(g); print('grade',j,'Krylov dim',d,'unnormalized resolvent',g)
for j in range(4):
 for bits in combinations(range(3),j):
  d,g=response(bits); ck('grade degeneracy '+str(bits),g==ref[j])
for j in (0,1):
 g=ref[j]; ck('port zero-frequency response 1/39 grade '+str(j),g[0,0].subs(z,0)==1)
 ck('face-port antiresonance grade '+str(j),g[0,1].subs(z,0)==0)
 ck('face self-response zero grade '+str(j),g[1,1].subs(z,0)==0)
 ck('mixed derivative -1/2 unnormalized grade '+str(j),sp.diff(g[0,1],z).subs(z,0)==-sp.Rational(1,2))
 ck('face derivative -1/8 grade '+str(j),sp.diff(g[1,1],z).subs(z,0)==-sp.Rational(1,8))
 # Normalized origin mode couples to E character with -sqrt8. Resolvent equation gives OE and OO.
 oe=-sp.sqrt(8)*g[1,1]/z; op=-sp.sqrt(8)*g[0,1]/(z*sp.sqrt(39)); oo=(1+8*g[1,1]/z)/z
 ck('origin-face finite nonzero read grade '+str(j),sp.limit(oe,z,0)==1/sp.sqrt(8))
 ck('origin-port finite read grade '+str(j),sp.limit(op,z,0)==sp.sqrt(8)/(2*sp.sqrt(39)))
 ck('origin self-response 1/8 grade '+str(j),sp.limit(oo,z,0)==sp.Rational(1,8))
 print('origin diagonal at zero',j,sp.limit(oo,z,0))
# Recursive projected resolvent using rank-one Woodbury formula, all quantities in physical energy units.
p,e,m,gamma,child=sp.symbols('p e m gamma child'); G=sp.Matrix([[p,m],[m,e]]); K=sp.Matrix([[0,0],[0,gamma**2*child]])
new=(I(2)-G*K).inv()*G
ck('rank-one recursion formula',eq(new[0,0],p+gamma**2*child*m**2/(1-gamma**2*child*e)))
ck('zero mixed response removes all child correction',eq(new[0,0].subs({m:0,e:0}),p))
# Finite nested matrix direct exact check for 1,2,3 levels, scalar & polar.
# z=0 resolvent can be singular on dark subspace: use reduced Krylov sector only.
for j in (0,1):
 a=sp.Matrix([int(np.prod(s[:j])) for s in S]); v=P*a; w=E*a; basis=[]
 for init in (v,w):
  x=init
  while sp.Matrix.hstack(*basis,x).rank()>len(basis):basis.append(x); x=H*x
 Q=sp.Matrix.hstack(*basis); M=Q.T*Q; A=Q.gauss_jordan_solve(H*Q)[0]; v=Q.gauss_jordan_solve(v)[0]; w=Q.gauss_jordan_solve(w)[0]; n=A.rows
 # use unnormalized v; coupling -E_unit P_unit^T / sqrt(39) instead of -E_unit P_unit^T; gamma=1/sqrt39.
 for levels in (1,2,3):
  J=sp.diag(*[3**i*A for i in range(levels)]); metric=sp.diag(*([M]*levels))
  for i in range(levels-1):
   J[i*n:(i+1)*n,(i+1)*n:(i+2)*n]=-w*v.T*M/312
   J[(i+1)*n:(i+2)*n,i*n:(i+1)*n]=-v*w.T*M/312
  ck(f'metric selfadjoint grade {j} depth {levels}',J.T*metric==metric*J)
  vv=sp.Matrix.vstack(v,sp.zeros(n*(levels-1),1)); R=(-J).inv(); ck(f'direct nested resolvent grade {j} depth {levels}',(vv.T*metric*R*vv)[0]/312==sp.Rational(1,39))
  # compare nonzero spectral parameter: avoid singular inverse, actual response changes.
  if levels>1:
   zz=sp.Rational(11,10); bare=ref[j][0,0].subs(z,zz)/39; val=(vv.T*metric*(zz*I(n*levels)-J).inv()*vv)[0]/312
   ck(f'nonzero operating frequency not protected grade {j} depth {levels}',val!=bare)
   print('finite-frequency',j,levels,float(bare),float(val))
ep,ec=sp.symbols('ep ec',positive=True)
ck('local origin correction coefficient',eq((1/sp.sqrt(8)/ep)**2*gamma**2/(39*ec),gamma**2/(312*ep**2*ec)))
ck('mixed-response quadratic leading coefficient',eq((1/(2*sp.sqrt(39)*ep**2))**2,1/(156*ep**4)))
print('TOTAL',checks)
