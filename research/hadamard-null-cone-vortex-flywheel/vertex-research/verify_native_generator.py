"""Native pulse obstruction and minimal positive reciprocal completion.
All native weights are inherited dimensionless witnesses, not physical calibration.
"""
from itertools import permutations, product
import numpy as np
import sympy as s
from pathlib import Path
p=Path(__file__).parent
n={'exact':0,'numerical':0}
def ck(label, condition,kind='exact'):
    assert bool(condition),label
    n[kind]+=1; print('PASS',kind,label)
r=s.Rational; I=s.eye; pairs=list(permutations(range(4),2)); d,a,k=r(-1,2),-1,-1
C=s.zeros(16); A=s.zeros(16)
for j,(i,l) in enumerate(pairs):
    C[j,pairs.index((l,i))]=d
    C[j,12+l]=C[12+l,j]=a
    A[j,12+i]=A[12+i,j]=-2
    for jj,(ii,ll) in enumerate(pairs):
        if i==ii and l!=ll:A[j,jj]=-1
C[12:16,12:16]=k*(s.ones(4)-I(4));A[12:16,12:16]=-r(99,10)*I(4)
x=s.symbols('x'); pU=x*x-(d+3*k)*x+3*(d*k-a*a);pT=x**3+k*x*x-(3*a*a+d*d)*x+a*a*d-d*d*k
ck('symmetric native C',C==C.T);ck('invertible',C.det()!=0);ck('characteristic polynomial',s.expand(C.charpoly(x).as_expr()-(x-d)**2*(x+d)**3*pU*pT**3)==0)
ck('uniform roots irrational discriminant',s.discriminant(pU,x)==r(73,4))
ck('triplet cubic irreducible over Q',s.Poly(pT,x).is_irreducible)
ck('triplet sum',-s.Poly(pT,x).all_coeffs()[1]==1)
for signs in product([-1,1],repeat=3):ck('no signed sum equals triplet sum '+str(signs),1-d*sum(signs)!=0)
ck('local graph does not commute with cross kernel',A*C-C*A!=s.zeros(16))
ck('constant record not eigenvector',len(set(C*s.ones(16,1)))>1)
print('native characteristic:',s.factor(C.charpoly(x).as_expr()))
print('native common row sums:',sorted(set(C*s.ones(16,1))))
Cn=np.array(C,float); An=np.array(A,float); eig,Q=np.linalg.eigh(Cn); D=(Q*abs(eig))@Q.T; S=(Q*np.sign(eig))@Q.T; W=(Q*(1/np.sqrt(abs(eig))))@Q.T
ck('sign inertia 7/9',sum(eig>0)==7 and sum(eig<0)==9,'numerical')
ck('metric whitened sign',np.allclose(W@Cn@W,S),'numerical');ck('sign orthogonal',np.allclose(S@S,np.eye(16)),'numerical')
ck('minimum block PSD',min(np.linalg.eigvalsh(np.block([[D,Cn],[Cn,D]])))>-1e-10,'numerical')
ck('minimum block rank 16',np.linalg.matrix_rank(np.block([[D,Cn],[Cn,D]]),tol=1e-9)==16,'numerical')
ck('minimum trace',np.isclose(np.trace(D),sum(abs(eig))),'numerical')
# Symmetric D >= +/- C implies diagonal in eigenbasis >= |lambda|; equality forces offdiagonals zero.
# Construct positive perturbations; each obeys PSD and raises trace.
rng=np.random.default_rng(20261126)
for j in range(8):
    R=rng.normal(size=(16,4));Dp=D+R@R.T
    ck(f'positive added stiffness {j}',min(np.linalg.eigvalsh(Dp+Cn))>-1e-9 and min(np.linalg.eigvalsh(Dp-Cn))>-1e-9 and np.trace(Dp)>np.trace(D),'numerical')
for t in [0,.1,.5,1,2,7,11]:
    # isolated kernel pulse, includes scalar nonlinear gain integrated over time
    A0=(Q*np.cos(t*eig))@Q.T; B0=(Q*np.sin(t*eig))@Q.T
    ck(f'raw pulse conservation {t}',np.allclose(A0.T@A0+B0.T@B0,np.eye(16)),'numerical')
    a0=np.cos(t)*np.eye(16); b0=np.sin(t)*S
    ck(f'whitened common gain {t}',np.allclose(a0.T@a0,np.cos(t)**2*np.eye(16)) and np.allclose(b0.T@b0,np.sin(t)**2*np.eye(16)),'numerical')
    ck(f'whitened pulse conservation {t}',np.allclose(a0.T@a0+b0.T@b0,np.eye(16)),'numerical')
    if t:ck(f'raw pulse unequal gains {t}',np.ptp(np.cos(t*eig)**2)>1e-5,'numerical')
# Algebraic common-gain criterion for passive polar-normalized relative energy read.
eta=s.symbols('eta',real=True); H=s.Matrix([[1,eta],[eta,1]])
ck('normalized two-channel determinant',H.det()==1-eta**2)
ck('Schur stiffness',s.simplify(H[0,0]-H[0,1]*H[1,0]/H[1,1]-(1-eta**2))==0)
# inherited normalized constitutive gain g_r(u*) =1, not sqrt(alpha)
u,c,z=s.symbols('u c z',positive=True);g=(1+z)*u/(z*c+u)
ck('constitutive gain at witness',s.simplify(g.subs(u,c))==1)
ck('curvature rank-one coefficient free',s.simplify(s.diff(g,u).subs(u,c)-z/(c*(1+z)))==0)
# local response alpha calibration is a hypothesis: no special alpha chosen by passive model.
alpha=1/137.035999177
for q in [alpha,.1,.25,.9]:
    theta=np.arccos(np.sqrt(q)); G=np.cos(theta)*np.eye(21)
    ck(f'21 determinant arbitrary calibration {q}',np.isclose(np.linalg.slogdet(G)[1]*2,21*np.log(q)),'numerical')
print('native eigenvalues:',eig)
print('minimum metric trace:',np.trace(D))
print('SUMMARY',n,'total',sum(n.values()))
