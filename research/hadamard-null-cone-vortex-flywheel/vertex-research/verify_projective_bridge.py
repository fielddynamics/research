import itertools as it
from collections import Counter
import numpy as np
import sympy as sp
from fractions import Fraction
n=0
def check(label, value):
    global n
    assert bool(value), label
    n+=1; print('PASS',label)
# F4 polynomial w^2+w+1; F64 = F4[b]/(b^3+b+1).
def m4(a,b):
    p=0
    while b:
        if b&1:p^=a
        b>>=1; a<<=1
        if a&4:a^=7
    return p

def digs(a):return [(a>>(2*i))&3 for i in range(3)]
def pack(a):return sum(x<<(2*i) for i,x in enumerate(a))
def m64(a,b):
    p=[0]*5
    for i,x in enumerate(digs(a)):
        for j,y in enumerate(digs(b)):p[i+j]^=m4(x,y)
    for j in [4,3]:p[j-3]^=p[j];p[j-2]^=p[j]
    return pack(p[:3])
def sc(a,b):return m64(a,b)
def project(a):
    d=digs(a); pivot=max(i for i,v in enumerate(d) if v)
    inv=next(x for x in range(1,4) if m4(x,d[pivot])==1)
    return sc(a,inv)
points=sorted({project(a) for a in range(1,64)})
grade=lambda a:max(i for i,v in enumerate(digs(a)) if v)
check('F64 multiplication: nonzero inverses',all(any(m64(a,b)==1 for b in range(1,64)) for a in range(1,64)))
check('21 projective classes, 1/4/16',Counter(map(grade,points))=={0:1,1:4,2:16})
# Walsh filter using integer H, simultaneous field multiplication by w.
H=np.array([[(-1)**((a&b).bit_count()%2) for b in range(64)] for a in range(64)],dtype=np.int64)
check('H^2=64 I',np.array_equal(H@H,64*np.eye(64,dtype=int)))
rot=np.array([sc(a,2) for a in range(64)])
check('scalar rotation order 3, only zero fixed',np.array_equal(rot[rot[rot]],np.arange(64)) and sum(rot==np.arange(64))==1)
Q3=np.eye(64,dtype=int)+np.eye(64,dtype=int)[rot]+np.eye(64,dtype=int)[rot[rot]]
check('Walsh intertwines orbit average',np.array_equal(H@Q3,Q3@H))
cols=[]
for a in points:
    o=[sc(a,j) for j in (1,2,3)]
    col=H[:,o].sum(axis=1);cols.append(col)
    check('plane contrast %d: +3 on 16 addresses, -1 on 48'%a,Counter(col)=={3:16,-1:48})
X=np.stack(cols,axis=1)
check('21 plane contrasts orthogonal',np.array_equal(X.T@X,192*np.eye(21,dtype=int)))
check('all plane contrasts zero mean',np.all(X.sum(axis=0)==0))
check('all plane contrasts rotation invariant',np.array_equal(X[rot],X))
# F4096 = F64[theta]/(theta^2+theta+w), w=2. F16 subfield represented by a,b in F4.
def m12(x,y):
    a,b=x;c,d=y;bd=m64(b,d)
    return m64(a,c)^m64(2,bd),m64(a,d)^m64(b,c)^bd
scalars=[(a,b) for a,b in it.product(range(4),repeat=2) if a or b]
def canon(z):return min(m12(z,s) for s in scalars)
def norm(z):
    a,b=z;return m64(a,a)^m64(a,b)^m64(2,m64(b,b))
check('quadratic extension irreducible',all((m64(a,a)^a^2)!=0 for a in range(64)))
pairs=[(u,v) for u in points for v in points if grade(u)==grade(v)]
Q=[canon(z) for z in pairs]
check('same-grade pairs give 273 distinct F16 projective points',len(Q)==len(set(Q))==273)
check('norm nonzero for every nonzero pair',all(norm((a,b))!=0 for a,b in it.product(range(64),repeat=2) if a or b))
check('norm projectively independent of F16 representative',all(project(norm(m12(z,s)))==project(norm(z)) for z in Q for s in scalars))
fibres=Counter(project(norm(z)) for z in Q)
check('21 norm fibres of 13',fibres=={p:13 for p in points})
# Baer subplane multiplicative cosets of embedded F64*/F4*.
base={canon((p,0)) for p in points}
check('embedded Baer plane has 21 points',len(base)==21)
remaining=set(Q);blocks=[]
while remaining:
    z=min(remaining); block={canon(m12(z,p)) for p in base}
    check('Baer coset size 21, disjoint',len(block)==21 and block<=remaining)
    check('each Baer coset is transversal to norm fibres',len({project(norm(p)) for p in block})==21)
    remaining-=block;blocks.append(block)
check('13 disjoint Baer planes',len(blocks)==13)
M=np.zeros((21,273),dtype=np.int64)
for i,z in enumerate(pairs):M[points.index(project(norm(z))),i]=1
v=np.array([int(a==b) for a,b in pairs],dtype=np.int64)
check('M M^T = 13 I',np.array_equal(M@M.T,13*np.eye(21,dtype=int)))
check('diagonal identity is transversal',np.array_equal(M@v,np.ones(21,dtype=int)))
check('identity vector squared norm 21',v@v==21)
# R=P quotient coisometry; P=I-vv^T/21. Exact integer scaling.
Cscaled=21*(M@M.T)-np.outer(M@v,M@v)
check('273 times compressed operator =273 I - J',np.array_equal(Cscaled,273*np.eye(21,dtype=int)-np.ones((21,21),dtype=int)))
tr=Fraction(int(np.trace(Cscaled)),273)
check('compressed trace=272/13',tr==Fraction(272,13))
check('trace normalized by 16 =17/13',tr/16==Fraction(17,13))
check('uniform mode eigenvalue 12/13',np.array_equal(Cscaled@np.ones(21,dtype=int),252*np.ones(21,dtype=int)))
# three shears with half-angle parameter p, exact rational rotation.
p=sp.symbols('p',real=True); L=lambda x:sp.Matrix([[1,0],[x,1]]);U=lambda x:L(x).T
R=U(-p)*L(2*p/(1+p*p))*U(-p)
check('alternating shears exact rotation',sp.simplify(R-sp.Matrix([[(1-p*p)/(1+p*p),-2*p/(1+p*p)],[2*p/(1+p*p),(1-p*p)/(1+p*p)]]))==sp.zeros(2))
check('one-way shears additive',L(2)*L(3)*L(4)==L(9))
print('TOTAL',n,'assertions passed')
