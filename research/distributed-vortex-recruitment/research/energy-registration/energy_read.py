"""Exact/conditional extension of native GFD port, energy and throat algebra."""
import numpy as np
import sympy as s
from scipy.optimize import root
from native_cell import H,F,C,A,base
from native_throat import G,C as CM,M,T,x,n,chi,h,L
W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]],float)/9
H4=np.array([[(-1)**((i&j).bit_count()) for j in range(4)] for i in range(4)])/2
FW=np.kron(np.kron(H4,H4),H4)

def history(rows,order):
    return np.vstack([rows@np.linalg.matrix_power(H,k) for k in range(order+1)])

def exact_observability():
    filt=s.Matrix(history(C[:4],6)); full=s.Matrix(history(np.vstack([f.T for f in F[:4]]),2))
    dark=s.Matrix.hstack(*filt.nullspace()); return filt,full,dark

def port_ledger(local,neighbours,J=1.):
    # a=face, b=local tile, c=remote tile. HALF incident bond energy.
    return np.array([-J*W*np.real(np.outer((F[a].T@local).conj(),F[a+4].T@neighbours[a])) for a in range(4)])

def bond(local,remote,a,J=1.):
    z=np.vdot(F[a].T@local,W@(F[a+4].T@remote))
    return -2*J*z.real,2*J*z.imag

def prefix_energies(e):
    return e.sum(axis=(1,2)),e.sum(axis=2),e.copy()

# Matched, fixed-orientation, projected nonlinear model, not full H36 lattice.
# Uniform circular orientation makes B_i=T/4 exactly.
Gn,Cn,Mn,Tn=[np.array(a,float) for a in (G,CM,M,T)]
x0=np.array(x,float).ravel(); norm=float(n); u0=float(chi)

def uniform(J):
    def f(v):
        y=v[:3]; u=y@Gn@Cn@y/(2*norm); g=2*u/(u0+abs(u))
        return np.r_[(Mn+(g-1)*Cn-J*Tn)@y-v[3]*y,y@Gn@y-norm]
    z=root(f,np.r_[x0,1.1],tol=1e-11)
    assert np.linalg.norm(f(z.x))<1e-9
    return z.x[:3],z.x[3]

def tangents(J,k):
    y,om=uniform(J); u=y@Gn@Cn@y/(2*norm); g=2*u/(u0+abs(u)); hh=4*u0/(u0+abs(u))**2
    gamma=abs(np.exp(1j*A@np.asarray(k)).sum())/4
    B=Mn+(g-1)*Cn-J*gamma*Tn-om*np.eye(3)
    P=B+hh/(2*norm)*np.outer(Cn@y,y@Gn@Cn)
    return y,B,P

def growth(J,k):
    y,B,P=tangents(J,k)
    return np.linalg.eigvals(-B@P)

def phase_coefficient(J):
    y,B,P=tangents(J,[0,0,0]); return -J/2*(y@Gn@Tn@y)/(y@Gn@np.linalg.solve(P,y))

def static_read(J,k):
    y,B,P=tangents(J,k)
    # source in real amplitude direction (chemical-potential perturbation), not calibrated physical mass
    dy=np.linalg.solve(P,y)
    return y@Gn@Cn@dy/norm
