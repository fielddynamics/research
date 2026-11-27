"""Finite read-register model, not a microscopic physical field simulator."""
from fractions import Fraction as F
from itertools import product
from math import sqrt
import numpy as np

K=4
PAIRS=list(product(range(8),repeat=2))

def coupling(s,k=K): return 1+s*k+k*k

def walsh(n):
    return np.array([[(-1)**((a&b).bit_count()) for b in range(n)] for a in range(n)],dtype=float)/sqrt(n)

def fwht(x):
    """Normalized binary butterfly, also valid for complex snapshots."""
    z=np.asarray(x,dtype=np.result_type(x,float)).copy(); n=len(z)
    assert n>0 and n&(n-1)==0
    k=1
    while k<n:
        for i in range(0,n,2*k):
            a=z[i:i+k].copy(); b=z[i+k:i+2*k].copy()
            z[i:i+k]=a+b;z[i+k:i+2*k]=a-b
        k*=2
    return z/sqrt(n)

def tree_read(x):
    """Fine to coarse, 16 + 4 + 1 four-port reads."""
    h=walsh(4);z=np.asarray(x).reshape(4,4,4).copy().astype(np.result_type(x,float))
    for a,b in product(range(4),repeat=2): z[a,b,:]=h@z[a,b,:]
    for a in range(4): z[a,:,0]=h@z[a,:,0]
    z[:,0,0]=h@z[:,0,0]
    return z.ravel()

def detail_mix(x):
    h=walsh(4);z=np.asarray(x).reshape(4,4,4).copy()
    for c in range(1,4):z[:,:,c]=h@z[:,:,c]@h
    for b in range(1,4):z[:,b,0]=h@z[:,b,0]
    return z.ravel()

def r(p): a,b=p;return b,a^b

def orbit(p): return tuple(sorted({p,r(p),r(r(p))}))
ORBITS=sorted({orbit(p) for p in PAIRS})
OID={p:i for i,o in enumerate(ORBITS) for p in o}
WEIGHTS=np.array([len(o) for o in ORBITS],dtype=float)
B=np.array([[float(p in o)/sqrt(len(o)) for o in ORBITS] for p in PAIRS])
W=np.array([[(-1)**(((a&d).bit_count()+(b&c).bit_count())%2) for c,d in PAIRS] for a,b in PAIRS],dtype=float)/8
J=np.array([[int(p==(q[1],q[0])) for q in PAIRS] for p in PAIRS],dtype=float)
W22=B.T@W@B; J22=B.T@J@B
# The I-Ching common seed is distinct from uniform mean.
f=np.array([int(a==0)+int(b==0)+int(a==b) for a,b in PAIRS],dtype=float)
f22=B.T@f; FSEED=np.outer(f22,f22)/30
m=np.sqrt(WEIGHTS)/8; MEAN=np.outer(m,m)

def support(u): return {i for i,o in enumerate(ORBITS) if any(v in (0,u) for v in (o[0][0],o[0][1],o[0][0]^o[0][1]))}

def mask_projector(ids):return np.diag([float(i in ids) for i in range(22)])

def reduced_mask(*axes):return mask_projector(set.union(*(support(u) for u in axes)))-FSEED

def orientation(u=7):
    q=mask_projector(support(u)); s=q+(np.eye(22)-q)@J22
    c=s@W22@s@W22
    M=(2*np.eye(22)-c-c@c)/3; A=(c-c@c)/sqrt(3)
    return s,c,M,A

def rotation(theta):
    _,_,M,A=orientation();return np.eye(22)+(np.cos(theta)-1)*M+np.sin(theta)*A

