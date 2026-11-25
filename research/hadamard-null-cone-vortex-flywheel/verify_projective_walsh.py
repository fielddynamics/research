"""Exact six-bit Walsh/projective closure bridge. No physical attenuation inferred."""
from pathlib import Path
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
n=0
def ck(test,label):
 global n
 assert test,label
 n+=1; print('PASS',label)
H=np.array([[(-1)**((i&j).bit_count()) for j in range(64)] for i in range(64)],dtype=np.int64)
def T(k):
 u,v=divmod(k,8);return 8*v+(u^v)
def tr(k):
 u,v=divmod(k,8);return tuple(((u>>i)&1)+2*((v>>i)&1) for i in (2,1,0))
def flag(k):
 a=tr(k);return next(i for i,x in enumerate(a) if x)
# basis (omega,omega^2), multiplication by omega: (u,v)->(v,u^v)
seen=set(); orbits=[]
for k in range(64):
 if k not in seen:
  o=sorted({k,T(k),T(T(k))});orbits.append(o);seen.update(o)
ck(all(T(T(T(k)))==k for k in range(64)),'order-three XOR cycle')
ck(len(seen)==64 and sorted(map(len,orbits))==[1]+[3]*21,'zero and 21 triples')
orbits=[orbits[0]]+sorted(orbits[1:],key=lambda o:(-flag(o[0]),o[0]))
E=np.zeros((64,22),dtype=np.int64)
for i,o in enumerate(orbits):E[o,i]=1
idx=E.argmax(axis=1)
ck(np.array_equal(E.T@E,np.diag([1]+[3]*21)),'orbit indicator basis')
ck(np.array_equal(np.bincount([flag(o[0]) for o in orbits[1:]]),[16,4,1]),'projective flag 16,4,1')
ck(sum(any(u==0 or v==0 or u==v for u,v in map(lambda k:divmod(k,8),o)) for o in orbits[1:])==7,'seven degenerate triples; fourteen Fano orientation triples')
# H commutes with orbit averaging because T^T=T, T^{-1}=T^2; H P_T=P_{T^{-T}} H
M=np.eye(64,dtype=int)[:,[T(k) for k in range(64)]]
Q3=np.eye(64,dtype=int)+M+M@M
ck(np.array_equal(H@M,M.T@H),'Walsh interchanges order-three generator and inverse')
ck(np.array_equal(H@Q3,Q3@H),'Walsh preserves orbit-constant subspace')
ck(np.array_equal(Q3@Q3,3*Q3),'orbit projector exact')
ck(np.trace(Q3)==66,'invariant rank 22')
R=(H@E)[[o[0] for o in orbits],:]
ck(np.array_equal(H@E,E@R),'exact restricted FWHT')
ck(np.array_equal(R@R,64*np.eye(22,dtype=int)),'restricted inverse')
ck(np.array_equal(R[0,1:],np.full(21,3)) and np.all(R[1:,0]==1),'zero-to-projective coupling')
A=(R[1:,1:]+1)//4
ck(np.array_equal(R[1:,1:],4*A-np.ones((21,21),int)),'projective incidence form')
ck(np.array_equal(A,A.T) and np.all((A==0)|(A==1)),'symmetric incidence')
ck(np.all(A.sum(1)==5),'five points on each polar line')
ck(np.array_equal(A@A,4*np.eye(21,dtype=int)+np.ones((21,21),int)),'projective plane incidence square')
# field multiplication in self-dual basis omega,omega^2 (1 field element is encoded 3)
mul=np.array([[0,0,0,0],[0,2,3,1],[0,3,1,2],[0,1,2,3]])
for i,o in enumerate(orbits[1:]):
 a=tr(o[0]);
 for j,p in enumerate(orbits[1:]):
  b=tr(p[0]);s=0
  for x,y in zip(a,b):s^=int(mul[x,y])
  assert A[i,j]==(s==0)
