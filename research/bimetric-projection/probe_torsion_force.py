"""Which irreducible torsion parts can push a slow particle?
Autoparallel: d^2x^i/dt^2 = -Gamma^i_(00) = -({i 00} + K^i_(00)), weak field, flat eta.
Convention: T^l_mn = Gamma^l_mn - Gamma^l_nm, K^l_mn = 1/2 (T^l_mn + T_m^l_n + T_n^l_m)  (so Gamma = LC + K)."""
import numpy as np, itertools
eta=np.diag([-1.,1,1,1])
def lower(T): return np.einsum('al,lmn->amn',eta,T)          # T_{a m n}
def raise_mid(Tl): return np.einsum('lb,abn->aln',eta,Tl)      # helper
def contorsion(T):
    Tl=lower(T)                               # T_{l m n}
    # T_m^l_n = eta^{l a} T_{m a n};  K^l_{mn} = 1/2 (T^l_mn + T_m^l_n + T_n^l_m)
    A=np.einsum('la,man->lmn',eta,Tl); Bt=np.einsum('la,nam->lmn',eta,Tl)
    return 0.5*(T+A+Bt)
def check_autoparallel_identity():
    # Gamma = LC + K reproduces torsion T: K^l_mn - K^l_nm = T^l_mn
    T=np.random.default_rng(0).normal(size=(4,4,4)); T=T-T.transpose(0,2,1)
    K=contorsion(T); return np.allclose(K-K.transpose(0,2,1),T)
print("contorsion reproduces torsion:",check_autoparallel_identity())
eps=np.zeros((4,4,4,4))
for p in itertools.permutations(range(4)):
    eps[p]=np.linalg.det(np.eye(4)[list(p)])
def vector(v):  # T^l_mn = (delta^l_n v_m - delta^l_m v_n)/3
    d=np.eye(4); return (np.einsum('ln,m->lmn',d,v)-np.einsum('lm,n->lmn',d,v))/3
def axial(a):   # T^l_mn = eta^{lb} eps_{b m n r} a^r
    return np.einsum('lb,bmnr,r->lmn',eta,eps,a)
def proj_tensor(T):
    v=np.einsum('lml->m',T)               # trace T^l_{m l}
    Tv=vector(v*(-1))*(-1)                # fix below by solving
    return v
# build bases of the three sectors numerically
rng=np.random.default_rng(1)
def force(T): K=contorsion(T); return np.array([K[i,0,0] for i in range(1,4)])  # symmetric part at (00) = K^i_00 itself
basisV=[vector(e) for e in np.eye(4)]
basisA=[axial(e) for e in np.eye(4)]
# full torsion space basis
full=[]
for l in range(4):
    for m in range(4):
        for n in range(m+1,4):
            T=np.zeros((4,4,4)); T[l,m,n]=1; T[l,n,m]=-1; full.append(T)
def vec(T): return T.reshape(-1)
Mfull=np.array([vec(T) for T in full]).T
# tensor sector = orthogonal complement (Euclidean) of vector+axial inside torsion space, restricted to trace-free & no totally-antisym part
VA=np.array([vec(T) for T in basisV+basisA]).T
# trace-free, axial-free condition: linear constraints
def trace(T): return np.einsum('lml->m',T)
def totanti(T):
    Tl=lower(T); return np.array([np.einsum('abcd,bcd->a',eps,Tl)])
cons=[]
for T in full: cons.append(np.concatenate([trace(T),np.einsum('abcd,bcd->a',eps,lower(T))]))
C=np.array(cons).T          # 8 x 24 constraint matrix on coefficients
import scipy.linalg as sl
ns=sl.null_space(C)          # 24 x 16
basisT=[sum(c*T for c,T in zip(col,full)) for col in ns.T]
for name,bas in (("vector (4)",basisV),("axial (4)",basisA),("tensor (16)",basisT)):
    F=np.array([force(T) for T in bas])
    print(f"{name:12s} dim={len(bas):2d}  rank of map to slow-particle force K^i_(00): {np.linalg.matrix_rank(F,1e-10)}")
print("check: vector+axial+tensor span all 24:",np.linalg.matrix_rank(np.array([vec(T) for T in basisV+basisA+basisT]))==24)
# which vector components: spatial v_i only?
for k,e in enumerate(np.eye(4)): print("  v along e",k,"-> force",np.round(force(vector(e)),4))
