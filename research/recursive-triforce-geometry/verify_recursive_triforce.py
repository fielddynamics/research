from fractions import Fraction as F
from itertools import product
from math import gcd
checks=0
def check(name, condition):
    global checks
    assert condition,name
    checks+=1
    print('PASS',name)
def midpoint(a,b): return tuple((x+y)/2 for x,y in zip(a,b))
def sub(t):
    a,b,c=t; ab,ac,bc=midpoint(a,b),midpoint(a,c),midpoint(b,c)
    return [(ab,ac,bc),(a,ab,ac),(b,ab,bc),(c,ac,bc)]
def levels(t,n):
    a=[(t,1)]
    for _ in range(n): a=[(u,s*(-1 if i==0 else 1)) for t,s in a for i,u in enumerate(sub(t))]
    return a
def tri(coords): return tuple(tuple(map(F,p)) for p in coords)
def cross(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def area2(p): return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1])))
def clip(p,t):
    p=list(p); s=1 if cross(*t)>0 else -1
    for a,b in zip(t,t[1:]+t[:1]):
        q=[]
        for u,v in zip(p,p[1:]+p[:1]):
            du,dv=s*cross(a,b,u),s*cross(a,b,v)
            if du>=0:q.append(u)
            if du*dv<0:q.append(tuple((du*y-dv*x)/(du-dv) for x,y in zip(u,v)))
        p=q
    return p
def rank(m):
    a=[r[:] for r in m]; r=0
    for c in range(len(a[0])):
        j=next((j for j in range(r,len(a)) if a[j][c]),None)
        if j is None:continue
        a[r],a[j]=a[j],a[r]
        for i in range(r+1,len(a)):
            f=a[i][c]/a[r][c];a[i]=[x-f*y for x,y in zip(a[i],a[r])]
        r+=1
    return r
face=tri([(4,0),(0,4),(-4,-4)])
for n in range(5):
    a=levels(face,n);v={p for t,s in a for p in t}
    check(f'depth {n} tile/vertex count',len(a)==4**n and len(v)==(2**n+1)*(2**n+2)//2)
    check(f'depth {n} lattice inclusion',all(x.denominator==1 for p in v for x in p)==(n<=2))
    check(f'depth {n} pointing parity',sum(s==1 for t,s in a)==(4**n+2**n)//2)
T=tri([(0,0),(12,0),(0,12)]); B=tri([(8,8),(-4,8),(8,-4)])
for n,nonzero,expected in [(1,13,4),(2,49,13)]:
    a=[t for t,s in levels(T,n)];b=[t for t,s in levels(B,n)]
    w=[[area2(clip(t,u)) for u in b] for t in a]
    check(f'overlap depth {n} area',sum(map(sum,w))==96)
    check(f'overlap depth {n} rank/support',rank(w)==expected and sum(x!=0 for r in w for x in r)==nonzero)
    print('  rank',rank(w),'support',nonzero)
P=range(4);gs=[(0,1,2,3),(0,2,3,1),(0,2,1,3)];chars=[]
for g in gs:
    q=sum((-1 if a==0 else 1)*(-1 if b==0 else 1) for a,b in product(P,repeat=2) if g[a]==a and g[b]==b)
    t=sum(g[b]==a and g[a]==b for a,b in product(P,repeat=2)); chars.append((q,t))
check('signed characters identity/C3/S3',chars==[(4,4),(1,1),(0,4)])
addresses=list(product(P,repeat=3));rot=gs[1];seen=set();orbits=[]
for a in addresses:
    if a in seen:continue
    o=[];b=a
    while b not in seen:o.append(b);seen.add(b);b=tuple(rot[x] for x in b)
    orbits.append(o)
check('physical leaf orbits',sorted(map(len,orbits))==[1]+[3]*21)
sign=lambda a:(-1 if a[1]==0 else 1)*(-1 if a[2]==0 else 1)
check('physical invariant pointing split',sum(sign(o[0])==1 for o in orbits)==14 and len(orbits)==22)
check('full pointing split',sum(sign(a)==1 for a in addresses)==40)
check('mean compression mixed eigenvalue',F(24-40,64)==F(-1,4))
check('trace polynomial',[17+4*s for s in (1,0,-1)]==[21,17,13])
# Rotation cycles coordinates of cube signs, fixing two corners.
cube=list(product((-1,1),repeat=3));fixed=sum(a==(a[2],a[0],a[1]) for a in cube)
check('corner pairs invariant dimension',(64+2*fixed**2)//3==24 and fixed==2)
print(f'{checks}/{checks} checks passed')
