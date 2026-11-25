"""FCC packing of whole GFD cells. Exact finite checks; no physical selection law implied."""
from itertools import product, combinations, permutations
from math import gcd
from collections import deque, Counter
import json
from pathlib import Path
import numpy as np

D=sorted(d for d in product((-1,0,1), repeat=3) if sum(x*x for x in d)==2)
S=sorted(s for s in product((-1,1), repeat=3) if np.prod(s)==1)
L=4
V=sorted(v for v in product(range(L), repeat=3) if sum(v)%2==0)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def wrap(v):return tuple(x%L for x in v)
def delta(v,w):return tuple((b-a+L//2)%L-L//2 for a,b in zip(v,w))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det(a,b,c):return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def rank3(ds):return any(det(*q)!=0 for q in combinations(ds,3))
def port(d):
    a=[i for i,s in enumerate(S) if dot(s,d)==2];assert len(a)==1;return a[0]
def base(v):
    a=[(1,1,0),(1,-1,0),(-1,0,1),(-1,0,-1)]
    return a if v[0]%2==0 else [neg(d) for d in a]
def edges():return {tuple(sorted((v,wrap(add(v,d))))) for v in V for d in base(v)}
REM={((0,0,0),(1,1,0)),((0,1,1),(1,0,1))}
ADD={((0,0,0),(0,1,1)),((1,0,1),(1,1,0))}
def neighbors(v,E):return sorted(delta(v,b if a==v else a) for a,b in E if v in (a,b))
def components(E):
    rest=set(V);out=[]
    while rest:
        root=min(rest);rest.remove(root);q=[root];c=[root]
        while q:
            v=q.pop()
            for d in neighbors(v,E):
                w=wrap(add(v,d))
                if w in rest:rest.remove(w);q.append(w);c.append(w)
        out.append(c)
    return out

def translation_index(E):
    # Tree lifts to Z^3; residual edge displacements generate deck-translation subgroup.
    root=V[0];p={root:root};q=deque([root]);cycles=set()
    while q:
        v=q.popleft()
        for d in neighbors(v,E):
            w=wrap(add(v,d));target=add(p[v],d)
            if w not in p:p[w]=target;q.append(w)
            else:
                diff=add(target,neg(p[w]));assert all(a%L==0 for a in diff)
                if any(diff):cycles.add(tuple(a//L for a in diff))
    index=0
    for c in combinations(cycles,3):index=gcd(index,abs(det(*c)))
    return len(p),index,sorted(cycles)

def verify():
    n=0
    def check(cond,label):
        nonlocal n
        assert cond,label;n+=1
    check(len(D)==12,'12 FCC contacts')
    check(all(dot(d,d)==2 for d in D),'equal distance')
    check(len(S)==4 and all(dot(a,b)==-1 for a,b in combinations(S,2)),'regular tetrahedron')
    check(all(3*dot(a,b)!=-2 for a,b in combinations(D,2)),'no exact tetrahedral angle')
    candidates=[]
    for ds in combinations(D,4):
        if tuple(map(sum,zip(*ds)))==(0,0,0) and rank3(ds):candidates.append(ds)
    check(len(candidates)==6,'six balanced nonplanar quartets')
    check(all(len({port(d) for d in ds})==4 for ds in candidates),'one per Hadamard port')
    # Every balanced candidate has the same anisotropy spectrum, exact via diagonal tensor.
    for ds in candidates:
        a=np.array(ds,dtype=int);m=a.T@a
        check(np.array_equal(m,np.diag(np.diag(m))) and sorted(m.diagonal())==[2,2,4],'moment eigenvalues')
    # Proper tetrahedral rotation group: even sign flips and even permutations.
    orbit=set()
    for p in permutations(range(3)):
        if sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2:continue
        for s in S:orbit.add(tuple(s[i]*D[0][p[i]] for i in range(3)))
    check(orbit==set(D),'Td proper subgroup transitive on contacts')
    E=edges();C=E-REM|ADD
    check(REM<=E and not ADD&E,'valid two-edge reconnection')
    for name,e in [('balanced',E),('connected',C)]:
        check(len(e)==64,name+' 64 active links')
        for v in V:
            ds=neighbors(v,e)
            check(len(ds)==4 and set(ds)<=set(D),name+' four of twelve')
            check(len(set(D)-set(ds))==8,name+' eight inactive')
            check(rank3(ds),name+' nonplanar')
            check(len({port(d) for d in ds})==4,name+' one contact per port')
            check(all(neg(d) in neighbors(wrap(add(v,d)),e) for d in ds),name+' reciprocal')
        cs=components(e)
        b=[v for v in V if tuple(map(sum,zip(*neighbors(v,e))))!=(0,0,0)]
        check(len(b)==(0 if name=='balanced' else 4),name+' imbalance sites')
        check(sorted(map(len,cs))==([16,16] if name=='balanced' else [32]),name+' components')
        reached,index,cycles=translation_index(e)
        check(index==1,name+' full period translation subgroup in reached component')
        # Uniform reciprocal hopping: finite-torus current/occupation continuity.
        a=np.zeros((len(V),len(V)));vi={v:i for i,v in enumerate(V)}
        for v,w in e:a[vi[v],vi[w]]=a[vi[w],vi[v]]=1
        h=-a;z=np.exp(1j*np.arange(len(V))*.37)*(1+np.arange(len(V))*.01)
        dz=-1j*h@z;dN=2*np.real(z.conj()*dz);j=2*np.imag(z.conj()[:,None]*h*z[None,:]);
        check(np.max(abs(j+j.T))<1e-12,name+' reciprocal currents')
        check(np.max(abs(dN-j.sum(axis=1)))<1e-12,name+' local conservation')
        check(abs(dN.sum())<1e-12,name+' total conservation')
        print(f'{name}: {len(V)} sites, {len(e)} active bonds, components {[len(c) for c in cs]}, imbalance sites {b}, lift translation index {index}')
    print(f'{n}/{n} checks passed. No physical selector or regular face-to-face FCC tiling derived.')
    data={'directions':D,'ports':S,'balanced':{','.join(map(str,v)):neighbors(v,E) for v in V},'connected':{','.join(map(str,v)):neighbors(v,C) for v in V}}
    Path(__file__).with_name('four_port_data.json').write_text(json.dumps(data))
if __name__=='__main__':verify()
