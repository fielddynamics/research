"""Exact integer/rational checks of the pi-addressed Walsh ledger; not a physical simulation."""
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
checks=0
def check(ok,label):
    global checks
    assert ok,label
    checks+=1
    print('PASS',label)
H=np.array([[(-1)**((i&j).bit_count()) for j in range(8)] for i in range(8)],dtype=np.int64)
def fwht(x):
    x=list(x); h=1
    while h<len(x):
        for i in range(0,len(x),2*h):
            for j in range(i,i+h):
                a,b=x[j],x[j+h]; x[j],x[j+h]=a+b,a-b
        h*=2
    return np.array(x,dtype=object).reshape(-1)
check(np.array_equal(H@H,8*np.eye(8,dtype=int)),'H8 orthogonal up to scale')
H64=np.kron(H,H)
check(np.array_equal(H64@H64,64*np.eye(64,dtype=int)),'H64 = H8 tensor H8')
check(np.array_equal(H64,np.array([[(-1)**((i&j).bit_count()) for j in range(64)] for i in range(64)])),'six-bit characters')
mp.mp.dps=400
v=int(mp.pi); z=mp.pi-v; seen=set(); walk=[]; first=np.zeros((8,8),int); counts=np.zeros((8,8),int)
for n in range(1,600):
    z*=8; d=int(z); z-=d; u=v; v=(u+d)%8; walk.append((u,v,d)); counts[u,v]+=1
    if (u,v) not in seen: first[u,v]=n; seen.add((u,v))
    if len(seen)==64:break
N=len(walk)
check(N==332,'pi first covers 64 ordered pairs at fractional digit 332')
check(len(seen)==64 and np.count_nonzero(first)==64,'all pair addresses')
check(int(counts.sum())==N,'raw visit count')
check(np.array_equal(H@np.ones((8,8),int)@H,64*np.outer(np.eye(8,dtype=int)[0],np.eye(8,dtype=int)[0])),'completed binary coverage is pure DC')
check(np.count_nonzero(H@counts@H)>1,'raw count ledger not pure DC')
check(np.array_equal(counts.sum(1)-counts.sum(0),np.eye(8,dtype=int)[walk[0][0]]-np.eye(8,dtype=int)[walk[-1][1]]),'path endpoints determine marginal imbalance')
D=np.fromfunction(lambda i,j:(j-i)%8,(8,8),dtype=int)
B=H@D@H # B/64 is the Walsh coefficient table of digit kernel
check(np.array_equal(H@B@H,64*D),'digit kernel reconstructed exactly')
check(np.count_nonzero(B)==16,'digit kernel has 16 nonzero Walsh coefficients')
check(any((u^v)!=d for u,v,d in walk),'modular walk is not XOR walk')
for u in range(8):
    for v in range(8):
        check(int(H[:,u]@B@H[:,v])==64*((v-u)%8),f'digit decoded from pair ({u},{v})')
# Arbitrary fixed field: sample only on first visit, store and accumulate all coefficients.
rng=np.random.default_rng(19)
for k in range(8):
    X=rng.integers(-100,101,(8,8)); Y=np.zeros((8,8),int); visited=set(); raw=np.zeros((8,8),int)
    for u,v,d in walk:
        if (u,v) in visited:continue
        visited.add((u,v)); raw[u,v]=X[u,v]; Y+=int(X[u,v])*np.outer(H[:,u],H[:,v])
    check(np.array_equal(raw,X) and np.array_equal(Y,H@X@H),f'pi-addressed streaming transform arbitrary matrix {k}')
    check(np.array_equal(fwht(X.ravel()).reshape(8,8),Y),f'six-stage butterfly agrees {k}')
    check(np.array_equal(H@Y@H,64*X),f'lossless inverse {k}')
    check(int(np.sum(Y*Y))==64*int(np.sum(X*X)),f'Parseval {k}')
