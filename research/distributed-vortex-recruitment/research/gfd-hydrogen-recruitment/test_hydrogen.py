import numpy as np
import pytest
from scipy.sparse.linalg import spsolve
from scipy.integrate import quad
from hydrogen import *
from native_cell import H,O,S,F,C

HS=[.65,.5,.35,.25]
@pytest.fixture(scope='session')
def grids():return {h:ground(h) for h in HS}

@pytest.mark.parametrize('h',HS)
@pytest.mark.parametrize('check',['adjacency','source','poisson','probability','eigen','energy','mean','positive','fixed','tetra'])
def test_fixed_lattice(grids,h,check):
 d=grids[h]; L=d['L'];p=d['p']; r=d['r'];i=d['i']; prob=d['psi']**2
 if check=='adjacency':assert (L-L.T).nnz==0 and np.allclose(L.diagonal(),2/h**2)
 elif check=='source':assert np.count_nonzero(d['source'])==1 and np.isclose(d['source'].sum()*d['vol'],4*np.pi)
 elif check=='poisson':assert np.linalg.norm(L@d['phi']-d['source']-d['b'])<1e-8
 elif check=='probability':assert np.isclose(prob.sum(),1) and np.isclose(np.sum(d['pg']**2),1)
 elif check=='eigen':assert max(d['res'],d['rg'])<1e-8
 elif check=='energy':assert d['E']<0 and d['Eg']<0
 elif check=='mean':assert 0<d['mean']<2 and 0<d['mg']<2
 elif check=='positive':assert d['psi'].min()>0 and d['phi'].min()>0
 elif check=='fixed':assert np.allclose(p/h,np.rint(p/h)) and np.count_nonzero(d['source'])==1
 else:
  v=p[L[i].indices]; v=v[np.linalg.norm(v,axis=1)>0];assert len(v)==4 and np.allclose(v.T@v,4*h*h*np.eye(3)) and np.allclose(v.sum(0),0)

@pytest.mark.parametrize('key,ref',[('E',-.5),('Eg',-.5),('mean',1.5),('mg',1.5)])
def test_convergence(grids,key,ref):
 e=[abs(grids[h][key]-ref) for h in HS];assert np.all(np.diff(e)<0)

@pytest.mark.parametrize('l,j,n',[(0,0,1),(0,1,2),(0,2,3),(1,0,2),(1,1,3),(2,0,3)])
def test_radial_reference(l,j,n):assert abs(radial(l)[j]+.5/n**2)<2e-5

@pytest.mark.parametrize('r',[.1,.25,.5,1,1.5,2,3,4,5,8,10])
@pytest.mark.parametrize('quantity',['charge','mass','potential'])
def test_spherical_charge_gravity(r,quantity):
 p=quad(lambda x:4*x*x*np.exp(-2*x),0,r)[0]
 if quantity=='charge':assert np.isclose(1-p,q_enc(r),atol=1e-13)
 elif quantity=='mass':assert np.isclose((1836.15267343+p)/1837.15267343,mass_fraction(r))
 else:
  v=(1-p)/r-quad(lambda x:4*x*np.exp(-2*x),r,np.inf)[0];assert np.isclose(v,phi_neutral(r),atol=1e-13)

@pytest.mark.parametrize('h',HS)
@pytest.mark.parametrize('what',['neutral','gravity','linearity','current','phase'])
def test_recruitment_reads(grids,h,what):
 d=grids[h];L=d['L'];prob=d['psi']**2;vol=d['vol'];p=d['p'];i=d['i'];delta=np.zeros(len(p));delta[i]=1
 if what in ('neutral','gravity','linearity'):
  a=4*np.pi/vol; Q=a*(delta-prob); M=a*(1836.15267343*delta+prob)/1837.15267343
  v=spsolve(L,Q);w=spsolve(L,M); boundary_weights=np.asarray(L.sum(1)).ravel()
  if what=='neutral':assert abs(Q.sum()*vol)<1e-12 and abs(boundary_weights@v*vol)<1e-10
  elif what=='gravity':assert np.isclose(M.sum()*vol,4*np.pi) and w.min()>0 and np.isclose(boundary_weights@w*vol,4*np.pi)
  else:assert np.allclose(spsolve(L,Q+M),v+w,atol=1e-10)
 else:
  co=L.tocoo();psi=d['psi']; z=psi*np.exp(1j*.4*p[:,0]);mask=co.row!=co.col
  if what=='current':assert np.allclose(np.imag(psi[co.row]*co.data*psi[co.col]),0)
  else:assert np.allclose(abs(z)**2,prob) and np.real(np.vdot(z,L@z))>np.real(np.vdot(psi,L@psi)) and np.max(abs(np.imag(z[co.row[mask]].conj()*z[co.col[mask]])))>0

@pytest.mark.parametrize('filtered,D',[(True,.10509418),(False,.12429467)])
@pytest.mark.parametrize('direction',[[1,0,0],[0,1,0],[0,0,1],[1,1,1],[1,-2,3]])
def test_native_band(filtered,D,direction):
 k=np.array(direction)*.015/np.linalg.norm(direction); e=band(k,filtered); e0=band([0,0,0],filtered)
 assert np.isclose(e,band(-k,filtered),atol=1e-12) and np.isclose((e-e0)/(.015**2),D,rtol=5e-5)

def test_native_no_physical_scale():
 assert H.shape==(36,36) and np.count_nonzero(np.triu(H,1))==128 and np.array_equal(H,H.T)
 # shift leaves eigenvectors and transition frequencies unchanged, absolute energies differ
 v=np.linalg.eigvalsh(H);w=np.linalg.eigvalsh(H+3*np.eye(36));assert np.allclose(w-v,3)

def test_neutral_reference():
 assert abs(quad(lambda r:4*r*r*np.exp(-2*r),0,np.inf)[0]-1)<1e-12
 assert np.isclose(quad(lambda r:4*r**3*np.exp(-2*r),0,np.inf)[0],1.5)

def test_no_source_no_dimple(grids):
 L=grids[.65]['L']; assert np.allclose(spsolve(L,np.zeros(L.shape[0])),0)
