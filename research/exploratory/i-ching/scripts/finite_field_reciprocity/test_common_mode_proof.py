"""Exact verification of the canonical common line and tensor proof."""
from itertools import product
import sympy as s
import pytest
from test_shared_zone_rotation import I,W,J,G,O,pair,cp,z
from test_shared_zone import zones
f=s.Matrix([3 if a==b==0 else int(a==0 or b==0 or a==b) for a,b in (o[0] for o in O)])
F=f*f.T*G/30
D=s.diag(*[int(v!=0) for v in f])
M=I-F

def test_common_mode_exact():
    assert (f.T*G*f)[0]==30 and W*f==f and J*f==f
    assert F**2==F and F.T*G==G*F and W*F==F*W==F

def test_all_axes_intersection():
    A=I
    for u in range(1,8): A=A*pair(u)[0]
    assert A==D and D.rank()==8

def test_odd_axes_intersection():
    A=I
    for u in [1,2,4,7]: A=A*pair(u)[0]
    assert A==D

def test_unique_common_line():
    assert s.Matrix.vstack(I-D,(I-D)*W).rank()==21
    assert (I-D)*W*f==s.zeros(22,1)

def test_zero_coordinate_is_not_common():
    e=I[:,0]
    assert W*e!=e and F*e!=e

@pytest.mark.parametrize('u',range(1,8))
def test_common_mode_all_axes(u):
    Q,V=pair(u);P,_=pair(u,1)
    assert Q*F==F*Q==V*F==F*V==P*F==F*P==F
    assert (Q-F).rank()==13 and (P-F).rank()==17
    assert (Q-F)**2==Q-F and (P-F)**2==P-F
    assert (P-F)*(Q-F)==Q-F
    assert M*W==W*M and M*J==J*M

@pytest.mark.parametrize('sign,r,c,m',[(0,13,7,6),(1,17,15,2),(-1,17,13,4)])
def test_reduced_spectra(sign,r,c,m):
    K,_=pair(7,sign); A=K-F; V=W*A*W
    assert A.rank()==r and c+m==r
    assert s.expand(cp(A*V*A)-z**(22-r)*(z-1)**c*(z-s.Rational(1,4))**m)==0
    # Reflection on the full space acts trivially on the removed line.
    C=(2*A-I)*(2*V-I)
    assert C**3==I and C*f==f
    R=A*(C*A*C**2)*(C**2*A*C)*A
    assert s.trace(R)==c-s.Rational(m,8)
    assert s.trace(R.T*G*R*G.inv())==c+s.Rational(m,64)

def test_tensor_compression():
    # u=111, transverse two-space alternating pairing. Order: 0, (u,v) with u,v nonzero.
    K=s.BlockMatrix([[s.ones(1),s.ones(1,9)],[s.ones(9,1),s.ones(9)-2*s.kronecker_product(s.ones(3)-s.eye(3),s.ones(3)-s.eye(3))]]).as_explicit()/4
    assert s.expand(cp(K)-(z-1)**5*(z+s.Rational(1,2))**5)==0
    # v permutation acts only on second index.
    cyc=s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    swap=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    for T in [cyc,swap]:
        A=s.diag(1,s.kronecker_product(s.eye(3),T));assert K*A==A*K
    # invariant under the three-cycle: +1 rank 3 and -1/2 rank 1.
    T=s.diag(1,s.kronecker_product(s.eye(3),cyc));E=(s.eye(10)+T+T**2)/3
    B=(2*K+s.eye(10))/3
    assert B**2==B and s.trace(B*E)==3 and s.trace((s.eye(10)-B)*E)==1

def test_actual_return_not_rank_ratio():
    Q,_=pair(7);P,_=pair(7,1)
    assert s.trace(P-F)/s.trace(Q-F)==s.Rational(17,13)
    assert (15-s.Rational(2,8))/(7-s.Rational(6,8))==s.Rational(59,25)
    assert (15+s.Rational(2,64))/(7+s.Rational(6,64))==s.Rational(481,227)
