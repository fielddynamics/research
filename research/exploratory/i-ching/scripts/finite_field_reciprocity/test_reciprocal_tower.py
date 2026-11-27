"""Exact checks for the Frobenius/reciprocity tower. No physical coupling assumed."""
from itertools import product
from collections import Counter
import numpy as np
import pytest
from finite_geometry import plane, registers, field, mul, projective

n=273
X=range(n); edge=range(1,n)
F=lambda x:64*x%n
K=lambda x:-x%n
J=lambda x:K(F(x))
lines,baer=plane(); pencil=[l-{0} for l in lines if 0 in l]
d={x:i for i,l in enumerate(pencil) for x in l}
f={i:d[F(next(iter(l)))] for i,l in enumerate(pencil)}
e={x:(d[x],d[K(x)]) for x in edge}
fix=lambda m, xs=X:{x for x in xs if m(x)==x}
small=fix(F); kernel=fix(J); rational={i for i in f if f[i]==i}
match={tuple(sorted(e[x])) for x in kernel-{0}}

def pair(x):return (x%21,x%13)
def orb(x, maps):return frozenset(m(x) for m in maps)
id_=lambda x:x
both=(id_,F,K,J)

def assert_eq(a,b): assert a==b

def mat(m):return np.eye(n,dtype=int)[:,[m(x) for x in X]]
FM,KM,JM=map(mat,(F,K,J))
A,C,_=registers(); A=np.column_stack((np.zeros(17,dtype=int),A)); P=A.T@A/16
C=np.array([[int(x in b) for x in X] for b in baer],dtype=int); Q=C.T@C/21
M=np.diag([int(x in kernel) for x in X]); D=np.diag([int(x in small) for x in X]); V=A.T/4; Z=C.T/np.sqrt(21)
idx=sorted(kernel); T=np.eye(n)[:,idx]
recip={min(x,K(x)) for x in X}; joint={min(orb(x,both)) for x in X}
N=lambda x:65*x%n # relative field norm to GF64 projective embedded in PG(2,16)

def nr(x):return min(N(x),K(N(x)))

def close(a,b): np.testing.assert_allclose(a,b,rtol=1e-12,atol=1e-12)
CASES={
'CRT bijection':lambda:assert_eq(len({pair(x) for x in X}),273),
'Frobenius fixes first factor negates second':lambda:assert_eq({(pair(x),pair(F(x))) for x in X},{((a,b),(a,-b%13)) for a,b in product(range(21),range(13))}),
'inversion negates both':lambda:assert_eq({(pair(x),pair(K(x))) for x in X},{((a,b),(-a%21,-b%13)) for a,b in product(range(21),range(13))}),
'Frobenius is involution':lambda:assert_eq([F(F(x)) for x in X],list(X)),
'reversal is involution':lambda:assert_eq([K(K(x)) for x in X],list(X)),
'Klein action commutes':lambda:assert_eq([F(K(x)) for x in X],[K(F(x)) for x in X]),
'fixed Frobenius subplane':lambda:assert_eq(small,set(baer[0])),
'fixed inversion origin':lambda:assert_eq(fix(K),{0}),
'fixed combined norm kernel':lambda:assert_eq(kernel,{x for x in X if N(x)==0}),
'13 kernel points':lambda:assert_eq(len(kernel),13),
'kernel unique representative per Baer coset':lambda:assert_eq([len(kernel&b) for b in baer],[1]*13),
'norm image small plane':lambda:assert_eq({N(x) for x in X},small),
'norm fibers 13':lambda:assert_eq(set(Counter(N(x) for x in X).values()),{13}),
'norm squares on subplane':lambda:assert_eq([N(x) for x in sorted(small)],[2*x%n for x in sorted(small)]),
'field power agrees projective action':lambda:assert_eq([projective(field()[0][64*x%4095]) for x in X],[F(x) for x in X]),
'Frobenius preserves pencil fibers':lambda:assert_eq({(f[d[x]],d[F(x)]) for x in edge},{(i,i) for i in f}),
'five fixed pencil directions':lambda:assert_eq(len(rational),5),
'six swapped pencil pairs':lambda:assert_eq(len({tuple(sorted((i,f[i]))) for i in f if i!=f[i]}),6),
'small plane edges exactly K5':lambda:assert_eq({e[x] for x in small-{0}},{(i,j) for i,j in product(rational,repeat=2) if i!=j}),
'kernel edges exactly Frobenius conjugate pairs':lambda:assert_eq({e[x] for x in kernel-{0}},{(i,f[i]) for i in f if f[i]!=i}),
'kernel perfect matching on external directions':lambda:assert_eq(Counter(i for m in match for i in m),Counter({i:1 for i in f if i not in rational})),
'Frobenius action on directed edges':lambda:assert_eq([e[F(x)] for x in edge],[(f[e[x][0]],f[e[x][1]]) for x in edge]),
'reciprocal norm fiber sizes':lambda:assert_eq(sorted(Counter(nr(x) for x in recip).values()),[7]+[13]*10),
'joint norm fiber sizes':lambda:assert_eq(sorted(Counter(nr(x) for x in joint).values()),[7]*11),
'joint orbit product independent signs':lambda:assert_eq(len({(min(a,-a%21),min(b,-b%13)) for a,b in map(pair,X)}),77),
'joint orbit size counts':lambda:assert_eq(Counter(map(len,{orb(x,both) for x in X})),Counter({1:1,2:16,4:60})),
'Klein character multiplicities':lambda:assert_eq([int(np.trace((np.eye(n)+s*FM+t*KM+s*t*JM)/4)) for s,t in [(1,1),(1,-1),(-1,1),(-1,-1)]],[77,70,60,66]),
'Baer sampling isometry':lambda:close((np.sqrt(21)*T.T@Z)@(np.sqrt(21)*T.T@Z).T,np.eye(13)),
'kernel compressed on pencil':lambda:close(np.linalg.eigvalsh(V.T@M@V),[0]*5+[1/16]*12),
'small plane compressed on pencil':lambda:close(np.linalg.eigvalsh(V.T@D@V),[0]*12+[1/4]*5),
'kernel mask is not Baer projector':lambda:assert_eq(np.allclose(M,Q),False),
'kernel Baer overlap trace':lambda:close(np.trace(M@Q),13/21),
'common norm sample and small plane only origin':lambda:assert_eq(small&kernel,{0}),
'Baer sector constant rank':lambda:assert_eq(np.linalg.matrix_rank(Q),13),
'pencil mask different from norm rank':lambda:assert_eq(np.linalg.matrix_rank(P@M@P),12),
'Frobenius fixed reciprocal edges are K5 and matching':lambda:assert_eq({x for x in recip if min(F(x),K(F(x)))==x}, {min(x,K(x)) for x in small|kernel}),
}
@pytest.mark.parametrize('name',list(CASES),ids=list(CASES))
def test_tower(name): CASES[name]()

