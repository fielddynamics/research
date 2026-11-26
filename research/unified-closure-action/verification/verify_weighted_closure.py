import numpy as np
from itertools import product
from math import pi
A=list(product(range(4),repeat=3)); n=len(A)
w=np.array([1/32 if b==0 else 1/96 for a,b,c in A]); u=np.ones(n)
cycle={0:0,1:2,2:3,3:1}
M=np.zeros((n,n))
for j,x in enumerate(A): M[A.index(tuple(cycle[i] for i in x)),j]=1
Q=(np.eye(n)+M+M@M)/3
assert np.allclose(w.sum(),1) and np.allclose(Q@w,w)
assert np.isclose(w@w,1/48) and np.isclose((w-u/64)@(w-u/64),1/192)
assert np.linalg.matrix_rank(Q)==22
alpha=7.2973525643e-3; t=np.sqrt(alpha)
P=np.outer(u,w); J=t*np.eye(n)+(1-t)*P; D=np.diag(w)
assert np.allclose(P@P,P) and np.allclose(J@u,u) and np.allclose(w@J,w)
assert np.allclose(D@J,J.T@D) and np.allclose(J@Q,Q@J)
e,V=np.linalg.eigh(Q); V=V[:,e>.5]; s,ld=np.linalg.slogdet(V.T@J@V)
assert s==1 and np.isclose(2*ld,21*np.log(alpha))
h=np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
F=np.kron(np.kron(h,h),h); fw=F@w
assert np.count_nonzero(abs(fw)>1e-12)==4
assert np.isclose(fw[0],1/8) and np.allclose(fw[[4,8,12]],1/24)
# Weighted contraction is equivalent to an orthogonal one after similarity.
W=np.diag(np.sqrt(w)); Jw=W@J@np.diag(1/np.sqrt(w))
assert np.allclose(Jw,Jw.T) and np.allclose(Jw@np.sqrt(w),np.sqrt(w))
# Independent reflected ports give the serial forward transmission probability.
S=np.array([[t,np.sqrt(1-alpha)],[np.sqrt(1-alpha),-t]])
assert np.allclose(S.T@S,np.eye(2))
assert np.isclose(sum(alpha**k*(1-alpha) for k in range(21))+alpha**21,1)
print('All weighted closure checks passed; invariant rank:',len(e[e>.5]),'log probability:',2*ld,'alpha^21:',alpha**21)
