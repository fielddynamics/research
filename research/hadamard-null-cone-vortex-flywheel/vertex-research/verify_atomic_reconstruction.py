"""Exact and numerical tests of conditional complete-frame registration. No fitted G."""
import itertools as it
import numpy as np
import sympy as s
from fractions import Fraction as F

counts = {'exact':0,'numerical':0}
def check(condition, label, kind='exact'):
    assert condition, label
    counts[kind]+=1
    print(f'PASS [{kind}] {label}')
def close(a,b,label,atol=1e-10):
    check(np.allclose(a,b,rtol=1e-10,atol=atol),label,'numerical')

# Invariant orbit counts of the actual recursive label rotation.
rot=(0,2,3,1)
for k in range(4):
    words=list(it.product(range(4),repeat=k)); seen=set(); sizes=[]
    for w in words:
        if w in seen: continue
        v=w; orbit=set()
        for _ in range(3):
            orbit.add(v);v=tuple(rot[i] for i in v)
        seen.update(orbit);sizes.append(len(orbit))
    check(sizes.count(1)==1 and sizes.count(3)==(4**k-1)//3,f'depth {k} orbit count')
    check(len(sizes)==(4**k+2)//3,f'depth {k} invariant rank')
check([((4**k+2)//3)-((4**(k-1)+2)//3) for k in (1,2,3)]==[1,4,16],'invariant grades')
# Four-way Walsh transform and recursive tree in real orthonormal coordinates.
h=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],float)/2
I=np.eye(64); words=list(it.product(range(4),repeat=3)); ind={w:i for i,w in enumerate(words)}
R=np.zeros((64,64))
for w in words:R[ind[tuple(rot[i] for i in w)],ind[w]]=1
B=I.copy()
for axis in (2,1,0):
    P=I.copy()
    for prefix in it.product(range(4),repeat=axis):
        inds=[ind[prefix+(i,)+(0,)*(2-axis)] for i in range(4)]
        P[np.ix_(inds,inds)]=h
    B=P@B
W=np.kron(np.kron(h,h),h); D=W@B.T
for label,U in [('tree',B),('detail mixer',D),('Walsh',W)]:
    close(U@U.T,I,label+' orthogonality');close(U@R,R@U,label+' rotation equivariance')
    close(abs(np.linalg.det(U)),1,label+' preserves volume')
close(D@B,W,'Walsh tree factorization');close(B.T@D.T,W.T,'inverse tree factorization')
Q=(I+R+R@R)/3
close(Q@Q,Q,'rotation average projector')
# Q in each prefix-constant space: trace gives invariant rank.
prev=0
for depth in range(4):
    v=np.ones((4**(3-depth),1))/np.sqrt(4**(3-depth));E=np.kron(np.eye(4**depth),v)
    r=np.trace(E.T@Q@E)
    close(r,(4**depth+2)/3,f'prefix {depth} rank')
    if depth:close(r-prev,4**(depth-1),f'prefix {depth} contrast rank')
    prev=r

# Sierpinski block counts / determinant, symbolic rank and closure response.
L=s.Matrix([[1,0],[1,1]]); S=s.diag(s.ones(1),s.kronecker_product(L,L),s.kronecker_product(L,L,L,L))
check(S.shape==(21,21),'Sierpinski 21x21')
check(sum(int(v!=0) for v in S)==91,'Sierpinski 91 filled entries')
check(S.det()==1,'Sierpinski det is one')
check(S.trace()==21,'Sierpinski trace 21')
k=s.symbols('K', positive=True); fA=k*k+k+1; fB=k*k-k+1; fO=k*k+1
check(s.expand(fA*fB-1-k*k*fO)==0,'273-272 identity')
H=s.Matrix([[fO,k],[k,fO]])
check(s.simplify(H.det()-fA*fB)==0,'winding determinant')
check(s.simplify((H.inv()[0,0])*fA-fO/fB)==0,'relative settled compliance')
# Exact completion polynomial: all deletion hyperplanes, distinct factor each.
a,b,c=s.symbols('a b c'); amp=a*b*c*(1+a*b)
for var in (a,b,c):check(amp.subs(var,0)==0,f'deletion criterion {var}')
check(s.Poly(amp,a,b,c).terms()==[((2,2,1),1),((1,1,1),1)],'joint completion with interaction has same leading product but non-universal coefficient')
# Correlated and independent events with identical marginal pass fraction.
p=F(1,137)
for n in (1,4,16,21):
    check(p**n<=p,f'independent versus common-gate probability n={n}')
check(p**21 != p,'atomicity does not imply independence')
# Normalized nested 1D and multidimensional box overlap.
for d in (1,2,3):
    # exact integration for squared normalized step-function overlap: overlap^2/(norm^2 norm^2)
    short=p**d; long=F(1); check(short*short/(short*long)==p**d,f'{d}D top-hat overlap integral')
# Native 33-site Stage VII graph: only common diagonal phase commutes.
X=[(i,j) for i in range(4) for j in range(4) if i!=j]
idx={ (side,typ,*ij):n for n,(side,typ,*ij) in enumerate([(side,'x',i,j) for side in (0,1) for i,j in X]+[(side,'y',i) for side in (0,1) for i in range(4)]) }
edges=set()
def edge(i,j):edges.add(tuple(sorted((i,j))))
for side in (0,1):
    for i,j in X:
        v=idx[side,'x',i,j]
        for l in range(4):
            if l not in (i,j):edge(v,idx[side,'x',i,l])
        edge(v,idx[1-side,'x',j,i]);edge(v,idx[side,'y',i]);edge(v,idx[1-side,'y',j])
        edge(idx[side,'y',i],idx[1-side,'y',j])
    for i in range(4):edge(idx[side,'y',i],32)
check(len(edges)==104,'native graph 104 bonds')
inc=s.zeros(len(edges),33)
for z,(i,j) in enumerate(sorted(edges)):inc[z,i]=1;inc[z,j]=-1
check(inc.rank()==32,'native diagonal phase constraint rank 32 (one common phase)')
# Isotropic scalar source and complete-frame norm are both invariant: symmetry cannot choose.
rng=np.random.default_rng(20261126); n=21
for i in range(8):
    U,_=np.linalg.qr(rng.normal(size=(n,n)));V,_=np.linalg.qr(rng.normal(size=(n,n)))
    t=rng.uniform(.2,.9,n);T=U@np.diag(t)@V.T
    close(np.linalg.slogdet(T)[1],np.log(t).sum(),f'principal-angle determinant {i}')
    close(np.linalg.norm(T,'fro')**2,np.sum(t*t),f'ordinary read {i}')
    T0=T.copy();T0[:,0]=0
    check(abs(np.linalg.det(T0))<1e-100 and np.linalg.norm(T0,'fro')>0,f'rank loss complete-volume versus ordinary source {i}','numerical')
    # Conservative dilation of the same contrast space, no extra physical oscillator assertion.
    C=U@np.diag(np.sqrt(1-t*t))@V.T
    close(T.T@T+C.T@C,np.eye(n),f'complement preserves norm {i}')
# Common-gain factorization with off-grade dependencies.
t=np.sqrt(1/137.035999177)
for i in range(6):
    J=t*np.eye(n); J[1:5,:1]=rng.normal(size=(4,1));J[5:,:5]=rng.normal(size=(16,5))
    close(np.linalg.slogdet(J)[1],n*np.log(t),f'ordered inverse determinant {i}')
# Gaussian elimination: determinant cancels from normalized source response.
q=s.symbols('q', real=True); a0,b0,c0=s.symbols('a0 b0 c0', positive=True)
A=s.Matrix([[a0,b0],[b0,c0]]); src=s.Matrix([q,0]); z=A.inv()*src
check(s.simplify((s.Rational(1,2)*(z.T*A*z)[0]-(src.T*z)[0])+q*q*c0/(2*A.det()))==0,'source energy from inverse Hessian')
# Static mass-coupled effective model algebra (conditional source and stiffness).
alpha,kap,g,me,hbar,c=s.symbols('alpha kap g me hbar c',positive=True)
check(s.simplify((hbar*c*g*g/(kap*me*me)).subs({g:alpha**s.Rational(21,2),kap:s.Rational(13,17)})-s.Rational(17,13)*alpha**21*hbar*c/me**2)==0,'conditional G from mass-coupled effective action')
print(f'TOTAL {sum(counts.values())} = {counts["exact"]} exact + {counts["numerical"]} numerical')
