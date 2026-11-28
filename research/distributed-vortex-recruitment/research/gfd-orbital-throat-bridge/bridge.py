"""Conditional orbital-to-throat bridge. Atomic units: reduced-mass Hartree/Bohr.
No physical source-to-throat conversion or new oscillator is fitted."""
import numpy as np
import sympy as s
from scipy.special import eval_genlaguerre, factorial, sph_harm_y
from scipy.integrate import quad
from native_throat import G,C,M,T,x,n,chi,K,r as tangent_read
S=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]],float)/9

def radial(n,l,r):
    t=2*np.asarray(r)/n
    return (2/n)**1.5*np.sqrt(factorial(n-l-1)/(2*n*factorial(n+l)))*np.exp(-t/2)*t**l*eval_genlaguerre(n-l-1,2*l+1,t)

def density(n,l,m,r,theta,phi):
    return radial(n,l,r)**2*abs(sph_harm_y(l,m,theta,phi))**2

def radial_moment(n,l,p):
    return quad(lambda r:r**(2+p)*radial(n,l,r)**2,0,np.inf,epsabs=1e-10)[0]

def ipr(n,l,m):
    radial_part=quad(lambda r:r*r*radial(n,l,r)**4,0,np.inf,epsabs=1e-11)[0]
    angular=2*np.pi*quad(lambda z:abs(sph_harm_y(l,m,np.arccos(z),0))**4,-1,1,epsabs=1e-12)[0]
    return radial_part*angular

def energy(n):return -.5/n**2

def p4(n,l):return -3/n**4+4/(n**3*(l+.5))

def sphere_avg(poly,xyz):
    out=0
    for exps,coef in s.Poly(poly,*xyz).terms():
        if any(e%2 for e in exps):continue
        out+=coef*s.prod(s.factorial2(e-1) for e in exps)/s.factorial2(sum(exps)+1)
    return s.simplify(out)

def cubic_expect(poly,xyz):
    return sphere_avg(poly**2*sum(v**4 for v in xyz),xyz)/sphere_avg(poly**2,xyz)

def quartic_energy(n,l,angular):
    # H= lambda_D/(4a²), correction /a²; only continuum perturbation,
    # not full hydrogen lattice discretization, potential correction absent.
    return p4(n,l)*(-1/8+float(angular)/12)

def port_operators(z):
    # Fixed-orientation projected matched-port injection. E^*E=4G.
    z=np.asarray(z,complex);z/=np.linalg.norm(z);q=S@z
    g=np.array(G,float);out=[]
    for i in range(4):
        E=np.array([[q[i],q[j],0] for j in range(4) if i!=j]+[[0,0,q[i]]])
        out.append(np.linalg.solve(4*g,E.conj().T@W@E))
    return np.array(out)

def tangent(B):
    # Real stationary bias -eps B/2, inherited normalization. Imaginary
    # port components require the separate phase tangent, not included here.
    xx=np.array(x,float).ravel(); kk=np.array(K,float)
    v=np.linalg.solve(kk,np.r_[np.real(B)@xx/2,0])[:3]
    return float((np.array(tangent_read,float)@v).item()),float(2*xx[2]*v[2]/float(n))

def shell_density(n,l,r,theta,phi,spin=2):
    return spin*sum(density(n,l,m,r,theta,phi) for m in range(-l,l+1))

def radial_derivative(n,l,r):
    t=2*np.asarray(r)/n; j=n-l-1; a=2*l+1
    p=eval_genlaguerre(j,a,t); dp=-eval_genlaguerre(j-1,a+1,t) if j else 0.
    norm=(2/n)**1.5*np.sqrt(factorial(j)/(2*n*factorial(n+l)))
    return norm*(2/n)*np.exp(-t/2)*((l*t**(l-1)*p if l else 0.)+t**l*(dp-p/2))

def radial_energy_density(n,l,r):
    R=radial(n,l,r);dR=radial_derivative(n,l,r)
    return .5*(r*r*dR*dR+l*(l+1)*R*R)-r*R*R

def integrated_energy(n,l,R=np.inf):
    return quad(lambda r:radial_energy_density(n,l,r),0,R,epsabs=1e-11)[0]
