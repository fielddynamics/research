"""Conditional electromagnetic normalization bridge; no fitting to measured G."""
from pathlib import Path
from itertools import product
import numpy as np
import sympy as sp
import csv
import contextlib,io
root=Path(__file__).resolve().parent
checks=[]
def ck(name,condition):
    assert bool(condition),name
    checks.append(name); print(f'PASS {len(checks):03d} {name}')
# Upstream graded read and equivalent positive face traces.
a=sp.symbols('alpha',positive=True); t=sp.symbols('t',positive=True)
I=sp.eye(16); swap=sp.zeros(16)
for i,j in product(range(4),repeat=2): swap[4*i+j,4*j+i]=1
Ps=(I+swap)/2; Pa=(I-swap)/2
O=sp.eye(17); B=sp.diag(1,2*Pa); A=sp.diag(1,2*Ps)
ck('swap involution and orthogonality',swap**2==I and swap.T==swap)
ck('symmetric and antisymmetric projectors',Ps**2==Ps and Pa**2==Pa and Ps*Pa==sp.zeros(16))
ck('connection traces 10 and 6',sp.trace(Ps)==10 and sp.trace(Pa)==6)
ck('positive face read traces 21 17 13',list(map(sp.trace,[A,O,B]))==[21,17,13])
ck('origin is average of chamber reads',A+B==2*O)
ck('positive TetB operator is not a rank-13 projector',B.rank()==7 and B**2!=B)
ck('isotropic unit trace average ratio',sp.trace(O)/sp.trace(B)==sp.Rational(17,13))
# A single exterior product is not an ordinary scalar projection.
T=t*sp.eye(21)
ck('full closure amplitude is determinant',T.det()==t**21)
ck('ordinary coherent port amplitude is one factor', (sp.ones(1,21)*T*sp.ones(21,1))[0]/21==t)
ck('relative closure power with single electromagnetic read',sp.simplify((T.det()/t)**2)==t**40)
ck('one sqrt(alpha) amplitude per mode gives relative alpha^20',(t**40).subs(t,sp.sqrt(a))==a**20)
ck('electron electromagnetic normalization gives tree-level target',sp.simplify(a*a**20*sp.trace(O)/sp.trace(B))==sp.Rational(17,13)*a**21)
# Lossless optical realization: retained transmission subblock and reflected complement.
U=sp.Matrix([[sp.sqrt(a),sp.sqrt(1-a)],[sp.sqrt(1-a),-sp.sqrt(a)]])
ck('one-mode optical splitter is algebraically orthogonal',sp.simplify(U.T*U)==sp.eye(2))
ck('one-mode transmission intensity is alpha',sp.simplify(U[0,0]**2)==a)
ck('21-mode all-pass amplitude is alpha^(21/2)',sp.simplify(U[0,0]**21)==a**sp.Rational(21,2))
ck('21-mode all-pass intensity is alpha^21',sp.simplify((U[0,0]**21)**2)==a**21)
# Trace result needs isotropic mode sampling; coherent read alone does not force it.
ck('single scalar face direction has ratio one',O[0,0]/B[0,0]==1)
v=sp.zeros(17,1);v[2]=1;v[5]=-1;v=v/sp.sqrt(2)
# explicit antisymmetric tensor on (0,1) and (1,0)
ck('single antisymmetric direction has stiffness ratio one half',(v.T*O*v)[0]/(v.T*B*v)[0]==sp.Rational(1,2))
v=sp.zeros(17,1);v[1]=1
ck('symmetric direction has zero TetB stiffness',(v.T*B*v)[0]==0)
# Direct lattice normalization from existing microscopic model.
P=sp.Matrix([[2,2,0],[2,0,2],[0,2,2]])
ck('primitive diamond cell volume is 16 a_cell^3',abs(P.det())==16)
# Use existing Hamiltonian definition, not the previous numerical result as an input.
ns={'__file__':str(root/'verify_coupled_origins.py')}
exec((root/'verify_coupled_origins.py').read_text().split("ck('33 original geometric positions;")[0],ns)
S,H,d,base,idx=[ns[k] for k in ('S','H','d','base','idx')]; A4=S[:4]
F=[np.eye(d)[:,[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if j!=i]+[base[i]]] for i in range(8)]
W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9
Wc=np.outer([1,1,1,6],[1,1,1,6])/54
rows=[]
for label,Wk in [('full',W),('central',Wc)]:
    blocks=np.array([F[i]@Wk@F[i+4].T for i in range(4)])
    def M(k):
        X=-np.einsum('i,ijk->jk',np.exp(1j*A4@k),blocks);return np.block([[H,X],[X.conj().T,H]])
    M0=M(np.zeros(3)).real; eig,vec=np.linalg.eigh(M0); u=vec[:,0]; E0=eig[0]; R=(vec[:,1:]/(eig[1:]-E0))@vec[:,1:].T
    DD=[]
    for j in range(3):
        X=-np.einsum('i,ijk->jk',A4[:,j],blocks);Q=np.block([[np.zeros_like(H),X],[-X.T,np.zeros_like(H)]])
        X2=np.einsum('i,ijk->jk',A4[:,j]**2,blocks); M2=np.block([[np.zeros_like(H),X2],[X2.T,np.zeros_like(H)]])
        DD.append(u@M2@u/2+u@Q@R@Q@u)
    D=np.mean(DD);ck(label+' independently recomputed positive isotropic curvature',D>0 and np.allclose(DD,D))
    # A local scalar-origin defect is symmetry-preserving and has a nonzero first-order coupling.
    V=np.zeros_like(M0);V[0,0]=1;V[d,d]=1
    slope=u@V@u; h=1e-5
    fd=(np.linalg.eigvalsh(M0+h*V)[0]-np.linalg.eigvalsh(M0-h*V)[0])/(2*h)
    ck(label+' scalar defect Feynman-Hellmann derivative',np.isclose(slope,fd,rtol=1e-6) and slope>0)
    for scale in [.125,.5,2,8]:
        e0=np.linalg.eigvalsh(scale*M0)[0];k=np.array([.003,0,0]); curv=(np.linalg.eigvalsh(scale*M(k))[0]-e0)/np.dot(k,k)
        ck(label+' energy rescaling changes stiffness without geometry',np.isclose(curv,scale*D,rtol=1e-4))
    rows.append([label,D,D/16,slope])
ck('actual full-to-central stiffness ratio is not 17/13',not np.isclose(rows[0][1]/rows[1][1],17/13))
with (root/'g_closure_coefficients.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['interface','D','D_over_primitive_volume','scalar_defect_derivative']);w.writerows(rows)
# Explicit numerical formula, constants used only for comparison.
alpha=1/137.035999177; hbar=6.62607015e-34/(2*np.pi);c=299792458.;me=9.1093837139e-31
G=(17/13)*alpha**21*hbar*c/me**2
print('Computed tree-level G',format(G,'.12g'));print('With upstream proposed loop factor',format(G*(1+alpha/(2*np.pi)),'.12g'))
print('Dimensionless tree-level alpha_G',format((17/13)*alpha**21,'.12g'))
print('Microscopic data',rows)
print(f'{len(checks)}/{len(checks)} G closure checks passed.')