# Discounted exact integer ledger; common denominator 8^N.
L=np.zeros((8,8),dtype=object); pnum=0
for u,v,d in walk:
    L*=8; L[u,v]+=1; pnum=8*pnum+d
Y=H@L@H
check(sum(L.ravel())==(8**N-1)//7,'discounted ledger total')
check(sum((D.astype(object)*L).ravel())==pnum,'pi fractional digit value from direct ledger')
check(sum((B.astype(object)*Y).ravel())==64*pnum,'pi value from Walsh spectral ledger')
check(np.array_equal(fwht(L.ravel()).reshape(8,8),Y),'exact FWHT for large-integer pi ledger')
q=3+F(pnum,8**N); check(0<=mp.pi-mp.mpf(q.numerator)/q.denominator<mp.mpf(8)**(-N),'pi truncation error below 8^-332')
# Every ledger cell has base-8 digits 0 or 1; retrieve each position exactly.
Lcopy=L.copy(); reconstructed=[]
for n in range(N):
    bits=Lcopy%8; loc=np.argwhere(bits==1); assert len(loc)==1 and sum(bits.ravel())==1
    u,v=map(int,loc[0]); reconstructed.append((u,v,(v-u)%8));Lcopy//=8
check(reconstructed[::-1]==walk and not np.any(Lcopy),'discounted ledger retains ordered walk exactly')
# Modular shift is block diagonal in Walsh, but not fully diagonal.
C=np.zeros((8,8),int)
for u in range(8):C[(u+1)%8,u]=1
CW=H@C@H
check(np.any(CW-np.diag(np.diag(CW))),'Walsh does not diagonalize modular shift')
blocks=[[0],[1],[2,3],[4,5,6,7]]
check(all(CW[i,j]==0 for a in blocks for b in blocks if a!=b for i in a for j in b),'modular shift preserves dyadic Walsh blocks 1,1,2,4')
# Xor shifts all diagonal in Walsh basis.
for d in range(8):
    X=np.zeros((8,8),int)
    for u in range(8):X[u^d,u]=1
    check(np.array_equal(H@X@H,8*np.diag(H[:,d])),f'XOR shift diagonal {d}')
# Three one-bit butterfly stages for 8; six for 64. Uniform chamber parity mask is 7.
check(np.array_equal(H[7],np.array([(-1)**i.bit_count() for i in range(8)])),'TetA/TetB parity character')
check([sum(i.bit_count()==j for i in range(64)) for j in range(7)]==[1,6,15,20,15,6,1],'six-bit Walsh grade counts')
print(f'{checks}/{checks} assertions passed; previous 5178 recorded checks not rerun.')
fig,ax=plt.subplots(1,3,figsize=(13.2,4.3),layout='constrained')
for a,M,title,cmap in zip(ax,[first,H@counts@H/8,B/64],['First visit at π digit n','Raw count Walsh spectrum','Digit decoder Walsh coefficients'],['viridis','coolwarm','coolwarm']):
    kw={} if a is ax[0] else {'vmin':-max(abs(M.ravel())), 'vmax':max(abs(M.ravel()))}
    im=a.imshow(M,cmap=cmap,**kw);a.set_title(title,fontsize=11);a.set_xticks(range(8));a.set_yticks(range(8));a.set_xlabel('destination / Walsh label');a.set_ylabel('source / Walsh label');fig.colorbar(im,ax=a,shrink=.75)
    for i in range(8):
        for j in range(8):
            if a is ax[0]:a.text(j,i,str(M[i,j]),ha='center',va='center',fontsize=7,color='white' if M[i,j]<185 else 'black')
            elif a is ax[2] and M[i,j]!=0:a.text(j,i,f'{M[i,j]:g}',ha='center',va='center',fontsize=8)
fig.suptitle('π addresses the 64-cell ledger; Walsh resolves its spectral content',fontsize=14)
for ext in ['png','svg']:fig.savefig(P/'figures'/f'41_pi_fwht_ledger.{ext}',dpi=160)
plt.close(fig)