from itertools import combinations
from collections import defaultdict
vertices=set(range(1,8)); states=set(product(range(8),repeat=2))
triangles={frozenset((a,b,a^b)) for a,b in combinations(vertices,2)}
R=lambda x:(x[1],x[0]^x[1]); S=lambda x:x[::-1]
G=lambda x:frozenset((x,R(x),R(R(x)),S(x),R(S(x)),R(R(S(x)))))
triorb={G(x) for x in states}; k8={frozenset(x) for x in combinations(range(8),2)}
star={frozenset((0,a)) for a in vertices}; tedges=[{frozenset(x) for x in combinations(t,2)} for t in triangles]
inc=np.array([[int(a in t) for t in sorted(triangles,key=lambda t:tuple(sorted(t)))] for a in sorted(vertices)])
FANO={
'Fano seven lines':lambda:assert_eq(len(triangles),7),
'Fano unique line on each distinct nonzero pair':lambda:assert_eq(Counter(p for ts in tedges for p in ts),Counter({p:1 for p in k8-star})),
'K8 star plus seven triangles':lambda:assert_eq(star|set.union(*tedges),k8),
'28 edges':lambda:assert_eq(len(k8),28),
'Fano incidence rows three':lambda:assert_eq(list(inc.sum(1)),[3]*7),
'Fano incidence design':lambda:close(inc@inc.T,2*np.eye(7)+np.ones((7,7))),
'S3 orbit sizes':lambda:assert_eq(Counter(map(len,triorb)),Counter({1:1,3:7,6:7})),
'rank one orbit unordered star':lambda:assert_eq({frozenset(x) for o in triorb if len(o)==3 for x in o if x[0]!=x[1]},star),
'rank two orbit unordered Fano triangles':lambda:assert_eq({frozenset(frozenset(x) for x in o) for o in triorb if len(o)==6},{frozenset(es) for es in tedges}),
'XOR difference perfect matchings':lambda:assert_eq(Counter(a^b for a,b in combinations(range(8),2)),Counter({a:4 for a in vertices})),
'one star and three triangle edges per difference':lambda:assert_eq(Counter(a^b for a,b in combinations(vertices,2)),Counter({a:3 for a in vertices})),
'each difference appears in exactly three Fano triangles':lambda:assert_eq({a:sum(a in t for t in triangles) for a in vertices},{a:3 for a in vertices}),
}
@pytest.mark.parametrize('name',list(FANO),ids=list(FANO))
def test_fano(name): FANO[name]()
