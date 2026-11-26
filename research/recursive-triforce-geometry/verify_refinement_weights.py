"""Compute actual solid-angle weights for medial subdivisions on a regular tetrahedron.
Exact rational vertex coordinates; solid angles evaluated in floating point.
No choice of optical kernel, physical read, or Hamiltonian is implied.
"""
from fractions import Fraction as F
from math import atan2, sqrt, pi, isclose
from itertools import product

def midpoint(a,b): return tuple((x+y)/2 for x,y in zip(a,b))
def sub(t):
    a,b,c=t; ab,ac,bc=midpoint(a,b),midpoint(a,c),midpoint(b,c)
    return [(ab,ac,bc),(a,ab,ac),(b,ab,bc),(c,ac,bc)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def omega(t):
    a,b,c=t; A,B,C=(sqrt(dot(v,v)) for v in t)
    return 2*atan2(abs(det(a,b,c)), A*B*C+dot(a,b)*C+dot(b,c)*A+dot(c,a)*B)
verts=[tuple(map(F,v)) for v in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]]
faces=[tuple(v for j,v in enumerate(verts) if j!=i) for i in range(4)]
weights=[]; checks=0
def check(name,cond):
    global checks
    assert cond,name; checks+=1; print('PASS',name)
for i,face in enumerate(faces):
    parents=sub(face); rows=[[omega(t)/(4*pi) for t in sub(p)] for p in parents]; weights.extend(w for r in rows for w in r)
    check(f'face {i} total equals quarter',isclose(sum(map(sum,rows)),.25,abs_tol=1e-14))
    for j,p in enumerate(parents):
        check(f'face {i} parent {j} child flux sums to parent',isclose(sum(rows[j]),omega(p)/(4*pi),abs_tol=1e-14))
    check(f'face {i} central children not equally weighted',not isclose(rows[0][0],rows[0][1],abs_tol=1e-14))
    check(f'face {i} lateral children not equally weighted',all(max(r)-min(r)>1e-4 for r in rows[1:]))
    if i==0:
        print('Face 0 weights as fractions of full-surface flux; rows = parent, cols = child')
        for r in rows: print(' '.join(f'{w:.12f}' for w in r))
        check('central parent is one eighth',isclose(sum(rows[0]),1/8,abs_tol=1e-14))
        check('lateral parents each one twenty-fourth',all(isclose(sum(r),1/24,abs_tol=1e-14) for r in rows[1:]))
check('64 positive weights normalize to one',len(weights)==64 and min(weights)>0 and isclose(sum(weights),1,abs_tol=1e-14))
# Physical rotation acts on actual 3D faces and triangles; address-free comparison.
def rotate(v): return (v[2],v[0],v[1])
def key(t): return tuple(sorted(t))
tiles={key(t):omega(t)/(4*pi) for face in faces for parent in sub(face) for t in sub(parent)}
check('64 distinct actual triangles on one tetrahedron',len(tiles)==64)
check('physical rotation permutes all triangles',all(key(tuple(map(rotate,t))) in tiles for t in tiles))
check('one fixed refined tile under physical rotation',sum(t==key(tuple(map(rotate,t))) for t in tiles)==1)
check('radial quadrature invariant under physical rotation',all(isclose(w,tiles[key(tuple(map(rotate,t)))],abs_tol=1e-14) for t,w in tiles.items()))
print(f'{checks}/{checks} checks passed')