ck(True,'all 441 incidence entries equal GF(4) orthogonality')
Q=E/np.sqrt(np.array([1]+[3]*21))
F=Q.T@H@Q/8
ck(np.allclose(F@F,np.eye(22),atol=1e-14),'normalized quotient orthogonal involution')
ck(np.allclose(np.linalg.eigvalsh(F),[-1]*11+[1]*11),'quotient spectrum 11+11')
ck(np.allclose(F[0,1:],np.sqrt(3)/8),'nonzero sector not closed under FWHT')
B=R[1:,1:]; J=np.ones((21,21),int)
ck(np.array_equal(B@B,64*np.eye(21,dtype=int)-3*J),'21-block squared is not identity')
ck(np.array_equal(B@np.ones(21,int),-np.ones(21,int)),'constant projective mode eigenvalue -1/8 normalized')
ck(np.array_equal((B@B)@(21*np.eye(21,dtype=int)-J),64*(21*np.eye(21,dtype=int)-J)),'20 projective contrasts invariant')
# Canonical simultaneous XOR translation is not preserved by chosen order-three projection.
L=np.eye(64,dtype=int)[:,[8*(u^1)+(v^1) for u in range(8) for v in range(8)]]
ck(not np.array_equal(L@Q3,Q3@L),'origin-selecting orbit symmetry not invariant under joint XOR translations')
# Original Sierpinski flag: choose representatives first nonzero = field 1 (encoded 3).
reps=[next(k for k in o if tr(k)[flag(k)]==3) for o in orbits[1:]]
# reorder within flag by free bits, using contiguous per-coordinate binary order
reps=sorted(reps,key=lambda k:(-flag(k),tr(k)[flag(k)+1:]))
S=np.array([[int((i&j)==j) for j in range(64)] for i in range(64)],int)
Sflag=S[np.ix_(reps,reps)]
for start,size in [(0,1),(1,4),(5,16)]:
 z=Sflag[start:start+size,start:start+size];ref=np.array([[int((i&j)==j) for j in range(size)] for i in range(size)])
 ck(np.array_equal(z,ref),f'flag diagonal Sierpinski block {size}')
ck(not np.array_equal(Sflag,np.diag(np.diag(Sflag))),'restricted Sierpinski has off-diagonal information')
ck(np.all(np.diag(Sflag)==1),'flag trace 21')
# Three block operators, separately chosen signed weights, as upstream.
for s,target in [(-1,13),(0,17),(1,21)]:
 d=np.array([1]+[s]*4+[1]*16)
 ck(d.sum()==target,f'graded trace {target} (specified middle grading)')
 # exact symbolic determinant exponent because triangular, use rational alpha=1/7
 ck(np.count_nonzero(d)==(17 if s==0 else 21),f'graded rank s={s}')
# Pi path coverage: projective orbits vs all addresses.
mp.mp.dps=400; z=mp.pi-3;v=3; addr=set(); classes=set(); hits=[];raw=np.zeros(64,int)
for t in range(1,333):
 z*=8;d=int(z);z-=d;u=v;v=(u+d)%8;k=8*u+v;addr.add(k);classes.add(int(idx[k]));raw[k]+=1;hits.append((t,len(addr),len(classes)))
ck(len(addr)==64 and hits[-2][1]==63,'full pi closure at 332')
t22=next(t for t,a,b in hits if b==22)
ck(np.count_nonzero(E.T@raw)==22,'all orbit classes visited')
ck(not np.array_equal(Q3@raw,3*raw),'raw pi count ledger not orbit-constant')
# Digit kernel cannot be decoded after orbit averaging for arbitrary ledgers.
D=np.array([(v-u)%8 for u in range(8) for v in range(8)])
ck(not np.array_equal(Q3@D,3*D),'projective compression loses generic modular digit read')
print('First all 22 orbit classes:',t22)
print('Restricted spectrum:',np.linalg.eigvalsh(F).round(6))
print(f'{n}/{n} checks passed. Prior 5378 recorded checks not rerun.')
fig,ax=plt.subplots(1,3,figsize=(13.4,4.5),layout='constrained')
im=ax[0].imshow(idx.reshape(8,8),cmap='tab20',vmin=0,vmax=21);ax[0].set_title('64 addresses → 22 orbit classes');ax[0].set_xlabel('destination');ax[0].set_ylabel('source')
for i in range(8):
 for j in range(8):ax[0].text(j,i,str(idx[8*i+j]),ha='center',va='center',fontsize=8,color='black',bbox=dict(facecolor='white',alpha=.55,edgecolor='none',pad=.3))
ax[1].imshow(F,cmap='coolwarm',vmin=-.5,vmax=.5);ax[1].set_title('Normalized quotient Walsh operator');ax[1].set_xlabel('orbit input');ax[1].set_ylabel('orbit output')
for k in [.5,1.5,5.5]:ax[1].axhline(k,color='black',lw=.6);ax[1].axvline(k,color='black',lw=.6)
h=np.array(hits);ax[2].step(h[:,0],h[:,1],where='post',label='all addresses (64)');ax[2].step(h[:,0],h[:,2],where='post',label='orbit classes (22)');ax[2].axvline(t22,ls='--',color='gray');ax[2].set_title(f'π coverage: quotient closes at {t22}');ax[2].set_xlabel('fractional digit index');ax[2].legend(fontsize=8);ax[2].set_ylim(0,68)
fig.suptitle('Projective closure of the six-bit Walsh ledger — algebraic quotient, not physical dynamics',fontsize=13)
for ext in ('png','svg'):fig.savefig(P/'figures'/f'43_projective_walsh.{ext}',dpi=160)
