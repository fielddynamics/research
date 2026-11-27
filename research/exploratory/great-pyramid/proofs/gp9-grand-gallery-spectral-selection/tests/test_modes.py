import numpy as np
import pytest
from scipy.sparse.csgraph import connected_components
from model import *

@pytest.mark.parametrize('r',[1,2,3,4])
def test_graph_and_null_mode(r):
    x,y,mask,K,D,d=grid('stepped',r)
    assert connected_components(K,directed=False)[0]==1
    assert (K-K.T).nnz==0
    np.testing.assert_allclose(K@np.ones(K.shape[0]),0,atol=1e-10)
    assert D.diagonal().min()==0 and np.count_nonzero(D.diagonal())==len(y)

@pytest.mark.parametrize('parity',['even','odd'])
@pytest.mark.parametrize('r',[1,2,3])
def test_eigen_residual_and_orthogonality(parity,r):
    _,_,_,K,D,d=grid('stepped',r); A=K if parity=='even' else K+D
    ev,V=modes('stepped',r,parity)
    assert np.linalg.norm(A@V-V*ev,ord=2)<1e-7
    np.testing.assert_allclose(V.T@V,np.eye(len(ev)),atol=1e-9)
    assert np.all(np.diff(ev)>=0) and ev[0]>=0
    if parity=='even': assert ev[0]==0
    else: assert ev[0]>0

@pytest.mark.parametrize('parity',['even','odd'])
@pytest.mark.parametrize('r',[1,2,3])
def test_rectangular_independent_analytic_benchmark(parity,r):
    _,_,_,_,_,d=grid('envelope',r)
    nx=28*r;ny=105*r
    inds=range(0,12,2) if parity=='even' else range(1,12,2)
    exact=sorted(4/d**2*(np.sin(i*np.pi/(2*nx))**2+np.sin(j*np.pi/(2*ny))**2) for i in inds for j in range(12))[:8]
    np.testing.assert_allclose(modes('envelope',r,parity)[0],exact,atol=1e-8,rtol=1e-9)

@pytest.mark.parametrize('r',[1,2,3,4])
def test_discrete_rayleigh_bounds(r):
    x,y,mask,K,D,d=grid('stepped',r)
    xx=np.broadcast_to(x,mask.shape)[mask]; yy=np.broadcast_to(y[:,None],mask.shape)[mask]; yy=yy-yy.mean()
    e=modes('stepped',r,'even')[0][1];o=modes('stepped',r,'odd')[0][0]
    assert e<=yy@(K@yy)/(yy@yy)+1e-10
    assert o<=xx@((K+D)@xx)/(xx@xx)+1e-10
    # discrete rectangular mixed 1D lower bound; no continuum convergence assumption
    lower=4/d**2*np.sin(np.pi/(2*28*r))**2
    assert o>=lower-1e-9

@pytest.mark.parametrize('parity',['even','odd'])
def test_refinement_stability(parity):
    v3=cutoff(modes('stepped',3,parity)[0]);v4=cutoff(modes('stepped',4,parity)[0])
    assert np.max(np.abs(v4[:5]-v3[:5]))<.15

@pytest.mark.parametrize('shape',['stepped','smooth','equal_area','envelope'])
def test_controls_constant_mode(shape):
    ev,v=modes(shape,2,'even'); assert ev[0]==0
    assert abs(v[:,0].sum())/np.sqrt(len(v))==pytest.approx(1,abs=1e-9)

def test_central_aperture_by_explicit_reflection():
    x,y,mask,K,D,d=grid('stepped',2)
    q=((x[None,:]<1)&(y[:,None]<2))[mask].astype(float)
    ev,v=modes('stepped',2,'odd')
    full=np.vstack([v,-v])/np.sqrt(2);src=np.r_[q,q]/np.sqrt(2*q@q)
    np.testing.assert_allclose(full.T@src,0,atol=1e-14)
    a=aperture_overlap('stepped',2,'even');assert np.sum(a*a)<=1+1e-12
    assert abs(a[0])>0

def test_even_vertical_trial():
    A,Y,Y2,X2=moments(); bound=cutoff(A/(Y2-Y*Y/A))
    assert bound<30 and cutoff(modes('stepped',4,'even')[0][1])<bound

@pytest.mark.parametrize('f',[16.3787,29.3449,32.7575])
def test_king_axial_fundamentals_below_odd(f):
    k=axial_k(f,odd_bound());assert k.imag>0 and k.real==0

def test_bragg_is_multimode():
    fb=C/(2*1.67); ev=cutoff(modes('stepped',4,'even')[0]);od=cutoff(modes('stepped',4,'odd')[0]);
    assert (ev<fb).sum()>=5 and (od<fb).sum()>=1
