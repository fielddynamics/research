"""Dimensionless AQUAL primitives. Physical scales enter explicitly."""
import numpy as np

def mu(x):
    x=np.asarray(x,dtype=float);return x/(1+x)
def sigma(x): return 2*mu(x)-1
def capacity(x): return 13+8*mu(x)
def source(x): return np.asarray(x)**2/(1+np.asarray(x))
def total(z):
    z=np.asarray(z,dtype=float);return (z+np.sqrt(z)*np.sqrt(z+4))/2

def energy(y):
    """Stable F(y): series at small x to avoid cancellation."""
    y=np.asarray(y,dtype=float);x=np.sqrt(y); direct=y-2*x+2*np.log1p(x)
    series=np.zeros_like(x)
    for k in range(3,20): series+=2*(-1)**(k+1)*x**k/k if np.all(x<.1) else 2*(-1)**(k+1)*np.minimum(x,.1)**k/k
    return np.where(x<.05,series,direct)

def flux(p,a0=1):
    p=np.asarray(p,dtype=float);return mu(np.linalg.norm(p)/a0)*p

def jacobian(p,a0=1):
    p=np.asarray(p,dtype=float);x=np.linalg.norm(p)/a0
    if x==0:return np.zeros((p.size,p.size))
    n=p/np.linalg.norm(p);return mu(x)*np.eye(p.size)+x/(1+x)**2*np.outer(n,n)

def dual(z):
    z=np.asarray(z,dtype=float);return 2*z*total(z)-energy(total(z)**2)

def dual_closed(z):
    z=np.asarray(z,dtype=float);return z*z/2+(z+2)*np.sqrt(z*(z+4))/2-4*np.arcsinh(np.sqrt(z)/2)

def bound_mu(x):
    x=np.asarray(x,dtype=float);return 4*x/(np.sqrt(1+4*x)+1)**2

def bound_energy(y):
    x=np.sqrt(np.asarray(y,dtype=float));return y+x-(2*x/3+1/6)*np.sqrt(1+4*x)+1/6

def decode(r,v,G=1,a0=1):return r*v**4/(G*(a0*r+v*v))
def point_mass(r,GM=1,a0=1):return a0*total(GM/(r*r*a0))
def potential(r,GM=1,a0=1):
    rM=np.sqrt(GM/a0);A=np.sqrt(GM*a0);psi=np.arcsinh(2*r/rM);return A*psi-r*point_mass(r,GM,a0)
def phantom_density(r,GM=1,a0=1,G=1):
    m=mu(point_mass(r,GM,a0)/a0);return a0*m/(2*np.pi*G*r*(2-m))
def vacancy_cost(b):return -b-np.log1p(-b)
def vacancy_dual(x):return x-np.log1p(x)
def settle(p,a0=1):
    p=np.asarray(p,dtype=float);return p/(1+np.linalg.norm(p)/a0)
def poiss_kernel(n,b,R=1):
    n=np.asarray(n);b=np.asarray(b);return (R*R-b@b)/(4*np.pi*R*np.linalg.norm(R*n-b,axis=-1)**3)

def sphere_quadrature(n=64):
    """Product Gauss-Legendre x periodic trapezoid on unit sphere."""
    z,w=np.polynomial.legendre.leggauss(n);phi=np.arange(2*n)*np.pi/n
    zz,pp=np.meshgrid(z,phi,indexing='ij');s=np.sqrt(1-zz*zz)
    dirs=np.stack([s*np.cos(pp),s*np.sin(pp),zz],axis=-1).reshape(-1,3)
    weights=np.repeat(w,2*n)*np.pi/n
    return dirs,weights

def shell_potential(x,A,R=1,n=64):
    d,w=sphere_quadrature(n);q=R*d-np.asarray(x);inv=np.linalg.inv(A)
    return (w/np.sqrt(np.einsum('ni,ij,nj->n',q,inv,q))).sum()/(4*np.pi*np.sqrt(np.linalg.det(A)))
