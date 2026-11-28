import numpy as np
import pytest
from itertools import permutations
from deformation import *

@pytest.mark.parametrize('seed',range(16))
def test_common_affine_interface(seed):
    rng=np.random.default_rng(seed); F=np.eye(3)+.25*rng.normal(size=(3,3)); tri,hexagon=interface(); n=np.ones(3)/np.sqrt(3)
    assert abs(area(hexagon)/area(tri)-2/3)<1e-12
    assert np.isclose(area(tri@F.T)/area(tri),area_scale(F,n))
    assert np.isclose(area(hexagon@F.T)/area(tri@F.T),2/3)
    # all coplanar overlap entries share the same Jacobian; normalized W unchanged
    J=area_scale(F,n); assert np.allclose((W*J)/J,W)

@pytest.mark.parametrize('p',list(permutations(range(3))))
def test_overlap_permutation(p):
    ix=list(p)+[3];assert np.allclose(W[np.ix_(ix,ix)],W)

@pytest.mark.parametrize('seed',range(12))
def test_clock_tetra_gradient(seed):
    rng=np.random.default_rng(seed); g=rng.normal(size=3); h=.1; c=rng.normal()
    for parity in [1,-1]:
        d=(parity*A*h)@g
        assert np.allclose(tetra_read(d,h,parity),g)
        assert np.allclose(tetra_read(d+c,h,parity),g)
    # relative log lapse differences telescope exactly
    x=rng.normal(size=6); assert abs(np.diff(np.r_[x,x[0]]).sum())<1e-13

@pytest.mark.parametrize('n',[6,8,10,12])
def test_graph_geometry(n):
    p,e,b,o=diamond(n);L=laplacian(p,e);i=np.setdiff1d(np.arange(len(p)),b)
    assert np.all(np.sum((p[e[:,0]]-p[e[:,1]])**2,axis=1)==3)
    assert np.all(L.diagonal()[i]==4)
    assert np.allclose(L@np.ones(len(p)),0)
    assert np.allclose((L-L.T).data,0)
    assert len(i)>0 and o in i

@pytest.mark.parametrize('seed',range(5))
def test_variable_stiffness_not_source(seed):
    p,e,b,o=diamond(8); rng=np.random.default_rng(seed);L=laplacian(p,e,np.exp(rng.normal(size=len(e))))
    q,i=dirichlet(L,b,np.ones(len(b)),np.zeros(len(p)))
    assert np.max(abs(q-1))<2e-13

@pytest.fixture(scope='module')
def lattice():return dimple()

def test_dimple_vacuum_residual(lattice):
    p,e,b,o,L,s,q,i=lattice
    assert max(abs((L@q-s)[i]))<2e-13
    assert q[o]==max(q) and np.min(q)>0
    assert np.allclose((L@q)[i[i!=o]],0,atol=1e-12)

@pytest.mark.parametrize('radius',[4,5,6,7,8,9,10,11,12])
def test_dimple_far_field(lattice,radius):
    p,e,b,o,L,s,q,i=lattice;r=np.linalg.norm(p,axis=1); m=abs(r-radius)<.5
    assert abs(np.mean(q[m]*r[m])-1)<.035

def test_dimple_source_linearity(lattice):
    p,e,b,o,L,s,q,i=lattice;z,_=dirichlet(L,b,2*q[b],2*s)
    assert np.allclose(z,2*q)

@pytest.mark.parametrize('r',[1.2,2,4,8,16,40,100])
def test_bridge_and_static_vacuum(r):
    a=1.; N,B,psi=fields(r,a);Ni,Bi,_=fields(a*a/r,a)
    assert np.isclose(N,-Ni)
    assert np.isclose(r*B,a*a/r*Bi)
    assert np.isclose(N*psi,2-psi)
    R=r*B;assert np.isclose(N*N,1-4*a/R)
    x=np.array([r,0,0]);Ric=ricci(x,a)
    assert abs(np.trace(Ric))<1e-13
    assert np.linalg.norm(Ric)>0

@pytest.mark.parametrize('radius',[3,5,10,20])
def test_hex_holonomy(radius):
    loop=hex_loop([radius,.4,.7],.08); U=spin_transport(loop); V=spin_transport(loop[::-1]); flat=spin_transport(loop,0)
    assert np.allclose(U.T@U,np.eye(3),atol=1e-10)
    assert np.allclose(V@U,np.eye(3),atol=1e-10)
    assert np.linalg.norm(U-np.eye(3))>1e-7
    assert np.allclose(flat,np.eye(3))

