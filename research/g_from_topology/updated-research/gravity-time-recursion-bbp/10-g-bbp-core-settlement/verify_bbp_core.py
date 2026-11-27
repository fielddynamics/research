import sympy as s
import mpmath as m
x,e=s.symbols('x e', real=True)
checks=[]
def check(name, value):
    assert bool(value), name
    checks.append(name)
    print('PASS',name)
def eq(name,a,b): check(name,s.simplify(a-b)==0)
f=(4-2*x**3-x**4-x**5)/(1-x**8/16)
f0=16*(x-1)/((x*x-2)*(x*x-2*x+2))
R=(2-x*x)/(x*x-2*x+2)
theta=s.pi+4*s.atan(x-1)
L=2*s.log(R)
S=theta+L
eq('reduced BBP integrand',f,f0)
eq('phase plus logarithm derivative',s.diff(S,x),f0)
eq('initial read',S.subs(x,0),0)
eq('closure read',S.subs(x,1),s.pi)
eq('phase slope',s.diff(theta,x).subs(x,1),4)
eq('log slope',s.diff(L,x).subs(x,1),-4)
eq('stationarity',s.diff(S,x).subs(x,1),0)
eq('phase curvature',s.diff(theta,x,2).subs(x,1),0)
eq('log curvature',s.diff(L,x,2).subs(x,1),-16)
eq('total curvature',s.diff(S,x,2).subs(x,1),-16)
eq('third derivative',s.diff(S,x,3).subs(x,1),-64)
eq('log lapse candidate slope',s.diff(s.log(R),x).subs(x,1),-2)
eq('log lapse candidate curvature',s.diff(s.log(R),x,2).subs(x,1),-8)
# Complex factor whose log modulus and argument give the two real pieces.
Z=(2-x*x)/(1+s.I*(x-1))**2
eq('complex modulus squared',Z*s.conjugate(Z),R**2)
eq('complex closure',Z.subs(x,1),1)
eq('complex closure slope',s.diff(Z,x).subs(x,1),-2-2*s.I)
for n in range(1,6):
    a=s.Rational(1,3)**n
    eq(f'level {n} curvature pullback',s.diff(S.subs(x,1+a*e),e,2).subs(e,0),-16*a*a)
m.mp.dps=80
for n in range(1,7):
    delta=m.mpf(3)**(-n-4)
    read=lambda x:m.pi+4*m.atan(x-1)+2*m.log((2-x*x)/(x*x-2*x+2))
    ratio=(m.pi-read(1+delta/3))/(m.pi-read(1+delta))
    check(f'level {n} error ratio approaches 1/9',abs(ratio-m.mpf(1)/9)<delta)
print(f'{len(checks)} checks passed')
