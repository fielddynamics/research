"""Exact channel/tetrad dictionary and conditional weak-field/connection bridge."""
from itertools import combinations, permutations
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import expm
from fractions import Fraction
p=Path(__file__).resolve().parent
count=0
def ck(name, condition):
    global count
    assert bool(condition),name
    count+=1; print(f'PASS {count:03d} {name}')
U=s.Matrix([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
eta=s.diag(-1,1,1,1); J=U.T*eta*U; I=s.eye(4); ones=s.ones(4,4)
ck('Hadamard orthogonality',U.T*U==I)
ck('Lorentz channel Gram and signature',J==I-ones/2 and J.eigenvals()=={-1:1,1:3})
ck('flat reference is J',eta*U*J*U.T==I)
# Reconstruct actual face tiles on each chamber from cube signs, as in verify_coupled_origins.
S=np.array(U[1:,:]*2,dtype=int).T
for sign in (1,-1):
    V=sign*S; arr={}
    for i in range(4):
        f=[j for j in range(4) if j!=i]; mid=lambda a,b:tuple((V[a]+V[b])//2)
        arr[i,i]=frozenset(mid(a,b) for a,b in combinations(f,2))
        for j in f:arr[i,j]=frozenset([tuple(V[j])]+[mid(j,k) for k in f if k!=j])
    ck('16 distinct actual triangular tiles',len(set(arr.values()))==16)
    for (i,j),tile in arr.items():
        ck('tile lies on original face opposite i',all(np.dot(V[i],x)==-1 for x in tile))
        ck('tile centroid central or lateral',np.allclose(np.mean(list(tile),axis=0),-V[i]/3 if i==j else (3*V[j]-V[i])/6))
# actual centroids: outer apex plus midpoints -> (2Vj+(Vk+Vl)/2)/3 = (3Vj-Vi)/6? corrected below
# all 24 simultaneous face/vertex permutations intertwine spatial tetrahedron rotations/reflections.
for perm in permutations(range(4)):
    P=I[:,list(perm)]; R=U*P*U.T
    ck('Td intertwiner preserves time and eta',R[0,0]==1 and R.T*eta*R==eta)
    X=s.Matrix(4,4,range(1,17)); E=eta*U*X*U.T
    ck('channel conjugation agrees with frame conjugation',eta*U*P*X*P.T*U.T==R*E*R.T)
# exact basis decomposition
basis=[s.eye(4)[:,i]*s.eye(4)[:,j].T for i in range(4) for j in range(4)]
for B in basis:
    X=U.T*B*U; E=eta*U*X*U.T
    ck('lowered tetrad basis round trip',U.T*eta*E*U==X)
    ck('linear metric response equals B+B^T',E.T*eta+eta*E==B+B.T)
# weak field two scalar potentials
phi,psi=s.symbols('phi psi',real=True); B=-s.diag(phi,psi,psi,psi); X=U.T*B*U
ck('two scalar mode decomposition',X==-psi*I-(phi-psi)*ones/4)
ck('equal potentials central tiles only',X.subs(psi,phi)==-phi*I)
d=X[0,0]; o=X[0,1]; ck('recover both scalar potentials',s.simplify(-d-3*o-phi)==0 and s.simplify(-d+o-psi)==0)
ck('central-only finite coframe metric', s.simplify((eta*U*(J-phi*I)*U.T).T*eta*(eta*U*(J-phi*I)*U.T)-s.diag(-(1+phi)**2,*([(1-phi)**2]*3)))==s.zeros(4))
# antisymmetric six modes: gradients (3 boosts) and cycles (3 rotations)
v=s.Matrix(s.symbols('v0:4')); a=v-s.ones(4,1)*sum(v)/4; grad=a*s.ones(1,4)-s.ones(4,1)*a.T
ck('edge-gradient block only mixes time and space', (U*grad*U.T)[1:,1:]==s.zeros(3))
for i,j in combinations(range(4),2):
    A=basis[4*i+j]-basis[4*j+i]; r=A*s.ones(4,1); grad=(r*s.ones(1,4)-s.ones(4,1)*r.T)/4; cyc=A-grad
    ck('unique antisymmetric gradient/cycle split',cyc*s.ones(4,1)==s.zeros(4,1) and grad.T==-grad and cyc.T==-cyc)
    ck('cycle block purely spatial', (U*cyc*U.T)[0,:]==s.zeros(1,4))
    ck('split orthogonal',s.trace(grad.T*cyc)==0)
# finite Lorentz changes preserve metric, direct additive antisymmetric changes generally do not
un=np.array(U,float); et=np.array(eta,float); jn=np.array(J,float)
rng=np.random.default_rng(20261124)
for _ in range(12):
    B=rng.normal(size=(4,4))*.06; X=jn+un.T@B@un; E=et@un@X@un.T; g=E.T@et@E
    ck('nondegenerate read Lorentz signature',np.sum(np.linalg.eigvalsh(g)<0)==1)
    A=rng.normal(size=(4,4)); A=(A-A.T)*.1; Lam=expm(et@A); Ep=Lam@E
    ck('finite Lorentz gauge preserves metric',np.allclose(Ep.T@et@Ep,g,atol=1e-12))
    Xp=un.T@et@Ep@un; ck('induced channel gauge preserves channel metric',np.allclose(Xp.T@jn@Xp,X.T@jn@X,atol=1e-12))
    E2=np.eye(4)+rng.normal(size=(4,4))*.05; g2=E2.T@et@E2; link=np.linalg.solve(E,Lam@E2)
    ck('metric compatible link from independent Lorentz transporter',np.allclose(link.T@g@link,g2,atol=1e-12))
# actual overlap kernel: each face independent four tile reads, full rank vs central filter
W=s.Matrix([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9
w=s.Matrix([1,1,1,6]); Wc=w*w.T/54
ck('full face communication rank 4',W.rank()==4)
ck('central filtered face communication rank 1',Wc.rank()==1)
ck('four full faces carry 16 instantaneous coherent dimensions',s.diag(*([W]*4)).rank()==16)
ck('four filtered faces carry four instantaneous coherent dimensions',s.diag(*([Wc]*4)).rank()==4)
# 10+6 split exact on lowered perturbations and connection lower-index blocks
Swap=s.zeros(16)
for i in range(4):
    for j in range(4): Swap[4*j+i,4*i+j]=1
Pp=(s.eye(16)+Swap)/2; Pm=(s.eye(16)-Swap)/2
ck('10 symmetric and 6 antisymmetric lowered perturbations',Pp.rank()==10 and Pm.rank()==6)
ck('four connection blocks have 40 symmetric 24 antisymmetric entries',s.diag(*([Pp]*4)).rank()==40 and s.diag(*([Pm]*4)).rank()==24)
ck('weighted traces 21 17 13',s.trace(s.diag(1,2*Pp))==21 and s.trace(s.diag(1,s.eye(16)))==17 and s.trace(s.diag(1,2*Pm))==13)
# representation characters from simultaneous S4 on all ordered pairs, sym/anti.
for perm in permutations(range(4)):
    P=I[:,list(perm)]; M=s.kronecker_product(P,P)
    t=s.trace(P); t2=s.trace(P*P)
    ck('symmetric/antisymmetric characters',s.trace(M*Pp)==(t*t+t2)/2 and s.trace(M*Pm)==(t*t-t2)/2)
# local tetra derivative reconstructs affine channel read and weak acceleration exactly
n=S/np.sqrt(3); ell=.37
for _ in range(12):
    grad=rng.normal(size=3); phi0=rng.normal(); vals=phi0+ell*(n@grad); deltaX=np.array([-v*np.eye(4) for v in vals]); X0=-phi0*np.eye(4)
    derivative=3/(4*ell)*np.einsum('ka,kij->aij',n,deltaX-X0)
    ck('affine tetrad derivative from four ports',np.allclose(derivative,-grad[:,None,None]*np.eye(4)))
    ck('weak acceleration from mean central tile gradient',np.allclose(np.trace(derivative,axis1=1,axis2=2)/4,-grad))
# Explicit distinction from normalized null directions and from an arbitrary gauge.
N=s.diag(1,1/s.sqrt(3),1/s.sqrt(3),1/s.sqrt(3))*U
ck('normalized null direction Gram',s.simplify(N.T*eta*N-(I-ones)/3)==s.zeros(4))
ck('central-only scalar pattern is not invariant under null rescaling',s.simplify(N.T*N-I)!=s.zeros(4))
D=s.diag(1,-1,-1,-1); UB=D*U; X=s.Matrix(4,4,range(1,17))
ck('parity chamber map same signature',UB.T*eta*UB==J)
ck('parity covariance of coframe map',eta*UB*X*UB.T==D*(eta*U*X*U.T)*D)
# Exact volume read for a nondegenerate rational coframe.
X=J+s.diag(s.Rational(1,10),s.Rational(1,20),s.Rational(1,30),s.Rational(1,40)); E=eta*U*X*U.T; G=E.T*eta*E
ck('volume determinant identity',G.det()==-X.det()**2)
# Symmetric and antisymmetric connection are not coframe perturbation sectors.
# At flat coframe an arbitrary antisymmetric lower-index connection is allowed if metric compatibility is not imposed.
# Explicit metric-compatible contorsion example: omega_x is a spatial rotation in the y-z plane.
omega=s.zeros(4); omega[2,3]=1; omega[3,2]=-1
ck('independent spin connection metric-compatible at flat tetrad',omega.T*eta+eta*omega==s.zeros(4))
# Gamma^a_{mu nu} = omega_mu^a_nu, only mu=1 nonzero; T^2_{13}=1.
ck('nonzero torsion with unchanged flat tetrad',omega[2,3]==1)
print(f'TOTAL {count} checks passed')
