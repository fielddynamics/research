from itertools import combinations
import numpy as np
import sympy as sp
from scipy.linalg import eigh
from pathlib import Path
# Geometry and local H reconstructed from verify_coupled_origins.py (Stage IX).
A=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)])
S=np.vstack((A,-A)); tiles=[('O',frozenset([(0,0,0)]))]
for tag,T in [('A',A),('B',-A)]:
    for f in combinations(range(4),3):
        tri=T[list(f)]; mid=lambda a,b:tuple((a+b)//2)
        tiles.append(('C'+tag,frozenset(mid(tri[i],tri[j]) for i,j in combinations(range(3),2))))
        for i in range(3): tiles.append(('E'+tag,frozenset([tuple(tri[i])]+[mid(tri[i],tri[j]) for j in range(3) if j!=i])))
pos=np.array([np.mean(list(v),axis=0) for _,v in tiles]); outer=[i for i,(k,_) in enumerate(tiles) if k[0]=='E']; inner=[i for i,(k,_) in enumerate(tiles) if k[0]=='C']
edges=[(i,j) for i,j in combinations(range(1,33),2) if len(tiles[i][1]&tiles[j][1])==2]+[(0,i) for i in inner]
idx={}; base=[]
for f,s in enumerate(S):
    ids=[i for i in outer if tuple(s) in tiles[i][1]]
    base.append(next(i for i in inner if np.allclose(pos[i],s/3)))
    for i in ids:
        t=next(g for g in range(4*(f//4),4*(f//4)+4) if g!=f and tuple((s+S[g])//2) not in tiles[i][1]);idx[f,t]=i
O=[0,33,34,35]; d=36; T=np.column_stack([np.ones(8,dtype=int),S]); H=np.zeros((d,d),dtype=np.int64)
for i,j in edges:
    if i!=0:H[i,j]=H[j,i]=-1
H[np.ix_(base,O)]=-T;H[np.ix_(O,base)]=-T.T
F=[np.eye(d,dtype=np.int64)[:,[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if i!=j]+[base[i]]] for i in range(8)]
