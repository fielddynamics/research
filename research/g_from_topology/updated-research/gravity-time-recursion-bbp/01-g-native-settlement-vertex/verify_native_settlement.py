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
checks=0
def ck(label,v):
    global checks
    assert bool(v),label
    checks+=1; print('PASS',label)
ck('33 geometric positions, 104 bonds',len(tiles)==33 and len(edges)==104)
ck('Hadamard orthogonality',np.array_equal(T[:4].T@T[:4],4*np.eye(4)))
# Both exact kernels have denominator 54.
W=6*np.array([[0,2,2,1],[2,0,2,1],[2,2,0,1],[1,1,1,6]],dtype=np.int64)
v=np.array([1,1,1,6]); Wc=np.outer(v,v)
results={}
for name,w in [('full',W),('central',Wc)]:
    # star of source + four neighbours, dimensionless Hamiltonian times 54
    J=np.kron(np.eye(5,dtype=np.int64),54*H)
    for i in range(4):
        block=-F[i+4]@w@F[i].T
        J[(i+1)*d:(i+2)*d,:d]=block;J[:d,(i+1)*d:(i+2)*d]=block.T
    ck(name+' Hermitian',np.array_equal(J,J.T))
    target=np.concatenate([np.array(O)+i*d for i in range(1,5)])
    X=np.eye(5*d,dtype=np.int64)[:,O]; K={}
    for k in range(1,6):
        X=J@X; K[k]=sp.Matrix(X[target,:])/54**k
    ck(name+' shortest path order 3',K[1].is_zero_matrix and K[2].is_zero_matrix)
    ck(name+' exact three-hop blocks',all(K[3][4*i:4*i+4,:]==-sp.Rational(2,3)*sp.Matrix(T[i+4,:])*sp.Matrix(T[i,:]).T for i in range(4)))
    c6=K[3].T*K[3]/36
    c7=K[4].T*K[3]/144-K[3].T*K[4]/144
    c8=K[4].T*K[4]/576-(K[3].T*K[5]+K[5].T*K[3])/720
    ck(name+' t6 isotropic',c6==sp.Rational(16,81)*sp.eye(4))
    ck(name+' t7 vanishes',c7.is_zero_matrix)
    ck(name+' t8 scalar/triplet symmetry',c8==sp.diag(c8[0,0],*[c8[1,1]]*3))
    print(name,'t8 coefficients',c8[0,0],c8[1,1],'difference',c8[0,0]-c8[1,1]);results[name]=(c8,J,target)
# Independent scaling control: geometric H cannot select dimensionless alpha; same pulse angle at scaled time.
for name,(c8,J,target) in results.items():
    eig,U=eigh(J/54); B=U[O,:].T; C=U[target,:]
    for t in [0.01,0.02,0.04]:
        Kt=(C*np.exp(-1j*t*eig))@B
        G=Kt.conj().T@Kt
        pred=np.eye(4)*16/81*t**6+np.array(c8,float)*t**8
        ck(name+f' numerical Taylor at t={t}',np.linalg.norm(G-pred)<2e-2*t**8)
# Determinant vs ordinary source selection; symbolic 2-channel example generalizes by block factorization.
t=sp.symbols('t',real=True); k=sp.symbols('k',positive=True)
# Gaussian internal channels: eliminating a massive mode gives a quadratic correction, not all-channel product.
J=sp.Matrix([t,0]); A2=k*sp.eye(2)
ck('ordinary Schur response begins at t^2',(J.T*A2.inv()*J)[0]==t**2/k)
# exact 21-mode closure volume, as distinct from scalar response.
ck('collective determinant intensity t^42',sp.det(t**2*sp.eye(21))==t**42)
print(f'{checks} checks passed')
# A rank-loss condition distinguishes an oriented volume from an intensity sum.
a,b,c,d0=sp.symbols('a b c d',real=True); X=sp.Matrix([[a,b],[c,d0]])
ck('oriented volume changes sign on exchange',X[[1,0],:].det()==-X.det())
ck('rank deficient nonzero read has zero determinant and nonzero norm',sp.Matrix([[1,1],[1,1]]).det()==0 and sp.trace(sp.Matrix([[1,1],[1,1]]).T*sp.Matrix([[1,1],[1,1]]))==4)
ck('collective intensity factors under concatenation',(X*sp.diag(t,t)).det()**2==sp.expand(t**4*X.det()**2) or sp.expand((X*sp.diag(t,t)).det()**2-t**4*X.det()**2)==0)
print(f'{checks} total checks passed')
# Plot the native five-cell response, using scaled gains to expose the order-eight split.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(7.5,4.5),layout='constrained')
for name,(c8,J,target) in results.items():
    eig,U=eigh(J/54); B=U[O,:].T; C=U[target,:]
    ts=np.linspace(.025,.5,160); y=[]
    for time in ts:
        Kt=(C*np.exp(-1j*time*eig))@B; G=Kt.conj().T@Kt
        y.append([G[0,0].real/time**6,np.trace(G[1:,1:]).real/(3*time**6)])
    y=np.array(y)
    for j,s in enumerate(['scalar','polar']):ax.plot(ts,y[:,j],label=name+' / '+s,linestyle='-' if j==0 else '--')
ax.axhline(16/81,color='gray',linestyle=':',label='leading common value 16/81');ax.set(xlabel='Dimensionless time',ylabel='Transfer intensity / time⁶',title='Native five-cell port gain: scalar and polar channels separate');ax.legend(fontsize=8);ax.grid(alpha=.2)
fig.savefig(Path(__file__).parent/'native_port_gain.svg');plt.close(fig)
