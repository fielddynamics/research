import itertools as it
import numpy as np
import pytest
U=7
V=range(8)
def wt(v):return v.bit_count()
def dot(a,b):return wt(a&b)%2
def orb(a,b):return min((a,b),(b,a^b),(a^b,a))
O=sorted({orb(a,b) for a in V for b in V})
D=sorted({orb(0,v) for v in range(1,8)})
N=sorted({orb(U,v) for v in range(1,7)})
Q=sorted(D+N)
def vec(v):return np.array([1-2*((v>>i)&1) for i in range(3)])
def proj(v):
    w=vec(v);return 3*w-w.sum() # 3 times planar projection, exact integers

def point(o):
    for v in range(1,8):
        if o==orb(0,v):return proj(v)
    for v in range(1,7):
        if o==orb(U,v):return 2*proj(v)
    raise ValueError(o)
def perm(v,p):return sum(((v>>i)&1)<<p[i] for i in range(3))
def normal(o):
    a,b=o;return next(n for n in range(1,8) if not dot(a,n) and not dot(b,n))

def test_orbits():
    assert len(O)==22 and len(Q)==13 and len(D)==7 and len(N)==6
    assert set(Q)=={o for o in O if o!=(0,0) and any(v in (0,U) for v in (o[0],o[1],o[0]^o[1]))}
def test_projection():
    assert len({tuple(point(o)) for o in Q})==13
    assert sorted(np.dot(point(o),point(o)) for o in Q)==[0]+[24]*6+[96]*6
    assert {tuple(point(o)) for o in N}=={tuple(2*point(o)) for o in D if o!=orb(0,U)}
@pytest.mark.parametrize('r',[1,2])
def test_hexagon(r):
    p=[r*proj(v) for v in range(1,7)]
    for a in p:
        assert sorted(int(a@b) for b in p)==[(-24)*r*r,-12*r*r,-12*r*r,12*r*r,12*r*r,24*r*r]
@pytest.mark.parametrize('p',list(it.permutations(range(3))))
def test_equivariant(p):
    for o in Q:
        op=orb(*(perm(v,p) for v in o))
        assert np.array_equal(point(op),point(o)[np.argsort(p)])
def test_antipodes_and_exchange():
    for v in range(1,7):
        assert np.array_equal(proj(v^U),-proj(v))
        assert orb(v,U)==orb(U,v^U)
        assert orb(0,v)==orb(v,0)
    assert orb(0,U)==orb(U,0)
def test_four_axes():
    exterior=set(O)-set(Q)-{(0,0)}
    assert len(exterior)==8
    ns={normal(o) for o in exterior}
    assert ns=={n for n in range(1,8) if dot(n,U)}
    assert all(sum(normal(o)==n for o in exterior)==2 for n in ns)
    M=np.stack([vec(n) for n in sorted(ns)])
    assert np.array_equal(M@M.T,4*np.eye(4,dtype=int)-1)
    assert np.array_equal(M.T@M,4*np.eye(3,dtype=int))
    assert np.array_equal(M.sum(axis=0),np.zeros(3))
def test_common_mode_label_isometry():
    f=np.array([3 if o==(0,0) else np.sqrt(3) if o in D else 0 for o in O])/np.sqrt(30)
    B=np.eye(22)[:,1:]; M=np.eye(22)-np.outer(f,f); L=M@B; G=L.T@L
    d=np.array([o in D for o in O[1:]],float); K=np.outer(d,d)/7
    assert np.allclose(G,np.eye(21)-.7*K)
    T=L@(np.eye(21)+(np.sqrt(10/3)-1)*K)
    assert np.allclose(T.T@T,np.eye(21)) and np.allclose(T@T.T,M)
    Qp=np.diag([o==(0,0) or o in Q for o in O]);
    assert np.allclose(T.T@Qp@T,np.diag([o in Q for o in O[1:]]))
    J=np.zeros((22,22))
    for i,(a,b) in enumerate(O):J[O.index(orb(b,a)),i]=1
    assert np.allclose(J@T,T@J[1:,1:])
    P=Qp+(np.eye(22)-Qp)@(np.eye(22)+J)/2
    assert np.isclose(np.trace(T.T@P@T),17)
@pytest.mark.parametrize('v',range(1,7))
def test_branch(v):
    assert set([orb(0,v),orb(0,v^U),orb(U,v),orb(U,v^U)]).issubset(Q)
    assert len({orb(0,v),orb(0,v^U),orb(U,v),orb(U,v^U)})==4
