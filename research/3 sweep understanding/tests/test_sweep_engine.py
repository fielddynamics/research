import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from itertools import combinations, permutations
import numpy as np
import pytest
from sweep_engine import *

def close(a,b):np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10)
def rank(a):return round(np.trace(a))
@pytest.fixture(scope='module')
def ledger():return pi_ledger(certified_octal())
@pytest.mark.parametrize('s,n',[(-1,13),(0,17),(1,21)])
def test_signed(s,n):assert coupling(s)==n
@pytest.mark.parametrize('n',[2,4,8,16,32,64])
def test_walsh(n):
    H=walsh(n);close(H@H,np.eye(n));x=np.arange(n)+1j*np.arange(n)[::-1];close(fwht(x),H@x)
@pytest.mark.parametrize('seed',range(8))
def test_tree(seed):
    x=np.random.default_rng(seed).normal(size=64);b=tree_read(x);close(np.linalg.norm(b),np.linalg.norm(x));close(b[0],sum(x)/8);close(detail_mix(b),fwht(x))
def test_orbit_structure():
    assert len(ORBITS)==22 and sorted(map(len,ORBITS))==[1]+[3]*21
    close(B.T@B,np.eye(22));close(W22@W22,np.eye(22));close(J22@J22,np.eye(22));close(W22@J22,J22@W22);assert rank((np.eye(22)+J22)/2)==15
    close(W@f,f);close(J@f,f);close(f@f,30);assert not np.allclose(FSEED,MEAN)
@pytest.mark.parametrize('u',range(1,8))
def test_mask(u):
    p=reduced_mask(u);close(p@p,p);assert rank(p)==13;close(p@f22,0)
@pytest.mark.parametrize('u,v',list(combinations(range(1,8),2)))
def test_pair(u,v):
    p,q=reduced_mask(u),reduced_mask(v);close(p@q,q@p);assert rank(p@q)==9;assert rank(reduced_mask(u,v))==17
@pytest.mark.parametrize('u,v,w',list(combinations(range(1,8),3)))
def test_triple(u,v,w):assert rank(reduced_mask(u,v,w))==(21 if u^v^w==0 else 19)
@pytest.mark.parametrize('order',list(permutations((3,5,6))))
def test_daughters(order):assert [rank(reduced_mask(*order[:k])) for k in (1,2,3)]==[13,17,21]
def test_orientation():
    S,C,M,A=orientation();I=np.eye(22);close(S@S,I);close(C@C@C,I);close(M@M,M);close(A@A,-M);close(A.T,-A);assert rank(M)==4;assert round(np.trace(S)-1)==13;assert not np.allclose(rotation(np.pi),S)
@pytest.mark.parametrize('theta',[0,np.pi/2,np.pi,2*np.pi/3,4*np.pi/3,2*np.pi])
def test_rotation(theta):
    U=rotation(theta);close(U.T@U,np.eye(22));close(np.trace(U)-1,17+4*np.cos(theta));close(np.linalg.det(U),1)
def test_pi_coverage(ledger):
    assert len(ledger)==332 and ledger[-1]['distinct']==64 and ledger[-2]['distinct']==63
    assert (ledger[-1]['a'],ledger[-1]['b'])==(3,2);assert bank_boundaries(ledger)==[156,192,332]
    assert [ledger[i-1]['bank3'] for i in (156,192,332)]==[13,17,21]
    assert [ledger[i-1]['distinct'] for i in (156,192,332)]==[54,60,64]
    assert next(z['step'] for z in ledger if z['orbit']==0)==87
    assert (ledger[155]['bank2']+ledger[155]['bank3'],ledger[191]['bank3'])==(32,17)
def test_no_exact_mask_match(ledger):
    d=first_seen_masks(ledger);nonzero=set(range(1,22))
    assert not any(d[155]==support(u)&nonzero for u in range(1,8))
    assert not any(d[191]==(support(u)|support(v))&nonzero for u,v in combinations(range(1,8),2))
