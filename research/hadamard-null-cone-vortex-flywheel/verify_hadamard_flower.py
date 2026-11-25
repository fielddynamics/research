"""Exact geometry, rational overlap areas, and a conditional conservative interface."""
from itertools import product, combinations
from fractions import Fraction as F
from collections import Counter
import sympy as sp
import numpy as np
from scipy.linalg import expm

ncheck=0
def check(c,msg):
    global ncheck
    assert c,msg
    ncheck+=1
    print(f'PASS {ncheck:03d} {msg}')
S=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
C=list(product((-1,1),repeat=3)); E=[tuple(s if j==i else 0 for j in range(3)) for i in range(3) for s in (-1,1)]
O=(0,0,0); v=sp.Matrix; P=sp.eye(3)-sp.ones(3)/3
pr=lambda x:tuple(P*v(x))
H=sp.Matrix([[1,*s] for s in S]); check(H*H.T==4*sp.eye(4),'Hadamard orthogonality')
check(P*P==P and P.T==P,'orthogonal body-diagonal projection')
check(len(set(map(pr,C+E+[O])))==13,'13 distinct projected positions from 15 spatial points')
check({x for x in C+E+[O] if pr(x)==O}=={S[0],tuple(-i for i in S[0]),O},'three axial points coalesce')
for e in E:
    check(sum(t*t for t in pr(e))==sp.Rational(2,3),'inner ring radius squared 2/3')
    check(tuple(2*t for t in pr(e)) in set(map(pr,C)),'outer ring aligned at double radius')
for s in C:
    check(sum(t*t for t in pr(s)) in [0,sp.Rational(8,3)],'cube projection outer radius or centre')
# FCC A and diamond B in integer cube units. Enumerate exact finite shells.
def sublattice(p):
    if all(t%2==0 for t in p) and sum(p)%4==0:return 0
    if all(t%2==1 for t in p) and sum(p)%4==3:return 1
    return None
L=[p for p in product(range(-4,5),repeat=3) if sublattice(p) is not None]
D=[tuple(a-b for a,b in zip(s,t)) for s in S for t in S if s!=t]
check(len(set(D))==12,'12 non-backtracking two-step vectors')
check(set(D)=={p for p in L if sum(t*t for t in p)==8},'two-step shell exactly FCC')
check({p for p in L if sum(t*t for t in p)==3}==set(S),'four nearest origins exactly tetrahedral')
check(Counter(sum(t*t for t in p) for p in L if 0<sum(t*t for t in p)<12)=={3:4,8:12,11:12},'28 overlapping equal envelopes (4+12+12)')
for p in L:
    if max(map(abs,p))>2:continue
    for s in S:
        q=tuple(a+(1 if sublattice(p)==0 else -1)*b for a,b in zip(p,s))
        check(sublattice(q)==1-sublattice(p) and sum((a-b)**2 for a,b in zip(p,q))==3,'reciprocal exact tetrahedral edge')
# A-basis determinant 16, generates all FCC A via explicit inverse; B=S[0]+A.
B=sp.Matrix.hstack(*(v(S[0])-v(s) for s in S[1:]));check(abs(B.det())==16,'FCC primitive translation determinant')
for p in L:
    a=v(p)-(v(S[0]) if sublattice(p)==1 else sp.zeros(3,1))
    check(all(x.q==1 for x in B.inv()*a),'integer FCC coordinates; connected by two-step generators')
# The actual stellated solids sit within their cubes. At a shared cube edge
# (two fixed coordinates ±1), each tetrahedron meets that edge only at its parity corner.
for d in D:
    pts=set(C)&{tuple(a+b for a,b in zip(c,d)) for c in C}
    check(len(pts)==2 and sum(t*t for t in tuple(a-b for a,b in zip(*pts)))==4,'second-neighbour solid contact at two cube-edge endpoints')
    check({np.prod(p) for p in pts}=={-1,1},'shared edge joins opposite parities')
for p in C:
    check(sum(p in {tuple(a+b for a,b in zip(c,d)) for c in C} for d in D)==3,'three second neighbours incident at each cube corner')
# Exact Voronoi cell: enumerate intersections of all triples of 16 candidate planes.
N=S+D; rhs=[sp.Rational(sum(i*i for i in n),2) for n in N]
V=set()
for ix in combinations(range(16),3):
    A=sp.Matrix([N[i] for i in ix]);
    if A.det()==0:continue
    x=A.inv()*v([rhs[i] for i in ix]);
    if all(v(n).dot(x)<=b for n,b in zip(N,rhs)): V.add(tuple(x))