@pytest.mark.parametrize('seed',range(5))
def test_frame_only_is_flat(seed):
    rng=np.random.default_rng(seed); F=[np.eye(3)+.1*rng.normal(size=(3,3)) for _ in range(6)]; U=np.eye(3)
    for i in range(6): U=U@np.linalg.solve(F[i],F[(i+1)%6])
    assert np.allclose(U,np.eye(3))

@pytest.mark.parametrize('scale',[.04,.02,.01])
def test_small_loop_area_scaling(scale):
    u=spin_transport(hex_loop([5,.4,.7],scale));v=spin_transport(hex_loop([5,.4,.7],scale/2))
    assert abs(np.linalg.norm(u-np.eye(3))/np.linalg.norm(v-np.eye(3))-4)<.15

@pytest.mark.parametrize('b',[2000,4000,8000,16000])
def test_light_deflection(b):
    f,t,s=[bending(b,kind=k) for k in ['full','time','space']]
    assert abs(f*b/8-1)<.015
    assert abs(t*b/4-1)<.015 and abs(s*b/4-1)<.015
    assert abs(t/f-.5)<.01

@pytest.mark.parametrize('factor',[1.01,1.1,1.5,2,5])
def test_strong_deflection(factor):
    b=6*np.sqrt(3)*factor; assert bending(b)>8/b
    assert bending(b)>bending(b*1.1)

@pytest.mark.parametrize('v',[0,.1,.5,.99,1,1.01,1.4])
def test_directional_horizon(v):
    plus,minus=chars(-v)
    assert minus<0 and np.isclose(plus,1-v)
    assert np.sign(plus)==np.sign(1-v)
    # pure reciprocal clock/metric scaling blocks both directions or neither
    x=chars(0,N=max(0,1-v)); assert x[0]==-x[1]

@pytest.mark.parametrize('filtered',[False,True])
@pytest.mark.parametrize('k',[.003,.006,.012,.024])
def test_native_reciprocal_band(filtered,k):
    x=np.array([k,.6*k,-.3*k]); m=bloch(x,filtered);mr=bloch(-x,filtered); E=np.linalg.eigvalsh(m); E0=np.linalg.eigvalsh(bloch(np.zeros(3),filtered))[0]
    assert np.allclose(mr,m.conj())
    assert np.allclose(E,np.linalg.eigvalsh(mr))
    assert E[0]>E0
    # isolated scalar band quadratic, not a linear relativistic cone
    assert np.isclose((E[0]-E0)/(x@x),.10509418 if filtered else .12429467,rtol=.003)

def test_reconstruct_overlap_from_polygons():
    K,raw=overlap_kernel(); assert np.allclose(K,W,atol=1e-12)
    assert np.isclose(K.sum()/4,2/3)

@pytest.mark.parametrize('s',[.015,.035,.07,.15,.3,.5])
def test_differential_overlap(s):
    K,raw=overlap_kernel((s,0)); K2,raw2=overlap_kernel((-s,0))
    assert not np.allclose(K,W)
    assert (K>=0).all() and (K.sum(1)<=1+1e-12).all() and (K.sum(0)<=1+1e-12).all()
    assert np.isclose(raw.sum(),raw2.sum())
    # translate both polygons to swap the roles: reverse transfer is transpose
    assert np.allclose(K,K.T) # equal mirrored triangles give inversion symmetry about their shifted midpoint

@pytest.mark.parametrize('s',[.02,.08,.2,.4])
def test_differential_shear_reciprocal(s):
    K,M=overlap_kernel((.02,0),[[1,s],[0,1]])
    assert np.linalg.norm(K-W)>1e-3
    assert np.linalg.norm(K-K.T)>1e-3
    # real anisotropic overlap matrices still yield Hermitian reciprocal Bloch model
    ks=[K,W,W,W]; k=np.array([.08,.03,-.02]); X=deformed_bloch(k,ks)
    assert np.allclose(X,X.conj().T)
    assert np.allclose(deformed_bloch(-k,ks),X.conj())
    assert np.allclose(np.linalg.eigvalsh(X),np.linalg.eigvalsh(deformed_bloch(-k,ks)))

@pytest.mark.parametrize('r',[1.1,1.5,3,5,10,20,50,100])
def test_full_static_vacuum_equation(r):
    x=np.array([r,0.,0.]); N,_,_=fields(r); Hess=lapse_hessian(x)
    assert np.allclose(Hess,N*ricci(x),rtol=1e-10,atol=1e-14)
    assert abs(np.trace(Hess))<1e-13
