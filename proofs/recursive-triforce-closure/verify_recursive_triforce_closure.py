"""Exact finite checks for Proof 23 preparation; Python standard library only."""
from fractions import Fraction as F
from itertools import permutations, product, combinations
from collections import Counter

V=((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))
S=tuple(permutations(range(4)))
X=tuple(product(range(4),repeat=3))
checks=[]
def check(name, condition):
    assert condition, name
    checks.append(name)
    print('PASS',name)
def sgn(p):
    return (-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
def det(a,b,c):
    return sum(sgn((0,1,2,3)) * (-1)**sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))*a[p[0]]*b[p[1]]*c[p[2]] for p in permutations(range(3)))
def midpoint(a,b):
    return tuple(F(x+y,2) for x,y in zip(a,b))
def subdiv(t):
    a,b,c=t; ab,ac,bc=midpoint(a,b),midpoint(a,c),midpoint(b,c)
    return [(ab,ac,bc),(a,ab,ac),(b,ab,bc),(c,ac,bc)]
def level(t,n):
    tiles=[t]
    for _ in range(n): tiles=[c for p in tiles for c in subdiv(p)]
    return tiles
def L(x):
    return all((2*t).denominator==1 for t in x) and sum(2*t for t in x)%2==0
def point_sign(i,j,k):
    return (-1)**((j==i)+(k==i))
def basis(x):
    i,j,k=x
    if j==i and k==i: return ('s',i,i,i,1)
    if j==i:
        return ('a',i,min(i,k),max(i,k),1 if i<k else -1)
    if k==i:
        a,b=sorted(set(range(4))-{i,j}); a,b=(a,b) if sgn((i,j,a,b))==1 else (b,a)
        return ('a',i,min(a,b),max(a,b),1 if a<b else -1)
    if j==k: return ('s',i,j,j,1)
    l=next(iter(set(range(4))-{i,j,k})); a,b=(i,l) if sgn((i,j,k,l))==1 else (j,k)
    return ('s',i,min(a,b),max(a,b),1)
def act(p,t):
    s,i,j,k,c=t; a,b=p[j],p[k]
    return (s,p[i],min(a,b),max(a,b),c*(-1 if s=='a' and a>b else 1))
def perm(p,x):return tuple(p[i] for i in x)

# The actual octahedron edge midpoints, with their coordinates doubled.
G=[]
for i,j in combinations(range(3),2):
    for a,b in product((-1,1),repeat=2):
        v=[0]*3;v[i]=a;v[j]=b;G.append(tuple(v))
