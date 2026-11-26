"""Exact certificates for the intrinsic flywheel-to-tetrad proof.
SymPy only for the new certificates. The inherited research verifier additionally
reconstructs the full Stage VII Hamiltonian and checks its time evolution.
"""
from itertools import combinations, permutations
import sympy as s
n=0
def ck(name, condition):
    global n
    assert bool(condition), name
    n+=1
    print(f'PASS {n:03} {name}')
I=s.eye(4); J=s.ones(4); G=4*I-J; one=s.ones(4,1); P=G/4
edges=list(combinations(range(4),2)); pairs=[(i,j) for i in range(4) for j in range(4) if i!=j]
B=s.zeros(4,6); D=s.zeros(6,4); R=s.zeros(4,12); Q=s.zeros(4,12)
for h,(i,j) in enumerate(edges): B[i,h]=-1; B[j,h]=1
for i in range(4):
    tri=[j for j in range(4) if j!=i]
    for a,b in zip(tri,tri[1:]+tri[:1]):
        D[edges.index(tuple(sorted((a,b)))),i]=(-1)**i*(1 if a<b else -1)
for h,(i,j) in enumerate(pairs): R[i,h]=1; Q[j,h]=1
Pr=s.eye(12)-R.T*R/3; C=Q*Pr; F=s.sqrt(s.Rational(3,2))*C.T
ck('incidence and cycle Gram',B*B.T==G and D.T*D==G)
ck('cycle kernel and projector',B*D==s.zeros(4,4) and D*D.T/4==s.eye(6)-B.T*B/4)
ck('row projector and column Gram',Pr*Pr==Pr and R*Pr==s.zeros(4,12) and C*C.T==s.Rational(2,3)*G)
L=D*F.T/4
ck('explicit isometry and its adjoint',L*F==D and L.T*L==F*F.T/4 and L*L.T==D*D.T/4)
Z=s.Rational(3,8)*C.T
ck('minimum norm right inverse on zero-sum inputs',Q*Z==P and R*Z==s.zeros(4,4))
ck('minimum norm formula componentwise',all(Z[h,:]*P==s.Rational(3,8)*(I[j,:]+I[i,:]/3)*P for h,(i,j) in enumerate(pairs)))
ck('right inverse norm',Z.T*Z==s.Rational(3,8)*P)
ck('orthogonal to every invisible row-closed perturbation',all(Z.T*v==s.zeros(4,1) for v in R.col_join(Q).nullspace()))
# Actual core dual graph, oriented from positive face i to negative face j.
B8=s.zeros(8,12); A=s.zeros(12,6); S=s.zeros(12,6); inv=s.zeros(12)
for h,(i,j) in enumerate(pairs):
    B8[i,h]=-1; B8[j+4,h]=1
    e=edges.index(tuple(sorted((i,j))))
    A[h,e]=1 if i<j else -1; S[h,e]=1
    inv[pairs.index((j,i)),h]=-1
ck('core dual incidence rank seven',B8.rank()==7)
ck('chamber inversion is signed transpose',inv**2==s.eye(12) and inv*A==A and inv*S==-S)
ck('antisymmetric embedding norm',A.T*A==2*s.eye(6) and S.T*S==2*s.eye(6) and A.T*S==s.zeros(6))
ck('even current cycles are exactly embedded four-leg cycles',B8*A*D==s.zeros(8,4) and (A*D).rank()==3 and (B8*A).rank()==3)
K=B8*S; V=s.Matrix.hstack(*K.nullspace()); E=A*D/4
ck('odd current cycles have dimension two',K.rank()==4 and V.cols==2 and B8*S*V==s.zeros(8,2))
ck('even and odd span all five core cycles',(A*D).row_join(S*V).rank()==5)
ck('core even projector', (A*D*D.T*A.T/8)**2==A*D*D.T*A.T/8)
# Gram weights: exact necessity of equal edge weights for regularity.
w=s.symbols('w0:6',positive=True); Gw=D.T*s.diag(*w)*D
for i,j in edges:
    complement=tuple(k for k in range(4) if k not in (i,j))
    ck(f'weighted Gram off diagonal {i},{j}',Gw[i,j]==-w[edges.index(complement)])
ck('equal edge weights give scaled regular Gram',Gw.subs(dict.fromkeys(w,w[0]))==w[0]*G)
ck('anisotropic weights disprove geometry without metric premise',D.T*s.diag(2,1,1,1,1,1)*D!=G)
# Symbolic generic complex phase wedge in W, not sampled.
x0,x1,x2,y0,y1,y2=s.symbols('x0 x1 x2 y0 y1 y2',real=True)
x=s.Matrix([x0,x1,x2,-x0-x1-x2]); y=s.Matrix([y0,y1,y2,-y0-y1-y2]); a=s.Matrix([x[i]*y[j]-x[j]*y[i] for i,j in edges]); j=D.T*a
ck('symbolic phase wedge divergence',s.simplify(B*a)==s.zeros(4,1))
ck('symbolic phase wedge reconstruction',s.simplify(D*j-4*a)==s.zeros(6,1))
ck('symbolic area identity',s.expand(a.dot(a)-x.dot(x)*y.dot(y)+x.dot(y)**2)==0)
# Generic u,v,w row-current cancellation, real polynomial certificate.
ur,ui,vr,vi,wr,wi=s.symbols('ur ui vr vi wr wi',real=True)
u=ur+s.I*ui; v=vr+s.I*vi; wv=wr+s.I*wi; q=x+s.I*y
for i in range(4):
    tri=[j for j in range(4) if j!=i]
    t=[u*q[i]+v*q[k] for k in tri]
    raw=(-1)**i*sum(s.im(s.conjugate(t[k])*t[(k+1)%3]) for k in range(3))
    ck(f'generic row shift cancels in cycle {i}',s.expand(raw-(vr**2+vi**2)*j[i])==0)
for h,(i,k) in enumerate(edges):
    ck(f'generic core phase products {i},{k}',s.expand(s.im(s.conjugate(wv*q[i])*wv*q[k])-(wr**2+wi**2)*a[h])==0)
# Equality of Gram does not remove the reflection twist.
for p in permutations(range(4)):
    T=s.zeros(4); U=s.zeros(12); E=s.zeros(6)
    for i,k in enumerate(p):T[k,i]=1
    for h,(i,k) in enumerate(pairs):U[pairs.index((p[i],p[k])),h]=1
    for h,(i,k) in enumerate(edges):
        a0,b0=p[i],p[k]; E[edges.index(tuple(sorted((a0,b0)))),h]=1 if a0<b0 else -1
    ck(f'polar/axial intertwining {p}',U*F==F*T and E*D==T.det()*D*T and E*L==T.det()*L*U)
M=s.Matrix([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
ck('realization is a tight tetrahedral frame',M*M.T==G and M.T*M==4*s.eye(3))
ck('geometry is metric-dependent',M*s.diag(4,1,1)*M.T!=G)
X=s.Matrix.vstack(*[M[i,:].T.cross(M[j,:].T).T for i,j in edges]); ck('cross products match oriented difference globally',X==D*M or X==-D*M)
mid={tuple((M[i,:]+M[j,:])/2) for i,j in edges}
ck('six midpoints of tetrahedron are octahedral vertices',mid=={tuple(sign*int(i==j) for j in range(3)) for i in range(3) for sign in (-1,1)})
# Span of sign directions; core is intersection of the two half-space systems.
ck('eight frame directions and inverses are cube corners',len({tuple(sign*M[i,:]) for i in range(4) for sign in (-1,1)})==8)
print(f'{n}/{n} exact checks passed.')
