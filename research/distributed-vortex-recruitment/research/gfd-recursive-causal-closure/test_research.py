import numpy as np
import pytest
from research import *
from core_model import rhs,core_moment,gain
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def near(a,b,rtol=1e-8,atol=1e-9):np.testing.assert_allclose(a,b,rtol=rtol,atol=atol)

@pytest.mark.parametrize('k',range(5))
def test_four_complete_children(k):
    b=packed(k);w=W16@b
    near(w[0],k);near(w[1:].dot(w[1:]),4*k-k*k);near(w.reshape(4,4)[:,1:],0);near(W16.T@w,b)

@pytest.mark.parametrize('k',range(17))
def test_full_64_address_prefix(k):
    b=np.repeat(np.arange(16)<k,4).astype(float);z=W64@b
    near(z[0],k/2);near(z[1:].dot(z[1:]),4*k-k*k/4);near(z.reshape(16,4)[:,1:],0)

@pytest.mark.parametrize('k',range(2,11))
def test_nuclear_binding_registration(k):
    b=alpha_binding(k);near(MASSES[k],k*MASSES[1]-b/MEV)
    if k==2:assert -.093<b<-.091
    else:assert b>0

def test_universal_pair_bond_fails():
    pair=alpha_binding(2);assert pair<0<alpha_binding(3)
    assert abs(6*pair-alpha_binding(4))>14
    # A universal pair and triple interaction fixed by Be and C overpredicts oxygen.
    triple=alpha_binding(3)-3*pair
    assert abs(6*pair+4*triple-alpha_binding(4))>14

@pytest.mark.parametrize('g',[.9,1.,1.15,1.3,1.5,1.7,1.9])
def test_nonlinear_energy_clock_source(g):
    p=branch(g)['p'];u=overlap(p);h=1e-5
    naive=(naive_clock(p,1+h)-naive_clock(p,1-h))/(2*h)
    correct=(full_clock(p,1+h)-full_clock(p,1-h))/(2*h)
    near(naive-correct,u*Fp(u)-F(u),rtol=1e-7)
    assert naive>correct
    x=abs(u)/CHI;near(naive-correct,4*CHI*(np.log1p(x)-x/(1+x)),rtol=1e-7)

@pytest.mark.parametrize('g',[.9,1.,1.2,1.5,1.8])
@pytest.mark.parametrize('k',[0,1,2,3,4])
def test_registered_energy_at_native_clock(g,k):
    p=branch(g)['p']+.13*load_tetb(k,.37);h=1e-5;v=source_local(p)
    near(v.sum(),energy(p));near(clock_local(p,[1,1,1]),energy(p))
    near(clock_local(p,[.7,.7,.7]),.7*energy(p));near(clock_local(p,[1.4,1.4,1.4]),1.4*energy(p))
    for i in range(3):
        d=np.eye(3)[i]*h;near((clock_local(p,1+d)-clock_local(p,1-d))/(2*h),v[i],rtol=1e-7)

@pytest.mark.parametrize('k',[1,2,3,4])
def test_packing_does_not_fix_energy(k):
    q=load_tetb(k,0);r=load_tetb(k,.7)
    near(abs(q),abs(r));near(np.vdot(q,q),4*k);near(overlap(q),0);near(overlap(r),0)
    assert abs(energy(q)-energy(r))>.1
    # Pure TetB packing cannot generate a cross gain at initialization.
    near(gain(overlap(q)),0)

@pytest.mark.parametrize('n',[1,2,4,8,16,32,64,100])
def test_nested_shell_clock(n):
    m,r=hierarchy(n);f=shell_factors(m,r);near(f[0],np.sqrt(.6));near(f[1:],np.sqrt(.6/.8))
    near(shell_log_clock(m,r),.5*np.log(.6)+(n-1)*.5*np.log(.6/.8));near(compactness(m,r),.4)
    assert np.all(radial_chars(.4)[0]>0)

@pytest.mark.parametrize('C',[0,.01,.1,.4,.8,.99,1,1.01,1.5,2])
def test_causal_threshold(C):
    a,b=radial_chars(C);near(a*b,C-1);assert b<0
    assert np.sign(a)==np.sign(1-C)

@pytest.mark.parametrize('name,m,r',benchmarks())
def test_scale_benchmarks(name,m,r):
    C=compactness(m,r);near(C,2*G*(m*c*c)/(r*c**4),atol=0);assert C>0
    if name=='Schwarzschild horizon':near(C,1)
    else:assert C<1
    near(compactness(13*m,13*r),C,atol=0)

def test_shell_dimple_is_not_local_force():
    # A spherical shell gives constant interior lapse; finite difference vanishes.
    m,r=hierarchy(1);N=np.sqrt(1-compactness(m[0],r[0]));assert N<1
    def phi(x):return c*c*np.log(N) if x<r[0] else .5*c*c*np.log(1-compactness(m[0],x))
    near(phi(.2*r[0]),phi(.7*r[0]));assert phi(2*r[0])>phi(.7*r[0])

def test_global_clock_arbitrarily_small_without_local_trapping():
    m,r=hierarchy(100);assert np.exp(shell_log_clock(m,r))<1e-6
    assert np.max(compactness(m,r))<.401

def test_source_is_not_unique_from_uniform_time_rescaling():
    p=branch(1)['p'];base=source_local(p);delta=np.array([.2,-.2,0.])
    near(base.sum(),(base+delta).sum());assert not np.allclose(base,base+delta)
    near(clock_local(p,[.8]*3),clock_local(p,[.8]*3)+delta@np.array([.8]*3))

@pytest.mark.parametrize('k',[1,2,3,4])
@pytest.mark.parametrize('phase',[0.,.4,1.1])
def test_loaded_existing_vortex_conserves_energy_and_norm(k,phase):
    base=branch(1)['p'];p=base+.13*load_tetb(k,phase)
    sol=solve_ivp(lambda t,y:rhs(y),[0,2],p,t_eval=np.linspace(0,2,51),rtol=2e-10,atol=2e-12,method='DOP853')
    assert sol.success
    near(np.sum(abs(sol.y)**2,axis=0),np.vdot(p,p).real,atol=1e-8)
    near([energy(y) for y in sol.y.T],energy(p),atol=1e-8)
    assert max(np.linalg.norm(core_moment(y,gain(overlap(y)))) for y in sol.y.T)>0

@pytest.mark.parametrize('N',[.2,.5,.9,1.3])
def test_full_clock_scales_entire_nonlinear_trajectory(N):
    p=branch(1)['p']+.13*load_tetb(2,.7)
    a=solve_ivp(lambda t,y:N*rhs(y),[0,1],p,rtol=1e-11,atol=1e-13,method='DOP853')
    b=solve_ivp(lambda t,y:rhs(y),[0,N],p,rtol=1e-11,atol=1e-13,method='DOP853')
    near(a.y[:,-1],b.y[:,-1],atol=1e-9)

def test_energy_zero_is_not_selected_by_projective_motion():
    p=branch(1)['p']+.13*load_tetb(2,.7);d=2.3
    a=solve_ivp(lambda t,y:rhs(y)-1j*d*y,[0,1],p,rtol=1e-13,atol=1e-15,max_step=.01,method='DOP853')
    b=solve_ivp(lambda t,y:rhs(y),[0,1],p,rtol=1e-13,atol=1e-15,max_step=.01,method='DOP853')
    near(a.y[:,-1],np.exp(-1j*d)*b.y[:,-1]);assert d*np.vdot(p,p).real>0
