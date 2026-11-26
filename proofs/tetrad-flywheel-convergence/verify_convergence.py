"""Exact algebra certificates for Proof 25, not a physical simulation."""
from itertools import combinations, permutations, product
import sympy as S
n=0
def check(label, pred):
    global n
    assert bool(pred), label
    n+=1; print(f'PASS {n:03} {label}')
I=S.eye(4); one=S.ones(4,1); J=one*one.T; G=4*I-J; P=G/4
es=list(combinations(range(4),2)); ps=[(i,j) for i in range(4) for j in range(4) if i!=j]
M=S.Matrix([[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])
B=S.zeros(4,6); D=S.zeros(6,4); R=S.zeros(4,12); Q=S.zeros(4,12)
for k,(i,j) in enumerate(es): B[i,k]=-1; B[j,k]=1
for i in range(4):
    t=[j for j in range(4) if j!=i]
    for a,b in zip(t,t[1:]+t[:1]): D[es.index(tuple(sorted((a,b)))),i]=(-1)**i*(1 if a<b else -1)
for k,(i,j) in enumerate(ps): R[i,k]=1; Q[j,k]=1
C=Q*(S.eye(12)-R.T*R/3); F=S.sqrt(S.Rational(3,2))*C.T
frames={'spatial':M,'cycles':D,'row-closed':F,'cut':B.T,'intrinsic':2*P}
check('closure projector',P**2==P and P*one==S.zeros(4,1) and P.rank()==3)
for name,X in frames.items():
    check(f'{name} Gram and closure',S.simplify(X.T*X-G)==S.zeros(4) and X*one==S.zeros(X.rows,1))
for na,A in frames.items():
    for nb,Bb in frames.items():
        U=Bb*A.T/4
        check(f'canonical transport {na} -> {nb}',S.simplify(U*A-Bb)==S.zeros(Bb.rows,4) and S.simplify(U.T*U-A*A.T/4)==S.zeros(A.rows))
for na,A in frames.items():
    for nb,Bb in frames.items():
        for nc,H in frames.items():
            check(f'composition {na} -> {nb} -> {nc}',S.simplify((H*Bb.T/4)*(Bb*A.T/4)-H*A.T/4)==S.zeros(H.rows,A.rows))
check('cut and cycle are orthogonal complementary triples',B*D==S.zeros(4) and (B.T*B+D*D.T)==4*S.eye(6))
# All four triangles through distinct edges of a reference triangle. Three labels
# outside it suffice to represent every equality pattern among the extra vertices.
def edges(t): return set(combinations(sorted(t),2))
for a,b,c in product(range(3,6),repeat=3):
    ts=[(0,1,2),(0,1,a),(0,2,b),(1,2,c)]
    ee=[edges(t) for t in ts]; pairwise=all(len(x&y)==1 for x,y in combinations(ee,2))
    check(f'triangle incidence equality pattern {a,b,c}',pairwise==(a==b==c))
# Geometry in W, q=M^T x. No real-point sampling is a proof of the polytope result.
verts=[G[:,i] for i in range(4)]
mids=[(verts[i]+verts[j])/2 for i,j in es]
check('core midpoint set equals hypersimplex signs', {tuple(v) for v in mids}=={v for v in product([-1,1],repeat=4) if sum(v)==0})
check('eight directions and six pair vertices map to exact coordinates',len({tuple(M*v/4) for v in verts+[-v for v in verts]})==8 and {tuple(M*v/4) for v in mids}=={tuple(s*int(i==j) for j in range(3)) for i in range(3) for s in [-1,1]})
# Core faces are triples of pair-vertices: stars and complement triangles.
faces=[frozenset(e for e in es if i in e) for i in range(4)]+[frozenset(e for e in es if i not in e) for i in range(4)]
adj={(i,j) for i,j in combinations(range(8),2) if len(faces[i]&faces[j])==2}
check('octahedral dual is crown graph',adj=={(i,4+j) for i,j in ps})
check('all triangular cliques are eight core faces', {frozenset(t) for t in combinations(es,3) if all(set(a)&set(b) for a,b in combinations(t,2))}==set(faces))
for i,j in ps:
    e1,e2=sorted(faces[i]&faces[j+4]); v1,v2=mids[es.index(e1)],mids[es.index(e2)]
    check(f'edge midpoint indexed by ordered distinct labels {i,j}',(v1+v2)/2==(verts[i]-verts[j])/4)
# Equivariance: polar vs axial, and canonical normed transport twists.
for p in permutations(range(4)):
    T=S.zeros(4); U=S.zeros(12); E=S.zeros(6)
    for i,j in enumerate(p): T[j,i]=1
    for h,(i,j) in enumerate(ps): U[ps.index((p[i],p[j])),h]=1
    for h,(i,j) in enumerate(es):
        a,b=p[i],p[j]; E[es.index(tuple(sorted((a,b)))),h]=1 if a<b else -1
    check(f'polar/axial actions {p}',U*F==F*T and E*B.T==B.T*T and E*D==T.det()*D*T)
# Symmetry of the metric and necessity of the norm assumption.
w=S.symbols('w:6',positive=True); Gw=D.T*S.diag(*w)*D
for i,j in es:
    comp=tuple(k for k in range(4) if k not in (i,j))
    check(f'weight uniquely visible at off-diagonal {i,j}',Gw[i,j]==-w[es.index(comp)])
check('mean edge weight is exact symmetrized Gram',sum((Gw[i,i] for i in range(4)),S.Integer(0))==2*sum(w))
T=S.diag(2,1,1)*M; Tg=T.T*T
check('closure and equal magnitudes alone do not imply regularity',T*one==S.zeros(3,1) and len(set(Tg[i,i] for i in range(4)))==1 and len(set(Tg[i,j] for i,j in es))>1)
check('nonuniform edge metric violates regularity',D.T*S.diag(2,1,1,1,1,1)*D!=G)
# Exact pointwise certificate: barycentric transform and inverse on symbolic W.
x,y,z=S.symbols('x y z',real=True); q=S.Matrix([x,y,z,-x-y-z]); lam=(q+one)/4
check('barycentric inverse',S.simplify(G*lam-q)==S.zeros(4,1) and sum(lam)==1)
# Local incidence refinement inherits counting, not a new independent proof.
check('depth-two address counts',4*4*4==64 and 4*10==40 and 4*6==24)
# Used by verify_convergence.py after the inherited checks; uses its definitions.
# Every assertion here uses exact arithmetic.
H=S.zeros(6)
for e,f,sgn in [(0,5,-1),(1,4,1),(2,3,-1)]: H[e,f]=H[f,e]=sgn
check('signed complementary-edge duality maps cut to cycle',H*B.T==D)
check('duality is symmetric orthogonal involution',H.T==H and H*H==S.eye(6))
check('duality exchanges complementary projectors',H*(B.T*B)*H==D*D.T)
N=S.zeros(4,6)
for k,(i,j) in enumerate(es): N[i,k]=N[j,k]=1
V=M*N/2
A=N.T*N-2*S.eye(6)
check('octahedron adjacency derived from incidence',all(A[i,j]==int(i!=j and bool(set(es[i])&set(es[j]))) for i in range(6) for j in range(6)))
check('core Gram is 2I+A-J',V.T*V==2*S.eye(6)+A-S.ones(6))
check('core has three orthogonal antipodal pairs',(V.T*V).eigenvals()=={S.Integer(2):3,S.Integer(0):3})
check('core is tight',V*V.T==2*S.eye(3))
check('unsigned incidence Gram',N*N.T==2*S.eye(4)+S.ones(4))
# Complement symmetry and orientation: actual label permutations on the oriented edge space.
for p in permutations(range(4)):
    T=S.zeros(4); E=S.zeros(6)
    for i,j in enumerate(p): T[j,i]=1
    for h,(i,j) in enumerate(es):
        a,b=p[i],p[j]; E[es.index(tuple(sorted((a,b)))),h]=1 if a<b else -1
    check(f'orientation covariance of complementary duality {p}',E*H==T.det()*H*E)
# Exact weighted anisotropy formula. The complementary-edge ordering converts the cycle Gram to a weighted Laplacian.
wbar=sum(w)/6; delta=S.Matrix([w0-wbar for w0 in w]); dev=Gw-wbar*G
# D's rows are signed complementary differences. |D|^T is the unsigned incidence on complementary labels.
deg=D.applyfunc(abs).T*delta
check('exact squared Frobenius anisotropy formula',S.expand(sum(x*x for x in dev)-2*(delta.dot(delta))-deg.dot(deg))==0)
check('weighted Gram is a Laplacian with zero constant mode',Gw*one==S.zeros(4,1))
check('metric symmetry average',S.simplify(sum((Gw.extract(p,p) for p in permutations(range(4))),S.zeros(4))/24-wbar*G)==S.zeros(4))
# Equality witnesses for sharp anisotropy constants, with positive underlying weights.
lo=S.Matrix([1,-1,0,0,-1,1]); hi=N.T*S.Matrix([1,-1,0,0]);
for label,dd,cst in [('lower',lo,2),('upper',hi,4)]:
    check(f'{label} zero-sum metric variation',sum(dd)==0)
    dG=D.T*S.diag(*dd)*D
    check(f'{label} sharp squared anisotropy factor',sum(x*x for x in dG)==cst*dd.dot(dd))
# All 14 mixed inequalities have an explicit nonzero recession direction.
for bits in product([False,True],repeat=4):
    if all(bits) or not any(bits): continue
    u=sum(bits); l=4-u; d=S.Matrix([-l if b else u for b in bits]);
    check(f'mixed sign escape {bits}',sum(d)==0 and d!=S.zeros(4,1) and all((d[i]<0 if b else d[i]>0) for i,b in enumerate(bits)))
# Facet/vertex incidence in the intrinsic q coordinates; 8 exposed stellation tetrahedra.
for i in range(4):
    for eps in [-1,1]:
        v=[eps*verts[i]]+[eps*(verts[i]+verts[j])/2 for j in range(4) if i!=j]
        X=[M*t/4 for t in v]
        vol=abs(S.Matrix.hstack(*[t-X[0] for t in X[1:]]).det())/6
        check(f'stellated component {i},{eps} volume and boundary',vol==S.Rational(1,3) and eps*v[0][i]==3 and all(eps*t[i]==1 for t in v[1:]))
check('fan counterexample if edge multiplicity condition omitted',all(len(edges((0,1,a))&edges((0,1,b)))==1 for a,b in combinations(range(2,6),2)))
print(f'{n}/{n} exact checks passed (overlapping identities and finite cases, not independent theorems).')
