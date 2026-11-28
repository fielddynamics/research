import numpy as np
import sympy as s
import pytest
from energy_read import *

@pytest.fixture(scope='module')
def obs(): return exact_observability()

def test_exact_rank(obs):
 f,full,d=obs; assert f.rank()==26 and full.rank()==36 and d.shape==(36,10)
def test_dark_spectrum(obs):
 f,full,d=obs; Hs=s.Matrix(H); assert Hs*(Hs-2*s.eye(36))*d==s.zeros(36,10); assert (Hs*d).rank()==5 and ((Hs-2*s.eye(36))*d).rank()==5
 assert d[base,:]==s.zeros(8,10)
def test_equal_norm_counterexample(obs):
 _,_,d=obs; Hs=s.Matrix(H); a=(Hs-2*s.eye(36))*d; b=Hs*d
 a=next(a[:,j] for j in range(10) if a[:,j]!=s.zeros(36,1)); b=next(b[:,j] for j in range(10) if b[:,j]!=s.zeros(36,1))
 assert (a.T*Hs*a)[0]==0 and (b.T*Hs*b)[0]==2*(b.T*b)[0]
 assert s.Matrix(C)*a==s.zeros(8,1) and s.Matrix(C)*b==s.zeros(8,1)
@pytest.mark.parametrize('seed',range(12))
def test_full_energy(seed):
 rng=np.random.default_rng(seed); v=rng.normal(size=36)+1j*rng.normal(size=36); R=history(np.vstack([f.T for f in F[:4]]),2).astype(float); dec=np.linalg.pinv(R); y=R@v
 assert np.allclose(dec@y,v,atol=1e-10)
 assert np.allclose(np.vdot(y,dec.T@H@dec@y),np.vdot(v,H@v),atol=1e-8)
@pytest.mark.parametrize('seed',range(16))
def test_ledger(seed):
 rng=np.random.default_rng(seed); a=rng.normal(size=36)+1j*rng.normal(size=36); b=rng.normal(size=(4,36))+1j*rng.normal(size=(4,36)); e=port_ledger(a,b); face,ch,leaf=prefix_energies(e)
 assert e.shape==(4,4,4) and np.allclose(face.sum(),ch.sum()) and np.allclose(ch.sum(),leaf.sum())
 assert np.allclose(e.sum(),sum(bond(a,b[i],i)[0] for i in range(4))/2)
 v=e.ravel(); w=FW@v; assert np.allclose(w[0],v.sum()/8) and np.allclose(FW@w,v)
 assert np.allclose(port_ledger(a*np.exp(1j*.37),b*np.exp(1j*.37)),e)
@pytest.mark.parametrize('seed',range(16))
def test_phase_current(seed):
 rng=np.random.default_rng(seed); a=rng.normal(size=36)+1j*rng.normal(size=36); b=rng.normal(size=36)+1j*rng.normal(size=36); i=seed%4; en,j=bond(a,b,i); z=np.vdot(F[i].T@a,W@(F[i+4].T@b)); e0,j0=bond(a,b*np.exp(-1j*np.angle(z)),i)
 assert abs(j0)<1e-10 and np.allclose(e0,-2*abs(z))
 d=(bond(a,b*np.exp(1j*1e-5),i)[0]-bond(a,b*np.exp(-1j*1e-5),i)[0])/2e-5
 assert np.allclose(d,j,rtol=1e-8,atol=1e-8)
@pytest.mark.parametrize('phase',np.linspace(0,2*np.pi,9))
def test_circular_ports(phase):
 z=np.array([1,1j,0])*np.exp(1j*phase)/np.sqrt(2); q=A@z
 for i in range(4):
  E=np.array([[q[i],q[j],0] for j in range(4) if i!=j]+[[0,0,q[i]]]); assert np.allclose(E.conj().T@E,Gn); assert np.allclose(np.linalg.solve(4*Gn,E.conj().T@W@E),Tn/4)
def test_exact_amplitude():
 from native_throat import r
 P=L+h/(2*n)*CM*x*x.T*G*CM
 assert P.det()==s.Rational(413,50)
 assert (r*P.inv()*x)[0]==1
 assert (x.T*G*T*x)[0]/n==-s.Rational(46,231)
 assert (x.T*G*P.inv()*x)[0]/n==s.Rational(102694,170569)
@pytest.mark.parametrize('J',[.001,.01,.05,.1,.2])
@pytest.mark.parametrize('direction',[[1,0,0],[1,1,0],[1,1,1]])
def test_phase_instability(J,direction):
 d=np.array(direction)/np.linalg.norm(direction); k=.01*d; coeff=phase_coefficient(J); e=growth(J,k)
 assert coeff>0 and np.max(abs(e.imag))<1e-8 and np.max(e.real)>0
 assert np.isclose(np.max(e.real)/.01**2,coeff,rtol=2e-4)
 assert np.isclose(static_read(J,k),static_read(J,np.zeros(3)),rtol=2e-4)

def test_general_curvature():
 from native_throat import r,hc
 q=s.symbols('q',positive=True); P=L+q/(2*n)*CM*x*x.T*G*CM
 assert s.factor(P.det())==3481*q/2200
 assert s.factor((r*P.inv()*x)[0])==308/(59*q)
 assert P.subs(q,hc).det()!=0
@pytest.mark.parametrize('seed',range(8))
def test_lapse_energy(seed):
 # Half-bond allocation on a pair gives total energy under uniform lapse.
 rng=np.random.default_rng(seed); a=rng.normal(size=36)+1j*rng.normal(size=36); b=rng.normal(size=36)+1j*rng.normal(size=36)
 ea=np.vdot(a,H@a).real; eb=np.vdot(b,H@b).real; edge,_=bond(a,b,seed%4)
 def E(na,nb): return na*ea+nb*eb+(na+nb)*edge/2
 eps=1e-5
 assert np.allclose((E(1+eps,1)-E(1-eps,1))/(2*eps),ea+edge/2)
 assert np.allclose(E(2,2),2*E(1,1))
