"""Fresh exact checks of the latest dialogue, not a physical gravity proof."""
import sympy as s
import numpy as np
import pytest
from scipy.optimize import root
G=s.Matrix([[3,-1,0],[-1,3,0],[0,0,1]])
C=s.Matrix([[0,-s.Rational(1,2),0],[-s.Rational(1,2),0,-1],[1,-3,1]])
M=s.Matrix([[-2,s.Rational(1,2),-2],[-s.Rational(1,2),1,-1],[-5,-1,-s.Rational(89,10)]])
x=s.Matrix([s.Rational(1,3),1,-s.Rational(4,15)])
W=s.Matrix([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9
T=s.Matrix([[4,-2,1],[0,-2,0],[3,-1,6]])/9
n=(x.T*G*x)[0]; chi=s.Rational(59,308); h=1/chi; hc=s.Rational(290521,42815)
L=M-s.Rational(11,10)*s.eye(3); r=x.T*G*C/n
K=(L+h/2*C*x*r).row_join(-x).col_join((x.T*G).row_join(s.zeros(1,1)))
def test_native():
 assert M*x==s.Rational(11,10)*x
 assert (x.T*G*C*x)[0]/(2*n)==chi
 assert G*T==T.T*G
 assert T*x==s.Matrix([-s.Rational(14,135),-s.Rational(2,9),-s.Rational(8,45)])
def test_port_reduction():
 a,b,c,q0,q1,q2=s.symbols('a b c q0 q1 q2'); q=[q0,q1,q2,-q0-q1-q2]
 for i in range(4):
  js=[j for j in range(4) if i!=j]; p=s.Matrix([a*q[i]+b*q[j] for j in js]+[c*q[i]])
  d=T*s.Matrix([a,b,c]); expected=s.Matrix([d[0]*q[i]+d[1]*q[j] for j in js]+[d[2]*q[i]])
  assert s.simplify(W*p-expected)==s.zeros(4,1)
def test_exact_tangent():
 y=K.inv()*(T*x/2).col_join(s.zeros(1,1))
 assert (r*y[:3,0])[0]==-s.Rational(3639415,71166942)
 assert 2*x[2]*y[2]/n==-s.Rational(3597250,391418181)
 y=K.inv()*(-C*x).col_join(s.zeros(1,1))
 assert (r*y[:3,0])[0]==2/(hc-h)
@pytest.mark.parametrize('eps',[1e-3,1e-4,1e-5,1e-6])
def test_stationary(eps):
 gn,cn,mn,tn=map(lambda a:np.array(a,float),(G,C,M,T)); xx=np.array(x,float).ravel(); nn=float(n); ch=float(chi)
 def solve(e):
  def f(z):
   v=z[:3]; u=v@gn@cn@v/(2*nn); gain=2*u/(ch+abs(u)); return np.r_[(mn+(gain-1)*cn-e*tn/2)@v-z[3]*v,v@gn@v-nn]
  sol=root(f,np.r_[xx,1.1],tol=1e-11); assert np.linalg.norm(f(sol.x))<1e-10
  v=sol.x[:3]; return np.array([v@gn@cn@v/(2*nn),v[2]**2/nn])
 deriv=(solve(eps)-solve(-eps))/(2*eps)
 assert np.allclose(deriv,[-3639415/71166942,-3597250/391418181],rtol=2e-5,atol=1e-8)
@pytest.mark.parametrize('k',[.1,.05,.025,.0125])
def test_radial(k):
 S=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])
 def band(v):return 4-abs(np.exp(1j*S@v).sum())
 a=band(np.array([k,0,0])); b=band(np.ones(3)*k/np.sqrt(3))
 assert abs((a-b)/a-k*k/9)<k**4/20
@pytest.mark.parametrize('D,kappa,lam',[(.124,1.,.2),(.105,2.,-.4),(1.,.2,2.)])
def test_gap(D,kappa,lam):
 for k in [0.,.1,1.]:
  mat=np.array([[lam**2/kappa+D*k*k,-lam],[-lam,kappa]])
  assert np.isclose(np.linalg.det(mat),kappa*D*k*k)
  assert np.linalg.eigvalsh(mat)[0]>-1e-12
