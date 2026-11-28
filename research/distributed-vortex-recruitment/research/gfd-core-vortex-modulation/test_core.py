import numpy as np
import pytest
from scipy.linalg import expm, eigh, null_space
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import solve_ivp
from core_model import *

def near(a,b,atol=1e-9,rtol=1e-8): np.testing.assert_allclose(a,b,atol=atol,rtol=rtol)

def test_native_geometry():
    assert np.count_nonzero(np.triu(H,1))==104
    assert np.count_nonzero(np.triu(V,1))==48
    near(H,H.T); near(V,V.T);near(B.conj().T@B,G)
    near(H@B,B@M);near(V@B,B@C);near(H0@B,B@A)
    near(G@M,M.T@G);near(G@C,C.T@G)

def test_original_state():
    d=branch(1);near(d['n'],1);near(d['omega'],1.1);near(d['u'],CHI);near(d['core'],2/77)
    near(d['x'],X/np.sqrt(X@G@X));near(np.linalg.norm(core_moment(d['p'],1)),8/693)

GS=[.4,.5,.6,.7,.8,.85,.9,1,1.1,1.25,1.4,1.5,1.65,1.75,1.9,1.99]
@pytest.mark.parametrize('g',GS)
def test_stationary_full_graph(g):
    d=branch(g);p=d['p']; assert d['n']>0
    near(np.vdot(p,p).real,d['n']);near(np.vdot(p,V@p).real/2,d['u']);near(gain(d['u']),g)
    near(rhs(p),-1j*d['omega']*p);near(p[O],0)
    near(np.sum(abs(p[24:32])**2)/d['n'],d['core'])

@pytest.mark.parametrize('g',GS)
def test_actual_core_current(g):
    d=branch(g);p=d['p'];J=current(p,g)
    near(J,-J.T);near(J.sum(1),0)
    core=J[24:28,28:32];near(core.sum(0),0);near(core.sum(1),0)
    assert np.linalg.norm(core)>0
    # Stage VII angular moment, with n normalization and g-scaled core bond.
    chirality=(-1j*np.cross(Z.conj(),Z)).real
    near(core_moment(p,g),-4*g*d['n']*d['core']/9*chirality)
    # Conjugating circulation reverses current, not the stationary energy or frequency.
    near(core_moment(p.conj(),g),-core_moment(p,g));near(energy(p.conj()),d['energy'])

@pytest.mark.parametrize('g',[.5,.65,.75,.8,.85,.9,1,1.2,1.4,1.6,1.8,1.95])
def test_hf_and_energy_derivative(g):
    eps=1e-5; d=branch(g);p=branch(g+eps);m=branch(g-eps)
    near((p['omega']-m['omega'])/(2*eps),2*d['h'],rtol=1e-6)
    dn=(p['n']-m['n'])/(2*eps);de=(p['energy']-m['energy'])/(2*eps)
    near(de,d['omega']*dn,rtol=1e-6)

@pytest.mark.parametrize('g',[.5,.65,.75,.8,.85,.9,1,1.2,1.4,1.6,1.8,1.95])
def test_fold_stability_identity(g):
    d=branch(g);x=d['x'];y=R@x;Q=null_space(y[None,:]);l=Q.T@(R@(A+g*C)@Ri-d['omega']*np.eye(3))@Q
    b=Q.T@R@C@x; hp=b@np.linalg.solve(-l,b);up=2*CHI/(2-g)**2
    eps=1e-5;dn=(branch(g+eps)['n']-branch(g-eps)['n'])/(2*eps)
    near(dn,(up-d['n']*hp)/d['h'],rtol=2e-6)
    assert (dn>0)==(d['growth_sq']<0)

@pytest.mark.parametrize('t',[.2,.5,1,1.5,2,3])
def test_fixed_unit_occupation_curvature_threshold(t):
    d=branch(1,t);near(d['n'],1);near(d['omega'],1.1);near(d['core'],2/77)
    assert (d['growth_sq']<0)==(t<222607/119913)

def test_fold_location_independent_methods():
    a=minimize_scalar(lambda g:branch(g)['n'],bounds=(.6,.99),method='bounded',options={'xatol':1e-13}).x
    b=brentq(lambda g:branch(g)['real_max'],.75,1,xtol=1e-13)
    near(a,b,atol=1e-7);near(b,.82682738752,atol=1e-9);near(branch(b)['n'],.9584347943)
    assert branch(b)['omega']>1 and branch(b)['core']>0

@pytest.mark.parametrize('n',[.96,.97,1,1.2,1.5,2,4,8])
def test_two_branches_same_workload(n):
    g1=brentq(lambda g:branch(g)['n']-n,.33,.8268273875)
    g2=brentq(lambda g:branch(g)['n']-n,.8268273876,1.999)
    a,b=branch(g1),branch(g2)
    near(a['n'],b['n']);assert a['growth_sq']>0>b['growth_sq'];assert a['omega']<b['omega'];assert a['core']<b['core']