@pytest.mark.parametrize('seed',range(8))
def test_stream(ledger,seed):
    x=np.random.default_rng(seed).normal(size=(8,8));h=walsh(8);close(stream_walsh(ledger,x),h@x@h)
def test_orbit_fourier():
    F=orbit_fourier();close(F@F.T,np.eye(3));x=np.array([1,4,8]);close(F.T@F@x,x)
def test_innovations(ledger):
    inv=read_innovations(ledger);ds=[d for _,d,_ in inv if rank(d)==1];assert len(ds)==21
    assert next(n for n,d,L in inv if rank(L)==21)==104
    assert next(z['step'] for z in ledger if z['seen_orbits']==22)==156
    close(sum(ds),np.eye(22)-MEAN)
    for d in ds:close(d@d,d)
    for d,e in combinations(ds,2):close(d@e,0)
@pytest.mark.parametrize('t',[0.25,0.8,1.0,0.5+0.2j])
def test_transfer(ledger,t):
    for n,d,L in read_innovations(ledger):
        T=transfer(L,t);close(np.linalg.det(T.conj().T@T),abs(t)**(2*rank(L)))
def test_flag():
    p,g=signed_flag();assert [rank(x) for x in p]==[1,2,6,22];assert [rank(x) for x in g]==[1,4,16]
    for x in g:close(x@x,x)
    for x,y in combinations(g,2):close(x@y,0)
    close(sum(g),p[-1]-p[0]);assert [round(np.trace(g[0]+s*g[1]+g[2])) for s in (-1,0,1)]==[13,17,21]
def test_cyclic_not_xor():
    H=walsh(8);C=np.roll(np.eye(8),1,axis=0);close(np.linalg.matrix_power(C,8),np.eye(8));assert not np.allclose(C@C,np.eye(8));D=H@C@H;close(np.linalg.norm(D-np.diag(np.diag(D))),sqrt(5))
def test_seed_not_zero_deletion():assert not np.allclose(W22[:,0],np.eye(22)[:,0])
def test_spatial_obstruction():assert (64+2*2**2)//3==24!=len(ORBITS)

@pytest.mark.parametrize('depth',range(4))
def test_prefix_projector(depth):
    E=np.column_stack([prefix_read(x,depth) for x in np.eye(64)])
    close(E,E.T);close(E@E,E);assert rank(E)==4**depth
    for j in range(4):
        F=np.column_stack([prefix_read(x,j) for x in np.eye(64)])
        close(E@F,np.column_stack([prefix_read(x,min(depth,j)) for x in np.eye(64)]))

@pytest.mark.parametrize('seed',range(8))
def test_progressive_snapshot(seed):
    rng=np.random.default_rng(seed);x=rng.normal(size=64)+1j*rng.normal(size=64)
    parts=progressive_snapshot(x);close(sum(parts),x)
    close(sum(np.vdot(z,z) for z in parts),np.vdot(x,x))
    for a,b in combinations(parts,2):close(np.vdot(a,b),0)
    for d in range(4):close(sum(parts[:d+1]),prefix_read(x,d))
    y=tree_read(x).reshape(4,4,4)
    for d,mask in [(0,(0,0,0)),(1,(slice(1,None),0,0)),(2,(slice(None),slice(1,None),0)),(3,(slice(None),slice(None),slice(1,None)))]:
        close(np.linalg.norm(parts[d]),np.linalg.norm(y[mask]))

@pytest.mark.parametrize('s',[-1,0,1])
def test_prefix_grade_character(s):
    p,g=signed_flag();a=g[0]+s*g[1]+g[2]
    assert rank(a)==coupling(s)
    assert np.linalg.matrix_rank(a,tol=1e-9)==(17 if s==0 else 21)
    assert [rank(z) for z in g]==[1,4,16]
