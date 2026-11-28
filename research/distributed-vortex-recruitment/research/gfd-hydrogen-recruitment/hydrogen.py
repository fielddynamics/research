"""Hydrogen recruitment research: fixed diamond network and conditional envelope.
Atomic units use reduced mass. Electrostatic input is conventional, not a GFD derivation.
"""
import numpy as np
from scipy.sparse import coo_matrix, eye, diags
from scipy.sparse.linalg import eigsh, spsolve
from scipy.linalg import eigh_tridiagonal
from native_cell import A,bloch

def lattice(h,R=7.):
    n=int(np.ceil(R/h))+2
    pts=[]
    for x in range(-n,n+1):
        for y in range(-n,n+1):
            for z in range(-n,n+1):
                if (x*x+y*y+z*z)*h*h>R*R:continue
                if x%2==y%2==z%2==0 and (x+y+z)%4==0:pts.append((x,y,z))
                elif x%2==y%2==z%2==1 and (x+y+z)%4==3:pts.append((x,y,z))
    p=np.array(pts); lookup={tuple(v):i for i,v in enumerate(p)}; ii=[];jj=[]; boundary=np.zeros(len(p))
    for i,v in enumerate(p):
        for s in (A if v[0]%2==0 else -A):
            j=lookup.get(tuple(v+s))
            if j is None:boundary[i]+=1/(h*np.linalg.norm(v+s))
            else:ii.append(i);jj.append(j)
    adj=coo_matrix((np.ones(len(ii)),(ii,jj)),shape=(len(p),len(p))).tocsr()
    L=(4*eye(len(p),format='csr')-adj)/(2*h*h)
    return p*h,L,boundary/(2*h*h),lookup[(0,0,0)]

def ground(h,R=7.):
    p,L,b,i=lattice(h,R);r=np.linalg.norm(p,axis=1);vol=8*h**3
    source=np.zeros(len(r));source[i]=4*np.pi/vol
    phi=spsolve(L,source+b)
    # Finite-volume regularization at origin; all other sites use conventional Coulomb.
    V=-1/np.maximum(r,1e-30);V[i]=-1.5/((3*vol/(4*np.pi))**(1/3))
    def solve(v):
        H=L/2+diags(v); vals,vec=eigsh(H,k=1,which='SA',tol=2e-10,v0=np.exp(-r)); psi=vec[:,0];psi*=np.sign(psi.sum());prob=psi**2
        return vals[0],psi,float(prob@r),float(np.linalg.norm(H@psi-vals[0]*psi))
    E,psi,mean,res=solve(V); Eg,pg,mg,rg=solve(-phi)
    return dict(h=h,R=R,p=p,L=L,b=b,i=i,r=r,vol=vol,phi=phi,E=E,psi=psi,mean=mean,res=res,Eg=Eg,pg=pg,mg=mg,rg=rg,source=source)

def radial(l,h=.01,R=45,n=3):
    r=np.arange(h,R,h); diag=1/h**2-1/r+l*(l+1)/(2*r*r)
    return eigh_tridiagonal(diag,np.full(len(r)-1,-.5/h**2),select='i',select_range=(0,n-1))[0]

def band(k,filtered=True):return np.linalg.eigvalsh(bloch(np.array(k),filtered))[0]

def q_enc(r):return np.exp(-2*r)*(1+2*r+2*r*r)
def phi_neutral(r):return np.exp(-2*r)*(1+1/r)

def mass_fraction(r,mp=1836.15267343):return (mp+1-q_enc(r))/(mp+1)
