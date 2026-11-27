from fractions import Fraction as F
import numpy as np
import pytest
from model import *

def test_exact_area():
    a=2*(F(1)+F(6)+sum(F(11,7)*(2-F(j,7)) for j in range(1,8)))
    assert a==F(318,7) and area()==pytest.approx(float(a))

def test_exact_moments():
    e=[F(0),F(1),F(4)]+[F(4)+F(11*j,7) for j in range(1,8)]
    w=[F(1),F(2)]+[2-F(j,7) for j in range(1,8)]
    ref=[sum(2*h*(b-a) for a,b,h in zip(e,e[1:],w)),sum(h*(b*b-a*a) for a,b,h in zip(e,e[1:],w)),sum(2*h*(b**3-a**3)/3 for a,b,h in zip(e,e[1:],w)),sum(2*h**3*(b-a)/3 for a,b,h in zip(e,e[1:],w))]
    np.testing.assert_allclose(moments(),np.array(ref,float),rtol=1e-13)

@pytest.mark.parametrize('j',range(1,8))
def test_course_width(j):
    assert half_width(4+(j-.5)*11/7)==pytest.approx(2-j/7)

@pytest.mark.parametrize('r',[1,2,3,4])
def test_aligned_area(r):
    _,_,mask,_,_,d=grid('stepped',r)
    assert 2*mask.sum()*d*d==pytest.approx(area())

@pytest.mark.parametrize('shape',['stepped','smooth','equal_area','envelope'])
def test_control_integral(shape):
    from scipy.integrate import quad
    val=quad(lambda y: 2*half_width(y,shape),0,15,points=[1,4,*list(4+np.arange(1,7)*11/7)],epsabs=1e-9)[0]
    assert val==pytest.approx(area(shape),rel=1e-9)

def test_endpoint_separation():
    assert VIRTUAL_RUN!=L
    assert VIRTUAL_RUN/.0254-H_PYRAMID/.0254*(1-1/np.sqrt(2))==pytest.approx(-2.8500318666,abs=.01)

def test_scale_law():
    for scale in [.1,1,10]:
        assert (H_PYRAMID*scale*(1-1/np.sqrt(2)))/(H_PYRAMID*scale)==pytest.approx(ZSTAR/H_PYRAMID)
        assert C/(2*(WMAX*scale))==pytest.approx(odd_bound()/scale)
