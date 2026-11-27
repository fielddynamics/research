import numpy as np
import pytest
from model import *

@pytest.mark.parametrize('N',[1,2,7,14,27,28])
def test_geometric_sum_against_direct(N):
    d=1.67; k=np.r_[np.random.default_rng(N).uniform(-20,20,100),0,np.pi/d,2*np.pi/d]
    np.testing.assert_allclose(array_closed(k,N,d),array_factor(k,np.arange(N)*d),atol=2e-11)

@pytest.mark.parametrize('N',[2,7,14,27,28])
def test_first_null_and_bragg(N):
    d=1.67;z=np.arange(N)*d
    assert abs(array_factor(np.pi/d,z))==pytest.approx(N)
    assert abs(array_factor(np.pi/(N*d),z))<1e-11

@pytest.mark.parametrize('N',[2,14,27,28])
def test_alternating_superperiod(N):
    d=1.67;a,b=.521,.592; w=np.where(np.arange(N)%2,b,a);p=np.arange(N)*d
    assert array_factor(np.pi/(2*d),p,w)==pytest.approx((N+1)//2*a-(N//2)*b,abs=1e-12)
    assert abs(array_factor(np.pi/d,p,w))==pytest.approx(w.sum())

@pytest.mark.parametrize('seed',range(3))
def test_translation_and_coherence_bound(seed):
    r=np.random.default_rng(seed);p=np.sort(r.uniform(0,46,27));w=r.uniform(0,1,27);k=r.uniform(0,10,30);F=array_factor(k,p,w)
    np.testing.assert_allclose(array_factor(k,p+3,w),F*np.exp(6j*k),atol=1e-11)
    assert np.all(np.abs(F)<=w.sum()+1e-12)

@pytest.mark.parametrize('fc',[0,23.2,45.3,88.5])
def test_dispersive_bragg(fc):
    d=1.67;f=np.hypot(fc,C/(2*d));assert axial_k(f,fc)==pytest.approx(np.pi/d)

@pytest.mark.parametrize('ratio',[.2,1,3,10,12.4])
def test_expansion_against_closed_form(ratio):
    for f in np.linspace(0,20,51):
        S=scatter(duct(f,L,ratio),1,1)
        assert abs(S[1,0])**2==pytest.approx(expansion_power(f,L,ratio),abs=1e-12)
        np.testing.assert_allclose(S.conj().T@S,np.eye(2),atol=2e-12)

@pytest.mark.parametrize('seed',range(5))
def test_lossless_reciprocal_cascade(seed):
    r=np.random.default_rng(seed);M=np.eye(2,dtype=complex);J=np.array([[0,1],[1,0]])
    for _ in range(5):
        f=r.uniform(.1,20);M=M@duct(f,r.uniform(.1,8),r.uniform(.5,12))@shunt(f,r.uniform(0,.02))
    np.testing.assert_allclose(M.conj().T@J@M,J,atol=1e-10)
    assert np.linalg.det(M)==pytest.approx(1,abs=1e-10)
    S=scatter(M,.7,1.5);np.testing.assert_allclose(S,S.T,atol=1e-10);np.testing.assert_allclose(S.conj().T@S,np.eye(2),atol=1e-10)

@pytest.mark.parametrize('a,b',[(1,1),(1,3),(3,1)])
def test_area_junction(a,b):
    S=scatter(np.eye(2),a,b);assert S[0,0]==pytest.approx((a-b)/(a+b));assert abs(S[1,0])**2==pytest.approx(4*a*b/(a+b)**2)

def test_slot_volume_and_locations():
    p,V=slots();assert len(p)==27 and p[-1]<L
    assert V.sum()==pytest.approx(2*.14*.18*(14*.521+13*.592))
    assert np.all(np.diff(p)>0)

def test_no_slot_limit():
    p,V=slots(); f=9.5;A=area()*CUBIT**2
    np.testing.assert_allclose(slot_chain(f,A,L,p,0*V),duct(f,L,A),atol=1e-12)

@pytest.mark.parametrize('f',[1,5,10,15,20])
def test_slot_chain_conserves_power(f):
    p,V=slots();S=scatter(slot_chain(f,area()*CUBIT**2,L,p,V),1,1)
    np.testing.assert_allclose(S.conj().T@S,np.eye(2),atol=2e-12)
    assert S[0,1]==pytest.approx(S[1,0],abs=1e-12)

@pytest.mark.parametrize('f',[0,5,10,15,20,100])
def test_position_independent_slot_bound(f):
    A=area()*CUBIT**2;_,V=slots(); rng=np.random.default_rng(102)
    for _ in range(10):
        p=np.sort(rng.uniform(0,L,len(V)))
        S=scatter(slot_chain(f,A,L,p,V),A,A)
        assert abs(S[0,0])**2<=shunt_reflection_bound(f,A,V)+1e-12
    # single shunt equality, checked separately
    S=scatter(shunt(f,V[0]),A,A)
    assert abs(S[0,0])**2==pytest.approx(shunt_reflection_bound(f,A,V[:1]),abs=1e-13)

def test_slot_bound_low_frequency():
    A=area()*CUBIT**2;_,V=slots();f=20
    assert shunt_reflection_bound(f,A,V)<(2*np.pi*f/C*V.sum()/(2*A))**2<.0002