@pytest.mark.parametrize('g',[.85,1,1.25,1.5,1.75,1.95])
def test_clock_is_not_universal_scaling(g):
    d=branch(g);e=eigh(R@(A+g*C)@Ri,eigvals_only=True);e0=eigh(R@M@Ri,eigvals_only=True)
    if g!=1:
        # A universal lapse would multiply both transition gaps by the same factor.
        assert abs((e[2]-e[1])/(e0[2]-e0[1])-(e[2]-e[0])/(e0[2]-e0[0]))>1e-4
    # A common energy offset changes phase rate, but not currents, projective motion or gaps.
    delta=.7;K=H0+g*V;p=d['p'];a=expm(-1j*K*.4)@p;b=expm(-1j*(K+delta*np.eye(33))*.4)@p
    near(b,np.exp(-1j*delta*.4)*a);near(abs(a),abs(b))

@pytest.mark.parametrize('g',[.5,.8,.85,1,1.5,1.9])
def test_frozen_reciprocity_and_no_horizon(g):
    K=H0+g*V;U=expm(-1j*K*.27)
    near(U,U.T);near(U.conj().T@U,np.eye(33));assert np.linalg.norm(U[24:28,28:32])>1e-3

@pytest.mark.parametrize('g',[.7,.9,1,1.5,1.9])
def test_full_trajectory_conservation(g):
    d=branch(g);p=d['p'].copy();rng=np.random.default_rng(74);delta=rng.normal(size=33)+1j*rng.normal(size=33);p+=.001*delta;p*=np.sqrt(d['n'])/np.linalg.norm(p)
    sol=solve_ivp(lambda t,y:rhs(y),[0,2],p,method='DOP853',rtol=1e-10,atol=1e-12,t_eval=np.linspace(0,2,31))
    assert sol.success;near(np.sum(abs(sol.y)**2,axis=0),d['n'],atol=1e-8);near([energy(y) for y in sol.y.T],energy(p),atol=1e-8)

@pytest.mark.parametrize('g',[.9,1,1.2,1.5,1.8,1.95])
def test_stable_branch_frequency_core_and_energy_increase(g):
    a=branch(g);b=branch(g+.001);assert b['n']>a['n'];assert b['omega']>a['omega'];assert b['core']>a['core'];assert b['energy']>a['energy']

def test_hidden_load_counterexample_same_core_clock():
    # Common H0,V dark-to-core modes of the actual weighted graph, outer symmetric zero row/column.
    q=np.zeros(33);arr=np.array([[0,1,-1,0],[1,0,0,-1],[-1,0,0,1],[0,-1,1,0]])
    for (s,i,j),k in outer.items():q[k]=arr[i,j]
    q/=np.linalg.norm(q);near(H0@q,q);near(V@q,-.5*q);near(B.conj().T@q,0)
    # Can add two opposite parity modes with opposite overlap, equal norm; total gain unchanged.
    r=q.copy();r[12:24]*=-1;near(H0@r,r);near(V@r,.5*r);near(np.vdot(q,r),0)
    p=branch(1)['p'];extra=.4;z=p+np.sqrt(extra/2)*(q+r)
    near(np.vdot(z,z).real,1+extra);near(np.vdot(z,V@z).real/2,CHI);near(energy(z)-energy(p),extra)
    near(B.conj().T@rhs(z),B.conj().T@rhs(p));near(core_moment(z,1),core_moment(p,1))
    # Independent phases evolve, overlap and energy of the hidden pair stay constant.
    for time in [.1,1,3]:
        zz=p*np.exp(-1.1j*time)+np.sqrt(extra/2)*(q*np.exp(-.5j*time)+r*np.exp(-1.5j*time))
        near(np.vdot(zz,V@zz).real/2,CHI);near(energy(zz),energy(z));near(core_moment(zz,1),core_moment(p,1))

@pytest.mark.parametrize('g',[1.9,1.99,1.999,1.9999])
def test_saturation_does_not_create_finite_upper_capacity(g):
    d=branch(g);lim=branch(1.999999)
    near(d['n']*(2-g),CHI*g/d['h']);assert d['omega']<lim['omega'];assert d['core']<.1
    assert d['growth_sq']<0
    assert d['n']>1

def test_dark_loading_with_arbitrary_relative_phase():
    q=np.zeros(33);arr=np.array([[0,1,-1,0],[1,0,0,-1],[-1,0,0,1],[0,-1,1,0]])
    for (s,i,j),k in outer.items():q[k]=arr[i,j]
    q/=np.linalg.norm(q);r=q.copy();r[12:24]*=-1
    p=branch(1)['p'];a=np.sqrt(.3)*np.exp(.7j);b=np.sqrt(.3)*np.exp(-.4j)
    sol=solve_ivp(lambda t,y:rhs(y),[0,3],p+a*q+b*r,method='DOP853',rtol=1e-11,atol=1e-12,t_eval=np.linspace(0,3,21))
    assert sol.success
    for t,y in zip(sol.t,sol.y.T):
        near(y,p*np.exp(-1.1j*t)+a*q*np.exp(-.5j*t)+b*r*np.exp(-1.5j*t),atol=2e-9)
        near(core_moment(y,1),core_moment(p,1));near(energy(y),energy(p)+.6)
