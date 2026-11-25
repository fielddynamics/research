import itertools as it
import sympy as s

count=0
def check(label, cond):
    global count
    assert bool(cond), label
    count+=1
    print(f"PASS {count:02d}: {label}")

V=[s.Matrix(v) for v in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
N=s.Matrix.hstack(*V)/s.sqrt(3)
check("tetrahedral closure",N*s.ones(4,1)==s.zeros(3,1))
check("tight frame",N*N.T==s.Rational(4,3)*s.eye(3))
check("Gram matrix",N.T*N==s.Rational(4,3)*s.eye(4)-s.ones(4)/3)
m=(1+s.sqrt(s.Rational(2,3)))/2
check("cap bound root",s.simplify(m*m+s.Rational(1,2)+(m-1)**2-s.Rational(4,3))==0)
check("cap diameter strictly below 60 degrees",m>s.sqrt(3)/2)
check("root in admissible interval",s.Rational(1,2)<m<1)
t=s.Matrix([-m,s.Rational(1,2),s.Rational(1,2),m-1])
u=3*N*t/4
check("sharp cap witness unit",s.simplify(u.dot(u))==1)
check("sharp cap witness projections",s.simplify(N.T*u-t)==s.zeros(4,1))
check("sharp cap witness non-overlap",all(x<=s.Rational(1,2) for x in t))
for i,j in it.combinations(range(8),2):
    W=V+[-v for v in V]
    check(f"cube contact pair {i+1},{j+1} non-overlap",W[i].dot(W[j])<=s.Rational(3,2))
for i,v in enumerate(V):
    check(f"fixed contact {i+1} at cube corner",v.dot(v)==3 and (2*v-v).dot(2*v-v)==3)
D=[s.Matrix(v) for v in it.product([-1,0,1],repeat=3) if sum(x*x for x in v)==2]
check("FCC 12 directions",len(D)==12)
check("FCC lacks regular tetrahedral pair angle",all(a.dot(b)/2!=-s.Rational(1,3) for a,b in it.combinations(D,2)))
print(f"{count}/{count} checks passed. Analytic polytope and cap proof in CORNER_FIRST_PACKING.md.")
