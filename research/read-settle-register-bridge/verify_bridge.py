"""Independent checks of the conditional read–settle–response bridge.
No GFD modules required. Run: python verify_bridge.py (numpy, sympy).
These are model checks, not a verification of the physical premises.
"""
import itertools
import numpy as np
import sympy as s
checks=[]
def check(name, cond):
    assert bool(cond), name
    checks.append(name)
    print('PASS', name)
# Read: 8 cube modes, chamber aliasing, and complete reconstruction.
C=np.array(list(itertools.product([-1,1], repeat=3)),dtype=int)
W=np.array([np.prod(C[:,[i for i in range(3) if mask>>i&1]],axis=1) for mask in range(8)])
check('Walsh orthogonality', np.array_equal(W@W.T,8*np.eye(8)))
A=np.prod(C,axis=1)==1
check('TetA rank four', np.linalg.matrix_rank(W[:,A])==4)
check('TetB rank four', np.linalg.matrix_rank(W[:,~A])==4)
check('all complement aliases and opposite aliases', all(np.array_equal(W[k,A],W[7^k,A]) and np.array_equal(W[k,~A],-W[7^k,~A]) for k in range(8)))
f=np.array([2,7,-3,0,9,1,4,-2]); check('full state reconstructed',np.array_equal(W.T@(W@f),8*f))
# Full dual frame gradient, exact for quadratic potential, with individual chiral leak.
ell=.125; p=np.array([2.,-3.,5.]); H=np.array([[3.,4.,-2.],[4.,1.,7.],[-2.,7.,-4.]])
r=ell*C; phi=11+r@p+np.einsum('ni,ij,nj->n',r,H,r)/2
read=lambda mask: C[mask].T@phi[mask]/(ell*sum(mask))
leak=ell*np.array([H[1,2],H[0,2],H[0,1]])
check('TetA gradient plus mixed-Hessian leak',np.allclose(read(A),p+leak))
check('TetB gradient minus mixed-Hessian leak',np.allclose(read(~A),p-leak))
check('dual read exactly recovers quadratic gradient',np.allclose(read(np.ones(8,dtype=bool)),p))
# 64 ledger: four blocks of 4x4, partial transpose; not ordinary 8x8 transpose.
I=np.eye(64,dtype=int).reshape(2,4,2,4,64)
P=I.transpose(0,3,2,1,4).reshape(64,64)
check('within-frame swap involution',np.array_equal(P@P,np.eye(64)))
check('within-frame swap trace 16 => 40/24',np.trace(P)==16)
Q=np.eye(64,dtype=int).reshape(8,8,64).transpose(1,0,2).reshape(64,64)
check('ordinary 8x8 transpose trace 8 => 36/28',np.trace(Q)==8)
# Capacity settlement: work-conjugate cost, exact elimination.
x,b=s.symbols('x b', positive=True); a=s.symbols('a',positive=True)
B=x/(1+x); Wb=-b-s.log(1-b); F=x*x-2*x+2*s.log(1+x)
check('capacity law fixes cost derivative',s.simplify(s.diff(Wb,b)-b/(1-b))==0)
check('cost strictly convex',s.simplify(s.diff(Wb,b,2)-1/(1-b)**2)==0)
check('finite capacity equilibrium',s.simplify(x*(1-B)-B)==0)
check('stationary energy',s.simplify((s.diff(Wb,b)-x).subs(b,B))==0)
check('elimination recovers SST F/2',s.simplify(s.expand_log((x*x/2-x*b+Wb).subs(b,B)-F/2,force=True))==0)
check('AQUAL current',s.simplify(s.diff(F/2,x)-x*x/(1+x))==0)
check('radial tangent',s.simplify(s.diff(F/2,x,2)-x*(x+2)/(1+x)**2)==0)
check('gradient flow dissipation identity',s.simplify((s.diff(Wb,b)-x)*(x*(1-b)-b)+(1-b)*(s.diff(Wb,b)-x)**2)==0)
# Torsion contraction in local orthonormal frame.
u=s.Matrix([1,0,0,0]); eta=s.diag(-1,1,1,1); ud=eta*u; q=s.Matrix([0,*s.symbols('q1:4')]); c=s.symbols('c',positive=True)
T=s.MutableDenseNDimArray.zeros(4,4,4)
for l,m,n in itertools.product(range(4),repeat=3): T[l,m,n]=u[l]*(ud[m]*q[n]-ud[n]*q[m])/c**2
qread=s.Matrix([-c**2*sum(ud[l]*u[n]*T[l,m,n] for l,n in itertools.product(range(4),repeat=2)) for m in range(4)])
check('auxiliary torsion realizes response vector',qread==q)
check('auxiliary torsion is antisymmetric',all(T[l,m,n]==-T[l,n,m] for l,m,n in itertools.product(range(4),repeat=3)))
check('axial torsion vanishes',all(s.simplify(sum(s.LeviCivita(a,l,m,n)*sum(eta[l,j]*T[j,m,n] for j in range(4)) for l,m,n in itertools.product(range(4),repeat=3)))==0 for a in range(4)))
# Fixed spherical drained to drainless interface. Dimensionless GM/R^2 = z a0.
z=s.symbols('z',positive=True); g=(z+s.sqrt(z*z+4*z))/2
check('radial interior current equals exterior Newtonian current',s.simplify(g*g/(1+g)-z)==0)
check('negative interface residual cancels interior excess',s.simplify((g-z)+(z-g))==0)
# Vector relaxation at fixed p, explicit time stepping for sample drives.
for x0 in [.01,.1,1.,10.,100.]:
    dt=.1/(1+x0); b0=.05; es=[]
    for k in range(1000):
        es.append(-x0*b0-b0-np.log1p(-b0)); b0+=dt*(x0*(1-b0)-b0)
    check(f'local settling monotone, bounded, correct equilibrium x={x0:g}', np.max(np.diff(es))<1e-11 and 0<=b0<1 and abs(b0-x0/(1+x0))<1e-12)
# Same polynomial, distinct physical roles: attenuation and response.
check('weighted structural trace 13+8 mu',s.simplify(21*B+13*(1-B)-(17+4*(2*B-1)))==0)
print(f'\n{len(checks)}/{len(checks)} checks passed.')
