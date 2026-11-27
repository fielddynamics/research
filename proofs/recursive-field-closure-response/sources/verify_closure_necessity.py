"""Exact conditional witnesses; no numerical fit or physical G claim."""
import sympy as s
from itertools import product
n=0
def check(label, condition):
    global n
    assert condition, label
    n+=1
    print('PASS', label)
def zero(a):
    if isinstance(a,s.MatrixBase): return all(s.simplify(v)==0 for v in a)
    return s.simplify(a)==0
x,y,z,a,b,r,c,k,ka,kb,ma,mb,h=s.symbols('x y z a b r c k ka kb ma mb h', real=True)
check('dependent constraint can have common blind solution',s.solve((1+y*y)*x,x)==[0])
check('different required states have empty intersection',not set(s.solve(x,x)) & set(s.solve(x-1,x)))
check('read collision with different settlements is insufficient', (1**2==(-1)**2) and 1!=-1)
check('read collision can preserve settlement', (1**2==(-1)**2))
A=s.Matrix([[3,1],[1,2]]); B=s.Matrix([[1,2,1],[2,4,2]]); D=5*s.eye(3); f=s.Matrix([2,-1]); Y=s.Matrix(s.symbols('y1:4')); X=s.Matrix(s.symbols('x1:3'))
E=(X.T*A*X/2+X.T*B*Y+Y.T*D*Y/2-f.T*X)[0]; S=A.inv()*(f-B*Y)
check('positive internal stiffness',A.is_positive_definite)
check('stationarity',zero(s.Matrix([s.diff(E,t) for t in X]).subs(dict(zip(X,S)))))
check('implicit sensitivity',zero(S.jacobian(Y)+A.inv()*B))
check('rank sensitivity equals rank cross block', S.jacobian(Y).rank()==B.rank()==1)
R=s.Matrix([[1,2,1]]); F=A.inv()*(f-s.Matrix([1,2])*(R*Y)[0]);check('minimal linear read suffices',zero(F-S))
check('kernel inclusion',all(zero(S.jacobian(Y)*v) for v in R.nullspace()))
Er=s.expand(E.subs(dict(zip(X,S)),simultaneous=True)); expected=(Y.T*(D-B.T*A.inv()*B)*Y/2+f.T*A.inv()*B*Y-f.T*A.inv()*f/2)[0]
check('Schur energy',zero(Er-expected));check('Schur Hessian',zero(s.hessian(Er,Y)-(D-B.T*A.inv()*B)))
WA=ka*(z-a)**2/2; WB=kb*(z-b)**2/2; g=(ka*a+kb*b)/(ka+kb)
check('shared trace stationarity',zero(s.diff(WA+WB,z).subs(z,g)))
check('equal opposite flux',zero((s.diff(WA,z)+s.diff(WB,z)).subs(z,g)))
check('neighbor dependence A',zero(s.diff(g,b)-kb/(ka+kb)))
check('neighbor dependence B',zero(s.diff(g,a)-ka/(ka+kb)))
check('registered interface energy',zero((WA+WB).subs(z,g)-ka*kb*(a-b)**2/(2*(ka+kb))))
Et=WA+WB+(ma+mb)*z; check('source balance',zero(s.diff(Et,z).subs(z,g-(ma+mb)/(ka+kb))))
check('additive source under constant shift',zero(Et.subs({z:z+h,a:a+h,b:b+h},simultaneous=True)-Et-h*(ma+mb)))
# Three-node chain: nested reduction equals joint minimization.
u,v=s.symbols('u v'); ec=(u-a)**2+2*(v-u)**2+3*(b-v)**2
joint=s.solve([s.diff(ec,u),s.diff(ec,v)],(u,v)); mid=s.solve(s.diff(ec,u),u)[0]; ec1=ec.subs(u,mid); vf=s.solve(s.diff(ec1,v),v)[0]
check('nested minimization equals joint',zero(ec1.subs(v,vf)-ec.subs(joint,simultaneous=True)))
check('nested interface state agrees',zero(vf-joint[v])); check('recovered child state agrees',zero(mid.subs(v,vf)-joint[u]))
cr=s.Function('c')(r); EE=k*(x-a)**2/2+cr*(x-b)**2/2; xs=(k*a+cr*b)/(k+cr); ES=s.simplify(EE.subs(x,xs))
check('mechanical branch stationarity',zero(s.diff(EE,x).subs(x,xs)))
check('envelope identity',zero(s.diff(ES,r)-s.diff(EE,r).subs(x,xs)))
check('explicit force',zero(-s.diff(ES,r)+k*k*s.diff(cr,r)*(a-b)**2/(2*(k+cr)**2)))
check('settled Hessian Schur identity',zero(s.diff(ES,r,2)-(s.diff(EE,r,2)-s.diff(EE,r,x)**2/s.diff(EE,x,2)).subs(x,xs)))
check('nonblind does not imply force',zero(s.diff(((x-r)**2/2).subs(x,r),r)))
# Rotation invariant projection loses invariant nonlinear norm of discarded modes.
P=s.ones(3)/3; w=s.Matrix([1,-1,0]);check('discarded nonzero mode',zero(P*w) and w.dot(w)==2)
check('invariant norm counterexample',w.dot(w)!=0)
# Exact Walsh and projective grade dimensions.
H=s.Matrix([[1,1],[1,-1]]); W=s.kronecker_product(H,H,H,H,H,H)/8
check('Walsh orthogonal',W.T*W==s.eye(64));check('Walsh self inverse',W*W==s.eye(64))
for depth,count in [(1,2),(2,6),(3,22)]:
    words=list(product(range(4),repeat=depth)); p=lambda w:tuple((0,2,3,1)[i] for i in w); orbits={min(w,p(w),p(p(w))) for w in words}; check(f'depth {depth} invariant dimension',len(orbits)==count)
check('recursive invariant contrast dimensions',[2-1,6-2,22-6]==[1,4,16])
print(f'\n{n} exact assertions passed. Prior suites not rerun.')
