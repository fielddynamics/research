"""Exact rational verification of the second threefold read (not a physical action)."""
from itertools import product
import sympy as s
import pytest
from test_shared_zone import O, H, idx, J21, zones, R, B
I=s.eye(22)
# Value basis, not normalized orbit basis. Gram weights (1,3,...,3).
W=s.Matrix([[sum(int(H[idx[o[0]],idx[y]]) for y in p) for p in O] for o in O])/8
J=s.diag(1,s.Matrix(J21)); G=s.diag(1,*([3]*21)); z=s.Symbol('z')

def pair(u, sign=0):
    U=zones(u)[3]; Q=s.diag(*[int(set(o)<=U) for o in O])
    P=Q if not sign else Q+(I-Q)*(I+sign*J)/2
    return P,W*P*W

def cp(A): return A.charpoly(z).as_expr()

def test_weighted_metric():
    assert W.T*G==G*W and W**2==I and J**2==I and W*J==J*W

@pytest.mark.parametrize('u',[1,2,4,7])
@pytest.mark.parametrize('sign,r,c,m,zero',[(0,14,8,6,8),(1,18,16,2,4),(-1,18,14,4,4)])
def test_odd_axis_spectrum(u,sign,r,c,m,zero):
    P,V=pair(u,sign)
    assert s.trace(P)==r and P*P==P and V*V==V
    assert s.expand(cp(P*V*P)-z**zero*(z-1)**c*(z-s.Rational(1,4))**m)==0

@pytest.mark.parametrize('u',[1,2,4,7])
@pytest.mark.parametrize('sign,core,m,dark',[(0,8,6,2),(1,16,2,2),(-1,14,4,0)])
def test_odd_axis_rotation(u,sign,core,m,dark):
    P,V=pair(u,sign); C=(2*P-I)*(2*V-I)
    assert C**3==I and C!=I
    assert C.T*G*C==G
    assert s.expand(cp(C)-(z-1)**(core+dark)*(z*z+z+1)**m)==0
    F=(P+C*P*C**2+C**2*P*C)/3
    assert s.expand(cp(F)-(z-1)**core*(z-s.Rational(1,2))**(2*m)*z**dark)==0

@pytest.mark.parametrize('u',[3,5,6])
@pytest.mark.parametrize('sign',[0,1])
def test_even_axis_counterexample(u,sign):
    P,V=pair(u,sign); C=(2*P-I)*(2*V-I)
    assert C**3!=I and C**4==I

@pytest.mark.parametrize('u',[1,2,4,7])
def test_orientation_discriminator(u):
    Q,_=pair(u); Pp,_=pair(u,1); Pm,_=pair(u,-1)
    assert [( (I-P)*W*P).rank() for P in [Q,Pp,Pm]]==[6,2,4]
    assert [s.Matrix.hstack(P,W*P).rank() for P in [Q,Pp,Pm]]==[20,20,22]
    dark=s.Matrix.vstack(Q,Q*W).nullspace()
    assert len(dark)==2 and all(J*v==-v and Pp*v==s.zeros(22,1) and Pm*v==v for v in dark)

@pytest.mark.parametrize('u',[1,2,4,7])
def test_small_exterior_block(u):
    E=[e for e in range(1,8) if (e&u).bit_count()%2==0]; e,f=E[:2]
    reps=[(a^(u*i),b^(u*j)) for a,b in [(e,f),(f,e)] for i,j in product(range(2),repeat=2)]
    D=s.Matrix([[sum((-1)**B(x,y1) for y1 in [y,R(y),R(R(y))]) for y in reps] for x in reps])
    A=s.diag(0,4,4,4)-s.ones(4); e0=s.eye(4)[:,0]; ones=s.ones(4,1)
    B0=4*(e0*ones.T+ones*e0.T-e0*e0.T)-s.ones(4)
    if (e&f).bit_count()%2 == 0:
        A,B0=B0,A
        expected=(z-1)*(z+1)*(z-s.Rational(1,2))**3*(z+s.Rational(1,2))**3
    else:
        expected=(z-1)*(z+1)*(z-s.Rational(1,2))**5*(z+s.Rational(1,2))
    assert D==s.BlockMatrix([[A,B0],[B0,A]]).as_explicit()
    assert s.expand(cp(D/8)-expected)==0

def test_zero_not_preserved():
    e0=I[:,0]; assert W*e0!=e0 and (W*e0)[0]==s.Rational(1,8)

@pytest.mark.parametrize('u',[1,2,4,7])
@pytest.mark.parametrize('sign,core,m',[(0,8,6),(1,16,2),(-1,14,4)])
def test_three_read_return(u,sign,core,m):
    P,V=pair(u,sign); C=(2*P-I)*(2*V-I)
    P1=C*P*C**2; P2=C**2*P*C
    D=P*P1*P2*P
    assert s.expand(cp(D)-z**(22-core-m)*(z-1)**core*(z+s.Rational(1,8))**m)==0
    if sign==1:
        Q,_=pair(u); E=(I+J)/2
        # Unique minimal subspace containing Q whose exchange-even part is W-invariant.
        L=s.Matrix.hstack(Q,W*Q*E)
        assert L.rank()==18 and P*L==L