def certified_octal(n=332,terms=270):
    """BBP rational bounds; lower/upper agree on floor(pi*8**n)."""
    # each BBP term positive and bounded by 4/((8k+1)*16**k)
    lo=sum((4*F(1,8*k+1)-2*F(1,8*k+4)-F(1,8*k+5)-F(1,8*k+6))/16**k for k in range(terms))
    hi=lo+F(64,15*(8*terms+1)*16**terms)
    a,b=int(lo*8**n),int(hi*8**n)
    if a!=b: raise ValueError('uncertified prefix: increase terms')
    return format(a,'o')

def pi_ledger(digits):
    v=int(digits[0]);seen=set(); members=[set() for _ in ORBITS]; rows=[]
    for step,d in enumerate(digits[1:],1):
        u=(v+int(d))%8;p=(v,u);oid=OID[p];new=p not in seen;seen.add(p);members[oid].add(p)
        rows.append(dict(step=step,digit=int(d),a=v,b=u,orbit=oid,new=int(new),distinct=len(seen),bank1=sum(len(x)>=1 for x in members[1:]),bank2=sum(len(x)>=2 for x in members[1:]),bank3=sum(len(x)>=3 for x in members[1:]),seen_orbits=sum(bool(x) for x in members)))
        v=u
    return rows

def bank_boundaries(rows):return [next(z['step'] for z in rows if z[f'bank{i}']==21) for i in (1,2,3)]

def orbit_fourier():return np.array([[1/sqrt(3)]*3,[2/sqrt(6),-1/sqrt(6),-1/sqrt(6)],[0,1/sqrt(2),-1/sqrt(2)]])

def residual(unread):
    """Orthonormalized version of the weighted, known-mean projector."""
    u=np.array([float(i in unread) for i in range(22)]);v=u*m
    return np.diag(u)-np.outer(v,v)/(v@v) if v@v else np.zeros((22,22))

def resolved(unread): return np.eye(22)-MEAN-residual(unread)

def read_innovations(rows):
    unread=set(range(22));old=residual(unread);out=[]
    for row in rows:
        unread.discard(row['orbit']);new=residual(unread);d=old-new
        out.append((row['step'],d,resolved(unread)));old=new
    return out

def signed_flag():
    """Internal simultaneous digit action on recursive prefix addresses."""
    # order-3 permutation fixes zero and cycles 1,2,3 on each digit
    addresses=list(product(range(4),repeat=3));rot=lambda a:tuple(0 if x==0 else x%3+1 for x in a)
    P=np.array([[float(a==rot(b)) for b in addresses] for a in addresses]);Q=(np.eye(64)+P+P@P)/3
    prefix=[]
    for d in range(4):
        E=np.array([[float(a[:d]==b[:d])/4**(3-d) for b in addresses] for a in addresses]);prefix.append(Q@E)
    return prefix,[prefix[d]-prefix[d-1] for d in (1,2,3)]

def stream_walsh(rows,x):
    H=walsh(8);y=np.zeros((8,8),dtype=np.result_type(x,float))
    for z in rows:
        a,b=z['a'],z['b']
        if z['new']:y+=x[a,b]*np.outer(H[:,a],H[:,b])
    return y

def transfer(L,t):return np.eye(len(L))+(t-1)*L

def first_seen_masks(rows):
    seen=set();done=[];slots=[set() for _ in ORBITS]
    for z in rows:
        p=(z['a'],z['b']);seen.add(p);slots[z['orbit']].add(p)
        done.append({i for i in range(1,22) if len(slots[i])==3})
    return done


def prefix_read(x, depth):
    """Broadcast the coherent prefix mean, orthogonal in counting inner product."""
    if depth not in range(4): raise ValueError('depth must be 0, 1, 2, or 3')
    z=np.asarray(x).reshape(4**depth,4**(3-depth))
    return np.broadcast_to(z.mean(axis=1,keepdims=True),z.shape).copy().ravel()


def progressive_snapshot(x):
    """Common scalar view and three orthogonal innovations; no native time claim."""
    e=[prefix_read(x,d) for d in range(4)]
    return [e[0]]+[e[d]-e[d-1] for d in (1,2,3)]
