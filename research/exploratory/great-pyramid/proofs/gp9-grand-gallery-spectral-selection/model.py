"""Grand Gallery: rigid-wall air acoustics, SI except cross-section mesh in cubits.
No GFD coupling or fitted resonance frequencies. Geometry is an idealized extrusion.
"""
from functools import lru_cache
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import eigsh
CUBIT=20.632*.0254
C=343.
L=88*CUBIT  # ideal north wall to Great Step, not virtual floor endpoint
WMAX=4*CUBIT
SLOT_LENGTHS=np.array([.521,.592])
SLOT_WIDTH=.14
SLOT_DEPTH=.18
H_PYRAMID=5776*.0254
ZSTAR=H_PYRAMID*(1-1/np.sqrt(2))
VIRTUAL_RUN=1688.9*.0254

def half_width(y, shape='stepped'):
    """Half-width in cubits; vertical coordinate normal to incline, not plumb.
    1-cubit bench, 3-cubit lower wall, 7 equal-height surrogate upper tiers.
    """
    y=np.asarray(y)
    if shape=='envelope': return np.full_like(y,2.,dtype=float)
    if shape=='equal_area': return np.full_like(y,area('stepped')/30,dtype=float)
    if shape=='stepped': upper=2-np.clip(np.floor((y-4)*7/11)+1,1,7)/7
    elif shape=='smooth': upper=2-np.clip((y-4)/11,0,1)**.75 # equal area, same endpoints
    else: raise ValueError(shape)
    return np.where(y<1,1.,np.where(y<4,2.,upper))

def area(shape='stepped'):
    if shape=='envelope': return 60.
    if shape in ('stepped','smooth','equal_area'): return 2*(1+6+110/7)
    raise ValueError(shape)

def moments():
    """Exact interval quadrature of polygonal area and first/second height moments, x^2."""
    edges=np.r_[0,1,4,4+np.arange(1,8)*11/7]
    a,b=edges[:-1],edges[1:]; w=half_width((a+b)/2)
    return np.array([sum(2*w*(b-a)),sum(w*(b*b-a*a)),sum(2*w*(b**3-a**3)/3),sum(2*w**3*(b-a)/3)])

@lru_cache(None)
def grid(shape='stepped', refine=1):
    """Half-domain cell-centred FV, missing faces = Neumann, x=0 mirror.
    Odd reflection adds 2/d^2 at axis faces. Mesh aligns with step edges.
    """
    d=1/(7*refine); x=(np.arange(14*refine)+.5)*d; y=(np.arange(105*refine)+.5)*d
    mask=x[None,:]<half_width(y,shape)[:,None]
    ids=np.full(mask.shape,-1); ids[mask]=np.arange(mask.sum()); n=mask.sum()
    rr=[];cc=[]
    for a,b in [(ids[:,:-1],ids[:,1:]),(ids[:-1,:],ids[1:,:])]:
        valid=(a>=0)&(b>=0); u=a[valid];v=b[valid];rr.extend([u,v]);cc.extend([v,u])
    rr=np.concatenate(rr);cc=np.concatenate(cc)
    A=coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()
    K=(diags(np.asarray(A.sum(axis=1)).ravel())-A)/d**2
    axis=np.zeros(n);axis[ids[:,0]]=2/d**2
    return x,y,mask,K.tocsr(),diags(axis).tocsr(),d

@lru_cache(None)
def modes(shape='stepped',refine=1,parity='even',n=8):
    x,y,mask,K,D,d=grid(shape,refine); A=K if parity=='even' else K+D
    ev,vec=eigsh(A,k=n,sigma=-.01,which='LM',v0=np.random.default_rng(42).normal(size=A.shape[0]))
    ev=np.maximum(ev,0); ev[ev<1e-10]=0
    return ev,vec

def cutoff(ev,c=C): return c*np.sqrt(np.maximum(ev,0))/(2*np.pi*CUBIT)
def axial_k(f,fc,c=C): return 2*np.pi/c*np.lib.scimath.sqrt(np.asarray(f)**2-np.asarray(fc)**2)
def odd_bound(c=C): return c/(2*WMAX)
def aperture_overlap(shape,refine,parity,width=2.,height=2.,n=8):
    """Normalized constant test profile on a centred rectangular patch in cubit coords.
    Not measured aperture; use as selection witness. Odd vanishes by reflection.
    """
    ev,v=modes(shape,refine,parity,n);x,y,mask,K,D,d=grid(shape,refine)
    q=((x[None,:]<width/2)&(y[:,None]<height))[mask].astype(float)
    return np.zeros(n) if parity=='odd' else v.T@q/np.linalg.norm(q)

def array_factor(k,positions,weights=None):
    p=np.asarray(positions); w=np.ones(len(p)) if weights is None else np.asarray(weights)
    return np.exp(2j*np.asarray(k)[...,None]*p)@w

def array_closed(k,N,d):
    x=np.asarray(k)*d
    # robust ratio, via reduced phase around multiples of pi
    z=(x+np.pi/2)%np.pi-np.pi/2
    return np.exp(1j*(N-1)*z)*N*np.sinc(N*z/np.pi)/np.sinc(z/np.pi)

def duct(f,length,A,c=C):
    """[p,U] left from right, normalized U by rho*c; time exp(+iwt)."""
    t=2*np.pi*f*length/c
    return np.array([[np.cos(t),1j*np.sin(t)/A],[1j*A*np.sin(t),np.cos(t)]])

def shunt(f,V,c=C):
    """Lumped rigid sealed recess compliance; normalized volume-velocity convention."""
    return np.array([[1,0],[1j*2*np.pi*f*V/c,1]],complex)

def scatter(M,A_left,A_right):
    """Power-normalized scattering matrix from transfer matrix. Z=1/A."""
    zl,zr=1/A_left,1/A_right
    a,b,c,d=M.ravel(); den=a+b/zr+zl*c+zl*d/zr
    s11=(a+b/zr-zl*c-zl*d/zr)/den
    s21=2*np.sqrt(zl/zr)/den
    s12=np.linalg.det(M)*s21
    s22=(-a+b/zr-zl*c+zl*d/zr)/den
    return np.array([[s11,s12],[s21,s22]])

def expansion_power(f,length,m,c=C):
    return 1/(1+.25*(m-1/m)**2*np.sin(2*np.pi*f*length/c)**2)

def slot_chain(f,A,length,positions,volumes):
    M=np.eye(2,dtype=complex); prev=0.
    for z,V in zip(positions,volumes):
        M=M@duct(f,z-prev,A)@shunt(f,V);prev=z
    return M@duct(f,length-prev,A)

def slots(N=27,d=1.67):
    """Illustrative centre spacing; alternate measured mean lengths; terminal omitted."""
    p=(np.arange(N)+.5)*d
    V=2*SLOT_WIDTH*SLOT_DEPTH*SLOT_LENGTHS[np.arange(N)%2]
    return p,V

def shunt_reflection_bound(f,A,volumes,c=C):
    """Upper bound for power reflection of shunts within uniform matched guide.
    Each shunt has rapidity asinh(|k| V/(2 A)); unitary propagation is diagonal
    phase in travelling-wave coordinates. Product norm submultiplicativity.
    Not a bound for the complete mismatched gallery or real slot impedances.
    """
    return np.tanh(np.arcsinh(abs(2*np.pi*f/c)*np.asarray(volumes)/(2*A)).sum())**2
