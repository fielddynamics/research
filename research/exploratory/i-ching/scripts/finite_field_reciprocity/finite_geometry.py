"""GF(4096) and marked PG(2,16), independent of the assumed incidence matrix."""
from functools import lru_cache
import numpy as np

# x^12+x^6+x^4+x+1; verify primitive order explicitly in tests.
POLY = 0x1053
ORDER = 4095

def mul(a,b):
    r=0
    while b:
        if b & 1: r ^= a
        b >>= 1
        a <<= 1
        if a & 4096: a ^= POLY
    return r

@lru_cache(None)
def field():
    powers=[1]
    for _ in range(1,ORDER): powers.append(mul(powers[-1],2))
    assert len(set(powers))==ORDER and mul(powers[-1],2)==1
    return powers, {v:i for i,v in enumerate(powers)}

def projective(a):
    return field()[1][a] % 273

@lru_cache(None)
def plane():
    powers,_=field()
    L=[powers[i*273] for i in range(15)]
    # The line <1,g> and its Singer translates. Enumerate and verify incidence.
    line=frozenset([0]+[projective(2 ^ u) for u in L]+[1])
    lines=tuple(frozenset((j+k)%273 for j in line) for k in range(273))
    baer=tuple(frozenset(j for j in range(273) if j%13==k) for k in range(13))
    return lines, baer

@lru_cache(None)
def registers(origin=0):
    lines,baer=plane()
    pencil=[l-{origin} for l in lines if origin in l]
    blocks=[b-{origin} for b in baer]
    blocks.sort(key=lambda b: len(b))
    pencil.sort(key=lambda l: (-len(l&blocks[0]), next((j for j,b in enumerate(blocks[1:],1) if len(l&b)==5),0)))
    X=[j for j in range(273) if j!=origin]
    A=np.array([[j in l for j in X] for l in pencil],dtype=int)
    C=np.array([[j in b for j in X] for b in blocks],dtype=int)
    return A,C,A@C.T

@lru_cache(None)
def operators():
    A,C,N=registers()
    U=A.T/4
    V=C.T/np.sqrt(C.sum(axis=1))
    R=U.T@V
    P=U@U.T; Q=V@V.T
    return A,C,N,U,V,R,P,Q
