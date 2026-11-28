import numpy as np
import sympy as s
import pytest
from scipy.special import sph_harm_y
from bridge import *
from native_cell import bloch

@pytest.mark.parametrize('n,l',[(n,l) for n in range(1,6) for l in range(n)])
def test_norm_and_virial(n,l):
    assert abs(radial_moment(n,l,0)-1)<1e-9
    assert abs(radial_moment(n,l,-1)-1/n**2)<1e-9
    assert abs(radial_moment(n,l,-2)-1/(n**3*(l+.5)))<1e-9
    assert abs(radial_moment(n,l,1)-(3*n*n-l*(l+1))/2)<1e-8
@pytest.mark.parametrize('l',range(7))
def test_addition(l):
    theta=np.linspace(.01,3.13,79);phi=np.linspace(0,6.1,79)
    assert np.allclose(sum(abs(sph_harm_y(l,m,theta,phi))**2 for m in range(-l,l+1)),(2*l+1)/(4*np.pi),rtol=1e-12)
@pytest.mark.parametrize('l',range(1,6))
def test_shell_and_coherent_distinction(l):
    th=np.linspace(.05,3.09,100); ph=np.linspace(.01,5.9,100)
    y=np.array([sph_harm_y(l,m,th,ph) for m in range(-l,l+1)])
    assert np.ptp(np.sum(abs(y)**2,axis=0))<1e-12
    assert np.ptp(abs(np.sum(y,axis=0))**2)>0.05
@pytest.mark.parametrize('n',range(1,9))
def test_capacity(n):assert sum(2*(2*l+1) for l in range(n))==2*n*n
@pytest.mark.parametrize('z',[[1,0,0],[0,1,0],[0,0,1],[1,1j,0],[1,2j,3],[1+2j,3,4j]])
def test_port(z):
    Bs=port_operators(z); gg=np.array(G,float)
    assert np.allclose(Bs.sum(0),np.array(T,float))
    assert all(np.allclose(gg@b,b.conj().T@gg) for b in Bs)
    assert np.allclose(sum(np.array(tangent(b)) for b in Bs),tangent(np.array(T,float)))
def test_core_response():
    assert np.allclose(tangent(np.array(T,float)),[-3639415/71166942,-3597250/391418181])
def test_state_energy_vs_intensity():
    assert integrated_energy(2,0)==pytest.approx(integrated_energy(2,1),abs=1e-11)
    assert ipr(2,0,0)!=pytest.approx(ipr(2,1,0))
    assert radial_moment(2,0,1)==pytest.approx(6)
    assert radial_moment(2,1,1)==pytest.approx(5)
    assert energy(2)-energy(1)==.375
    assert abs(ipr(1,0,0)-1/(8*np.pi))<1e-11
@pytest.mark.parametrize('m',[-1,0,1])
def test_excitation_same_energy(m):
    assert radial_moment(2,1,-1)==pytest.approx(.25)
    assert energy(2)==-.125

def test_cubic_split():
    xx,yy,zz=s.symbols('xx yy zz');xyz=(xx,yy,zz)
    E=[2*zz**2-xx**2-yy**2,xx**2-yy**2];T2=[xx*yy,xx*zz,yy*zz]
    e=[cubic_expect(p,xyz) for p in E];t=[cubic_expect(p,xyz) for p in T2]
    assert len(set(e))==len(set(t))==1 and e[0]!=t[0]
    assert (2*e[0]+3*t[0])/5==s.Rational(3,5)
    assert all(cubic_expect(p,xyz)==s.Rational(3,5) for p in xyz)
    assert quartic_energy(3,2,e[0])-quartic_energy(3,2,t[0])==pytest.approx(p4(3,2)*float(e[0]-t[0])/12)
@pytest.mark.parametrize('a',[.1,.05,.025,.0125])
def test_diamond_expansion(a):
    for u in [np.array([1,0,0]),np.ones(3)/np.sqrt(3),np.array([1,2,3])/np.sqrt(14)]:
        k=a*u; lam=4-abs(np.exp(1j*S@k).sum()); approx=2*a*a-a**4/6*sum(u**4)-a**4*sum(u[i]**2*u[j]**2 for i in range(3) for j in range(i))
        assert abs(lam-approx)<2*a**6
@pytest.mark.parametrize('filtered',[False,True])
def test_native_band(filtered):
    e0=np.linalg.eigvalsh(bloch(np.zeros(3),filtered))[0]
    ds=[]
    for axis in np.eye(3):
        k=.002*axis;ds.append((np.linalg.eigvalsh(bloch(k,filtered))[0]-e0)/.002**2)
    assert np.ptp(ds)<1e-7
    assert np.mean(ds)==pytest.approx(.10509418 if filtered else .12429467,rel=1e-4)

@pytest.mark.parametrize('n,l',[(n,l) for n in range(1,5) for l in range(n)])
def test_energy_functional(n,l):
    assert integrated_energy(n,l)==pytest.approx(energy(n),abs=1e-10)
@pytest.mark.parametrize('R',[1.,2.,4.,6.,12.,20.])
def test_enclosed_energy_difference(R):
    expected=-R**2*(R-12)*(R-2)*np.exp(-R)/96
    assert integrated_energy(2,0,R)-integrated_energy(2,1,R)==pytest.approx(expected,abs=1e-11)
@pytest.mark.parametrize('gamma',[.01,.1,.5,1.])
def test_density_blind_to_phase_energy(gamma):
    # e^(i gamma z^2) times 1s has unchanged density and zero mean momentum;
    # grad phase=2 gamma z e_z. Delta T=2 gamma^2 <z^2>.
    assert radial_moment(1,0,2)/3==pytest.approx(1.)
    assert 2*gamma**2*radial_moment(1,0,2)/3==pytest.approx(2*gamma**2)
@pytest.mark.parametrize('z,weights',[([1,1j,0],[1,0,0,0]),([1,2j,3],[1,2,3,4]),([1,2,3],[1,-1,0,0])])
def test_weighted_port_stationary(z,weights):
    from scipy.optimize import root
    B=np.real(np.einsum('i,ijk->jk',weights,port_operators(z)))
    gn,cn,mn=map(lambda a:np.array(a,float),(G,C,M)); xx=np.array(x,float).ravel(); nn=float(n); ch=float(chi)
    def solve(e):
        def f(v):
            y=v[:3];u=y@gn@cn@y/(2*nn);gain=2*u/(ch+abs(u));return np.r_[(mn+(gain-1)*cn-e*B/2)@y-v[3]*y,y@gn@y-nn]
        sol=root(f,np.r_[xx,1.1]); assert np.linalg.norm(f(sol.x))<1e-8
        y=sol.x[:3];return np.array([y@gn@cn@y/(2*nn),y[2]**2/nn])
    eps=1e-5;assert np.allclose((solve(eps)-solve(-eps))/(2*eps),tangent(B),atol=1e-8)
