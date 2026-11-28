"""Research models: exact geometric tests, conditional GR benchmarks, native H36 checks.
All distances dimensionless unless stated. a=GM/(2c^2) for the GR comparison.
"""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
from native_cell import A, H, bloch

W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9

def area(poly):
    p=np.asarray(poly); return np.linalg.norm(np.cross(p,np.roll(p,-1,axis=0)).sum(0))/2

def interface():
    tri=np.array([[1,.25,.25],[.25,1,.25],[.25,.25,1]])
    hexagon=np.array([[.25,.5,.75],[.25,.75,.5],[.5,.75,.25],[.75,.5,.25],[.75,.25,.5],[.5,.25,.75]])
    return tri,hexagon

def area_scale(F,n):
    return abs(np.linalg.det(F))*np.linalg.norm(np.linalg.solve(F.T,n))

def diamond(n=12):
    """Finite cube of the existing diamond lattice; boundary nodes have missing neighbors."""
    xyz=[]
    for i in range(-n,n+1):
      for j in range(-n,n+1):
       for k in range(-n,n+1):
        if (i%2==j%2==k%2) and ((i+j+k)%4==(3 if i%2 else 0)):
            xyz.append((i,j,k))
    p=np.array(xyz); index={x:i for i,x in enumerate(xyz)}; edges=[]; boundary=[]
    for i,x in enumerate(p):
        nb=[index.get(tuple(x+s)) for s in (A if x[0]%2==0 else -A)]
        if None in nb: boundary.append(i)
        edges.extend((i,j) for j in nb if j is not None and i<j)
    return p,np.array(edges),np.array(boundary),index[(0,0,0)]

def laplacian(p,edges,weights=None):
    i,j=edges.T; w=np.ones(len(i)) if weights is None else weights
    return coo_matrix((np.r_[w,w,-w,-w],(np.r_[i,j,i,j],np.r_[i,j,j,i])),shape=(len(p),len(p))).tocsr()

def dirichlet(L,boundary,values,source):
    inside=np.setdiff1d(np.arange(L.shape[0]),boundary); q=np.zeros(L.shape[0]); q[boundary]=values
    q[inside]=spsolve(L[inside][:,inside],source[inside]-L[inside][:,boundary]@values)
    return q,inside

def dimple(n=16,a=1.):
    p,e,b,o=diamond(n); L=laplacian(p,e); s=np.zeros(len(p));s[o]=np.pi*a
    q,i=dirichlet(L,b,a/np.linalg.norm(p[b],axis=1),s)
    return p,e,b,o,L,s,q,i

def tetra_read(values,h=1.,parity=1):
    return 3/(4*np.sqrt(3)*h)*((parity*A/np.sqrt(3)).T@values)

def fields(r,a=1.):
    q=a/np.asarray(r); psi=1+q; N=(1-q)/(1+q); B=psi**2
    return N,B,psi

def conformal_data(x,a=1.):
    """f=ln B; spatial metric exp(2f) I. Gradient, Hessian exact."""
    x=np.array(x,float);r=np.linalg.norm(x); n=x/r
    fp=-2*a/(r*(r+a)); fpp=2*a*(2*r+a)/(r*r*(r+a)**2)
    return fp*n,fpp*np.outer(n,n)+(fp/r)*(np.eye(3)-np.outer(n,n))

def ricci(x,a=1.):
    g,h=conformal_data(x,a)
    return -h+np.outer(g,g)-(np.trace(h)+g@g)*np.eye(3)

def spin_transport(loop,a=1.):
    """Orthonormal frame Levi-Civita transport of conformal 3-metric."""
    U=np.eye(3)
    for x,y in zip(loop[:-1],loop[1:]):
        d=y-x
        def rhs(t,z):
            g,_=conformal_data(x+t*d,a); omega=np.outer(d,g)-np.outer(g,d)
            return (-omega@z.reshape(3,3)).ravel()
        U=solve_ivp(rhs,[0,1],U.ravel(),rtol=2e-11,atol=2e-13).y[:,-1].reshape(3,3)
    return U

def hex_loop(center,scale):
    s,t,u=A[:3]; steps=np.array([s,-t,u,-s,t,-u]); pts=np.vstack([np.zeros(3),np.cumsum(steps,axis=0)])
    return np.asarray(center)+scale*(pts-pts[:-1].mean(0))

def optical_index(r,a=1.,kind='full'):
    N,B,_=fields(r,a)
    return {'full':B/N,'time':1/N,'space':B}[kind]

def bending(b,a=1.,kind='full'):
    # outer turning point (weak-field samples for all kinds, strong full only)
    low=a*(2+np.sqrt(3)) if kind=='full' else max(a*1.01,b*.4)
    r0=brentq(lambda r:r*optical_index(r,a,kind)-b,low,b,xtol=1e-12)
    m=b/r0
    def integrand(t):
        y=1-t*t; n=optical_index(r0/y,a,kind) if y else 1.
        return 2*t*m/np.sqrt(max(n*n-m*m*y*y,1e-30))
    val=quad(integrand,0,1,epsabs=1e-10,epsrel=1e-10)[0]
    return 2*val-np.pi

def chars(V,N=1.,B=1.):return np.array([V+N/B,V-N/B])

def overlap_kernel(shift=(0.,0.),F2=None):
    """Exact planar polygons up to floating precision; common midplane assumed.
    Normalization uses original tile area, fixed on the first triangle.
    Second triangle may move/shear in this plane; not an unconstrained 3D intersection.
    """
    from shapely.geometry import Polygon
    tri,_=interface(); s=np.ones(3); e=np.array([1.,-1.,0.])/np.sqrt(2); f=np.cross(s/np.sqrt(3),e); proj=np.column_stack([e,f]); T=tri@proj
    def tiles(t):
        mid=lambda i,j:(t[i]+t[j])/2
        return [Polygon([t[i],mid(i,(i+1)%3),mid(i,(i+2)%3)]) for i in range(3)]+[Polygon([mid(0,1),mid(1,2),mid(2,0)])]
    U=-T if F2 is None else -T@np.asarray(F2).T
    U=U+shift; X=tiles(T); Y=tiles(U)
    M=np.array([[x.intersection(y).area for y in Y] for x in X]);return M/X[0].area,M

def deformed_bloch(k,kernels):
    from native_cell import F
    X=-sum(np.exp(1j*A[i]@k)*F[i]@kernels[i]@F[i+4].T for i in range(4))
    return np.block([[H,X],[X.conj().T,H]])

def lapse_hessian(x,a=1.):
    x=np.asarray(x,float);r=np.linalg.norm(x);n=x/r; N,B,psi=fields(r,a)
    d=2*a/(r+a)**2; dd=-4*a/(r+a)**3; g=d*n; Hess=dd*np.outer(n,n)+(d/r)*(np.eye(3)-np.outer(n,n))
    f,_=conformal_data(x,a)
    return Hess-np.outer(f,g)-np.outer(g,f)+np.eye(3)*(f@g)
