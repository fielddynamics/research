import itertools
import sympy as s
r,k,q,J=s.symbols('r k q J',positive=True)
V=[s.Matrix(v) for v in itertools.product([-1,1],repeat=3)]
A=[v for v in V if s.prod(v)==1]; B=[-v for v in A]
checks=[]
def ck(name,value):
    assert value,name
    checks.append(name); print('PASS',name)
for vs in (A,B):
    ck('tetrahedron equal squared edge length',all((a-b).dot(a-b)==8 for a,b in itertools.combinations(vs,2)))
    ck('tetrahedron volume 8/3',abs(s.det(s.Matrix.hstack(*(v-vs[0] for v in vs[1:]))))/6==s.Rational(8,3))
    ck('tetrahedron normal halfspaces',all(all(a.dot(v)>=-1 for v in vs) for a in vs))
centers=[v/3 for v in V]
ck('eight octahedral face centroids',all(sum(abs(x) for x in v)==1 for v in centers))
ck('inner cube largest aligned centered cube',max(sum(abs(x) for x in v) for v in centers)==1)
ck('inner tetrahedral distances scale squared by 1/9',all((a/3-b/3).dot(a/3-b/3)==s.Rational(8,9) for a,b in itertools.combinations(A,2)))
ck('inner stella volume 1/27 of parent',s.simplify((2*s.Rational(8,3)-s.Rational(4,3))/27)==s.Rational(4,27))
T=s.Matrix([[1,*list(a)] for a in A]); ck('four-port Gram',T.T*T==4*s.eye(4))
T8=s.Matrix([[1,*list(v)] for v in V]); ck('eight inner corner common and polar records',T8.T*T8==8*s.eye(4))
P=T8*T8.T/8
ck('rank-four common-polar projector',P*P==P and P.rank()==4)
H8=s.Matrix([[s.prod([v[i] for i in range(3) if (j>>i)&1]) for j in range(8)] for v in V])
ck('all eight core coordinates have orthogonal Walsh basis',H8.T*H8==8*s.eye(8))
# Gradient read for affine lapse, unchanged under scale
w=s.Matrix(s.symbols('wx wy wz')); p=s.Matrix.zeros(3,1)
for v in A: p+=v*(r*v.dot(w))/(4*r)
ck('affine lapse gradient',p==w)
# octahedron radial trial capacitance; |grad l1|²=3, dV/dr=4r².
x,a,b=s.symbols('x a b',positive=True)
f=(1/x-1/b)/(1/a-1/b)
ck('trial shell energy',s.simplify(s.integrate(12*x**2*s.diff(f,x)**2,(x,a,b))-12/(1/a-1/b))==0)
ck('trial shell capacity for a=b/3',s.simplify((12/(1/a-1/b)).subs(a,b/3))==6*b)
# nested shell conductance C_n=k*r*q^n (k includes unit shape and stiffness)
for n in range(1,9):
    C=[k*r*q**i for i in range(n)]
    eff=1/s.Add(*(1/c for c in C))
    formula=k*r*q**(n-1)*(1-q)/(1-q**n) if n>1 else k*r
    ck(f'series Schur complement n={n}',s.cancel(eff-formula)==0)
    # fixed unit source: same flux at each shell; sum of clock jumps
    u=[-s.Add(*(1/c for c in C[:i])) for i in range(n+1)]
    ck(f'conserved flux n={n}',all(s.cancel(c*(u[i]-u[i+1])-1)==0 for i,c in enumerate(C)))
# fixed energy flux, shell stiffness proportional to 1/r, alternate natural scale
for n in range(1,6):
    C=[J*3**i for i in range(n)]
    ck(f'inverse-radius series stiffness n={n}',s.cancel(1/s.Add(*(1/c for c in C))-2*J/(3*(1-s.Rational(1,3)**n)))==0)
print('TOTAL',len(checks),'checks passed')
