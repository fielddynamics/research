"""Dimensionless native model + external GR benchmarks, not a derived metric."""
import numpy as np
from core_model import H0,V,CHI,energy,branch,outer,inner,O
from scipy.constants import G,c,physical_constants,astronomical_unit,parsec
U=physical_constants['atomic mass constant'][0]; MEV=physical_constants['atomic mass constant energy equivalent in MeV'][0]
MASSES={1:4.00260325413,2:8.005305102,3:12.,4:15.99491461957,5:19.9924401762,6:23.985041697,7:27.97692653465,8:31.9720711744,9:35.967545105,10:39.962590863}
H4=np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])
W16=np.kron(H4,H4)/4; W64=np.kron(np.kron(H4,H4),H4)/8

def packed(k):
    # k complete four-address children in a 4x4 block; ordering is a model witness.
    return np.repeat(np.arange(4)<k,4).astype(float)

def alpha_binding(k):return (k*MASSES[1]-MASSES[k])*MEV

def overlap(p):return np.vdot(p,V@p).real/2

def F(u,t=1):return 2*(1+t)*(abs(u)-t*CHI*np.log1p(abs(u)/(t*CHI)))
def Fp(u,t=1):return 2*(1+t)*u/(t*CHI+abs(u))

def naive_clock(p,N,t=1):return N*np.vdot(p,H0@p).real+F(N*overlap(p),t)

def full_clock(p,N,t=1):return N*energy(p,t)

# A/B/O ownership; fixed geometry, use half endpoint allocation of each local bond.
LABEL=np.zeros(33,int)
for (s,i,j),k in outer.items():LABEL[k]=s
for (s,i),k in inner.items():LABEL[k]=s
LABEL[O]=2

def clock_local(p,N,t=1):
    D=np.sqrt(np.array(N)[LABEL]); q=D*p
    return np.vdot(q,H0@q).real+np.sqrt(N[0]*N[1])*F(overlap(p),t)

def source_local(p,t=1):
    return np.array([np.vdot(p[LABEL==i],(H0@p)[LABEL==i]).real for i in range(3)])+np.array([.5,.5,0])*F(overlap(p),t)

def load_tetb(k,phase=0.):
    # Existing row/base indexing. Each complete row is a four-address child.
    q=np.zeros(33,complex)
    for i in range(k):
        for j in range(4):
            idx=inner[1,i] if i==j else outer[1,i,j]
            q[idx]=np.exp(1j*phase*(4*i+j))
    return q

def compactness(m,r):return 2*G*m/(r*c*c)
def shell_factors(m,r):
    # static thin shells, cumulative gravitational masses; no EOS claimed.
    m=np.asarray(m,float);r=np.asarray(r,float);prev=np.r_[0,m[:-1]]
    co=compactness(m,r);ci=compactness(prev,r)
    if np.any(co>=1) or np.any(ci>=1):raise ValueError('not a static exterior shell configuration')
    return np.sqrt((1-co)/(1-ci))
def shell_log_clock(m,r):return np.log(shell_factors(m,r)).sum()

def hierarchy(n,compact=.4,ratio=2):
    r=ratio**np.arange(n,dtype=float);m=compact*c*c*r/(2*G);return m,r

def radial_chars(C):return 1-np.sqrt(C),-1-np.sqrt(C)
def null_product(C):
    a,b=radial_chars(C);return a*b

def benchmarks():
    ms=1.9884e30; earth=5.9722e24
    return [('He-4 nucleus proxy',MASSES[1]*U,1.2e-15*4**(1/3)),('C-12 nucleus proxy',12*U,1.2e-15*12**(1/3)),('O-16 nucleus proxy',MASSES[4]*U,1.2e-15*16**(1/3)),('Earth surface',earth,6.371e6),('Sun surface',ms,6.957e8),('Solar system at 1 AU',ms,astronomical_unit),('Solar Jacobi boundary',ms,1.44*parsec),('White dwarf example',.6*ms,7e6),('Neutron star example',1.4*ms,12e3),('Schwarzschild horizon',ms,2*G*ms/c**2)]
