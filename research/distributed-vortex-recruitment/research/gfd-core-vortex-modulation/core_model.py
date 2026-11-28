"""Stage VII weighted 33-coordinate graph, reconstructed from the published bond dictionary.
All variables dimensionless. No new oscillator. Existing constitutive gain, fixed t=1 by default.
"""
import numpy as np
from scipy.linalg import eigh, null_space
from itertools import product
G=np.array([[3.,-1,0],[-1,3,0],[0,0,1]])
M=np.array([[-2,.5,-2],[-.5,1,-1],[-5,-1,-8.9]])
C=np.array([[0,-.5,0],[-.5,0,-1],[1,-3,1]])
A=M-C
X=np.array([1/3,1,-4/15]); CHI=59/308
S=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
Z=np.array([1,1j,0])/np.sqrt(2)
outer={(s,i,j):n for n,(s,i,j) in enumerate((s,i,j) for s in range(2) for i in range(4) for j in range(4) if i!=j)}
inner={(s,i):24+4*s+i for s in range(2) for i in range(4)}
O=32
H=np.zeros((33,33)); V=H.copy()
def bond(i,j,w,cross=False):
    H[i,j]=H[j,i]=w
    if cross: V[i,j]=V[j,i]=w
for (s,i,j),k in outer.items():
    for l in range(4):
        if l not in (i,j): bond(k,outer[s,i,l],-1)
    bond(k,outer[1-s,j,i],-.5,True)
    bond(k,inner[s,i],-2)
    bond(k,inner[1-s,j],-1,True)
for (s,i),k in inner.items():
    H[k,k]=-9.9
    bond(k,O,-1)
    for j in range(4):
        if i!=j: bond(k,inner[1-s,j],-1,True)
H0=H-V

def embed(z=Z,odd=False):
    q=S@z; B=np.zeros((33,3),complex)
    for (s,i,j),k in outer.items(): B[k,:2]=((-1)**s if odd else 1)*np.array([q[i],q[j]])
    for (s,i),k in inner.items(): B[k,2]=((-1)**s if odd else 1)*q[i]
    return B/np.sqrt(8)
B=embed()

def gain(u,t=1): return (1+t)*u/(t*CHI+abs(u))
def curvature(u,t=1): return 2*(1+t)*t*CHI/(t*CHI+abs(u))**2
def energy(p,t=1):
    u=np.vdot(p,V@p).real/2
    return np.vdot(p,H0@p).real+2*(1+t)*(abs(u)-t*CHI*np.log1p(abs(u)/(t*CHI)))
def rhs(p,t=1): return -1j*(H0+gain(np.vdot(p,V@p).real/2,t)*V)@p
# M(g) eigenvector normalized in G, choose continuation by largest eigenvalue (simple on tested interval).
R=np.linalg.cholesky(G).T; Ri=np.linalg.inv(R)
def branch(g,t=1):
    ev,Y=eigh(R@(A+g*C)@Ri); y=Y[:,-1]; x=Ri@y
    if x@G@X<0: x=-x; y=-y
    h=x@G@C@x/2
    u=t*CHI*g/(1+t-g)
    n=u/h
    p=np.sqrt(n)*(B@x)
    Q=null_space(y[None,:]); l=Q.T@(R@(A+g*C)@Ri-ev[-1]*np.eye(3))@Q
    b=Q.T@R@C@x
    real=l+curvature(u,t)*n/2*np.outer(b,b)
    growth=np.max(np.linalg.eigvals(-l@real).real)
    return dict(g=g,n=n,u=u,omega=ev[-1],p=p,x=x,core=x[2]**2,h=h,real_max=np.linalg.eigvalsh(real)[-1],growth_sq=growth,energy=energy(p,t))

def current(p,g):
    K=H0+g*V
    return 2*np.imag(p[:,None]*K.T*p.conj()[None,:])
def core_moment(p,g):
    J=current(p,g); out=np.zeros(3)
    for i in range(4):
        for j in range(4):
            if i!=j: out+=J[inner[0,i],inner[1,j]]*np.cross(S[i]/3,-S[j]/3)
    return out