check(len(V)==16,'Voronoi candidate has 16 vertices')
check(max(sum(t*t for t in p) for p in V)==3,'Voronoi cell contained in sphere R=sqrt(3)')
for p in L:
    d2=sum(t*t for t in p)
    if not 0<d2<=12:continue
    m=max(v(p).dot(v(x)) for x in V); equal=[x for x in V if v(p).dot(v(x))==sp.Rational(d2,2)]
    check(m<=sp.Rational(d2,2),'all nearby diamond halfspaces satisfied')
    rank=sp.Matrix([list(v(x)-v(equal[0])) for x in equal]).rank() if equal else -1
    check((d2,len(equal),rank) in [(3,6,2),(8,3,2),(11,1,0)],'facet or point incidence classified')
# Beyond 2R, inequalities strict by Cauchy-Schwarz. Integer lattice search above covers <=2R.
# Exact Triforce clipping in barycentric (u,v) coordinates, area ratios invariant.
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def signed(poly):return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1]))/2 if poly else F(0)
def ccw(poly):return poly if signed(poly)>=0 else poly[::-1]
def area(poly):return abs(signed(poly))
def clip(poly,other):
    for a,b in zip(other,other[1:]+other[:1]):
        out=[]
        for p,q in zip(poly,poly[1:]+poly[:1]):
            cp,cq=cross(a,b,p),cross(a,b,q)
            if cp>=0:out.append(p)
            if (cp<0<cq) or (cq<0<cp):
                t=cp/(cp-cq);out.append(tuple(x+t*(y-x) for x,y in zip(p,q)))
        poly=out
        if not poly:break
    return poly
T=[(F(1),F(0)),(F(0),F(1)),(F(0),F(0))]; U=[(F(2,3)-x,F(2,3)-y) for x,y in T]
def tiles(T):
    m=[tuple((x+y)/2 for x,y in zip(T[(i+1)%3],T[(i+2)%3])) for i in range(3)]
    return [ccw([T[i],m[(i+1)%3],m[(i+2)%3]]) for i in range(3)]+[ccw(m)]
TA,TB=tiles(T),tiles(U); W=sp.Matrix([[sp.Rational(area(clip(a,b))/area(TA[0])) for b in TB] for a in TA]);
check(W==sp.Matrix([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9,'exact rational 4x4 Triforce overlap matrix')
check(W==W.T,'reciprocal area kernel')
check(W.rank()==4,'all four subchannels retained in overlap map')
check(W.eigenvals()=={sp.Rational(-2,9):2,sp.Rational(1,3):1,sp.Rational(7,9):1},'exact overlap spectrum')
check(sum(W)/4==sp.Rational(2,3),'shared hexagon covers 2/3 of each triangle')
check(W*sp.ones(4,1)==v([sp.Rational(5,9)]*3+[1]),'outer tiles partially shared, central tile fully shared')
# Full 3D cross-section coordinates from the actual tetrahedra, along +++ link.
A=[tuple(sp.Rational(5,8)*s+sp.Rational(3,8)*t for s,t in zip(S[0],q)) for q in S[1:]]
check(set(A)==set((sp.Rational(1),sp.Rational(1,4),sp.Rational(1,4)) if i==0 else (sp.Rational(1,4),sp.Rational(1),sp.Rational(1,4)) if i==1 else (sp.Rational(1,4),sp.Rational(1,4),sp.Rational(1)) for i in range(3)),'midplane cross sections derived from tetrahedron edges')
hexv=[tuple(sp.Rational(1,4)+sp.Rational(3,4)*q for q in (u,vv,1-u-vv)) for u,vv in clip(ccw(T),ccw(U))]
check(set(hexv)==set(__import__('itertools').permutations([sp.Rational(1,4),sp.Rational(1,2),sp.Rational(3,4)])),'actual shared hexagon vertices')
# Conditional amplitude dynamics using the area kernel; not a derivation of gravity.
M=np.array(W,float); HH=np.block([[np.zeros((4,4)),-M],[-M,np.zeros((4,4))]])
rng=np.random.default_rng(42)
for i in range(12):
    z=rng.normal(size=8)+1j*rng.normal(size=8); z/=np.linalg.norm(z)
    dz=-1j*HH@z; rate=2*np.real(np.conj(z)*dz); J=2*np.imag(np.conj(z[4:])[:,None]*(-M.T)*z[:4][None,:]);
    check(abs(rate[:4].sum()+J.sum())<1e-12 and abs(rate[4:].sum()-J.sum())<1e-12,'interface current reciprocal')
    zz=expm(-1j*HH*(i+1)/3)@z
    check(abs(np.linalg.norm(zz)-1)<1e-12 and abs(np.vdot(zz,HH@zz)-np.vdot(z,HH@z))<1e-12,'conditional unitary occupation/energy conservation')
print(f'\n{ncheck}/{ncheck} checks passed. Historical suites not rerun.')