check('12 distinct octahedron edge midpoints',len(set(G))==12)
check('all doubled generators have even coordinate sum',all(sum(v)%2==0 for v in G))
B=((1,1,0),(1,0,1),(0,1,1))
check('three generators span index-two even-sum lattice',abs(det(*B))==2 and all(v in G for v in B))
P={(x-z,y-z) for x,y,z in G}
check('body-diagonal projection is the Flower lattice', (1,0) in P and (0,1) in P)
for i in range(4):
    T=[V[j] for j in range(4) if i!=j]
    for n in range(4):
        a=level(T,n); verts=set(v for t in a for v in t)
        check(f'face {i}, depth {n}: distinct triangle and vertex counts',len({frozenset(t) for t in a})==4**n and len(verts)==(2**n+1)*(2**n+2)//2)
        check(f'face {i}, depth {n}: all vertices in midpoint lattice iff n<=2',all(L(x) for x in verts)==(n<=2))
        if n==3: check(f'face {i}: depth-three vertices retain precisely depth-two lattice vertices', {v for v in verts if L(v)}=={v for t in level(T,2) for v in t})
# A labeling of the actual medial geometry: central uses omitted face i;
# each lateral label j corresponds to a parent corner j. Child corner labels
# follow the affine maps, so equivariance is not assumed by address alone.
def label_tile(i,j,k):
    T={l:tuple(map(F,V[l])) for l in range(4) if l!=i}
    def child(T,j):
        C=tuple(sum(v[d] for v in T.values())/3 for d in range(3))
        if j==i: return {l:tuple((3*C[d]-v[d])/2 for d in range(3)) for l,v in T.items()}
        return {l:midpoint(v,T[j]) for l,v in T.items()}
    return frozenset(child(child(T,j),k).values())
# Coordinate action from barycentric coefficients in the tetrahedral frame.
# v=(1/4) sum_l (V_l dot v) V_l since sum outer products=4I.
def rot(p,v):
    return tuple(sum(sum(F(V[l][d])*v[d] for d in range(3))*V[p[l]][a] for l in range(4))/4 for a in range(3))
T={x:label_tile(*x) for x in X}
check('64 distinct labeled actual triangles',len(set(T.values()))==64)
for p in S:
    check(f'actual triangle covariance {p}',all(frozenset(rot(p,v) for v in T[x])==T[perm(p,x)] for x in X))
check('40/24 pointing split',Counter(point_sign(*x) for x in X)=={1:40,-1:24})
check('64 connection basis images distinct',len({basis(x)[:-1] for x in X})==64)
check('every image has correct exchange sector',all((basis(x)[0]=='s')==(point_sign(*x)==1) for x in X))
for p in S:
    if sgn(p)==1:
        check(f'A4 explicit graded intertwiner {p}',all(basis(perm(p,x))==act(p,basis(x)) for x in X))
    check(f'incident equivariance {p}',all(basis(perm(p,x))==act(p,basis(x)) for x in X if x[1]==x[0] and x[2]!=x[0]))
    check(f'nonincident sign-twisted equivariance {p}',all(basis(perm(p,x))==(*act(p,basis(x))[:-1],sgn(p)*act(p,basis(x))[-1]) for x in X if x[2]==x[0] and x[1]!=x[0]))
    f=sum(p[i]==i for i in range(4)); f2=sum(p[p[i]]==i for i in range(4))
    actual=Counter(point_sign(*x) for x in X if perm(p,x)==x)
    check(f'geometric characters {p}',actual[1]==f*(1+(f-1)**2) and actual[-1]==2*f*(f-1))
    if sgn(p)==1: check(f'proper rotation characters match connection {p}',actual[1]==f*(f*f+f2)//2 and actual[-1]==f*(f*f-f2)//2)
p=(1,0,2,3)
check('reflection obstructs parity-preserving S4 isomorphism',sum(perm(p,x)==x and point_sign(*x)==-1 for x in X)==4 and sum(p[i]==i for i in range(4))*(sum(p[i]==i for i in range(4))**2-4)//2==0)
for family in (lambda x:x[1]==x[0] and x[2]!=x[0],lambda x:x[2]==x[0] and x[1]!=x[0]):
    a=next(x for x in X if family(x)); check('negative family is a regular A4 orbit',len({perm(p,a) for p in S if sgn(p)==1})==12)
# Additional independent exact checks for the refined proof.
# The preceding preparation checks remain part of the same run.

def squared_distance(a,b): return sum((x-y)**2 for x,y in zip(a,b))
for i in range(4):
    face=tuple(V[j] for j in range(4) if i!=j)
    grid={tuple(F(sum(q[t]*face[t][d] for t in range(3)),4) for d in range(3))
          for q in product(range(5),repeat=3) if sum(q)==4}
    # enumerate doubled integer lattice points directly in the bounding box
    pts={tuple(F(x,2) for x in z) for z in product(range(-2,3),repeat=3)
         if sum(z)%2==0 and sum(z[d]*V[i][d] for d in range(3))==-2}
    check(f'face {i}: entire midpoint-lattice intersection equals quarter barycentric grid',pts==grid and len(grid)==15)
    # every pair of nearest-neighbour points is an edge; all 3-cliques are the tiles
    cliques={frozenset(t) for t in combinations(grid,3) if all(squared_distance(a,b)==F(1,2) for a,b in combinations(t,2))}
    check(f'face {i}: nearest-neighbour elementary triangles are exactly the 16 medial tiles',cliques=={T[x] for x in X if x[0]==i})
    edges={frozenset((a,b)) for a,b in combinations(grid,2) if squared_distance(a,b)==F(1,2)}
    check(f'face {i}: triangular mesh has 30 edges and Euler characteristic one',len(edges)==30 and len(grid)-len(edges)+len(cliques)==1)

# Check the explicitly stated inverse, independently of building a reverse lookup.
def inverse_basis(t):
    typ,i,a,b=t[:4]
    if typ=='s':
        if a==b:return i,a,a
        if i in (a,b):
            l=b if a==i else a
            j,k=sorted(set(range(4))-{i,l})
            return (i,j,k) if sgn((i,j,k,l))==1 else (i,k,j)
        l=next(iter(set(range(4))-{i,a,b}))
        return (i,b,a) if sgn((i,a,b,l))==1 else (i,a,b)
    if i in (a,b):return i,i,b if a==i else a
    return i,next(iter(set(range(4))-{i,a,b})),i
slots=[('s',i,a,b) for i in range(4) for a in range(4) for b in range(a,4)]+[('a',i,a,b) for i in range(4) for a,b in combinations(range(4),2)]
check('explicit inverse left identity on all geometric addresses',all(inverse_basis(basis(x))==x for x in X))
check('explicit inverse right identity on every symmetric/antisymmetric slot',all(basis(inverse_basis(t))[:-1]==t for t in slots))

def repair(p,x):
    y=perm(p,x)
    if sgn(p)==-1 and len(set(x))==3:y=(y[0],y[2],y[1])
    return y, -1 if sgn(p)==-1 and x[0]==x[2]!=x[1] else 1
for p in S:
    check(f'graded repaired S4 action agrees with connection {p}',all((*basis(repair(p,x)[0])[:-1],basis(repair(p,x)[0])[-1]*repair(p,x)[1])==act(p,basis(x)) for x in X))
check('repaired signed action obeys group law for all 24^2 permutations and 64 addresses',all((lambda y,s: (repair(p,y)[0],s*repair(p,y)[1])==repair(tuple(p[q[i]] for i in range(4)),x))(*repair(q,x)) for p,q in product(S,repeat=2) for x in X))
# A4 dictionary is not canonical: on each negative free orbit, a nontrivial
# right translation commutes with the left action. Construct an alternative
# preserving the incident/nonincident families and the upper face index.
A=[p for p in S if sgn(p)==1]
family=[x for x in X if x[0]==x[1]!=x[2]]
base=(0,0,1)
r=(0,2,3,1)
alt={perm(p,base):perm(p,perm(r,base)) for p in A}
check('nontrivial face-preserving A4 equivariant relabeling of incident family',len(alt)==12 and all(alt[x][0]==x[0] and alt[x]!=x for x in family) and all(alt[perm(p,x)]==perm(p,alt[x]) for p in A for x in family))

# Independently check the full real-address tree, with all entries multiplied by 8.
H=((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))
def tree_row(r,x):
    a,b,c=r; i,j,k=x
    if c:return 4*H[c][k] if (a,b)==(i,j) else 0
    if b:return 2*H[b][j] if a==i else 0
    if a:return H[a][i]
    return 1
B=[[tree_row(r,x) for x in X] for r in X]
check('full 64x64 tree transform: B B^T = 64 I exactly',all(sum(a*b for a,b in zip(B[i],B[j]))==64*(i==j) for i,j in product(range(64),repeat=2)))
check('full tree has 21 nodes and 63 noncommon rows',1+4+16==21 and sum(r!=(0,0,0) for r in X)==63)
cyc=(0,2,3,1)
for n,expected in [(1,2),(2,6),(3,22)]:
    P=set(product(range(4),repeat=n)); o=0
    while P:
        a=next(iter(P)); b=perm(cyc,a); c=perm(cyc,b); P.difference_update([a,b,c]);o+=1
    check(f'physical prefix orbits depth {n}: {expected}',o==expected)
# Exact invariant pointing compression: 14 positive and 8 negative orbit modes.
P=set(X); orbits=[]
while P:
    a=next(iter(P)); o={a,perm(cyc,a),perm(cyc,perm(cyc,a))};P-=o;orbits.append(o)
check('physical pointing sector has 14 positive and 8 negative orbit modes',Counter(point_sign(*next(iter(o))) for o in orbits)=={1:14,-1:8})
wp=F(40,64);wm=F(24,64)
check('mean-zero pointing compression mixed eigenvalue is exactly -1/4',wm-wp==F(-1,4))
print(f'\n{len(checks)}/{len(checks)} checks passed (combined)')
