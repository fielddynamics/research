import numpy as np
from itertools import combinations
# Reconstruct the original Stage IX H36 graph, with its directional centre.
A=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)])
S=np.vstack((A,-A)); tiles=[('O',frozenset([(0,0,0)]))]
for tag,T in [('A',A),('B',-A)]:
    for f in combinations(range(4),3):
        tri=T[list(f)]; mid=lambda a,b:tuple((a+b)//2)
        tiles.append(('C'+tag,frozenset(mid(tri[i],tri[j]) for i,j in combinations(range(3),2))))
        for i in range(3): tiles.append(('E'+tag,frozenset([tuple(tri[i])]+[mid(tri[i],tri[j]) for j in range(3) if j!=i])))
pos=np.array([np.mean(list(v),axis=0) for _,v in tiles]); inner=[i for i,(k,_) in enumerate(tiles) if k[0]=='C'];outer=[i for i,(k,_) in enumerate(tiles) if k[0]=='E']
base=[];idx={}
for f,s in enumerate(S):
    base.append(next(i for i in inner if np.allclose(pos[i],s/3)))
    for i in outer:
        if tuple(s) in tiles[i][1]:
            t=next(g for g in range(4*(f//4),4*(f//4)+4) if g!=f and tuple((s+S[g])//2) not in tiles[i][1]);idx[f,t]=i
H=np.zeros((36,36));O=[0,33,34,35]
for i,j in combinations(range(1,33),2):
    if len(tiles[i][1]&tiles[j][1])==2:H[i,j]=H[j,i]=-1
T=np.c_[np.ones(8),S]; H[np.ix_(base,O)]=-T;H[np.ix_(O,base)]=-T.T
assert np.count_nonzero(np.triu(H,1))==128
F=[np.eye(36)[:,[idx[i,j] for j in range(4*(i//4),4*(i//4)+4) if j!=i]+[base[i]]] for i in range(8)]
W=np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]])/9; Wc=np.outer([1,1,1,6],[1,1,1,6])/54
for label,Wk,expected in [('full',W,.1242946733),('central',Wc,.1050941805)]:
    blocks=np.array([F[i]@Wk@F[i+4].T for i in range(4)])
    X=-blocks.sum(axis=0);M=np.block([[H,X],[X.T,H]])
    ev,V=np.linalg.eigh(M);u=V[:,0];R=(V[:,1:]/(ev[1:]-ev[0]))@V[:,1:].T
    Ds=[]
    for j in range(3):
        X=-np.einsum('i,ijk->jk',A[:,j],blocks);Q=np.block([[np.zeros_like(H),X],[-X.T,np.zeros_like(H)]])
        X2=np.einsum('i,ijk->jk',A[:,j]**2,blocks);M2=np.block([[np.zeros_like(H),X2],[X2.T,np.zeros_like(H)]])
        Ds.append(u@M2@u/2+u@Q@R@Q@u)
    D=np.mean(Ds);assert np.allclose(Ds,expected,atol=1e-9)
    print(label,'D=',D,'a/lambda_e (E*=mc², baseline)=',np.pi*D/2)
# Swap on four-by-four face pair space, plus independent scalar.
T=np.zeros((16,16))
for i in range(4):
    for j in range(4):T[4*j+i,4*i+j]=1
B=np.zeros((17,17));B[0,0]=1;B[1:,1:]=np.eye(16)-T
C=np.zeros((17,17));C[0,0]=1;C[1:,1:]=np.eye(16)+T
assert np.trace(B)==13 and np.trace(C)==21 and np.linalg.matrix_rank(B)==7
h=np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
L=np.eye(17);L[1:,1:]=np.kron(h,h)
assert np.allclose(L.T@B@L,B)
assert np.isclose(np.mean(np.diag(L.T@B@L)),13/17)
print('locked face pair stiffness:',np.trace(B)/17,'ratio:',17/13)
# Shift the same schedule's weight toward self-pairs: stiffness is not fixed without balance.
for p in [0,.25,.5,1]:
    pred=1-16*p/17
    weights=np.array([1/17]+[16/17*(p/4 if i==j else (1-p)/12) for i in range(4) for j in range(4)])
    assert np.isclose(weights@np.diag(B),pred)
print('PASS: original graph curvatures, swap grade, Walsh invariance, collision dependence')
